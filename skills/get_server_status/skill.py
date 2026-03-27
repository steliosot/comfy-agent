from comfy_agent.config import ComfyConfig
from comfy_agent.monitoring import fetch_queue, fetch_system_stats


def run(server=None, headers=None, api_prefix=None):
    cfg = ComfyConfig.from_env(load_env=True)
    resolved_server = server or cfg.server
    resolved_headers = headers if headers is not None else (cfg.headers or None)

    queue = fetch_queue(resolved_server, headers=resolved_headers, api_prefix=api_prefix or cfg.api_prefix)
    stats = fetch_system_stats(resolved_server, headers=resolved_headers, api_prefix=api_prefix or cfg.api_prefix)

    running_count = len(queue.get("running", []))
    pending_count = len(queue.get("pending", []))
    busy = running_count > 0 or pending_count > 0

    return {
        "status": "ok" if queue.get("ok") else "degraded",
        "skill": "get_server_status",
        "server": resolved_server,
        "busy": busy,
        "running_count": running_count,
        "pending_count": pending_count,
        "queue": queue,
        "system_stats": stats,
    }
