from datetime import datetime, timezone
from pathlib import Path
from time import perf_counter, time

from comfy_agent.config import ComfyConfig
from skills.infra.delete_image_job.skill import run as delete_image_job_run
from skills.infra.delete_video_job.skill import run as delete_video_job_run
from skills.infra.download_image.skill import run as download_image_run
from skills.infra.download_video.skill import run as download_video_run
from skills.workflows.img2img_inpaint_outpaint.generate_flux_multi_input_img2img.skill import run as generate_image_run
from skills.workflows.video_t2v_i2v_avatar.generate_ltxv_img2video.skill import run as generate_video_run
from skills.infra.upload_image.skill import run as upload_image_run


def _now_iso():
    return datetime.now(timezone.utc).isoformat()


def _pick_one_image(items):
    images = [item for item in items if item.get("output_kind") == "images"]
    if len(images) != 1:
        raise RuntimeError(f"Expected exactly 1 still image output, got {len(images)}")
    return images[0]


def _pick_one_video(items):
    videos = [
        item
        for item in items
        if item.get("output_kind") in {"videos", "gifs"}
        or str(item.get("filename", "")).lower().endswith((".mp4", ".webm", ".gif"))
    ]
    if len(videos) != 1:
        raise RuntimeError(f"Expected exactly 1 video output, got {len(videos)}")
    return videos[0]


cfg = ComfyConfig.from_env(load_env=True)
headers = cfg.headers or None
run_id = f"odeon_cleanup_{int(time())}"
total_start = perf_counter()

woman_path = Path(cfg.input_dir) / "woman.png"
odeon_path = Path(cfg.input_dir) / "odeon-athens-greece.avif"

woman_remote = upload_image_run(
    image_path=str(woman_path),
    run_id=run_id,
    remote_name=f"{run_id}_woman{woman_path.suffix}",
    server=cfg.server,
    headers=headers,
    api_prefix=cfg.api_prefix,
)["input_image_remote"]

odeon_remote = upload_image_run(
    image_path=str(odeon_path),
    run_id=run_id,
    remote_name=f"{run_id}_odeon{odeon_path.suffix}",
    server=cfg.server,
    headers=headers,
    api_prefix=cfg.api_prefix,
)["input_image_remote"]

still_result = generate_image_run(
    prompt=(
        "Photorealistic image of the same woman standing at the Odeon of Herodes Atticus in Athens, "
        "natural Mediterranean daylight, realistic perspective, cinematic composition."
    ),
    images=[woman_remote, odeon_remote],
    run_id=run_id,
    filename_prefix=f"{run_id}_odeon_still",
    batch_size=1,
    engine="auto",
    history_retries=180,
    history_delay=1.0,
    server=cfg.server,
    headers=headers,
    api_prefix=cfg.api_prefix,
)
still_meta = _pick_one_image(still_result["output_images"])

still_local = download_image_run(
    image_meta=still_meta,
    run_id=run_id,
    stage="still",
    output_dir=cfg.output_dir,
    server=cfg.server,
    headers=headers,
    api_prefix=cfg.api_prefix,
)
still_path = [a["downloaded_path"] for a in still_local["artifacts"] if a.get("downloaded_path")][0]

video_result = generate_video_run(
    image=still_meta["filename"],
    image_source="output",
    image_subfolder=still_meta.get("subfolder", ""),
    image_type=still_meta.get("type", "output"),
    prompt=(
        "Same woman at the Odeon in Athens, subtle natural movement, gentle blink, slight head movement, "
        "cinematic camera motion, realistic textures and lighting."
    ),
    run_id=run_id,
    filename_prefix=f"{run_id}_odeon_video",
    frame_rate=24,
    length=144,
    batch_size=1,
    steps=30,
    cfg=3.0,
    history_retries=900,
    history_delay=2.0,
    server=cfg.server,
    headers=headers,
    api_prefix=cfg.api_prefix,
)
video_meta = _pick_one_video(video_result["output_items"])

video_local = download_video_run(
    video_meta=video_meta,
    run_id=run_id,
    stage="video",
    output_dir=cfg.output_dir,
    first_only=True,
    server=cfg.server,
    headers=headers,
    api_prefix=cfg.api_prefix,
)
video_path = [a["downloaded_path"] for a in video_local["artifacts"] if a.get("downloaded_path")][0]

# Cleanup jobs from server history.
delete_still = delete_image_job_run(
    prompt_id=still_result["prompt_id"],
    server=cfg.server,
    headers=headers,
    api_prefix=cfg.api_prefix,
)
delete_video = delete_video_job_run(
    prompt_id=video_result["prompt_id"],
    server=cfg.server,
    headers=headers,
    api_prefix=cfg.api_prefix,
)

total_seconds = perf_counter() - total_start

log_path = Path(__file__).resolve().parent / "log.md"
log_path.write_text(
    "\n".join(
        [
            "# Odeon Compose + Cleanup Log",
            f"- Timestamp (UTC): {_now_iso()}",
            f"- Run ID: `{run_id}`",
            f"- Still Prompt ID: `{still_result['prompt_id']}`",
            f"- Video Prompt ID: `{video_result['prompt_id']}`",
            f"- Still file: `{still_path}`",
            f"- Video file: `{video_path}`",
            f"- Delete still status: `{delete_still['status']}` deleted={delete_still.get('deleted', {}).get('deleted')}",
            f"- Delete video status: `{delete_video['status']}` deleted={delete_video.get('deleted', {}).get('deleted')}",
            f"- Total: `{total_seconds:.2f}s`",
        ]
    )
    + "\n",
    encoding="utf-8",
)

print("run_id:", run_id)
print("still:", still_path)
print("video:", video_path)
print("deleted_still:", delete_still.get("deleted", {}).get("deleted"))
print("deleted_video:", delete_video.get("deleted", {}).get("deleted"))
print(f"total: {total_seconds:.2f}s")
print("log:", str(log_path))
