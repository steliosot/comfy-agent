---
name: curated_ep28_liveportrait_expression_editor_with_flux_upscale
description: >
  Curated ComfyUI workflow imported from `Ep28 LivePortrait Expression Editor with Flux Upscale.json`.
homepage: https://github.com/steliosot/comfy-agent
metadata.clawdbot.os: ["darwin", "linux"]
metadata.clawdbot.requires.bins: ["python3"]
metadata.clawdbot.requires.env: ["COMFY_URL", "COMFY_AUTH_HEADER"]
metadata.clawdbot.files: ["workflow.json", "skill.py", "skill.yaml", "scripts/*"]
metadata.clawdbot.tags: ["comfyui", "workflow", "curated", "video_t2v_i2v_avatar"]
metadata.clawdbot.category: "media-generation"
metadata.clawdbot.input_type: "image/png"
metadata.clawdbot.output_type: "image/png"
metadata.clawdbot.output_can_feed_into: []
metadata.clawdbot.accepts_input_from: []
metadata.clawdbot.priority: 70
---

# curated_ep28_liveportrait_expression_editor_with_flux_upscale

Curated workflow skill generated from `Ep28 LivePortrait Expression Editor with Flux Upscale.json`.

## Capability Family

- `video_t2v_i2v_avatar`

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

- `clip`: `t5-v1_1-xxl-encoder-Q8_0.gguf` -> `models/clip`
- `diffusion_model`: `flux1-dev-Q8_0.gguf` -> `models/diffusion_models`
- `vae`: `ae.safetensors` -> `models/vae`
- `upscale_model`: `4x_NMKD-Siax_200k.pth` -> `models/upscale_models`

## Custom Node Requirements

- None detected.

## Links Extracted From Workflow Notes

- None detected.

## Source

- Original: `comfy-data/workflows/Ep28 LivePortrait Expression Editor with Flux Upscale.json`
