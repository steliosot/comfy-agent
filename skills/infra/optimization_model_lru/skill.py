from skills.infra.configure_optimizations.skill import run as configure


def run(**kwargs):
    kwargs = dict(kwargs or {})
    kwargs["mode"] = "model_lru"
    result = configure(**kwargs)
    result["skill"] = "optimization_model_lru"
    return result
