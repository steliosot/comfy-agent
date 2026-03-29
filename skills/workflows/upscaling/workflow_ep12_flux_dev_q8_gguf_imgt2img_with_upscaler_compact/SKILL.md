---
name: workflow_ep12_flux_dev_q8_gguf_imgt2img_with_upscaler_compact
description: >
  Workflow wrapper imported from `Ep12 Flux Dev Q8 GGUF IMGT2IMG with Upscaler COMPACT.json`.
homepage: https://github.com/steliosot/comfy-agent
metadata.clawdbot.os: ["darwin", "linux"]
metadata.clawdbot.requires.bins: ["python3"]
metadata.clawdbot.requires.env: ["COMFY_URL", "COMFY_AUTH_HEADER"]
metadata.clawdbot.files: ["workflow.json", "skill.py", "skill.yaml", "scripts/*"]
metadata.clawdbot.tags: ["comfyui", "workflow", "library", "upscaling"]
metadata.clawdbot.category: "media-generation"
metadata.clawdbot.input_type: "image/png"
metadata.clawdbot.output_type: "image/png"
metadata.clawdbot.output_can_feed_into: []
metadata.clawdbot.accepts_input_from: []
metadata.clawdbot.priority: 60
---

# workflow_ep12_flux_dev_q8_gguf_imgt2img_with_upscaler_compact

Imported workflow skill generated from `Ep12 Flux Dev Q8 GGUF IMGT2IMG with Upscaler COMPACT.json`.

## Family

- `upscaling`

## Inputs

- Optional runtime overrides supported by `run(...)`:
  - `prompt`
  - `negative_prompt`
  - `width`, `height`
  - `seed`, `steps`, `cfg`
  - `sampler_name`, `scheduler`, `denoise`
  - `server`, `headers`, `api_prefix`

## Outputs

- Returns JSON with:
  - `status`
  - `prompt_id`
  - `output_images`

## Model Requirements

- None detected from loader nodes.

## Custom Node Requirements

- None detected.

## Links

- None detected.

<!-- AUTO-METADATA-START -->
## Routing Metadata

- Family: `upscaling`
- Input modalities: `image`
- Output modalities: `image/png`
- Model families: `flux`
- Node count: `12`
- Complexity score: `0`
- Resource profile: `low`
- Estimated runtime: `fast (usually under 30s on modern GPU)`
- Max latent resolution hint: `None`x`None`
- Max sampler steps hint: `None`

## Detected Models

- None detected.

## Detected Custom Nodes

- None detected.

## Runtime Warnings

- No major runtime warnings detected.
<!-- AUTO-METADATA-END -->

