from comfy_agent import Workflow

COMFY_URL = "http://127.0.0.1:8000"


def run(
    image="preview_source.png",
    prompt="""stylized concept art repaint, stronger silhouette, richer contrast,
clean shapes, detailed costume design""",
    negative_prompt="watermark, text, blurry, muddy colors, extra limbs",
    steps=12,
    denoise=0.4,
    seed=1122334455,
):
    wf = Workflow(COMFY_URL)

    source_image = wf.loadimage(image=image)[0]
    model, clip, vae = wf.checkpointloadersimple(
        ckpt_name="sd15/juggernaut_reborn.safetensors"
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
        cfg=6.5,
        sampler_name="euler",
        scheduler="normal",
        denoise=denoise,
    )

    img = wf.vaedecode(samples=samples, vae=vae)
    wf.previewimage(images=img)
    wf.run()

    return {"status": "preview shown"}
