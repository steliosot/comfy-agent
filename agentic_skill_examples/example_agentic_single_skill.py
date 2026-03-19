import os

from comfy_agent import run_agentic


result = run_agentic(
    prompt="cinematic product photo of a bottle of Coca-Cola on a kitchen counter, realistic lighting",
    server=os.getenv("COMFY_URL"),
    headers={"Authorization": os.getenv("COMFY_AUTH_HEADER")} if os.getenv("COMFY_AUTH_HEADER") else None,
)

print(result)
