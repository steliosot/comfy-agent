from __future__ import annotations

import types
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Protocol, Tuple


@dataclass
class AttentionCacheEntry:
    model_id: str
    layer_id: str
    step: int
    total_steps: int
    attention_kind: str
    prompt_fingerprint: str
    tensor_shape: Tuple[Any, ...]
    runtime_signature: str
    tensor: Any


@dataclass
class _PatchedLayer:
    layer_id: str
    module: Any
    original_forward: Any


@dataclass
class _AdapterHandle:
    model_obj: Any
    patched_layers: List[_PatchedLayer]


class AttentionReuseAdapterProtocol(Protocol):
    def is_compatible(self, model_obj: Any) -> bool:  # pragma: no cover - protocol
        ...

    def attach(self, model_obj: Any, plugin_runtime: "AttentionReusePlugin") -> Any:  # pragma: no cover - protocol
        ...

    def detach(self, handle: Any) -> None:  # pragma: no cover - protocol
        ...


class AutoModuleAttentionReuseAdapter:
    """
    Dynamic adapter that patches attention-module forwards directly.

    Notes:
    - Never patches model/unet forward globally.
    - Scans model.named_modules() and wraps attention-like modules only.
    - Works for image and video-ish architectures (temporal/transformer/attn).
    """

    _ATTN_MARKERS = (
        "attention",
        "attn",
        "transformer",
        "temporal",
        "crossattn",
        "cross_attention",
        "self_attention",
    )

    def _module_iter(self, model_obj: Any):
        named_modules = getattr(model_obj, "named_modules", None)
        if not callable(named_modules):
            return []
        try:
            return list(named_modules())
        except Exception:
            return []

    def _module_text(self, name: str, module: Any) -> str:
        cls_name = getattr(getattr(module, "__class__", None), "__name__", "")
        return f"{name} {cls_name}".lower()

    def _is_attention_module(self, name: str, module: Any) -> bool:
        text = self._module_text(name, module)
        if not any(marker in text for marker in self._ATTN_MARKERS):
            return False
        forward = getattr(module, "forward", None)
        return callable(forward)

    def is_compatible(self, model_obj: Any) -> bool:
        modules = self._module_iter(model_obj)
        if not modules:
            return False
        for name, module in modules:
            if self._is_attention_module(name, module):
                return True
        return False

    def _classify_attention_kind(self, layer_id: str, module: Any) -> str:
        text = self._module_text(layer_id, module)
        if "cross" in text:
            return "cross_attention"
        if "temporal" in text:
            return "temporal_attention"
        if "transformer" in text:
            return "transformer_attention"
        if "spatial" in text:
            return "spatial_attention"
        return "attention"

    @staticmethod
    def _extract_step_from_call(args: tuple, kwargs: dict, fallback_step: int) -> int:
        # Best effort extraction from commonly used keys in attention/sampler calls.
        for key in ("step", "timestep", "t", "sigma_idx", "iteration", "idx"):
            if key in kwargs:
                try:
                    return int(kwargs[key])
                except Exception:
                    pass

        # Try first scalar-ish positional that looks like a step/timestep.
        for value in args[:3]:
            if isinstance(value, (int, float)):
                try:
                    return int(value)
                except Exception:
                    pass
            item = getattr(value, "item", None)
            if callable(item):
                try:
                    return int(item())
                except Exception:
                    pass

        return int(max(0, fallback_step))

    @staticmethod
    def _first_tensor_like(*values: Any) -> Any:
        stack = list(values)
        while stack:
            value = stack.pop(0)
            if value is None:
                continue
            if hasattr(value, "shape"):
                return value
            if isinstance(value, dict):
                stack.extend(value.values())
                continue
            if isinstance(value, (list, tuple)):
                stack.extend(value)
                continue
        return None

    def attach(self, model_obj: Any, plugin_runtime: "AttentionReusePlugin") -> _AdapterHandle:
        patched_layers: List[_PatchedLayer] = []

        modules = self._module_iter(model_obj)
        if not modules:
            return _AdapterHandle(model_obj=model_obj, patched_layers=[])

        for layer_id, module in modules:
            if not self._is_attention_module(layer_id, module):
                continue

            original_forward = getattr(module, "forward", None)
            if not callable(original_forward):
                continue

            attention_kind = self._classify_attention_kind(layer_id, module)
            internal_counter = {"value": 0}

            def wrapper(*args, __orig=original_forward, __layer_id=str(layer_id), __kind=attention_kind, **kwargs):
                total_steps = int(plugin_runtime._context.get("total_steps") or 0)
                model_id = str(plugin_runtime._context.get("model_id") or "")
                prompt_fingerprint = str(plugin_runtime._context.get("prompt_fingerprint") or "")
                runtime_signature = plugin_runtime._runtime_signature()

                inferred = self._extract_step_from_call(args, kwargs, internal_counter["value"])
                if total_steps > 0:
                    # keep step in a valid range when extracted value is noisy
                    step = max(0, min(inferred, total_steps))
                else:
                    step = max(0, inferred)

                probe = self._first_tensor_like(args, kwargs)
                req_shape = plugin_runtime._shape_signature(probe)

                reused = plugin_runtime.on_attention_request(
                    model_id=model_id,
                    layer_id=__layer_id,
                    step=step,
                    total_steps=total_steps,
                    attention_kind=__kind,
                    prompt_fingerprint=prompt_fingerprint,
                    attention_shape=req_shape,
                    runtime_signature=runtime_signature,
                )
                if reused is not None:
                    internal_counter["value"] = step + 1
                    return reused

                output = __orig(*args, **kwargs)

                plugin_runtime.on_attention_compute(
                    model_id=model_id,
                    layer_id=__layer_id,
                    step=step,
                    total_steps=total_steps,
                    attn_tensor=output,
                    attention_kind=__kind,
                    prompt_fingerprint=prompt_fingerprint,
                    attention_shape=plugin_runtime._shape_signature(output),
                    runtime_signature=runtime_signature,
                )
                internal_counter["value"] = step + 1
                return output

            # assign per-instance wrapper; module.__call__ invokes module.forward(...)
            module.forward = wrapper
            patched_layers.append(_PatchedLayer(layer_id=str(layer_id), module=module, original_forward=original_forward))

        return _AdapterHandle(model_obj=model_obj, patched_layers=patched_layers)

    def detach(self, handle: _AdapterHandle) -> None:
        if handle is None:
            return
        for patch in handle.patched_layers:
            try:
                patch.module.forward = patch.original_forward
            except Exception:
                pass


class AttentionReusePlugin:
    """
    Compatibility-first attention reuse plugin.

    This plugin is optional and safe by default:
    - no adapter => no-op with fallback logs
    - incompatible adapter/model => no-op with fallback logs
    - all failures degrade to normal compute path
    """

    def __init__(self):
        self.enabled = False
        self.threshold = 0.6
        self.cache_device = "cpu"
        self.store_frequency = 2
        self.reuse_layers = ["cross_attention", "temporal_attention", "transformer_attention"]
        self.debug = False

        self.cache: Dict[Tuple[str, str, int, Tuple[Any, ...]], AttentionCacheEntry] = {}
        self.adapter: Optional[AttentionReuseAdapterProtocol] = AutoModuleAttentionReuseAdapter()
        self._adapter_handle: Any = None
        self._attached_model_id: Optional[str] = None

        self._context: Dict[str, Any] = {}
        self._model_type: str = "unknown"
        self._last_fallback_reason: Optional[str] = None
        self._stats_total = {
            "attn_store": 0,
            "attn_reuse": 0,
            "attn_fallback": 0,
        }
        self._stats_run = {
            "attn_store": 0,
            "attn_reuse": 0,
            "attn_fallback": 0,
        }

    def _log(self, text: str) -> None:
        if self.debug:
            print(text)

    @staticmethod
    def _shape_signature(value: Any) -> Tuple[Any, ...]:
        shape = getattr(value, "shape", None)
        if shape is None:
            return tuple()
        try:
            return tuple(int(x) for x in shape)
        except Exception:
            try:
                return tuple(shape)
            except Exception:
                return tuple()

    @staticmethod
    def _normalize_runtime_field(value: Any) -> str:
        if value is None:
            return ""
        if isinstance(value, (list, tuple)):
            return "[" + ",".join(str(v) for v in value) + "]"
        return str(value)

    def _runtime_signature(self) -> str:
        return "|".join(
            [
                f"model_type={self._normalize_runtime_field(self._context.get('model_type'))}",
                f"seed={self._normalize_runtime_field(self._context.get('seed'))}",
                f"frames={self._normalize_runtime_field(self._context.get('frame_count'))}",
                f"scheduler={self._normalize_runtime_field(self._context.get('scheduler'))}",
                f"prompt={self._normalize_runtime_field(self._context.get('prompt_fingerprint'))}",
            ]
        )

    def _detect_model_type(self, model_obj: Any, model_id: str = "") -> str:
        text_parts = [str(model_id or "")]
        cls_name = getattr(getattr(model_obj, "__class__", None), "__name__", "")
        if cls_name:
            text_parts.append(cls_name)

        named_modules = getattr(model_obj, "named_modules", None)
        if callable(named_modules):
            try:
                for idx, (name, module) in enumerate(named_modules()):
                    if idx > 200:
                        break
                    mod_cls = getattr(getattr(module, "__class__", None), "__name__", "")
                    text_parts.append(str(name))
                    text_parts.append(str(mod_cls))
            except Exception:
                pass

        blob = " ".join(text_parts).lower()
        video_markers = ("temporal", "transformer", "ltx", "wan", "video", "dit")
        if any(marker in blob for marker in video_markers):
            return "video"
        return "image"

    def set_adapter(self, adapter: Optional[AttentionReuseAdapterProtocol]) -> None:
        self.adapter = adapter

    def enable(
        self,
        threshold: float = 0.6,
        cache_device: str = "cpu",
        store_frequency: int = 2,
        reuse_layers: Optional[List[str]] = None,
        debug: bool = False,
    ) -> None:
        self.enabled = True
        self.threshold = float(threshold)
        self.cache_device = str(cache_device or "cpu")
        self.store_frequency = max(1, int(store_frequency))
        self.reuse_layers = list(reuse_layers or ["cross_attention", "temporal_attention", "transformer_attention"])
        self.debug = bool(debug)
        self._log("[ATTN ENABLED]")

    def disable(self) -> None:
        self.enabled = False
        self._detach_adapter_safely()

    def clear(self) -> None:
        self.cache.clear()

    def begin_run(self, context: Dict[str, Any]) -> None:
        self._stats_run = {"attn_store": 0, "attn_reuse": 0, "attn_fallback": 0}
        self._context = dict(context or {})

        if not self.enabled:
            return

        model_obj = self._context.get("model_obj")
        model_id = str(self._context.get("model_id") or "")
        self._model_type = self._detect_model_type(model_obj=model_obj, model_id=model_id)
        self._context["model_type"] = self._model_type

        if self.adapter is None:
            self._fallback(reason="no_adapter", step=self._context.get("step", 0), layer_id="n/a")
            return

        if model_obj is None:
            self._fallback(reason="no_model_object", step=self._context.get("step", 0), layer_id="n/a")
            return

        compatible = False
        try:
            compatible = bool(self.adapter.is_compatible(model_obj))
        except Exception:
            compatible = False

        if not compatible:
            self._fallback(reason="incompatible_adapter_or_model", step=self._context.get("step", 0), layer_id="n/a")
            return

        try:
            self._detach_adapter_safely()
            self._adapter_handle = self.adapter.attach(model_obj=model_obj, plugin_runtime=self)
            self._attached_model_id = model_id
        except Exception:
            self._fallback(reason="adapter_attach_failed", step=self._context.get("step", 0), layer_id="n/a")

    def end_run(self) -> None:
        self._detach_adapter_safely()

    def _detach_adapter_safely(self) -> None:
        if self.adapter is None or self._adapter_handle is None:
            self._adapter_handle = None
            self._attached_model_id = None
            return
        try:
            self.adapter.detach(self._adapter_handle)
        except Exception:
            pass
        self._adapter_handle = None
        self._attached_model_id = None

    def run_stats(self) -> Dict[str, int]:
        return dict(self._stats_run)

    def total_stats(self) -> Dict[str, int]:
        return dict(self._stats_total)

    def _inc(self, key: str) -> None:
        self._stats_run[key] += 1
        self._stats_total[key] += 1

    def _safe_tensor_copy(self, tensor: Any) -> Any:
        current = tensor
        detach_fn = getattr(current, "detach", None)
        if callable(detach_fn):
            try:
                current = detach_fn()
            except Exception:
                current = tensor

        if self.cache_device:
            to_fn = getattr(current, "to", None)
            if callable(to_fn):
                try:
                    moved = to_fn(self.cache_device)
                    if moved is not None:
                        current = moved
                except Exception:
                    pass
        return current

    def _normalize_attention_kind(self, attention_kind: Any) -> str:
        return str(attention_kind or "").strip().lower()

    def _normalize_layer_id(self, layer_id: Any) -> str:
        return str(layer_id or "").strip()

    def should_store(
        self,
        *,
        step: int,
        total_steps: int,
        attention_kind: str,
    ) -> bool:
        if not self.enabled:
            return False
        if total_steps <= 0:
            return False
        if step < 0:
            return False
        if (step % max(1, self.store_frequency)) != 0:
            return False
        if (float(step) / float(total_steps)) <= float(self.threshold):
            return False
        normalized_kind = self._normalize_attention_kind(attention_kind)
        allowed = {self._normalize_attention_kind(x) for x in self.reuse_layers}
        return normalized_kind in allowed

    def should_reuse(
        self,
        *,
        model_id: str,
        layer_id: str,
        step: int,
        total_steps: int,
        attention_kind: str,
        prompt_fingerprint: str,
    ) -> bool:
        if not self.enabled:
            return False
        if not self.should_store(step=step, total_steps=total_steps, attention_kind=attention_kind):
            return False
        if not model_id or not layer_id:
            return False
        if not prompt_fingerprint:
            return False
        return True

    def _fallback(self, *, reason: str, step: Any, layer_id: Any) -> None:
        self._last_fallback_reason = str(reason)
        self._inc("attn_fallback")
        self._log(f"[ATTN FALLBACK] step={step} layer={layer_id} reason={reason}")

    def store_attention(
        self,
        *,
        model_id: str,
        layer_id: str,
        step: int,
        total_steps: int,
        attention_kind: str,
        prompt_fingerprint: str,
        attention_tensor: Any,
        attention_shape: Optional[Tuple[Any, ...]] = None,
        runtime_signature: Optional[str] = None,
    ) -> bool:
        if not self.should_store(step=step, total_steps=total_steps, attention_kind=attention_kind):
            return False

        if not model_id or not prompt_fingerprint:
            self._fallback(reason="missing_model_or_prompt_fingerprint", step=step, layer_id=layer_id)
            return False

        shape = tuple(attention_shape or self._shape_signature(attention_tensor))
        signature = str(runtime_signature or self._runtime_signature())
        key = (str(model_id), self._normalize_layer_id(layer_id), int(step), shape)
        entry = AttentionCacheEntry(
            model_id=str(model_id),
            layer_id=self._normalize_layer_id(layer_id),
            step=int(step),
            total_steps=int(total_steps),
            attention_kind=self._normalize_attention_kind(attention_kind),
            prompt_fingerprint=str(prompt_fingerprint),
            tensor_shape=shape,
            runtime_signature=signature,
            tensor=self._safe_tensor_copy(attention_tensor),
        )
        self.cache[key] = entry
        self._inc("attn_store")
        self._log(f"[ATTN STORE] model={self._model_type} step={step} layer={layer_id}")
        return True

    def load_reusable_attention(
        self,
        *,
        model_id: str,
        layer_id: str,
        step: int,
        total_steps: int,
        attention_kind: str,
        prompt_fingerprint: str,
        attention_shape: Optional[Tuple[Any, ...]] = None,
        runtime_signature: Optional[str] = None,
    ) -> Any:
        if not self.should_reuse(
            model_id=model_id,
            layer_id=layer_id,
            step=step,
            total_steps=total_steps,
            attention_kind=attention_kind,
            prompt_fingerprint=prompt_fingerprint,
        ):
            self._fallback(reason="reuse_policy_blocked", step=step, layer_id=layer_id)
            return None

        normalized_layer = self._normalize_layer_id(layer_id)
        model_id = str(model_id)
        prompt_fingerprint = str(prompt_fingerprint)
        requested_shape = tuple(attention_shape or tuple())
        requested_signature = str(runtime_signature or self._runtime_signature())

        candidates: List[AttentionCacheEntry] = []
        for (cached_model_id, cached_layer_id, _, _), entry in self.cache.items():
            if cached_model_id != model_id:
                continue
            if cached_layer_id != normalized_layer:
                continue
            if entry.prompt_fingerprint != prompt_fingerprint:
                continue
            if requested_shape and tuple(entry.tensor_shape) != requested_shape:
                continue
            if entry.runtime_signature != requested_signature:
                continue
            # later-step reuse: only reuse earlier cached steps
            if int(entry.step) >= int(step):
                continue
            candidates.append(entry)

        if not candidates:
            self._fallback(reason="cache_miss_or_shape_mismatch", step=step, layer_id=layer_id)
            return None

        chosen = sorted(candidates, key=lambda e: e.step)[-1]
        self._inc("attn_reuse")
        self._log(f"[ATTN REUSE] model={self._model_type} step={step} layer={layer_id}")
        return chosen.tensor

    # Adapter callback entrypoints
    def on_attention_compute(
        self,
        model_id: str,
        layer_id: str,
        step: int,
        total_steps: int,
        attn_tensor: Any,
        attention_kind: str,
        prompt_fingerprint: str,
        attention_shape: Optional[Tuple[Any, ...]] = None,
        runtime_signature: Optional[str] = None,
    ) -> bool:
        try:
            return self.store_attention(
                model_id=model_id,
                layer_id=layer_id,
                step=step,
                total_steps=total_steps,
                attention_kind=attention_kind,
                prompt_fingerprint=prompt_fingerprint,
                attention_tensor=attn_tensor,
                attention_shape=attention_shape,
                runtime_signature=runtime_signature,
            )
        except Exception:
            self._fallback(reason="store_exception", step=step, layer_id=layer_id)
            return False

    def on_attention_request(
        self,
        model_id: str,
        layer_id: str,
        step: int,
        total_steps: int,
        attention_kind: str,
        prompt_fingerprint: str,
        attention_shape: Optional[Tuple[Any, ...]] = None,
        runtime_signature: Optional[str] = None,
    ) -> Any:
        try:
            return self.load_reusable_attention(
                model_id=model_id,
                layer_id=layer_id,
                step=step,
                total_steps=total_steps,
                attention_kind=attention_kind,
                prompt_fingerprint=prompt_fingerprint,
                attention_shape=attention_shape,
                runtime_signature=runtime_signature,
            )
        except Exception:
            self._fallback(reason="reuse_exception", step=step, layer_id=layer_id)
            return None
