import os
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[3]))

from skills.infra.match_curated_workflow.skill import run as match_workflow
from skills.workflows.txt2img.run_curated_workflow.skill import run as run_workflow


matches = match_workflow(prompt="cinematic portrait photo", top_k=1)
skill_id = matches["matches"][0]["id"]

result = run_workflow(
    skill_id=skill_id,
    prompt="cinematic portrait of a runner on a city street at sunset",
    server=os.getenv("COMFY_URL"),
    headers={"Authorization": os.getenv("COMFY_AUTH_HEADER")} if os.getenv("COMFY_AUTH_HEADER") else None,
)
print(result)
