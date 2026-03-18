"""
Comfy Agent Workflow Test: SD15 Crop Then Img2Img

This example adds ImageCrop into the path before VAE encoding so we can
test a slightly richer node chain with the same SD1.5 checkpoint.

Pipeline
--------
LoadImage -> ImageCrop -> CheckpointLoaderSimple -> CLIPTextEncode
-> VAEEncode -> KSampler -> VAEDecode -> SaveImage

Requirements
------------
ComfyUI running at:
http://127.0.0.1:8000

Required model:
models/checkpoints/sd1.5/juggernaut_reborn.safetensors

Required input image:
Place crop_source.png in the ComfyUI input directory.
"""

import sys

from comfy_agent import Workflow

COMFY_URL = "http://127.0.0.1:8000"

wf = Workflow(COMFY_URL)

source_image = wf.loadimage(
    image="crop_source.png"
)[0]

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
refined editorial portrait based on the cropped source image,
soft studio light, crisp details, natural skin texture
"""
)

neg = wf.cliptextencode(
    clip=clip,
    text="watermark, text, blurry, low quality, distorted face"
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
    seed=73111924500188,
    steps=24,
    cfg=6.8,
    sampler_name="euler",
    scheduler="normal",
    denoise=0.5
)

img = wf.vaedecode(
    samples=samples,
    vae=vae
)

wf.saveimage(
    images=img,
    filename_prefix="sd15_crop_then_img2img"
)

wf.run()
