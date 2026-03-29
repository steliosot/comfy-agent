---
name: workflow_ep11_flux_1_dev_gguf_txt2img_with_florence2_pompt_from_image_workflow_update_v2
description: >
  Workflow wrapper imported from `EP11 Flux 1 Dev GGUF TXT2IMG with Florence2 Pompt from Image Workflow UPDATE V2.json`.
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

# workflow_ep11_flux_1_dev_gguf_txt2img_with_florence2_pompt_from_image_workflow_update_v2

Imported workflow skill generated from `EP11 Flux 1 Dev GGUF TXT2IMG with Florence2 Pompt from Image Workflow UPDATE V2.json`.

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

- `clip`: `t5-v1_1-xxl-encoder-Q8_0.gguf` -> `models/clip`
- `vae`: `ae.safetensors` -> `models/vae`
- `diffusion_model`: `flux1-dev-Q8_0.gguf` -> `models/diffusion_models`

## Custom Node Requirements

- `ComfyUI-GGUF`
- `comfyui-easy-use`
- `rgthree-comfy`

## Links

- None detected.

<!-- AUTO-METADATA-START -->
## Routing Metadata

- Family: `txt2img`
- Input modalities: `image, text_prompt`
- Output modalities: `image/png`
- Model families: `flux, sd3, wan`
- Node count: `19`
- Complexity score: `6`
- Resource profile: `high`
- Estimated runtime: `slow (often 2-6 min depending on model/server load)`
- Max latent resolution hint: `1024`x`1024`
- Max sampler steps hint: `30`

## Detected Models

- `clip`: `t5-v1_1-xxl-encoder-Q8_0.gguf` -> `models/clip`
- `vae`: `ae.safetensors` -> `models/vae`
- `diffusion_model`: `flux1-dev-Q8_0.gguf` -> `models/diffusion_models`

## Detected Custom Nodes

- `ComfyUI-GGUF`
- `comfyui-easy-use`
- `rgthree-comfy`

## Runtime Warnings

- Large model(s) detected; ensure enough VRAM and disk space.
- Medium-high resolution detected; expect moderate extra runtime.
- Uses custom nodes; missing nodes can cause validation/runtime failures.
<!-- AUTO-METADATA-END -->

