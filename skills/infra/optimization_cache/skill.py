from skills.infra.configure_optimizations.skill import run as configure


def run(**kwargs):
    kwargs = dict(kwargs or {})
    kwargs["mode"] = "deterministic_cache"
    result = configure(**kwargs)
    result["skill"] = "optimization_cache"
    return result
