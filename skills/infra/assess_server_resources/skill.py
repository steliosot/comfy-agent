from comfy_agent.config import ComfyConfig
from comfy_agent.monitoring import fetch_queue, fetch_system_stats


def _to_float(value, default=None):
    if value in (None, ""):
        return default
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _extract_resource_view(stats_payload):
    stats = stats_payload.get("stats", {}) if isinstance(stats_payload, dict) else {}
    system = stats.get("system", {}) if isinstance(stats, dict) else {}
    devices = stats.get("devices", []) if isinstance(stats, dict) else []

    free_vram_mb = 0.0
    total_vram_mb = 0.0
    for device in devices if isinstance(devices, list) else []:
        vram_total = _to_float(device.get("vram_total"), default=0.0) or 0.0
        vram_free = _to_float(device.get("vram_free"), default=0.0) or 0.0
        total_vram_mb += vram_total / (1024 * 1024) if vram_total > 1024 else vram_total
        free_vram_mb += vram_free / (1024 * 1024) if vram_free > 1024 else vram_free

    free_storage_gb = _to_float(system.get("free_disk_gb"), default=None)
    if free_storage_gb is None:
        free_storage_gb = _to_float(stats.get("free_disk_gb"), default=None)

    return {
        "free_vram_mb": round(free_vram_mb, 2),
        "total_vram_mb": round(total_vram_mb, 2),
        "free_storage_gb": round(free_storage_gb, 2) if free_storage_gb is not None else None,
        "device_count": len(devices) if isinstance(devices, list) else 0,
        "raw": stats,
    }


def run(
    min_vram_mb=None,
    min_storage_gb=None,
    warn_only=True,
    server=None,
    headers=None,
    api_prefix=None,
):
    cfg = ComfyConfig.from_env(load_env=True)
    resolved_server = server or cfg.server
    resolved_headers = headers if headers is not None else (cfg.headers or None)
    resolved_api_prefix = api_prefix if api_prefix is not None else cfg.api_prefix

    required_vram = _to_float(
        min_vram_mb, default=cfg.resource_min_free_vram_mb if cfg.resource_min_free_vram_mb is not None else 0.0
    )
    required_storage = _to_float(
        min_storage_gb,
        default=cfg.resource_min_free_storage_gb if cfg.resource_min_free_storage_gb is not None else 0.0,
    )

    queue = fetch_queue(resolved_server, headers=resolved_headers, api_prefix=resolved_api_prefix)
    stats = fetch_system_stats(resolved_server, headers=resolved_headers, api_prefix=resolved_api_prefix)
    resource_view = _extract_resource_view(stats)

    warnings = []
    blockers = []

    free_vram = resource_view["free_vram_mb"]
    free_storage = resource_view["free_storage_gb"]
    if required_vram and free_vram < required_vram:
        message = (
            f"Free VRAM appears below requested threshold: free={free_vram}MB, required={required_vram}MB."
        )
        (warnings if warn_only else blockers).append(message)
    if required_storage and free_storage is not None and free_storage < required_storage:
        message = (
            f"Free storage appears below requested threshold: free={free_storage}GB, required={required_storage}GB."
        )
        (warnings if warn_only else blockers).append(message)

    running_count = len(queue.get("running", []))
    pending_count = len(queue.get("pending", []))
    queue_busy = running_count > 0 or pending_count > 0
    if queue_busy:
        warnings.append(
            f"Queue is busy (running={running_count}, pending={pending_count}); dependency actions may take longer."
        )

    ready = len(blockers) == 0
    return {
        "status": "ok" if ready else "blocked",
        "skill": "assess_server_resources",
        "server": resolved_server,
        "warn_only": bool(warn_only),
        "requirements": {
            "min_vram_mb": required_vram,
            "min_storage_gb": required_storage,
        },
        "resources": {
            "free_vram_mb": free_vram,
            "total_vram_mb": resource_view["total_vram_mb"],
            "free_storage_gb": free_storage,
            "device_count": resource_view["device_count"],
        },
        "queue": {
            "running_count": running_count,
            "pending_count": pending_count,
            "busy": queue_busy,
        },
        "warnings": warnings,
        "blockers": blockers,
        "ready_for_install": ready,
        "system_stats": stats,
    }
