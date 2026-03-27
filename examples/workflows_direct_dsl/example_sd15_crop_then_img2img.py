from skills.generate_sd15_crop_then_img2img.skill import run

result = run(
    image="woman.png",
    prompt="editorial portrait from cropped reference",
    x=64,
    y=64,
    width=512,
    height=512,
)
print(result)
