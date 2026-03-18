"""
Comfy Agent Workflow Test: Image Crop (Cloud + Optional Headers)

Pipeline:
LoadImage -> ImageCrop -> SaveImage
"""

import os

from comfy_agent import Workflow

COMFY_URL = os.getenv("COMFY_URL", "http://34.30.216.121")
AUTH_HEADER = os.getenv(
    "COMFY_AUTH_HEADER",
    "XXXXXX",
)
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
