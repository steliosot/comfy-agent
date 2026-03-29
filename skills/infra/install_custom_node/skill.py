from comfy_agent import Workflow
from comfy_agent.config import ComfyConfig
from comfy_agent.manager import manager_install


def _normalize_expected(expected_node_classes):
    if expected_node_classes is None:
        return []
    if isinstance(expected_node_classes, str):
        return [expected_node_classes]
    return [str(item) for item in expected_node_classes if str(item).strip()]


def run(
    repo_url,
    expected_node_classes=None,
    server=None,
    headers=None,
    api_prefix=None,
    manager_api_prefix=None,
):
    cfg = ComfyConfig.from_env(load_env=True)
    resolved_server = server or cfg.server
    resolved_headers = headers if headers is not None else (cfg.headers or None)
    resolved_api_prefix = api_prefix if api_prefix is not None else cfg.api_prefix
    resolved_manager_prefix = (
        manager_api_prefix if manager_api_prefix is not None else cfg.manager_api_prefix
    )
    expected = _normalize_expected(expected_node_classes)

    payload = {"repo_url": repo_url, "git_url": repo_url}
    install = manager_install(
        operation="custom_node_install",
        payload=payload,
        server=resolved_server,
        headers=resolved_headers,
        api_prefix=resolved_api_prefix,
        manager_api_prefix=resolved_manager_prefix,
    )

    verification = {"verified": False, "missing": expected, "present": []}
    if install.get("ok"):
        wf = Workflow(
            server=resolved_server,
            headers=resolved_headers,
            api_prefix=resolved_api_prefix,
        )
        present = [name for name in expected if name in wf.registry]
        missing = [name for name in expected if name not in wf.registry]
        verification = {
            "verified": len(missing) == 0 if expected else True,
            "missing": missing,
            "present": present,
            "registry_node_count": len(wf.registry),
        }

    return {
        "status": "ok" if install.get("ok") else "error",
        "skill": "install_custom_node",
        "server": resolved_server,
        "repo_url": repo_url,
        "expected_node_classes": expected,
        "install": install,
        "verification": verification,
    }
