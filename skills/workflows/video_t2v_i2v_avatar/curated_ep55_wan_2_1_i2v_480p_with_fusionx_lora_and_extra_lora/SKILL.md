---
name: curated_ep55_wan_2_1_i2v_480p_with_fusionx_lora_and_extra_lora
description: >
  Curated ComfyUI workflow imported from `Ep55 Wan 2.1 I2V 480p with FusionX Lora and Extra Lora.json`.
homepage: https://github.com/steliosot/comfy-agent
metadata.clawdbot.os: ["darwin", "linux"]
metadata.clawdbot.requires.bins: ["python3"]
metadata.clawdbot.requires.env: ["COMFY_URL", "COMFY_AUTH_HEADER"]
metadata.clawdbot.files: ["workflow.json", "skill.py", "skill.yaml", "scripts/*"]
metadata.clawdbot.tags: ["comfyui", "workflow", "curated", "video_t2v_i2v_avatar"]
metadata.clawdbot.category: "media-generation"
metadata.clawdbot.input_type: "image/png"
metadata.clawdbot.output_type: "video/mp4"
metadata.clawdbot.output_can_feed_into: []
metadata.clawdbot.accepts_input_from: []
metadata.clawdbot.priority: 70
---

# curated_ep55_wan_2_1_i2v_480p_with_fusionx_lora_and_extra_lora

Curated workflow skill generated from `Ep55 Wan 2.1 I2V 480p with FusionX Lora and Extra Lora.json`.

## Capability Family

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
  - `output_images` (includes image/video entries reported by Comfy history)

## Model Requirements

- `vae`: `wan_2.1_vae.safetensors` -> `models/vae`
- `clip`: `umt5_xxl_fp8_e4m3fn_scaled.safetensors` -> `models/clip`
- `diffusion_model`: `wan2.1-i2v-14b-480p-Q4_0.gguf` -> `models/diffusion_models`

## Custom Node Requirements

- `ComfyUI-GGUF`
- `comfyui-videohelpersuite`
- `rgthree-comfy`

## Links Extracted From Workflow Notes

- https://discord.com/invite/gggpkVgBf3
- https://github.com/Tavris1/ComfyUI-Easy-Install/tree/Windows
- https://huggingface.co/Comfy-Org/Wan_2.1_ComfyUI_repackaged/resolve/main/split_files/clip_vision/clip_vision_h.safetensors?download=true
- https://huggingface.co/Comfy-Org/Wan_2.1_ComfyUI_repackaged/resolve/main/split_files/text_encoders/umt5_xxl_fp8_e4m3fn_scaled.safetensors?download=true
- https://huggingface.co/Comfy-Org/Wan_2.1_ComfyUI_repackaged/resolve/main/split_files/vae/wan_2.1_vae.safetensors?download=true
- https://huggingface.co/Remade-AI/Squish/resolve/main/squish_18.safetensors?download=true
- https://huggingface.co/city96/Wan2.1-I2V-14B-480P-gguf/resolve/main/wan2.1-i2v-14b-480p-Q4_0.gguf?download=true
- https://huggingface.co/city96/Wan2.1-I2V-14B-480P-gguf/tree/main
- https://huggingface.co/collections/Remade-AI/wan21-14b-480p-i2v-loras-67d0e26f08092436b585919b
- https://huggingface.co/vrgamedevgirl84/Wan14BT2VFusioniX
- https://huggingface.co/vrgamedevgirl84/Wan14BT2VFusioniX/resolve/main/FusionX_LoRa/Wan2.1_I2V_14B_FusionX_LoRA.safetensors?download=true
- https://www.youtube.com/@pixaroma

## Source

- Original: `comfy-data/workflows/Ep55 Wan 2.1 I2V 480p with FusionX Lora and Extra Lora.json`

<!-- AUTO-METADATA-START -->
## Routing Metadata

- Family: `video_t2v_i2v_avatar`
- Input modalities: `image, text_prompt`
- Output modalities: `video/mp4`
- Model families: `sd3, wan`
- Node count: `19`
- Complexity score: `8`
- Resource profile: `high`
- Estimated runtime: `slow (often 2-6 min depending on model/server load)`
- Max latent resolution hint: `None`x`None`
- Max sampler steps hint: `8`

## Detected Models

- `vae`: `wan_2.1_vae.safetensors` -> `models/vae`
- `clip`: `umt5_xxl_fp8_e4m3fn_scaled.safetensors` -> `models/clip`
- `diffusion_model`: `wan2.1-i2v-14b-480p-Q4_0.gguf` -> `models/diffusion_models`

## Detected Custom Nodes

- `ComfyUI-GGUF`
- `comfyui-videohelpersuite`
- `rgthree-comfy`

## Runtime Warnings

- Large model(s) detected; ensure enough VRAM and disk space.
- Uses custom nodes; missing nodes can cause validation/runtime failures.
- Video workflow: usually slower and VRAM-intensive than still-image workflows.
<!-- AUTO-METADATA-END -->

