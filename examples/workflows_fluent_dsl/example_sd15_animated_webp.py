import sys

from comfy_agent import Workflow

wf = Workflow()

(
    wf
    .checkpoint("sd1.5/juggernaut_reborn.safetensors")
    .prompt(
        """
stylized robot walking through neon rain, cinematic lighting,
dynamic pose, reflective street, detailed concept art
"""
    )
    .negative("watermark, text, blurry, low quality, extra limbs")
    .latent(512, 512, batch_size=8)
    .sample(
        seed=20260317,
        steps=20,
        cfg=7.0,
        sampler_name="euler",
        scheduler="normal",
        denoise=1.0,
    )
    .decode()
    .save_animated_webp("sd15_anim_test_simple", fps=6, quality=80, method="default")
)

wf.run(debug=True)
