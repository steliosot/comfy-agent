#!/usr/bin/env python3
import argparse
import json
import re
import shutil
import sys
from collections import defaultdict, deque
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from comfy_agent.curated_workflow_runtime import slugify


SOURCE_DIR = REPO_ROOT / "comfy-data" / "workflows"
DEST_ROOT = REPO_ROOT / "skills" / "curated_workflows"

FAMILY_QUOTAS = {
    "txt2img": 28,
    "img2img_inpaint_outpaint": 22,
    "editing_restyle": 18,
    "video_t2v_i2v_avatar": 28,
    "upscaling": 14,
    "audio": 10,
}

MODEL_TOKENS = (
    "flux",
    "sdxl",
    "wan",
    "ltx",
    "qwen",
    "z_image_turbo",
    "other",
)


def _extract_urls(text):
    if not text:
        return []
    return sorted(set(re.findall(r"https?://[^\s)\]>\"']+", str(text))))


def _normalize_variant_name(name):
    text = name.lower()
    text = re.sub(r"\b\d{3,4}x\d{3,4}px?\b", " ", text)
    text = re.sub(r"\b(landscape|portrait|square|fullhd|2k|4k|update|compact|ultra compact)\b", " ", text)
    text = re.sub(r"\b(ep|episode)\s*\d+\b", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _as_text(widget_values):
    if isinstance(widget_values, str):
        return widget_values
    if isinstance(widget_values, list):
        return " ".join(str(v) for v in widget_values if isinstance(v, (str, int, float, bool)))
    if isinstance(widget_values, dict):
        return " ".join(str(v) for v in widget_values.values())
    return ""


def _infer_family(name, node_types):
    text = name.lower()
    if any(token in text for token in ("music", "audio", "voice", "acestep")):
        return "audio"
    if (
        "video" in text
        or "i2v" in text
        or "t2v" in text
        or "ltx" in text
        or "wan " in f"{text} "
        or "liveportrait" in text
        or "VHS_VideoCombine" in node_types
    ):
        return "video_t2v_i2v_avatar"
    if "upscale" in text or "upscaler" in text or "ImageUpscaleWithModel" in node_types:
        return "upscaling"
    if any(token in text for token in ("inpaint", "outpaint", "img2img", "i2i", "variation", "retouch")):
        return "img2img_inpaint_outpaint"
    if any(token in text for token in ("edit", "replace", "remove", "logo", "branding", "product placement", "colorize", "style")):
        return "editing_restyle"
    return "txt2img"


def _infer_model_families(name, node_types):
    text = name.lower()
    families = set()
    if "flux" in text or "FluxGuidance" in node_types:
        families.add("flux")
    if "sdxl" in text:
        families.add("sdxl")
    if " wan" in f" {text}" or "wan" in text or "EmptyHunyuanLatentVideo" in node_types:
        families.add("wan")
    if "ltx" in text:
        families.add("ltx")
    if "qwen" in text:
        families.add("qwen")
    if "z image turbo" in text or "z-image-turbo" in text or "z_image_turbo" in text:
        families.add("z_image_turbo")
    if not families:
        families.add("other")
    return sorted(families)


def _extract_requirements(nodes):
    model_reqs = []
    cnr_ids = set()
    links = set()
    node_types = []
    input_modalities = set()
    output_modalities = set()

    for node in nodes:
        if not isinstance(node, dict):
            continue
        node_type = node.get("type", "")
        node_types.append(node_type)
        props = node.get("properties") or {}
        cnr_id = props.get("cnr_id")
        if cnr_id and cnr_id != "comfy-core":
            cnr_ids.add(str(cnr_id))

        text_blob = _as_text(node.get("widgets_values"))
        for url in _extract_urls(text_blob):
            links.add(url)

        widgets = node.get("widgets_values")
        first = None
        if isinstance(widgets, list) and widgets:
            first = widgets[0]

        if node_type in {"CheckpointLoaderSimple"} and isinstance(first, str):
            model_reqs.append({"type": "checkpoint", "name": first, "target_folder": "models/checkpoints"})
        if node_type in {"VAELoader"} and isinstance(first, str):
            model_reqs.append({"type": "vae", "name": first, "target_folder": "models/vae"})
        if node_type in {"CLIPLoader", "DualCLIPLoaderGGUF"} and isinstance(first, str):
            model_reqs.append({"type": "clip", "name": first, "target_folder": "models/clip"})
        if node_type in {"UNETLoader", "UnetLoaderGGUF"} and isinstance(first, str):
            model_reqs.append({"type": "diffusion_model", "name": first, "target_folder": "models/diffusion_models"})
        if node_type in {"LoraLoaderModelOnly", "LoraLoader"} and isinstance(first, str):
            model_reqs.append({"type": "lora", "name": first, "target_folder": "models/loras"})
        if node_type in {"ControlNetLoader"} and isinstance(first, str):
            model_reqs.append({"type": "controlnet", "name": first, "target_folder": "models/controlnet"})
        if node_type in {"UpscaleModelLoader"} and isinstance(first, str):
            model_reqs.append({"type": "upscale_model", "name": first, "target_folder": "models/upscale_models"})

        lower_type = node_type.lower()
        if "loadimage" in lower_type:
            input_modalities.add("image")
        if "loadvideo" in lower_type:
            input_modalities.add("video")
        if node_type == "CLIPTextEncode":
            input_modalities.add("text_prompt")

        if node_type in {"SaveImage", "PreviewImage", "Image Comparer (rgthree)"}:
            output_modalities.add("image/png")
        if node_type in {"VHS_VideoCombine", "SaveVideo"}:
            output_modalities.add("video/mp4")
        if "audio" in lower_type:
            output_modalities.add("audio/wav")

    deduped_models = []
    seen = set()
    for item in model_reqs:
        key = (item["type"], item["name"])
        if key in seen:
            continue
        seen.add(key)
        deduped_models.append(item)

    if not output_modalities:
        output_modalities.add("application/json")

    return {
        "model_requirements": deduped_models,
        "custom_nodes": sorted(cnr_ids),
        "links": sorted(links),
        "node_types": sorted(set(node_types)),
        "input_modalities": sorted(input_modalities) or ["text_prompt"],
        "output_modalities": sorted(output_modalities),
    }


def _score_candidate(meta):
    score = 0.0
    score += 2.0 * len(meta["model_families"])
    score += 1.3 * len(meta["requirements"]["model_requirements"])
    score += 1.2 * len(meta["requirements"]["custom_nodes"])
    score += 0.7 * len(meta["requirements"]["links"])
    score += 2.0 if "SaveImage" in meta["requirements"]["node_types"] else 0
    score += 2.0 if "VHS_VideoCombine" in meta["requirements"]["node_types"] else 0
    score += 1.0 if "ControlNetLoader" in meta["requirements"]["node_types"] else 0
    score += 1.0 if "LoraLoaderModelOnly" in meta["requirements"]["node_types"] else 0
    return score


def _collect_candidates():
    candidates = []
    for path in sorted(SOURCE_DIR.glob("*.json")):
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            continue
        nodes = payload.get("nodes") or []
        node_types = {n.get("type", "") for n in nodes if isinstance(n, dict)}
        name = path.stem
        family = _infer_family(name, node_types)
        requirements = _extract_requirements(nodes)
        model_families = _infer_model_families(name, requirements["node_types"])
        meta = {
            "source_path": str(path),
            "source_name": path.name,
            "title": name,
            "family": family,
            "model_families": model_families,
            "dedupe_key": _normalize_variant_name(name),
            "requirements": requirements,
        }
        meta["score"] = _score_candidate(meta)
        candidates.append(meta)
    return candidates


def _dedupe_candidates(candidates):
    by_key = {}
    for item in candidates:
        key = (item["family"], item["dedupe_key"])
        prev = by_key.get(key)
        if prev is None or item["score"] > prev["score"]:
            by_key[key] = item
    return list(by_key.values())


def _select_with_quotas(candidates, limit):
    by_family = defaultdict(list)
    for item in candidates:
        by_family[item["family"]].append(item)
    for family in by_family:
        by_family[family].sort(key=lambda x: (x["score"], x["title"]), reverse=True)

    selected = []
    used_sources = set()

    for family, quota in FAMILY_QUOTAS.items():
        family_items = by_family.get(family, [])
        buckets = defaultdict(deque)
        for item in family_items:
            primary = item["model_families"][0] if item["model_families"] else "other"
            buckets[primary].append(item)
        bucket_names = [token for token in MODEL_TOKENS if token in buckets] or list(buckets.keys())

        family_selected = 0
        idx = 0
        while family_selected < quota and bucket_names:
            bucket = bucket_names[idx % len(bucket_names)]
            queue = buckets[bucket]
            picked = None
            while queue:
                candidate = queue.popleft()
                if candidate["source_path"] in used_sources:
                    continue
                picked = candidate
                break
            if picked:
                selected.append(picked)
                used_sources.add(picked["source_path"])
                family_selected += 1
            else:
                bucket_names = [b for b in bucket_names if buckets[b]]
                if not bucket_names:
                    break
                idx = 0
                continue
            idx += 1

        if family_selected < quota:
            leftovers = [x for x in family_items if x["source_path"] not in used_sources]
            for item in leftovers[: quota - family_selected]:
                selected.append(item)
                used_sources.add(item["source_path"])

    if len(selected) < limit:
        leftovers = sorted(
            [x for x in candidates if x["source_path"] not in used_sources],
            key=lambda x: (x["score"], x["title"]),
            reverse=True,
        )
        for item in leftovers[: limit - len(selected)]:
            selected.append(item)
            used_sources.add(item["source_path"])

    return selected[:limit]


def _family_category(family):
    if family in {"img2img_inpaint_outpaint", "editing_restyle", "upscaling"}:
        return "media-editing"
    if family == "audio":
        return "media-generation"
    return "media-generation"


def _default_output_type(outputs):
    if any("video" in x for x in outputs):
        return "video/mp4"
    if any("audio" in x for x in outputs):
        return "audio/wav"
    if any("image" in x for x in outputs):
        return "image/png"
    return "application/json"


def _default_input_type(inputs):
    if "image" in inputs:
        return "image/png"
    if "video" in inputs:
        return "video/mp4"
    return "text"


def _write_skill_files(dest_dir, skill_name, family, meta):
    requirements = meta["requirements"]
    output_type = _default_output_type(requirements["output_modalities"])
    input_type = _default_input_type(requirements["input_modalities"])
    category = _family_category(family)
    links = requirements["links"]
    models = requirements["model_requirements"]
    custom_nodes = requirements["custom_nodes"]

    frontmatter = f"""---
name: {skill_name}
description: >
  Curated ComfyUI workflow imported from `{meta["source_name"]}`.
homepage: https://github.com/steliosot/comfy-agent
metadata.clawdbot.os: ["darwin", "linux"]
metadata.clawdbot.requires.bins: ["python3"]
metadata.clawdbot.requires.env: ["COMFY_URL", "COMFY_AUTH_HEADER"]
metadata.clawdbot.files: ["workflow.json", "skill.py", "skill.yaml", "scripts/*"]
metadata.clawdbot.tags: ["comfyui", "workflow", "curated", "{family}"]
metadata.clawdbot.category: "{category}"
metadata.clawdbot.input_type: "{input_type}"
metadata.clawdbot.output_type: "{output_type}"
metadata.clawdbot.output_can_feed_into: []
metadata.clawdbot.accepts_input_from: []
metadata.clawdbot.priority: 70
---
"""

    model_lines = "\n".join(
        f"- `{item['type']}`: `{item['name']}` -> `{item['target_folder']}`" for item in models
    ) or "- None detected from loader nodes."
    custom_lines = "\n".join(f"- `{item}`" for item in custom_nodes) or "- None detected."
    links_lines = "\n".join(f"- {link}" for link in links[:30]) or "- None detected."

    skill_md = f"""{frontmatter}
# {skill_name}

Curated workflow skill generated from `{meta["source_name"]}`.

## Capability Family

- `{family}`

## Inputs

- Optional runtime overrides supported by `run(...)`:
  - `prompt`
  - `negative_prompt`
  - `width`, `height`
  - `seed`, `steps`, `cfg`
  - `sampler_name`, `scheduler`, `denoise`
  - `server`, `headers`, `api_prefix`

## Outputs

- Returns JSON with:
  - `status`
  - `prompt_id`
  - `output_images` (includes image/video entries reported by Comfy history)

## Model Requirements

{model_lines}

## Custom Node Requirements

{custom_lines}

## Links Extracted From Workflow Notes

{links_lines}

## Source

- Original: `comfy-data/workflows/{meta["source_name"]}`
"""

    skill_yaml = {
        "name": skill_name,
        "description": f"Curated workflow wrapper for {meta['source_name']}",
        "inputs": {
            "prompt": {"type": "string", "required": False},
            "negative_prompt": {"type": "string", "required": False},
            "width": {"type": "integer", "required": False},
            "height": {"type": "integer", "required": False},
            "seed": {"type": "integer", "required": False},
            "steps": {"type": "integer", "required": False},
            "cfg": {"type": "number", "required": False},
            "sampler_name": {"type": "string", "required": False},
            "scheduler": {"type": "string", "required": False},
            "denoise": {"type": "number", "required": False},
            "server": {"type": "string", "required": False},
            "headers": {"type": "object", "required": False},
            "api_prefix": {"type": "string", "required": False},
        },
        "outputs": {
            "status": {"type": "string"},
            "prompt_id": {"type": "string"},
            "output_images": {"type": "array"},
        },
        "requirements": {
            "models": models,
            "custom_nodes": custom_nodes,
            "links": links[:30],
            "input_modalities": requirements["input_modalities"],
            "output_modalities": requirements["output_modalities"],
        },
    }

    skill_py = f"""from pathlib import Path

from comfy_agent.curated_workflow_runtime import run_curated_workflow


WORKFLOW_PATH = Path(__file__).with_name("workflow.json")


def run(
    prompt=None,
    negative_prompt=None,
    width=None,
    height=None,
    seed=None,
    steps=None,
    cfg=None,
    sampler_name=None,
    scheduler=None,
    denoise=None,
    server=None,
    headers=None,
    api_prefix=None,
):
    return run_curated_workflow(
        workflow_path=WORKFLOW_PATH,
        server=server,
        headers=headers,
        api_prefix=api_prefix,
        prompt=prompt,
        negative_prompt=negative_prompt,
        width=width,
        height=height,
        seed=seed,
        steps=steps,
        cfg=cfg,
        sampler_name=sampler_name,
        scheduler=scheduler,
        denoise=denoise,
    )
"""

    run_py = f"""#!/usr/bin/env python3
\"\"\"CLI wrapper for skills.curated_workflows.{family}.{skill_name}.skill.run\"\"\"

import argparse
import json
import sys
from pathlib import Path


THIS = Path(__file__).resolve()
REPO_ROOT = THIS.parents[4]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from skills.curated_workflows.{family}.{skill_name}.skill import run


def main():
    parser = argparse.ArgumentParser(description="Run curated workflow skill: {skill_name}")
    parser.add_argument("--args", default="{{}}", help="JSON object with kwargs for run(...)")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output")
    args = parser.parse_args()

    try:
        kwargs = json.loads(args.args)
    except json.JSONDecodeError as exc:
        print(f"Invalid --args JSON: {{exc}}", file=sys.stderr)
        sys.exit(2)

    if not isinstance(kwargs, dict):
        print("--args must decode to a JSON object", file=sys.stderr)
        sys.exit(2)

    result = run(**kwargs)
    if args.pretty:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(json.dumps(result))


if __name__ == "__main__":
    main()
"""

    (dest_dir / "SKILL.md").write_text(skill_md, encoding="utf-8")
    (dest_dir / "skill.yaml").write_text(yaml.safe_dump(skill_yaml, sort_keys=False), encoding="utf-8")
    (dest_dir / "skill.py").write_text(skill_py, encoding="utf-8")
    scripts_dir = dest_dir / "scripts"
    scripts_dir.mkdir(exist_ok=True)
    run_path = scripts_dir / "run.py"
    run_path.write_text(run_py, encoding="utf-8")
    run_path.chmod(0o755)


def _write_catalog(selected):
    by_family = defaultdict(list)
    for item in selected:
        by_family[item["family"]].append(item)

    lines = ["# Curated Workflows", "", "This folder contains curated ComfyUI workflows wrapped as OpenClaw skills.", ""]
    for family in sorted(by_family.keys()):
        lines.append(f"## {family}")
        lines.append("")
        for item in sorted(by_family[family], key=lambda x: x["title"].lower()):
            lines.append(f"- `{item['id']}`: {item['title']}")
        lines.append("")
    (DEST_ROOT / "README.md").write_text("\n".join(lines).strip() + "\n", encoding="utf-8")

    manifest = {
        "generated_count": len(selected),
        "source_dir": str(SOURCE_DIR),
        "destination_root": str(DEST_ROOT),
        "entries": selected,
    }
    (DEST_ROOT / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def reindex_existing():
    entries = []
    for family_dir in sorted(DEST_ROOT.iterdir()):
        if not family_dir.is_dir() or family_dir.name.startswith("_"):
            continue
        family = family_dir.name
        for skill_dir in sorted(family_dir.iterdir()):
            if not skill_dir.is_dir():
                continue
            skill_id = skill_dir.name
            source_name = None
            skill_md = skill_dir / "SKILL.md"
            if skill_md.exists():
                text = skill_md.read_text(encoding="utf-8")
                match = re.search(r"Original:\s*`comfy-data/workflows/(.+?)`", text)
                if match:
                    source_name = match.group(1).strip()

            skill_yaml = {}
            skill_yaml_path = skill_dir / "skill.yaml"
            if skill_yaml_path.exists():
                skill_yaml = yaml.safe_load(skill_yaml_path.read_text(encoding="utf-8")) or {}

            req = skill_yaml.get("requirements", {}) if isinstance(skill_yaml, dict) else {}
            entries.append(
                {
                    "id": skill_id,
                    "family": family,
                    "title": skill_id.replace("curated_", "").replace("_", " "),
                    "score": None,
                    "source_path": f"comfy-data/workflows/{source_name}" if source_name else None,
                    "destination": str(skill_dir),
                    "model_families": [],
                    "input_modalities": req.get("input_modalities", []),
                    "output_modalities": req.get("output_modalities", []),
                    "custom_nodes": req.get("custom_nodes", []),
                    "links": req.get("links", []),
                }
            )
    _write_catalog(entries)
    return entries


def build(limit=120, dry_run=False):
    candidates = _collect_candidates()
    deduped = _dedupe_candidates(candidates)
    selected = _select_with_quotas(deduped, limit=limit)

    if not dry_run:
        DEST_ROOT.mkdir(parents=True, exist_ok=True)
        (DEST_ROOT / "__init__.py").write_text("", encoding="utf-8")

    final_entries = []
    for item in selected:
        family = item["family"]
        source_path = Path(item["source_path"])
        skill_name = f"curated_{slugify(item['title'])}"
        dest_dir = DEST_ROOT / family / skill_name
        dest_json = dest_dir / "workflow.json"

        manifest_entry = {
            "id": skill_name,
            "family": family,
            "title": item["title"],
            "score": item["score"],
            "source_path": str(source_path),
            "destination": str(dest_dir),
            "model_families": item["model_families"],
            "input_modalities": item["requirements"]["input_modalities"],
            "output_modalities": item["requirements"]["output_modalities"],
            "custom_nodes": item["requirements"]["custom_nodes"],
            "links": item["requirements"]["links"][:30],
        }
        final_entries.append(manifest_entry)

        if dry_run:
            continue

        dest_dir.mkdir(parents=True, exist_ok=True)
        (DEST_ROOT / family / "__init__.py").write_text("", encoding="utf-8")
        (dest_dir / "__init__.py").write_text("", encoding="utf-8")
        shutil.move(str(source_path), str(dest_json))
        _write_skill_files(dest_dir, skill_name=skill_name, family=family, meta=item)

    if not dry_run:
        _write_catalog(final_entries)

    return final_entries


def main():
    parser = argparse.ArgumentParser(description="Build curated workflow skills by moving selected workflow JSON files.")
    parser.add_argument("--limit", type=int, default=120, help="Number of curated workflows to move and wrap.")
    parser.add_argument("--dry-run", action="store_true", help="Preview selection without moving files.")
    parser.add_argument("--reindex", action="store_true", help="Rebuild manifest + README from existing curated folders.")
    args = parser.parse_args()

    if args.reindex:
        entries = reindex_existing()
        print(json.dumps({"selected": len(entries), "reindex": True}, indent=2))
        return

    entries = build(limit=args.limit, dry_run=args.dry_run)
    print(json.dumps({"selected": len(entries), "dry_run": args.dry_run}, indent=2))


if __name__ == "__main__":
    main()
