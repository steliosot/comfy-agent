---
name: workflow_netayume_v3_5_txt2img_upscaler_2k_landscape
description: >
  Workflow wrapper imported from `NetaYume v3.5 txt2img + Upscaler 2K Landscape.json`.
homepage: https://github.com/steliosot/comfy-agent
metadata.clawdbot.os: ["darwin", "linux"]
metadata.clawdbot.requires.bins: ["python3"]
metadata.clawdbot.requires.env: ["COMFY_URL", "COMFY_AUTH_HEADER"]
metadata.clawdbot.files: ["workflow.json", "skill.py", "skill.yaml", "scripts/*"]
metadata.clawdbot.tags: ["comfyui", "workflow", "library", "upscaling"]
metadata.clawdbot.category: "media-generation"
metadata.clawdbot.input_type: "text"
metadata.clawdbot.output_type: "image/png"
metadata.clawdbot.output_can_feed_into: []
metadata.clawdbot.accepts_input_from: []
metadata.clawdbot.priority: 60
---

# workflow_netayume_v3_5_txt2img_upscaler_2k_landscape

Imported workflow skill generated from `NetaYume v3.5 txt2img + Upscaler 2K Landscape.json`.

## Family

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
  - `output_images`

## Model Requirements

- `checkpoint`: `NetaYumev35_pretrained_all_in_one.safetensors` -> `models/checkpoints`
- `upscale_model`: `4xNomos2_hq_dat2.safetensors` -> `models/upscale_models`

## Custom Node Requirements

- `ComfyUI-TiledDiffusion`
- `comfyui-easy-use`
- `rgthree-comfy`

## Links

- https://discord.com/invite/gggpkVgBf3
- https://huggingface.co/Phips/4xNomos2_hq_dat2
- https://huggingface.co/Phips/4xNomos2_hq_dat2/resolve/main/4xNomos2_hq_dat2.safetensors?download=true
- https://huggingface.co/duongve/NetaYume-Lumina-Image-2.0
- https://huggingface.co/duongve/NetaYume-Lumina-Image-2.0/resolve/main/NetaYumev35_pretrained_all_in_one.safetensors
- https://neta-lumina-style.tz03.xyz/
- https://nieta-art.feishu.cn/wiki/RY3GwpT59icIQlkWXEfcCqIMnQd
- https://www.youtube.com/@pixaroma

<!-- AUTO-METADATA-START -->
## Routing Metadata

- Family: `upscaling`
- Input modalities: `text_prompt`
- Output modalities: `image/png`
- Model families: `sd3`
- Node count: `27`
- Complexity score: `3`
- Resource profile: `medium`
- Estimated runtime: `moderate (about 30-120s depending on server)`
- Max latent resolution hint: `1280`x`720`
- Max sampler steps hint: `30`

## Detected Models

- `checkpoint`: `NetaYumev35_pretrained_all_in_one.safetensors` -> `models/checkpoints`
- `upscale_model`: `4xNomos2_hq_dat2.safetensors` -> `models/upscale_models`

## Detected Custom Nodes

- `ComfyUI-TiledDiffusion`
- `comfyui-easy-use`
- `rgthree-comfy`

## Runtime Warnings

- Medium-high resolution detected; expect moderate extra runtime.
- Uses custom nodes; missing nodes can cause validation/runtime failures.
<!-- AUTO-METADATA-END -->

