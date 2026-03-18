"""
Comfy Agent Workflow Test: SD15 Img2Img Remix

This example exercises a compatibility path that uses image-to-image
generation with the same Juggernaut SD1.5 checkpoint.

Pipeline
--------
LoadImage -> CheckpointLoaderSimple -> CLIPTextEncode -> VAEEncode
-> KSampler -> VAEDecode -> SaveImage

Requirements
------------
ComfyUI running at:
http://127.0.0.1:8000

Required model:
models/checkpoints/sd15/juggernaut_reborn.safetensors

Required input image:
Place remix_source.png in the ComfyUI input directory.
"""

import sys

from comfy_agent import Workflow

COMFY_URL = "http://127.0.0.1:8000"

wf = Workflow(COMFY_URL)

source_image = wf.loadimage(
    image="remix_source.png"
)[0]

model, clip, vae = wf.checkpointloadersimple(
    ckpt_name="sd15/juggernaut_reborn.safetensors"
)

pos = wf.cliptextencode(
    clip=clip,
    text="""
cinematic sci-fi repaint of the source image, dramatic lighting,
high detail, realistic textures, polished composition
"""
)

neg = wf.cliptextencode(
    clip=clip,
    text="watermark, text, blurry, low quality, artifacts"
)

latent = wf.vaeencode(
    pixels=source_image,
    vae=vae
)

samples = wf.ksampler(
    model=model,
    positive=pos,
    negative=neg,
    latent_image=latent,
    seed=56120499810023,
    steps=28,
    cfg=7.0,
    sampler_name="euler",
    scheduler="normal",
    denoise=0.55
)

img = wf.vaedecode(
    samples=samples,
    vae=vae
)

wf.saveimage(
    images=img,
    filename_prefix="sd15_img2img_remix"
)

wf.run()
