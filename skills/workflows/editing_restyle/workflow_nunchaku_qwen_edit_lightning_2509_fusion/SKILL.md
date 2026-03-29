---
name: workflow_nunchaku_qwen_edit_lightning_2509_fusion
description: >
  Workflow wrapper imported from `Nunchaku Qwen Edit Lightning 2509 - Fusion.json`.
homepage: https://github.com/steliosot/comfy-agent
metadata.clawdbot.os: ["darwin", "linux"]
metadata.clawdbot.requires.bins: ["python3"]
metadata.clawdbot.requires.env: ["COMFY_URL", "COMFY_AUTH_HEADER"]
metadata.clawdbot.files: ["workflow.json", "skill.py", "skill.yaml", "scripts/*"]
metadata.clawdbot.tags: ["comfyui", "workflow", "library", "editing_restyle"]
metadata.clawdbot.category: "media-generation"
metadata.clawdbot.input_type: "image/png"
metadata.clawdbot.output_type: "image/png"
metadata.clawdbot.output_can_feed_into: []
metadata.clawdbot.accepts_input_from: []
metadata.clawdbot.priority: 60
---

# workflow_nunchaku_qwen_edit_lightning_2509_fusion

Imported workflow skill generated from `Nunchaku Qwen Edit Lightning 2509 - Fusion.json`.

## Family

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
  - `output_images`

## Model Requirements

- `clip`: `qwen_2.5_vl_7b_fp8_scaled.safetensors` -> `models/clip`
- `vae`: `qwen_image_vae.safetensors` -> `models/vae`

## Custom Node Requirements

- `ComfyUI-nunchaku`
- `comfyui-qwenimageloraloader`
- `rgthree-comfy`

## Links

- https://discord.com/invite/gggpkVgBf3
- https://github.com/Tavris1/ComfyUI-Easy-Install
- https://github.com/nunchaku-tech/ComfyUI-nunchaku
- https://huggingface.co/Comfy-Org/Qwen-Image_ComfyUI/resolve/main/split_files/text_encoders/qwen_2.5_vl_7b_fp8_scaled.safetensors
- https://huggingface.co/Comfy-Org/Qwen-Image_ComfyUI/resolve/main/split_files/vae/qwen_image_vae.safetensors
- https://huggingface.co/Comfy-Org/Qwen-Image_ComfyUI/tree/main/split_files/text_encoders
- https://huggingface.co/dx8152/Qwen-Image-Edit-2509-Fusion
- https://huggingface.co/dx8152/Qwen-Image-Edit-2509-Fusion/resolve/main/%E6%BA%B6%E5%9B%BE.safetensors?download=true
- https://huggingface.co/nunchaku-tech/nunchaku-qwen-image-edit-2509/resolve/main/svdq-int4_r128-qwen-image-edit-2509-lightningv2.0-4steps.safetensors?download=true
- https://huggingface.co/nunchaku-tech/nunchaku-qwen-image-edit-2509/tree/main
- https://www.youtube.com/@pixaroma

<!-- AUTO-METADATA-START -->
## Routing Metadata

- Family: `editing_restyle`
- Input modalities: `image`
- Output modalities: `image/png`
- Model families: `qwen`
- Node count: `19`
- Complexity score: `1`
- Resource profile: `low`
- Estimated runtime: `fast (usually under 30s on modern GPU)`
- Max latent resolution hint: `None`x`None`
- Max sampler steps hint: `4`

## Detected Models

- `clip`: `qwen_2.5_vl_7b_fp8_scaled.safetensors` -> `models/clip`
- `vae`: `qwen_image_vae.safetensors` -> `models/vae`

## Detected Custom Nodes

- `ComfyUI-nunchaku`
- `comfyui-qwenimageloraloader`
- `rgthree-comfy`

## Runtime Warnings

- Uses custom nodes; missing nodes can cause validation/runtime failures.
<!-- AUTO-METADATA-END -->

