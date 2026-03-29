import os

from comfy_agent import Workflow
from comfy_agent.artifacts import build_artifact, ensure_run_id
from comfy_agent.config import ComfyConfig


def run(
    video_path,
    run_id=None,
    remote_name=None,
    server=None,
    headers=None,
    api_prefix=None,
):
    cfg = ComfyConfig.from_env(load_env=True)
    resolved_run_id = ensure_run_id(run_id)
    resolved_video_path = video_path
    if not os.path.isabs(resolved_video_path) and not os.path.exists(resolved_video_path):
        candidate = os.path.join(cfg.input_dir, resolved_video_path)
        if os.path.exists(candidate):
            resolved_video_path = candidate

    suffix = os.path.splitext(resolved_video_path)[1] or ".mp4"
    resolved_remote = remote_name or f"{resolved_run_id}_input{suffix}"

    wf = Workflow(server=server, headers=headers, api_prefix=api_prefix)
    uploaded = wf.upload_image(
        local_path=resolved_video_path,
        remote_name=resolved_remote,
        overwrite=True,
        type="input",
    )

    artifact = build_artifact(
        role="input",
        local_path=uploaded["local_path"],
        remote_name=uploaded["remote_name"],
        source=uploaded.get("source", "upload"),
        subfolder=uploaded.get("subfolder", ""),
        type=uploaded.get("type", "input"),
    )

    return {
        "status": "ok",
        "skill": "upload_video",
        "run_id": resolved_run_id,
        "prompt_id": None,
        "filename_prefix": f"{resolved_run_id}_upload_video",
        "artifacts": [artifact],
        "input_video_remote": uploaded["remote_name"],
    }
