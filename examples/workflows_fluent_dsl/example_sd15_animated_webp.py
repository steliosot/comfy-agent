from skills.workflows.video_t2v_i2v_avatar.generate_sd15_animated_webp.skill import run

result = run(prompt="robot character turntable, smooth motion", batch_size=8, fps=8)
print(result)
