from skills.workflows.video_t2v_i2v_avatar.generate_video_clip.skill import run


prompt = "Create a cinematic product video clip and export as video/h264-mp4."

print("Reasoning:")
print("- generate_video_clip: confidence=0.97 (prompt asks for WAN T2V video/h264-mp4 export)")
print("Plan: generate_video_clip")

result = run(
    prompt=prompt,
    filename_prefix="agentic_video_clip_h264",
)

print(result)
