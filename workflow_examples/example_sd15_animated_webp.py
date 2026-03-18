"""
Comfy Agent Workflow Test: SD15 Animated WEBP

This is a simple animation/export example for compatibility testing.
It generates a small batch of SD1.5 frames and sends them to
SaveAnimatedWEBP so ComfyUI exports an animated file.

This is not true temporally coherent video generation. It is mainly a
sanity check for:
- batch image generation
- animated export nodes
- end-to-end workflow submission

Pipeline
--------
CheckpointLoaderSimple -> CLIPTextEncode -> EmptyLatentImage
-> KSampler -> VAEDecode -> SaveAnimatedWEBP

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
stylized robot walking through neon rain, cinematic lighting,
dynamic pose, reflective street, detailed concept art
"""
)

neg = wf.cliptextencode(
    clip=clip,
    text="watermark, text, blurry, low quality, extra limbs"
)

# Batch generation gives us multiple frames to export as an animation.
latent = wf.emptylatentimage(
    width=512,
    height=512,
    batch_size=8
)

samples = wf.ksampler(
    model=model,
    positive=pos,
    negative=neg,
    latent_image=latent,
    seed=20260317,
    steps=20,
    cfg=7.0,
    sampler_name="euler",
    scheduler="normal",
    denoise=1.0
)

img = wf.vaedecode(
    samples=samples,
    vae=vae
)

# If your ComfyUI build includes SaveAnimatedWEBP, this should export an
# animated .webp to the output directory.
wf.saveanimatedwebp(
    images=img,
    filename_prefix="sd15_anim_test",
    fps=6,
    lossless=False,
    quality=80,
    method="default"
)

wf.run(debug=True)
