from skills.generate_wan21_cat_gif.skill import run


prompt = "Create a cute 3D-rendered cartoon cat animation and export as GIF."

print("Reasoning:")
print("- generate_wan21_cat_gif: confidence=0.97 (prompt asks for WAN T2V GIF export)")
print("Plan: generate_wan21_cat_gif")

result = run(
    prompt=prompt,
    filename_prefix="wan21_agentic_cat",
)

print(result)
