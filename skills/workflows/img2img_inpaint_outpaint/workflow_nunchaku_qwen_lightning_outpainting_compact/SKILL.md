---
name: workflow_nunchaku_qwen_lightning_outpainting_compact
description: >
  Workflow wrapper imported from `Nunchaku Qwen Lightning - Outpainting - COMPACT.json`.
homepage: https://github.com/steliosot/comfy-agent
metadata.clawdbot.os: ["darwin", "linux"]
metadata.clawdbot.requires.bins: ["python3"]
metadata.clawdbot.requires.env: ["COMFY_URL", "COMFY_AUTH_HEADER"]
metadata.clawdbot.files: ["workflow.json", "skill.py", "skill.yaml", "scripts/*"]
metadata.clawdbot.tags: ["comfyui", "workflow", "library", "img2img_inpaint_outpaint"]
metadata.clawdbot.category: "media-generation"
metadata.clawdbot.input_type: "image/png"
metadata.clawdbot.output_type: "image/png"
metadata.clawdbot.output_can_feed_into: []
metadata.clawdbot.accepts_input_from: []
metadata.clawdbot.priority: 60
---

# workflow_nunchaku_qwen_lightning_outpainting_compact

Imported workflow skill generated from `Nunchaku Qwen Lightning - Outpainting - COMPACT.json`.

## Family

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
  - `output_images`

## Model Requirements

- None detected from loader nodes.

## Custom Node Requirements

- `rgthree-comfy`

## Links

- https://discord.com/invite/gggpkVgBf3
- https://github.com/Tavris1/ComfyUI-Easy-Install
- https://github.com/nunchaku-tech/ComfyUI-nunchaku
- https://huggingface.co/Comfy-Org/Qwen-Image-InstantX-ControlNets/resolve/main/split_files/controlnet/Qwen-Image-InstantX-ControlNet-Inpainting.safetensors?download=true
- https://huggingface.co/Comfy-Org/Qwen-Image_ComfyUI/resolve/main/split_files/text_encoders/qwen_2.5_vl_7b_fp8_scaled.safetensors
- https://huggingface.co/Comfy-Org/Qwen-Image_ComfyUI/resolve/main/split_files/vae/qwen_image_vae.safetensors
- https://huggingface.co/Comfy-Org/Qwen-Image_ComfyUI/tree/main/split_files/text_encoders
- https://huggingface.co/nunchaku-tech/nunchaku-qwen-image/resolve/main/svdq-int4_r32-qwen-image-lightningv1.1-8steps.safetensors?download=true
- https://huggingface.co/nunchaku-tech/nunchaku-qwen-image/tree/main
- https://www.youtube.com/@pixaroma

<!-- AUTO-METADATA-START -->
## Routing Metadata

- Family: `img2img_inpaint_outpaint`
- Input modalities: `image`
- Output modalities: `image/png`
- Model families: `other`
- Node count: `6`
- Complexity score: `1`
- Resource profile: `low`
- Estimated runtime: `fast (usually under 30s on modern GPU)`
- Max latent resolution hint: `None`x`None`
- Max sampler steps hint: `None`

## Detected Models

- None detected.

## Detected Custom Nodes

- `rgthree-comfy`

## Runtime Warnings

- Uses custom nodes; missing nodes can cause validation/runtime failures.
<!-- AUTO-METADATA-END -->

