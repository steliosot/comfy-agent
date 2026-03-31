from comfy_agent.optimizations import build_optimization_profile


def _python_snippet(profile):
    wf_cfg = profile["workflow"]
    mgr_cfg = profile["model_manager"]
    attn_cfg = profile.get("attention_reuse", {})
    lines = [
        "from comfy_agent import Workflow, ModelManager",
        "wf = Workflow()",
    ]

    if mgr_cfg.get("enabled"):
        lines.extend(
            [
                "manager = ModelManager(" \
                f"max_models_in_vram={mgr_cfg['max_models_in_vram']}, " \
                f"enable_cpu_offload={mgr_cfg['enable_cpu_offload']})",
                "wf.set_model_manager(manager)",
            ]
        )

    if wf_cfg.get("cache_enabled"):
        lines.append(
            "wf.enable_cache(" \
            f"policy='{wf_cfg.get('cache_policy', 'LRU')}', " \
            f"size={wf_cfg.get('cache_size')})"
        )
    else:
        lines.append("wf.disable_cache()")

    if wf_cfg.get("memoization_enabled"):
        lines.append("wf.enable_memoization()")
    else:
        lines.append("wf.disable_memoization()")

    if attn_cfg.get("enabled"):
        lines.append(
            "wf.enable_attention_reuse("
            f"threshold={attn_cfg.get('threshold', 0.6)}, "
            f"cache_device='{attn_cfg.get('cache_device', 'cpu')}', "
            f"store_frequency={attn_cfg.get('store_frequency', 2)}, "
            f"reuse_layers={attn_cfg.get('reuse_layers', ['cross_attention'])})"
        )
    else:
        lines.append("wf.disable_attention_reuse()")

    return "\n".join(lines)


def run(
    mode="full_stack",
    cache_policy="LRU",
    cache_size=256,
    max_models_in_vram=1,
    enable_cpu_offload=True,
    lazy_loading=True,
    attn_reuse_threshold=0.6,
    attn_cache_device="cpu",
    attn_store_frequency=2,
    attn_reuse_layers=None,
):
    try:
        profile = build_optimization_profile(
            mode=mode,
            cache_policy=cache_policy,
            cache_size=cache_size,
            max_models_in_vram=max_models_in_vram,
            enable_cpu_offload=enable_cpu_offload,
            lazy_loading=lazy_loading,
            attn_reuse_threshold=attn_reuse_threshold,
            attn_cache_device=attn_cache_device,
            attn_store_frequency=attn_store_frequency,
            attn_reuse_layers=attn_reuse_layers,
        )
    except Exception as exc:
        return {
            "status": "error",
            "skill": "configure_optimizations",
            "mode": mode,
            "message": str(exc),
        }

    return {
        "status": "ok",
        "skill": "configure_optimizations",
        "mode": profile["mode"],
        "workflow": profile["workflow"],
        "model_manager": profile["model_manager"],
        "attention_reuse": profile.get("attention_reuse", {}),
        "python_snippet": _python_snippet(profile),
        "notes": [
            "Apply workflow settings before building/running your DAG.",
            "ModelManager is client-side compatibility logic; Comfy server still controls server-side memory.",
            "Attention reuse needs a compatible backend adapter for real attention interception.",
        ],
    }
