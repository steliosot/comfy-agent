from pathlib import Path

from comfy_agent import Workflow
from comfy_agent.artifacts import build_artifact, ensure_run_id, make_download_filename
from comfy_agent.config import ComfyConfig


VIDEO_EXTS = {".mp4", ".webm", ".mov", ".mkv", ".avi"}


def _normalize_output_dir(output_dir):
    return str(Path(output_dir).resolve())


def _is_video(item):
    filename = str(item.get("filename", "")).lower()
    ext = Path(filename).suffix
    return item.get("output_kind") in {"videos", "gifs"} or ext in VIDEO_EXTS


def run(
    video_meta=None,
    prompt_id=None,
    output_dir=None,
    run_id=None,
    stage="video",
    first_only=True,
    history_retries=120,
    history_delay=1.0,
    server=None,
    headers=None,
    api_prefix=None,
):
    if video_meta is None and not prompt_id:
        raise ValueError("Either video_meta or prompt_id is required")

    resolved_run_id = ensure_run_id(run_id)
    cfg = ComfyConfig.from_env(load_env=True)
    resolved_output_dir = _normalize_output_dir(output_dir or cfg.output_dir)
    wf = Workflow(server=server, headers=headers, api_prefix=api_prefix)

    downloaded = []
    if video_meta is not None:
        local_name = make_download_filename(
            resolved_run_id,
            stage,
            1,
            source_filename=video_meta.get("filename", "video.mp4"),
        )
        downloaded.append(
            wf.download_image(
                image_meta=video_meta,
                output_path=str(Path(resolved_output_dir) / local_name),
                output_dir=resolved_output_dir,
            )
        )
    else:
        all_items = wf.saved_images(prompt_id=prompt_id, retries=history_retries, delay=history_delay)
        candidates = [item for item in all_items if _is_video(item)]
        if first_only and candidates:
            candidates = candidates[:1]

        for index, item in enumerate(candidates, start=1):
            local_name = make_download_filename(
                resolved_run_id,
                stage,
                index,
                source_filename=item.get("filename", "video.mp4"),
            )
            downloaded.append(
                wf.download_image(
                    image_meta=item,
                    output_path=str(Path(resolved_output_dir) / local_name),
                    output_dir=resolved_output_dir,
                )
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
        "skill": "download_video",
        "run_id": resolved_run_id,
        "prompt_id": prompt_id,
        "filename_prefix": f"{resolved_run_id}_{stage}",
        "artifacts": artifacts,
        "downloaded": downloaded,
        "output_dir": resolved_output_dir,
    }
