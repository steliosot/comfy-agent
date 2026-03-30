from comfy_agent.config import get_server_config
from comfy_agent.manager import manager_probe
from comfy_agent.monitoring import fetch_json


def run(server_name=None, require_ready=False):
    try:
        resolved = get_server_config(name=server_name, load_env=True)
    except Exception as exc:
        return {
            "status": "error",
            "skill": "select_comfy_server",
            "server_name": server_name,
            "server": None,
            "headers": {},
            "api_prefix": None,
            "manager_api_prefix": None,
            "ready": None,
            "message": str(exc),
            "source": None,
            "servers_file": None,
            "health": None,
            "manager": None,
        }

    response = {
        "status": "ok",
        "skill": "select_comfy_server",
        "server_name": resolved.get("server_name"),
        "server": resolved["server"],
        "headers": resolved["headers"],
        "api_prefix": resolved["api_prefix"],
        "manager_api_prefix": resolved["manager_api_prefix"],
        "ready": None,
        "message": "Server config resolved.",
        "source": resolved.get("source"),
        "servers_file": resolved.get("servers_file"),
        "health": None,
        "manager": None,
    }

    if not require_ready:
        return response

    health = fetch_json(
        resolved["server"],
        "/object_info",
        headers=resolved["headers"] or None,
        api_prefix=resolved["api_prefix"],
    )
    manager = manager_probe(
        server=resolved["server"],
        headers=resolved["headers"] or None,
        api_prefix=resolved["api_prefix"],
        manager_api_prefix=resolved["manager_api_prefix"],
    )

    ready = bool(health.get("ok"))
    response["ready"] = ready
    response["health"] = {
        "ok": bool(health.get("ok")),
        "url": health.get("url"),
        "error": health.get("error"),
    }
    response["manager"] = {
        "ok": bool(manager.get("ok")),
        "manager_available": bool(manager.get("manager_available")),
        "root": manager.get("root"),
        "error": manager.get("error"),
    }

    if ready:
        if manager.get("ok"):
            response["message"] = "Server is reachable and manager probe succeeded."
        else:
            response["message"] = "Server is reachable; manager probe failed (optional for workflow runs)."
    else:
        response["status"] = "blocked"
        response["message"] = "Server is not reachable via /object_info."

    return response
