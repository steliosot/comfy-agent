import os

from skills.download_image.skill import run as download_run
from skills.generate_flux_multi_input_img2img.skill import run
from skills.upload_image.skill import run as upload_run


image1 = os.getenv("COMFY_REF_IMAGE1", "/Users/stelios/Downloads/St-Pauls-Cathedral.png")
image2 = os.getenv("COMFY_REF_IMAGE2", "/Users/stelios/Documents/ComfyUI/input/mary.JPG")
image3 = os.getenv("COMFY_REF_IMAGE3")
run_id = os.getenv("COMFY_RUN_ID", "skills_basic_flux_multi")

local_images = [image1, image2]
if image3:
    local_images.append(image3)

remote_images = []
for index, local_path in enumerate(local_images, start=1):
    upload = upload_run(
        image_path=local_path,
        run_id=run_id,
        remote_name=f"{run_id}_ref{index}{os.path.splitext(local_path)[1]}",
    )
    remote_images.append(upload["input_image_remote"])

result = run(
    prompt=os.getenv(
        "COMFY_MULTI_PROMPT",
        "Ultra realistic portrait selfie scene in London near St Paul's Cathedral.",
    ),
    images=remote_images,
    run_id=run_id,
)

downloaded = download_run(prompt_id=result["prompt_id"], run_id=run_id)

print(result)
print(downloaded)
