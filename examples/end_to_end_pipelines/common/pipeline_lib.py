import time
from datetime import datetime, timezone
from pathlib import Path
from time import perf_counter

from comfy_agent.config import ComfyConfig
from skills.download_image.skill import run as download_image_run
from skills.download_video.skill import run as download_video_run
from skills.generate_flux_multi_input_img2img.skill import build as build_still
from skills.generate_flux_multi_input_img2img.skill import run as generate_still_run
from skills.generate_ltxv_img2video.skill import build as build_video
from skills.generate_ltxv_img2video.skill import run as generate_video_run
from skills.get_progress.skill import run as get_progress_run
from skills.get_queue_status.skill import run as get_queue_status_run
from skills.get_server_status.skill import run as get_server_status_run
from skills.upload_image.skill import run as upload_image_run


def _now_iso():
    return datetime.now(timezone.utc).isoformat()


def _pick_one_image(items):
    images = [item for item in items if item.get("output_kind") == "images"]
    if len(images) != 1:
        raise RuntimeError(f"Expected exactly 1 still image, got {len(images)}")
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


def _write_log(path, lines):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _wait_with_progress(prompt_id, label, poll_seconds=8, max_wait_seconds=3600):
    start = perf_counter()
    snapshots = []
    while True:
        progress = get_progress_run(prompt_id=prompt_id)
        queue = get_queue_status_run()
        percent = float(progress.get("progress_percent", 0.0))
        snapshots.append(
            {
                "t": round(perf_counter() - start, 2),
                "percent": percent,
                "state": progress.get("state") or progress.get("source"),
                "running": queue.get("running_count", 0),
                "pending": queue.get("pending_count", 0),
            }
        )
        print(
            f"[{label}] progress={percent:.1f}% running={queue.get('running_count', 0)} "
            f"pending={queue.get('pending_count', 0)}",
            flush=True,
        )
        if percent >= 100.0:
            return snapshots, perf_counter() - start
        if perf_counter() - start > max_wait_seconds:
            raise TimeoutError(f"Timed out waiting for {label}: {prompt_id}")
        time.sleep(poll_seconds)


def _resolve_inputs(cfg, run_id):
    woman_local = Path(cfg.input_dir) / "woman.png"
    bbk_local = Path(cfg.input_dir) / "bbk.jpg"
    for path in [woman_local, bbk_local]:
        if not path.exists():
            raise FileNotFoundError(f"Missing input file: {path}")

    woman_uploaded = upload_image_run(
        image_path=str(woman_local),
        run_id=run_id,
        remote_name=f"{run_id}_woman{woman_local.suffix}",
        server=cfg.server,
        headers=cfg.headers or None,
        api_prefix=cfg.api_prefix,
    )
    bbk_uploaded = upload_image_run(
        image_path=str(bbk_local),
        run_id=run_id,
        remote_name=f"{run_id}_bbk{bbk_local.suffix}",
        server=cfg.server,
        headers=cfg.headers or None,
        api_prefix=cfg.api_prefix,
    )
    return woman_uploaded["input_image_remote"], bbk_uploaded["input_image_remote"]


def run_basic(video_seconds=6, log_path=None):
    total_start = perf_counter()
    cfg = ComfyConfig.from_env(load_env=True)
    run_id = f"birkbeck_story_{int(time.time())}"
    frame_rate = 24
    length = int(video_seconds * frame_rate)

    t_upload = perf_counter()
    woman_remote, bbk_remote = _resolve_inputs(cfg, run_id)
    upload_seconds = perf_counter() - t_upload

    t_still = perf_counter()
    still_result = generate_still_run(
        prompt=(
            "A realistic portrait of the same woman standing outside Birkbeck, University of London. "
            "Keep her identity and blend naturally with Birkbeck architecture."
        ),
        images=[woman_remote, bbk_remote],
        run_id=run_id,
        filename_prefix=f"{run_id}_birkbeck_still",
        batch_size=1,
        engine="auto",
        history_retries=180,
        history_delay=1.0,
        server=cfg.server,
        headers=cfg.headers or None,
        api_prefix=cfg.api_prefix,
    )
    still_seconds = perf_counter() - t_still
    still_meta = _pick_one_image(still_result["output_images"])

    t_still_dl = perf_counter()
    still_download = download_image_run(
        image_meta=still_meta,
        run_id=run_id,
        stage="still",
        output_dir=cfg.output_dir,
        server=cfg.server,
        headers=cfg.headers or None,
        api_prefix=cfg.api_prefix,
    )
    still_dl_seconds = perf_counter() - t_still_dl
    still_path = [a["downloaded_path"] for a in still_download["artifacts"] if a.get("downloaded_path")][0]

    t_video = perf_counter()
    video_result = generate_video_run(
        image=still_meta["filename"],
        image_source="output",
        image_subfolder=still_meta.get("subfolder", ""),
        image_type=still_meta.get("type", "output"),
        prompt=(
            "The same woman at Birkbeck, subtle natural movement, gentle blink, slight head turn, "
            "soft camera push-in, realistic motion."
        ),
        run_id=run_id,
        filename_prefix=f"{run_id}_birkbeck_video",
        frame_rate=frame_rate,
        length=length,
        batch_size=1,
        steps=30,
        cfg=3.0,
        history_retries=900,
        history_delay=2.0,
        server=cfg.server,
        headers=cfg.headers or None,
        api_prefix=cfg.api_prefix,
    )
    video_seconds_taken = perf_counter() - t_video
    video_meta = _pick_one_video(video_result["output_items"])

    t_video_dl = perf_counter()
    video_download = download_video_run(
        video_meta=video_meta,
        run_id=run_id,
        stage="video",
        output_dir=cfg.output_dir,
        first_only=True,
        server=cfg.server,
        headers=cfg.headers or None,
        api_prefix=cfg.api_prefix,
    )
    video_dl_seconds = perf_counter() - t_video_dl
    video_path = [a["downloaded_path"] for a in video_download["artifacts"] if a.get("downloaded_path")][0]

    total_seconds = perf_counter() - total_start
    if log_path is None:
        log_path = Path(__file__).resolve().parent / "log.md"
    else:
        log_path = Path(log_path)
    _write_log(
        log_path,
        [
            "# Birkbeck End-to-End Run Log",
            f"- Timestamp (UTC): {_now_iso()}",
            f"- Run ID: `{run_id}`",
            f"- Still Prompt ID: `{still_result['prompt_id']}`",
            f"- Video Prompt ID: `{video_result['prompt_id']}`",
            f"- Video Duration Request: `{video_seconds}s` ({length} frames @ {frame_rate}fps)",
            f"- Still file: `{still_path}`",
            f"- Video file: `{video_path}`",
            "## Timings",
            f"- Upload refs: `{upload_seconds:.2f}s`",
            f"- Generate still: `{still_seconds:.2f}s`",
            f"- Download still: `{still_dl_seconds:.2f}s`",
            f"- Generate video: `{video_seconds_taken:.2f}s`",
            f"- Download video: `{video_dl_seconds:.2f}s`",
            f"- Total pipeline: `{total_seconds:.2f}s`",
        ],
    )
    return {
        "run_id": run_id,
        "still_prompt_id": still_result["prompt_id"],
        "video_prompt_id": video_result["prompt_id"],
        "still_path": still_path,
        "video_path": video_path,
        "total_seconds": total_seconds,
        "log_path": str(log_path),
    }


def run_monitored(video_seconds=6, log_path=None):
    total_start = perf_counter()
    cfg = ComfyConfig.from_env(load_env=True)
    run_id = f"birkbeck_monitored_{int(time.time())}"
    frame_rate = 24
    length = int(video_seconds * frame_rate)

    initial_status = get_server_status_run()
    t_upload = perf_counter()
    woman_remote, bbk_remote = _resolve_inputs(cfg, run_id)
    upload_seconds = perf_counter() - t_upload

    t_still_submit = perf_counter()
    wf_still, _, _, _, _ = build_still(
        prompt=(
            "A realistic portrait of the same woman standing outside Birkbeck, University of London. "
            "Keep her identity and blend naturally with Birkbeck architecture."
        ),
        images=[woman_remote, bbk_remote],
        run_id=run_id,
        filename_prefix=f"{run_id}_birkbeck_still",
        batch_size=1,
        engine="auto",
        server=cfg.server,
        headers=cfg.headers or None,
        api_prefix=cfg.api_prefix,
    )
    still_submit_result = wf_still.run()
    still_prompt_id = still_submit_result.get("prompt_id")
    still_submit_seconds = perf_counter() - t_still_submit
    still_progress, still_wait_seconds = _wait_with_progress(still_prompt_id, "still")

    still_items = wf_still.saved_images(prompt_id=still_prompt_id, retries=2, delay=1.0)
    still_meta = _pick_one_image(still_items)
    t_still_dl = perf_counter()
    still_download = download_image_run(
        image_meta=still_meta,
        run_id=run_id,
        stage="still",
        output_dir=cfg.output_dir,
        server=cfg.server,
        headers=cfg.headers or None,
        api_prefix=cfg.api_prefix,
    )
    still_dl_seconds = perf_counter() - t_still_dl
    still_path = [a["downloaded_path"] for a in still_download["artifacts"] if a.get("downloaded_path")][0]

    t_video_submit = perf_counter()
    wf_video, _, _, _ = build_video(
        image=still_meta["filename"],
        image_source="output",
        image_subfolder=still_meta.get("subfolder", ""),
        image_type=still_meta.get("type", "output"),
        prompt=(
            "The same woman at Birkbeck, subtle natural movement, gentle blink, slight head turn, "
            "soft camera push-in, realistic motion."
        ),
        run_id=run_id,
        filename_prefix=f"{run_id}_birkbeck_video",
        frame_rate=frame_rate,
        length=length,
        batch_size=1,
        steps=30,
        cfg=3.0,
        server=cfg.server,
        headers=cfg.headers or None,
        api_prefix=cfg.api_prefix,
    )
    video_submit_result = wf_video.run()
    video_prompt_id = video_submit_result.get("prompt_id")
    video_submit_seconds = perf_counter() - t_video_submit
    video_progress, video_wait_seconds = _wait_with_progress(video_prompt_id, "video")

    video_items = wf_video.saved_images(prompt_id=video_prompt_id, retries=2, delay=1.0)
    video_meta = _pick_one_video(video_items)
    t_video_dl = perf_counter()
    video_download = download_video_run(
        video_meta=video_meta,
        run_id=run_id,
        stage="video",
        output_dir=cfg.output_dir,
        first_only=True,
        server=cfg.server,
        headers=cfg.headers or None,
        api_prefix=cfg.api_prefix,
    )
    video_dl_seconds = perf_counter() - t_video_dl
    video_path = [a["downloaded_path"] for a in video_download["artifacts"] if a.get("downloaded_path")][0]

    final_status = get_server_status_run()
    total_seconds = perf_counter() - total_start
    if log_path is None:
        log_path = Path(__file__).resolve().parent / "log_monitored.md"
    else:
        log_path = Path(log_path)
    lines = [
        "# Birkbeck Monitored End-to-End Log",
        f"- Timestamp (UTC): {_now_iso()}",
        f"- Run ID: `{run_id}`",
        f"- Still Prompt ID: `{still_prompt_id}`",
        f"- Video Prompt ID: `{video_prompt_id}`",
        f"- Video Duration Request: `{video_seconds}s` ({length} frames @ {frame_rate}fps)",
        f"- Still file: `{still_path}`",
        f"- Video file: `{video_path}`",
        "## Status",
        f"- Initial busy: `{initial_status.get('busy')}` running={initial_status.get('running_count')} pending={initial_status.get('pending_count')}",
        f"- Final busy: `{final_status.get('busy')}` running={final_status.get('running_count')} pending={final_status.get('pending_count')}",
        "## Timings",
        f"- Upload refs: `{upload_seconds:.2f}s`",
        f"- Still submit: `{still_submit_seconds:.2f}s`",
        f"- Still wait: `{still_wait_seconds:.2f}s`",
        f"- Still download: `{still_dl_seconds:.2f}s`",
        f"- Video submit: `{video_submit_seconds:.2f}s`",
        f"- Video wait: `{video_wait_seconds:.2f}s`",
        f"- Video download: `{video_dl_seconds:.2f}s`",
        f"- Total: `{total_seconds:.2f}s`",
        "## Progress Snapshots (Still)",
    ]
    lines.extend(
        [
            f"- t={s['t']}s percent={s['percent']} state={s['state']} running={s['running']} pending={s['pending']}"
            for s in still_progress
        ]
    )
    lines.append("## Progress Snapshots (Video)")
    lines.extend(
        [
            f"- t={s['t']}s percent={s['percent']} state={s['state']} running={s['running']} pending={s['pending']}"
            for s in video_progress
        ]
    )
    _write_log(log_path, lines)
    return {
        "run_id": run_id,
        "still_prompt_id": still_prompt_id,
        "video_prompt_id": video_prompt_id,
        "still_path": still_path,
        "video_path": video_path,
        "total_seconds": total_seconds,
        "log_path": str(log_path),
    }
