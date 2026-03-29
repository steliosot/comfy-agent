from comfy_agent import agentic_execute


def run(
    plan_payload,
    server=None,
    headers=None,
    api_prefix=None,
    run_id=None,
    context=None,
):
    return agentic_execute(
        plan_payload=plan_payload,
        server=server,
        headers=headers,
        api_prefix=api_prefix,
        run_id=run_id,
        context=context,
    )
