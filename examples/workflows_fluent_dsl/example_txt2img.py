from skills.generate_sd15_image.skill import run

result = run(
    prompt="photo of a rusty robot, cinematic lighting, shallow depth of field",
    negative_prompt="watermark, text"
)
print(result)
