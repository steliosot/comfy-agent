from skills.infra.configure_optimizations.skill import run as configure


def run(**kwargs):
    kwargs = dict(kwargs or {})
    kwargs["mode"] = "lazy_loading"
    result = configure(**kwargs)
    result["skill"] = "optimization_lazy_loading"
    return result
