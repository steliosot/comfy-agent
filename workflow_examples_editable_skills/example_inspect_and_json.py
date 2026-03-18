from skills.generate_sd15_cinematic_portrait.skill import build


wf = build(prompt="cinematic portrait of a neon courier")

print("Workflow structure:")
wf.inspect()

print("\nComfyUI prompt JSON:")
print(wf.to_json())
