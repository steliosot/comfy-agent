"""
Comfy Agent Workflow Test: SD15 Img2Img Preview

This example uses the img2img path with PreviewImage so compatibility
can be checked without writing files on every run.

Pipeline
--------
LoadImage -> CheckpointLoaderSimple -> CLIPTextEncode -> VAEEncode
-> KSampler -> VAEDecode -> PreviewImage

Requirements
------------
ComfyUI running at:
http://127.0.0.1:8000

Required model:
models/checkpoints/sd15/juggernaut_reborn.safetensors

Required input image:
Place preview_source.png in the ComfyUI input directory.
"""

import sys

from comfy_agent import Workflow

COMFY_URL = "http://127.0.0.1:8000"

wf = Workflow(COMFY_URL)

source_image = wf.loadimage(
    image="preview_source.png"
)[0]

model, clip, vae = wf.checkpointloadersimple(
    ckpt_name="sd15/juggernaut_reborn.safetensors"
)

pos = wf.cliptextencode(
    clip=clip,
    text="""
stylized concept art repaint, stronger silhouette, richer contrast,
clean shapes, detailed costume design
"""
)

neg = wf.cliptextencode(
    clip=clip,
    text="watermark, text, blurry, muddy colors, extra limbs"
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
    seed=1122334455,
    steps=12,
    cfg=6.5,
    sampler_name="euler",
    scheduler="normal",
    denoise=0.4
)

img = wf.vaedecode(
    samples=samples,
    vae=vae
)

wf.previewimage(images=img)

wf.run()
