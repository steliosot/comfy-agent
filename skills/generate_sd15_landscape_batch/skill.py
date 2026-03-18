from comfy_agent import Workflow

COMFY_URL = "http://127.0.0.1:8000"


def run(
    prompt="""epic mountain valley at sunrise, winding river, pine forest,
golden morning fog, cinematic landscape photography,
volumetric light, crisp details, wide composition""",
    negative_prompt="watermark, text, low quality, blurry, oversaturated",
    width=768,
    height=512,
    batch_size=3,
    steps=30,
    seed=440912775103002,
):
    wf = build(
        prompt=prompt,
        negative_prompt=negative_prompt,
        width=width,
        height=height,
        batch_size=batch_size,
        steps=steps,
        seed=seed,
    )
    wf.run()

    return {"status": "done", "output": "sd15_landscape_batch"}


def build(
    prompt="""epic mountain valley at sunrise, winding river, pine forest,
golden morning fog, cinematic landscape photography,
volumetric light, crisp details, wide composition""",
    negative_prompt="watermark, text, low quality, blurry, oversaturated",
    width=768,
    height=512,
    batch_size=3,
    steps=30,
    seed=440912775103002,
):
    wf = Workflow(COMFY_URL)

    model, clip, vae = wf.checkpointloadersimple(
        ckpt_name="sd1.5/juggernaut_reborn.safetensors"
    )

    pos = wf.cliptextencode(clip=clip, text=prompt)
    neg = wf.cliptextencode(clip=clip, text=negative_prompt)
    latent = wf.emptylatentimage(width=width, height=height, batch_size=batch_size)

    samples = wf.ksampler(
        model=model,
        positive=pos,
        negative=neg,
        latent_image=latent,
        seed=seed,
        steps=steps,
        cfg=7.0,
        sampler_name="euler",
        scheduler="normal",
        denoise=1.0,
    )

    img = wf.vaedecode(samples=samples, vae=vae)

    wf.saveimage(images=img, filename_prefix="sd15_landscape_batch")

    return wf
