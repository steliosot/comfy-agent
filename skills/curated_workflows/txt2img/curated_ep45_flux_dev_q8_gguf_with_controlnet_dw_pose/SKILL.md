---
name: curated_ep45_flux_dev_q8_gguf_with_controlnet_dw_pose
description: >
  Curated ComfyUI workflow imported from `Ep45 Flux Dev Q8 GGUF with ControlNet DW Pose.json`.
homepage: https://github.com/steliosot/comfy-agent
metadata.clawdbot.os: ["darwin", "linux"]
metadata.clawdbot.requires.bins: ["python3"]
metadata.clawdbot.requires.env: ["COMFY_URL", "COMFY_AUTH_HEADER"]
metadata.clawdbot.files: ["workflow.json", "skill.py", "skill.yaml", "scripts/*"]
metadata.clawdbot.tags: ["comfyui", "workflow", "curated", "txt2img"]
metadata.clawdbot.category: "media-generation"
metadata.clawdbot.input_type: "image/png"
metadata.clawdbot.output_type: "image/png"
metadata.clawdbot.output_can_feed_into: []
metadata.clawdbot.accepts_input_from: []
metadata.clawdbot.priority: 70
---

# curated_ep45_flux_dev_q8_gguf_with_controlnet_dw_pose

Curated workflow skill generated from `Ep45 Flux Dev Q8 GGUF with ControlNet DW Pose.json`.

## Capability Family

- `txt2img`

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

- `diffusion_model`: `flux1-dev-Q8_0.gguf` -> `models/diffusion_models`
- `vae`: `ae.safetensors` -> `models/vae`
- `controlnet`: `flux-cn-pro-2.safetensors` -> `models/controlnet`
- `clip`: `t5-v1_1-xxl-encoder-Q8_0.gguf` -> `models/clip`

## Custom Node Requirements

- `comfyui-gguf`
- `comfyui_controlnet_aux`
- `kaytool`

## Links Extracted From Workflow Notes

- https://discord.com/invite/gggpkVgBf3
- https://huggingface.co/Shakker-Labs/FLUX.1-dev-ControlNet-Union-Pro-2.0
- https://huggingface.co/Shakker-Labs/FLUX.1-dev-ControlNet-Union-Pro-2.0/resolve/main/diffusion_pytorch_model.safetensors?download=true
- https://huggingface.co/black-forest-labs/FLUX.1-schnell
- https://huggingface.co/black-forest-labs/FLUX.1-schnell/resolve/main/ae.safetensors?download=true
- https://huggingface.co/city96/FLUX.1-dev-gguf/resolve/main/flux1-dev-Q8_0.gguf?download=true
- https://huggingface.co/city96/FLUX.1-dev-gguf/tree/main
- https://huggingface.co/city96/t5-v1_1-xxl-encoder-gguf/resolve/main/t5-v1_1-xxl-encoder-Q8_0.gguf?download=true
- https://huggingface.co/city96/t5-v1_1-xxl-encoder-gguf/tree/main
- https://huggingface.co/comfyanonymous/flux_text_encoders/resolve/main/clip_l.safetensors?download=true
- https://www.youtube.com/@pixaroma

## Source

- Original: `comfy-data/workflows/Ep45 Flux Dev Q8 GGUF with ControlNet DW Pose.json`
