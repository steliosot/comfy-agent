from skills.workflows.txt2img.generate_sd15_image.skill import build


wf = build(
    prompt="cinematic photo of a rusty robot",
    negative_prompt="watermark, text",
    width=512,
    height=512,
    steps=35,
)

wf.run()
