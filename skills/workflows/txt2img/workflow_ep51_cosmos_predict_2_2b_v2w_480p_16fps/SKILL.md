---
name: workflow_ep51_cosmos_predict_2_2b_v2w_480p_16fps
description: >
  Workflow wrapper imported from `EP51 Cosmos Predict 2 2B v2w 480p 16fps.json`.
homepage: https://github.com/steliosot/comfy-agent
metadata.clawdbot.os: ["darwin", "linux"]
metadata.clawdbot.requires.bins: ["python3"]
metadata.clawdbot.requires.env: ["COMFY_URL", "COMFY_AUTH_HEADER"]
metadata.clawdbot.files: ["workflow.json", "skill.py", "skill.yaml", "scripts/*"]
metadata.clawdbot.tags: ["comfyui", "workflow", "library", "txt2img"]
metadata.clawdbot.category: "media-generation"
metadata.clawdbot.input_type: "image/png"
metadata.clawdbot.output_type: "video/mp4"
metadata.clawdbot.output_can_feed_into: []
metadata.clawdbot.accepts_input_from: []
metadata.clawdbot.priority: 60
---

# workflow_ep51_cosmos_predict_2_2b_v2w_480p_16fps

Imported workflow skill generated from `EP51 Cosmos Predict 2 2B v2w 480p 16fps.json`.

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

- `diffusion_model`: `cosmos_predict2_2B_video2world_480p_16fps.safetensors` -> `models/diffusion_models`
- `clip`: `oldt5_xxl_fp8_e4m3fn_scaled.safetensors` -> `models/clip`
- `vae`: `wan_2.1_vae.safetensors` -> `models/vae`

## Custom Node Requirements

- None detected.

## Links

- https://discord.com/invite/gggpkVgBf3
- https://huggingface.co/Comfy-Org/Cosmos_Predict2_repackaged/resolve/main/cosmos_predict2_2B_video2world_480p_16fps.safetensors?download=true
- https://huggingface.co/Comfy-Org/Cosmos_Predict2_repackaged/tree/main
- https://huggingface.co/Comfy-Org/Wan_2.1_ComfyUI_repackaged/resolve/main/split_files/vae/wan_2.1_vae.safetensors
- https://huggingface.co/comfyanonymous/cosmos_1.0_text_encoder_and_VAE_ComfyUI/resolve/main/text_encoders/oldt5_xxl_fp8_e4m3fn_scaled.safetensors
- https://www.youtube.com/@pixaroma

<!-- AUTO-METADATA-START -->
## Routing Metadata

- Family: `txt2img`
- Input modalities: `image, text_prompt`
- Output modalities: `video/mp4`
- Model families: `wan`
- Node count: `13`
- Complexity score: `2`
- Resource profile: `low`
- Estimated runtime: `fast (usually under 30s on modern GPU)`
- Max latent resolution hint: `None`x`None`
- Max sampler steps hint: `35`

## Detected Models

- `diffusion_model`: `cosmos_predict2_2B_video2world_480p_16fps.safetensors` -> `models/diffusion_models`
- `clip`: `oldt5_xxl_fp8_e4m3fn_scaled.safetensors` -> `models/clip`
- `vae`: `wan_2.1_vae.safetensors` -> `models/vae`

## Detected Custom Nodes

- None detected.

## Runtime Warnings

- Large model(s) detected; ensure enough VRAM and disk space.
<!-- AUTO-METADATA-END -->

