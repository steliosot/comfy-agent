"""
Comfy Agent Workflow Test: Image Crop (Local)

Pipeline:
LoadImage -> ImageCrop -> SaveImage
"""

from comfy_agent import Workflow

COMFY_URL = "http://127.0.0.1:8000"

wf = Workflow(COMFY_URL)

img = wf.loadimage(
    image="rosie.jpg"
)[0]  # 0 -> IMAGE, 1 -> MASK

cropped = wf.imagecrop(
    image=img,
    x=100,
    y=100,
    width=256,
    height=256
)

wf.saveimage(
    images=cropped,
    filename_prefix="cloud_local_crop"
)

wf.run()

