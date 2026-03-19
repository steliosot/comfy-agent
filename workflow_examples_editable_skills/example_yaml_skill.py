import os

from comfy_agent import load_yaml_skill

auth_header = os.getenv("COMFY_AUTH_HEADER")
headers = {"Authorization": auth_header} if auth_header else None

wf = load_yaml_skill(
    "workflow_examples_editable_skills/generate_sd15_image.yaml",
    server=os.getenv("COMFY_URL"),
    headers=headers,
    prompt="cinematic robot",
    negative_prompt="watermark, text",
)

wf.inspect()
wf.run()
