import sys

from comfy_agent import Workflow

wf = Workflow()

(
    wf
    .load_image("agentic_1773257438367_00001_.png")
    .crop(64, 64, 512, 512)
    .checkpoint("sd1.5/juggernaut_reborn.safetensors")
    .prompt(
        """
cinematic redesign of the source image, crisp details,
realistic lighting, polished textures, strong composition,
high quality concept art
"""
    )
    .negative("watermark, text, blurry, artifacts, low quality, distorted anatomy")
    .encode()
    .sample(
        seed=845102994511,
        steps=20,
        cfg=7.0,
        sampler_name="euler",
        scheduler="normal",
        denoise=0.5,
    )
    .decode()
    .preview()
    .save("sd15_compat_combo_simple")
)

wf.run(debug=True)
