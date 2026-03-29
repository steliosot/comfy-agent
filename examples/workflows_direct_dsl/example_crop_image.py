from skills.workflows.img2img_inpaint_outpaint.crop_image.skill import run

result = run(image="woman.png", x=64, y=64, width=512, height=512)
print(result)
