import os

from comfy_agent import Workflow


DEFAULT_COMFY_URL = "http://127.0.0.1:8000"


def _resolve_headers(headers):
    if headers is not None:
        return headers
    auth_header = os.getenv("COMFY_AUTH_HEADER")
    if auth_header:
        return {"Authorization": auth_header}
    return None


def build(
    prompt="A cute 3D-rendered cartoon cat curiously looks at the camera with big, sparkling eyes.",
    negative_prompt="Overexposure, static, blurred details, low quality, artifacts",
    unet_name="wan2.1/wan2.1_t2v_1.3B_fp16.safetensors",
    clip_name="umt5_xxl_fp8_e4m3fn_scaled.safetensors",
    vae_name="wan_2.1_vae.safetensors",
    width=832,
    height=480,
    batch_size=1,
    seed=226274808933316,
    steps=10,
    cfg=8,
    sampler_name="uni_pc",
    scheduler="simple",
    denoise=1,
    frame_rate=16,
    loop_count=0,
    filename_prefix="wan21_cat_skill",
    format="image/gif",
    pingpong=False,
    save_output=True,
    server=None,
    headers=None,
    api_prefix=None,
):
    wf = Workflow(
        server or os.getenv("COMFY_URL", DEFAULT_COMFY_URL),
        headers=_resolve_headers(headers),
        api_prefix=api_prefix,
    )

    model = wf.unetloader(unet_name=unet_name, weight_dtype="default")[0]
    clip = wf.cliploader(clip_name=clip_name, type="wan", device="default")[0]
    vae = wf.vaeloader(vae_name=vae_name)[0]

    pos = wf.cliptextencode(clip=clip, text=prompt)[0]
    neg = wf.cliptextencode(clip=clip, text=negative_prompt)[0]
    latent = wf.emptylatentimage(width=width, height=height, batch_size=batch_size)[0]

    samples = wf.ksampler(
        model=model,
        positive=pos,
        negative=neg,
        latent_image=latent,
        seed=seed,
        steps=steps,
        cfg=cfg,
        sampler_name=sampler_name,
        scheduler=scheduler,
        denoise=denoise,
    )[0]

    images = wf.vaedecode(samples=samples, vae=vae)[0]

    wf.vhs_videocombine(
        images=images,
        frame_rate=frame_rate,
        loop_count=loop_count,
        filename_prefix=filename_prefix,
        format=format,
        pingpong=pingpong,
        save_output=save_output,
    )

    return wf


def run(**kwargs):
    wf = build(**kwargs)
    run_result = wf.run()
    return {
        "status": "done",
        "skill": "generate_wan21_cat_gif",
        "prompt_id": run_result.get("prompt_id"),
        "output_images": wf.saved_images(run_result.get("prompt_id")),
    }

