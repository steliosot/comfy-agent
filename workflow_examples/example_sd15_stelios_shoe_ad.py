"""
Comfy Agent Workflow Test: Stelios Shoe Ad

This example follows the same simple animated export approach as the
other SD1.5 workflow examples, but uses an advertising-style prompt for
the fictional shoe brand "Stelios".

This is a compatibility test for animated export, not true
motion-consistent video generation.

Pipeline
--------
CheckpointLoaderSimple -> CLIPTextEncode -> EmptyLatentImage
-> KSampler -> VAEDecode -> SaveAnimatedWEBP

Requirements
------------
ComfyUI running at:
http://127.0.0.1:8000

Required model:
models/checkpoints/sd1.5/juggernaut_reborn.safetensors
"""

import sys

from comfy_agent import Workflow

COMFY_URL = "http://127.0.0.1:8000"

wf = Workflow(COMFY_URL)

model, clip, vae = wf.checkpointloadersimple(
    ckpt_name="sd1.5/juggernaut_reborn.safetensors"
)

pos = wf.cliptextencode(
    clip=clip,
    text="""
cinematic advertisement for luxury shoes called Stelios, stylish young man
walking confidently through a modern city street at golden hour, premium
fashion commercial, elegant close-up focus on the shoes, smooth tracking
shot, polished reflections on the pavement, luxury brand campaign, warm
sunlight, shallow depth of field, realistic, high-end commercial look,
heroic fashion photography, urban lifestyle, premium leather shoes
"""
)

neg = wf.cliptextencode(
    clip=clip,
    text="""
watermark, text, blurry, low quality, bad anatomy, extra limbs,
deformed feet, distorted shoes, jittery motion, shaky camera,
logo glitches, duplicate person
"""
)

# 10 seconds at 6 fps = 60 frames
latent = wf.emptylatentimage(
    width=512,
    height=768,
    batch_size=60
)

samples = wf.ksampler(
    model=model,
    positive=pos,
    negative=neg,
    latent_image=latent,
    seed=2026031701,
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

wf.saveanimatedwebp(
    images=img,
    filename_prefix="stelios_shoe_ad",
    fps=6,
    lossless=False,
    quality=80,
    method="default"
)

wf.run(debug=True)
