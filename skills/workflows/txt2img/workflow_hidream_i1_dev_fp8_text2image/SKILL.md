---
name: workflow_hidream_i1_dev_fp8_text2image
description: >
  Workflow wrapper imported from `HiDream i1 Dev fp8 text2image.json`.
homepage: https://github.com/steliosot/comfy-agent
metadata.clawdbot.os: ["darwin", "linux"]
metadata.clawdbot.requires.bins: ["python3"]
metadata.clawdbot.requires.env: ["COMFY_URL", "COMFY_AUTH_HEADER"]
metadata.clawdbot.files: ["workflow.json", "skill.py", "skill.yaml", "scripts/*"]
metadata.clawdbot.tags: ["comfyui", "workflow", "library", "txt2img"]
metadata.clawdbot.category: "media-generation"
metadata.clawdbot.input_type: "text"
metadata.clawdbot.output_type: "image/png"
metadata.clawdbot.output_can_feed_into: []
metadata.clawdbot.accepts_input_from: []
metadata.clawdbot.priority: 60
---

# workflow_hidream_i1_dev_fp8_text2image

Imported workflow skill generated from `HiDream i1 Dev fp8 text2image.json`.

## Family

- `txt2img`

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

- `vae`: `ae.safetensors` -> `models/vae`
- `diffusion_model`: `hidream_i1_dev_fp8.safetensors` -> `models/diffusion_models`

## Custom Node Requirements

- None detected.

## Links

- https://blog.comfy.org/p/hidream-i1-native-support-in-comfyui
- https://comfyanonymous.github.io/ComfyUI_examples/hidream/
- https://discord.com/invite/gggpkVgBf3
- https://docs.comfy.org/tutorials/advanced/hidream
- https://huggingface.co/Comfy-Org/HiDream-I1_ComfyUI/resolve/main/split_files/diffusion_models/hidream_i1_dev_fp8.safetensors?download=true
- https://huggingface.co/Comfy-Org/HiDream-I1_ComfyUI/resolve/main/split_files/text_encoders/clip_g_hidream.safetensors?download=true
- https://huggingface.co/Comfy-Org/HiDream-I1_ComfyUI/resolve/main/split_files/text_encoders/clip_l_hidream.safetensors?download=true
- https://huggingface.co/Comfy-Org/HiDream-I1_ComfyUI/resolve/main/split_files/text_encoders/llama_3.1_8b_instruct_fp8_scaled.safetensors?download=true
- https://huggingface.co/Comfy-Org/HiDream-I1_ComfyUI/resolve/main/split_files/text_encoders/t5xxl_fp8_e4m3fn_scaled.safetensors?download=true
- https://huggingface.co/Comfy-Org/HiDream-I1_ComfyUI/resolve/main/split_files/vae/ae.safetensors?download=true
- https://huggingface.co/Comfy-Org/HiDream-I1_ComfyUI/tree/main/split_files/diffusion_models
- https://huggingface.co/Comfy-Org/HiDream-I1_ComfyUI/tree/main/split_files/text_encoders
- https://www.youtube.com/@pixaroma

<!-- AUTO-METADATA-START -->
## Routing Metadata

- Family: `txt2img`
- Input modalities: `text_prompt`
- Output modalities: `image/png`
- Model families: `sd3`
- Node count: `11`
- Complexity score: `2`
- Resource profile: `low`
- Estimated runtime: `fast (usually under 30s on modern GPU)`
- Max latent resolution hint: `1024`x`1024`
- Max sampler steps hint: `28`

## Detected Models

- `vae`: `ae.safetensors` -> `models/vae`
- `diffusion_model`: `hidream_i1_dev_fp8.safetensors` -> `models/diffusion_models`

## Detected Custom Nodes

- None detected.

## Runtime Warnings

- Medium-high resolution detected; expect moderate extra runtime.
<!-- AUTO-METADATA-END -->

