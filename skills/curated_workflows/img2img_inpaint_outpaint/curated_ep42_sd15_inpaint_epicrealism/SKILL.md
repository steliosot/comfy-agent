---
name: curated_ep42_sd15_inpaint_epicrealism
description: >
  Curated ComfyUI workflow imported from `EP42 SD15 INPAINT EpicRealism.json`.
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

# curated_ep42_sd15_inpaint_epicrealism

Curated workflow skill generated from `EP42 SD15 INPAINT EpicRealism.json`.

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

- `checkpoint`: `epicrealism_v10-inpainting.safetensors` -> `models/checkpoints`

## Custom Node Requirements

- `comfyui-inpaint-cropandstitch`

## Links Extracted From Workflow Notes

- https://civitai.com/api/download/models/95864?type=Model&format=SafeTensor&size=pruned&fp=fp16
- https://civitai.com/models/90018/epicrealism-pureevolution-inpainting
- https://discord.com/invite/gggpkVgBf3
- https://www.youtube.com/@pixaroma

## Source

- Original: `comfy-data/workflows/EP42 SD15 INPAINT EpicRealism.json`
