import sys

from comfy_agent import Workflow

wf = Workflow()

(
    wf
    .load_image("rosie.jpg")
    .crop(100, 100, 256, 256)
    .save("robot_crop_simple")
)

wf.run()
