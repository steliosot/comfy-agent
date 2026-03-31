from typing import Any, Dict

from .model_manager import ModelManager


SUPPORTED_MODES = {
    "none",
    "deterministic_cache",
    "graph_memoization",
    "model_lru",
    "cpu_offload",
    "lazy_loading",
    "attention_reuse",
    "attention_reuse_cpu_offload",
    "attention_reuse_wan21",
    "attention_reuse_wan21_cpu_offload",
    "full_stack",
}


def build_optimization_profile(
    mode: str = "full_stack",
    cache_policy: str = "LRU",
    cache_size: int = 256,
    max_models_in_vram: int = 1,
    enable_cpu_offload: bool = True,
    lazy_loading: bool = True,
    attn_reuse_threshold: float = 0.6,
    attn_cache_device: str = "cpu",
    attn_store_frequency: int = 2,
    attn_reuse_layers=None,
) -> Dict[str, Any]:
    normalized_mode = str(mode or "full_stack").strip().lower()
    if normalized_mode not in SUPPORTED_MODES:
        raise ValueError(
            f"Unsupported optimization mode '{mode}'. "
            f"Supported: {sorted(SUPPORTED_MODES)}"
        )

    profile = {
        "mode": normalized_mode,
        "workflow": {
            "cache_enabled": False,
            "cache_policy": str(cache_policy or "LRU").upper(),
            "cache_size": int(cache_size) if cache_size is not None else None,
            "memoization_enabled": False,
        },
        "model_manager": {
            "enabled": False,
            "max_models_in_vram": max(1, int(max_models_in_vram)),
            "enable_cpu_offload": bool(enable_cpu_offload),
            "lazy_loading": bool(lazy_loading),
        },
        "attention_reuse": {
            "enabled": False,
            "threshold": float(attn_reuse_threshold),
            "cache_device": str(attn_cache_device or "cpu"),
            "store_frequency": max(1, int(attn_store_frequency)),
            "reuse_layers": list(attn_reuse_layers or ["cross_attention"]),
        },
    }

    if normalized_mode == "none":
        return profile

    if normalized_mode == "deterministic_cache":
        profile["workflow"]["cache_enabled"] = True
        return profile

    if normalized_mode == "graph_memoization":
        profile["workflow"]["cache_enabled"] = True
        profile["workflow"]["memoization_enabled"] = True
        return profile

    if normalized_mode == "model_lru":
        profile["model_manager"]["enabled"] = True
        profile["model_manager"]["enable_cpu_offload"] = False
        return profile

    if normalized_mode == "cpu_offload":
        profile["model_manager"]["enabled"] = True
        profile["model_manager"]["enable_cpu_offload"] = True
        return profile

    if normalized_mode == "lazy_loading":
        profile["model_manager"]["enabled"] = True
        profile["model_manager"]["lazy_loading"] = True
        return profile

    if normalized_mode == "attention_reuse":
        profile["attention_reuse"]["enabled"] = True
        return profile

    if normalized_mode == "attention_reuse_cpu_offload":
        profile["attention_reuse"]["enabled"] = True
        profile["model_manager"]["enabled"] = True
        profile["model_manager"]["enable_cpu_offload"] = True
        return profile

    if normalized_mode == "attention_reuse_wan21":
        profile["attention_reuse"]["enabled"] = True
        # WAN2.1 is transformer/temporal-heavy; prefer broader layer coverage.
        profile["attention_reuse"]["threshold"] = float(attn_reuse_threshold)
        profile["attention_reuse"]["store_frequency"] = max(1, int(attn_store_frequency))
        profile["attention_reuse"]["reuse_layers"] = list(
            attn_reuse_layers or ["cross_attention", "temporal_attention", "transformer_attention"]
        )
        return profile

    if normalized_mode == "attention_reuse_wan21_cpu_offload":
        profile["attention_reuse"]["enabled"] = True
        profile["attention_reuse"]["threshold"] = float(attn_reuse_threshold)
        profile["attention_reuse"]["store_frequency"] = max(1, int(attn_store_frequency))
        profile["attention_reuse"]["reuse_layers"] = list(
            attn_reuse_layers or ["cross_attention", "temporal_attention", "transformer_attention"]
        )
        profile["model_manager"]["enabled"] = True
        profile["model_manager"]["enable_cpu_offload"] = True
        return profile

    # full_stack
    profile["workflow"]["cache_enabled"] = True
    profile["workflow"]["memoization_enabled"] = True
    profile["model_manager"]["enabled"] = True
    profile["attention_reuse"]["enabled"] = True
    return profile


def apply_optimization_profile(workflow, profile: Dict[str, Any]):
    """
    Apply a profile to a Workflow instance in a compatibility-first way.
    """
    wf_cfg = (profile or {}).get("workflow", {})
    mgr_cfg = (profile or {}).get("model_manager", {})
    attn_cfg = (profile or {}).get("attention_reuse", {})

    if wf_cfg.get("cache_enabled"):
        workflow.enable_cache(
            policy=wf_cfg.get("cache_policy", "LRU"),
            size=wf_cfg.get("cache_size"),
        )
    else:
        workflow.disable_cache()

    if wf_cfg.get("memoization_enabled"):
        workflow.enable_memoization()
    else:
        workflow.disable_memoization()

    if mgr_cfg.get("enabled"):
        manager = ModelManager(
            max_models_in_vram=mgr_cfg.get("max_models_in_vram", 1),
            enable_cpu_offload=bool(mgr_cfg.get("enable_cpu_offload", True)),
        )
        workflow.set_model_manager(manager)

    if attn_cfg.get("enabled"):
        workflow.enable_attention_reuse(
            threshold=attn_cfg.get("threshold", 0.6),
            cache_device=attn_cfg.get("cache_device", "cpu"),
            store_frequency=attn_cfg.get("store_frequency", 2),
            reuse_layers=attn_cfg.get("reuse_layers", ["cross_attention"]),
        )
    else:
        workflow.disable_attention_reuse()

    return workflow
