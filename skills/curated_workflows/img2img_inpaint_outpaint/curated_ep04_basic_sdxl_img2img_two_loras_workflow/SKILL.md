---
name: curated_ep04_basic_sdxl_img2img_two_loras_workflow
description: >
  Curated ComfyUI workflow imported from `EP04 Basic SDXL IMG2IMG TWO LORAS Workflow.json`.
homepage: https://github.com/steliosot/comfy-agent
metadata.clawdbot.os: ["darwin", "linux"]
metadata.clawdbot.requires.bins: ["python3"]
metadata.clawdbot.requires.env: ["COMFY_URL", "COMFY_AUTH_HEADER"]
metadata.clawdbot.files: ["workflow.json", "skill.py", "skill.yaml", "scripts/*"]
metadata.clawdbot.tags: ["comfyui", "workflow", "curated", "img2img_inpaint_outpaint"]
metadata.clawdbot.category: "media-editing"
metadata.clawdbot.input_type: "text"
metadata.clawdbot.output_type: "image/png"
metadata.clawdbot.output_can_feed_into: []
metadata.clawdbot.accepts_input_from: []
metadata.clawdbot.priority: 70
---

# curated_ep04_basic_sdxl_img2img_two_loras_workflow

Curated workflow skill generated from `EP04 Basic SDXL IMG2IMG TWO LORAS Workflow.json`.

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

- `checkpoint`: `Juggernaut_X_RunDiffusion.safetensors` -> `models/checkpoints`
- `lora`: `Aether_Cloud_v1.safetensors` -> `models/loras`
- `lora`: `Aether_Fire_v1_SDXL_LoRA.safetensors` -> `models/loras`

## Custom Node Requirements

- None detected.

## Links Extracted From Workflow Notes

- None detected.

## Source

- Original: `comfy-data/workflows/EP04 Basic SDXL IMG2IMG TWO LORAS Workflow.json`
