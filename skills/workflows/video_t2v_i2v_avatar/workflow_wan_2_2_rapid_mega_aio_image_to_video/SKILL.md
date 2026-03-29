---
name: workflow_wan_2_2_rapid_mega_aio_image_to_video
description: >
  Workflow wrapper imported from `Wan 2.2 Rapid Mega AIO Image to Video.json`.
homepage: https://github.com/steliosot/comfy-agent
metadata.clawdbot.os: ["darwin", "linux"]
metadata.clawdbot.requires.bins: ["python3"]
metadata.clawdbot.requires.env: ["COMFY_URL", "COMFY_AUTH_HEADER"]
metadata.clawdbot.files: ["workflow.json", "skill.py", "skill.yaml", "scripts/*"]
metadata.clawdbot.tags: ["comfyui", "workflow", "library", "video_t2v_i2v_avatar"]
metadata.clawdbot.category: "media-generation"
metadata.clawdbot.input_type: "image/png"
metadata.clawdbot.output_type: "video/mp4"
metadata.clawdbot.output_can_feed_into: []
metadata.clawdbot.accepts_input_from: []
metadata.clawdbot.priority: 60
---

# workflow_wan_2_2_rapid_mega_aio_image_to_video

Imported workflow skill generated from `Wan 2.2 Rapid Mega AIO Image to Video.json`.

## Family

- `video_t2v_i2v_avatar`

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

- `checkpoint`: `wan2.2-rapid-mega-aio-v8.safetensors` -> `models/checkpoints`

## Custom Node Requirements

- `ComfyUI-WanVideoWrapper`
- `comfyui-videohelpersuite`

## Links

- https://discord.com/invite/gggpkVgBf3
- https://huggingface.co/Phr00t/WAN2.2-14B-Rapid-AllInOne/resolve/main/Mega-v8/wan2.2-rapid-mega-aio-v8.safetensors?download=true
- https://huggingface.co/Phr00t/WAN2.2-14B-Rapid-AllInOne/tree/main
- https://huggingface.co/Phr00t/WAN2.2-14B-Rapid-AllInOne/tree/main/Mega-v8
- https://www.youtube.com/@pixaroma

<!-- AUTO-METADATA-START -->
## Routing Metadata

- Family: `video_t2v_i2v_avatar`
- Input modalities: `image, text_prompt`
- Output modalities: `video/mp4`
- Model families: `sd3, wan`
- Node count: `16`
- Complexity score: `5`
- Resource profile: `medium`
- Estimated runtime: `moderate (about 30-120s depending on server)`
- Max latent resolution hint: `None`x`None`
- Max sampler steps hint: `4`

## Detected Models

- `checkpoint`: `wan2.2-rapid-mega-aio-v8.safetensors` -> `models/checkpoints`

## Detected Custom Nodes

- `ComfyUI-WanVideoWrapper`
- `comfyui-videohelpersuite`

## Runtime Warnings

- Uses custom nodes; missing nodes can cause validation/runtime failures.
- Video workflow: usually slower and VRAM-intensive than still-image workflows.
<!-- AUTO-METADATA-END -->

