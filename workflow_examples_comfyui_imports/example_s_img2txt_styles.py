from comfy_agent import Workflow


COMFY_URL = "http://127.0.0.1:8000"

wf = Workflow(COMFY_URL)

model, clip, vae = wf.checkpointloadersimple(
    ckpt_name="sd1.5/juggernaut_reborn.safetensors"
)

style_pos, style_neg = wf.node(
    "Load Styles CSV",
    styles="Fashion | Vintage",
    csv_file_path="styles.csv",
)

pos = wf.cliptextencode(
    clip=clip,
    text=style_pos,
)

neg = wf.cliptextencode(
    clip=clip,
    text=style_neg,
)

latent = wf.emptylatentimage(
    width=1024,
    height=1024,
    batch_size=1,
)

samples = wf.ksampler(
    model=model,
    positive=pos,
    negative=neg,
    latent_image=latent,
    seed=271043077902139,
    steps=30,
    cfg=30,
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
