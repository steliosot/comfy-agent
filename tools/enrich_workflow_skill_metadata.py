#!/usr/bin/env python3
import json
import re
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS_ROOT = REPO_ROOT / "skills" / "workflows"
FAMILY_DIRS = {
    "audio",
    "txt2img",
    "img2img_inpaint_outpaint",
    "editing_restyle",
    "video_t2v_i2v_avatar",
    "upscaling",
}


MODEL_NODE_MAP = {
    "CheckpointLoaderSimple": ("checkpoint", "models/checkpoints"),
    "VAELoader": ("vae", "models/vae"),
    "CLIPLoader": ("clip", "models/clip"),
    "DualCLIPLoaderGGUF": ("clip", "models/clip"),
    "UNETLoader": ("diffusion_model", "models/diffusion_models"),
    "UnetLoaderGGUF": ("diffusion_model", "models/diffusion_models"),
    "LoraLoader": ("lora", "models/loras"),
    "LoraLoaderModelOnly": ("lora", "models/loras"),
    "ControlNetLoader": ("controlnet", "models/controlnet"),
    "UpscaleModelLoader": ("upscale_model", "models/upscale_models"),
}


def _extract_urls(text):
    if not text:
        return []
    return sorted(set(re.findall(r"https?://[^\s)\]>\"']+", str(text))))


def _as_text(widget_values):
    if isinstance(widget_values, str):
        return widget_values
    if isinstance(widget_values, list):
        return " ".join(str(v) for v in widget_values if isinstance(v, (str, int, float, bool)))
    if isinstance(widget_values, dict):
        return " ".join(str(v) for v in widget_values.values())
    return ""


def _infer_model_families(models, node_types, family):
    probe = " ".join([family] + [m["name"] for m in models] + list(node_types)).lower()
    out = []
    for token in ("flux", "sdxl", "wan", "ltx", "qwen", "z_image_turbo", "sd3", "sd1.5"):
        key = token.replace("_", " ")
        if key in probe or token in probe:
            out.append(token)
    if not out:
        out.append("other")
    return sorted(set(out))


def _extract_metrics(nodes):
    max_width = None
    max_height = None
    max_steps = None
    for node in nodes:
        node_type = str(node.get("type", ""))
        values = node.get("widgets_values")
        if isinstance(values, list):
            if node_type in {
                "EmptyLatentImage",
                "EmptyHunyuanLatentVideo",
                "EmptySD3LatentImage",
                "EmptySanaLatentImage",
            } and len(values) >= 2:
                if isinstance(values[0], int):
                    max_width = max(max_width or values[0], values[0])
                if isinstance(values[1], int):
                    max_height = max(max_height or values[1], values[1])
            if node_type.startswith("KSampler") and len(values) >= 3 and isinstance(values[2], int):
                max_steps = max(max_steps or values[2], values[2])
    return {
        "max_width": max_width,
        "max_height": max_height,
        "max_steps": max_steps,
    }


def _resource_profile(family, models, node_types, metrics, custom_nodes_count):
    score = 0
    warnings = []

    is_video = family == "video_t2v_i2v_avatar" or "VHS_VideoCombine" in node_types
    if is_video:
        score += 4
        warnings.append("Video workflow: usually slower and VRAM-intensive than still-image workflows.")

    has_audio = family == "audio" or any("audio" in n.lower() for n in node_types)
    if has_audio:
        score += 2
        warnings.append("Audio generation may take longer on CPU-only or low-VRAM servers.")

    heavy_model_tokens = ("14b", "13b", "12b", "xxl", "large", "q8", "fp16")
    heavy_hits = [m["name"] for m in models if any(tok in m["name"].lower() for tok in heavy_model_tokens)]
    if heavy_hits:
        score += min(4, 1 + len(heavy_hits))
        warnings.append("Large model(s) detected; ensure enough VRAM and disk space.")

    width = metrics.get("max_width") or 0
    height = metrics.get("max_height") or 0
    px = width * height
    if px >= 1920 * 1080:
        score += 3
        warnings.append("High output resolution detected; generation time/memory use can increase significantly.")
    elif px >= 1280 * 720:
        score += 2
        warnings.append("Medium-high resolution detected; expect moderate extra runtime.")

    steps = metrics.get("max_steps") or 0
    if steps >= 60:
        score += 3
        warnings.append("High sampler steps detected (>=60); expect longer generation time.")
    elif steps >= 40:
        score += 2
        warnings.append("Moderate-high sampler steps detected (>=40); runtime may be longer.")

    if custom_nodes_count >= 4:
        score += 2
        warnings.append("Multiple custom nodes required; verify node installation/version compatibility.")
    elif custom_nodes_count >= 1:
        score += 1
        warnings.append("Uses custom nodes; missing nodes can cause validation/runtime failures.")

    if score <= 2:
        profile = "low"
        est = "fast (usually under 30s on modern GPU)"
    elif score <= 5:
        profile = "medium"
        est = "moderate (about 30-120s depending on server)"
    elif score <= 8:
        profile = "high"
        est = "slow (often 2-6 min depending on model/server load)"
    else:
        profile = "very_high"
        est = "heavy (can exceed 6 min; best on high-VRAM GPU)"

    return {
        "complexity_score": score,
        "resource_profile": profile,
        "estimated_runtime": est,
        "warnings": sorted(set(warnings)),
    }


def analyze_workflow(family, workflow_path):
    payload = json.loads(workflow_path.read_text(encoding="utf-8"))
    nodes = payload.get("nodes") or []

    links = set()
    custom_nodes = set()
    models = []
    model_seen = set()
    node_types = set()
    input_modalities = set()
    output_modalities = set()

    for node in nodes:
        if not isinstance(node, dict):
            continue
        node_type = str(node.get("type", ""))
        node_types.add(node_type)

        props = node.get("properties") or {}
        cnr_id = props.get("cnr_id")
        if cnr_id and cnr_id != "comfy-core":
            custom_nodes.add(str(cnr_id))

        text_blob = _as_text(node.get("widgets_values"))
        links.update(_extract_urls(text_blob))

        values = node.get("widgets_values")
        first = values[0] if isinstance(values, list) and values else None
        mapped = MODEL_NODE_MAP.get(node_type)
        if mapped and isinstance(first, str):
            model_type, folder = mapped
            key = (model_type, first)
            if key not in model_seen:
                model_seen.add(key)
                models.append({"type": model_type, "name": first, "target_folder": folder})

        low = node_type.lower()
        if "loadimage" in low:
            input_modalities.add("image")
        if "loadvideo" in low:
            input_modalities.add("video")
        if "audio" in low and "load" in low:
            input_modalities.add("audio")
        if node_type == "CLIPTextEncode":
            input_modalities.add("text_prompt")

        if node_type in {"SaveImage", "PreviewImage", "Image Comparer (rgthree)"}:
            output_modalities.add("image/png")
        if node_type in {"VHS_VideoCombine", "SaveVideo"}:
            output_modalities.add("video/mp4")
        if "audio" in low and ("save" in low or "combine" in low):
            output_modalities.add("audio/wav")

    if not output_modalities:
        output_modalities.add("application/json")
    if not input_modalities:
        input_modalities.add("text_prompt")

    metrics = _extract_metrics(nodes)
    profile = _resource_profile(
        family=family,
        models=models,
        node_types=node_types,
        metrics=metrics,
        custom_nodes_count=len(custom_nodes),
    )

    return {
        "node_count": len(nodes),
        "node_types": sorted(node_types),
        "models": models,
        "custom_nodes": sorted(custom_nodes),
        "links": sorted(links),
        "input_modalities": sorted(input_modalities),
        "output_modalities": sorted(output_modalities),
        "model_families": _infer_model_families(models, node_types, family),
        "max_width": metrics.get("max_width"),
        "max_height": metrics.get("max_height"),
        "max_steps": metrics.get("max_steps"),
        "complexity_score": profile["complexity_score"],
        "resource_profile": profile["resource_profile"],
        "estimated_runtime": profile["estimated_runtime"],
        "warnings": profile["warnings"],
    }


def upsert_metadata_block(skill_md_path, meta):
    text = skill_md_path.read_text(encoding="utf-8")
    start = "<!-- AUTO-METADATA-START -->"
    end = "<!-- AUTO-METADATA-END -->"

    models = meta["models"]
    warnings = meta["warnings"] or ["No major runtime warnings detected."]
    model_lines = (
        "\n".join(f"- `{m['type']}`: `{m['name']}` -> `{m['target_folder']}`" for m in models)
        if models
        else "- None detected."
    )
    custom_lines = "\n".join(f"- `{n}`" for n in meta["custom_nodes"]) if meta["custom_nodes"] else "- None detected."
    warn_lines = "\n".join(f"- {w}" for w in warnings)

    block = (
        f"\n{start}\n"
        "## Routing Metadata\n\n"
        f"- Family: `{meta['family']}`\n"
        f"- Input modalities: `{', '.join(meta['input_modalities'])}`\n"
        f"- Output modalities: `{', '.join(meta['output_modalities'])}`\n"
        f"- Model families: `{', '.join(meta['model_families'])}`\n"
        f"- Node count: `{meta['node_count']}`\n"
        f"- Complexity score: `{meta['complexity_score']}`\n"
        f"- Resource profile: `{meta['resource_profile']}`\n"
        f"- Estimated runtime: `{meta['estimated_runtime']}`\n"
        f"- Max latent resolution hint: `{meta.get('max_width')}`x`{meta.get('max_height')}`\n"
        f"- Max sampler steps hint: `{meta.get('max_steps')}`\n\n"
        "## Detected Models\n\n"
        f"{model_lines}\n\n"
        "## Detected Custom Nodes\n\n"
        f"{custom_lines}\n\n"
        "## Runtime Warnings\n\n"
        f"{warn_lines}\n"
        f"{end}\n"
    )

    if start in text and end in text:
        pattern = re.compile(re.escape(start) + r".*?" + re.escape(end), flags=re.S)
        text = pattern.sub(block.strip(), text)
        text += "\n"
    else:
        if not text.endswith("\n"):
            text += "\n"
        text += block
    skill_md_path.write_text(text, encoding="utf-8")


def _load_skill_yaml(path):
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    return payload if isinstance(payload, dict) else {}


def _update_skill_yaml(path, meta):
    skill = _load_skill_yaml(path)
    requirements = skill.get("requirements")
    if not isinstance(requirements, dict):
        requirements = {}
    requirements.update(
        {
            "models": meta["models"],
            "custom_nodes": meta["custom_nodes"],
            "links": meta["links"][:50],
            "input_modalities": meta["input_modalities"],
            "output_modalities": meta["output_modalities"],
            "model_families": meta["model_families"],
            "node_count": meta["node_count"],
            "node_types": meta["node_types"],
        }
    )
    skill["requirements"] = requirements
    skill["selection_metadata"] = {
        "family": meta["family"],
        "resource_profile": meta["resource_profile"],
        "complexity_score": meta["complexity_score"],
        "estimated_runtime": meta["estimated_runtime"],
        "warnings": meta["warnings"],
        "max_width": meta["max_width"],
        "max_height": meta["max_height"],
        "max_steps": meta["max_steps"],
    }
    path.write_text(yaml.safe_dump(skill, sort_keys=False), encoding="utf-8")


def _source_name_from_skill_md(path):
    text = path.read_text(encoding="utf-8")
    m = re.search(r"imported from `(.+?)`", text, re.I)
    if m:
        return m.group(1).strip()
    m = re.search(r"Original:\s*`comfy-data/workflows/(.+?)`", text)
    if m:
        return m.group(1).strip()
    return None


def _iter_workflow_skill_dirs():
    for family_dir in sorted(WORKFLOWS_ROOT.iterdir()):
        if not family_dir.is_dir() or family_dir.name.startswith("_"):
            continue
        if family_dir.name not in FAMILY_DIRS:
            continue
        for skill_dir in sorted(family_dir.iterdir()):
            if not skill_dir.is_dir() or skill_dir.name.startswith("_"):
                continue
            if (skill_dir / "workflow.json").exists() and (skill_dir / "skill.yaml").exists() and (skill_dir / "SKILL.md").exists():
                yield family_dir.name, skill_dir


def _iter_non_wrapper_skill_dirs():
    for family_dir in sorted(WORKFLOWS_ROOT.iterdir()):
        if not family_dir.is_dir() or family_dir.name.startswith("_"):
            continue
        if family_dir.name not in FAMILY_DIRS:
            continue
        for skill_dir in sorted(family_dir.iterdir()):
            if not skill_dir.is_dir() or skill_dir.name.startswith("_"):
                continue
            if (skill_dir / "workflow.json").exists():
                continue
            if (skill_dir / "skill.yaml").exists() and (skill_dir / "SKILL.md").exists():
                yield family_dir.name, skill_dir


def _entry_from_skill_dir(family, skill_dir):
    skill_yaml = _load_skill_yaml(skill_dir / "skill.yaml")
    req = skill_yaml.get("requirements", {}) if isinstance(skill_yaml, dict) else {}
    sel = skill_yaml.get("selection_metadata", {}) if isinstance(skill_yaml, dict) else {}
    source_name = _source_name_from_skill_md(skill_dir / "SKILL.md")
    return {
        "id": skill_dir.name,
        "family": family,
        "title": skill_dir.name.replace("curated_", "").replace("workflow_", "").replace("_", " "),
        "destination": str(skill_dir),
        "source_path": f"comfy-data/workflows/{source_name}" if source_name else None,
        "input_modalities": req.get("input_modalities", []),
        "output_modalities": req.get("output_modalities", []),
        "model_families": req.get("model_families", []),
        "custom_nodes": req.get("custom_nodes", []),
        "links": req.get("links", []),
        "resource_profile": sel.get("resource_profile"),
        "complexity_score": sel.get("complexity_score"),
        "estimated_runtime": sel.get("estimated_runtime"),
        "warnings": sel.get("warnings", []),
    }


def _fallback_enrich_non_wrapper_skill(family, skill_dir):
    skill_yaml_path = skill_dir / "skill.yaml"
    skill_md_path = skill_dir / "SKILL.md"
    skill = _load_skill_yaml(skill_yaml_path)
    req = skill.get("requirements")
    if not isinstance(req, dict):
        req = {}
    req.setdefault("models", [])
    req.setdefault("custom_nodes", [])
    req.setdefault("links", [])
    req.setdefault("input_modalities", ["text_prompt"])
    req.setdefault("output_modalities", ["application/json"])
    req.setdefault("model_families", ["other"])
    req.setdefault("node_count", None)
    req.setdefault("node_types", [])
    skill["requirements"] = req
    skill["selection_metadata"] = {
        "family": family,
        "resource_profile": "unknown",
        "complexity_score": None,
        "estimated_runtime": "depends on runtime parameters and server resources",
        "warnings": [
            "Hand-authored skill (no embedded workflow.json); metadata is inferred and may be approximate."
        ],
        "max_width": None,
        "max_height": None,
        "max_steps": None,
    }
    skill_yaml_path.write_text(yaml.safe_dump(skill, sort_keys=False), encoding="utf-8")
    upsert_metadata_block(
        skill_md_path,
        {
            "family": family,
            "input_modalities": req["input_modalities"],
            "output_modalities": req["output_modalities"],
            "model_families": req["model_families"],
            "node_count": req["node_count"],
            "complexity_score": None,
            "resource_profile": "unknown",
            "estimated_runtime": "depends on runtime parameters and server resources",
            "max_width": None,
            "max_height": None,
            "max_steps": None,
            "models": req["models"],
            "custom_nodes": req["custom_nodes"],
            "warnings": [
                "Hand-authored skill (no embedded workflow.json); metadata is inferred and may be approximate."
            ],
        },
    )


def write_manifests(entries):
    curated = [e for e in entries if e["id"].startswith("curated_")]
    all_wrapped = [e for e in entries if e["id"].startswith("workflow_")]

    curated_path = WORKFLOWS_ROOT / "curated_manifest.json"
    all_path = WORKFLOWS_ROOT / "all_workflows_manifest.json"
    index_path = WORKFLOWS_ROOT / "skills_index.json"

    curated_path.write_text(
        json.dumps(
            {
                "generated_count": len(curated),
                "entries": curated,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    all_path.write_text(
        json.dumps(
            {
                "generated_count": len(all_wrapped),
                "entries": all_wrapped,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    index_path.write_text(
        json.dumps(
            {
                "generated_count": len(entries),
                "entries": entries,
            },
            indent=2,
        ),
        encoding="utf-8",
    )


def main():
    updated = 0
    fallback_updated = 0
    entries = []
    for family, skill_dir in _iter_workflow_skill_dirs():
        meta = analyze_workflow(family, skill_dir / "workflow.json")
        meta["family"] = family
        _update_skill_yaml(skill_dir / "skill.yaml", meta)
        upsert_metadata_block(skill_dir / "SKILL.md", meta)
        entries.append(_entry_from_skill_dir(family, skill_dir))
        updated += 1

    for family, skill_dir in _iter_non_wrapper_skill_dirs():
        _fallback_enrich_non_wrapper_skill(family, skill_dir)
        entries.append(_entry_from_skill_dir(family, skill_dir))
        fallback_updated += 1

    write_manifests(entries)
    print(
        json.dumps(
            {
                "updated_workflow_skills": updated,
                "updated_non_wrapper_skills": fallback_updated,
                "curated_count": len([e for e in entries if e["id"].startswith("curated_")]),
                "all_workflow_count": len([e for e in entries if e["id"].startswith("workflow_")]),
                "total_indexed_skills": len(entries),
                "skills_index": str(WORKFLOWS_ROOT / "skills_index.json"),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
