from skills.generate_sd15_animated_webp.skill import run

result = run(prompt="robot animation", batch_size=8, fps=8)
print(result)
