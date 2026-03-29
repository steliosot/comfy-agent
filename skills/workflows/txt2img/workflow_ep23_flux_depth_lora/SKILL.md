---
name: workflow_ep23_flux_depth_lora
description: >
  Workflow wrapper imported from `EP23 Flux Depth Lora.json`.
homepage: https://github.com/steliosot/comfy-agent
metadata.clawdbot.os: ["darwin", "linux"]
metadata.clawdbot.requires.bins: ["python3"]
metadata.clawdbot.requires.env: ["COMFY_URL", "COMFY_AUTH_HEADER"]
metadata.clawdbot.files: ["workflow.json", "skill.py", "skill.yaml", "scripts/*"]
metadata.clawdbot.tags: ["comfyui", "workflow", "library", "txt2img"]
metadata.clawdbot.category: "media-generation"
metadata.clawdbot.input_type: "image/png"
metadata.clawdbot.output_type: "image/png"
metadata.clawdbot.output_can_feed_into: []
metadata.clawdbot.accepts_input_from: []
metadata.clawdbot.priority: 60
---

# workflow_ep23_flux_depth_lora

Imported workflow skill generated from `EP23 Flux Depth Lora.json`.

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
- `clip`: `clip_l.safetensors` -> `models/clip`
- `vae`: `ae.safetensors` -> `models/vae`

## Custom Node Requirements

- None detected.

## Links

- None detected.

<!-- AUTO-METADATA-START -->
## Routing Metadata

- Family: `txt2img`
- Input modalities: `image, text_prompt`
- Output modalities: `image/png`
- Model families: `flux`
- Node count: `14`
- Complexity score: `2`
- Resource profile: `low`
- Estimated runtime: `fast (usually under 30s on modern GPU)`
- Max latent resolution hint: `None`x`None`
- Max sampler steps hint: `30`

## Detected Models

- `diffusion_model`: `flux1-dev-Q8_0.gguf` -> `models/diffusion_models`
- `clip`: `clip_l.safetensors` -> `models/clip`
- `vae`: `ae.safetensors` -> `models/vae`

## Detected Custom Nodes

- None detected.

## Runtime Warnings

- Large model(s) detected; ensure enough VRAM and disk space.
<!-- AUTO-METADATA-END -->

