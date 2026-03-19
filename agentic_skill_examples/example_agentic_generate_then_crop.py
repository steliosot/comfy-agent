import os

from comfy_agent import run_agentic


result = run_agentic(
    prompt="generate a bottle of Coca-Cola and then crop it to wide screen 1280x720",
    server=os.getenv("COMFY_URL"),
    headers={"Authorization": os.getenv("COMFY_AUTH_HEADER")} if os.getenv("COMFY_AUTH_HEADER") else None,
)

print(result)
