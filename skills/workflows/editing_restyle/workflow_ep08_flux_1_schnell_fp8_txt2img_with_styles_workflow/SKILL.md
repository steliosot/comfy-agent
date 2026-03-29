---
name: workflow_ep08_flux_1_schnell_fp8_txt2img_with_styles_workflow
description: >
  Workflow wrapper imported from `EP08 Flux 1 Schnell fp8 TXT2IMG with Styles Workflow.json`.
homepage: https://github.com/steliosot/comfy-agent
metadata.clawdbot.os: ["darwin", "linux"]
metadata.clawdbot.requires.bins: ["python3"]
metadata.clawdbot.requires.env: ["COMFY_URL", "COMFY_AUTH_HEADER"]
metadata.clawdbot.files: ["workflow.json", "skill.py", "skill.yaml", "scripts/*"]
metadata.clawdbot.tags: ["comfyui", "workflow", "library", "editing_restyle"]
metadata.clawdbot.category: "media-generation"
metadata.clawdbot.input_type: "text"
metadata.clawdbot.output_type: "image/png"
metadata.clawdbot.output_can_feed_into: []
metadata.clawdbot.accepts_input_from: []
metadata.clawdbot.priority: 60
---

# workflow_ep08_flux_1_schnell_fp8_txt2img_with_styles_workflow

Imported workflow skill generated from `EP08 Flux 1 Schnell fp8 TXT2IMG with Styles Workflow.json`.

## Family

- `editing_restyle`

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

- `checkpoint`: `flux1-schnell-fp8.safetensors` -> `models/checkpoints`

## Custom Node Requirements

- None detected.

## Links

- None detected.

<!-- AUTO-METADATA-START -->
## Routing Metadata

- Family: `editing_restyle`
- Input modalities: `text_prompt`
- Output modalities: `image/png`
- Model families: `flux, sd3`
- Node count: `10`
- Complexity score: `2`
- Resource profile: `low`
- Estimated runtime: `fast (usually under 30s on modern GPU)`
- Max latent resolution hint: `1024`x`1024`
- Max sampler steps hint: `4`

## Detected Models

- `checkpoint`: `flux1-schnell-fp8.safetensors` -> `models/checkpoints`

## Detected Custom Nodes

- None detected.

## Runtime Warnings

- Medium-high resolution detected; expect moderate extra runtime.
<!-- AUTO-METADATA-END -->

