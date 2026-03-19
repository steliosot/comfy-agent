import sys

from comfy_agent import Workflow

wf = Workflow()

(
    wf
    .checkpoint("sd1.5/juggernaut_reborn.safetensors")
    .prompt(
        """
cinematic advertisement for luxury shoes called Stelios, stylish young man
walking confidently through a modern city street at golden hour, premium
fashion commercial, elegant close-up focus on the shoes, smooth tracking
shot, polished reflections on the pavement, luxury brand campaign, warm
sunlight, shallow depth of field, realistic, high-end commercial look,
heroic fashion photography, urban lifestyle, premium leather shoes
"""
    )
    .negative(
        """
watermark, text, blurry, low quality, bad anatomy, extra limbs,
deformed feet, distorted shoes, jittery motion, shaky camera,
logo glitches, duplicate person
"""
    )
    .latent(512, 768, batch_size=60)
    .sample(
        seed=2026031701,
        steps=20,
        cfg=7.0,
        sampler_name="euler",
        scheduler="normal",
        denoise=1.0,
    )
    .decode()
    .save_animated_webp("stelios_shoe_ad_simple", fps=6, quality=80, method="default")
)

wf.run(debug=True)
