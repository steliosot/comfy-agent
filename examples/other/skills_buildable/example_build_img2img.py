from skills.workflows.img2img_inpaint_outpaint.generate_sd15_img2img_remix.skill import build


wf = build(
    image="remix_source.png",
    prompt="cinematic sci-fi repaint with stronger reflections",
    denoise=0.6,
)

wf.run()
