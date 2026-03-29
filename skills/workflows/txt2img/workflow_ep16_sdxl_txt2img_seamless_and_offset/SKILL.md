---
name: workflow_ep16_sdxl_txt2img_seamless_and_offset
description: >
  Workflow wrapper imported from `Ep16 SDXL TXT2IMG Seamless and Offset.json`.
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

# workflow_ep16_sdxl_txt2img_seamless_and_offset

Imported workflow skill generated from `Ep16 SDXL TXT2IMG Seamless and Offset.json`.

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

- `checkpoint`: `Juggernaut_X_RunDiffusion.safetensors` -> `models/checkpoints`

## Custom Node Requirements

- None detected.

## Links

- None detected.

<!-- AUTO-METADATA-START -->
## Routing Metadata

- Family: `txt2img`
- Input modalities: `text_prompt`
- Output modalities: `image/png`
- Model families: `other`
- Node count: `12`
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

