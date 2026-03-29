---
name: curated_netayume_v3_5_txt2img_upscaler
description: >
  Curated ComfyUI workflow imported from `NetaYume v3.5 txt2img + Upscaler.json`.
homepage: https://github.com/steliosot/comfy-agent
metadata.clawdbot.os: ["darwin", "linux"]
metadata.clawdbot.requires.bins: ["python3"]
metadata.clawdbot.requires.env: ["COMFY_URL", "COMFY_AUTH_HEADER"]
metadata.clawdbot.files: ["workflow.json", "skill.py", "skill.yaml", "scripts/*"]
metadata.clawdbot.tags: ["comfyui", "workflow", "curated", "upscaling"]
metadata.clawdbot.category: "media-editing"
metadata.clawdbot.input_type: "text"
metadata.clawdbot.output_type: "image/png"
metadata.clawdbot.output_can_feed_into: []
metadata.clawdbot.accepts_input_from: []
metadata.clawdbot.priority: 70
---

# curated_netayume_v3_5_txt2img_upscaler

Curated workflow skill generated from `NetaYume v3.5 txt2img + Upscaler.json`.

## Capability Family

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
  - `output_images` (includes image/video entries reported by Comfy history)

## Model Requirements

- `checkpoint`: `NetaYumev35_pretrained_all_in_one.safetensors` -> `models/checkpoints`
- `upscale_model`: `4xNomos2_hq_dat2.safetensors` -> `models/upscale_models`

## Custom Node Requirements

- `ComfyUI-TiledDiffusion`
- `comfyui-easy-use`
- `controlaltai-nodes`
- `rgthree-comfy`

## Links Extracted From Workflow Notes

- https://discord.com/invite/gggpkVgBf3
- https://huggingface.co/Phips/4xNomos2_hq_dat2
- https://huggingface.co/Phips/4xNomos2_hq_dat2/resolve/main/4xNomos2_hq_dat2.safetensors?download=true
- https://huggingface.co/duongve/NetaYume-Lumina-Image-2.0
- https://huggingface.co/duongve/NetaYume-Lumina-Image-2.0/resolve/main/NetaYumev35_pretrained_all_in_one.safetensors
- https://neta-lumina-style.tz03.xyz/
- https://nieta-art.feishu.cn/wiki/RY3GwpT59icIQlkWXEfcCqIMnQd
- https://www.youtube.com/@pixaroma

## Source

- Original: `comfy-data/workflows/NetaYume v3.5 txt2img + Upscaler.json`

<!-- AUTO-METADATA-START -->
## Routing Metadata

- Family: `upscaling`
- Input modalities: `text_prompt`
- Output modalities: `image/png`
- Model families: `flux, sd3, wan`
- Node count: `29`
- Complexity score: `4`
- Resource profile: `medium`
- Estimated runtime: `moderate (about 30-120s depending on server)`
- Max latent resolution hint: `1024`x`1024`
- Max sampler steps hint: `30`

## Detected Models

- `checkpoint`: `NetaYumev35_pretrained_all_in_one.safetensors` -> `models/checkpoints`
- `upscale_model`: `4xNomos2_hq_dat2.safetensors` -> `models/upscale_models`

## Detected Custom Nodes

- `ComfyUI-TiledDiffusion`
- `comfyui-easy-use`
- `controlaltai-nodes`
- `rgthree-comfy`

## Runtime Warnings

- Medium-high resolution detected; expect moderate extra runtime.
- Multiple custom nodes required; verify node installation/version compatibility.
<!-- AUTO-METADATA-END -->

