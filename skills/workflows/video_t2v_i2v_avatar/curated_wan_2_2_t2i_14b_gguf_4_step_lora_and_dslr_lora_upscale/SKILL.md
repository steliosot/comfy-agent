---
name: curated_wan_2_2_t2i_14b_gguf_4_step_lora_and_dslr_lora_upscale
description: >
  Curated ComfyUI workflow imported from `Wan 2.2 T2I 14b GGUF + 4 Step Lora and DSLR Lora + Upscale.json`.
homepage: https://github.com/steliosot/comfy-agent
metadata.clawdbot.os: ["darwin", "linux"]
metadata.clawdbot.requires.bins: ["python3"]
metadata.clawdbot.requires.env: ["COMFY_URL", "COMFY_AUTH_HEADER"]
metadata.clawdbot.files: ["workflow.json", "skill.py", "skill.yaml", "scripts/*"]
metadata.clawdbot.tags: ["comfyui", "workflow", "curated", "video_t2v_i2v_avatar"]
metadata.clawdbot.category: "media-generation"
metadata.clawdbot.input_type: "text"
metadata.clawdbot.output_type: "image/png"
metadata.clawdbot.output_can_feed_into: []
metadata.clawdbot.accepts_input_from: []
metadata.clawdbot.priority: 70
---

# curated_wan_2_2_t2i_14b_gguf_4_step_lora_and_dslr_lora_upscale

Curated workflow skill generated from `Wan 2.2 T2I 14b GGUF + 4 Step Lora and DSLR Lora + Upscale.json`.

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

- `diffusion_model`: `Wan2.2-T2V-A14B-LowNoise-Q8_0.gguf` -> `models/diffusion_models`
- `vae`: `wan_2.1_vae.safetensors` -> `models/vae`
- `clip`: `umt5_xxl_fp8_e4m3fn_scaled.safetensors` -> `models/clip`
- `upscale_model`: `4x_NMKD-Siax_200k.pth` -> `models/upscale_models`

## Custom Node Requirements

- `ComfyUI-GGUF`
- `comfyui-easy-use`
- `comfyui-kjnodes`
- `controlaltai-nodes`
- `rgthree-comfy`

## Links Extracted From Workflow Notes

- https://civitai.com/models/1832621/dslr-photovideo-wan-2122-low-noise?modelVersionId=2073884
- https://discord.com/invite/gggpkVgBf3
- https://huggingface.co/Akumetsu971/SD_Anime_Futuristic_Armor/resolve/main/4x_NMKD-Siax_200k.pth?download=true
- https://huggingface.co/Comfy-Org/Wan_2.1_ComfyUI_repackaged/resolve/main/split_files/text_encoders/umt5_xxl_fp8_e4m3fn_scaled.safetensors?download=true
- https://huggingface.co/Comfy-Org/Wan_2.1_ComfyUI_repackaged/resolve/main/split_files/vae/wan_2.1_vae.safetensors?download=true
- https://huggingface.co/QuantStack/Wan2.2-T2V-A14B-GGUF/resolve/main/LowNoise/Wan2.2-T2V-A14B-LowNoise-Q8_0.gguf?download=true
- https://huggingface.co/QuantStack/Wan2.2-T2V-A14B-GGUF/tree/main/LowNoise
- https://huggingface.co/lightx2v/Wan2.2-Lightning/resolve/main/Wan2.2-T2V-A14B-4steps-lora-rank64-Seko-V1.1/low_noise_model.safetensors?download=true
- https://huggingface.co/lightx2v/Wan2.2-Lightning/tree/main/Wan2.2-T2V-A14B-4steps-lora-rank64-Seko-V1.1
- https://www.youtube.com/@pixaroma
- https://www.youtube.com/watch?v=CgLL5aoEX-s

## Source

- Original: `comfy-data/workflows/Wan 2.2 T2I 14b GGUF + 4 Step Lora and DSLR Lora + Upscale.json`

<!-- AUTO-METADATA-START -->
## Routing Metadata

- Family: `video_t2v_i2v_avatar`
- Input modalities: `text_prompt`
- Output modalities: `image/png`
- Model families: `flux, sd3, wan`
- Node count: `32`
- Complexity score: `12`
- Resource profile: `very_high`
- Estimated runtime: `heavy (can exceed 6 min; best on high-VRAM GPU)`
- Max latent resolution hint: `1920`x`1088`
- Max sampler steps hint: `8`

## Detected Models

- `diffusion_model`: `Wan2.2-T2V-A14B-LowNoise-Q8_0.gguf` -> `models/diffusion_models`
- `vae`: `wan_2.1_vae.safetensors` -> `models/vae`
- `clip`: `umt5_xxl_fp8_e4m3fn_scaled.safetensors` -> `models/clip`
- `upscale_model`: `4x_NMKD-Siax_200k.pth` -> `models/upscale_models`

## Detected Custom Nodes

- `ComfyUI-GGUF`
- `comfyui-easy-use`
- `comfyui-kjnodes`
- `controlaltai-nodes`
- `rgthree-comfy`

## Runtime Warnings

- High output resolution detected; generation time/memory use can increase significantly.
- Large model(s) detected; ensure enough VRAM and disk space.
- Multiple custom nodes required; verify node installation/version compatibility.
- Video workflow: usually slower and VRAM-intensive than still-image workflows.
<!-- AUTO-METADATA-END -->

