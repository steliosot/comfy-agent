---
name: curated_hidream_i1_fast_q8_gguf_text2image
description: >
  Curated ComfyUI workflow imported from `HiDream i1 Fast Q8 GGUF text2image.json`.
homepage: https://github.com/steliosot/comfy-agent
metadata.clawdbot.os: ["darwin", "linux"]
metadata.clawdbot.requires.bins: ["python3"]
metadata.clawdbot.requires.env: ["COMFY_URL", "COMFY_AUTH_HEADER"]
metadata.clawdbot.files: ["workflow.json", "skill.py", "skill.yaml", "scripts/*"]
metadata.clawdbot.tags: ["comfyui", "workflow", "curated", "txt2img"]
metadata.clawdbot.category: "media-generation"
metadata.clawdbot.input_type: "text"
metadata.clawdbot.output_type: "image/png"
metadata.clawdbot.output_can_feed_into: []
metadata.clawdbot.accepts_input_from: []
metadata.clawdbot.priority: 70
---

# curated_hidream_i1_fast_q8_gguf_text2image

Curated workflow skill generated from `HiDream i1 Fast Q8 GGUF text2image.json`.

## Capability Family

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
  - `output_images` (includes image/video entries reported by Comfy history)

## Model Requirements

- `vae`: `ae.safetensors` -> `models/vae`
- `diffusion_model`: `hidream-i1-fast-Q8_0.gguf` -> `models/diffusion_models`

## Custom Node Requirements

- `comfyui-gguf`

## Links Extracted From Workflow Notes

- https://blog.comfy.org/p/hidream-i1-native-support-in-comfyui
- https://comfyanonymous.github.io/ComfyUI_examples/hidream/
- https://discord.com/invite/gggpkVgBf3
- https://docs.comfy.org/tutorials/advanced/hidream
- https://huggingface.co/Comfy-Org/HiDream-I1_ComfyUI/resolve/main/split_files/text_encoders/clip_g_hidream.safetensors?download=true
- https://huggingface.co/Comfy-Org/HiDream-I1_ComfyUI/resolve/main/split_files/text_encoders/clip_l_hidream.safetensors?download=true
- https://huggingface.co/Comfy-Org/HiDream-I1_ComfyUI/resolve/main/split_files/text_encoders/llama_3.1_8b_instruct_fp8_scaled.safetensors?download=true
- https://huggingface.co/Comfy-Org/HiDream-I1_ComfyUI/resolve/main/split_files/text_encoders/t5xxl_fp8_e4m3fn_scaled.safetensors?download=true
- https://huggingface.co/Comfy-Org/HiDream-I1_ComfyUI/resolve/main/split_files/vae/ae.safetensors?download=true
- https://huggingface.co/Comfy-Org/HiDream-I1_ComfyUI/tree/main/split_files/text_encoders
- https://huggingface.co/city96/HiDream-I1-Fast-gguf/resolve/main/hidream-i1-fast-Q8_0.gguf?download=true
- https://huggingface.co/city96/HiDream-I1-Fast-gguf/tree/main
- https://www.youtube.com/@pixaroma

## Source

- Original: `comfy-data/workflows/HiDream i1 Fast Q8 GGUF text2image.json`

<!-- AUTO-METADATA-START -->
## Routing Metadata

- Family: `txt2img`
- Input modalities: `text_prompt`
- Output modalities: `image/png`
- Model families: `sd3`
- Node count: `11`
- Complexity score: `5`
- Resource profile: `medium`
- Estimated runtime: `moderate (about 30-120s depending on server)`
- Max latent resolution hint: `1024`x`1024`
- Max sampler steps hint: `16`

## Detected Models

- `vae`: `ae.safetensors` -> `models/vae`
- `diffusion_model`: `hidream-i1-fast-Q8_0.gguf` -> `models/diffusion_models`

## Detected Custom Nodes

- `comfyui-gguf`

## Runtime Warnings

- Large model(s) detected; ensure enough VRAM and disk space.
- Medium-high resolution detected; expect moderate extra runtime.
- Uses custom nodes; missing nodes can cause validation/runtime failures.
<!-- AUTO-METADATA-END -->

