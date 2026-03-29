---
name: curated_ep42_sdxl_outpaint_juggernaut
description: >
  Curated ComfyUI workflow imported from `EP42 SDXL OUTPAINT Juggernaut.json`.
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

# curated_ep42_sdxl_outpaint_juggernaut

Curated workflow skill generated from `EP42 SDXL OUTPAINT Juggernaut.json`.

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

- `checkpoint`: `juggernautXL_versionXInpaint.safetensors` -> `models/checkpoints`

## Custom Node Requirements

- `comfyui-inpaint-cropandstitch`

## Links Extracted From Workflow Notes

- https://civitai.com/api/download/models/456538?type=Model&format=SafeTensor&size=pruned&fp=fp16
- https://civitai.com/models/403361?modelVersionId=456538
- https://discord.com/invite/gggpkVgBf3
- https://www.youtube.com/@pixaroma

## Source

- Original: `comfy-data/workflows/EP42 SDXL OUTPAINT Juggernaut.json`

<!-- AUTO-METADATA-START -->
## Routing Metadata

- Family: `img2img_inpaint_outpaint`
- Input modalities: `image, text_prompt`
- Output modalities: `image/png`
- Model families: `other`
- Node count: `13`
- Complexity score: `1`
- Resource profile: `low`
- Estimated runtime: `fast (usually under 30s on modern GPU)`
- Max latent resolution hint: `None`x`None`
- Max sampler steps hint: `30`

## Detected Models

- `checkpoint`: `juggernautXL_versionXInpaint.safetensors` -> `models/checkpoints`

## Detected Custom Nodes

- `comfyui-inpaint-cropandstitch`

## Runtime Warnings

- Uses custom nodes; missing nodes can cause validation/runtime failures.
<!-- AUTO-METADATA-END -->

