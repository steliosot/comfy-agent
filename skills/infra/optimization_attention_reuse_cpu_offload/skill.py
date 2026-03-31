from skills.infra.configure_optimizations.skill import run as configure


def run(**kwargs):
    kwargs = dict(kwargs or {})
    kwargs["mode"] = "attention_reuse_cpu_offload"
    result = configure(**kwargs)
    result["skill"] = "optimization_attention_reuse_cpu_offload"
    return result
