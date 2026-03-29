---
name: workflow_sdxl_vector_svg_workflow_update
description: >
  Workflow wrapper imported from `SDXL Vector SVG Workflow Update.json`.
homepage: https://github.com/steliosot/comfy-agent
metadata.clawdbot.os: ["darwin", "linux"]
metadata.clawdbot.requires.bins: ["python3"]
metadata.clawdbot.requires.env: ["COMFY_URL", "COMFY_AUTH_HEADER"]
metadata.clawdbot.files: ["workflow.json", "skill.py", "skill.yaml", "scripts/*"]
metadata.clawdbot.tags: ["comfyui", "workflow", "library", "txt2img"]
metadata.clawdbot.category: "media-generation"
metadata.clawdbot.input_type: "text"
metadata.clawdbot.output_type: "image/png"
metadata.clawdbot.output_can_feed_into: []
metadata.clawdbot.accepts_input_from: []
metadata.clawdbot.priority: 60
---

# workflow_sdxl_vector_svg_workflow_update

Imported workflow skill generated from `SDXL Vector SVG Workflow Update.json`.

## Family

- `txt2img`

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

- `checkpoint`: `juggernautXL_ragnarokBy.safetensors` -> `models/checkpoints`

## Custom Node Requirements

- `comfyui-tosvg`

## Links

- None detected.

<!-- AUTO-METADATA-START -->
## Routing Metadata

- Family: `txt2img`
- Input modalities: `text_prompt`
- Output modalities: `image/png`
- Model families: `other`
- Node count: `27`
- Complexity score: `3`
- Resource profile: `medium`
- Estimated runtime: `moderate (about 30-120s depending on server)`
- Max latent resolution hint: `1024`x`1024`
- Max sampler steps hint: `30`

## Detected Models

- `checkpoint`: `juggernautXL_ragnarokBy.safetensors` -> `models/checkpoints`

## Detected Custom Nodes

- `comfyui-tosvg`

## Runtime Warnings

- Medium-high resolution detected; expect moderate extra runtime.
- Uses custom nodes; missing nodes can cause validation/runtime failures.
<!-- AUTO-METADATA-END -->

