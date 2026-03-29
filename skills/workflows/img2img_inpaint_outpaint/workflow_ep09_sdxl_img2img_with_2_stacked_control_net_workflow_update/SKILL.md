---
name: workflow_ep09_sdxl_img2img_with_2_stacked_control_net_workflow_update
description: >
  Workflow wrapper imported from `EP09 SDXL IMG2IMG With 2 Stacked Control Net Workflow Update.json`.
homepage: https://github.com/steliosot/comfy-agent
metadata.clawdbot.os: ["darwin", "linux"]
metadata.clawdbot.requires.bins: ["python3"]
metadata.clawdbot.requires.env: ["COMFY_URL", "COMFY_AUTH_HEADER"]
metadata.clawdbot.files: ["workflow.json", "skill.py", "skill.yaml", "scripts/*"]
metadata.clawdbot.tags: ["comfyui", "workflow", "library", "img2img_inpaint_outpaint"]
metadata.clawdbot.category: "media-generation"
metadata.clawdbot.input_type: "image/png"
metadata.clawdbot.output_type: "image/png"
metadata.clawdbot.output_can_feed_into: []
metadata.clawdbot.accepts_input_from: []
metadata.clawdbot.priority: 60
---

# workflow_ep09_sdxl_img2img_with_2_stacked_control_net_workflow_update

Imported workflow skill generated from `EP09 SDXL IMG2IMG With 2 Stacked Control Net Workflow Update.json`.

## Family

- `img2img_inpaint_outpaint`

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

- `checkpoint`: `Juggernaut_X_RunDiffusion.safetensors` -> `models/checkpoints`

## Custom Node Requirements

- None detected.

## Links

- None detected.

<!-- AUTO-METADATA-START -->
## Routing Metadata

- Family: `img2img_inpaint_outpaint`
- Input modalities: `image, text_prompt`
- Output modalities: `image/png`
- Model families: `other`
- Node count: `14`
- Complexity score: `0`
- Resource profile: `low`
- Estimated runtime: `fast (usually under 30s on modern GPU)`
- Max latent resolution hint: `None`x`None`
- Max sampler steps hint: `30`

## Detected Models

- `checkpoint`: `Juggernaut_X_RunDiffusion.safetensors` -> `models/checkpoints`

## Detected Custom Nodes

- None detected.

## Runtime Warnings

- No major runtime warnings detected.
<!-- AUTO-METADATA-END -->

