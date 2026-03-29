from comfy_agent.curated_catalog import load_curated_manifest


def run(family=None, model_family=None, limit=100):
    manifest = load_curated_manifest()
    entries = manifest.get("entries", [])

    out = []
    model_filter = str(model_family).lower() if model_family else None
    for item in entries:
        if family and item.get("family") != family:
            continue
        if model_filter:
            families = [str(x).lower() for x in (item.get("model_families") or [])]
            probe = " ".join(
                [str(item.get("title", "")), str(item.get("id", ""))]
            ).lower()
            if model_filter not in families and model_filter not in probe:
                continue
        out.append(item)
        if len(out) >= int(limit):
            break

    return {
        "status": "ok",
        "skill": "list_curated_workflows",
        "count": len(out),
        "total": len(entries),
        "items": out,
    }
