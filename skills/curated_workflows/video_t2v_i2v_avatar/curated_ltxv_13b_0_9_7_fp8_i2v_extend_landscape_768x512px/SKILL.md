---
name: curated_ltxv_13b_0_9_7_fp8_i2v_extend_landscape_768x512px
description: >
  Curated ComfyUI workflow imported from `LTXV 13b 0.9.7-FP8 i2v EXTEND Landscape 768x512px.json`.
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

# curated_ltxv_13b_0_9_7_fp8_i2v_extend_landscape_768x512px

Curated workflow skill generated from `LTXV 13b 0.9.7-FP8 i2v EXTEND Landscape 768x512px.json`.

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
- `checkpoint`: `ltxv-13b-0.9.7-distilled-fp8.safetensors` -> `models/checkpoints`

## Custom Node Requirements

- `ComfyUI-LTXVideo`
- `comfyui-easy-use`
- `comfyui-kjnodes`
- `comfyui-videohelpersuite`

## Links Extracted From Workflow Notes

- https://discord.com/invite/gggpkVgBf3
- https://github.com/Lightricks/ComfyUI-LTXVideo/
- https://huggingface.co/Comfy-Org/mochi_preview_repackaged/resolve/main/split_files/text_encoders/t5xxl_fp16.safetensors?download=true
- https://huggingface.co/Comfy-Org/mochi_preview_repackaged/resolve/main/split_files/text_encoders/t5xxl_fp8_e4m3fn_scaled.safetensors?download=true
- https://huggingface.co/Lightricks/LTX-Video
- https://huggingface.co/Lightricks/LTX-Video/resolve/main/ltxv-13b-0.9.7-distilled-fp8.safetensors?download=true
- https://huggingface.co/Lightricks/LTX-Video/tree/main
- https://www.youtube.com/@pixaroma

## Source

- Original: `comfy-data/workflows/LTXV 13b 0.9.7-FP8 i2v EXTEND Landscape 768x512px.json`
