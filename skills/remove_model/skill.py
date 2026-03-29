from comfy_agent import Workflow
from comfy_agent.config import ComfyConfig
from comfy_agent.manager import manager_install
from skills.download_model.skill import MODEL_TYPE_TO_GROUP


def _normalize_model_type(model_type):
    text = str(model_type or "").strip().lower()
    if text == "diffusion":
        text = "diffusion_model"
    if text not in MODEL_TYPE_TO_GROUP:
        raise ValueError(
            "model_type must be one of: checkpoint, vae, clip, lora, unet, diffusion_model, custom"
        )
    return text


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


def _is_present(wf, model_type, filename):
    node_name, input_name, _ = MODEL_TYPE_TO_GROUP[model_type]
    if node_name is None:
        return None
    choices = _extract_choices(wf.registry, node_name, input_name)
    lowered = filename.lower()
    return any(item.lower() == lowered or item.lower().endswith(lowered) for item in choices)


def run(
    filename,
    model_type,
    subfolder=None,
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
    normalized_model_type = _normalize_model_type(model_type)
    _, _, default_folder = MODEL_TYPE_TO_GROUP[normalized_model_type]
    target_subfolder = subfolder or default_folder

    payload = {
        "filename": filename,
        "model_type": normalized_model_type,
        "subfolder": target_subfolder,
    }
    remove = manager_install(
        operation="model_remove",
        payload=payload,
        server=resolved_server,
        headers=resolved_headers,
        api_prefix=resolved_api_prefix,
        manager_api_prefix=resolved_manager_prefix,
    )

    verification = {"present_after_remove": None}
    if remove.get("ok"):
        try:
            wf = Workflow(
                server=resolved_server,
                headers=resolved_headers,
                api_prefix=resolved_api_prefix,
            )
            present = _is_present(wf, normalized_model_type, filename)
            verification = {
                "present_after_remove": present,
                "verified_removed": (present is False) if present is not None else None,
            }
        except Exception as exc:
            verification = {
                "present_after_remove": None,
                "verified_removed": None,
                "verification_error": str(exc),
            }

    return {
        "status": "ok" if remove.get("ok") else "error",
        "skill": "remove_model",
        "server": resolved_server,
        "filename": filename,
        "model_type": normalized_model_type,
        "target_subfolder": target_subfolder,
        "remove": remove,
        "verification": verification,
    }
