---
name: curated_ep15_flux_dev_q8_gguf_txt2img_with_multi_styles
description: >
  Curated ComfyUI workflow imported from `Ep15 Flux Dev Q8 GGUF TXT2IMG with Multi Styles.json`.
homepage: https://github.com/steliosot/comfy-agent
metadata.clawdbot.os: ["darwin", "linux"]
metadata.clawdbot.requires.bins: ["python3"]
metadata.clawdbot.requires.env: ["COMFY_URL", "COMFY_AUTH_HEADER"]
metadata.clawdbot.files: ["workflow.json", "skill.py", "skill.yaml", "scripts/*"]
metadata.clawdbot.tags: ["comfyui", "workflow", "curated", "editing_restyle"]
metadata.clawdbot.category: "media-editing"
metadata.clawdbot.input_type: "text"
metadata.clawdbot.output_type: "image/png"
metadata.clawdbot.output_can_feed_into: []
metadata.clawdbot.accepts_input_from: []
metadata.clawdbot.priority: 70
---

# curated_ep15_flux_dev_q8_gguf_txt2img_with_multi_styles

Curated workflow skill generated from `Ep15 Flux Dev Q8 GGUF TXT2IMG with Multi Styles.json`.

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

- `diffusion_model`: `flux1-dev-Q8_0.gguf` -> `models/diffusion_models`
- `clip`: `t5-v1_1-xxl-encoder-Q8_0.gguf` -> `models/clip`
- `vae`: `ae.safetensors` -> `models/vae`

## Custom Node Requirements

- None detected.

## Links Extracted From Workflow Notes

- None detected.

## Source

- Original: `comfy-data/workflows/Ep15 Flux Dev Q8 GGUF TXT2IMG with Multi Styles.json`

<!-- AUTO-METADATA-START -->
## Routing Metadata

- Family: `editing_restyle`
- Input modalities: `text_prompt`
- Output modalities: `image/png`
- Model families: `flux, sd3`
- Node count: `18`
- Complexity score: `5`
- Resource profile: `medium`
- Estimated runtime: `moderate (about 30-120s depending on server)`
- Max latent resolution hint: `1024`x`1024`
- Max sampler steps hint: `20`

## Detected Models

- `diffusion_model`: `flux1-dev-Q8_0.gguf` -> `models/diffusion_models`
- `clip`: `t5-v1_1-xxl-encoder-Q8_0.gguf` -> `models/clip`
- `vae`: `ae.safetensors` -> `models/vae`

## Detected Custom Nodes

- None detected.

## Runtime Warnings

- Large model(s) detected; ensure enough VRAM and disk space.
- Medium-high resolution detected; expect moderate extra runtime.
<!-- AUTO-METADATA-END -->

