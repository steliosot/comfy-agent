---
name: curated_wan_2_2_i2v_14b_gguf_lora
description: >
  Curated ComfyUI workflow imported from `Wan 2.2 I2V 14b GGUF + Lora.json`.
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

# curated_wan_2_2_i2v_14b_gguf_lora

Curated workflow skill generated from `Wan 2.2 I2V 14b GGUF + Lora.json`.

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
- `diffusion_model`: `wan2.2_i2v_low_noise_14B_Q4_K_M.gguf` -> `models/diffusion_models`
- `diffusion_model`: `wan2.2_i2v_high_noise_14B_Q4_K_M.gguf` -> `models/diffusion_models`
- `lora`: `Wan2.2-Lightning_I2V-A14B-4steps-lora_LOW_fp16.safetensors` -> `models/loras`
- `lora`: `Wan2.2-Lightning_I2V-A14B-4steps-lora_HIGH_fp16.safetensors` -> `models/loras`
- `clip`: `umt5_xxl_fp8_e4m3fn_scaled.safetensors` -> `models/clip`

## Custom Node Requirements

- `ComfyUI-GGUF`
- `comfyui-videohelpersuite`

## Links Extracted From Workflow Notes

- https://discord.com/invite/gggpkVgBf3
- https://docs.comfy.org/tutorials/video/wan/wan2_2
- https://huggingface.co/Comfy-Org/Wan_2.1_ComfyUI_repackaged/resolve/main/split_files/text_encoders/umt5_xxl_fp8_e4m3fn_scaled.safetensors?download=true
- https://huggingface.co/Comfy-Org/Wan_2.1_ComfyUI_repackaged/resolve/main/split_files/vae/wan_2.1_vae.safetensors?download=true
- https://huggingface.co/Kijai/WanVideo_comfy/resolve/main/LoRAs/Wan22-Lightning/old/Wan2.2-Lightning_I2V-A14B-4steps-lora_HIGH_fp16.safetensors?download=true
- https://huggingface.co/Kijai/WanVideo_comfy/resolve/main/LoRAs/Wan22-Lightning/old/Wan2.2-Lightning_I2V-A14B-4steps-lora_LOW_fp16.safetensors?download=true
- https://huggingface.co/Wan-AI/Wan2.2-I2V-A14B
- https://huggingface.co/bullerwins/Wan2.2-I2V-A14B-GGUF/resolve/main/wan2.2_i2v_high_noise_14B_Q4_K_M.gguf?download=true
- https://huggingface.co/bullerwins/Wan2.2-I2V-A14B-GGUF/resolve/main/wan2.2_i2v_low_noise_14B_Q4_K_M.gguf?download=true
- https://huggingface.co/bullerwins/Wan2.2-I2V-A14B-GGUF/tree/main
- https://www.youtube.com/@pixaroma

## Source

- Original: `comfy-data/workflows/Wan 2.2 I2V 14b GGUF + Lora.json`
