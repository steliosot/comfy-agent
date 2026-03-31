from skills.infra.configure_optimizations.skill import run as configure


def run(**kwargs):
    kwargs = dict(kwargs or {})
    kwargs["mode"] = "full_stack"
    result = configure(**kwargs)
    result["skill"] = "optimization_full_stack"
    return result
