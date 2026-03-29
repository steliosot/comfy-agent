---
name: workflow_05_z_image_turbo_txt2img_aio_fp8_or_bf16_lora
description: >
  Workflow wrapper imported from `05-Z Image Turbo txt2img AIO FP8 or BF16 + Lora.json`.
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

# workflow_05_z_image_turbo_txt2img_aio_fp8_or_bf16_lora

Imported workflow skill generated from `05-Z Image Turbo txt2img AIO FP8 or BF16 + Lora.json`.

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

- `checkpoint`: `z-image-turbo-fp8-aio.safetensors` -> `models/checkpoints`
- `lora`: `pixag1rlwh1t3.safetensors` -> `models/loras`

## Custom Node Requirements

- None detected.

## Links

- https://discord.com/invite/gggpkVgBf3
- https://huggingface.co/Pixaroma/experimental_loras/resolve/main/pixag1rlwh1t3.safetensors?download=true
- https://huggingface.co/SeeSee21/Z-Image-Turbo-AIO
- https://huggingface.co/SeeSee21/Z-Image-Turbo-AIO/resolve/main/z-image-turbo-bf16-aio.safetensors?download=true
- https://huggingface.co/SeeSee21/Z-Image-Turbo-AIO/resolve/main/z-image-turbo-fp8-aio.safetensors?download=true
- https://www.youtube.com/@pixaroma

<!-- AUTO-METADATA-START -->
## Routing Metadata

- Family: `txt2img`
- Input modalities: `text_prompt`
- Output modalities: `image/png`
- Model families: `sd3`
- Node count: `11`
- Complexity score: `2`
- Resource profile: `low`
- Estimated runtime: `fast (usually under 30s on modern GPU)`
- Max latent resolution hint: `1024`x`1024`
- Max sampler steps hint: `5`

## Detected Models

- `checkpoint`: `z-image-turbo-fp8-aio.safetensors` -> `models/checkpoints`
- `lora`: `pixag1rlwh1t3.safetensors` -> `models/loras`

## Detected Custom Nodes

- None detected.

## Runtime Warnings

- Medium-high resolution detected; expect moderate extra runtime.
<!-- AUTO-METADATA-END -->

