"""
Comfy Agent Workflow Test: SD15 Fast Character Preview

This example is tuned for quick prompt iteration. It uses the same
SD1.5 checkpoint but fewer steps and PreviewImage output for a lighter
testing loop in ComfyUI.

Pipeline
--------
CheckpointLoaderSimple -> CLIPTextEncode -> EmptyLatentImage
-> KSampler -> VAEDecode -> PreviewImage

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
stylized explorer character, leather coat, brass gadgets,
full body pose, neutral studio background, clean silhouette,
game concept art, detailed costume
"""
)

neg = wf.cliptextencode(
    clip=clip,
    text="watermark, text, blurry, duplicate limbs, low quality"
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
    seed=192837465,
    steps=12,
    cfg=6.5,
    sampler_name="euler",
    scheduler="normal",
    denoise=1.0
)

img = wf.vaedecode(samples=samples, vae=vae)

wf.previewimage(images=img)

wf.run()
