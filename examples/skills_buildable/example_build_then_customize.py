from skills.generate_sd15_cinematic_portrait.skill import build


wf = build(
    prompt="cinematic portrait of a futuristic courier in the rain",
    steps=30,
)

# Customize the built workflow before execution by adding an extra output.
final_images = wf.nodes[-1].inputs["images"]
wf.previewimage(images=final_images)
wf.saveimage(images=final_images, filename_prefix="portrait_custom_copy")

wf.run()
