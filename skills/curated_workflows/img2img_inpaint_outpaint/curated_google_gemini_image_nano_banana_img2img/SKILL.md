---
name: curated_google_gemini_image_nano_banana_img2img
description: >
  Curated ComfyUI workflow imported from `Google Gemini Image - Nano Banana - img2img.json`.
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

# curated_google_gemini_image_nano_banana_img2img

Curated workflow skill generated from `Google Gemini Image - Nano Banana - img2img.json`.

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

- None detected from loader nodes.

## Custom Node Requirements

- None detected.

## Links Extracted From Workflow Notes

- https://discord.com/invite/gggpkVgBf3
- https://docs.comfy.org/tutorials/api-nodes/pricing
- https://www.youtube.com/@pixaroma

## Source

- Original: `comfy-data/workflows/Google Gemini Image - Nano Banana - img2img.json`
