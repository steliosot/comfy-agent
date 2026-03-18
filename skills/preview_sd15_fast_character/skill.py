from comfy_agent import Workflow

COMFY_URL = "http://127.0.0.1:8000"


def run(
    prompt="""stylized explorer character, leather coat, brass gadgets,
full body pose, neutral studio background, clean silhouette,
game concept art, detailed costume""",
    negative_prompt="watermark, text, blurry, duplicate limbs, low quality",
    steps=12,
    seed=192837465,
):
    wf = Workflow(COMFY_URL)

    model, clip, vae = wf.checkpointloadersimple(
        ckpt_name="sd15/juggernaut_reborn.safetensors"
    )

    pos = wf.cliptextencode(clip=clip, text=prompt)
    neg = wf.cliptextencode(clip=clip, text=negative_prompt)
    latent = wf.emptylatentimage(width=512, height=512, batch_size=1)

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
        denoise=1.0,
    )

    img = wf.vaedecode(samples=samples, vae=vae)
    wf.previewimage(images=img)
    wf.run()

    return {"status": "preview shown"}
