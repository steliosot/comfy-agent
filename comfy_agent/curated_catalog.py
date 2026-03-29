import json
import re
from pathlib import Path


def _repo_root():
    return Path(__file__).resolve().parents[1]


def curated_manifest_path():
    return _repo_root() / "skills" / "curated_workflows" / "manifest.json"


def load_curated_manifest():
    path = curated_manifest_path()
    if not path.exists():
        return {"generated_count": 0, "entries": []}
    return json.loads(path.read_text(encoding="utf-8"))


def _tokens(text):
    return {t for t in re.findall(r"[a-z0-9]+", str(text).lower()) if len(t) > 1}


def _derive_model_families(entry):
    explicit = entry.get("model_families") or []
    if explicit:
        return [str(x).lower() for x in explicit]

    probe = " ".join(
        [
            str(entry.get("title", "")),
            str(entry.get("id", "")),
            " ".join(str(x) for x in entry.get("links", [])),
            " ".join(str(x) for x in entry.get("custom_nodes", [])),
        ]
    ).lower()

    families = []
    for key in ("flux", "sdxl", "wan", "ltx", "qwen", "z_image_turbo"):
        if key.replace("_", " ") in probe or key in probe:
            families.append(key)
    if not families:
        families.append("other")
    return families


def _family_from_prompt(prompt):
    text = str(prompt or "").lower()
    if any(k in text for k in ("music", "audio", "voice", "song", "lyrics")):
        return "audio"
    if any(k in text for k in ("video", "animation", "i2v", "t2v", "avatar", "talking")):
        return "video_t2v_i2v_avatar"
    if any(k in text for k in ("upscale", "upscaler", "super resolution")):
        return "upscaling"
    if any(k in text for k in ("inpaint", "outpaint", "img2img", "i2i", "variation", "retouch")):
        return "img2img_inpaint_outpaint"
    if any(k in text for k in ("edit", "replace", "remove", "colorize", "style", "branding")):
        return "editing_restyle"
    return "txt2img"


def match_curated_entries(
    prompt,
    entries,
    top_k=5,
    family=None,
    input_modality=None,
    output_modality=None,
    model_family=None,
):
    query = _tokens(prompt)
    prompt_text = str(prompt or "").lower()
    preferred_family = family or _family_from_prompt(prompt)
    requested_model_family = str(model_family).lower() if model_family else None
    requested_input = str(input_modality).lower() if input_modality else None
    requested_output = str(output_modality).lower() if output_modality else None

    ranked = []
    for entry in entries:
        entry_family = str(entry.get("family", "txt2img"))
        title = str(entry.get("title", ""))
        entry_tokens = _tokens(f"{title} {entry.get('id', '')}")
        overlap = len(query & entry_tokens)

        score = 0.15 + (overlap * 0.08)
        reasons = []

        if entry_family == preferred_family:
            score += 0.45
            reasons.append(f"Matches requested family `{preferred_family}`.")

        families = _derive_model_families(entry)
        if requested_model_family and requested_model_family in families:
            score += 0.18
            reasons.append(f"Matches model family `{requested_model_family}`.")
        elif any(k in str(prompt).lower() for k in ("flux", "sdxl", "wan", "ltx", "qwen")):
            hinted = [k for k in ("flux", "sdxl", "wan", "ltx", "qwen") if k in str(prompt).lower()]
            if hinted and any(h in families for h in hinted):
                score += 0.15
                reasons.append(f"Matches prompt model hints `{', '.join(hinted)}`.")

        outputs = [str(x).lower() for x in entry.get("output_modalities", [])]
        inputs = [str(x).lower() for x in entry.get("input_modalities", [])]
        if requested_output and any(requested_output in out for out in outputs):
            score += 0.12
            reasons.append(f"Output modality includes `{requested_output}`.")
        if requested_input and any(requested_input in inp for inp in inputs):
            score += 0.12
            reasons.append(f"Input modality includes `{requested_input}`.")

        if "video" in prompt_text and any("video" in x for x in outputs):
            score += 0.08
        if "video" in prompt_text and not any("video" in x for x in outputs):
            score -= 0.2
            reasons.append("Penalized because prompt asks for video but workflow output is not video.")
        if "image" in prompt_text and any("image" in x for x in outputs):
            score += 0.06
        if "upscale" in prompt_text and entry_family == "upscaling":
            score += 0.1

        asks_for_explicit_input = any(
            key in prompt_text
            for key in ("from image", "using image", "img2img", "i2i", "from video", "using video", "input image")
        )
        needs_input_media = any(x in {"image", "video"} for x in inputs)
        if needs_input_media and not asks_for_explicit_input:
            score -= 0.22
            reasons.append("Penalized because workflow expects media input not requested by prompt.")

        if entry_family == "upscaling" and "upscale" not in prompt_text and "super resolution" not in prompt_text:
            score -= 0.25
            reasons.append("Penalized because prompt does not ask for upscaling.")

        if not reasons:
            reasons.append("Best available semantic overlap for prompt terms.")

        ranked.append(
            {
                "id": entry.get("id"),
                "title": title,
                "family": entry_family,
                "destination": entry.get("destination"),
                "score": score,
                "confidence": round(max(0.0, min(0.99, score)), 4),
                "reasons": reasons,
                "model_families": families,
                "input_modalities": entry.get("input_modalities", []),
                "output_modalities": entry.get("output_modalities", []),
            }
        )

    ranked.sort(key=lambda x: (x["score"], x["id"]), reverse=True)
    return ranked[: max(1, int(top_k))]
