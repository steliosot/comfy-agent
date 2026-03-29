import json
from pathlib import Path

from comfy_agent import Workflow
from comfy_agent.config import ComfyConfig
from skills.infra.assess_server_resources.skill import run as assess_resources
from skills.infra.download_model.skill import run as download_model
from skills.infra.install_custom_node.skill import run as install_custom_node


MODEL_FIELDS = {
    "ckpt_name": "checkpoint",
    "vae_name": "vae",
    "clip_name": "clip",
    "lora_name": "lora",
    "unet_name": "unet",
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


def _available_models(registry):
    return {
        "checkpoint": _extract_choices(registry, "CheckpointLoaderSimple", "ckpt_name"),
        "vae": _extract_choices(registry, "VAELoader", "vae_name"),
        "clip": _extract_choices(registry, "CLIPLoader", "clip_name"),
        "lora": _extract_choices(registry, "LoraLoaderModelOnly", "lora_name"),
        "unet": _extract_choices(registry, "UNETLoader", "unet_name"),
    }


def _normalize_requirements(requirements):
    req = requirements or {}
    models = req.get("models", []) if isinstance(req, dict) else []
    custom_nodes = req.get("custom_nodes", []) if isinstance(req, dict) else []
    min_vram = req.get("min_vram_mb") if isinstance(req, dict) else None
    min_storage = req.get("min_storage_gb") if isinstance(req, dict) else None
    return {
        "models": models if isinstance(models, list) else [],
        "custom_nodes": custom_nodes if isinstance(custom_nodes, list) else [],
        "min_vram_mb": min_vram,
        "min_storage_gb": min_storage,
    }


def _normalize_workflow_payload(workflow_payload=None, workflow_path=None):
    if workflow_payload is not None:
        data = workflow_payload
    elif workflow_path:
        text = Path(workflow_path).read_text(encoding="utf-8")
        data = json.loads(text)
    else:
        return {}

    if isinstance(data, dict) and "prompt" in data and isinstance(data["prompt"], dict):
        return data["prompt"]
    if isinstance(data, dict):
        return data
    return {}


def _extract_workflow_requirements(prompt_map):
    required_models = []
    required_class_types = set()
    if not isinstance(prompt_map, dict):
        return {"models": [], "class_types": []}

    for _, node in prompt_map.items():
        if not isinstance(node, dict):
            continue
        class_type = node.get("class_type")
        if class_type:
            required_class_types.add(str(class_type))
        inputs = node.get("inputs", {})
        if not isinstance(inputs, dict):
            continue
        for key, model_type in MODEL_FIELDS.items():
            value = inputs.get(key)
            if value:
                required_models.append(
                    {
                        "name": str(value),
                        "model_type": model_type,
                    }
                )
    return {
        "models": required_models,
        "class_types": sorted(required_class_types),
    }


def _find_model_spec(model_name, model_type, explicit_specs):
    for item in explicit_specs:
        if not isinstance(item, dict):
            continue
        candidate_name = str(item.get("name") or item.get("filename") or "").strip()
        candidate_type = str(item.get("model_type", "")).strip().lower()
        if not candidate_name:
            continue
        if candidate_type and candidate_type != model_type:
            continue
        if candidate_name.lower() == model_name.lower():
            return item
    return None


def run(
    requirements=None,
    workflow_payload=None,
    workflow_path=None,
    auto_fix=True,
    warn_only=True,
    min_vram_mb=None,
    min_storage_gb=None,
    server=None,
    headers=None,
    api_prefix=None,
):
    cfg = ComfyConfig.from_env(load_env=True)
    resolved_server = server or cfg.server
    resolved_headers = headers if headers is not None else (cfg.headers or None)
    resolved_api_prefix = api_prefix if api_prefix is not None else cfg.api_prefix

    try:
        wf = Workflow(
            server=resolved_server,
            headers=resolved_headers,
            api_prefix=resolved_api_prefix,
        )
    except Exception as exc:
        return {
            "status": "error",
            "skill": "prepare_workflow_dependencies",
            "server": resolved_server,
            "auto_fix": bool(auto_fix),
            "warn_only": bool(warn_only),
            "resource_assessment": None,
            "detected": {"models": [], "class_types": []},
            "required_models": [],
            "fixed": {"models": [], "custom_nodes": []},
            "still_missing": {"models": [], "custom_nodes": []},
            "warnings": [],
            "actions": [],
            "ready_for_run": False,
            "error": "workflow_connectivity_failed",
            "message": str(exc),
        }
    registry = wf.registry
    available = _available_models(registry)

    normalized_requirements = _normalize_requirements(requirements)
    prompt_map = _normalize_workflow_payload(
        workflow_payload=workflow_payload,
        workflow_path=workflow_path,
    )
    detected = _extract_workflow_requirements(prompt_map)

    required_models = list(detected["models"])
    for item in normalized_requirements["models"]:
        if isinstance(item, dict):
            name = str(item.get("name") or item.get("filename") or "").strip()
            model_type = str(item.get("model_type") or "").strip().lower()
            if name and model_type:
                required_models.append({"name": name, "model_type": model_type})

    # Deduplicate while preserving meaning
    deduped_models = []
    seen_model_keys = set()
    for item in required_models:
        key = (item["name"].lower(), item["model_type"])
        if key in seen_model_keys:
            continue
        seen_model_keys.add(key)
        deduped_models.append(item)
    required_models = deduped_models

    missing_models = []
    for model in required_models:
        model_name = model["name"]
        model_type = model["model_type"]
        candidates = available.get(model_type, [])
        if not candidates:
            # Some server configs do not expose complete model lists in object_info.
            # Treat as unknown availability instead of hard missing.
            continue
        present = any(
            model_name.lower() == candidate.lower() or candidate.lower().endswith(model_name.lower())
            for candidate in candidates
        )
        if not present:
            missing_models.append(model)

    missing_custom_nodes = []
    for class_type in detected["class_types"]:
        if class_type not in registry:
            missing_custom_nodes.append(class_type)

    resource = assess_resources(
        min_vram_mb=min_vram_mb if min_vram_mb is not None else normalized_requirements["min_vram_mb"],
        min_storage_gb=min_storage_gb if min_storage_gb is not None else normalized_requirements["min_storage_gb"],
        warn_only=warn_only,
        server=resolved_server,
        headers=resolved_headers,
        api_prefix=resolved_api_prefix,
    )

    fixed = {"models": [], "custom_nodes": []}
    still_missing = {"models": list(missing_models), "custom_nodes": list(missing_custom_nodes)}
    warnings = list(resource.get("warnings", []))
    actions = []

    if auto_fix and resource.get("ready_for_install", False):
        model_specs = normalized_requirements["models"]
        resolved_missing_models = []
        for item in still_missing["models"]:
            spec = _find_model_spec(item["name"], item["model_type"], model_specs)
            if spec is None:
                resolved_missing_models.append(
                    {
                        **item,
                        "reason": "No install spec provided for this missing model.",
                    }
                )
                continue

            try:
                dl_result = download_model(
                    source=spec.get("source"),
                    model_id_or_url=spec.get("model_id_or_url"),
                    filename=spec.get("filename") or spec.get("name"),
                    model_type=spec.get("model_type") or item["model_type"],
                    revision=spec.get("revision"),
                    subfolder=spec.get("subfolder"),
                    token=spec.get("token"),
                    server=resolved_server,
                    headers=resolved_headers,
                    api_prefix=resolved_api_prefix,
                )
            except Exception as exc:
                dl_result = {
                    "status": "error",
                    "error": str(exc),
                    "skill": "download_model",
                }
            actions.append({"type": "download_model", "target": item, "result": dl_result})
            verified = bool(dl_result.get("verification", {}).get("verified"))
            if dl_result.get("status") == "ok" and verified:
                fixed["models"].append(item)
            else:
                resolved_missing_models.append(
                    {
                        **item,
                        "reason": "Download/install failed or model not verified.",
                        "install_status": dl_result.get("status"),
                    }
                )
        still_missing["models"] = resolved_missing_models

        node_specs = normalized_requirements["custom_nodes"]
        if still_missing["custom_nodes"]:
            if not node_specs:
                warnings.append(
                    "Custom nodes are missing but no custom_nodes install specs were provided."
                )
            for spec in node_specs:
                if not isinstance(spec, dict):
                    continue
                repo_url = spec.get("repo_url")
                if not repo_url:
                    continue
                expected = spec.get("expected_node_classes") or still_missing["custom_nodes"]
                node_result = install_custom_node(
                    repo_url=repo_url,
                    expected_node_classes=expected,
                    server=resolved_server,
                    headers=resolved_headers,
                    api_prefix=resolved_api_prefix,
                )
                actions.append(
                    {"type": "install_custom_node", "target": {"repo_url": repo_url}, "result": node_result}
                )
                if node_result.get("status") == "ok":
                    fixed["custom_nodes"].append({"repo_url": repo_url, "expected_node_classes": expected})

            wf_after = Workflow(
                server=resolved_server,
                headers=resolved_headers,
                api_prefix=resolved_api_prefix,
            )
            still_missing["custom_nodes"] = [
                class_type for class_type in still_missing["custom_nodes"] if class_type not in wf_after.registry
            ]

    ready_for_run = (
        len(still_missing["models"]) == 0
        and len(still_missing["custom_nodes"]) == 0
        and len(resource.get("blockers", [])) == 0
    )

    return {
        "status": "ok" if ready_for_run else "degraded",
        "skill": "prepare_workflow_dependencies",
        "server": resolved_server,
        "auto_fix": bool(auto_fix),
        "warn_only": bool(warn_only),
        "resource_assessment": resource,
        "detected": detected,
        "required_models": required_models,
        "fixed": fixed,
        "still_missing": still_missing,
        "warnings": warnings,
        "actions": actions,
        "ready_for_run": ready_for_run,
    }
