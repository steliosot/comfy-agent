---
name: curated_ep29_flux_dev_replace_simple_or_white_background
description: >
  Curated ComfyUI workflow imported from `EP29 Flux Dev Replace Simple or White Background.json`.
homepage: https://github.com/steliosot/comfy-agent
metadata.clawdbot.os: ["darwin", "linux"]
metadata.clawdbot.requires.bins: ["python3"]
metadata.clawdbot.requires.env: ["COMFY_URL", "COMFY_AUTH_HEADER"]
metadata.clawdbot.files: ["workflow.json", "skill.py", "skill.yaml", "scripts/*"]
metadata.clawdbot.tags: ["comfyui", "workflow", "curated", "editing_restyle"]
metadata.clawdbot.category: "media-editing"
metadata.clawdbot.input_type: "image/png"
metadata.clawdbot.output_type: "image/png"
metadata.clawdbot.output_can_feed_into: []
metadata.clawdbot.accepts_input_from: []
metadata.clawdbot.priority: 70
---

# curated_ep29_flux_dev_replace_simple_or_white_background

Curated workflow skill generated from `EP29 Flux Dev Replace Simple or White Background.json`.

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

- `vae`: `ae.safetensors` -> `models/vae`
- `controlnet`: `flux-dev-controlnet-union.safetensors` -> `models/controlnet`
- `diffusion_model`: `flux1-dev-Q8_0.gguf` -> `models/diffusion_models`
- `clip`: `t5-v1_1-xxl-encoder-Q8_0.gguf` -> `models/clip`

## Custom Node Requirements

- None detected.

## Links Extracted From Workflow Notes

- None detected.

## Source

- Original: `comfy-data/workflows/EP29 Flux Dev Replace Simple or White Background.json`
