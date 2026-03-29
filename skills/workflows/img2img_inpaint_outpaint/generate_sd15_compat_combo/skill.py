from comfy_agent import Workflow


def run(
    image="agentic_1773257438367_00001_.png",
    prompt="""cinematic redesign of the source image, crisp details,
realistic lighting, polished textures, strong composition,
high quality concept art""",
    negative_prompt="watermark, text, blurry, artifacts, low quality, distorted anatomy",
    x=64,
    y=64,
    width=512,
    height=512,
    steps=20,
    denoise=0.5,
    seed=845102994511,
):
    wf = build(
        image=image,
        prompt=prompt,
        negative_prompt=negative_prompt,
        x=x,
        y=y,
        width=width,
        height=height,
        steps=steps,
        denoise=denoise,
        seed=seed,
    )
    wf.run()

    return {"status": "done", "output": "sd15_compat_combo"}


def build(
    image="agentic_1773257438367_00001_.png",
    prompt="""cinematic redesign of the source image, crisp details,
realistic lighting, polished textures, strong composition,
high quality concept art""",
    negative_prompt="watermark, text, blurry, artifacts, low quality, distorted anatomy",
    x=64,
    y=64,
    width=512,
    height=512,
    steps=20,
    denoise=0.5,
    seed=845102994511,
):
    wf = Workflow()

    source_image = wf.loadimage(image=image)[0]
    cropped = wf.imagecrop(
        image=source_image,
        x=x,
        y=y,
        width=width,
        height=height,
    )

    model, clip, vae = wf.checkpointloadersimple(
        ckpt_name="sd1.5/juggernaut_reborn.safetensors"
    )

    pos = wf.cliptextencode(clip=clip, text=prompt)
    neg = wf.cliptextencode(clip=clip, text=negative_prompt)
    latent = wf.vaeencode(pixels=cropped, vae=vae)

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
        denoise=denoise,
    )

    img = wf.vaedecode(samples=samples, vae=vae)
    wf.previewimage(images=img)
    wf.saveimage(images=img, filename_prefix="sd15_compat_combo")

    return wf
