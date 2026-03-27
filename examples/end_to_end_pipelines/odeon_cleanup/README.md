# Odeon Compose + Cleanup Pipeline

This example demonstrates composition plus server cleanup in one run:

1. Upload `woman.png` and `odeon-athens-greece.avif`
2. Generate one composed still image
3. Download that still image locally
4. Generate one video from the still
5. Download the video locally
6. Delete both Comfy history jobs from the server (image + video)
7. Write results to `log.md`

## Script

- `example_odeon_compose_and_cleanup.py`

This script directly composes single-purpose skills:

- `upload_image`
- `generate_flux_multi_input_img2img`
- `download_image`
- `generate_ltxv_img2video`
- `download_video`
- `delete_image_job`
- `delete_video_job`

## Inputs

From `.env`:

- `COMFY_INPUT_DIR/woman.png`
- `COMFY_INPUT_DIR/odeon-athens-greece.avif`

## Outputs

From `.env` output directory (`COMFY_OUTPUT_DIR`):

- downloaded still image
- downloaded video

In this folder:

- `log.md` with run ID, prompt IDs, output paths, cleanup status, and total duration

## Run

```bash
PYTHONPATH=. python3 examples/end_to_end_pipelines/odeon_cleanup/example_odeon_compose_and_cleanup.py
```

