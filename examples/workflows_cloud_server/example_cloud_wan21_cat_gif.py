"""
Comfy Agent Workflow Test: WAN 2.1 Text-to-Video H264 MP4 (Cloud)

Setup (examples):
export COMFY_URL=http://34.30.216.121
export COMFY_AUTH_HEADER="XXXXXX"

For localhost without auth:
export COMFY_URL=localhost:8000
unset COMFY_AUTH_HEADER

Pipeline:
UNETLoader -> CLIPLoader -> CLIPTextEncode -> EmptyHunyuanLatentVideo ->
KSampler -> VAEDecode -> VHS_VideoCombine
"""

import os

from comfy_agent import Workflow


COMFY_URL = os.getenv("COMFY_URL", "http://34.30.216.121")
AUTH_HEADER = os.getenv("COMFY_AUTH_HEADER", "XXXXXX")

headers = {"Authorization": AUTH_HEADER} if AUTH_HEADER else None

wf = Workflow(COMFY_URL, headers=headers)

model = wf.unetloader(
    unet_name="wan2.1/wan2.1_t2v_1.3B_fp16.safetensors",
    weight_dtype="default",
)[0]

clip = wf.cliploader(
    clip_name="umt5_xxl_fp8_e4m3fn_scaled.safetensors",
    type="wan",
    device="default",
)[0]

vae = wf.vaeloader(
    vae_name="wan_2.1_vae.safetensors",
)[0]

pos = wf.cliptextencode(
    clip=clip,
    text="A cute 3D-rendered cartoon cat curiously looks at the camera with big, sparkling eyes. Its soft fur and tiny whiskers add to its adorable charm. The warm, cozy home setting features soft lighting and comfy furniture in the background. A smooth close-up camera movement enhances the animation's intimate and heartwarming feel.",
)

neg = wf.cliptextencode(
    clip=clip,
    text="Overexposure, static, blurred details, subtitles, paintings, pictures, still, overall gray, worst quality, low quality, JPEG compression residue, ugly, mutilated, redundant fingers, poorly painted hands, poorly painted faces, deformed, disfigured, deformed limbs, fused fingers, cluttered background, three legs, a lot of people in the background, upside down",
)

latent = wf.emptyhunyuanlatentvideo(width=848, height=480, length=25, batch_size=1)[0]

samples = wf.ksampler(
    model=model,
    positive=pos,
    negative=neg,
    latent_image=latent,
    seed=226274808933316,
    steps=10,
    cfg=8,
    sampler_name="uni_pc",
    scheduler="simple",
    denoise=1,
)[0]

images = wf.vaedecode(samples=samples, vae=vae)[0]

wf.vhs_videocombine(
    images=images,
    vae=vae,
    frame_rate=16,
    loop_count=0,
    filename_prefix="wan21_cat_h264_cloud",
    format="video/h264-mp4",
    pix_fmt="yuv420p",
    crf=19,
    save_metadata=True,
    trim_to_audio=False,
    pingpong=False,
    save_output=True,
)

wf.run(debug=True)
