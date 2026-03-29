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


def _choices(registry, node_name, input_name):
    node_info = registry.get(node_name, {})
    required = node_info.get("input", {}).get("required", {})
    spec = required.get(input_name)
    if not spec:
        return []
    values = spec[0]
    if isinstance(values, (list, tuple)):
        return [str(v) for v in values]
    return []


def _select_engine(wf, engine, unet_name, clip_name, vae_name):
    unet_choices = _choices(wf.registry, "UNETLoader", "unet_name")
    clip_choices = _choices(wf.registry, "CLIPLoader", "clip_name")
    vae_choices = _choices(wf.registry, "VAELoader", "vae_name")
    if engine == "flux":
        return "flux"
    if engine == "checkpoint":
        return "checkpoint"
    if unet_name in unet_choices and clip_name in clip_choices and vae_name in vae_choices:
        return "flux"
    return "checkpoint"


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
    upload_inputs=False,
    workflow=None,
    filename_prefix=None,
):
    if upload_inputs:
        raise ValueError(
            "generate_flux_multi_input_img2img is generation-only. "
            "Use upload_image skill before this skill."
        )

    resolved_run_id = ensure_run_id(run_id)
    resolved_filename_prefix = filename_prefix or make_stage_prefix(
        resolved_run_id, "flux_multi_input"
    )
    remote_images = _normalize_images(images=images, image1=image1, image2=image2, image3=image3)

    wf = workflow or Workflow(
        server=server or os.getenv("COMFY_URL"),
        headers=_resolve_headers(headers),
        api_prefix=api_prefix,
    )

    resolved_engine = _select_engine(wf, engine, unet_name, clip_name, vae_name)
    if resolved_engine == "flux":
        model = wf.unetloader(unet_name=unet_name, weight_dtype="default")[0]
        clip = wf.cliploader(clip_name=clip_name, type=clip_type, device="default")[0]
        vae = wf.vaeloader(vae_name=vae_name)[0]
        latent = wf.emptyflux2latentimage(width=width, height=height, batch_size=batch_size)[0]
    else:
        model, clip, vae = wf.checkpointloadersimple(ckpt_name=ckpt_name)
        latent = wf.emptylatentimage(width=width, height=height, batch_size=batch_size)[0]

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
        positive = wf.referencelatent(conditioning=positive, latent=reference_latent)[0]
        negative = wf.referencelatent(conditioning=negative, latent=reference_latent)[0]

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

    input_artifacts = [
        build_artifact(
            role=f"input_{index}",
            local_path=None,
            remote_name=name,
            source="comfy_input",
            node_id=None,
            subfolder="",
            type="input",
            downloaded_path=None,
        )
        for index, name in enumerate(remote_images, start=1)
    ]

    return wf, resolved_run_id, resolved_filename_prefix, input_artifacts, resolved_engine


def run(
    prompt,
    images=None,
    image1=None,
    image2=None,
    image3=None,
    history_retries=60,
    history_delay=1.0,
    download_output=False,
    **kwargs,
):
    if download_output:
        raise ValueError(
            "generate_flux_multi_input_img2img is generation-only. "
            "Use download_image skill after this skill."
        )

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
    output_images = wf.saved_images(prompt_id, retries=history_retries, delay=history_delay)

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

    return {
        "status": "done",
        "skill": "generate_flux_multi_input_img2img",
        "run_id": resolved_run_id,
        "prompt_id": prompt_id,
        "filename_prefix": filename_prefix,
        "engine": selected_engine,
        "image_count": len(_normalize_images(images=images, image1=image1, image2=image2, image3=image3)),
        "output_images": output_images,
        "artifacts": input_artifacts + output_artifacts,
    }
