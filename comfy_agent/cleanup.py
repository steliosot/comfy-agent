import json
from urllib import request

from .monitoring import fetch_history_entry, fetch_json


def delete_history_jobs(server, prompt_ids, headers=None, api_prefix=None):
    ids = [str(pid) for pid in prompt_ids if str(pid).strip()]
    if not ids:
        raise ValueError("prompt_ids is required")

    payload = json.dumps({"delete": ids}).encode("utf-8")
    result = fetch_json(server, "/history", headers=headers, api_prefix=api_prefix)
    if not result.get("url"):
        return {"ok": False, "deleted": [], "error": result.get("error"), "url": None}

    req = request.Request(
        result["url"],
        data=payload,
        method="POST",
        headers={
            **(headers or {}),
            "Content-Type": "application/json",
        },
    )
    try:
        with request.urlopen(req, timeout=30):
            pass
    except Exception as exc:
        return {"ok": False, "deleted": [], "error": str(exc), "url": result["url"]}

    deleted = []
    for pid in ids:
        check = fetch_history_entry(server, pid, headers=headers, api_prefix=api_prefix)
        if check.get("ok") and not check.get("entry"):
            deleted.append(pid)
    return {"ok": True, "deleted": deleted, "requested": ids, "url": result["url"]}
