import os

from skills.workflows.video_t2v_i2v_avatar.generate_video_clip.skill import build


wf = build(
    server=os.getenv("COMFY_URL"),
    headers={"Authorization": os.getenv("COMFY_AUTH_HEADER")} if os.getenv("COMFY_AUTH_HEADER") else None,
    filename_prefix="video_clip_h264_skill_buildable",
)

wf.inspect()
result = wf.run()
print(result)
print(wf.saved_images(result.get("prompt_id")))
