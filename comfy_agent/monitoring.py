import json
from urllib import error, request
from urllib.parse import urlparse


def _normalize_base_url(base_url):
    text = str(base_url).strip()
    if "://" in text:
        parsed = urlparse(text)
        if parsed.scheme:
            return text.rstrip("/")
    return f"http://{text}".rstrip("/")


def _candidate_roots(server, api_prefix=None):
    base = _normalize_base_url(server)
    normalized_prefix = (api_prefix or "").strip()
    if normalized_prefix and not normalized_prefix.startswith("/"):
        normalized_prefix = f"/{normalized_prefix}"
    normalized_prefix = normalized_prefix.rstrip("/")

    roots = []
    if normalized_prefix:
        roots.append(f"{base}{normalized_prefix}")
    roots.append(base)
    if not normalized_prefix:
        roots.append(f"{base}/api")

    seen = set()
    unique = []
    for root in roots:
        if root not in seen:
            seen.add(root)
            unique.append(root)
    return unique


def _request_json(url, headers):
    req = request.Request(url, headers=headers or {})
    with request.urlopen(req, timeout=30) as resp:
        raw = resp.read().decode("utf-8")
    return json.loads(raw)


def fetch_json(server, path, headers=None, api_prefix=None):
    normalized_path = path if path.startswith("/") else f"/{path}"
    last_error = None
    for root in _candidate_roots(server, api_prefix=api_prefix):
        url = f"{root}{normalized_path}"
        try:
            data = _request_json(url, headers=headers)
            return {"ok": True, "url": url, "data": data}
        except error.HTTPError as exc:
            last_error = exc
            if exc.code in {404, 405}:
                continue
            return {"ok": False, "url": url, "error": f"HTTP {exc.code}"}
        except Exception as exc:  # pragma: no cover
            last_error = exc
            continue

    message = str(last_error) if last_error else "unavailable"
    return {"ok": False, "url": None, "error": message}


def fetch_queue(server, headers=None, api_prefix=None):
    result = fetch_json(server, "/queue", headers=headers, api_prefix=api_prefix)
    if not result["ok"]:
        return {"ok": False, "running": [], "pending": [], "error": result["error"], "url": result["url"]}
    data = result["data"] if isinstance(result["data"], dict) else {}
    running = data.get("queue_running", []) if isinstance(data, dict) else []
    pending = data.get("queue_pending", []) if isinstance(data, dict) else []
    return {"ok": True, "running": running, "pending": pending, "url": result["url"]}


def fetch_system_stats(server, headers=None, api_prefix=None):
    result = fetch_json(server, "/system_stats", headers=headers, api_prefix=api_prefix)
    if not result["ok"]:
        return {"ok": False, "stats": {}, "error": result["error"], "url": result["url"]}
    data = result["data"] if isinstance(result["data"], dict) else {}
    return {"ok": True, "stats": data, "url": result["url"]}


def fetch_progress(server, headers=None, api_prefix=None):
    result = fetch_json(server, "/progress", headers=headers, api_prefix=api_prefix)
    if not result["ok"]:
        return {"ok": False, "progress": {}, "error": result["error"], "url": result["url"]}
    data = result["data"] if isinstance(result["data"], dict) else {}
    return {"ok": True, "progress": data, "url": result["url"]}


def fetch_history_entry(server, prompt_id, headers=None, api_prefix=None):
    result = fetch_json(server, f"/history/{prompt_id}", headers=headers, api_prefix=api_prefix)
    if not result["ok"]:
        return {"ok": False, "entry": None, "error": result["error"], "url": result["url"]}
    data = result["data"]
    if isinstance(data, dict):
        entry = data.get(prompt_id, data)
    else:
        entry = None
    return {"ok": True, "entry": entry, "url": result["url"]}
