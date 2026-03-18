from comfy_agent import Workflow


COMFY_URL = "http://127.0.0.1:8000"

wf = Workflow(COMFY_URL)

source = wf.loadimage(
    image="a124c61d-bb3f-4485-9c6b-fec142e56e6d.JPG"
)[0]

model, clip, vae = wf.checkpointloadersimple(
    ckpt_name="sd3/sd3_medium_incl_clips.safetensors"
)

model, clip = wf.loraloader(
    model=model,
    clip=clip,
    lora_name="sd15/CakeStyle.safetensors",
    strength_model=1,
    strength_clip=1,
)

scaled = wf.imagescale(
    image=source,
    upscale_method="nearest-exact",
    width=1024,
    height=1024,
    crop="disabled",
)

latent = wf.vaeencode(
    pixels=scaled,
    vae=vae,
)

pos = wf.cliptextencode(
    clip=clip,
    text="""face focus, cute, masterpiece, best quality, 1girl, green hair, sweater,
looking at viewer, upper body, beanie, outdoors, night, turtleneck

Animated""",
)

neg = wf.cliptextencode(
    clip=clip,
    text="""lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit,
fewer digits, cropped, worst quality, low quality, normal quality,
jpeg artifacts, signature, watermark, username, blurry""",
)

samples = wf.ksampler(
    model=model,
    positive=pos,
    negative=neg,
    latent_image=latent,
    seed=981291770453895,
    steps=20,
    cfg=8,
    sampler_name="dpmpp_2m",
    scheduler="sgm_uniform",
    denoise=1,
)

img = wf.vaedecode(
    samples=samples,
    vae=vae,
)

wf.previewimage(images=img)
wf.saveimage(
    images=img,
    filename_prefix="s_img2txt_lora",
)

wf.run(debug=True)
