import os

from skills.generate_wan21_cat_gif.skill import run


result = run(
    server=os.getenv("COMFY_URL"),
    headers={"Authorization": os.getenv("COMFY_AUTH_HEADER")} if os.getenv("COMFY_AUTH_HEADER") else None,
    filename_prefix="wan21_cat_skill_basic",
)

print(result)

