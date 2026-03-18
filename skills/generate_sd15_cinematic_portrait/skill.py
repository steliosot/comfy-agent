from comfy_agent import Workflow

COMFY_URL = "http://127.0.0.1:8000"


def run(
    prompt="""cinematic portrait of a weathered space courier, detailed face,
subtle freckles, dramatic rim light, moody atmosphere, 35mm photo,
high contrast, realistic skin texture, shallow depth of field,
dark teal background, ultra detailed""",
    negative_prompt="watermark, text, logo, blurry, deformed hands, extra fingers",
    width=512,
    height=768,
    steps=35,
    seed=904210331245118,
):
    wf = Workflow(COMFY_URL)

    model, clip, vae = wf.checkpointloadersimple(
        ckpt_name="sd15/juggernaut_reborn.safetensors"
    )

    pos = wf.cliptextencode(clip=clip, text=prompt)
    neg = wf.cliptextencode(clip=clip, text=negative_prompt)
    latent = wf.emptylatentimage(width=width, height=height, batch_size=1)

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

    wf.saveimage(images=img, filename_prefix="sd15_cinematic_portrait")
    wf.run()

    return {"status": "done", "output": "sd15_cinematic_portrait"}
