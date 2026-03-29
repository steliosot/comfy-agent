---
name: curated_stability_ai_text_to_audio
description: >
  Curated ComfyUI workflow imported from `Stability AI Text To Audio.json`.
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

# curated_stability_ai_text_to_audio

Curated workflow skill generated from `Stability AI Text To Audio.json`.

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

- None detected.

## Links Extracted From Workflow Notes

- https://discord.com/invite/gggpkVgBf3
- https://docs.comfy.org/tutorials/api-nodes/pricing
- https://www.youtube.com/@pixaroma

## Source

- Original: `comfy-data/workflows/Stability AI Text To Audio.json`

<!-- AUTO-METADATA-START -->
## Routing Metadata

- Family: `audio`
- Input modalities: `text_prompt`
- Output modalities: `audio/wav`
- Model families: `other`
- Node count: `4`
- Complexity score: `2`
- Resource profile: `low`
- Estimated runtime: `fast (usually under 30s on modern GPU)`
- Max latent resolution hint: `None`x`None`
- Max sampler steps hint: `None`

## Detected Models

- None detected.

## Detected Custom Nodes

- None detected.

## Runtime Warnings

- Audio generation may take longer on CPU-only or low-VRAM servers.
<!-- AUTO-METADATA-END -->

