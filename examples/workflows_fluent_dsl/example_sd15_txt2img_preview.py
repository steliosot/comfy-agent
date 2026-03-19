import sys

from comfy_agent import Workflow

wf = Workflow()

(
    wf
    .checkpoint("sd1.5/juggernaut_reborn.safetensors")
    .prompt("a man face with a wall behind")
    .negative("low quality, blurry")
    .latent(512, 512)
    .sample(
        seed=123,
        steps=8,
        cfg=8,
        sampler_name="euler",
        scheduler="normal",
        denoise=0.7,
    )
    .decode()
    .preview()
)

wf.run()
