---
name: workflow_ltxv_13b_0_9_7_fp8_i2v_square_704x704px_to_1408x1408px
description: >
  Workflow wrapper imported from `LTXV 13b 0.9.7-FP8 i2v Square 704x704px to 1408x1408px.json`.
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

# workflow_ltxv_13b_0_9_7_fp8_i2v_square_704x704px_to_1408x1408px

Imported workflow skill generated from `LTXV 13b 0.9.7-FP8 i2v Square 704x704px to 1408x1408px.json`.

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

- `clip`: `t5xxl_fp16.safetensors` -> `models/clip`
- `checkpoint`: `ltxv-13b-0.9.7-distilled-fp8.safetensors` -> `models/checkpoints`

## Custom Node Requirements

- `ComfyUI-LTXVideo`
- `comfyui-easy-use`
- `comfyui-kjnodes`
- `comfyui-videohelpersuite`

## Links

- https://discord.com/invite/gggpkVgBf3
- https://github.com/Lightricks/ComfyUI-LTXVideo/
- https://huggingface.co/Comfy-Org/mochi_preview_repackaged/resolve/main/split_files/text_encoders/t5xxl_fp16.safetensors?download=true
- https://huggingface.co/Comfy-Org/mochi_preview_repackaged/resolve/main/split_files/text_encoders/t5xxl_fp8_e4m3fn_scaled.safetensors?download=true
- https://huggingface.co/Lightricks/LTX-Video
- https://huggingface.co/Lightricks/LTX-Video/resolve/main/ltxv-13b-0.9.7-distilled-fp8.safetensors?download=true
- https://huggingface.co/Lightricks/LTX-Video/tree/main
- https://www.youtube.com/@pixaroma

<!-- AUTO-METADATA-START -->
## Routing Metadata

- Family: `video_t2v_i2v_avatar`
- Input modalities: `image, text_prompt`
- Output modalities: `video/mp4`
- Model families: `ltx`
- Node count: `34`
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

