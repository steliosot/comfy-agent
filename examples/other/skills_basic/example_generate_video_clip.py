import os

from skills.generate_video_clip.skill import run


result = run(
    server=os.getenv("COMFY_URL"),
    headers={"Authorization": os.getenv("COMFY_AUTH_HEADER")} if os.getenv("COMFY_AUTH_HEADER") else None,
    filename_prefix="video_clip_h264_skill_basic",
)

print(result)
