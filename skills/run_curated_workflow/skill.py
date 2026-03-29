from pathlib import Path

from comfy_agent.curated_catalog import load_curated_manifest
from comfy_agent.curated_workflow_runtime import run_curated_workflow as _run_curated


def _resolve_workflow_path(skill_id):
    manifest = load_curated_manifest()
    entries = manifest.get("entries", [])
    for item in entries:
        if item.get("id") == skill_id:
            destination = item.get("destination")
            if destination:
                workflow_path = Path(destination) / "workflow.json"
                if workflow_path.exists():
                    return workflow_path, item
    raise ValueError(f"Unknown curated skill_id: {skill_id}")


def run(
    skill_id,
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
    workflow_path, meta = _resolve_workflow_path(skill_id)
    result = _run_curated(
        workflow_path=workflow_path,
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
    result["skill"] = "run_curated_workflow"
    result["skill_id"] = skill_id
    result["family"] = meta.get("family")
    return result
