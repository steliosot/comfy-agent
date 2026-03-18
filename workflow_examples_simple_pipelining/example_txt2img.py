import sys

from comfy_agent import Workflow

wf = Workflow()

(
    wf
    .checkpoint("sd1.5/juggernaut_reborn.safetensors")
    .prompt(
        """photo of a rusty robot, 3D render, sharp focus,
studio lighting, dramatic shadows, soft rim light,
shallow depth of field, centered composition,
realistic reflections, cinematic contrast,
ultra detailed textures, high quality 3D portrait,
dark background"""
    )
    .negative("watermark, text")
    .latent(512, 512)
    .sample(
        seed=763573443419271,
        steps=35,
        cfg=7.0,
        sampler_name="euler",
        scheduler="normal",
        denoise=1.0,
    )
    .decode()
    .save("robot_simple")
)

wf.run()
