from pathlib import Path

from comfy_agent import Workflow
from comfy_agent.artifacts import (
    build_artifact,
    ensure_run_id,
    make_download_filename,
)
from comfy_agent.config import ComfyConfig


def _normalize_output_dir(output_dir):
    return str(Path(output_dir).resolve())


def run(
    image_meta=None,
    prompt_id=None,
    output_dir=None,
    run_id=None,
    stage="download",
    history_retries=12,
    history_delay=0.5,
    server=None,
    headers=None,
    api_prefix=None,
):
    if image_meta is None and not prompt_id:
        raise ValueError("Either image_meta or prompt_id is required")

    resolved_run_id = ensure_run_id(run_id)
    cfg = ComfyConfig.from_env(load_env=True)
    resolved_output_dir = _normalize_output_dir(output_dir or cfg.output_dir)
    wf = Workflow(server=server, headers=headers, api_prefix=api_prefix)

    downloaded = []
    if image_meta is not None:
        local_name = make_download_filename(
            resolved_run_id,
            stage,
            1,
            source_filename=image_meta.get("filename", ""),
        )
        record = wf.download_image(
            image_meta=image_meta,
            output_path=str(Path(resolved_output_dir) / local_name),
            output_dir=resolved_output_dir,
        )
        downloaded.append(record)
    else:
        downloaded = wf.download_saved_images(
            prompt_id=prompt_id,
            output_dir=resolved_output_dir,
            filename_strategy=lambda meta, index: make_download_filename(
                resolved_run_id,
                stage,
                index,
                source_filename=meta.get("filename", ""),
            ),
            retries=history_retries,
            delay=history_delay,
        )

    artifacts = [
        build_artifact(
            role="output",
            local_path=item.get("downloaded_path"),
            remote_name=item.get("filename"),
            source=item.get("source", "download"),
            node_id=item.get("node_id"),
            subfolder=item.get("subfolder", ""),
            type=item.get("type", "output"),
            downloaded_path=item.get("downloaded_path"),
        )
        for item in downloaded
    ]

    return {
        "status": "ok",
        "skill": "download_image",
        "run_id": resolved_run_id,
        "prompt_id": prompt_id,
        "filename_prefix": f"{resolved_run_id}_{stage}",
        "artifacts": artifacts,
        "downloaded": downloaded,
        "output_dir": resolved_output_dir,
    }
