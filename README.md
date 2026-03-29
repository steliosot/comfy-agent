# Comfy Agent

Comfy Agent is a lightweight Python DSL for building and running ComfyUI workflows from code.

It supports:
- direct node-based workflow construction
- a fluent chaining style for simple pipelines
- reusable skills built on top of workflows

## OpenClaw Guide

For skill-first usage (compose, monitor, and cleanup pipelines), see:

- [openclaw-helper.md](openclaw-helper.md)

## Installation

Install directly from GitHub:

```bash
pip install git+https://github.com/steliosot/comfy-agent.git
```

Install a specific branch or tag:

```bash
pip install git+https://github.com/steliosot/comfy-agent.git@main
```

Quick install check on another machine:

```bash
python3 -c "from comfy_agent import Workflow; print('comfy-agent ok')"
```

For local development from this repository:

```bash
pip install -e .
```

Optional: install from `requirements.txt` for script usage:

```bash
pip install -r requirements.txt
```

## Requirements

- Python 3.10+
- A running ComfyUI server
- The required models placed in the correct ComfyUI `models/` directories

All runnable examples are organized under [examples/README.md](examples/README.md).

Before running the examples, first test the JSON workflows in [workflows_comfyui_json](examples/other/workflows_comfyui_json) inside ComfyUI. Those files include notes about:

- which models to download
- where to place them in ComfyUI

## Quick Start

Basic workflow style:

```python
from comfy_agent import Workflow

wf = Workflow("http://127.0.0.1:8000")

model, clip, vae = wf.checkpointloadersimple(
    ckpt_name="sd1.5/juggernaut_reborn.safetensors"
)

pos = wf.cliptextencode(clip=clip, text="rusty robot")
neg = wf.cliptextencode(clip=clip, text="watermark, text")
latent = wf.emptylatentimage(width=512, height=512, batch_size=1)

samples = wf.ksampler(
    model=model,
    positive=pos,
    negative=neg,
    latent_image=latent,
    steps=20,
    cfg=7.0,
    sampler_name="euler",
    scheduler="normal",
    denoise=1.0,
)

img = wf.vaedecode(samples=samples, vae=vae)
wf.saveimage(images=img, filename_prefix="robot")

wf.run()
```

Fluent chaining style:

```python
from comfy_agent import Workflow

wf = Workflow()

(
    wf
    .checkpoint("sd1.5/juggernaut_reborn.safetensors")
    .prompt("rusty robot")
    .negative("bad quality")
    .latent(512, 512)
    .sample()
    .decode()
    .save("robot")
)

wf.run()
```

`Workflow()` reads config from `.env` (or process env vars).

Create a local config:

```bash
cp .env.example .env
```

Example `.env` for your remote server:

```bash
COMFY_URL=http://34.27.83.101
COMFY_AUTH_HEADER=YOUR_AUTH_KEY
COMFY_INPUT_DIR=tmp/inputs
COMFY_OUTPUT_DIR=tmp/outputs
```

Example `.env` for localhost:

```bash
COMFY_URL=http://127.0.0.1:8000
COMFY_AUTH_HEADER=
COMFY_INPUT_DIR=/absolute/path/to/local/input
COMFY_OUTPUT_DIR=/absolute/path/to/local/output
```

Optional keys for dependency auto-repair skills:

```bash
HF_TOKEN=
CIVITAI_API_KEY=
COMFY_MANAGER_API_PREFIX=/manager
COMFY_RESOURCE_MIN_FREE_VRAM_MB=
COMFY_RESOURCE_MIN_FREE_STORAGE_GB=
```

Validate config and endpoints in one command:

```bash
comfy-agent-doctor
```

Or without installing the script entrypoint:

```bash
python3 -m comfy_agent.doctor
```

JSON output mode:

```bash
python3 -m comfy_agent.doctor --json
```

Cloud/Nginx style with optional auth headers:

```python
from comfy_agent import Workflow
import os

wf = Workflow(
    "http://YOUR_SERVER_IP",
    headers={
        "Authorization": os.getenv("COMFY_AUTH_HEADER", "")
    }
)
```

If your Nginx proxy exposes ComfyUI under `/api`, `Workflow(...)` now auto-detects that path.

## Dependency Auto-Repair Skills

New ops skills are available for dependency preflight and remediation:

- `assess_server_resources`
- `download_model`
- `install_custom_node`
- `prepare_workflow_dependencies`
- `model_folder_guide`
- `remove_model`
- `list_curated_workflows`
- `match_curated_workflow`
- `run_curated_workflow`
- `get_workflow_download_links`
- `predict_job_success_likelihood`

Example preflight call:

```python
from skills.infra.prepare_workflow_dependencies.skill import run

result = run(
    requirements={
        "models": [
            {
                "name": "sd1.5/juggernaut_reborn.safetensors",
                "model_type": "checkpoint",
                "source": "huggingface",
                "model_id_or_url": "runwayml/stable-diffusion-v1-5",
                "filename": "sd1.5/juggernaut_reborn.safetensors",
            }
        ],
        "custom_nodes": [
            {
                "repo_url": "https://github.com/Kosinkadink/ComfyUI-VideoHelperSuite",
                "expected_node_classes": ["VHS_VideoCombine"],
            }
        ],
    },
    auto_fix=True,
)
print(result)
```

Check where a model type should be installed:

```python
from skills.infra.model_folder_guide.skill import run

print(run(model_type="lora"))
print(run(model_type="unet"))  # maps to models/diffusion_models
```

Remove an installed model by type + filename:

```python
from skills.infra.remove_model.skill import run

print(run(filename="my_lora.safetensors", model_type="lora"))
```

Route a prompt to best curated workflows:

```python
from skills.infra.match_curated_workflow.skill import run

result = run(
    prompt="cinematic product video with smooth camera movement",
    top_k=3,
)
print(result)
```

Then execute one:

```python
from skills.workflows.txt2img.run_curated_workflow.skill import run

result = run(
    skill_id="curated_ltx_0_95_text2video",
    prompt="cinematic drone shot of a Greek island",
)
print(result)
```

Get model/dependency links directly from workflow notes:

```python
from skills.infra.get_workflow_download_links.skill import run

# by curated skill id
print(run(skill_id="curated_ltx_0_95_text2video"))

# or by any local workflow path
print(run(workflow_path="comfy-data/workflows/example.json"))
```

Predict execution likelihood before submitting:

```python
from skills.infra.predict_job_success_likelihood.skill import run

result = run(skill_id="curated_ltx_0_95_text2video")
print(result["likelihood"], result["recommendation"])
```

Skill organization is now documented in:

- `skills/README.md`
- `skills/infra/README.md`
- `skills/workflows/README.md`

Workflow capability folders:

- `skills/workflows/audio/`
- `skills/workflows/txt2img/`
- `skills/workflows/img2img_inpaint_outpaint/`
- `skills/workflows/editing_restyle/`
- `skills/workflows/video_t2v_i2v_avatar/`
- `skills/workflows/upscaling/`

Curated workflow catalog (human-readable library):

- [CURATED_WORKFLOWS.md](CURATED_WORKFLOWS.md)

Infra subcategories:

- `skills/infra/dependencies/README.md`
- `skills/infra/server_monitoring/README.md`
- `skills/infra/transfer_and_cleanup/README.md`
- `skills/infra/catalog_and_routing/README.md`

`run_agentic(...)` now supports automatic dependency preflight:

```python
from comfy_agent import run_agentic

result = run_agentic(
    prompt="cinematic product video clip of a bottle on a kitchen counter",
    auto_prepare=True,
)
print(result)
```

Two-step agentic flow is also available when you want to inspect the plan before execution:

```python
from comfy_agent import agentic_plan, agentic_execute

plan = agentic_plan(
    prompt="generate a bottle of Coca-Cola and then crop it to wide screen 1280x720",
    auto_prepare=True,
)
print(plan)

result = agentic_execute(plan_payload=plan)
print(result)
```

Slash indicator helper:

```python
from comfy_agent import agentic_command

plan = agentic_command("/plan cinematic product photo of a bottle of Coca-Cola")
result = agentic_command("/execute", plan_payload=plan)
```

## Recommended KSampler Settings

For the bundled SD1.5 examples, these settings are the baseline used in the repo:

```text
sampler_name: euler
scheduler: normal
cfg: 20
```

Depending on your setup and model choice, you may want to tune them.

## Workflow Examples

The [workflows_direct_dsl](examples/workflows_direct_dsl) folder contains direct DSL examples.

For cloud/Nginx header examples, see
[workflows_cloud_server](examples/other/workflows_cloud_server).

To try one:

1. Open an example such as [example_txt2img.py](examples/workflows_direct_dsl/example_txt2img.py)
2. Confirm the ComfyUI URL is correct for your machine
3. Run it with Python

```bash
python examples/workflows_direct_dsl/example_txt2img.py
```

Generated files are written to the ComfyUI output directory, not the repository folder.

Additional SD1.5 examples include:

- `example_sd15_cinematic_portrait.py`
- `example_sd15_landscape_batch.py`
- `example_sd15_fast_preview_character.py`
- `example_sd15_img2img_remix.py`
- `example_sd15_crop_then_img2img.py`
- `example_sd15_img2img_preview.py`
- `example_sd15_compat_combo.py`
- `example_sd15_animated_webp.py`
- `example_sd15_stelios_shoe_ad.py`

Compatibility-focused examples:

- `LoadImage` + `VAEEncode`: `example_sd15_img2img_remix.py`
- `LoadImage` + `ImageCrop` + `VAEEncode`: `example_sd15_crop_then_img2img.py`
- `LoadImage` + `VAEEncode` + `PreviewImage`: `example_sd15_img2img_preview.py`
- `LoadImage` + `ImageCrop` + `VAEEncode` + `PreviewImage` + `SaveImage`: `example_sd15_compat_combo.py`

## Simple Pipelining Examples

The [workflows_fluent_dsl](examples/workflows_fluent_dsl) folder contains the same general ideas in the fluent chaining style.

Run one with:

```bash
python examples/workflows_fluent_dsl/example_txt2img.py
```

These examples are useful if you want a simpler authoring style while keeping the original lower-level API available.

## Skill Examples

The [skills_basic](examples/other/skills_basic) folder shows how workflows can be wrapped as reusable skills.

Curated imported workflow skills are indexed in:

- `skills/workflows/curated_manifest.json`

All imported workflow wrappers are indexed in:

- `skills/workflows/all_workflows_manifest.json`

They are generated from `comfy-data/workflows` with:

```bash
python3 tools/build_curated_workflow_skills.py --limit 120
python3 tools/validate_curated_workflow_skills.py
```

The [skills](skills) folder contains the actual skill definitions, including:

- image generation skills
- preview skills
- img2img skills
- animated WEBP skills

Each skill folder now follows a consistent package structure:

- `skill.py`: implementation (`build(...)` / `run(...)`)
- `skill.yaml`: input/output schema
- `SKILL.md`: rich metadata + usage notes (Claw-style frontmatter)
- `scripts/run.py`: tiny CLI wrapper for `run(...)` with JSON kwargs

Example:

```bash
python3 skills/workflows/generate_sd15_image/scripts/run.py \
  --args '{"prompt":"cinematic robot"}' \
  --pretty
```

YAML skill loading also supports both local and cloud ComfyUI:

```python
from comfy_agent import load_yaml_skill
import os

wf = load_yaml_skill(
    "examples/other/workflows_editable/generate_sd15_image.yaml",
    server=os.getenv("COMFY_URL"),
    headers={"Authorization": os.getenv("COMFY_AUTH_HEADER", "")},
    prompt="cinematic robot",
    negative_prompt="watermark, text",
)

wf.run()
```

## Agent Examples

The [agents_threaded](examples/other/agents_threaded) folder shows how multiple jobs can be executed using threads.

Example:

```text
example_agent_parallel.py
```

ComfyUI processes requests serially by default, so true parallel execution typically requires multiple ComfyUI instances.

## Agentic Skill Examples

The [agents_agentic](examples/agents_agentic) folder shows an agnostic routing layer that:

- reasons over prompt intent
- selects one or more skills with confidence scores
- executes a single-skill or multi-skill plan

Included examples:

- `example_agentic_single_skill.py` (generate a Coke bottle image)
- `example_agentic_generate_then_crop.py` (generate then crop to `1280x720`)
- `example_agentic_plan_then_execute.py` (explicit two-step flow)
- `example_agentic_slash_commands.py` (`/plan` and `/execute` helper flow)
- `example_upload_crop_download.py` (upload local image -> run skill -> download locally)

## Running in Parallel

To achieve real parallel execution, run multiple ComfyUI servers and distribute jobs across them.

Example:

```text
ComfyUI worker 1 -> localhost:8188
ComfyUI worker 2 -> localhost:8189
ComfyUI worker 3 -> localhost:8190
```

An orchestrator can then distribute jobs across those workers.
