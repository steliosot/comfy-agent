from skills.infra.configure_optimizations.skill import run as configure


def run(**kwargs):
    kwargs = dict(kwargs or {})
    kwargs["mode"] = "graph_memoization"
    result = configure(**kwargs)
    result["skill"] = "optimization_memoization"
    return result
