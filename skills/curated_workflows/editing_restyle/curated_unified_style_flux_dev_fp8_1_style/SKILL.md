---
name: curated_unified_style_flux_dev_fp8_1_style
description: >
  Curated ComfyUI workflow imported from `Unified Style Flux Dev FP8 - 1 Style.json`.
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

# curated_unified_style_flux_dev_fp8_1_style

Curated workflow skill generated from `Unified Style Flux Dev FP8 - 1 Style.json`.

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

- `checkpoint`: `flux1-dev-fp8.safetensors` -> `models/checkpoints`
- `lora`: `uso-flux1-dit-lora-v1.safetensors` -> `models/loras`

## Custom Node Requirements

- `controlaltai-nodes`

## Links Extracted From Workflow Notes

- https://blog.comfy.org/p/uso-available-in-comfyui
- https://discord.com/invite/gggpkVgBf3
- https://github.com/bytedance/USO
- https://huggingface.co/Comfy-Org/USO_1.0_Repackaged/resolve/main/split_files/loras/uso-flux1-dit-lora-v1.safetensors
- https://huggingface.co/Comfy-Org/USO_1.0_Repackaged/resolve/main/split_files/model_patches/uso-flux1-projector-v1.safetensors
- https://huggingface.co/Comfy-Org/flux1-dev/resolve/main/flux1-dev-fp8.safetensors
- https://huggingface.co/Comfy-Org/sigclip_vision_384/resolve/main/sigclip_vision_patch14_384.safetensors
- https://www.youtube.com/@pixaroma

## Source

- Original: `comfy-data/workflows/Unified Style Flux Dev FP8 - 1 Style.json`
