from comfy_agent.curated_catalog import load_curated_manifest, match_curated_entries


def run(
    prompt,
    top_k=5,
    family=None,
    input_modality=None,
    output_modality=None,
    model_family=None,
):
    manifest = load_curated_manifest()
    entries = manifest.get("entries", [])

    matches = match_curated_entries(
        prompt=prompt,
        entries=entries,
        top_k=top_k,
        family=family,
        input_modality=input_modality,
        output_modality=output_modality,
        model_family=model_family,
    )
    return {
        "status": "ok",
        "skill": "match_curated_workflow",
        "prompt": prompt,
        "preferred_family": family,
        "top_k": int(top_k),
        "matches": matches,
    }
