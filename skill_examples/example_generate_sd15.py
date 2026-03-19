import os

from skills.generate_sd15_image.skill import run

run(
    prompt="cinematic photo of a rusty robot",
    server=os.getenv("COMFY_URL"),
    headers={"Authorization": os.getenv("COMFY_AUTH_HEADER")} if os.getenv("COMFY_AUTH_HEADER") else None,
)
