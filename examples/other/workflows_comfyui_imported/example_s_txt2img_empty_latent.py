from comfy_agent import Workflow


COMFY_URL = "http://127.0.0.1:8000"

wf = Workflow(COMFY_URL)

model, clip, vae = wf.checkpointloadersimple(
    ckpt_name="sd1.5/juggernaut_reborn.safetensors"
)

pos = wf.cliptextencode(
    clip=clip,
    text="beautiful scenery nature glass bottle landscape, , purple galaxy bottle,",
)

neg = wf.cliptextencode(
    clip=clip,
    text="text, watermark",
)

latent = wf.emptylatentimage(
    width=512,
    height=512,
    batch_size=1,
)

samples = wf.ksampler(
    model=model,
    positive=pos,
    negative=neg,
    latent_image=latent,
    seed=156680208700286,
    steps=20,
    cfg=8,
    sampler_name="euler",
    scheduler="normal",
    denoise=1,
)

img = wf.vaedecode(
    samples=samples,
    vae=vae,
)

wf.saveimage(
    images=img,
    filename_prefix="ComfyUI",
)

wf.run(debug=True)
