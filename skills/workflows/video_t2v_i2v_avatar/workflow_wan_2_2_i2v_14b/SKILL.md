---
name: workflow_wan_2_2_i2v_14b
description: >
  Workflow wrapper imported from `Wan 2.2 I2V 14B.json`.
homepage: https://github.com/steliosot/comfy-agent
metadata.clawdbot.os: ["darwin", "linux"]
metadata.clawdbot.requires.bins: ["python3"]
metadata.clawdbot.requires.env: ["COMFY_URL", "COMFY_AUTH_HEADER"]
metadata.clawdbot.files: ["workflow.json", "skill.py", "skill.yaml", "scripts/*"]
metadata.clawdbot.tags: ["comfyui", "workflow", "library", "video_t2v_i2v_avatar"]
metadata.clawdbot.category: "media-generation"
metadata.clawdbot.input_type: "image/png"
metadata.clawdbot.output_type: "video/mp4"
metadata.clawdbot.output_can_feed_into: []
metadata.clawdbot.accepts_input_from: []
metadata.clawdbot.priority: 60
---

# workflow_wan_2_2_i2v_14b

Imported workflow skill generated from `Wan 2.2 I2V 14B.json`.

## Family

- `video_t2v_i2v_avatar`

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

- `clip`: `umt5_xxl_fp8_e4m3fn_scaled.safetensors` -> `models/clip`
- `vae`: `wan_2.1_vae.safetensors` -> `models/vae`
- `diffusion_model`: `wan2.2_i2v_high_noise_14B_fp8_scaled.safetensors` -> `models/diffusion_models`
- `diffusion_model`: `wan2.2_i2v_low_noise_14B_fp8_scaled.safetensors` -> `models/diffusion_models`

## Custom Node Requirements

- `comfyui-videohelpersuite`

## Links

- https://discord.com/invite/gggpkVgBf3
- https://docs.comfy.org/tutorials/video/wan/wan2_2
- https://huggingface.co/Comfy-Org/Wan_2.1_ComfyUI_repackaged/resolve/main/split_files/text_encoders/umt5_xxl_fp8_e4m3fn_scaled.safetensors?download=true
- https://huggingface.co/Comfy-Org/Wan_2.1_ComfyUI_repackaged/resolve/main/split_files/vae/wan_2.1_vae.safetensors?download=true
- https://huggingface.co/Comfy-Org/Wan_2.2_ComfyUI_Repackaged/resolve/main/split_files/diffusion_models/wan2.2_i2v_high_noise_14B_fp8_scaled.safetensors?download=true
- https://huggingface.co/Comfy-Org/Wan_2.2_ComfyUI_Repackaged/resolve/main/split_files/diffusion_models/wan2.2_i2v_low_noise_14B_fp8_scaled.safetensors?download=true
- https://huggingface.co/Comfy-Org/Wan_2.2_ComfyUI_Repackaged/tree/main/split_files/diffusion_models
- https://huggingface.co/Wan-AI/Wan2.2-I2V-A14B
- https://www.youtube.com/@pixaroma

<!-- AUTO-METADATA-START -->
## Routing Metadata

- Family: `video_t2v_i2v_avatar`
- Input modalities: `image, text_prompt`
- Output modalities: `video/mp4`
- Model families: `sd3, wan`
- Node count: `18`
- Complexity score: `9`
- Resource profile: `very_high`
- Estimated runtime: `heavy (can exceed 6 min; best on high-VRAM GPU)`
- Max latent resolution hint: `None`x`None`
- Max sampler steps hint: `None`

## Detected Models

- `clip`: `umt5_xxl_fp8_e4m3fn_scaled.safetensors` -> `models/clip`
- `vae`: `wan_2.1_vae.safetensors` -> `models/vae`
- `diffusion_model`: `wan2.2_i2v_high_noise_14B_fp8_scaled.safetensors` -> `models/diffusion_models`
- `diffusion_model`: `wan2.2_i2v_low_noise_14B_fp8_scaled.safetensors` -> `models/diffusion_models`

## Detected Custom Nodes

- `comfyui-videohelpersuite`

## Runtime Warnings

- Large model(s) detected; ensure enough VRAM and disk space.
- Uses custom nodes; missing nodes can cause validation/runtime failures.
- Video workflow: usually slower and VRAM-intensive than still-image workflows.
<!-- AUTO-METADATA-END -->

