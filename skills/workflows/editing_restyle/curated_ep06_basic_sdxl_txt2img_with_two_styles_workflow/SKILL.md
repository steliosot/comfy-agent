---
name: curated_ep06_basic_sdxl_txt2img_with_two_styles_workflow
description: >
  Curated ComfyUI workflow imported from `EP06 Basic SDXL TXT2IMG with TWO STYLES Workflow.json`.
homepage: https://github.com/steliosot/comfy-agent
metadata.clawdbot.os: ["darwin", "linux"]
metadata.clawdbot.requires.bins: ["python3"]
metadata.clawdbot.requires.env: ["COMFY_URL", "COMFY_AUTH_HEADER"]
metadata.clawdbot.files: ["workflow.json", "skill.py", "skill.yaml", "scripts/*"]
metadata.clawdbot.tags: ["comfyui", "workflow", "curated", "editing_restyle"]
metadata.clawdbot.category: "media-editing"
metadata.clawdbot.input_type: "text"
metadata.clawdbot.output_type: "image/png"
metadata.clawdbot.output_can_feed_into: []
metadata.clawdbot.accepts_input_from: []
metadata.clawdbot.priority: 70
---

# curated_ep06_basic_sdxl_txt2img_with_two_styles_workflow

Curated workflow skill generated from `EP06 Basic SDXL TXT2IMG with TWO STYLES Workflow.json`.

## Capability Family

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
  - `output_images` (includes image/video entries reported by Comfy history)

## Model Requirements

- `checkpoint`: `Juggernaut_X_RunDiffusion.safetensors` -> `models/checkpoints`

## Custom Node Requirements

- None detected.

## Links Extracted From Workflow Notes

- None detected.

## Source

- Original: `comfy-data/workflows/EP06 Basic SDXL TXT2IMG with TWO STYLES Workflow.json`

<!-- AUTO-METADATA-START -->
## Routing Metadata

- Family: `editing_restyle`
- Input modalities: `text_prompt`
- Output modalities: `image/png`
- Model families: `other`
- Node count: `18`
- Complexity score: `2`
- Resource profile: `low`
- Estimated runtime: `fast (usually under 30s on modern GPU)`
- Max latent resolution hint: `1024`x`1024`
- Max sampler steps hint: `30`

## Detected Models

- `checkpoint`: `Juggernaut_X_RunDiffusion.safetensors` -> `models/checkpoints`

## Detected Custom Nodes

- None detected.

## Runtime Warnings

- Medium-high resolution detected; expect moderate extra runtime.
<!-- AUTO-METADATA-END -->

