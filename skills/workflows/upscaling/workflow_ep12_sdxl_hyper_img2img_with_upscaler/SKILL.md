---
name: workflow_ep12_sdxl_hyper_img2img_with_upscaler
description: >
  Workflow wrapper imported from `Ep12 SDXL Hyper IMG2IMG with Upscaler.json`.
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

# workflow_ep12_sdxl_hyper_img2img_with_upscaler

Imported workflow skill generated from `Ep12 SDXL Hyper IMG2IMG with Upscaler.json`.

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

- `upscale_model`: `4x_NMKD-Siax_200k.pth` -> `models/upscale_models`
- `checkpoint`: `Juggernaut_X_RunDiffusion_Hyper.safetensors` -> `models/checkpoints`

## Custom Node Requirements

- None detected.

## Links

- https://civitai.com/models/133005?modelVersionId=471120

<!-- AUTO-METADATA-START -->
## Routing Metadata

- Family: `upscaling`
- Input modalities: `image, text_prompt`
- Output modalities: `image/png`
- Model families: `other`
- Node count: `27`
- Complexity score: `0`
- Resource profile: `low`
- Estimated runtime: `fast (usually under 30s on modern GPU)`
- Max latent resolution hint: `None`x`None`
- Max sampler steps hint: `4`

## Detected Models

- `upscale_model`: `4x_NMKD-Siax_200k.pth` -> `models/upscale_models`
- `checkpoint`: `Juggernaut_X_RunDiffusion_Hyper.safetensors` -> `models/checkpoints`

## Detected Custom Nodes

- None detected.

## Runtime Warnings

- No major runtime warnings detected.
<!-- AUTO-METADATA-END -->

