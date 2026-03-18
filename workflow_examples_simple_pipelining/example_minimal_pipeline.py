import sys

from comfy_agent import Workflow

wf = Workflow()

(
    wf
    .checkpoint("sd1.5/juggernaut_reborn.safetensors")
    .prompt("rusty robot, cinematic lighting, detailed 3D render")
    .latent(512, 512)
    .sample(steps=20)
    .decode()
    .save("minimal_pipeline")
)

wf.run()
