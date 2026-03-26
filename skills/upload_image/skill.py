import os

from comfy_agent import Workflow
from comfy_agent.artifacts import build_artifact, ensure_run_id, make_remote_input_name
from comfy_agent.config import ComfyConfig


def run(
    image_path,
    run_id=None,
    remote_name=None,
    server=None,
    headers=None,
    api_prefix=None,
):
    cfg = ComfyConfig.from_env(load_env=True)
    resolved_run_id = ensure_run_id(run_id)
    resolved_image_path = image_path
    if not os.path.isabs(resolved_image_path) and not os.path.exists(resolved_image_path):
        candidate = os.path.join(cfg.input_dir, resolved_image_path)
        if os.path.exists(candidate):
            resolved_image_path = candidate

    resolved_remote = remote_name or make_remote_input_name(resolved_run_id, resolved_image_path)

    wf = Workflow(server=server, headers=headers, api_prefix=api_prefix)
    uploaded = wf.upload_image(
        local_path=resolved_image_path,
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
        "skill": "upload_image",
        "run_id": resolved_run_id,
        "prompt_id": None,
        "filename_prefix": f"{resolved_run_id}_upload",
        "artifacts": [artifact],
        "input_image_remote": uploaded["remote_name"],
    }
