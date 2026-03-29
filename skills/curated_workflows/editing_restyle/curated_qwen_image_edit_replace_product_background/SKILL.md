---
name: curated_qwen_image_edit_replace_product_background
description: >
  Curated ComfyUI workflow imported from `Qwen Image Edit - Replace Product Background.json`.
homepage: https://github.com/steliosot/comfy-agent
metadata.clawdbot.os: ["darwin", "linux"]
metadata.clawdbot.requires.bins: ["python3"]
metadata.clawdbot.requires.env: ["COMFY_URL", "COMFY_AUTH_HEADER"]
metadata.clawdbot.files: ["workflow.json", "skill.py", "skill.yaml", "scripts/*"]
metadata.clawdbot.tags: ["comfyui", "workflow", "curated", "editing_restyle"]
metadata.clawdbot.category: "media-editing"
metadata.clawdbot.input_type: "image/png"
metadata.clawdbot.output_type: "image/png"
metadata.clawdbot.output_can_feed_into: []
metadata.clawdbot.accepts_input_from: []
metadata.clawdbot.priority: 70
---

# curated_qwen_image_edit_replace_product_background

Curated workflow skill generated from `Qwen Image Edit - Replace Product Background.json`.

## Capability Family

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
  - `output_images` (includes image/video entries reported by Comfy history)

## Model Requirements

- `vae`: `qwen_image_vae.safetensors` -> `models/vae`
- `diffusion_model`: `Qwen_Image_Edit-Q8_0.gguf` -> `models/diffusion_models`
- `clip`: `qwen_2.5_vl_7b_fp8_scaled.safetensors` -> `models/clip`
- `lora`: `Qwen-Image-Edit-Lightning-8steps-V1.0.safetensors` -> `models/loras`

## Custom Node Requirements

- `ComfyUI-GGUF`
- `rgthree-comfy`

## Links Extracted From Workflow Notes

- https://blog.comfy.org/p/qwen-image-in-comfyui-new-era-of
- https://discord.com/invite/gggpkVgBf3
- https://github.com/ModelTC/Qwen-Image-Lightning/
- https://huggingface.co/Comfy-Org/Qwen-Image_ComfyUI/resolve/main/split_files/text_encoders/qwen_2.5_vl_7b_fp8_scaled.safetensors
- https://huggingface.co/Comfy-Org/Qwen-Image_ComfyUI/resolve/main/split_files/vae/qwen_image_vae.safetensors
- https://huggingface.co/Comfy-Org/Qwen-Image_ComfyUI/tree/main/split_files/text_encoders
- https://huggingface.co/QuantStack/Qwen-Image-Edit-GGUF
- https://huggingface.co/QuantStack/Qwen-Image-Edit-GGUF/tree/main
- https://huggingface.co/lightx2v/Qwen-Image-Lightning/resolve/main/Qwen-Image-Edit-Lightning-8steps-V1.0.safetensors?download=true
- https://huggingface.co/lightx2v/Qwen-Image-Lightning/tree/main
- https://www.youtube.com/@pixaroma

## Source

- Original: `comfy-data/workflows/Qwen Image Edit - Replace Product Background.json`
