---
name: curated_ep46_juggernaut_xl_ragnarok_txt2img_with_upscaler
description: >
  Curated ComfyUI workflow imported from `EP46 Juggernaut XL Ragnarok TXT2IMG with Upscaler.json`.
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

# curated_ep46_juggernaut_xl_ragnarok_txt2img_with_upscaler

Curated workflow skill generated from `EP46 Juggernaut XL Ragnarok TXT2IMG with Upscaler.json`.

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

- `upscale_model`: `4x_NMKD-Siax_200k.pth` -> `models/upscale_models`
- `checkpoint`: `juggernautXL_ragnarokBy.safetensors` -> `models/checkpoints`

## Custom Node Requirements

- `ComfyUI-TiledDiffusion`
- `comfyui-easy-use`
- `controlaltai-nodes`

## Links Extracted From Workflow Notes

- https://civitai.com/api/download/models/1759168?type=Model&format=SafeTensor&size=full&fp=fp16
- https://civitai.com/models/133005?modelVersionId=1759168
- https://discord.com/invite/gggpkVgBf3
- https://huggingface.co/Akumetsu971/SD_Anime_Futuristic_Armor/resolve/main/4x_NMKD-Siax_200k.pth?download=true
- https://www.youtube.com/@pixaroma

## Source

- Original: `comfy-data/workflows/EP46 Juggernaut XL Ragnarok TXT2IMG with Upscaler.json`

<!-- AUTO-METADATA-START -->
## Routing Metadata

- Family: `upscaling`
- Input modalities: `text_prompt`
- Output modalities: `image/png`
- Model families: `flux, sd3, wan`
- Node count: `29`
- Complexity score: `3`
- Resource profile: `medium`
- Estimated runtime: `moderate (about 30-120s depending on server)`
- Max latent resolution hint: `1024`x`1024`
- Max sampler steps hint: `30`

## Detected Models

- `upscale_model`: `4x_NMKD-Siax_200k.pth` -> `models/upscale_models`
- `checkpoint`: `juggernautXL_ragnarokBy.safetensors` -> `models/checkpoints`

## Detected Custom Nodes

- `ComfyUI-TiledDiffusion`
- `comfyui-easy-use`
- `controlaltai-nodes`

## Runtime Warnings

- Medium-high resolution detected; expect moderate extra runtime.
- Uses custom nodes; missing nodes can cause validation/runtime failures.
<!-- AUTO-METADATA-END -->

