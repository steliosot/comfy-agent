---
name: generate_sd15_landscape_batch
description: >
  Generate a batch of SD1.5 landscape images.
homepage: https://github.com/steliosot/comfy-agent
metadata.clawdbot.os: ["darwin", "linux"]
metadata.clawdbot.requires.bins: ["python3"]
metadata.clawdbot.requires.env: ["COMFY_URL", "COMFY_AUTH_HEADER"]
metadata.clawdbot.files: ["skill.py", "skill.yaml", "scripts/*"]
metadata.clawdbot.tags: ["comfyui", "skill", "image-generation"]
metadata.clawdbot.category: "media-generation"
metadata.clawdbot.input_type: "text"
metadata.clawdbot.output_type: "image/png"
metadata.clawdbot.output_can_feed_into: []
metadata.clawdbot.accepts_input_from: []
metadata.clawdbot.priority: 80
---

# generate_sd15_landscape_batch

Generate a batch of SD1.5 landscape images.

## Usage

```bash
python3 skills/workflows/generate_sd15_landscape_batch/scripts/run.py --args '{}' --pretty
```

Pass JSON kwargs for `run(...)` via `--args`:

```bash
python3 skills/workflows/generate_sd15_landscape_batch/scripts/run.py --args '{"param":"value"}' --pretty
```

## Inputs / Outputs

- Inputs follow `skills/workflows/generate_sd15_landscape_batch/skill.yaml`.
- Output is JSON printed to stdout from `run(...)`.

## Composition

This skill is designed to compose with other single-purpose skills.
Use `run_id` and artifact references when chaining.

<!-- AUTO-METADATA-START -->
## Routing Metadata

- Family: `txt2img`
- Input modalities: `text_prompt`
- Output modalities: `application/json`
- Model families: `other`
- Node count: `None`
- Complexity score: `None`
- Resource profile: `unknown`
- Estimated runtime: `depends on runtime parameters and server resources`
- Max latent resolution hint: `None`x`None`
- Max sampler steps hint: `None`

## Detected Models

- None detected.

## Detected Custom Nodes

- None detected.

## Runtime Warnings

- Hand-authored skill (no embedded workflow.json); metadata is inferred and may be approximate.
<!-- AUTO-METADATA-END -->
