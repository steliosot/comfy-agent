from skills.workflows.img2img_inpaint_outpaint.generate_sd15_img2img_remix.skill import run

result = run(image="woman.png", prompt="cinematic remix with realistic lighting")
print(result)
