from skills.infra.configure_optimizations.skill import run as configure


def run(**kwargs):
    kwargs = dict(kwargs or {})
    kwargs["mode"] = "attention_reuse"
    result = configure(**kwargs)
    result["skill"] = "optimization_attention_reuse"
    return result
