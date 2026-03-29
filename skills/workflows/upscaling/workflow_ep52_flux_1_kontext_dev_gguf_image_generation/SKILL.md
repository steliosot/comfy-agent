---
name: workflow_ep52_flux_1_kontext_dev_gguf_image_generation
description: >
  Workflow wrapper imported from `EP52 Flux 1 Kontext Dev GGUF - Image Generation.json`.
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

# workflow_ep52_flux_1_kontext_dev_gguf_image_generation

Imported workflow skill generated from `EP52 Flux 1 Kontext Dev GGUF - Image Generation.json`.

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

- `vae`: `ae.safetensors` -> `models/vae`
- `upscale_model`: `4x_NMKD-Siax_200k.pth` -> `models/upscale_models`
- `clip`: `clip_l.safetensors` -> `models/clip`
- `diffusion_model`: `flux1-kontext-dev-Q8_0.gguf` -> `models/diffusion_models`

## Custom Node Requirements

- `comfyui-easy-use`
- `comfyui-gguf`

## Links

- https://bfl.ai/models/flux-kontext
- https://discord.com/invite/gggpkVgBf3
- https://docs.comfy.org/tutorials/flux/flux-1-kontext-dev
- https://docs.comfy.org/tutorials/flux/flux-1-kontext-dev#flux-kontext-prompt-techniques
- https://huggingface.co/Akumetsu971/SD_Anime_Futuristic_Armor/resolve/main/4x_NMKD-Siax_200k.pth?download=true
- https://huggingface.co/Comfy-Org/Lumina_Image_2.0_Repackaged/resolve/main/split_files/vae/ae.safetensors?download=true
- https://huggingface.co/QuantStack/FLUX.1-Kontext-dev-GGUF/tree/main
- https://huggingface.co/bullerwins/FLUX.1-Kontext-dev-GGUF/resolve/main/flux1-kontext-dev-Q8_0.gguf?download=true
- https://huggingface.co/bullerwins/FLUX.1-Kontext-dev-GGUF/tree/main
- https://huggingface.co/city96/t5-v1_1-xxl-encoder-gguf/resolve/main/t5-v1_1-xxl-encoder-Q8_0.gguf?download=true
- https://huggingface.co/city96/t5-v1_1-xxl-encoder-gguf/tree/main
- https://huggingface.co/comfyanonymous/flux_text_encoders/resolve/main/clip_l.safetensors?download=true
- https://www.youtube.com/@pixaroma

<!-- AUTO-METADATA-START -->
## Routing Metadata

- Family: `upscaling`
- Input modalities: `text_prompt`
- Output modalities: `image/png`
- Model families: `flux, sd3`
- Node count: `26`
- Complexity score: `5`
- Resource profile: `medium`
- Estimated runtime: `moderate (about 30-120s depending on server)`
- Max latent resolution hint: `1024`x`1024`
- Max sampler steps hint: `20`

## Detected Models

- `vae`: `ae.safetensors` -> `models/vae`
- `upscale_model`: `4x_NMKD-Siax_200k.pth` -> `models/upscale_models`
- `clip`: `clip_l.safetensors` -> `models/clip`
- `diffusion_model`: `flux1-kontext-dev-Q8_0.gguf` -> `models/diffusion_models`

## Detected Custom Nodes

- `comfyui-easy-use`
- `comfyui-gguf`

## Runtime Warnings

- Large model(s) detected; ensure enough VRAM and disk space.
- Medium-high resolution detected; expect moderate extra runtime.
- Uses custom nodes; missing nodes can cause validation/runtime failures.
<!-- AUTO-METADATA-END -->

