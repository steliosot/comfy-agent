#!/usr/bin/env python3
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from comfy_agent.curated_workflow_runtime import slugify


SOURCE_DIR = REPO_ROOT / "comfy-data" / "workflows"
DEST_ROOT = REPO_ROOT / "skills" / "workflows"


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
    if any(
        token in text for token in ("edit", "replace", "remove", "logo", "branding", "product placement", "colorize", "style")
    ):
        return "editing_restyle"
    return "txt2img"


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


def _write_skill_files(dest_dir, skill_name, family, source_name, requirements):
    output_type = _default_output_type(requirements["output_modalities"])
    input_type = _default_input_type(requirements["input_modalities"])
    links = requirements["links"]
    models = requirements["model_requirements"]
    custom_nodes = requirements["custom_nodes"]

    frontmatter = f"""---
name: {skill_name}
description: >
  Workflow wrapper imported from `{source_name}`.
homepage: https://github.com/steliosot/comfy-agent
metadata.clawdbot.os: ["darwin", "linux"]
metadata.clawdbot.requires.bins: ["python3"]
metadata.clawdbot.requires.env: ["COMFY_URL", "COMFY_AUTH_HEADER"]
metadata.clawdbot.files: ["workflow.json", "skill.py", "skill.yaml", "scripts/*"]
metadata.clawdbot.tags: ["comfyui", "workflow", "library", "{family}"]
metadata.clawdbot.category: "media-generation"
metadata.clawdbot.input_type: "{input_type}"
metadata.clawdbot.output_type: "{output_type}"
metadata.clawdbot.output_can_feed_into: []
metadata.clawdbot.accepts_input_from: []
metadata.clawdbot.priority: 60
---
"""

    model_lines = "\n".join(
        f"- `{item['type']}`: `{item['name']}` -> `{item['target_folder']}`" for item in models
    ) or "- None detected from loader nodes."
    custom_lines = "\n".join(f"- `{item}`" for item in custom_nodes) or "- None detected."
    links_lines = "\n".join(f"- {link}" for link in links[:30]) or "- None detected."

    skill_md = f"""{frontmatter}
# {skill_name}

Imported workflow skill generated from `{source_name}`.

## Family

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
  - `output_images`

## Model Requirements

{model_lines}

## Custom Node Requirements

{custom_lines}

## Links

{links_lines}
"""

    skill_yaml = {
        "name": skill_name,
        "description": f"Workflow wrapper for {source_name}",
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

    skill_py = """from pathlib import Path

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
import argparse
import json
import sys
from pathlib import Path


THIS = Path(__file__).resolve()
REPO_ROOT = THIS.parents[4]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from skills.workflows.{family}.{skill_name}.skill import run


def main():
    parser = argparse.ArgumentParser(description="Run workflow skill: {skill_name}")
    parser.add_argument("--args", default="{{}}", help="JSON object with kwargs for run(...)")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output")
    args = parser.parse_args()

    kwargs = json.loads(args.args)
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


def _write_catalog(entries):
    by_family = defaultdict(list)
    for item in entries:
        by_family[item["family"]].append(item)

    lines = [
        "# All Workflow Skills",
        "",
        "Auto-generated wrappers for every JSON in `comfy-data/workflows`.",
        "",
    ]
    for family in sorted(by_family.keys()):
        lines.append(f"## {family}")
        lines.append("")
        for item in sorted(by_family[family], key=lambda x: x["title"].lower()):
            lines.append(f"- `{item['id']}`: {item['title']}")
        lines.append("")
    (DEST_ROOT / "all_workflows_README.md").write_text("\n".join(lines).strip() + "\n", encoding="utf-8")
    (DEST_ROOT / "all_workflows_manifest.json").write_text(
        json.dumps({"generated_count": len(entries), "entries": entries}, indent=2), encoding="utf-8"
    )


def build():
    DEST_ROOT.mkdir(parents=True, exist_ok=True)
    (DEST_ROOT / "__init__.py").write_text("", encoding="utf-8")

    entries = []
    slug_counts = defaultdict(int)
    for src in sorted(SOURCE_DIR.glob("*.json")):
        payload = json.loads(src.read_text(encoding="utf-8"))
        nodes = payload.get("nodes") or []
        node_types = {n.get("type", "") for n in nodes if isinstance(n, dict)}
        family = _infer_family(src.stem, node_types)
        base_slug = f"workflow_{slugify(src.stem)}"
        slug_counts[(family, base_slug)] += 1
        if slug_counts[(family, base_slug)] > 1:
            skill_name = f"{base_slug}_{slug_counts[(family, base_slug)]}"
        else:
            skill_name = base_slug

        family_dir = DEST_ROOT / family
        family_dir.mkdir(parents=True, exist_ok=True)
        (family_dir / "__init__.py").write_text("", encoding="utf-8")
        dest_dir = family_dir / skill_name
        dest_dir.mkdir(parents=True, exist_ok=True)
        (dest_dir / "__init__.py").write_text("", encoding="utf-8")
        (dest_dir / "workflow.json").write_text(src.read_text(encoding="utf-8"), encoding="utf-8")

        requirements = _extract_requirements(nodes)
        _write_skill_files(dest_dir, skill_name=skill_name, family=family, source_name=src.name, requirements=requirements)

        entries.append(
            {
                "id": skill_name,
                "title": src.stem,
                "family": family,
                "source_path": str(src),
                "destination": str(dest_dir),
                "custom_nodes": requirements["custom_nodes"],
                "links": requirements["links"][:30],
                "input_modalities": requirements["input_modalities"],
                "output_modalities": requirements["output_modalities"],
            }
        )

    _write_catalog(entries)
    return entries


def main():
    entries = build()
    print(json.dumps({"generated": len(entries), "destination": str(DEST_ROOT)}, indent=2))


if __name__ == "__main__":
    main()
