import json
from pathlib import Path

from comfy_agent import Workflow
from comfy_agent.config import ComfyConfig
from comfy_agent.curated_catalog import load_curated_manifest
from comfy_agent.monitoring import fetch_json, fetch_queue, fetch_system_stats


MODEL_FIELDS = {
    "ckpt_name": "checkpoint",
    "vae_name": "vae",
    "clip_name": "clip",
    "lora_name": "lora",
    "unet_name": "unet",
}


def _clamp(value, low=0.02, high=0.99):
    return max(low, min(high, float(value)))


def _resolve_workflow_source(skill_id=None, workflow_path=None, workflow_payload=None):
    if workflow_payload is not None:
        return workflow_payload
    if workflow_path:
        return json.loads(Path(workflow_path).read_text(encoding="utf-8"))
    if skill_id:
        manifest = load_curated_manifest()
        for item in manifest.get("entries", []):
            if item.get("id") == skill_id:
                wf_path = Path(item.get("destination", "")) / "workflow.json"
                if wf_path.exists():
                    return json.loads(wf_path.read_text(encoding="utf-8"))
        raise ValueError(f"Unknown curated skill_id: {skill_id}")
    raise ValueError("Provide one of: skill_id, workflow_path, workflow_payload")


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


def _extract_signature(workflow_obj):
    class_types = set()
    model_requirements = []

    # API prompt shape
    if isinstance(workflow_obj, dict) and "prompt" in workflow_obj and isinstance(workflow_obj["prompt"], dict):
        workflow_obj = workflow_obj["prompt"]

    if isinstance(workflow_obj, dict) and all(isinstance(v, dict) for v in workflow_obj.values()):
        for node in workflow_obj.values():
            class_type = node.get("class_type")
            if class_type:
                class_types.add(str(class_type))
            inputs = node.get("inputs", {})
            if not isinstance(inputs, dict):
                continue
            for key, model_type in MODEL_FIELDS.items():
                value = inputs.get(key)
                if isinstance(value, str) and value.strip():
                    model_requirements.append({"name": value.strip(), "model_type": model_type})
        return {
            "class_types": sorted(class_types),
            "model_requirements": _dedupe_models(model_requirements),
        }

    # Exported Comfy graph shape
    nodes = workflow_obj.get("nodes") if isinstance(workflow_obj, dict) else None
    if isinstance(nodes, list):
        for node in nodes:
            if not isinstance(node, dict):
                continue
            node_type = node.get("type")
            if node_type:
                class_types.add(str(node_type))
            widgets = node.get("widgets_values")
            first = widgets[0] if isinstance(widgets, list) and widgets else None
            if isinstance(first, str):
                if node_type == "CheckpointLoaderSimple":
                    model_requirements.append({"name": first, "model_type": "checkpoint"})
                elif node_type in {"UNETLoader", "UnetLoaderGGUF"}:
                    model_requirements.append({"name": first, "model_type": "unet"})
                elif node_type == "VAELoader":
                    model_requirements.append({"name": first, "model_type": "vae"})
                elif node_type in {"CLIPLoader", "DualCLIPLoaderGGUF"}:
                    model_requirements.append({"name": first, "model_type": "clip"})
                elif node_type in {"LoraLoader", "LoraLoaderModelOnly"}:
                    model_requirements.append({"name": first, "model_type": "lora"})
        return {
            "class_types": sorted(class_types),
            "model_requirements": _dedupe_models(model_requirements),
        }

    return {"class_types": [], "model_requirements": []}


def _dedupe_models(models):
    out = []
    seen = set()
    for item in models:
        key = (str(item.get("model_type", "")).lower(), str(item.get("name", "")).lower())
        if key in seen:
            continue
        seen.add(key)
        out.append({"name": item.get("name"), "model_type": item.get("model_type")})
    return out


def _dependency_score(signature, registry):
    class_types = signature.get("class_types", [])
    model_requirements = signature.get("model_requirements", [])
    available = _available_models(registry)

    missing_nodes = [x for x in class_types if x not in registry]
    missing_models = []
    for model in model_requirements:
        mtype = model.get("model_type")
        mname = str(model.get("name", ""))
        choices = available.get(mtype, [])
        if not choices:
            continue
        present = any(mname.lower() == c.lower() or c.lower().endswith(mname.lower()) for c in choices)
        if not present:
            missing_models.append(model)

    base = 0.95
    base -= min(0.55, 0.18 * len(missing_nodes))
    base -= min(0.35, 0.10 * len(missing_models))
    if missing_nodes:
        # Unknown class types usually indicate missing custom nodes, which are high-risk.
        base -= 0.24

    return {
        "score": _clamp(base),
        "missing_class_types": missing_nodes,
        "missing_models": missing_models,
        "required_models": model_requirements,
        "required_class_types": class_types,
    }


def _history_entries(server, headers=None, api_prefix=None):
    result = fetch_json(server, "/history", headers=headers, api_prefix=api_prefix)
    if not result.get("ok"):
        return []
    data = result.get("data")
    if isinstance(data, dict):
        return list(data.values())
    if isinstance(data, list):
        return data
    return []


def _entry_prompt_map(entry):
    if not isinstance(entry, dict):
        return {}
    prompt = entry.get("prompt")
    if isinstance(prompt, dict):
        return prompt
    if isinstance(prompt, list):
        for item in prompt:
            if isinstance(item, dict) and all(isinstance(v, dict) for v in item.values()):
                return item
    return {}


def _entry_success(entry):
    outputs = entry.get("outputs", {}) if isinstance(entry, dict) else {}
    if not isinstance(outputs, dict):
        return None
    count = 0
    for node_output in outputs.values():
        if not isinstance(node_output, dict):
            continue
        for key in ("images", "videos", "gifs", "audio"):
            values = node_output.get(key)
            if isinstance(values, list):
                count += len(values)
    return count > 0


def _jaccard(a, b):
    sa, sb = set(a), set(b)
    if not sa and not sb:
        return 0.0
    if not sa or not sb:
        return 0.0
    return len(sa & sb) / max(1, len(sa | sb))


def _history_score(signature, server, headers=None, api_prefix=None, recent_history_limit=200):
    target = signature.get("class_types", [])
    entries = _history_entries(server, headers=headers, api_prefix=api_prefix)[: int(recent_history_limit)]
    if not entries:
        return {
            "score": 0.65,
            "history_count": 0,
            "similar_count": 0,
            "similar_success_rate": None,
            "top_similar_examples": [],
            "note": "No history entries available; using neutral baseline.",
        }

    samples = []
    for entry in entries:
        prompt_map = _entry_prompt_map(entry)
        classes = [node.get("class_type") for node in prompt_map.values() if isinstance(node, dict) and node.get("class_type")]
        similarity = _jaccard(target, classes)
        success = _entry_success(entry)
        samples.append(
            {
                "similarity": similarity,
                "success": success,
                "class_count": len(classes),
            }
        )

    similar = [x for x in samples if x["similarity"] >= 0.35 and x["success"] is not None]
    if not similar:
        return {
            "score": 0.62,
            "history_count": len(entries),
            "similar_count": 0,
            "similar_success_rate": None,
            "top_similar_examples": sorted(samples, key=lambda x: x["similarity"], reverse=True)[:3],
            "note": "No sufficiently similar prior runs found; using conservative-neutral estimate.",
        }

    weighted_success = sum(x["similarity"] * (1.0 if x["success"] else 0.0) for x in similar)
    weight_sum = sum(x["similarity"] for x in similar)
    rate = (weighted_success / weight_sum) if weight_sum > 0 else 0.62

    score = 0.45 + 0.5 * rate
    return {
        "score": _clamp(score),
        "history_count": len(entries),
        "similar_count": len(similar),
        "similar_success_rate": round(rate, 4),
        "top_similar_examples": sorted(similar, key=lambda x: x["similarity"], reverse=True)[:5],
        "note": "Estimated from similar historical runs.",
    }


def _resource_score(server, headers=None, api_prefix=None):
    queue = fetch_queue(server, headers=headers, api_prefix=api_prefix)
    stats = fetch_system_stats(server, headers=headers, api_prefix=api_prefix)

    score = 0.8
    warnings = []
    blockers = []

    pending = len(queue.get("pending", []))
    running = len(queue.get("running", []))
    if pending > 10:
        score -= 0.12
        warnings.append(f"Queue pending is high ({pending}).")
    elif pending > 3:
        score -= 0.06
        warnings.append(f"Queue pending is moderate ({pending}).")

    if running > 3:
        score -= 0.05

    stat_payload = stats.get("stats", {}) if isinstance(stats, dict) else {}
    devices = stat_payload.get("devices", []) if isinstance(stat_payload, dict) else []
    if devices:
        free_vals = []
        for dev in devices:
            if not isinstance(dev, dict):
                continue
            free = dev.get("vram_free")
            if isinstance(free, (int, float)):
                free_vals.append(float(free) / (1024 * 1024))
        if free_vals:
            max_free_mb = max(free_vals)
            if max_free_mb < 1024:
                score -= 0.25
                blockers.append(f"Very low free VRAM ({int(max_free_mb)} MB).")
            elif max_free_mb < 2048:
                score -= 0.10
                warnings.append(f"Low free VRAM ({int(max_free_mb)} MB).")

    return {
        "score": _clamp(score),
        "queue_pending": pending,
        "queue_running": running,
        "warnings": warnings,
        "blockers": blockers,
    }


def run(
    skill_id=None,
    workflow_path=None,
    workflow_payload=None,
    server=None,
    headers=None,
    api_prefix=None,
    recent_history_limit=200,
):
    cfg = ComfyConfig.from_env(load_env=True)
    resolved_server = server or cfg.server
    resolved_headers = headers if headers is not None else (cfg.headers or None)
    resolved_api_prefix = api_prefix if api_prefix is not None else cfg.api_prefix

    source = _resolve_workflow_source(
        skill_id=skill_id,
        workflow_path=workflow_path,
        workflow_payload=workflow_payload,
    )

    wf = Workflow(server=resolved_server, headers=resolved_headers, api_prefix=resolved_api_prefix)
    signature = _extract_signature(source)
    dep = _dependency_score(signature, wf.registry)
    hist = _history_score(
        signature,
        server=resolved_server,
        headers=resolved_headers,
        api_prefix=resolved_api_prefix,
        recent_history_limit=recent_history_limit,
    )
    res = _resource_score(server=resolved_server, headers=resolved_headers, api_prefix=resolved_api_prefix)

    likelihood = (
        0.45 * dep["score"]
        + 0.35 * hist["score"]
        + 0.20 * res["score"]
    )
    likelihood = _clamp(likelihood)

    confidence = 0.45
    confidence += 0.20 if dep["required_class_types"] else 0.0
    confidence += 0.20 if hist["history_count"] >= 20 else 0.10 if hist["history_count"] >= 5 else 0.0
    confidence += 0.15 if not res["blockers"] else 0.05
    confidence = _clamp(confidence, low=0.1, high=0.99)

    return {
        "status": "ok",
        "skill": "predict_job_success_likelihood",
        "server": resolved_server,
        "likelihood": round(likelihood, 4),
        "confidence": round(confidence, 4),
        "breakdown": {
            "dependencies": dep,
            "history_similarity": hist,
            "resources": res,
        },
        "recommendation": (
            "safe_to_run"
            if likelihood >= 0.7
            else "run_with_caution"
            if likelihood >= 0.45
            else "fix_dependencies_first"
        ),
    }
