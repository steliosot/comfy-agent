from skills.generate_video_clip.skill import run

result = run(
    prompt="cinematic product video clip, smooth camera motion, high detail",
    negative_prompt="Overexposure, static, blurred details, low quality",
)
print(result)
