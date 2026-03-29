from comfy_agent import Workflow
from comfy_agent.config import ComfyConfig


DEFAULT_GROUPS = ["checkpoints", "vae", "clip", "lora", "unet"]


def _extract_choices(registry, node_name, input_name):
    node_info = registry.get(node_name, {})
    required = node_info.get("input", {}).get("required", {})
    spec = required.get(input_name)
    if not spec:
        return []
    raw = spec[0] if isinstance(spec, (list, tuple)) and spec else spec
    if isinstance(raw, (list, tuple)):
        return sorted({str(item) for item in raw if str(item).strip()})
    return []


def _normalize_model_names(model_names):
    if model_names is None:
        return []
    if isinstance(model_names, str):
        return [model_names]
    return [str(x) for x in model_names if str(x).strip()]


def run(
    model_names=None,
    include_groups=None,
    case_sensitive=False,
    server=None,
    headers=None,
    api_prefix=None,
):
    cfg = ComfyConfig.from_env(load_env=True)
    wf = Workflow(
        server=server or cfg.server,
        headers=headers if headers is not None else (cfg.headers or None),
        api_prefix=api_prefix if api_prefix is not None else cfg.api_prefix,
    )

    groups = include_groups or DEFAULT_GROUPS
    assets = {
        "checkpoints": _extract_choices(wf.registry, "CheckpointLoaderSimple", "ckpt_name"),
        "vae": _extract_choices(wf.registry, "VAELoader", "vae_name"),
        "clip": _extract_choices(wf.registry, "CLIPLoader", "clip_name"),
        "lora": _extract_choices(wf.registry, "LoraLoaderModelOnly", "lora_name"),
        "unet": _extract_choices(wf.registry, "UNETLoader", "unet_name"),
    }

    selected_assets = {k: assets.get(k, []) for k in groups if k in assets}
    all_models = sorted({name for values in selected_assets.values() for name in values})

    requested = _normalize_model_names(model_names)
    exists = {}
    resolved_matches = {}
    missing = []

    if case_sensitive:
        model_set = set(all_models)
        for name in requested:
            ok = name in model_set
            exists[name] = ok
            resolved_matches[name] = name if ok else None
            if not ok:
                missing.append(name)
    else:
        lower_map = {name.lower(): name for name in all_models}
        for name in requested:
            matched = lower_map.get(name.lower())
            ok = matched is not None
            exists[name] = ok
            resolved_matches[name] = matched
            if not ok:
                missing.append(name)

    return {
        "status": "ok",
        "skill": "validate_server_models",
        "server": wf.url,
        "groups": list(selected_assets.keys()),
        "counts": {k: len(v) for k, v in selected_assets.items()},
        "models": selected_assets,
        "all_model_names": all_models,
        "requested": requested,
        "exists": exists,
        "resolved_matches": resolved_matches,
        "missing": missing,
    }
