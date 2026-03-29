---
name: curated_ep27_sdxl_image_to_oil_painting_with_lora_and_control_net_and_upscaler
description: >
  Curated ComfyUI workflow imported from `EP27 SDXL Image to Oil Painting with Lora and Control Net and UPSCALER.json`.
homepage: https://github.com/steliosot/comfy-agent
metadata.clawdbot.os: ["darwin", "linux"]
metadata.clawdbot.requires.bins: ["python3"]
metadata.clawdbot.requires.env: ["COMFY_URL", "COMFY_AUTH_HEADER"]
metadata.clawdbot.files: ["workflow.json", "skill.py", "skill.yaml", "scripts/*"]
metadata.clawdbot.tags: ["comfyui", "workflow", "curated", "upscaling"]
metadata.clawdbot.category: "media-editing"
metadata.clawdbot.input_type: "image/png"
metadata.clawdbot.output_type: "image/png"
metadata.clawdbot.output_can_feed_into: []
metadata.clawdbot.accepts_input_from: []
metadata.clawdbot.priority: 70
---

# curated_ep27_sdxl_image_to_oil_painting_with_lora_and_control_net_and_upscaler

Curated workflow skill generated from `EP27 SDXL Image to Oil Painting with Lora and Control Net and UPSCALER.json`.

## Capability Family

- `upscaling`

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

- `upscale_model`: `4x_NMKD-Siax_200k.pth` -> `models/upscale_models`
- `checkpoint`: `Juggernaut_X_RunDiffusion.safetensors` -> `models/checkpoints`
- `controlnet`: `diffusion_pytorch_model_promax.safetensors` -> `models/controlnet`
- `lora`: `ClassipeintXL2.1.safetensors` -> `models/loras`

## Custom Node Requirements

- None detected.

## Links Extracted From Workflow Notes

- None detected.

## Source

- Original: `comfy-data/workflows/EP27 SDXL Image to Oil Painting with Lora and Control Net and UPSCALER.json`

<!-- AUTO-METADATA-START -->
## Routing Metadata

- Family: `upscaling`
- Input modalities: `image, text_prompt`
- Output modalities: `image/png`
- Model families: `other`
- Node count: `28`
- Complexity score: `0`
- Resource profile: `low`
- Estimated runtime: `fast (usually under 30s on modern GPU)`
- Max latent resolution hint: `None`x`None`
- Max sampler steps hint: `30`

## Detected Models

- `upscale_model`: `4x_NMKD-Siax_200k.pth` -> `models/upscale_models`
- `checkpoint`: `Juggernaut_X_RunDiffusion.safetensors` -> `models/checkpoints`
- `controlnet`: `diffusion_pytorch_model_promax.safetensors` -> `models/controlnet`
- `lora`: `ClassipeintXL2.1.safetensors` -> `models/loras`

## Detected Custom Nodes

- None detected.

## Runtime Warnings

- No major runtime warnings detected.
<!-- AUTO-METADATA-END -->

