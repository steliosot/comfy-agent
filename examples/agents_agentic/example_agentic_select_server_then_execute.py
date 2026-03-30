import os

from comfy_agent import agentic_execute, agentic_plan
from skills.infra.select_comfy_server.skill import run as select_comfy_server


prompt = os.getenv(
    "AGENTIC_PROMPT",
    "generate a minimal product photo of a coffee mug on a wooden table",
)
server_name = os.getenv("COMFY_SERVER_NAME")
require_ready = os.getenv("COMFY_REQUIRE_READY", "true").strip().lower() not in {"0", "false", "no"}

selected = select_comfy_server(server_name=server_name, require_ready=require_ready)
print("SELECTED SERVER:")
print(selected)

if selected.get("status") != "ok":
    raise SystemExit(f"Server selection failed: {selected.get('message')}")

plan = agentic_plan(
    prompt=prompt,
    server=selected.get("server"),
    headers=selected.get("headers") or None,
    api_prefix=selected.get("api_prefix"),
)

print("PLAN:")
print(plan)

if plan.get("status") == "planned":
    result = agentic_execute(
        plan_payload=plan,
        server=selected.get("server"),
        headers=selected.get("headers") or None,
        api_prefix=selected.get("api_prefix"),
    )
    print("RESULT:")
    print(result)
else:
    print("Plan not executable. Status:", plan.get("status"))
