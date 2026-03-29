---
name: curated_ep09_sdxl_txt2img_with_control_net_workflow_update
description: >
  Curated ComfyUI workflow imported from `EP09 SDXL TXT2IMG With Control Net Workflow Update.json`.
homepage: https://github.com/steliosot/comfy-agent
metadata.clawdbot.os: ["darwin", "linux"]
metadata.clawdbot.requires.bins: ["python3"]
metadata.clawdbot.requires.env: ["COMFY_URL", "COMFY_AUTH_HEADER"]
metadata.clawdbot.files: ["workflow.json", "skill.py", "skill.yaml", "scripts/*"]
metadata.clawdbot.tags: ["comfyui", "workflow", "curated", "txt2img"]
metadata.clawdbot.category: "media-generation"
metadata.clawdbot.input_type: "image/png"
metadata.clawdbot.output_type: "image/png"
metadata.clawdbot.output_can_feed_into: []
metadata.clawdbot.accepts_input_from: []
metadata.clawdbot.priority: 70
---

# curated_ep09_sdxl_txt2img_with_control_net_workflow_update

Curated workflow skill generated from `EP09 SDXL TXT2IMG With Control Net Workflow Update.json`.

## Capability Family

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
  - `output_images` (includes image/video entries reported by Comfy history)

## Model Requirements

- `checkpoint`: `Juggernaut_X_RunDiffusion.safetensors` -> `models/checkpoints`
- `controlnet`: `diffusion_pytorch_model_promax.safetensors` -> `models/controlnet`

## Custom Node Requirements

- None detected.

## Links Extracted From Workflow Notes

- None detected.

## Source

- Original: `comfy-data/workflows/EP09 SDXL TXT2IMG With Control Net Workflow Update.json`
