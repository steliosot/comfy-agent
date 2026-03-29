---
name: workflow_sonic_talking_avatar_portrait_576x1024px
description: >
  Workflow wrapper imported from `Sonic Talking Avatar Portrait 576x1024px.json`.
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

# workflow_sonic_talking_avatar_portrait_576x1024px

Imported workflow skill generated from `Sonic Talking Avatar Portrait 576x1024px.json`.

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

- None detected from loader nodes.

## Custom Node Requirements

- `comfyui-easy-use`
- `comfyui-videohelpersuite`
- `pr-was-node-suite-comfyui-47064894`

## Links

- https://discord.com/invite/gggpkVgBf3
- https://drive.google.com/drive/folders/1QIIDvCDU-rp1ZB8qDA6NQqVn8F9WYMhE
- https://drive.google.com/drive/folders/1jI32B-2JX17seSGG0-MnZgUhCMHCEZlx
- https://drive.google.com/drive/folders/1oe8VTPUy0-MHHW2a_NJ1F8xL-0VN5G7W
- https://github.com/smthemex/ComfyUI_Sonic
- https://huggingface.co/openai/whisper-tiny/tree/main
- https://huggingface.co/stabilityai/stable-video-diffusion-img2vid-xt-1-1/tree/main
- https://huggingface.co/stabilityai/stable-video-diffusion-img2vid-xt/tree/main
- https://www.youtube.com/@pixaroma

<!-- AUTO-METADATA-START -->
## Routing Metadata

- Family: `video_t2v_i2v_avatar`
- Input modalities: `audio, image`
- Output modalities: `image/png, video/mp4`
- Model families: `other`
- Node count: `13`
- Complexity score: `7`
- Resource profile: `high`
- Estimated runtime: `slow (often 2-6 min depending on model/server load)`
- Max latent resolution hint: `None`x`None`
- Max sampler steps hint: `None`

## Detected Models

- None detected.

## Detected Custom Nodes

- `comfyui-easy-use`
- `comfyui-videohelpersuite`
- `pr-was-node-suite-comfyui-47064894`

## Runtime Warnings

- Audio generation may take longer on CPU-only or low-VRAM servers.
- Uses custom nodes; missing nodes can cause validation/runtime failures.
- Video workflow: usually slower and VRAM-intensive than still-image workflows.
<!-- AUTO-METADATA-END -->

