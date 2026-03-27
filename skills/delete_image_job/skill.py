from comfy_agent.cleanup import delete_history_jobs
from comfy_agent.config import ComfyConfig
from comfy_agent.monitoring import fetch_history_entry


def _count_outputs(entry):
    counts = {"images": 0, "videos": 0, "gifs": 0}
    outputs = entry.get("outputs", {}) if isinstance(entry, dict) else {}
    for node in outputs.values():
        for key in counts:
            counts[key] += len(node.get(key, []))
    return counts


def run(prompt_id, server=None, headers=None, api_prefix=None, force=False):
    cfg = ComfyConfig.from_env(load_env=True)
    resolved_server = server or cfg.server
    resolved_headers = headers if headers is not None else (cfg.headers or None)
    resolved_prefix = api_prefix or cfg.api_prefix

    hist = fetch_history_entry(
        resolved_server,
        prompt_id=prompt_id,
        headers=resolved_headers,
        api_prefix=resolved_prefix,
    )
    entry = hist.get("entry") if hist.get("ok") else None
    counts = _count_outputs(entry or {})

    if not force and counts["images"] <= 0:
        return {
            "status": "error",
            "skill": "delete_image_job",
            "prompt_id": prompt_id,
            "error": "prompt_has_no_image_outputs",
            "counts": counts,
        }

    deleted = delete_history_jobs(
        resolved_server,
        prompt_ids=[prompt_id],
        headers=resolved_headers,
        api_prefix=resolved_prefix,
    )

    return {
        "status": "ok" if deleted.get("ok") else "error",
        "skill": "delete_image_job",
        "prompt_id": prompt_id,
        "counts": counts,
        "deleted": deleted,
    }
