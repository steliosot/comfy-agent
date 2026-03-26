import os
from pathlib import Path

from comfy_agent import Workflow
from comfy_agent.artifacts import build_artifact, ensure_run_id, make_stage_prefix
from comfy_agent.config import ComfyConfig


def _resolve_headers(headers):
    if headers is not None:
        return headers
    auth_header = os.getenv("COMFY_AUTH_HEADER")
    if auth_header:
        return {"Authorization": auth_header}
    return None


def _normalize_images(images=None, image1=None, image2=None, image3=None):
    values = []
    if images:
        values.extend(images)
    for item in [image1, image2, image3]:
        if item:
            values.append(item)
    normalized = [str(v) for v in values if str(v).strip()]
    if len(normalized) < 2:
        raise ValueError("At least 2 images are required")
    if len(normalized) > 3:
        raise ValueError("At most 3 images are supported")
    return normalized


def _resolve_image_sources(images, run_id, wf, upload_inputs):
    artifacts = []
    remote_names = []
    for idx, image in enumerate(images, start=1):
        if upload_inputs:
            path = Path(image)
            if not path.exists():
                raise FileNotFoundError(f"Input image not found: {image}")
            remote_name = f"{run_id}_input{idx}{path.suffix or '.png'}"
            uploaded = wf.upload_image(
                local_path=str(path),
                remote_name=remote_name,
                overwrite=True,
                type="input",
            )
            remote_names.append(uploaded["remote_name"])
            artifacts.append(
                build_artifact(
                    role=f"input_{idx}",
                    local_path=uploaded.get("local_path"),
                    remote_name=uploaded.get("remote_name"),
                    source=uploaded.get("source", "upload"),
                    node_id=None,
                    subfolder=uploaded.get("subfolder", ""),
                    type=uploaded.get("type", "input"),
                    downloaded_path=None,
                )
            )
        else:
            remote_names.append(image)
            artifacts.append(
                build_artifact(
                    role=f"input_{idx}",
                    local_path=None,
                    remote_name=image,
                    source="comfy_input",
                    node_id=None,
                    subfolder="",
                    type="input",
                    downloaded_path=None,
                )
            )
    return remote_names, artifacts


def build(
    prompt,
    images=None,
    image1=None,
    image2=None,
    image3=None,
    width=1024,
    height=1024,
    batch_size=1,
    seed=240917432485804,
    steps=10,
    cfg=1.0,
    sampler_name="euler",
    scheduler="simple",
    denoise=1.0,
    upscale_method="nearest-exact",
    megapixels=1.0,
    resolution_steps=1,
    unet_name="flux-2-klein-4b-fp8.safetensors",
    clip_name="qwen_3_4b.safetensors",
    clip_type="flux2",
    vae_name="flux2-vae.safetensors",
    ckpt_name="sd1.5/juggernaut_reborn.safetensors",
    engine="auto",
    server=None,
    headers=None,
    api_prefix=None,
    run_id=None,
    upload_inputs=True,
    workflow=None,
    filename_prefix=None,
):
    resolved_run_id = ensure_run_id(run_id)
    resolved_filename_prefix = filename_prefix or make_stage_prefix(
        resolved_run_id, "flux_multi_input"
    )
    image_values = _normalize_images(images=images, image1=image1, image2=image2, image3=image3)

    wf = workflow or Workflow(
        server=server or os.getenv("COMFY_URL"),
        headers=_resolve_headers(headers),
        api_prefix=api_prefix,
    )

    remote_images, input_artifacts = _resolve_image_sources(
        image_values,
        resolved_run_id,
        wf,
        upload_inputs=upload_inputs,
    )

    def _choices(node_name, input_name):
        node_info = wf.registry.get(node_name, {})
        req = node_info.get("input", {}).get("required", {})
        spec = req.get(input_name)
        if not spec:
            return []
        values = spec[0]
        if isinstance(values, (list, tuple)):
            return list(values)
        return []

    unet_choices = _choices("UNETLoader", "unet_name")
    clip_choices = _choices("CLIPLoader", "clip_name")
    vae_choices = _choices("VAELoader", "vae_name")
    use_flux = (
        engine == "flux"
        or (
            engine == "auto"
            and unet_name in unet_choices
            and clip_name in clip_choices
            and vae_name in vae_choices
        )
    )

    if use_flux:
        model = wf.unetloader(unet_name=unet_name, weight_dtype="default")[0]
        clip = wf.cliploader(clip_name=clip_name, type=clip_type, device="default")[0]
        vae = wf.vaeloader(vae_name=vae_name)[0]
        latent = wf.emptyflux2latentimage(width=width, height=height, batch_size=batch_size)[0]
        resolved_engine = "flux"
    else:
        model, clip, vae = wf.checkpointloadersimple(ckpt_name=ckpt_name)
        latent = wf.emptylatentimage(width=width, height=height, batch_size=batch_size)[0]
        resolved_engine = "checkpoint"

    positive = wf.cliptextencode(clip=clip, text=prompt)[0]
    negative = wf.conditioningzeroout(conditioning=positive)[0]

    for image_name in remote_images:
        base_image = wf.loadimage(image=image_name)[0]
        scaled_image = wf.imagescaletototalpixels(
            image=base_image,
            upscale_method=upscale_method,
            megapixels=megapixels,
            resolution_steps=resolution_steps,
        )[0]
        reference_latent = wf.vaeencode(pixels=scaled_image, vae=vae)[0]
        positive = wf.referencelatent(
            conditioning=positive,
            latent=reference_latent,
        )[0]
        negative = wf.referencelatent(
            conditioning=negative,
            latent=reference_latent,
        )[0]

    sampled = wf.ksampler(
        model=model,
        seed=seed,
        steps=steps,
        cfg=cfg,
        sampler_name=sampler_name,
        scheduler=scheduler,
        positive=positive,
        negative=negative,
        latent_image=latent,
        denoise=denoise,
    )[0]

    image = wf.vaedecode(samples=sampled, vae=vae)[0]
    wf.saveimage(images=image, filename_prefix=resolved_filename_prefix)

    return wf, resolved_run_id, resolved_filename_prefix, input_artifacts, resolved_engine


def run(
    prompt,
    images=None,
    image1=None,
    image2=None,
    image3=None,
    output_dir=None,
    download_output=True,
    history_retries=60,
    history_delay=1.0,
    **kwargs,
):
    cfg = ComfyConfig.from_env(load_env=True)
    wf, resolved_run_id, filename_prefix, input_artifacts, selected_engine = build(
        prompt=prompt,
        images=images,
        image1=image1,
        image2=image2,
        image3=image3,
        **kwargs,
    )
    run_result = wf.run()
    prompt_id = run_result.get("prompt_id")
    output_images = wf.saved_images(
        prompt_id,
        retries=history_retries,
        delay=history_delay,
    )

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
        for item in output_images
    ]

    downloaded = []
    if download_output:
        resolved_output_dir = output_dir or cfg.output_dir
        for index, meta in enumerate(output_images, start=1):
            downloaded.append(
                wf.download_image(
                    image_meta=meta,
                    output_path=str(
                        Path(resolved_output_dir)
                        / f"{filename_prefix}_{index}{Path(meta.get('filename', 'x.png')).suffix or '.png'}"
                    ),
                    output_dir=resolved_output_dir,
                )
            )
        for item in downloaded:
            output_artifacts.append(
                build_artifact(
                    role="downloaded_output",
                    local_path=item.get("downloaded_path"),
                    remote_name=item.get("filename"),
                    source=item.get("source", "download"),
                    node_id=item.get("node_id"),
                    subfolder=item.get("subfolder", ""),
                    type=item.get("type", "output"),
                    downloaded_path=item.get("downloaded_path"),
                )
            )

    return {
        "status": "done",
        "skill": "generate_flux_multi_input_img2img",
        "run_id": resolved_run_id,
        "prompt_id": prompt_id,
        "filename_prefix": filename_prefix,
        "engine": selected_engine,
        "image_count": len(_normalize_images(images=images, image1=image1, image2=image2, image3=image3)),
        "output_images": output_images,
        "downloaded": downloaded,
        "artifacts": input_artifacts + output_artifacts,
    }
