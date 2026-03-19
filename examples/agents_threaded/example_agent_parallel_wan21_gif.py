import os
from concurrent.futures import ThreadPoolExecutor

from skills.generate_wan21_cat_gif.skill import run


def submit(prompt):
    return run(
        prompt=prompt,
        server=os.getenv("COMFY_URL"),
        headers={"Authorization": os.getenv("COMFY_AUTH_HEADER")} if os.getenv("COMFY_AUTH_HEADER") else None,
        filename_prefix="wan21_agent_parallel",
    )


prompts = [
    "A cute 3D-rendered cartoon cat looking at the camera.",
    "A cute 3D-rendered cartoon cat blinking and tilting its head.",
]

with ThreadPoolExecutor(max_workers=2) as pool:
    results = list(pool.map(submit, prompts))

print(results)

