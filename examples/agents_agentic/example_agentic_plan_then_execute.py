import os

from comfy_agent import agentic_execute, agentic_plan

prompt = "generate a bottle of Coca-Cola and then crop it to wide screen 1280x720"

plan = agentic_plan(
    prompt=prompt,
    server=os.getenv("COMFY_URL"),
    headers={"Authorization": os.getenv("COMFY_AUTH_HEADER")} if os.getenv("COMFY_AUTH_HEADER") else None,
)

print("PLAN:")
print(plan)

if plan.get("status") == "planned":
    result = agentic_execute(
        plan_payload=plan,
        server=os.getenv("COMFY_URL"),
        headers={"Authorization": os.getenv("COMFY_AUTH_HEADER")} if os.getenv("COMFY_AUTH_HEADER") else None,
    )
    print("RESULT:")
    print(result)
