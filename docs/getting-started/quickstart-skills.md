# Quickstart (Skills)

This page prioritizes copy-paste commands.

## Prerequisites

- Installed `comfy-agent`
- `COMFY_URL` points to a live ComfyUI server
- Running from repository root

## 1) Txt2Img (first image)

```bash
PYTHONPATH=. python3 skills/workflows/txt2img/generate_sd15_image/scripts/run.py \
  --args '{"prompt":"cinematic product photo of a coffee mug"}' --pretty
```

Expected output: JSON containing a `prompt_id`.

## 2) Download image

```bash
PYTHONPATH=. python3 skills/infra/download_image/scripts/run.py \
  --args '{"prompt_id":"<PROMPT_ID>","run_id":"quickstart_txt2img"}' --pretty
```

Expected output: downloaded file paths under `tmp/outputs/...`.

## 3) Img2Img remix

```bash
PYTHONPATH=. python3 skills/workflows/img2img_inpaint_outpaint/generate_sd15_img2img_remix/scripts/run.py \
  --args '{"image_path":"tmp/inputs/example.png","prompt":"high detail cinematic remix"}' --pretty
```

Expected output: new image prompt id and output file.

## 4) Video clip

```bash
PYTHONPATH=. python3 skills/workflows/video_t2v_i2v_avatar/generate_video_clip/scripts/run.py \
  --args '{"prompt":"a cinematic drone shot over mountains at sunset"}' --pretty
```

Expected output: video prompt id and downloadable video artifact.

## 5) Audio generation

```bash
PYTHONPATH=. python3 skills/workflows/audio/curated_ep47_acestep_v1_3_5b_text_to_music_lyrics/scripts/run.py \
  --args '{"prompt":"hello there I am Stelios, warm orchestral intro"}' --pretty
```

Expected output: audio prompt id and `.wav` output metadata.

## 6) Upscale image

```bash
PYTHONPATH=. python3 skills/workflows/upscaling/workflow_simple_upscale_with_model/scripts/run.py \
  --args '{"image_path":"tmp/inputs/example.png"}' --pretty
```

Expected output: upscaled image output metadata.

## Quick failures and fixes

- `connection refused`: check `COMFY_URL` and ComfyUI process.
- `missing model`: run dependency prep (`prepare_workflow_dependencies`) first.
- `validation failed`: install required custom nodes/models for that workflow.
