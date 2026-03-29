import os
import time

from comfy_agent.config import ComfyConfig
from comfy_agent.monitoring import fetch_history_entry, fetch_progress, fetch_queue

_PROMPT_STARTED_AT = {}


def _contains_prompt(queue_items, prompt_id):
    for item in queue_items:
        if isinstance(item, (list, tuple)) and len(item) >= 2 and str(item[1]) == str(prompt_id):
            return True
    return False


def _running_percent(prompt_id):
    now = time.monotonic()
    started = _PROMPT_STARTED_AT.get(prompt_id)
    if started is None:
        _PROMPT_STARTED_AT[prompt_id] = now
        started = now
    elapsed = max(0.0, now - started)
    expected = float(os.getenv("COMFY_PROGRESS_EXPECTED_SECONDS", "900") or 900)
    ramp = min(75.0, (elapsed / max(1.0, expected)) * 75.0)
    return round(20.0 + ramp, 2)


def _pending_percent(prompt_id):
    now = time.monotonic()
    started = _PROMPT_STARTED_AT.get(prompt_id)
    if started is None:
        _PROMPT_STARTED_AT[prompt_id] = now
        started = now
    elapsed = max(0.0, now - started)
    expected = float(os.getenv("COMFY_PROGRESS_EXPECTED_SECONDS", "900") or 900)
    pending_window = max(30.0, expected * 0.1)
    ramp = min(10.0, (elapsed / pending_window) * 10.0)
    return round(5.0 + ramp, 2)


def run(prompt_id=None, server=None, headers=None, api_prefix=None):
    cfg = ComfyConfig.from_env(load_env=True)
    resolved_server = server or cfg.server
    resolved_headers = headers if headers is not None else (cfg.headers or None)
    resolved_prefix = api_prefix or cfg.api_prefix

    # Try exact Comfy progress endpoint first.
    raw_progress = fetch_progress(resolved_server, headers=resolved_headers, api_prefix=resolved_prefix)
    if raw_progress.get("ok"):
        payload = raw_progress.get("progress", {}) if isinstance(raw_progress.get("progress"), dict) else {}
        value = float(payload.get("value", 0) or 0)
        maximum = float(payload.get("max", 0) or 0)
        percent = round((value / maximum) * 100, 2) if maximum > 0 else 0.0
        return {
            "status": "ok",
            "skill": "get_progress",
            "prompt_id": prompt_id,
            "progress_percent": percent,
            "value": value,
            "max": maximum,
            "source": "progress_endpoint",
            "raw": payload,
        }

    # Fallback for servers without /progress: queue + history heuristics.
    queue = fetch_queue(resolved_server, headers=resolved_headers, api_prefix=resolved_prefix)
    if prompt_id:
        hist = fetch_history_entry(
            resolved_server,
            prompt_id=prompt_id,
            headers=resolved_headers,
            api_prefix=resolved_prefix,
        )
        if hist.get("ok") and hist.get("entry"):
            _PROMPT_STARTED_AT.pop(prompt_id, None)
            return {
                "status": "ok",
                "skill": "get_progress",
                "prompt_id": prompt_id,
                "progress_percent": 100.0,
                "source": "history_complete",
                "queue_running": len(queue.get("running", [])),
                "queue_pending": len(queue.get("pending", [])),
            }

        running = queue.get("running", [])
        pending = queue.get("pending", [])
        if _contains_prompt(running, prompt_id):
            percent = _running_percent(prompt_id)
            state = "running"
        elif _contains_prompt(pending, prompt_id):
            percent = _pending_percent(prompt_id)
            state = "pending"
        else:
            percent = 0.0
            state = "unknown"
            _PROMPT_STARTED_AT.pop(prompt_id, None)

        return {
            "status": "ok" if queue.get("ok") else "degraded",
            "skill": "get_progress",
            "prompt_id": prompt_id,
            "progress_percent": percent,
            "state": state,
            "source": "queue_heuristic",
            "queue_running": len(running),
            "queue_pending": len(pending),
            "progress_endpoint_error": raw_progress.get("error"),
        }

    running_count = len(queue.get("running", []))
    pending_count = len(queue.get("pending", []))
    percent = 20.0 if running_count > 0 else (5.0 if pending_count > 0 else 0.0)
    return {
        "status": "ok" if queue.get("ok") else "degraded",
        "skill": "get_progress",
        "prompt_id": None,
        "progress_percent": percent,
        "state": "running" if running_count > 0 else ("pending" if pending_count > 0 else "idle"),
        "source": "queue_heuristic",
        "queue_running": running_count,
        "queue_pending": pending_count,
        "progress_endpoint_error": raw_progress.get("error"),
    }
