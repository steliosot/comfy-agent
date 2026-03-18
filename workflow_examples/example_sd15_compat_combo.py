"""
Comfy Agent Workflow Test: SD15 Compatibility Combo

This example combines several core nodes into one workflow so you can
test a broader compatibility path with a single run.

Pipeline
--------
LoadImage -> ImageCrop -> CheckpointLoaderSimple -> CLIPTextEncode
-> VAEEncode -> KSampler -> VAEDecode -> PreviewImage + SaveImage

Nodes covered
-------------
- LoadImage
- ImageCrop
- CheckpointLoaderSimple
- CLIPTextEncode
- VAEEncode
- KSampler
- VAEDecode
- PreviewImage
- SaveImage

Requirements
------------
ComfyUI running at:
http://127.0.0.1:8000

Required model:
models/checkpoints/sd1.5/juggernaut_reborn.safetensors

Required input image:
Place agentic_1773257438367_00001_.png in the ComfyUI input directory.
"""

import sys

from comfy_agent import Workflow

COMFY_URL = "http://127.0.0.1:8000"

wf = Workflow(COMFY_URL)

# Load an input image from ComfyUI/input
source_image = wf.loadimage(
    image="agentic_1773257438367_00001_.png"
)[0]

# Crop to a stable square region before img2img processing
cropped = wf.imagecrop(
    image=source_image,
    x=64,
    y=64,
    width=512,
    height=512
)

model, clip, vae = wf.checkpointloadersimple(
    ckpt_name="sd1.5/juggernaut_reborn.safetensors"
)

pos = wf.cliptextencode(
    clip=clip,
    text="""
cinematic redesign of the source image, crisp details,
realistic lighting, polished textures, strong composition,
high quality concept art
"""
)

neg = wf.cliptextencode(
    clip=clip,
    text="watermark, text, blurry, artifacts, low quality, distorted anatomy"
)

latent = wf.vaeencode(
    pixels=cropped,
    vae=vae
)

samples = wf.ksampler(
    model=model,
    positive=pos,
    negative=neg,
    latent_image=latent,
    seed=845102994511,
    steps=20,
    cfg=7.0,
    sampler_name="euler",
    scheduler="normal",
    denoise=0.5
)

img = wf.vaedecode(
    samples=samples,
    vae=vae
)

# Send to both preview and output so both action nodes are exercised.
wf.previewimage(images=img)

wf.saveimage(
    images=img,
    filename_prefix="sd15_compat_combo"
)

wf.run(debug=True)
