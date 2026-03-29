# OpenClaw Prompt Recipes

This guide gives practical prompt examples for the two-step agentic flow:

1. plan first
2. execute second

Use this when you want safer execution, better predictability, and clearer skill selection.

## Quick Pattern

```python
from comfy_agent import agentic_plan, agentic_execute

prompt = "your prompt here"

plan = agentic_plan(prompt=prompt, auto_prepare=True)
print(plan)

result = agentic_execute(plan_payload=plan)
print(result)
```

Slash-command helper:

```python
from comfy_agent import agentic_command

plan = agentic_command("/plan your prompt here")
result = agentic_command("/execute", plan_payload=plan)
```

## 1) Basic Text-to-Image

**Prompt**
`cinematic portrait of a rusty robot, realistic lighting`

**Plan**
- Expected core skills: `prepare_workflow_dependencies`, `generate_sd15_image`

**Execute**
- Run the returned plan payload as-is.

## 2) Product Photo

**Prompt**
`studio product photo of a white sneaker on a neutral background`

**Plan**
- Expected core skills: `prepare_workflow_dependencies`, `generate_sd15_image`

**Execute**
- Use default execute flow.

## 3) Generate Then Crop (Widescreen)

**Prompt**
`generate a bottle of Coca-Cola and then crop it to 1280x720`

**Plan**
- Expected core skills: `prepare_workflow_dependencies`, `generate_sd15_image`, `crop_image`
- Crop parameters should appear in plan params.

**Execute**
- Execute the exact plan payload.

## 4) Generate Then Crop (Custom Region)

**Prompt**
`generate a fashion portrait then crop x=120 y=40 to 1024x1024`

**Plan**
- Expected core skills: `prepare_workflow_dependencies`, `generate_sd15_image`, `crop_image`

**Execute**
- Execute with the extracted crop coordinates from plan payload.

## 5) Video Clip Generation

**Prompt**
`cinematic video clip of a person walking on a rainy city street`

**Plan**
- Expected core skills: `prepare_workflow_dependencies`, `generate_video_clip`
- Plan warnings may note video runtime/VRAM requirements.

**Execute**
- Execute the plan payload; result should include video artifacts metadata.

## 6) Video + Crop Request (Behavior Check)

**Prompt**
`generate a video of a Greek island and then crop to widescreen`

**Plan**
- Expected core skills: `prepare_workflow_dependencies`, `generate_video_clip`
- Likely warning: crop is image-only in current agentic execution.

**Execute**
- Execute to confirm current fallback behavior and warning propagation.

## 7) Fast/Lightweight Image Request

**Prompt**
`quick low-vram concept image of a futuristic shoe design`

**Plan**
- Use `agentic_plan` to inspect selected route and warnings.
- If using curated routing elsewhere, prefer lower `resource_profile` entries.

**Execute**
- Execute only if plan preflight is ready.

## 8) Curated Workflow Match -> Run

**Prompt**
`high quality product image with clean branding area for ad copy`

**Plan Phase (Catalog)**
- Use curated matcher first:

```python
from skills.infra.match_curated_workflow.skill import run as match_workflow

candidates = match_workflow(prompt="high quality product image with clean branding area for ad copy", top_k=3)
print(candidates)
```

**Execute Phase**
- Run selected curated skill:

```python
from skills.workflows.txt2img.run_curated_workflow.skill import run as run_curated

result = run_curated(skill_id=candidates["items"][0]["skill_id"], prompt="high quality product image with clean branding area for ad copy")
print(result)
```

## 9) Generate -> Upscale (Curated Upscale Workflow)

**Prompt**
`generate a premium sneaker product image and upscale for poster print`

**Plan**
- Phase A: `agentic_plan` for generation
- Phase B: choose an `upscaling` curated workflow from catalog

**Execute**
- Run generation plan first, then execute selected upscaling workflow on resulting asset.

## 10) Upload -> Crop -> Download (Asset Pipeline)

**Prompt**
`crop my uploaded portrait to clean 1:1 social media framing`

**Plan**
- Asset skills + workflow skill chain:
  - `upload_image`
  - `crop_image`
  - `download_image`

**Execute**
- Use upload metadata as input to crop, then download final output.

## 11) Dependency Recovery Before Execution

**Prompt**
`generate a WAN video trailer shot with cinematic lighting`

**Plan**
- `agentic_plan(..., auto_prepare=True)` should include preflight summary.
- If dependencies are missing, resolve via:
  - `download_model`
  - `install_custom_node`
  - `prepare_workflow_dependencies`

**Execute**
- Re-run plan after dependencies are ready, then execute.

## 12) Slash-Driven Operator Flow

**Prompt**
`/plan generate a bottle of Coca-Cola and then crop it to 1280x720`

**Plan**
- Run via slash command helper and inspect payload.

**Execute**
`/execute` with the exact returned plan payload.

```python
from comfy_agent import agentic_command

plan = agentic_command("/plan generate a bottle of Coca-Cola and then crop it to 1280x720")
result = agentic_command("/execute", plan_payload=plan)
print(result)
```

## Notes

- Prefer `agentic_plan` + `agentic_execute` when running on cloud/remote servers.
- Keep plan payload immutable between plan and execute for deterministic behavior.
- For long/heavy jobs, check warnings and preflight before execution.
- For large libraries, use curated matching first, then execute the selected workflow.
