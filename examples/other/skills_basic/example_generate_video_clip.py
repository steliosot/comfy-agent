import os
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[3]))

from skills.workflows.video_t2v_i2v_avatar.generate_video_clip.skill import run


result = run(
    server=os.getenv("COMFY_URL"),
    headers={"Authorization": os.getenv("COMFY_AUTH_HEADER")} if os.getenv("COMFY_AUTH_HEADER") else None,
    filename_prefix="video_clip_h264_skill_basic",
)

print(result)
