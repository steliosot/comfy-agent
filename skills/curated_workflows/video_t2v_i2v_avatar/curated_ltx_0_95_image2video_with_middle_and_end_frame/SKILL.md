---
name: curated_ltx_0_95_image2video_with_middle_and_end_frame
description: >
  Curated ComfyUI workflow imported from `LTX 0.95 image2video with Middle and End Frame.json`.
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

# curated_ltx_0_95_image2video_with_middle_and_end_frame

Curated workflow skill generated from `LTX 0.95 image2video with Middle and End Frame.json`.

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

- `clip`: `t5xxl_fp16.safetensors` -> `models/clip`
- `checkpoint`: `ltx-video-2b-v0.9.5.safetensors` -> `models/checkpoints`

## Custom Node Requirements

- `comfyui-videohelpersuite`

## Links Extracted From Workflow Notes

- https://blog.comfy.org/p/ltx-video-095-day-1-support-in-comfyui
- https://discord.com/invite/gggpkVgBf3
- https://huggingface.co/Comfy-Org/mochi_preview_repackaged/resolve/main/split_files/text_encoders/t5xxl_fp16.safetensors?download=true
- https://huggingface.co/Comfy-Org/mochi_preview_repackaged/resolve/main/split_files/text_encoders/t5xxl_fp8_e4m3fn_scaled.safetensors?download=true
- https://huggingface.co/Lightricks/LTX-Video/resolve/main/ltx-video-2b-v0.9.5.safetensors?download=true
- https://www.youtube.com/@pixaroma

## Source

- Original: `comfy-data/workflows/LTX 0.95 image2video with Middle and End Frame.json`
