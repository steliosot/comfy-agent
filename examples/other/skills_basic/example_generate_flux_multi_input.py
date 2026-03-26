import os

from skills.generate_flux_multi_input_img2img.skill import run


image1 = os.getenv("COMFY_REF_IMAGE1", "/Users/stelios/Downloads/St-Pauls-Cathedral.png")
image2 = os.getenv("COMFY_REF_IMAGE2", "/Users/stelios/Documents/ComfyUI/input/mary.JPG")
image3 = os.getenv("COMFY_REF_IMAGE3")

images = [image1, image2]
if image3:
    images.append(image3)

result = run(
    prompt=os.getenv(
        "COMFY_MULTI_PROMPT",
        "Ultra realistic portrait selfie scene in London near St Paul's Cathedral.",
    ),
    images=images,
    upload_inputs=True,
    download_output=True,
)

print(result)
