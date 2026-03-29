import os

from comfy_agent import Workflow
from comfy_agent.artifacts import build_artifact, ensure_run_id, make_stage_prefix


def _resolve_headers(headers):
    if headers is not None:
        return headers
    auth_header = os.getenv("COMFY_AUTH_HEADER")
    if auth_header:
        return {"Authorization": auth_header}
    return None


def build(
    image,
    image_source="input",
    image_subfolder="",
    image_type="output",
    prompt=(
        "A young woman with short, curly purple hair and a gentle smile stands in a warmly lit "
        "modern apartment. She wears a light gray T-shirt and has a small nose piercing. She looks "
        "directly at the camera, blinks naturally, then tilts her head slightly with a curious "
        "expression. Soft sunlight from the side highlights the texture of her skin and the vibrant "
        "tones in her hair. The mood is calm, intimate, and beautiful. Slow cinematic camera movement."
    ),
    negative_prompt=(
        "low quality, worst quality, deformed, distorted, disfigured, motion smear, motion artifacts, "
        "fused fingers, bad anatomy, weird hand, ugly"
    ),
    ckpt_name="ltx-video-2b-v0.9.5.safetensors",
    clip_name="t5xxl_fp16.safetensors",
    clip_type="ltxv",
    width=768,
    height=512,
    length=97,
    batch_size=1,
    strength=0.15,
    frame_rate=24,
    steps=30,
    max_shift=2.05,
    base_shift=0.95,
    stretch=True,
    terminal=0.1,
    sampler_name="euler",
    add_noise=True,
    seed=73662340640206,
    cfg=3.0,
    format="video/h264-mp4",
    loop_count=0,
    pingpong=False,
    save_output=True,
    server=None,
    headers=None,
    api_prefix=None,
    run_id=None,
    filename_prefix=None,
    workflow=None,
):
    if not image or not str(image).strip():
        raise ValueError("image is required and must be a Comfy input filename")
    if image_source not in {"input", "output"}:
        raise ValueError("image_source must be 'input' or 'output'")

    resolved_run_id = ensure_run_id(run_id)
    resolved_prefix = filename_prefix or make_stage_prefix(resolved_run_id, "ltxv_img2video")

    wf = workflow or Workflow(
        server=server or os.getenv("COMFY_URL"),
        headers=_resolve_headers(headers),
        api_prefix=api_prefix,
    )

    model, _, vae = wf.checkpointloadersimple(ckpt_name=ckpt_name)
    clip = wf.cliploader(clip_name=clip_name, type=clip_type, device="default")[0]
    image_name = str(image)
    if image_source == "output":
        suffix = os.path.splitext(image_name)[1] or ".png"
        transferred = wf.transfer_output_to_input(
            image_meta={
                "filename": image_name,
                "subfolder": image_subfolder,
                "type": image_type,
            },
            remote_name=f"{resolved_run_id}_video_source{suffix}",
            overwrite=True,
        )
        image_name = transferred["remote_name"]

    source = wf.loadimage(image=image_name, upload="image")[0]

    pos = wf.cliptextencode(clip=clip, text=prompt)[0]
    neg = wf.cliptextencode(clip=clip, text=negative_prompt)[0]

    img2video = wf.ltxvimgtovideo(
        positive=pos,
        negative=neg,
        vae=vae,
        image=source,
        width=width,
        height=height,
        length=length,
        batch_size=batch_size,
        strength=strength,
    )
    img2video_pos = img2video[0]
    img2video_neg = img2video[1]
    latent = img2video[2]

    conditioned_pos, conditioned_neg = wf.ltxvconditioning(
        positive=img2video_pos,
        negative=img2video_neg,
        frame_rate=frame_rate,
    )

    sampler = wf.ksamplerselect(sampler_name=sampler_name)[0]
    sigmas = wf.ltxvscheduler(
        steps=steps,
        max_shift=max_shift,
        base_shift=base_shift,
        stretch=stretch,
        terminal=terminal,
        latent=latent,
    )[0]

    sampled = wf.samplercustom(
        model=model,
        add_noise=add_noise,
        noise_seed=seed,
        cfg=cfg,
        positive=conditioned_pos,
        negative=conditioned_neg,
        sampler=sampler,
        sigmas=sigmas,
        latent_image=latent,
    )[0]

    decoded = wf.vaedecode(samples=sampled, vae=vae)[0]
    wf.vhs_videocombine(
        images=decoded,
        vae=vae,
        frame_rate=frame_rate,
        loop_count=loop_count,
        filename_prefix=resolved_prefix,
        format=format,
        pingpong=pingpong,
        save_output=save_output,
    )

    input_artifact = build_artifact(
        role="input_1",
        local_path=None,
        remote_name=str(image),
        source="comfy_input",
        node_id=None,
        subfolder="",
        type="input",
        downloaded_path=None,
    )

    return wf, resolved_run_id, resolved_prefix, input_artifact


def run(
    image,
    image_source="input",
    image_subfolder="",
    image_type="output",
    history_retries=120,
    history_delay=1.0,
    **kwargs,
):
    wf, resolved_run_id, filename_prefix, input_artifact = build(
        image=image,
        image_source=image_source,
        image_subfolder=image_subfolder,
        image_type=image_type,
        **kwargs,
    )
    run_result = wf.run()
    prompt_id = run_result.get("prompt_id")
    output_items = wf.saved_images(prompt_id, retries=history_retries, delay=history_delay)

    output_artifacts = [
        build_artifact(
            role="output",
            local_path=None,
            remote_name=item.get("filename"),
            source="comfy_history",
            node_id=item.get("node_id"),
            subfolder=item.get("subfolder", ""),
            type=item.get("type", "output"),
            downloaded_path=None,
        )
        for item in output_items
    ]

    return {
        "status": "done",
        "skill": "generate_ltxv_img2video",
        "run_id": resolved_run_id,
        "prompt_id": prompt_id,
        "filename_prefix": filename_prefix,
        "output_items": output_items,
        "artifacts": [input_artifact] + output_artifacts,
    }
