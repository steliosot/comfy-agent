---
name: curated_ep18_sdxl_animationcartoon_img2img_with_controlnet
description: >
  Curated ComfyUI workflow imported from `EP18 SDXL AnimationCartoon IMG2IMG with ControlNet.json`.
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

# curated_ep18_sdxl_animationcartoon_img2img_with_controlnet

Curated workflow skill generated from `EP18 SDXL AnimationCartoon IMG2IMG with ControlNet.json`.

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
- `checkpoint`: `wildcardxXLANIMATION_wildcardxXLANIMATION.safetensors` -> `models/checkpoints`

## Custom Node Requirements

- None detected.

## Links Extracted From Workflow Notes

- https://civitai.com/models/297501?modelVersionId=357959

## Source

- Original: `comfy-data/workflows/EP18 SDXL AnimationCartoon IMG2IMG with ControlNet.json`

<!-- AUTO-METADATA-START -->
## Routing Metadata

- Family: `img2img_inpaint_outpaint`
- Input modalities: `image, text_prompt`
- Output modalities: `image/png`
- Model families: `flux, wan`
- Node count: `28`
- Complexity score: `2`
- Resource profile: `low`
- Estimated runtime: `fast (usually under 30s on modern GPU)`
- Max latent resolution hint: `None`x`None`
- Max sampler steps hint: `30`

## Detected Models

- `controlnet`: `diffusion_pytorch_model_promax.safetensors` -> `models/controlnet`
- `checkpoint`: `wildcardxXLANIMATION_wildcardxXLANIMATION.safetensors` -> `models/checkpoints`

## Detected Custom Nodes

- None detected.

## Runtime Warnings

- Large model(s) detected; ensure enough VRAM and disk space.
<!-- AUTO-METADATA-END -->

