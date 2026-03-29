from comfy_agent import agentic_plan


def run(
    prompt,
    server=None,
    headers=None,
    api_prefix=None,
    negative_prompt="watermark, text",
    ckpt_name="sd1.5/juggernaut_reborn.safetensors",
    auto_prepare=True,
    dependency_requirements=None,
):
    return agentic_plan(
        prompt=prompt,
        server=server,
        headers=headers,
        api_prefix=api_prefix,
        negative_prompt=negative_prompt,
        ckpt_name=ckpt_name,
        auto_prepare=auto_prepare,
        dependency_requirements=dependency_requirements,
    )
