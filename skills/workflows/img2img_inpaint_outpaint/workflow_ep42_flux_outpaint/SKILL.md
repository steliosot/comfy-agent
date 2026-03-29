---
name: workflow_ep42_flux_outpaint
description: >
  Workflow wrapper imported from `EP42 FLUX OUTPAINT.json`.
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

# workflow_ep42_flux_outpaint

Imported workflow skill generated from `EP42 FLUX OUTPAINT.json`.

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

- `vae`: `ae.safetensors` -> `models/vae`
- `clip`: `t5-v1_1-xxl-encoder-Q8_0.gguf` -> `models/clip`
- `diffusion_model`: `flux1-fill-dev-Q8_0.gguf` -> `models/diffusion_models`

## Custom Node Requirements

- `comfyui-easy-use`
- `comfyui-gguf`
- `comfyui-inpaint-cropandstitch`

## Links

- https://civitai.com/api/download/models/1377767?type=Model&format=SafeTensor&size=full&fp=fp32
- https://discord.com/invite/gggpkVgBf3
- https://huggingface.co/YarvixPA/FLUX.1-Fill-dev-gguf/resolve/main/flux1-fill-dev-Q8_0.gguf?download=true
- https://huggingface.co/YarvixPA/FLUX.1-Fill-dev-gguf/tree/main
- https://huggingface.co/black-forest-labs/FLUX.1-schnell/resolve/main/ae.safetensors?download=true
- https://huggingface.co/city96/t5-v1_1-xxl-encoder-gguf/resolve/main/t5-v1_1-xxl-encoder-Q8_0.gguf?download=true
- https://huggingface.co/city96/t5-v1_1-xxl-encoder-gguf/tree/main
- https://www.youtube.com/@pixaroma

<!-- AUTO-METADATA-START -->
## Routing Metadata

- Family: `img2img_inpaint_outpaint`
- Input modalities: `image, text_prompt`
- Output modalities: `image/png`
- Model families: `flux`
- Node count: `17`
- Complexity score: `4`
- Resource profile: `medium`
- Estimated runtime: `moderate (about 30-120s depending on server)`
- Max latent resolution hint: `None`x`None`
- Max sampler steps hint: `30`

## Detected Models

- `vae`: `ae.safetensors` -> `models/vae`
- `clip`: `t5-v1_1-xxl-encoder-Q8_0.gguf` -> `models/clip`
- `diffusion_model`: `flux1-fill-dev-Q8_0.gguf` -> `models/diffusion_models`

## Detected Custom Nodes

- `comfyui-easy-use`
- `comfyui-gguf`
- `comfyui-inpaint-cropandstitch`

## Runtime Warnings

- Large model(s) detected; ensure enough VRAM and disk space.
- Uses custom nodes; missing nodes can cause validation/runtime failures.
<!-- AUTO-METADATA-END -->

