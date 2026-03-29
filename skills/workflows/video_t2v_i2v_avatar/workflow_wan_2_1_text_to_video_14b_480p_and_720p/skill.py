from pathlib import Path

from comfy_agent.curated_workflow_runtime import run_curated_workflow


WORKFLOW_PATH = Path(__file__).with_name("workflow.json")


def run(
    prompt=None,
    negative_prompt=None,
    width=None,
    height=None,
    seed=None,
    steps=None,
    cfg=None,
    sampler_name=None,
    scheduler=None,
    denoise=None,
    server=None,
    headers=None,
    api_prefix=None,
):
    return run_curated_workflow(
        workflow_path=WORKFLOW_PATH,
        server=server,
        headers=headers,
        api_prefix=api_prefix,
        prompt=prompt,
        negative_prompt=negative_prompt,
        width=width,
        height=height,
        seed=seed,
        steps=steps,
        cfg=cfg,
        sampler_name=sampler_name,
        scheduler=scheduler,
        denoise=denoise,
    )
