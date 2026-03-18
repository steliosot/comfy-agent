"""
Comfy Agent Workflow Test: SD15 Cinematic Portrait

This example exercises the standard text-to-image pipeline using the
same SD1.5 checkpoint as the other tests, but with a portrait-oriented
composition and a more descriptive prompt.

Pipeline
--------
CheckpointLoaderSimple -> CLIPTextEncode -> EmptyLatentImage
-> KSampler -> VAEDecode -> SaveImage

Requirements
------------
ComfyUI running at:
http://127.0.0.1:8000

Required model:
models/checkpoints/sd15/juggernaut_reborn.safetensors
"""

import sys

from comfy_agent import Workflow

COMFY_URL = "http://127.0.0.1:8000"

wf = Workflow(COMFY_URL)

model, clip, vae = wf.checkpointloadersimple(
    ckpt_name="sd15/juggernaut_reborn.safetensors"
)

pos = wf.cliptextencode(
    clip=clip,
    text="""
cinematic portrait of a weathered space courier, detailed face,
subtle freckles, dramatic rim light, moody atmosphere, 35mm photo,
high contrast, realistic skin texture, shallow depth of field,
dark teal background, ultra detailed
"""
)

neg = wf.cliptextencode(
    clip=clip,
    text="watermark, text, logo, blurry, deformed hands, extra fingers"
)

latent = wf.emptylatentimage(
    width=512,
    height=768,
    batch_size=1
)

samples = wf.ksampler(
    model=model,
    positive=pos,
    negative=neg,
    latent_image=latent,
    seed=904210331245118,
    steps=35,
    cfg=7.0,
    sampler_name="euler",
    scheduler="normal",
    denoise=1.0
)

img = wf.vaedecode(samples=samples, vae=vae)

wf.saveimage(
    images=img,
    filename_prefix="sd15_cinematic_portrait"
)

wf.run()
