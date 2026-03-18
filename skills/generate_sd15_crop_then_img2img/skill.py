from comfy_agent import Workflow

COMFY_URL = "http://127.0.0.1:8000"


def run(
    image="crop_source.png",
    prompt="""refined editorial portrait based on the cropped source image,
soft studio light, crisp details, natural skin texture""",
    negative_prompt="watermark, text, blurry, low quality, distorted face",
    x=64,
    y=64,
    width=512,
    height=512,
    steps=24,
    denoise=0.5,
    seed=73111924500188,
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

    return {"status": "done", "output": "sd15_crop_then_img2img"}


def build(
    image="crop_source.png",
    prompt="""refined editorial portrait based on the cropped source image,
soft studio light, crisp details, natural skin texture""",
    negative_prompt="watermark, text, blurry, low quality, distorted face",
    x=64,
    y=64,
    width=512,
    height=512,
    steps=24,
    denoise=0.5,
    seed=73111924500188,
):
    wf = Workflow(COMFY_URL)

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
        cfg=6.8,
        sampler_name="euler",
        scheduler="normal",
        denoise=denoise,
    )

    img = wf.vaedecode(samples=samples, vae=vae)
    wf.saveimage(images=img, filename_prefix="sd15_crop_then_img2img")

    return wf
