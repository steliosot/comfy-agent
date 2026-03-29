from comfy_agent import Workflow
from comfy_agent.config import ComfyConfig
from comfy_agent.manager import manager_install


MODEL_TYPE_TO_GROUP = {
    "checkpoint": ("CheckpointLoaderSimple", "ckpt_name", "models/checkpoints"),
    "vae": ("VAELoader", "vae_name", "models/vae"),
    "clip": ("CLIPLoader", "clip_name", "models/clip"),
    "lora": ("LoraLoaderModelOnly", "lora_name", "models/loras"),
    "unet": ("UNETLoader", "unet_name", "models/diffusion_models"),
    "diffusion_model": ("UNETLoader", "unet_name", "models/diffusion_models"),
    "custom": (None, None, "models/custom"),
}


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


def _resolve_token(source, token, cfg):
    if token:
        return token
    source_text = str(source or "").lower().strip()
    if source_text == "huggingface":
        return cfg.hf_token
    if source_text == "civitai":
        return cfg.civitai_api_key
    return None


def _validate_source(source):
    normalized = str(source or "").strip().lower()
    if normalized not in {"huggingface", "civitai"}:
        raise ValueError("source must be 'huggingface' or 'civitai'")
    return normalized


def _normalize_model_type(model_type):
    normalized = str(model_type or "").strip().lower()
    if normalized == "diffusion":
        normalized = "diffusion_model"
    if normalized not in MODEL_TYPE_TO_GROUP:
        raise ValueError(
            "model_type must be one of: checkpoint, vae, clip, lora, unet, diffusion_model, custom"
        )
    return normalized


def _verify_model_present(wf, model_type, expected_name):
    node_name, input_name, _ = MODEL_TYPE_TO_GROUP[model_type]
    if node_name is None:
        return {"verified": False, "reason": "custom model type has no direct loader validation"}

    candidates = _extract_choices(wf.registry, node_name, input_name)
    match = None
    if expected_name:
        lowered_expected = expected_name.lower()
        for item in candidates:
            if item.lower() == lowered_expected or item.lower().endswith(lowered_expected):
                match = item
                break
    return {
        "verified": match is not None,
        "matched_name": match,
        "available_count": len(candidates),
        "available_names": candidates,
    }


def run(
    source,
    model_id_or_url,
    filename,
    model_type,
    revision=None,
    subfolder=None,
    token=None,
    server=None,
    headers=None,
    api_prefix=None,
    manager_api_prefix=None,
):
    cfg = ComfyConfig.from_env(load_env=True)
    resolved_server = server or cfg.server
    resolved_headers = headers if headers is not None else (cfg.headers or None)
    resolved_api_prefix = api_prefix if api_prefix is not None else cfg.api_prefix
    resolved_manager_prefix = (
        manager_api_prefix if manager_api_prefix is not None else cfg.manager_api_prefix
    )

    normalized_source = _validate_source(source)
    normalized_model_type = _normalize_model_type(model_type)
    _, _, default_target = MODEL_TYPE_TO_GROUP[normalized_model_type]
    token_value = _resolve_token(normalized_source, token, cfg)
    target_subfolder = subfolder or default_target

    payload = {
        "source": normalized_source,
        "model_id_or_url": model_id_or_url,
        "model_url": model_id_or_url,
        "filename": filename,
        "model_type": normalized_model_type,
        "subfolder": target_subfolder,
        "revision": revision,
        "token": token_value,
    }
    payload = {k: v for k, v in payload.items() if v not in (None, "")}

    install = manager_install(
        operation="model_install",
        payload=payload,
        server=resolved_server,
        headers=resolved_headers,
        api_prefix=resolved_api_prefix,
        manager_api_prefix=resolved_manager_prefix,
    )

    verification = None
    if install.get("ok"):
        wf = Workflow(
            server=resolved_server,
            headers=resolved_headers,
            api_prefix=resolved_api_prefix,
        )
        verification = _verify_model_present(
            wf=wf,
            model_type=normalized_model_type,
            expected_name=filename,
        )
    else:
        verification = {"verified": False, "reason": "install_failed"}

    return {
        "status": "ok" if install.get("ok") else "error",
        "skill": "download_model",
        "server": resolved_server,
        "source": normalized_source,
        "model_type": normalized_model_type,
        "filename": filename,
        "target_subfolder": target_subfolder,
        "token_used": bool(token_value),
        "install": install,
        "verification": verification,
    }
