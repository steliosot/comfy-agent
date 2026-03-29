from skills.workflows.img2img_inpaint_outpaint.generate_sd15_compat_combo.skill import run

result = run(
    image="woman.png",
    prompt="cinematic redesign, realistic skin and lighting"
)
print(result)
