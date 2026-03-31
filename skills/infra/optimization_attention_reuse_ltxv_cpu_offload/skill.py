from skills.infra.configure_optimizations.skill import run as configure


def run(**kwargs):
    kwargs = dict(kwargs or {})
    kwargs["mode"] = "attention_reuse_cpu_offload"
    kwargs.setdefault("attn_reuse_layers", ['cross_attention', 'temporal_attention', 'transformer_attention'])
    result = configure(**kwargs)
    result["skill"] = "optimization_attention_reuse_ltxv_cpu_offload"
    return result
