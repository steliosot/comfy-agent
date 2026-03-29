---
name: curated_longcat_img2video_5_to_30s_video_no_subgraphs
description: >
  Curated ComfyUI workflow imported from `LongCat img2video - 5 to 30s Video - No Subgraphs.json`.
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

# curated_longcat_img2video_5_to_30s_video_no_subgraphs

Curated workflow skill generated from `LongCat img2video - 5 to 30s Video - No Subgraphs.json`.

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

- `ComfyUI-WanVideoWrapper`
- `comfyui-kjnodes`
- `comfyui-videohelpersuite`

## Links Extracted From Workflow Notes

- https://discord.com/invite/gggpkVgBf3
- https://huggingface.co/ALGOTECH/WanVideo_comfy/resolve/main/umt5-xxl-enc-bf16.safetensors?download=true
- https://huggingface.co/Comfy-Org/Wan_2.1_ComfyUI_repackaged/resolve/main/split_files/vae/wan_2.1_vae.safetensors?download=true
- https://huggingface.co/Kijai/LongCat-Video_comfy/resolve/main/LongCat_TI2V_comfy_bf16.safetensors?download=true
- https://huggingface.co/Kijai/LongCat-Video_comfy/resolve/main/LongCat_TI2V_comfy_fp8_e4m3fn_scaled_KJ.safetensors?download=true
- https://huggingface.co/Kijai/LongCat-Video_comfy/resolve/main/LongCat_distill_lora_alpha64_bf16.safetensors?download=true
- https://huggingface.co/Kijai/LongCat-Video_comfy/tree/main
- https://www.youtube.com/@pixaroma

## Source

- Original: `comfy-data/workflows/LongCat img2video - 5 to 30s Video - No Subgraphs.json`
