---
name: curated_ep47_acestep_v1_3_5b_text_to_music_lyrics
description: >
  Curated ComfyUI workflow imported from `EP47 AceStep V1 3.5b text to music - Lyrics.json`.
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

# curated_ep47_acestep_v1_3_5b_text_to_music_lyrics

Curated workflow skill generated from `EP47 AceStep V1 3.5b text to music - Lyrics.json`.

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

- `checkpoint`: `ace_step_v1_3.5b.safetensors` -> `models/checkpoints`

## Custom Node Requirements

- None detected.

## Links Extracted From Workflow Notes

- https://discord.com/invite/gggpkVgBf3
- https://docs.comfy.org/tutorials/audio/ace-step/ace-step-v1
- https://docs.comfy.org/tutorials/audio/ace-step/ace-step-v1#multilingual-support
- https://github.com/ace-step/ACE-Step
- https://huggingface.co/ACE-Step/ACE-Step-v1-3.5B
- https://huggingface.co/Comfy-Org/ACE-Step_ComfyUI_repackaged/resolve/main/all_in_one/ace_step_v1_3.5b.safetensors?download=true
- https://www.youtube.com/@pixaroma

## Source

- Original: `comfy-data/workflows/EP47 AceStep V1 3.5b text to music - Lyrics.json`
