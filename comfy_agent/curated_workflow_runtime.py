import json
import os
import re
import uuid
from pathlib import Path

from .workflow import Workflow, requests


NEGATIVE_HINTS = (
    "negative",
    "worst quality",
    "low quality",
    "blurry",
    "watermark",
    "text,",
    "jpeg",
)


def _normalize_name(text):
    return re.sub(r"[^a-z0-9]+", "_", str(text).strip().lower()).strip("_")


def _resolve_headers(headers):
    if headers is not None:
        return headers
    auth_header = os.getenv("COMFY_AUTH_HEADER")
    if auth_header:
        return {"Authorization": auth_header}
    return None


def _registry_input_names(registry, class_type):
    info = registry.get(class_type, {})
    spec = info.get("input", {})
    required = spec.get("required", {})
    optional = spec.get("optional", {})
    required_names = list(required.keys()) if isinstance(required, dict) else []
    optional_names = list(optional.keys()) if isinstance(optional, dict) else []
    return required_names + optional_names


def _convert_exported_to_prompt(exported, registry):
    nodes = exported.get("nodes") or []
    links = exported.get("links") or []
    if not nodes:
        return {}

    link_map = {}
    for item in links:
        if isinstance(item, list) and len(item) >= 6:
            link_id = item[0]
            link_map[link_id] = {
                "origin_id": str(item[1]),
                "origin_slot": int(item[2]),
            }

    def _sort_key(node):
        if not isinstance(node, dict):
            return (10**9, 10**9)
        return (int(node.get("order", 10**9)), int(node.get("id", 10**9)))

    sorted_nodes = sorted(nodes, key=_sort_key)
    prompt = {}

    for node in sorted_nodes:
        if not isinstance(node, dict):
            continue

        node_id = str(node.get("id"))
        class_type = node.get("type")
        if not class_type:
            continue

        inputs = {}
        connected_names = set()
        for inp in node.get("inputs") or []:
            if not isinstance(inp, dict):
                continue
            name = inp.get("name")
            link_id = inp.get("link")
            if not name or link_id is None:
                continue
            link = link_map.get(link_id)
            if not link:
                continue
            inputs[name] = [link["origin_id"], link["origin_slot"]]
            connected_names.add(name)

        widget_values = node.get("widgets_values")
        allowed_names = _registry_input_names(registry, class_type)
        assignable = [name for name in allowed_names if name not in connected_names]

        if isinstance(widget_values, dict):
            for key, value in widget_values.items():
                if key in allowed_names:
                    inputs[key] = value
        elif isinstance(widget_values, list):
            idx = 0
            for name in assignable:
                if idx >= len(widget_values):
                    break
                inputs[name] = widget_values[idx]
                idx += 1
            # Compatibility shim: older KSampler exports included control_after_generate
            # in widget values, which newer schemas no longer expose.
            if (
                class_type == "KSampler"
                and len(widget_values) >= 7
                and isinstance(inputs.get("steps"), str)
                and isinstance(widget_values[2], (int, float))
            ):
                inputs["seed"] = int(widget_values[0])
                inputs["steps"] = int(widget_values[2])
                inputs["cfg"] = float(widget_values[3])
                inputs["sampler_name"] = widget_values[4]
                inputs["scheduler"] = widget_values[5]
                inputs["denoise"] = float(widget_values[6])
            # Compatibility shim: some server versions removed StabilityTextToAudio seed mode,
            # so exported widget order may shift and place "randomize" into steps.
            if (
                class_type == "StabilityTextToAudio"
                and len(widget_values) >= 6
                and isinstance(inputs.get("steps"), str)
                and isinstance(widget_values[-1], (int, float))
            ):
                inputs["steps"] = int(widget_values[-1])
        elif widget_values is not None and assignable:
            inputs[assignable[0]] = widget_values

        prompt[node_id] = {"class_type": class_type, "inputs": inputs}

    return prompt


def _is_probably_negative(text):
    lowered = str(text or "").lower()
    return any(token in lowered for token in NEGATIVE_HINTS)


def _apply_overrides(prompt_map, overrides):
    if not isinstance(prompt_map, dict) or not prompt_map:
        return prompt_map

    prompt = overrides.get("prompt")
    negative_prompt = overrides.get("negative_prompt")
    width = overrides.get("width")
    height = overrides.get("height")
    seed = overrides.get("seed")
    steps = overrides.get("steps")
    cfg = overrides.get("cfg")
    sampler_name = overrides.get("sampler_name")
    scheduler = overrides.get("scheduler")
    denoise = overrides.get("denoise")

    clip_nodes = []
    for node_id, node in prompt_map.items():
        if node.get("class_type") != "CLIPTextEncode":
            continue
        text_value = (node.get("inputs") or {}).get("text")
        clip_nodes.append((node_id, text_value))

    if prompt is not None and clip_nodes:
        positive_target = None
        for node_id, text_value in clip_nodes:
            if not _is_probably_negative(text_value):
                positive_target = node_id
                break
        if positive_target is None:
            positive_target = clip_nodes[0][0]
        prompt_map[positive_target]["inputs"]["text"] = prompt

    if negative_prompt is not None and clip_nodes:
        negative_target = None
        for node_id, text_value in clip_nodes:
            if _is_probably_negative(text_value):
                negative_target = node_id
                break
        if negative_target is None and len(clip_nodes) > 1:
            negative_target = clip_nodes[1][0]
        if negative_target is None:
            negative_target = clip_nodes[0][0]
        prompt_map[negative_target]["inputs"]["text"] = negative_prompt

    # Audio text conditioning compatibility for AceStep nodes.
    if prompt is not None:
        for node in prompt_map.values():
            if node.get("class_type") in {"TextEncodeAceStepAudio", "TextEncodeAceStepAudio1.5"}:
                inputs = node.get("inputs") or {}
                if "lyrics" in inputs:
                    inputs["lyrics"] = prompt
                elif "text" in inputs:
                    inputs["text"] = prompt
                elif "prompt" in inputs:
                    inputs["prompt"] = prompt

    for node in prompt_map.values():
        class_type = node.get("class_type")
        inputs = node.get("inputs") or {}

        if width is not None and "width" in inputs:
            inputs["width"] = int(width)
        if height is not None and "height" in inputs:
            inputs["height"] = int(height)

        if class_type and class_type.lower().startswith("ksampler"):
            if seed is not None and "seed" in inputs:
                inputs["seed"] = int(seed)
            if steps is not None and "steps" in inputs:
                inputs["steps"] = int(steps)
            if cfg is not None and "cfg" in inputs:
                inputs["cfg"] = float(cfg)
            if sampler_name is not None and "sampler_name" in inputs:
                inputs["sampler_name"] = sampler_name
            if scheduler is not None and "scheduler" in inputs:
                inputs["scheduler"] = scheduler
            if denoise is not None and "denoise" in inputs:
                inputs["denoise"] = float(denoise)

    return prompt_map


def _prune_unsupported_nodes(prompt_map, registry):
    if not isinstance(prompt_map, dict) or not prompt_map:
        return prompt_map

    supported = set(registry.keys()) if isinstance(registry, dict) else set()
    pruned = dict(prompt_map)

    def _collect_refs(node_inputs):
        refs = set()
        if isinstance(node_inputs, dict):
            stack = list(node_inputs.values())
        else:
            stack = []
        while stack:
            value = stack.pop()
            if isinstance(value, list) and len(value) == 2 and str(value[0]).isdigit():
                refs.add(str(value[0]))
                continue
            if isinstance(value, dict):
                stack.extend(value.values())
                continue
            if isinstance(value, (list, tuple)):
                stack.extend(value)
        return refs

    changed = True
    while changed:
        changed = False
        referenced = set()
        for node in pruned.values():
            referenced.update(_collect_refs((node or {}).get("inputs", {})))

        for node_id, node in list(pruned.items()):
            class_type = str((node or {}).get("class_type") or "")
            if class_type in supported:
                continue
            # Safe prune only when node is not referenced by any other node.
            if str(node_id) in referenced:
                continue
            pruned.pop(node_id, None)
            changed = True

    return pruned


def run_curated_workflow(
    workflow_path,
    server=None,
    headers=None,
    api_prefix=None,
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
):
    wf = Workflow(
        server=server or os.getenv("COMFY_URL"),
        headers=_resolve_headers(headers),
        api_prefix=api_prefix,
    )

    exported = json.loads(Path(workflow_path).read_text(encoding="utf-8"))
    prompt_map = _convert_exported_to_prompt(exported, wf.registry)
    prompt_map = _prune_unsupported_nodes(prompt_map, wf.registry)
    prompt_map = _apply_overrides(
        prompt_map,
        {
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "width": width,
            "height": height,
            "seed": seed,
            "steps": steps,
            "cfg": cfg,
            "sampler_name": sampler_name,
            "scheduler": scheduler,
            "denoise": denoise,
        },
    )

    payload = {"prompt": prompt_map, "client_id": str(uuid.uuid4())}
    response = requests.post(f"{wf.url}/prompt", json=payload, headers=wf.headers)
    if not response.ok:
        message = f"ComfyUI prompt request failed with {response.status_code}"
        try:
            detail = response.json()
            message += f": {json.dumps(detail, indent=2)}"
        except ValueError:
            message += f": {response.text}"
        raise requests.HTTPError(message, response=response)

    result = response.json()
    prompt_id = result.get("prompt_id")
    wf.last_prompt_id = prompt_id
    outputs = wf.saved_images(prompt_id) if prompt_id else []

    return {
        "status": "done",
        "prompt_id": prompt_id,
        "output_images": outputs,
        "source_workflow": str(Path(workflow_path)),
    }


def slugify(text):
    normalized = _normalize_name(text)
    if normalized:
        return normalized
    return "workflow"
