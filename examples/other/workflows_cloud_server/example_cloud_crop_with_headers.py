"""
Comfy Agent Workflow Test: Image Crop (Cloud + Optional Headers)

Setup (examples):
export COMFY_URL=http://34.27.83.101
export COMFY_AUTH_HEADER="YOUR_AUTH_KEY"
export COMFY_INPUT_IMAGE="a124c61d-bb3f-4485-9c6b-fec142e56e6d.JPG"

For localhost without auth:
export COMFY_URL=localhost:8000
unset COMFY_AUTH_HEADER

Pipeline:
LoadImage -> ImageCrop -> SaveImage
"""

import os

from comfy_agent import Workflow

COMFY_URL = os.getenv("COMFY_URL", "http://34.27.83.101")
AUTH_HEADER = os.getenv("COMFY_AUTH_HEADER")
INPUT_IMAGE = os.getenv("COMFY_INPUT_IMAGE", "a124c61d-bb3f-4485-9c6b-fec142e56e6d.JPG")

headers = {"Authorization": AUTH_HEADER} if AUTH_HEADER else {}

wf = Workflow(
    COMFY_URL,
    headers=headers,
)

img = wf.loadimage(
    image=INPUT_IMAGE
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
    filename_prefix="cloud_auth_crop"
)

wf.run(debug=True)
