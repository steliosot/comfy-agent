import time
from collections import OrderedDict
from dataclasses import dataclass
from typing import Any, Callable, Dict, Optional


@dataclass
class _ShimModel:
    """Fallback placeholder model object used by the compatibility shim."""

    name: str
    device: str = "cpu"

    def to(self, device: str):
        self.device = str(device)
        return self


def load_model(model_name: str) -> Any:
    """
    Placeholder disk loader for compatibility mode.
    Integrate with a real local loader if needed.
    """
    return _ShimModel(name=str(model_name), device="cpu")


class ModelManager:
    """
    Compatibility-first model manager:
    - LRU cache over "VRAM" slots
    - optional CPU offload cache
    - lazy loading on first access
    """

    def __init__(
        self,
        max_models_in_vram: int = 1,
        enable_cpu_offload: bool = True,
        loader: Optional[Callable[[str], Any]] = None,
        move_to_cuda: Optional[Callable[[Any], Any]] = None,
        move_to_cpu: Optional[Callable[[Any], Any]] = None,
        logger: Optional[Callable[[str], None]] = None,
    ):
        self.max_models_in_vram = max(1, int(max_models_in_vram))
        self.enable_cpu_offload = bool(enable_cpu_offload)
        self.loader = loader or load_model
        self._move_to_cuda_hook = move_to_cuda
        self._move_to_cpu_hook = move_to_cpu
        self._logger = logger or print

        self.vram_models = OrderedDict()
        self.cpu_models: Dict[str, Any] = {}
        self._stats = {
            "requests": 0,
            "vram_hits": 0,
            "cpu_hits": 0,
            "disk_loads": 0,
            "evictions": 0,
            "evictions_to_cpu": 0,
            "evictions_dropped": 0,
            "total_load_time_s": 0.0,
        }

    def _log(self, message: str) -> None:
        if self._logger is not None:
            self._logger(message)

    def _move_to_device(self, model: Any, device: str) -> Any:
        if device == "cuda" and self._move_to_cuda_hook is not None:
            return self._move_to_cuda_hook(model)
        if device == "cpu" and self._move_to_cpu_hook is not None:
            return self._move_to_cpu_hook(model)

        to_method = getattr(model, "to", None)
        if callable(to_method):
            try:
                moved = to_method(device)
                return model if moved is None else moved
            except Exception:
                return model
        return model

    def _load_from_disk(self, model_name: str) -> Any:
        # integrate with ComfyUI/local model loader when needed
        return self.loader(model_name)

    def _evict_if_needed(self) -> None:
        while len(self.vram_models) > self.max_models_in_vram:
            old_name, old_model = self.vram_models.popitem(last=False)
            self._stats["evictions"] += 1
            if self.enable_cpu_offload:
                moved = self._move_to_device(old_model, "cpu")
                self.cpu_models[old_name] = moved
                self._stats["evictions_to_cpu"] += 1
                self._log(f"[EVICT \u2192 CPU] {old_name}")
            else:
                self._stats["evictions_dropped"] += 1
                del old_model

    def get_model(self, model_name: str) -> Any:
        name = str(model_name)
        self._stats["requests"] += 1

        if name in self.vram_models:
            model = self.vram_models[name]
            self.vram_models.move_to_end(name)
            self._stats["vram_hits"] += 1
            self._log(f"[VRAM HIT] {name}")
            return model

        if name in self.cpu_models:
            model = self.cpu_models.pop(name)
            model = self._move_to_device(model, "cuda")
            self.vram_models[name] = model
            self._stats["cpu_hits"] += 1
            self._log(f"[CPU HIT \u2192 GPU] {name}")
            self._evict_if_needed()
            return model

        started = time.perf_counter()
        model = self._load_from_disk(name)
        self._stats["total_load_time_s"] += (time.perf_counter() - started)
        self._stats["disk_loads"] += 1
        self._log(f"[LOAD DISK] {name}")

        model = self._move_to_device(model, "cuda")
        self.vram_models[name] = model
        self._evict_if_needed()
        return model

    def stats(self) -> Dict[str, Any]:
        snapshot = dict(self._stats)
        snapshot["vram_models"] = list(self.vram_models.keys())
        snapshot["cpu_models"] = list(self.cpu_models.keys())
        snapshot["max_models_in_vram"] = self.max_models_in_vram
        snapshot["enable_cpu_offload"] = self.enable_cpu_offload
        return snapshot


_DEFAULT_MODEL_MANAGER: Optional[ModelManager] = None


def get_default_model_manager() -> ModelManager:
    global _DEFAULT_MODEL_MANAGER
    if _DEFAULT_MODEL_MANAGER is None:
        _DEFAULT_MODEL_MANAGER = ModelManager()
    return _DEFAULT_MODEL_MANAGER

