---
name: curated_ep29_sdxl_inpaint_replace_complex_background
description: >
  Curated ComfyUI workflow imported from `EP29 SDXL Inpaint Replace Complex Background.json`.
homepage: https://github.com/steliosot/comfy-agent
metadata.clawdbot.os: ["darwin", "linux"]
metadata.clawdbot.requires.bins: ["python3"]
metadata.clawdbot.requires.env: ["COMFY_URL", "COMFY_AUTH_HEADER"]
metadata.clawdbot.files: ["workflow.json", "skill.py", "skill.yaml", "scripts/*"]
metadata.clawdbot.tags: ["comfyui", "workflow", "curated", "img2img_inpaint_outpaint"]
metadata.clawdbot.category: "media-editing"
metadata.clawdbot.input_type: "image/png"
metadata.clawdbot.output_type: "image/png"
metadata.clawdbot.output_can_feed_into: []
metadata.clawdbot.accepts_input_from: []
metadata.clawdbot.priority: 70
---

# curated_ep29_sdxl_inpaint_replace_complex_background

Curated workflow skill generated from `EP29 SDXL Inpaint Replace Complex Background.json`.

## Capability Family

- `img2img_inpaint_outpaint`

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

- `controlnet`: `diffusion_pytorch_model_promax.safetensors` -> `models/controlnet`
- `checkpoint`: `juggernautXL_versionXInpaint.safetensors` -> `models/checkpoints`

## Custom Node Requirements

- None detected.

## Links Extracted From Workflow Notes

- None detected.

## Source

- Original: `comfy-data/workflows/EP29 SDXL Inpaint Replace Complex Background.json`
