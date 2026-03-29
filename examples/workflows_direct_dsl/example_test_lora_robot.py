from skills.workflows.txt2img.generate_sd15_lora.skill import run

result = run(
    prompt="portrait of a stylish robot, cinematic lighting",
    lora="sd15/CakeStyle.safetensors",
    strength=0.8,
)
print(result)
