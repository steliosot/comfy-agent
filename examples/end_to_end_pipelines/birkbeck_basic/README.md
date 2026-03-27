# Birkbeck Basic Pipeline

This example runs a simple end-to-end chain with minimal code:

1. Upload `woman.png` and `bbk.jpg`
2. Generate one still image (woman at Birkbeck)
3. Download the still locally
4. Generate one video from that still
5. Download the video locally
6. Write timing/results to `log.md`

## Script

- `example_birkbeck_image_to_video.py`

It calls `run_basic(...)` from `examples/end_to_end_pipelines/common/pipeline_lib.py`.

## Inputs

From `.env`:

- `COMFY_INPUT_DIR/woman.png`
- `COMFY_INPUT_DIR/bbk.jpg`

## Outputs

From `.env` output directory (`COMFY_OUTPUT_DIR`):

- downloaded still image
- downloaded video

In this folder:

- `log.md` with run ID, prompt IDs, file paths, and timing breakdown

## Run

```bash
PYTHONPATH=. python3 examples/end_to_end_pipelines/birkbeck_basic/example_birkbeck_image_to_video.py
```

