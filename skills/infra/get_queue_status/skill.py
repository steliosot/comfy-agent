from comfy_agent.config import ComfyConfig
from comfy_agent.monitoring import fetch_queue


def run(server=None, headers=None, api_prefix=None):
    cfg = ComfyConfig.from_env(load_env=True)
    resolved_server = server or cfg.server
    resolved_headers = headers if headers is not None else (cfg.headers or None)

    queue = fetch_queue(resolved_server, headers=resolved_headers, api_prefix=api_prefix or cfg.api_prefix)
    return {
        "status": "ok" if queue.get("ok") else "error",
        "skill": "get_queue_status",
        "server": resolved_server,
        "running_count": len(queue.get("running", [])),
        "pending_count": len(queue.get("pending", [])),
        "running": queue.get("running", []),
        "pending": queue.get("pending", []),
        "source_url": queue.get("url"),
        "error": queue.get("error"),
    }
