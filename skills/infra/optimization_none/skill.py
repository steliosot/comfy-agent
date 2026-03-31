from skills.infra.configure_optimizations.skill import run as configure


def run(**kwargs):
    kwargs = dict(kwargs or {})
    kwargs["mode"] = "none"
    result = configure(**kwargs)
    result["skill"] = "optimization_none"
    return result
