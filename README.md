# Comfy Agent

Comfy Agent is a lightweight Python DSL for building and running ComfyUI workflows from code.

It supports:
- direct node-based workflow construction
- a fluent chaining style for simple pipelines
- reusable skills built on top of workflows

## Installation

Install directly from GitHub:

```bash
pip install git+https://github.com/steliosot/comfy-agent.git
```

For local development from this repository:

```bash
pip install -e .
```

## Requirements

- Python 3.10+
- A running ComfyUI server
- The required models placed in the correct ComfyUI `models/` directories

Before running the examples, first test the JSON workflows in [comfyUI_workflows](/Users/stelios/Documents/comfy-agent/comfyUI_workflows) inside ComfyUI. Those files include notes about:

- which models to download
- where to place them in ComfyUI

## Quick Start

Basic workflow style:

```python
from comfy_agent import Workflow

wf = Workflow("http://127.0.0.1:8000")

model, clip, vae = wf.checkpointloadersimple(
    ckpt_name="sd15/juggernaut_reborn.safetensors"
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
    .checkpoint("sd15/juggernaut_reborn.safetensors")
    .prompt("rusty robot")
    .negative("bad quality")
    .latent(512, 512)
    .sample()
    .decode()
    .save("robot")
)

wf.run()
```

`Workflow()` reads `COMFY_URL` if it is set. Otherwise it defaults to `http://127.0.0.1:8000`.

## Recommended KSampler Settings

For the bundled SD1.5 examples, these settings are the baseline used in the repo:

```text
sampler_name: euler
scheduler: normal
cfg: 20
```

Depending on your setup and model choice, you may want to tune them.

## Workflow Examples

The [workflow_examples](/Users/stelios/Documents/comfy-agent/workflow_examples) folder contains direct DSL examples.

To try one:

1. Open an example such as [example_txt2img.py](/Users/stelios/Documents/comfy-agent/workflow_examples/example_txt2img.py)
2. Confirm the ComfyUI URL is correct for your machine
3. Run it with Python

```bash
python workflow_examples/example_txt2img.py
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

The [workflow_examples_simple_pipelining](/Users/stelios/Documents/comfy-agent/workflow_examples_simple_pipelining) folder contains the same general ideas in the fluent chaining style.

Run one with:

```bash
python workflow_examples_simple_pipelining/example_txt2img.py
```

These examples are useful if you want a simpler authoring style while keeping the original lower-level API available.

## Skill Examples

The [skill_examples](/Users/stelios/Documents/comfy-agent/skill_examples) folder shows how workflows can be wrapped as reusable skills.

The [skills](/Users/stelios/Documents/comfy-agent/skills) folder contains the actual skill definitions, including:

- image generation skills
- preview skills
- img2img skills
- animated WEBP skills

## Agent Examples

The [agent_examples](/Users/stelios/Documents/comfy-agent/agent_examples) folder shows how multiple jobs can be executed using threads.

Example:

```text
example_agent_parallel.py
```

ComfyUI processes requests serially by default, so true parallel execution typically requires multiple ComfyUI instances.

## Running in Parallel

To achieve real parallel execution, run multiple ComfyUI servers and distribute jobs across them.

Example:

```text
ComfyUI worker 1 -> localhost:8188
ComfyUI worker 2 -> localhost:8189
ComfyUI worker 3 -> localhost:8190
```

An orchestrator can then distribute jobs across those workers.
