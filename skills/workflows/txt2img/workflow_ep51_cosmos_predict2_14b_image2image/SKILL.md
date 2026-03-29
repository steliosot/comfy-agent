---
name: workflow_ep51_cosmos_predict2_14b_image2image
description: >
  Workflow wrapper imported from `EP51 Cosmos Predict2 14B Image2Image.json`.
homepage: https://github.com/steliosot/comfy-agent
metadata.clawdbot.os: ["darwin", "linux"]
metadata.clawdbot.requires.bins: ["python3"]
metadata.clawdbot.requires.env: ["COMFY_URL", "COMFY_AUTH_HEADER"]
metadata.clawdbot.files: ["workflow.json", "skill.py", "skill.yaml", "scripts/*"]
metadata.clawdbot.tags: ["comfyui", "workflow", "library", "txt2img"]
metadata.clawdbot.category: "media-generation"
metadata.clawdbot.input_type: "image/png"
metadata.clawdbot.output_type: "image/png"
metadata.clawdbot.output_can_feed_into: []
metadata.clawdbot.accepts_input_from: []
metadata.clawdbot.priority: 60
---

# workflow_ep51_cosmos_predict2_14b_image2image

Imported workflow skill generated from `EP51 Cosmos Predict2 14B Image2Image.json`.

## Family

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
  - `output_images`

## Model Requirements

- `clip`: `oldt5_xxl_fp8_e4m3fn_scaled.safetensors` -> `models/clip`
- `diffusion_model`: `cosmos-predict2-14b-t2i-ex3-q8_0.gguf` -> `models/diffusion_models`
- `vae`: `wan_2.1_vae.safetensors` -> `models/vae`

## Custom Node Requirements

- `comfyui-easy-use`
- `comfyui-gguf`

## Links

- https://discord.com/invite/gggpkVgBf3
- https://huggingface.co/Comfy-Org/Wan_2.1_ComfyUI_repackaged/resolve/main/split_files/vae/wan_2.1_vae.safetensors
- https://huggingface.co/calcuis/cosmos-predict2-gguf/resolve/main/cosmos-predict2-14b-t2i-ex3-q4_0.gguf?download=true
- https://huggingface.co/calcuis/cosmos-predict2-gguf/resolve/main/cosmos-predict2-14b-t2i-ex3-q8_0.gguf?download=true
- https://huggingface.co/calcuis/cosmos-predict2-gguf/tree/main
- https://huggingface.co/comfyanonymous/cosmos_1.0_text_encoder_and_VAE_ComfyUI/resolve/main/text_encoders/oldt5_xxl_fp8_e4m3fn_scaled.safetensors
- https://www.youtube.com/@pixaroma

<!-- AUTO-METADATA-START -->
## Routing Metadata

- Family: `txt2img`
- Input modalities: `image, text_prompt`
- Output modalities: `image/png`
- Model families: `wan`
- Node count: `12`
- Complexity score: `4`
- Resource profile: `medium`
- Estimated runtime: `moderate (about 30-120s depending on server)`
- Max latent resolution hint: `None`x`None`
- Max sampler steps hint: `35`

## Detected Models

- `clip`: `oldt5_xxl_fp8_e4m3fn_scaled.safetensors` -> `models/clip`
- `diffusion_model`: `cosmos-predict2-14b-t2i-ex3-q8_0.gguf` -> `models/diffusion_models`
- `vae`: `wan_2.1_vae.safetensors` -> `models/vae`

## Detected Custom Nodes

- `comfyui-easy-use`
- `comfyui-gguf`

## Runtime Warnings

- Large model(s) detected; ensure enough VRAM and disk space.
- Uses custom nodes; missing nodes can cause validation/runtime failures.
<!-- AUTO-METADATA-END -->

