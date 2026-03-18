"""
Comfy Agent Workflow Test: SD15 Landscape Batch

This example generates multiple images in one run so batch handling can
be tested while keeping the same SD1.5 checkpoint and sampler settings.

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
epic mountain valley at sunrise, winding river, pine forest,
golden morning fog, cinematic landscape photography,
volumetric light, crisp details, wide composition
"""
)

neg = wf.cliptextencode(
    clip=clip,
    text="watermark, text, low quality, blurry, oversaturated"
)

latent = wf.emptylatentimage(
    width=768,
    height=512,
    batch_size=3
)

samples = wf.ksampler(
    model=model,
    positive=pos,
    negative=neg,
    latent_image=latent,
    seed=440912775103002,
    steps=30,
    cfg=7.0,
    sampler_name="euler",
    scheduler="normal",
    denoise=1.0
)

img = wf.vaedecode(samples=samples, vae=vae)

wf.saveimage(
    images=img,
    filename_prefix="sd15_landscape_batch"
)

wf.run()
