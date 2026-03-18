from comfy_agent import Workflow


COMFY_URL = "http://127.0.0.1:8000"

wf = Workflow(COMFY_URL)

source = wf.loadimage(
    image="a124c61d-bb3f-4485-9c6b-fec142e56e6d.JPG"
)[0]

model, clip, vae = wf.checkpointloadersimple(
    ckpt_name="sdxl/juggernautXL_version2.safetensors"
)

pos = wf.cliptextencode(
    clip=clip,
    text="Generate an image of a (Japan) (brown hair) girl\n",
)

neg = wf.cliptextencode(
    clip=clip,
    text="ugly",
)

latent = wf.vaeencode(
    pixels=source,
    vae=vae,
)

samples = wf.ksampler(
    model=model,
    positive=pos,
    negative=neg,
    latent_image=latent,
    seed=89030519922403,
    steps=20,
    cfg=8,
    sampler_name="dpmpp_2m",
    scheduler="karras",
    denoise=0.85,
)

img = wf.vaedecode(
    samples=samples,
    vae=vae,
)

wf.previewimage(images=img)
wf.saveimage(
    images=img,
    filename_prefix="s_txt2img_load_img",
)

wf.run(debug=True)
