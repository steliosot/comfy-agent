import os

from comfy_agent import Workflow

wf = Workflow(
    os.getenv("COMFY_URL"),
    headers={"Authorization": os.getenv("COMFY_AUTH_HEADER")} if os.getenv("COMFY_AUTH_HEADER") else None,
)

model = wf.unetloader(
    unet_name="wan2.1/wan2.1_t2v_1.3B_fp16.safetensors",
    weight_dtype="default",
)[0]
clip = wf.cliploader(
    clip_name="umt5_xxl_fp8_e4m3fn_scaled.safetensors",
    type="wan",
    device="default",
)[0]
vae = wf.vaeloader(vae_name="wan_2.1_vae.safetensors")[0]

pos = wf.cliptextencode(
    clip=clip,
    text="A cute 3D-rendered cartoon cat curiously looks at the camera with big, sparkling eyes.",
)[0]
neg = wf.cliptextencode(
    clip=clip,
    text="low quality, blurry, artifacts",
)[0]

latent = wf.emptylatentimage(width=832, height=480, batch_size=1)[0]
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
    frame_rate=16,
    loop_count=0,
    filename_prefix="wan21_editable",
    format="image/gif",
    pingpong=False,
    save_output=True,
)

clone = wf.clone().override(
    {
        "ksampler.steps": 12,
        "vhs_videocombine.frame_rate": 20,
        "vhs_videocombine.filename_prefix": "wan21_editable_override",
    }
)

print("Original:")
wf.inspect()
print("\nOverridden:")
clone.inspect()

clone.run(debug=True)
