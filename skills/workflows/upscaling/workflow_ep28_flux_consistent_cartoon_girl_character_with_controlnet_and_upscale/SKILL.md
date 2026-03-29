---
name: workflow_ep28_flux_consistent_cartoon_girl_character_with_controlnet_and_upscale
description: >
  Workflow wrapper imported from `Ep28 Flux Consistent Cartoon Girl Character with ControlNet and Upscale.json`.
homepage: https://github.com/steliosot/comfy-agent
metadata.clawdbot.os: ["darwin", "linux"]
metadata.clawdbot.requires.bins: ["python3"]
metadata.clawdbot.requires.env: ["COMFY_URL", "COMFY_AUTH_HEADER"]
metadata.clawdbot.files: ["workflow.json", "skill.py", "skill.yaml", "scripts/*"]
metadata.clawdbot.tags: ["comfyui", "workflow", "library", "upscaling"]
metadata.clawdbot.category: "media-generation"
metadata.clawdbot.input_type: "image/png"
metadata.clawdbot.output_type: "image/png"
metadata.clawdbot.output_can_feed_into: []
metadata.clawdbot.accepts_input_from: []
metadata.clawdbot.priority: 60
---

# workflow_ep28_flux_consistent_cartoon_girl_character_with_controlnet_and_upscale

Imported workflow skill generated from `Ep28 Flux Consistent Cartoon Girl Character with ControlNet and Upscale.json`.

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

- `upscale_model`: `4x_NMKD-Siax_200k.pth` -> `models/upscale_models`
- `vae`: `ae.safetensors` -> `models/vae`
- `controlnet`: `flux-dev-controlnet-union.safetensors` -> `models/controlnet`
- `clip`: `t5-v1_1-xxl-encoder-Q8_0.gguf` -> `models/clip`
- `diffusion_model`: `flux1-dev-Q8_0.gguf` -> `models/diffusion_models`

## Custom Node Requirements

- None detected.

## Links

- None detected.

<!-- AUTO-METADATA-START -->
## Routing Metadata

- Family: `upscaling`
- Input modalities: `image, text_prompt`
- Output modalities: `image/png`
- Model families: `flux, sd3`
- Node count: `27`
- Complexity score: `5`
- Resource profile: `medium`
- Estimated runtime: `moderate (about 30-120s depending on server)`
- Max latent resolution hint: `1024`x`1024`
- Max sampler steps hint: `30`

## Detected Models

- `upscale_model`: `4x_NMKD-Siax_200k.pth` -> `models/upscale_models`
- `vae`: `ae.safetensors` -> `models/vae`
- `controlnet`: `flux-dev-controlnet-union.safetensors` -> `models/controlnet`
- `clip`: `t5-v1_1-xxl-encoder-Q8_0.gguf` -> `models/clip`
- `diffusion_model`: `flux1-dev-Q8_0.gguf` -> `models/diffusion_models`

## Detected Custom Nodes

- None detected.

## Runtime Warnings

- Large model(s) detected; ensure enough VRAM and disk space.
- Medium-high resolution detected; expect moderate extra runtime.
<!-- AUTO-METADATA-END -->

