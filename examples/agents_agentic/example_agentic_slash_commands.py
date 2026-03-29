import os

from comfy_agent import agentic_command

server = os.getenv("COMFY_URL")
headers = {"Authorization": os.getenv("COMFY_AUTH_HEADER")} if os.getenv("COMFY_AUTH_HEADER") else None

plan = agentic_command(
    "/plan cinematic product photo of a bottle of Coca-Cola on a kitchen counter",
    server=server,
    headers=headers,
)
print("PLAN:")
print(plan)

result = agentic_command(
    "/execute",
    plan_payload=plan,
    server=server,
    headers=headers,
)
print("RESULT:")
print(result)
