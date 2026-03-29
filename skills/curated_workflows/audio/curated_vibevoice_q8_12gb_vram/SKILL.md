---
name: curated_vibevoice_q8_12gb_vram
description: >
  Curated ComfyUI workflow imported from `VibeVoice Q8 - 12GB VRAM.json`.
homepage: https://github.com/steliosot/comfy-agent
metadata.clawdbot.os: ["darwin", "linux"]
metadata.clawdbot.requires.bins: ["python3"]
metadata.clawdbot.requires.env: ["COMFY_URL", "COMFY_AUTH_HEADER"]
metadata.clawdbot.files: ["workflow.json", "skill.py", "skill.yaml", "scripts/*"]
metadata.clawdbot.tags: ["comfyui", "workflow", "curated", "audio"]
metadata.clawdbot.category: "media-generation"
metadata.clawdbot.input_type: "text"
metadata.clawdbot.output_type: "audio/wav"
metadata.clawdbot.output_can_feed_into: []
metadata.clawdbot.accepts_input_from: []
metadata.clawdbot.priority: 70
---

# curated_vibevoice_q8_12gb_vram

Curated workflow skill generated from `VibeVoice Q8 - 12GB VRAM.json`.

## Capability Family

- `audio`

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

- `vibevoice-comfyui`

## Links Extracted From Workflow Notes

- https://discord.com/invite/gggpkVgBf3
- https://github.com/Enemyx-net/VibeVoice-ComfyUI
- https://huggingface.co/FabioSarracino/VibeVoice-Large-Q8/tree/main
- https://huggingface.co/Qwen/Qwen2.5-1.5B/tree/main
- https://www.youtube.com/@pixaroma

## Source

- Original: `comfy-data/workflows/VibeVoice Q8 - 12GB VRAM.json`
