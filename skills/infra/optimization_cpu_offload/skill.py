from skills.infra.configure_optimizations.skill import run as configure


def run(**kwargs):
    kwargs = dict(kwargs or {})
    kwargs["mode"] = "cpu_offload"
    result = configure(**kwargs)
    result["skill"] = "optimization_cpu_offload"
    return result
