---
name: curated_ltxv_13b_0_9_7_fp8_i2v_2frames_landscape_768x512px_to_1536x1024px
description: >
  Curated ComfyUI workflow imported from `LTXV 13b 0.9.7-FP8 i2v 2Frames - Landscape 768x512px to 1536x1024px.json`.
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

# curated_ltxv_13b_0_9_7_fp8_i2v_2frames_landscape_768x512px_to_1536x1024px

Curated workflow skill generated from `LTXV 13b 0.9.7-FP8 i2v 2Frames - Landscape 768x512px to 1536x1024px.json`.

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

- Original: `comfy-data/workflows/LTXV 13b 0.9.7-FP8 i2v 2Frames - Landscape 768x512px to 1536x1024px.json`

<!-- AUTO-METADATA-START -->
## Routing Metadata

- Family: `video_t2v_i2v_avatar`
- Input modalities: `image, text_prompt`
- Output modalities: `video/mp4`
- Model families: `ltx`
- Node count: `38`
- Complexity score: `9`
- Resource profile: `very_high`
- Estimated runtime: `heavy (can exceed 6 min; best on high-VRAM GPU)`
- Max latent resolution hint: `None`x`None`
- Max sampler steps hint: `None`

## Detected Models

- `clip`: `t5xxl_fp16.safetensors` -> `models/clip`
- `checkpoint`: `ltxv-13b-0.9.7-distilled-fp8.safetensors` -> `models/checkpoints`

## Detected Custom Nodes

- `ComfyUI-LTXVideo`
- `comfyui-easy-use`
- `comfyui-kjnodes`
- `comfyui-videohelpersuite`

## Runtime Warnings

- Large model(s) detected; ensure enough VRAM and disk space.
- Multiple custom nodes required; verify node installation/version compatibility.
- Video workflow: usually slower and VRAM-intensive than still-image workflows.
<!-- AUTO-METADATA-END -->

