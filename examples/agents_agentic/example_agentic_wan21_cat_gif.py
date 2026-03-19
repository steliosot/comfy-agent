from skills.generate_wan21_cat_gif.skill import run


prompt = "Create a cute 3D-rendered cartoon cat animation and export as video/h264-mp4."

print("Reasoning:")
print("- generate_wan21_cat_gif: confidence=0.97 (prompt asks for WAN T2V video/h264-mp4 export)")
print("Plan: generate_wan21_cat_gif")

result = run(
    prompt=prompt,
    filename_prefix="wan21_agentic_cat_h264",
)

print(result)
