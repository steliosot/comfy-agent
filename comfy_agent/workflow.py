import copy
import io
import json
import mimetypes
import os
import time
import uuid
from collections import OrderedDict
from pathlib import Path
from urllib.parse import urlencode, urlparse
from urllib import error, request

try:
    import requests
except ImportError:  # pragma: no cover
    class _HTTPError(Exception):
        def __init__(self, message, response=None):
            super().__init__(message)
            self.response = response

    class _Response:
        def __init__(self, payload, status_code=200, text=None, content=None):
            self._payload = payload
            self.status_code = status_code
            self.ok = 200 <= status_code < 300
            self.text = text if text is not None else json.dumps(payload)
            self.content = content if content is not None else self.text.encode("utf-8")

        def json(self):
            return self._payload

        def raise_for_status(self):
            if not self.ok:
                raise _HTTPError(self.text, response=self)

    class _RequestsCompat:
        HTTPError = _HTTPError

        @staticmethod
        def get(url, headers=None, params=None):
            if params:
                separator = "&" if "?" in url else "?"
                url = f"{url}{separator}{urlencode(params)}"
            req = request.Request(
                url,
                headers=headers or {},
                method="GET",
            )
            try:
                with request.urlopen(req) as response:
                    content = response.read()
                    try:
                        payload = json.loads(content.decode("utf-8"))
                    except ValueError:
                        payload = {}
                    return _Response(
                        payload,
                        status_code=response.status,
                        content=content
                    )
            except error.HTTPError as exc:
                body = exc.read()
                return _Response(
                    {},
                    status_code=exc.code,
                    text=body.decode("utf-8", errors="replace"),
                    content=body
                )

        @staticmethod
        def post(url, json=None, headers=None, data=None, files=None):
            payload = data
            merged_headers = {}
            if headers:
                merged_headers.update(headers)
            if json is not None:
                payload = __import__("json").dumps(json).encode("utf-8")
                merged_headers["Content-Type"] = "application/json"
            elif files:
                field_name, file_spec = next(iter(files.items()))
                filename, file_obj, content_type = file_spec
                file_data = file_obj.read()
                boundary = f"----comfy-agent-{uuid.uuid4().hex}"
                merged_headers["Content-Type"] = f"multipart/form-data; boundary={boundary}"
                parts = []
                if isinstance(data, dict):
                    for key, value in data.items():
                        parts.extend(
                            [
                                f"--{boundary}".encode("utf-8"),
                                f'Content-Disposition: form-data; name="{key}"'.encode("utf-8"),
                                b"",
                                str(value).encode("utf-8"),
                            ]
                        )
                parts.extend(
                    [
                        f"--{boundary}".encode("utf-8"),
                        (
                            f'Content-Disposition: form-data; name="{field_name}"; '
                            f'filename="{filename}"'
                        ).encode("utf-8"),
                        f"Content-Type: {content_type}".encode("utf-8"),
                        b"",
                        file_data,
                        f"--{boundary}--".encode("utf-8"),
                        b"",
                    ]
                )
                payload = b"\r\n".join(parts)
            req = request.Request(
                url,
                data=payload,
                headers=merged_headers,
                method="POST",
            )
            try:
                with request.urlopen(req) as response:
                    raw = response.read()
                    try:
                        parsed = __import__("json").loads(raw.decode("utf-8"))
                    except ValueError:
                        parsed = {}
                    return _Response(parsed, status_code=response.status, content=raw)
            except error.HTTPError as exc:
                body = exc.read().decode("utf-8")
                try:
                    payload = __import__("json").loads(body)
                except ValueError:
                    payload = {}
                return _Response(payload, status_code=exc.code, text=body, content=body.encode("utf-8"))

    requests = _RequestsCompat()

from .node import Node
from .refs import DataRef, NodeResult
from .config import ComfyConfig
from .cache_utils import hash_node, hash_value
from .model_manager import get_default_model_manager
from .attention_reuse_plugin import AttentionReusePlugin


class Workflow:
    """Spark-style lazy DAG builder for ComfyUI"""

    def __init__(self, comfy_url=None, server=None, headers=None, api_prefix=None, model_manager=None):
        cfg = ComfyConfig.from_env(load_env=True)
        base_url = server or comfy_url or cfg.server
        if not base_url:
            base_url = "http://127.0.0.1:8000"
        base_url = self._normalize_base_url(base_url)

        self.base_url = base_url.rstrip("/")
        self.headers = dict(headers if headers is not None else cfg.headers)

        env_api_prefix = cfg.api_prefix
        if api_prefix is None:
            api_prefix = env_api_prefix

        normalized_prefix = (api_prefix or "").strip()
        if normalized_prefix and not normalized_prefix.startswith("/"):
            normalized_prefix = f"/{normalized_prefix}"
        normalized_prefix = normalized_prefix.rstrip("/")

        candidates = []
        if normalized_prefix:
            candidates.append(f"{self.base_url}{normalized_prefix}")
        candidates.append(self.base_url)
        if not normalized_prefix:
            candidates.append(f"{self.base_url}/api")

        seen = set()
        ordered_candidates = []
        for candidate in candidates:
            if candidate not in seen:
                seen.add(candidate)
                ordered_candidates.append(candidate)

        last_response = None
        self.url = None
        for candidate in ordered_candidates:
            response = requests.get(f"{candidate}/object_info", headers=self.headers)
            last_response = response
            if response.ok:
                self.url = candidate
                self.registry = response.json()
                break

        if self.url is None:
            if last_response is not None:
                last_response.raise_for_status()
            raise RuntimeError("Unable to connect to ComfyUI /object_info endpoint")

        self.nodes = []
        self.next_id = 1
        self._last_checkpoint = None
        self.last_prompt_id = None
        self.cache_enabled = False
        self.memoization_enabled = False
        self.cache_policy = "FULL"
        self.cache_size = None
        self.cache = {}
        self.execution_state = {}
        self._last_run_signature = None
        self._last_run_result = None
        self.model_manager = model_manager or get_default_model_manager()
        self._active_checkpoint_model_object = None
        self._active_checkpoint_name = None
        self.attention_reuse_plugin = AttentionReusePlugin()
        self.attn_reuse_threshold = 0.6
        self.attn_cache_device = "cpu"
        self.attn_store_frequency = 2
        self.attn_reuse_layers = ["cross_attention"]
        self._reset_pipeline_state()
        print("Loaded nodes:", len(self.registry), "via", self.url)

    @staticmethod
    def _normalize_base_url(base_url):
        base_url = str(base_url).strip()
        if "://" in base_url:
            parsed = urlparse(base_url)
            if parsed.scheme:
                return base_url
        return f"http://{base_url}"

    def _resolve(self, value):
        if isinstance(value, DataRef):
            # Comfy API link format
            return [str(value.node_id), int(value.output_index)]

        if isinstance(value, NodeResult):
            return self._resolve(value.primary())

        if isinstance(value, list):
            return [self._resolve(v) for v in value]

        if isinstance(value, tuple):
            return [self._resolve(v) for v in value]

        if isinstance(value, dict):
            return {k: self._resolve(v) for k, v in value.items()}

        return value

    def _add_node(self, class_type, **kwargs):
        alias = kwargs.pop("__alias", None)
        kwargs = self._prepare_inputs(class_type, kwargs)

        node_id = str(self.next_id)
        self.next_id += 1

        # store inputs lazily (do not resolve DataRef yet)
        node = Node(node_id, class_type, kwargs, alias=alias)
        self.nodes.append(node)

        # inspect outputs from Comfy registry
        node_info = self.registry.get(class_type, {})
        outputs = node_info.get("output", [])
        output_names = node_info.get("output_name", outputs)

        # create DataRef objects for each output
        refs = tuple(DataRef(node_id, i) for i in range(len(outputs)))
        normalized_names = tuple(
            self._normalize_output_name(name, i) for i, name in enumerate(output_names)
        )

        if len(refs) == 0:
            return None

        result = NodeResult(refs, normalized_names)

        if class_type == "CheckpointLoaderSimple":
            self._last_checkpoint = result

        return result

    def _prepare_inputs(self, class_type, kwargs):
        prepared = dict(kwargs)

        if class_type == "CLIPTextEncode":
            if "clip" not in prepared and self._last_checkpoint is not None:
                prepared["clip"] = self._last_checkpoint.CLIP

        if class_type in {"VAEEncode", "VAEDecode"}:
            if "vae" not in prepared and self._last_checkpoint is not None:
                prepared["vae"] = self._last_checkpoint.VAE

        if class_type == "KSampler":
            if "model" not in prepared and self._last_checkpoint is not None:
                prepared["model"] = self._last_checkpoint.MODEL

            if "negative" not in prepared and self._last_checkpoint is not None:
                negative = self._add_node(
                    "CLIPTextEncode",
                    clip=self._last_checkpoint.CLIP,
                    text=""
                )
                prepared["negative"] = negative.CONDITIONING

            prepared.setdefault("seed", 1)
            prepared.setdefault("steps", 20)
            prepared.setdefault("cfg", 7.0)
            prepared.setdefault("sampler_name", "euler")
            prepared.setdefault("scheduler", "normal")
            prepared.setdefault("denoise", 1.0)

        return prepared

    def _reset_pipeline_state(self):
        self._current_checkpoint = None
        self._current_model = None
        self._current_clip = None
        self._current_vae = None
        self._current_positive = None
        self._current_negative = None
        self._current_latent = None
        self._current_image = None
        self._current_mask = None
        self._current_prompt_text = ""
        self._current_negative_text = ""
        self._current_sample_steps = 20

    def checkpoint(self, ckpt_name):
        self._active_checkpoint_model_object = self.model_manager.get_model(str(ckpt_name))
        self._active_checkpoint_name = str(ckpt_name)
        checkpoint = self._add_node(
            "CheckpointLoaderSimple",
            __alias="checkpoint",
            ckpt_name=ckpt_name,
        )
        self._current_checkpoint = checkpoint
        self._current_model = checkpoint.MODEL
        self._current_clip = checkpoint.CLIP
        self._current_vae = checkpoint.VAE
        return self

    def set_model_manager(self, model_manager):
        self.model_manager = model_manager
        return self

    def configure_model_manager(self, max_models_in_vram=None, enable_cpu_offload=None):
        manager = self.model_manager or get_default_model_manager()
        if max_models_in_vram is not None:
            manager.max_models_in_vram = max(1, int(max_models_in_vram))
            manager._evict_if_needed()
        if enable_cpu_offload is not None:
            manager.enable_cpu_offload = bool(enable_cpu_offload)
        self.model_manager = manager
        return self

    def set_attention_reuse_adapter(self, adapter):
        self.attention_reuse_plugin.set_adapter(adapter)
        return self

    def enable_attention_reuse(
        self,
        threshold=0.6,
        cache_device="cpu",
        store_frequency=2,
        reuse_layers=None,
        debug=False,
    ):
        self.attn_reuse_threshold = float(threshold)
        self.attn_cache_device = str(cache_device or "cpu")
        self.attn_store_frequency = max(1, int(store_frequency))
        self.attn_reuse_layers = list(reuse_layers or ["cross_attention"])
        self.attention_reuse_plugin.enable(
            threshold=self.attn_reuse_threshold,
            cache_device=self.attn_cache_device,
            store_frequency=self.attn_store_frequency,
            reuse_layers=self.attn_reuse_layers,
            debug=bool(debug),
        )
        return self

    def disable_attention_reuse(self):
        self.attention_reuse_plugin.disable()
        return self

    def lora(self, lora_name, strength=1.0):
        if self._current_model is None:
            raise RuntimeError("Call .checkpoint(...) before .lora(...)")

        model = self._add_node(
            "LoraLoaderModelOnly",
            __alias="lora",
            model=self._current_model,
            lora_name=lora_name,
            strength_model=strength,
        )
        self._current_model = model.MODEL
        return self

    def prompt(self, text):
        if self._current_clip is None:
            raise RuntimeError("Call .checkpoint(...) before .prompt(...)")

        conditioning = self._add_node(
            "CLIPTextEncode",
            __alias="prompt",
            clip=self._current_clip,
            text=text,
        )
        self._current_positive = conditioning.CONDITIONING
        self._current_prompt_text = str(text)
        return self

    def negative(self, text):
        if self._current_clip is None:
            raise RuntimeError("Call .checkpoint(...) before .negative(...)")

        conditioning = self._add_node(
            "CLIPTextEncode",
            __alias="negative",
            clip=self._current_clip,
            text=text,
        )
        self._current_negative = conditioning.CONDITIONING
        self._current_negative_text = str(text)
        return self

    def latent(self, width, height, batch_size=1):
        latent = self._add_node(
            "EmptyLatentImage",
            __alias="latent",
            width=width,
            height=height,
            batch_size=batch_size,
        )
        self._current_latent = latent.LATENT
        return self

    def load_image(self, image):
        result = self._add_node("LoadImage", __alias="load_image", image=image)
        self._current_image = result.IMAGE
        if hasattr(result, "MASK"):
            self._current_mask = result.MASK
        return self

    def crop(self, x, y, width, height):
        if self._current_image is None:
            raise RuntimeError("Call .load_image(...) before .crop(...)")

        cropped = self._add_node(
            "ImageCrop",
            __alias="crop",
            image=self._current_image,
            x=x,
            y=y,
            width=width,
            height=height,
        )
        self._current_image = cropped.IMAGE
        return self

    def encode(self):
        if self._current_image is None:
            raise RuntimeError("Call .load_image(...) before .encode()")
        if self._current_vae is None:
            raise RuntimeError("Call .checkpoint(...) before .encode()")

        latent = self._add_node(
            "VAEEncode",
            __alias="encode",
            pixels=self._current_image,
            vae=self._current_vae,
        )
        self._current_latent = latent.LATENT
        return self

    def sample(
        self,
        seed=1,
        steps=20,
        cfg=7.0,
        sampler_name="euler",
        scheduler="normal",
        denoise=1.0,
    ):
        if self._current_model is None:
            raise RuntimeError("Call .checkpoint(...) before .sample()")
        if self._current_positive is None:
            raise RuntimeError("Call .prompt(...) before .sample()")
        if self._current_latent is None:
            raise RuntimeError("Call .latent(...) or .encode() before .sample()")

        negative = self._current_negative
        if negative is None:
            negative = self._add_node(
                "CLIPTextEncode",
                __alias="negative",
                clip=self._current_clip,
                text="",
            ).CONDITIONING
            self._current_negative = negative

        sample = self._add_node(
            "KSampler",
            __alias="ksampler",
            model=self._current_model,
            positive=self._current_positive,
            negative=negative,
            latent_image=self._current_latent,
            seed=seed,
            steps=steps,
            cfg=cfg,
            sampler_name=sampler_name,
            scheduler=scheduler,
            denoise=denoise,
        )
        self._current_latent = sample.LATENT
        self._current_sample_steps = int(steps)
        return self

    def decode(self):
        if self._current_latent is None:
            raise RuntimeError("Call .sample(...) or .encode() before .decode()")
        if self._current_vae is None:
            raise RuntimeError("Call .checkpoint(...) before .decode()")

        image = self._add_node(
            "VAEDecode",
            __alias="decode",
            samples=self._current_latent,
            vae=self._current_vae,
        )
        self._current_image = image.IMAGE
        return self

    def preview(self):
        if self._current_image is None:
            raise RuntimeError("Call .decode() before .preview()")

        self._add_node("PreviewImage", __alias="preview", images=self._current_image)
        return self

    def save(self, filename_prefix):
        if self._current_image is None:
            raise RuntimeError("Call .decode() before .save(...)")

        self._add_node(
            "SaveImage",
            __alias="save",
            images=self._current_image,
            filename_prefix=filename_prefix,
        )
        return self

    def save_animated_webp(
        self,
        filename_prefix,
        fps=6,
        lossless=False,
        quality=80,
        method="default",
    ):
        if self._current_image is None:
            raise RuntimeError("Call .decode() before .save_animated_webp(...)")

        self._add_node(
            "SaveAnimatedWEBP",
            __alias="save_animated_webp",
            images=self._current_image,
            filename_prefix=filename_prefix,
            fps=fps,
            lossless=lossless,
            quality=quality,
            method=method,
        )
        return self

    def clone(self):
        cloned = self.__class__.__new__(self.__class__)
        for key, value in self.__dict__.items():
            setattr(cloned, key, copy.deepcopy(value))
        return cloned

    def override(self, overrides):
        for path, value in overrides.items():
            selector, input_name = path.rsplit(".", 1)
            node = self._find_node(selector)
            if input_name not in node.inputs:
                raise KeyError(f"Node '{selector}' has no input '{input_name}'")
            node.inputs[input_name] = value
        return self

    def inspect(self, print_output=True):
        lines = []
        for index, node in enumerate(self.nodes):
            outputs = self._output_names(node.class_type)
            label = node.alias or self._normalize_node_name(node.class_type)
            if outputs:
                lines.append(
                    f"{index}. {node.class_type} [{label}] -> {', '.join(outputs)}"
                )
            else:
                lines.append(f"{index}. {node.class_type} [{label}]")

        summary = "\n".join(lines)
        if print_output:
            print(summary)
        return summary

    def to_json(self, indent=2):
        return json.dumps(self._build_dag(), indent=indent)

    def then(self, other):
        combined = self.clone()
        mapping = {}

        for node in other.nodes:
            new_id = str(combined.next_id)
            combined.next_id += 1
            mapping[node.node_id] = new_id

            combined.nodes.append(
                Node(
                    new_id,
                    node.class_type,
                    combined._remap_value(copy.deepcopy(node.inputs), mapping),
                    alias=node.alias,
                )
            )

        combined._remap_pipeline_state_from(other, mapping)
        return combined

    def _normalize_output_name(self, name, index):
        if not name:
            return f"OUTPUT_{index}"

        normalized = []
        previous_was_separator = False

        for char in str(name):
            if char.isalnum():
                normalized.append(char.upper())
                previous_was_separator = False
            elif not previous_was_separator:
                normalized.append("_")
                previous_was_separator = True

        result = "".join(normalized).strip("_")
        if not result:
            result = f"OUTPUT_{index}"
        if result[0].isdigit():
            result = f"OUTPUT_{result}"
        return result

    def _normalize_node_name(self, name):
        normalized = []
        previous_upper = False

        for char in name:
            if char.isupper() and normalized and not previous_upper:
                normalized.append("_")
            normalized.append(char.lower())
            previous_upper = char.isupper()

        return "".join(normalized)

    def _output_names(self, class_type):
        node_info = self.registry.get(class_type, {})
        names = node_info.get("output_name") or node_info.get("output") or []
        return [self._normalize_output_name(name, index) for index, name in enumerate(names)]

    def _find_node(self, selector):
        index = None
        if selector.endswith("]") and "[" in selector:
            selector, raw_index = selector[:-1].split("[", 1)
            index = int(raw_index)

        matches = []
        normalized_selector = selector.lower()

        for node in self.nodes:
            alias = (node.alias or "").lower()
            class_name = self._normalize_node_name(node.class_type)
            candidates = {alias, class_name, node.class_type.lower()}
            if normalized_selector in candidates:
                matches.append(node)
                continue

            if alias and alias.startswith(normalized_selector):
                matches.append(node)
                continue

            if class_name.startswith(normalized_selector):
                matches.append(node)

        if not matches:
            raise KeyError(f"No node matched selector '{selector}'")

        if index is None:
            return matches[-1]

        try:
            return matches[index]
        except IndexError as exc:
            raise IndexError(f"Selector '{selector}' has no match at index {index}") from exc

    def _remap_value(self, value, mapping):
        if isinstance(value, DataRef):
            return DataRef(mapping[value.node_id], value.output_index)
        if isinstance(value, NodeResult):
            refs = tuple(self._remap_value(ref, mapping) for ref in value)
            return NodeResult(refs, value._output_names)
        if isinstance(value, list):
            return [self._remap_value(v, mapping) for v in value]
        if isinstance(value, tuple):
            return tuple(self._remap_value(v, mapping) for v in value)
        if isinstance(value, dict):
            return {k: self._remap_value(v, mapping) for k, v in value.items()}
        return value

    def _remap_pipeline_state_from(self, other, mapping):
        state_fields = [
            "_current_checkpoint",
            "_current_model",
            "_current_clip",
            "_current_vae",
            "_current_positive",
            "_current_negative",
            "_current_latent",
            "_current_image",
            "_current_mask",
            "_last_checkpoint",
        ]

        for field in state_fields:
            value = getattr(other, field)
            setattr(self, field, self._remap_value(copy.deepcopy(value), mapping) if value is not None else None)

    def __getattr__(self, name):
        for node_name in self.registry:
            if node_name.lower() == name.lower():
                def wrapper(**kwargs):
                    return self._add_node(node_name, **kwargs)
                return wrapper
        raise AttributeError(name)

    def node(self, name, **kwargs):
        return self._add_node(name, **kwargs)

    def _build_dag(self):
        return self._build_dag_subset(include_node_ids=None)

    def _build_dag_subset(self, include_node_ids=None):
        include_set = set(include_node_ids) if include_node_ids is not None else None
        dag = {}
        for node in self.nodes:
            if include_set is not None and node.node_id not in include_set:
                continue
            dag[node.node_id] = {
                "class_type": node.class_type,
                "inputs": {k: self._resolve(v) for k, v in node.inputs.items()},
            }
        return dag

    def validate(self):
        if not self.nodes:
            raise RuntimeError("Workflow is empty")

        produced = set()

        for node in self.nodes:
            for value in node.inputs.values():
                self._validate_refs(value, produced)
            produced.add(node.node_id)

        print("Workflow validation passed")

    def _validate_refs(self, value, produced):
        if isinstance(value, DataRef):
            if value.node_id not in produced:
                raise RuntimeError(
                    f"Invalid reference: node {value.node_id} not defined before use"
                )
            return

        if isinstance(value, NodeResult):
            self._validate_refs(value.primary(), produced)
            return

        if isinstance(value, (list, tuple)):
            for v in value:
                self._validate_refs(v, produced)
            return

        if isinstance(value, dict):
            for v in value.values():
                self._validate_refs(v, produced)

    def enable_cache(self, policy="FULL", size=None):
        normalized = str(policy or "FULL").strip().upper()
        if normalized not in {"FULL", "LRU"}:
            raise ValueError("cache policy must be FULL or LRU")
        self.cache_enabled = True
        self.cache_policy = normalized
        self.cache_size = int(size) if size is not None else None
        if self.cache_policy == "LRU":
            if not isinstance(self.cache, OrderedDict):
                self.cache = OrderedDict(self.cache)
        elif isinstance(self.cache, OrderedDict):
            self.cache = dict(self.cache)
        return self

    def disable_cache(self):
        self.cache_enabled = False
        return self

    def enable_memoization(self):
        self.memoization_enabled = True
        return self

    def disable_memoization(self):
        self.memoization_enabled = False
        return self

    def clear_cache(self):
        self.cache.clear()
        self.execution_state.clear()
        self._last_run_signature = None
        self._last_run_result = None
        self.attention_reuse_plugin.clear()
        return self

    def _cache_get(self, key):
        if key not in self.cache:
            return None
        if self.cache_policy == "LRU" and isinstance(self.cache, OrderedDict):
            self.cache.move_to_end(key)
        return self.cache[key]

    def _cache_put(self, key, value):
        if self.cache_policy == "LRU":
            if not isinstance(self.cache, OrderedDict):
                self.cache = OrderedDict(self.cache)
            self.cache[key] = value
            self.cache.move_to_end(key)
            if self.cache_size is not None and self.cache_size > 0:
                while len(self.cache) > self.cache_size:
                    self.cache.popitem(last=False)
            return

        self.cache[key] = value
        if self.cache_size is not None and self.cache_size > 0 and len(self.cache) > self.cache_size:
            # Keep behavior simple for FULL policy with optional cap.
            for stale_key in list(self.cache.keys())[:-self.cache_size]:
                self.cache.pop(stale_key, None)

    def _collect_ref_node_ids(self, value, out):
        if isinstance(value, DataRef):
            out.add(str(value.node_id))
            return
        if isinstance(value, NodeResult):
            for ref in value:
                self._collect_ref_node_ids(ref, out)
            return
        if isinstance(value, (list, tuple)):
            for item in value:
                self._collect_ref_node_ids(item, out)
            return
        if isinstance(value, dict):
            for item in value.values():
                self._collect_ref_node_ids(item, out)

    def _resolve_target_nodes(self, target):
        if target is None:
            return [node.node_id for node in self.nodes]

        if isinstance(target, Node):
            return [target.node_id]

        if isinstance(target, (list, tuple, set)):
            resolved = []
            for item in target:
                resolved.extend(self._resolve_target_nodes(item))
            unique = []
            seen = set()
            for node_id in resolved:
                if node_id not in seen:
                    seen.add(node_id)
                    unique.append(node_id)
            return unique

        if isinstance(target, int):
            target = str(target)

        if isinstance(target, str):
            text = target.strip()
            if not text:
                raise ValueError("target selector must not be empty")
            if text.isdigit():
                node_id = str(int(text))
                node = next((n for n in self.nodes if n.node_id == node_id), None)
                if node is None:
                    raise KeyError(f"No node with id '{node_id}'")
                return [node_id]
            node = self._find_node(text)
            return [node.node_id]

        raise TypeError("target must be None, selector string, node id, Node, or list of selectors")

    def _ancestor_closure(self, target_node_ids):
        node_by_id = {node.node_id: node for node in self.nodes}
        closure = set()
        stack = [str(node_id) for node_id in target_node_ids]

        while stack:
            node_id = stack.pop()
            if node_id in closure:
                continue
            closure.add(node_id)
            node = node_by_id.get(node_id)
            if node is None:
                continue
            refs = set()
            for value in node.inputs.values():
                self._collect_ref_node_ids(value, refs)
            for ref_id in refs:
                if ref_id not in closure:
                    stack.append(ref_id)

        ordered = [node.node_id for node in self.nodes if node.node_id in closure]
        return ordered

    def _compute_signatures(self):
        signatures = {}
        for node in self.nodes:
            upstream_ids = set()
            for value in node.inputs.values():
                self._collect_ref_node_ids(value, upstream_ids)
            upstream_signatures = [
                {"node_id": upstream_id, "signature": signatures.get(upstream_id)}
                for upstream_id in sorted(upstream_ids)
            ]
            signatures[node.node_id] = hash_node(
                class_type=node.class_type,
                inputs=node.inputs,
                upstream_signatures=upstream_signatures,
            )
        return signatures

    def _attention_runtime_hints(self):
        seed = None
        frame_count = None
        scheduler = None

        # Prefer explicit sampler/sequencer-like nodes.
        for node in self.nodes:
            class_name = str(node.class_type or "").lower()
            inputs = node.inputs if isinstance(node.inputs, dict) else {}

            if seed is None:
                for key in ("seed", "noise_seed"):
                    if key in inputs and isinstance(inputs.get(key), (int, float)):
                        seed = int(inputs.get(key))
                        break

            if scheduler is None:
                for key in ("scheduler", "sampler_name", "sampler"):
                    value = inputs.get(key)
                    if isinstance(value, str) and value.strip():
                        scheduler = value.strip()
                        break

            if frame_count is None:
                for key in ("length", "frame_count", "frames", "num_frames"):
                    value = inputs.get(key)
                    if isinstance(value, (int, float)):
                        frame_count = int(value)
                        break

            if seed is not None and frame_count is not None and scheduler is not None:
                break

        return {
            "seed": seed,
            "frame_count": frame_count,
            "scheduler": scheduler,
        }

    def run(self, target=None, debug=False):
        if isinstance(target, bool) and debug is False:
            # Backward compatibility with historical positional style run(True).
            debug = target
            target = None

        attn_hints = self._attention_runtime_hints()
        run_context = {
            "model_id": str(self._active_checkpoint_name or ""),
            "model_obj": self._active_checkpoint_model_object,
            "prompt_fingerprint": hash_value(
                {
                    "prompt": self._current_prompt_text,
                    "negative": self._current_negative_text,
                }
            ),
            "total_steps": int(self._current_sample_steps or 0),
            "seed": attn_hints.get("seed"),
            "frame_count": attn_hints.get("frame_count"),
            "scheduler": attn_hints.get("scheduler"),
        }
        self.attention_reuse_plugin.begin_run(run_context)

        try:
            self.validate()
            target_ids = self._resolve_target_nodes(target)
            closure_ids = self._ancestor_closure(target_ids)
            closure_set = set(closure_ids)
            signatures = self._compute_signatures()

            trace = []
            execute_required = set()
            unchanged = set()
            skipped_by_target = set()

            for node in self.nodes:
                node_id = node.node_id
                if node_id not in closure_set:
                    skipped_by_target.add(node_id)
                    trace.append(
                        {"event": "skip", "node_id": node_id, "class_type": node.class_type, "reason": "outside_target"}
                    )
                    continue

                signature = signatures[node_id]
                previous = self.execution_state.get(node_id, {})
                previous_signature = previous.get("signature")
                in_cache = self._cache_get(signature) is not None if self.cache_enabled else False

                if self.cache_enabled and previous_signature == signature and in_cache:
                    unchanged.add(node_id)
                    trace.append({"event": "cache_hit", "node_id": node_id, "class_type": node.class_type})
                else:
                    execute_required.add(node_id)
                    if self.cache_enabled:
                        trace.append(
                            {
                                "event": "cache_miss",
                                "node_id": node_id,
                                "class_type": node.class_type,
                                "reason": "signature_changed_or_missing",
                            }
                        )
                    trace.append({"event": "execute", "node_id": node_id, "class_type": node.class_type})

            run_signature_payload = {
                "target": target_ids,
                "closure": closure_ids,
                "signatures": [signatures[node_id] for node_id in closure_ids],
            }
            run_signature = hash_value(run_signature_payload)

            if (
                self.cache_enabled
                and self.memoization_enabled
                and not execute_required
                and self._last_run_signature == run_signature
                and self._last_run_result is not None
            ):
                result = copy.deepcopy(self._last_run_result)
                metrics = self._trace_metrics(trace)
                metrics.update(self.attention_reuse_plugin.run_stats())
                if debug:
                    for item in trace:
                        if item["event"] == "cache_hit":
                            print(f"[CACHE HIT] {item['class_type']}#{item['node_id']}")
                        elif item["event"] == "cache_miss":
                            print(f"[CACHE MISS] {item['class_type']}#{item['node_id']}")
                        elif item["event"] == "skip":
                            print(f"[SKIP] {item['class_type']}#{item['node_id']} (outside target)")
                    print("[CACHE HIT] WORKFLOW")
                    result["execution_trace"] = trace
                result["execution_metrics"] = metrics
                return result

            dag = self._build_dag_subset(include_node_ids=closure_ids)

            payload = {
                "prompt": dag,
                "client_id": str(uuid.uuid4())
            }

            if debug:
                for item in trace:
                    if item["event"] == "execute":
                        print(f"[EXECUTE] {item['class_type']}#{item['node_id']}")
                    elif item["event"] == "cache_hit":
                        print(f"[CACHE HIT] {item['class_type']}#{item['node_id']}")
                    elif item["event"] == "cache_miss":
                        print(f"[CACHE MISS] {item['class_type']}#{item['node_id']}")
                    elif item["event"] == "skip":
                        print(f"[SKIP] {item['class_type']}#{item['node_id']} (outside target)")
                print(json.dumps(payload, indent=2))

            r = requests.post(f"{self.url}/prompt", json=payload, headers=self.headers)
            if not r.ok:
                message = f"ComfyUI prompt request failed with {r.status_code}"
                try:
                    detail = r.json()
                    message += f": {json.dumps(detail, indent=2)}"
                except ValueError:
                    message += f": {r.text}"
                raise requests.HTTPError(message, response=r)
            result = r.json()
            self.last_prompt_id = result.get("prompt_id")
            metrics = self._trace_metrics(trace)
            metrics.update(self.attention_reuse_plugin.run_stats())
            result = dict(result)
            result["execution_metrics"] = metrics
            if debug:
                result["execution_trace"] = trace

            for node_id in closure_ids:
                signature = signatures[node_id]
                state = self.execution_state.get(node_id, {})
                state["signature"] = signature
                state["last_run_marker"] = run_signature
                state["output"] = self._cache_get(signature) if self.cache_enabled else None
                self.execution_state[node_id] = state
                if self.cache_enabled:
                    self._cache_put(
                        signature,
                        {
                            "node_id": node_id,
                            "class_type": next(n.class_type for n in self.nodes if n.node_id == node_id),
                        },
                    )

            if self.cache_enabled:
                self._last_run_signature = run_signature
                self._last_run_result = copy.deepcopy(result)

            print(result)
            return result
        finally:
            self.attention_reuse_plugin.end_run()

    @staticmethod
    def _trace_metrics(trace):
        executed = 0
        skipped = 0
        cache_hits = 0
        cache_misses = 0
        sampler_runs = 0
        for item in trace:
            event = item.get("event")
            class_type = item.get("class_type")
            if event == "execute":
                executed += 1
                if class_type == "KSampler":
                    sampler_runs += 1
            elif event == "skip":
                skipped += 1
            elif event == "cache_hit":
                cache_hits += 1
            elif event == "cache_miss":
                cache_misses += 1
        return {
            "executed_nodes": executed,
            "skipped_nodes": skipped,
            "cache_hits": cache_hits,
            "cache_misses": cache_misses,
            "sampler_runs": sampler_runs,
        }

    def history(self, prompt_id=None):
        target = prompt_id or self.last_prompt_id
        if not target:
            raise ValueError("prompt_id is required when no run() has been executed")

        response = requests.get(f"{self.url}/history/{target}", headers=self.headers)
        response.raise_for_status()
        return response.json()

    def saved_images(self, prompt_id=None, retries=12, delay=0.5):
        target = prompt_id or self.last_prompt_id
        if not target:
            raise ValueError("prompt_id is required when no run() has been executed")

        for attempt in range(max(1, retries)):
            history = self.history(target)
            entry = history.get(target, history) if isinstance(history, dict) else history
            outputs = entry.get("outputs", {}) if isinstance(entry, dict) else {}

            images = []
            for node_id, node_output in outputs.items():
                for key in ("images", "gifs", "videos", "audio", "audios"):
                    for image in node_output.get(key, []):
                        item = dict(image)
                        item["node_id"] = str(node_id)
                        item["output_kind"] = key
                        images.append(item)

            if images:
                return images

            if attempt < retries - 1:
                time.sleep(delay)

        return []

    def upload_image(self, local_path, remote_name=None, overwrite=True, type="input"):
        path = Path(local_path)
        if not path.exists():
            raise FileNotFoundError(f"Image path not found: {local_path}")
        if not path.is_file():
            raise ValueError(f"Image path must be a file: {local_path}")

        resolved_remote = remote_name or path.name
        mime_type = mimetypes.guess_type(resolved_remote)[0] or "application/octet-stream"

        with path.open("rb") as file_obj:
            response = requests.post(
                f"{self.url}/upload/image",
                files={
                    "image": (resolved_remote, file_obj, mime_type)
                },
                data={
                    "overwrite": "true" if overwrite else "false",
                    "type": type,
                },
                headers=self.headers,
            )
        if not response.ok:
            response.raise_for_status()
        payload = response.json() if hasattr(response, "json") else {}
        filename = payload.get("name", resolved_remote) if isinstance(payload, dict) else resolved_remote
        subfolder = payload.get("subfolder", "") if isinstance(payload, dict) else ""
        image_type = payload.get("type", type) if isinstance(payload, dict) else type

        return {
            "local_path": str(path.resolve()),
            "remote_name": filename,
            "subfolder": subfolder,
            "type": image_type,
            "source": "upload",
        }

    def download_image(self, image_meta, output_path=None, output_dir=None):
        if not isinstance(image_meta, dict):
            raise ValueError("image_meta must be a dict")
        filename = image_meta.get("filename")
        if not filename:
            raise ValueError("image_meta.filename is required")

        params = {
            "filename": filename,
            "subfolder": image_meta.get("subfolder", ""),
            "type": image_meta.get("type", "output"),
        }

        if output_path is None:
            resolved_output_dir = output_dir or ComfyConfig.from_env(load_env=True).output_dir
            out_dir = Path(resolved_output_dir)
            out_dir.mkdir(parents=True, exist_ok=True)
            target_path = out_dir / filename
        else:
            target_path = Path(output_path)
            target_path.parent.mkdir(parents=True, exist_ok=True)

        response = requests.get(
            f"{self.url}/view",
            params=params,
            headers=self.headers
        )
        if not response.ok:
            response.raise_for_status()
        content = getattr(response, "content", None)
        if content is None:
            content = response.text.encode("utf-8")
        target_path.write_bytes(content)

        return {
            "filename": filename,
            "subfolder": params["subfolder"],
            "type": params["type"],
            "downloaded_path": str(target_path.resolve()),
            "source": "download",
            "node_id": image_meta.get("node_id"),
            "output_kind": image_meta.get("output_kind"),
        }

    def download_saved_images(
        self,
        prompt_id,
        output_dir=None,
        filename_strategy=None,
        retries=12,
        delay=0.5,
    ):
        resolved_output_dir = output_dir or ComfyConfig.from_env(load_env=True).output_dir
        images = self.saved_images(prompt_id=prompt_id, retries=retries, delay=delay)
        downloaded = []
        for index, image_meta in enumerate(images, start=1):
            if filename_strategy is not None:
                if callable(filename_strategy):
                    custom_name = filename_strategy(image_meta, index)
                else:
                    custom_name = str(filename_strategy).format(
                        index=index,
                        filename=image_meta.get("filename", ""),
                        node_id=image_meta.get("node_id", ""),
                        output_kind=image_meta.get("output_kind", ""),
                    )
                output_path = str(Path(resolved_output_dir) / custom_name)
            else:
                output_path = None

            downloaded.append(
                self.download_image(
                    image_meta=image_meta,
                    output_path=output_path,
                    output_dir=resolved_output_dir,
                )
            )
        return downloaded

    def transfer_output_to_input(
        self,
        image_meta,
        remote_name=None,
        overwrite=True,
    ):
        if not isinstance(image_meta, dict):
            raise ValueError("image_meta must be a dict")
        filename = image_meta.get("filename")
        if not filename:
            raise ValueError("image_meta.filename is required")

        params = {
            "filename": filename,
            "subfolder": image_meta.get("subfolder", ""),
            "type": image_meta.get("type", "output"),
        }
        response = requests.get(
            f"{self.url}/view",
            params=params,
            headers=self.headers,
        )
        if not response.ok:
            response.raise_for_status()
        content = getattr(response, "content", None)
        if content is None:
            content = response.text.encode("utf-8")

        resolved_remote = remote_name or filename
        mime_type = mimetypes.guess_type(resolved_remote)[0] or "application/octet-stream"
        file_obj = io.BytesIO(content)

        upload_response = requests.post(
            f"{self.url}/upload/image",
            files={"image": (resolved_remote, file_obj, mime_type)},
            data={
                "overwrite": "true" if overwrite else "false",
                "type": "input",
            },
            headers=self.headers,
        )
        if not upload_response.ok:
            upload_response.raise_for_status()
        payload = upload_response.json() if hasattr(upload_response, "json") else {}
        uploaded_name = (
            payload.get("name", resolved_remote) if isinstance(payload, dict) else resolved_remote
        )
        subfolder = payload.get("subfolder", "") if isinstance(payload, dict) else ""
        item_type = payload.get("type", "input") if isinstance(payload, dict) else "input"

        return {
            "source_filename": filename,
            "remote_name": uploaded_name,
            "subfolder": subfolder,
            "type": item_type,
            "source": "server_transfer",
        }
