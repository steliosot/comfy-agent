import os
from concurrent.futures import ThreadPoolExecutor

from skills.generate_video_clip.skill import run


def submit(prompt):
    return run(
        prompt=prompt,
        server=os.getenv("COMFY_URL"),
        headers={"Authorization": os.getenv("COMFY_AUTH_HEADER")} if os.getenv("COMFY_AUTH_HEADER") else None,
        filename_prefix="video_clip_agent_parallel",
    )


prompts = [
    "A cinematic product video clip of a beverage bottle on a kitchen counter.",
    "A cinematic product video clip of running shoes in an urban street.",
]

with ThreadPoolExecutor(max_workers=2) as pool:
    results = list(pool.map(submit, prompts))

print(results)
