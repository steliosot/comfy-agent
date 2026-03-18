from comfy_agent import Workflow

COMFY_URL = "http://127.0.0.1:8000"


def run(
    image="remix_source.png",
    prompt="""cinematic sci-fi repaint of the source image, dramatic lighting,
high detail, realistic textures, polished composition""",
    negative_prompt="watermark, text, blurry, low quality, artifacts",
    steps=28,
    denoise=0.55,
    seed=56120499810023,
):
    wf = build(
        image=image,
        prompt=prompt,
        negative_prompt=negative_prompt,
        steps=steps,
        denoise=denoise,
        seed=seed,
    )
    wf.run()

    return {"status": "done", "output": "sd15_img2img_remix"}


def build(
    image="remix_source.png",
    prompt="""cinematic sci-fi repaint of the source image, dramatic lighting,
high detail, realistic textures, polished composition""",
    negative_prompt="watermark, text, blurry, low quality, artifacts",
    steps=28,
    denoise=0.55,
    seed=56120499810023,
):
    wf = Workflow(COMFY_URL)

    source_image = wf.loadimage(image=image)[0]
    model, clip, vae = wf.checkpointloadersimple(
        ckpt_name="sd1.5/juggernaut_reborn.safetensors"
    )

    pos = wf.cliptextencode(clip=clip, text=prompt)
    neg = wf.cliptextencode(clip=clip, text=negative_prompt)
    latent = wf.vaeencode(pixels=source_image, vae=vae)

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
    wf.saveimage(images=img, filename_prefix="sd15_img2img_remix")

    return wf
