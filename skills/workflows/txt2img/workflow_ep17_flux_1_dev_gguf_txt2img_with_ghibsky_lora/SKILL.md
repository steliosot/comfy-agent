---
name: workflow_ep17_flux_1_dev_gguf_txt2img_with_ghibsky_lora
description: >
  Workflow wrapper imported from `EP17 Flux 1 Dev GGUF TXT2IMG with Ghibsky Lora.json`.
homepage: https://github.com/steliosot/comfy-agent
metadata.clawdbot.os: ["darwin", "linux"]
metadata.clawdbot.requires.bins: ["python3"]
metadata.clawdbot.requires.env: ["COMFY_URL", "COMFY_AUTH_HEADER"]
metadata.clawdbot.files: ["workflow.json", "skill.py", "skill.yaml", "scripts/*"]
metadata.clawdbot.tags: ["comfyui", "workflow", "library", "txt2img"]
metadata.clawdbot.category: "media-generation"
metadata.clawdbot.input_type: "text"
metadata.clawdbot.output_type: "image/png"
metadata.clawdbot.output_can_feed_into: []
metadata.clawdbot.accepts_input_from: []
metadata.clawdbot.priority: 60
---

# workflow_ep17_flux_1_dev_gguf_txt2img_with_ghibsky_lora

Imported workflow skill generated from `EP17 Flux 1 Dev GGUF TXT2IMG with Ghibsky Lora.json`.

## Family

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
  - `output_images`

## Model Requirements

- `diffusion_model`: `flux1-dev-Q8_0.gguf` -> `models/diffusion_models`
- `clip`: `t5-v1_1-xxl-encoder-Q8_0.gguf` -> `models/clip`
- `vae`: `ae.safetensors` -> `models/vae`

## Custom Node Requirements

- None detected.

## Links

- None detected.

<!-- AUTO-METADATA-START -->
## Routing Metadata

- Family: `txt2img`
- Input modalities: `text_prompt`
- Output modalities: `image/png`
- Model families: `flux, sd3`
- Node count: `11`
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

