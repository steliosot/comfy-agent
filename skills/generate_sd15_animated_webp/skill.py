from comfy_agent import Workflow

COMFY_URL = "http://127.0.0.1:8000"


def run(
    prompt="""stylized robot walking through neon rain, cinematic lighting,
dynamic pose, reflective street, detailed concept art""",
    negative_prompt="watermark, text, blurry, low quality, extra limbs",
    width=512,
    height=512,
    batch_size=8,
    steps=20,
    fps=6,
    seed=20260317,
):
    wf = Workflow(COMFY_URL)

    model, clip, vae = wf.checkpointloadersimple(
        ckpt_name="sd15/juggernaut_reborn.safetensors"
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

    wf.saveanimatedwebp(
        images=img,
        filename_prefix="sd15_anim_test",
        fps=fps,
        lossless=False,
        quality=80,
        method="default",
    )
    wf.run()

    return {"status": "done", "output": "sd15_anim_test"}
