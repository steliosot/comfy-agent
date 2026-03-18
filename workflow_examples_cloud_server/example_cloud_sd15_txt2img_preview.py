"""
Comfy Agent Workflow Test: SD15 txt2img (Cloud)

Pipeline:
CheckpointLoaderSimple -> CLIPTextEncode -> EmptyLatentImage ->
KSampler -> VAEDecode -> PreviewImage + SaveImage
"""

import os

from comfy_agent import Workflow

COMFY_URL = os.getenv("COMFY_URL", "http://34.30.216.121")
AUTH_HEADER = os.getenv(
    "COMFY_AUTH_HEADER",
    "XXXXXX",
)
CKPT_NAME = os.getenv("COMFY_CKPT", "juggernaut_reborn.safetensors")

headers = {"Authorization": AUTH_HEADER} if AUTH_HEADER else {}

wf = Workflow(COMFY_URL, headers=headers)

model, clip, vae = wf.checkpointloadersimple(
    ckpt_name=CKPT_NAME
)

pos = wf.cliptextencode(
    clip=clip,
    text="cinematic portrait of a man in a city street, realistic, soft light"
)

neg = wf.cliptextencode(
    clip=clip,
    text="low quality, blurry, watermark, text"
)

latent = wf.emptylatentimage(
    width=512,
    height=512,
    batch_size=1
)

samples = wf.ksampler(
    model=model,
    positive=pos,
    negative=neg,
    latent_image=latent,
    seed=123456,
    steps=20,
    cfg=7.0,
    sampler_name="euler",
    scheduler="normal",
    denoise=1.0
)

img = wf.vaedecode(samples=samples, vae=vae)

wf.previewimage(images=img)
wf.saveimage(images=img, filename_prefix="cloud_sd15_txt2img_preview")

wf.run(debug=True)
