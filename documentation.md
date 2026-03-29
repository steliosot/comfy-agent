# Comfy Agent Documentation

Comfy Agent is a Python toolkit for building ComfyUI workflows in code.

It gives you a few layers to work with:

- direct workflow construction
- fluent pipeline construction
- reusable skills
- editable skills that return workflows
- simple agent execution on top of skills

This guide starts from zero and builds up step by step.

## Installation

Install directly from GitHub:

```bash
pip install git+https://github.com/steliosot/comfy-agent.git
```

To update an existing installation to the latest commit:

```bash
pip install -U --force-reinstall --no-cache-dir git+https://github.com/steliosot/comfy-agent.git
```

Or install a specific branch/tag:

```bash
pip install git+https://github.com/steliosot/comfy-agent.git@main
```

Quick install check:

```bash
python3 -c "from comfy_agent import Workflow; print('comfy-agent ok')"
```

For local development inside the repository:

```bash
pip install -e .
```

If you want YAML skill loading, make sure `PyYAML` is installed:

```bash
pip install PyYAML
```

## Before You Start

You need:

- Python 3.10 or newer
- a running ComfyUI server
- the required models inside your ComfyUI `models/` folders

By default, `Workflow()` uses:

```text
http://127.0.0.1:8000
```

You can also override that with the `COMFY_URL` environment variable.

Example:

```bash
export COMFY_URL=http://127.0.0.1:8000
```

You can also use `localhost:8000` without the scheme.
Comfy Agent normalizes it to `http://localhost:8000`.

For remote servers behind Nginx, you can pass auth headers:

```python
from comfy_agent import Workflow

wf = Workflow(
    "http://YOUR_SERVER_IP",
    headers={
        "Authorization": "XXXXXX"
    }
)
```

`Workflow(...)` keeps local behavior unchanged and auto-detects `/api` when needed.

For localhost without auth:

```bash
export COMFY_URL=localhost:8000
unset COMFY_AUTH_HEADER
```

Optional env keys for dependency auto-repair:

```bash
export HF_TOKEN=
export CIVITAI_API_KEY=
export COMFY_MANAGER_API_PREFIX=/manager
export COMFY_RESOURCE_MIN_FREE_VRAM_MB=
export COMFY_RESOURCE_MIN_FREE_STORAGE_GB=
```

Provider token usage:

- `HF_TOKEN` is used by `download_model` when `source="huggingface"`.
- `CIVITAI_API_KEY` is used by `download_model` when `source="civitai"`.
- You can still pass `token=...` directly per call to override env values.

## Your First Workflow

Start with the direct workflow API. This is the lowest-level and most explicit way to build a ComfyUI graph.

```python
from comfy_agent import Workflow

wf = Workflow()

model, clip, vae = wf.checkpointloadersimple(
    ckpt_name="sd1.5/juggernaut_reborn.safetensors"
)

pos = wf.cliptextencode(
    clip=clip,
    text="cinematic photo of a rusty robot"
)

neg = wf.cliptextencode(
    clip=clip,
    text="watermark, text"
)

latent = wf.emptylatentimage(
    width=512,
    height=512,
    batch_size=1
)

samples = wf.ksampler(
    model=model,
    positive=pos,
    negative=neg,
    latent_image=latent,
    steps=20,
    cfg=7.0,
    sampler_name="euler",
    scheduler="normal",
    denoise=1.0
)

img = wf.vaedecode(
    samples=samples,
    vae=vae
)

wf.saveimage(
    images=img,
    filename_prefix="robot"
)

wf.run()
```

What happens here:

1. A checkpoint is loaded.
2. Positive and negative prompts are encoded.
3. A latent image is created.
4. Sampling is performed.
5. The latent is decoded into an image.
6. The image is saved in the ComfyUI output folder.

## A Simpler Workflow Style

If you prefer a cleaner, chain-based style, use the fluent API.

```python
from comfy_agent import Workflow

wf = Workflow()

(
    wf
    .checkpoint("sd1.5/juggernaut_reborn.safetensors")
    .prompt("cinematic photo of a rusty robot")
    .negative("watermark, text")
    .latent(512, 512)
    .sample(steps=20, cfg=7.0)
    .decode()
    .save("robot")
)

wf.run()
```

This style is useful when you want to describe the workflow as a sequence of steps rather than as individual nodes.

## Inspecting a Workflow

You can inspect the structure of a workflow before running it.

```python
from comfy_agent import Workflow

wf = Workflow()

(
    wf
    .checkpoint("sd1.5/juggernaut_reborn.safetensors")
    .prompt("robot")
    .negative("bad quality")
    .latent(512, 512)
    .sample()
    .decode()
    .save("robot")
)

wf.inspect()
```

You can also export the internal DAG as JSON:

```python
print(wf.to_json())
```

This is useful for debugging, teaching, or understanding how the workflow is composed.

## Your First Skill

A skill wraps a workflow into a reusable interface.

A simple skill looks like this:

```python
from comfy_agent import Workflow


def build(prompt,
          negative_prompt="watermark, text",
          width=512,
          height=512,
          steps=35):
    wf = Workflow()

    model, clip, vae = wf.checkpointloadersimple(
        ckpt_name="sd1.5/juggernaut_reborn.safetensors"
    )

    pos = wf.cliptextencode(clip=clip, text=prompt)
    neg = wf.cliptextencode(clip=clip, text=negative_prompt)

    latent = wf.emptylatentimage(
        width=width,
        height=height,
        batch_size=1
    )

    samples = wf.ksampler(
        model=model,
        positive=pos,
        negative=neg,
        latent_image=latent,
        steps=steps,
        cfg=7.0,
        sampler_name="euler",
        scheduler="normal",
        denoise=1.0
    )

    img = wf.vaedecode(samples=samples, vae=vae)
    wf.saveimage(images=img, filename_prefix="generated")

    return wf


def run(**kwargs):
    wf = build(**kwargs)
    wf.run()
    return wf
```

This pattern is useful because:

- `build(...)` returns the workflow without executing it
- `run(...)` is a convenient wrapper for immediate execution

## Using a Skill

Once you have a skill with a `build(...)` function:

```python
from skills.workflows.txt2img.generate_sd15_image.skill import build

wf = build(prompt="cinematic robot")
wf.run()
```

If you want the shortcut:

```python
from skills.workflows.txt2img.generate_sd15_image.skill import run

run(prompt="cinematic robot")
```

## Curated Workflow Skills

This repo now supports a curated migration path from raw ComfyUI-exported workflows into OpenClaw-ready skill packages.

Build curated skills from `comfy-data/workflows`:

```bash
python3 tools/build_curated_workflow_skills.py --limit 120
python3 tools/validate_curated_workflow_skills.py
```

Generated output lives in:

- `skills/workflows/<capability>/<skill_name>/`

Each folder contains:

- `workflow.json`
- `SKILL.md`
- `skill.yaml`
- `skill.py`
- `scripts/run.py`

### Match and Run the Best Curated Workflow

```python
from skills.infra.match_curated_workflow.skill import run as match_workflow
from skills.workflows.txt2img.run_curated_workflow.skill import run as run_workflow

prompt = "cinematic product video of sneakers with smooth camera motion"

matches = match_workflow(prompt=prompt, top_k=3)
print(matches)

best_id = matches["matches"][0]["id"]
result = run_workflow(skill_id=best_id, prompt=prompt)
print(result)
```

### Extract Correct Download Links From Workflow Notes

```python
from skills.infra.get_workflow_download_links.skill import run

links = run(skill_id="curated_ltx_0_95_text2video")
print(links)
```

This reads URLs directly from note/content nodes inside `workflow.json` and groups them by provider:

- `huggingface`
- `civitai`
- `github`
- `comfy_docs`
- `community`

### Predict Whether a Job Is Likely to Succeed

```python
from skills.infra.predict_job_success_likelihood.skill import run

result = run(skill_id="curated_ltx_0_95_text2video")
print(result["likelihood"], result["confidence"], result["recommendation"])
```

Prediction uses:

- installed dependencies (required nodes/models vs current server)
- similar historical runs from `/history`
- current queue and resource pressure

### Skills Organization

To keep the repository easier to navigate:

- Infra/ops skills are documented in `skills/infra/README.md`
- Workflow/execution skills are documented in `skills/workflows/README.md`

## Extending a Skill Before Execution

Because a skill returns a workflow, it can be edited before it runs.

```python
from skills.workflows.txt2img.generate_sd15_image.skill import build

wf = build(prompt="cinematic robot")

wf.override({
    "ksampler.cfg": 12,
    "ksampler.steps": 30,
    "save.filename_prefix": "robot_override"
})

wf.inspect()
wf.run()
```

This is the key idea behind editable skills:

- skills are reusable
- skills are not black boxes
- skills can be inspected and modified by code or by agents

## Dependency Skills: Download, Folder Guide, Remove

Use `model_folder_guide` to check where each model should be installed:

```python
from skills.infra.model_folder_guide.skill import run as folder_guide

print(folder_guide(model_type="checkpoint"))      # models/checkpoints
print(folder_guide(model_type="lora"))            # models/loras
print(folder_guide(model_type="diffusion_model")) # models/diffusion_models
```

Download a model with provider-backed auth:

```python
from skills.infra.download_model.skill import run as download_model

result = download_model(
    source="civitai",
    model_id_or_url="https://civitai.com/api/download/models/12345",
    filename="example_light_lora.safetensors",
    model_type="lora",
)
print(result)
```

Remove a model if you need to roll back:

```python
from skills.infra.remove_model.skill import run as remove_model

result = remove_model(
    filename="example_light_lora.safetensors",
    model_type="lora",
)
print(result)
```

## Cloning a Skill Workflow

If you want to branch a workflow safely, clone it first.

```python
from skills.workflows.txt2img.generate_sd15_image.skill import build

wf = build(prompt="robot portrait")

wf_fast = wf.clone().override({
    "ksampler.steps": 12,
    "save.filename_prefix": "robot_fast"
})

wf_quality = wf.clone().override({
    "ksampler.steps": 40,
    "ksampler.cfg": 9,
    "save.filename_prefix": "robot_quality"
})

wf_fast.run()
wf_quality.run()
```

This is useful for experimentation, A/B testing, and agents that want to try multiple variations.

## Building Skills with YAML

You can also describe a skill as a simple YAML graph and load it dynamically.

Example YAML:

```yaml
graph:
  - node: checkpoint
    params:
      ckpt_name: sd1.5/juggernaut_reborn.safetensors

  - node: prompt
    input: prompt

  - node: negative
    input: negative_prompt

  - node: latent
    params:
      width: 512
      height: 512
      batch_size: 1

  - node: sample
    params:
      steps: 35
      cfg: 7.0
      sampler_name: euler
      scheduler: normal
      denoise: 1.0

  - node: decode

  - node: save
    params:
      filename_prefix: generated_yaml
```

Load it like this:

```python
from comfy_agent import load_yaml_skill

headers = {
    "Authorization": "XXXXXX"
}

wf = load_yaml_skill(
    "examples/workflows_editable/generate_sd15_image.yaml",
    server="http://YOUR_SERVER_IP",
    headers=headers,
    prompt="cinematic robot",
    negative_prompt="watermark, text"
)

wf.inspect()
wf.run()
```

This gives you a declarative way to define reusable workflow templates.

## Image-to-Image Skills

Skills can also work with input images.

Example:

```python
from skills.workflows.img2img_inpaint_outpaint.generate_sd15_img2img_remix.skill import build

wf = build(
    image="remix_source.png",
    prompt="cinematic sci-fi repaint",
    denoise=0.55
)

wf.run()
```

For these workflows, the image file must exist in the ComfyUI input folder.

## Animation and Video Skills

You can also create simple animated outputs by generating image batches and exporting them with `SaveAnimatedWEBP`.

Example:

```python
from skills.workflows.txt2img.generate_sd15_stelios_shoe_ad.skill import build

wf = build(
    prompt="cinematic advertisement for Stelios shoes",
    batch_size=60,
    fps=6
)

wf.run()
```

This is useful for compatibility testing and lightweight animation pipelines.

For true video clip generation with WAN 2.1, use the generic video skill:

```python
from skills.workflows.video_t2v_i2v_avatar.generate_video_clip.skill import run

result = run(
    prompt="cinematic product video clip of a bottle on a kitchen counter",
    server="http://34.30.216.121",
    headers={"Authorization": "XXXXXX"},
    filename_prefix="video_clip_h264",
)

print(result)
```

This exports via `VHS_VideoCombine` using `video/h264-mp4`.

## Using Skills in an Agent

You can wrap skills inside agent-style job execution.

Example:

```python
from comfy_agent.job import Job, Executor
from skills.workflows.txt2img.generate_sd15_image.skill import run as generate_image

jobs = [
    Job(generate_image, prompt="greek island"),
    Job(generate_image, prompt="greek island cinematic lighting"),
    Job(generate_image, prompt="greek island sunset"),
]

executor = Executor()
results = executor.run_parallel(jobs)
print(results)
```

This pattern is a good fit when:

- an agent wants to generate multiple variants
- different skills should be run concurrently
- workflows are part of a bigger orchestration layer

## Agent-Ready Editable Skill Pattern

The most important pattern in this project is:

```python
from skills.workflows.txt2img.generate_sd15_image.skill import build

wf = build(prompt="robot")

wf.override({
    "ksampler.cfg": 10,
    "ksampler.steps": 24
})

wf.run()
```

That lets an agent:

1. pick a skill
2. build the underlying workflow
3. inspect or override key parameters
4. run the final graph

This makes skills reusable, inspectable, and composable.

## Agentic Skill Routing

The project also includes an agnostic agentic layer that reasons about prompt intent,
selects skills with confidence scores, and executes the plan.

You can use it in one-shot mode (`run_agentic`) or explicit two-step mode
(`agentic_plan` then `agentic_execute`).

Example (single image skill):

```python
from comfy_agent import run_agentic

result = run_agentic(
    prompt="cinematic product photo of a bottle of Coca-Cola",
    server="http://34.30.216.121",
    headers={"Authorization": "XXXXXX"},
)

print(result)
```

Example (single video skill):

```python
from comfy_agent import run_agentic

result = run_agentic(
    prompt="cinematic product video clip of a bottle on a kitchen counter",
    server="http://34.30.216.121",
    headers={"Authorization": "XXXXXX"},
)

print(result)
```

Example (auto dependency preflight + remediation):

```python
from comfy_agent import run_agentic

result = run_agentic(
    prompt="cinematic product video clip of a bottle on a kitchen counter",
    auto_prepare=True,
    dependency_requirements={
        "models": [
            {
                "name": "wan2.1/wan2.1_t2v_1.3B_fp16.safetensors",
                "model_type": "unet",
                "source": "huggingface",
                "model_id_or_url": "Wan-AI/Wan2.1-T2V-1.3B",
                "filename": "wan2.1/wan2.1_t2v_1.3B_fp16.safetensors",
            }
        ],
        "custom_nodes": [
            {
                "repo_url": "https://github.com/Kosinkadink/ComfyUI-VideoHelperSuite",
                "expected_node_classes": ["VHS_VideoCombine"],
            }
        ],
    },
)

print(result)
```

Example (combined skills: generate image then crop):

```python
from comfy_agent import run_agentic

result = run_agentic(
    prompt="generate a bottle of Coca-Cola and then crop it to wide screen 1280x720",
    server="http://34.30.216.121",
    headers={"Authorization": "XXXXXX"},
)

print(result)
```

Example (two-step plan then execute):

```python
from comfy_agent import agentic_plan, agentic_execute

plan = agentic_plan(
    prompt="generate a bottle of Coca-Cola and then crop it to wide screen 1280x720",
    auto_prepare=True,
)
print(plan)

result = agentic_execute(
    plan_payload=plan,
    server="http://34.30.216.121",
    headers={"Authorization": "XXXXXX"},
)
print(result)
```

Example (slash indicators helper):

```python
from comfy_agent import agentic_command

plan = agentic_command("/plan cinematic product photo of a bottle of Coca-Cola")
result = agentic_command("/execute", plan_payload=plan)
print(result)
```

If your prompt asks for video and crop together, current behavior is:

- route to `generate_video_clip`
- include a note that crop is image-only in `run_agentic` for now

Try the ready-made examples in:

- `examples/agents_agentic/`

## Ops Skills for Dependency Management

The project now includes dependency and resource ops skills:

- `assess_server_resources`
- `download_model`
- `install_custom_node`
- `prepare_workflow_dependencies`

These are designed for agent workflows that need to auto-fix missing models and custom nodes.

## Testing

The repository includes unit tests for workflows, skills, agents, and examples.

Run them with:

```bash
python3 -m unittest discover -s unit_tests -v
```

These tests use mocked ComfyUI API responses, so most of them do not require a live ComfyUI server.

## Recommended Learning Path

If you are new to the project, this is a good order to follow:

1. Run a direct example from `examples/workflows_direct_dsl`
2. Run a fluent example from `examples/workflows_fluent_dsl`
3. Open a skill in `skills/` and study `build(...)`
4. Try a buildable skill example from `examples/skills_buildable`
5. Try an editable workflow example from `examples/workflows_editable`
6. Try a video clip example (`example_wan21_video_clip.py` or `example_cloud_wan21_video_clip.py`)
7. Try an agentic routing example from `examples/agents_agentic`
8. Run the unit tests
9. Build your own skill

## Where to Look Next

Useful folders in the repository:

- `examples/workflows_direct_dsl/`
- `examples/workflows_fluent_dsl/`
- `examples/workflows_editable/`
- `skills/`
- `examples/skills_basic/`
- `examples/skills_buildable/`
- `examples/agents_agentic/`
- `examples/agents_threaded/`
- `unit_tests/`

If you want to extend the system, the main place to start is:

- `comfy_agent/workflow.py`
