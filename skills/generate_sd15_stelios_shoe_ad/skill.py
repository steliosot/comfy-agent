from comfy_agent import Workflow

COMFY_URL = "http://127.0.0.1:8000"


def run(
    prompt="""cinematic advertisement for luxury shoes called Stelios, stylish young man
walking confidently through a modern city street at golden hour, premium
fashion commercial, elegant close-up focus on the shoes, smooth tracking
shot, polished reflections on the pavement, luxury brand campaign, warm
sunlight, shallow depth of field, realistic, high-end commercial look,
heroic fashion photography, urban lifestyle, premium leather shoes""",
    negative_prompt="""watermark, text, blurry, low quality, bad anatomy, extra limbs,
deformed feet, distorted shoes, jittery motion, shaky camera,
logo glitches, duplicate person""",
    width=512,
    height=768,
    batch_size=60,
    steps=20,
    fps=6,
    seed=2026031701,
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
        filename_prefix="stelios_shoe_ad",
        fps=fps,
        lossless=False,
        quality=80,
        method="default",
    )
    wf.run()

    return {"status": "done", "output": "stelios_shoe_ad"}
