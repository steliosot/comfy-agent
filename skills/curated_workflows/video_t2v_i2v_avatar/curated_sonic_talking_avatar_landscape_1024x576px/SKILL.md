---
name: curated_sonic_talking_avatar_landscape_1024x576px
description: >
  Curated ComfyUI workflow imported from `Sonic Talking Avatar Landscape 1024x576px.json`.
homepage: https://github.com/steliosot/comfy-agent
metadata.clawdbot.os: ["darwin", "linux"]
metadata.clawdbot.requires.bins: ["python3"]
metadata.clawdbot.requires.env: ["COMFY_URL", "COMFY_AUTH_HEADER"]
metadata.clawdbot.files: ["workflow.json", "skill.py", "skill.yaml", "scripts/*"]
metadata.clawdbot.tags: ["comfyui", "workflow", "curated", "video_t2v_i2v_avatar"]
metadata.clawdbot.category: "media-generation"
metadata.clawdbot.input_type: "image/png"
metadata.clawdbot.output_type: "video/mp4"
metadata.clawdbot.output_can_feed_into: []
metadata.clawdbot.accepts_input_from: []
metadata.clawdbot.priority: 70
---

# curated_sonic_talking_avatar_landscape_1024x576px

Curated workflow skill generated from `Sonic Talking Avatar Landscape 1024x576px.json`.

## Capability Family

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
  - `output_images` (includes image/video entries reported by Comfy history)

## Model Requirements

- None detected from loader nodes.

## Custom Node Requirements

- `comfyui-easy-use`
- `comfyui-videohelpersuite`
- `pr-was-node-suite-comfyui-47064894`

## Links Extracted From Workflow Notes

- https://discord.com/invite/gggpkVgBf3
- https://drive.google.com/drive/folders/1QIIDvCDU-rp1ZB8qDA6NQqVn8F9WYMhE
- https://drive.google.com/drive/folders/1jI32B-2JX17seSGG0-MnZgUhCMHCEZlx
- https://drive.google.com/drive/folders/1oe8VTPUy0-MHHW2a_NJ1F8xL-0VN5G7W
- https://github.com/smthemex/ComfyUI_Sonic
- https://huggingface.co/openai/whisper-tiny/tree/main
- https://huggingface.co/stabilityai/stable-video-diffusion-img2vid-xt-1-1/tree/main
- https://huggingface.co/stabilityai/stable-video-diffusion-img2vid-xt/tree/main
- https://www.youtube.com/@pixaroma

## Source

- Original: `comfy-data/workflows/Sonic Talking Avatar Landscape 1024x576px.json`
