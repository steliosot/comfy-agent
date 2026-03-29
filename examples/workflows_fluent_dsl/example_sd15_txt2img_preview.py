from skills.workflows.txt2img.preview_sd15_image.skill import run

result = run(
    prompt="cinematic portrait of a neon courier",
    negative_prompt="watermark, text"
)
print(result)
