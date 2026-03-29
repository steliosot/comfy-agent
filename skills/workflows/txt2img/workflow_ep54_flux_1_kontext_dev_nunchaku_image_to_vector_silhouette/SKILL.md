---
name: workflow_ep54_flux_1_kontext_dev_nunchaku_image_to_vector_silhouette
description: >
  Workflow wrapper imported from `EP54 Flux 1 Kontext Dev (Nunchaku) - Image to Vector Silhouette.json`.
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

# workflow_ep54_flux_1_kontext_dev_nunchaku_image_to_vector_silhouette

Imported workflow skill generated from `EP54 Flux 1 Kontext Dev (Nunchaku) - Image to Vector Silhouette.json`.

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

- `vae`: `ae.safetensors` -> `models/vae`

## Custom Node Requirements

- `ComfyUI-nunchaku`
- `comfyui-tosvg`
- `rgthree-comfy`

## Links

- https://bfl.ai/models/flux-kontext
- https://discord.com/invite/gggpkVgBf3
- https://docs.comfy.org/tutorials/flux/flux-1-kontext-dev
- https://docs.comfy.org/tutorials/flux/flux-1-kontext-dev#flux-kontext-prompt-techniques
- https://github.com/Tavris1/ComfyUI-Easy-Install/tree/Windows-Nunchaku
- https://github.com/Yanick112/ComfyUI-ToSVG
- https://github.com/mit-han-lab/ComfyUI-nunchaku
- https://huggingface.co/Comfy-Org/Lumina_Image_2.0_Repackaged/resolve/main/split_files/vae/ae.safetensors?download=true
- https://huggingface.co/Pixaroma/flux-kontext-loras/resolve/main/vector_silhouette.safetensors?download=true
- https://huggingface.co/comfyanonymous/flux_text_encoders/resolve/main/clip_l.safetensors?download=true
- https://huggingface.co/mit-han-lab/nunchaku-flux.1-kontext-dev/resolve/main/svdq-int4_r32-flux.1-kontext-dev.safetensors?download=true
- https://huggingface.co/mit-han-lab/nunchaku-flux.1-kontext-dev/tree/main
- https://huggingface.co/mit-han-lab/nunchaku-t5/resolve/main/awq-int4-flux.1-t5xxl.safetensors?download=true
- https://www.youtube.com/@pixaroma

<!-- AUTO-METADATA-START -->
## Routing Metadata

- Family: `txt2img`
- Input modalities: `image, text_prompt`
- Output modalities: `image/png`
- Model families: `flux`
- Node count: `28`
- Complexity score: `1`
- Resource profile: `low`
- Estimated runtime: `fast (usually under 30s on modern GPU)`
- Max latent resolution hint: `None`x`None`
- Max sampler steps hint: `20`

## Detected Models

- `vae`: `ae.safetensors` -> `models/vae`

## Detected Custom Nodes

- `ComfyUI-nunchaku`
- `comfyui-tosvg`
- `rgthree-comfy`

## Runtime Warnings

- Uses custom nodes; missing nodes can cause validation/runtime failures.
<!-- AUTO-METADATA-END -->

