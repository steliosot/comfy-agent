# Birkbeck Monitored Pipeline

This example runs the same image-to-video flow as the basic pipeline, with monitoring included:

1. Check server status
2. Upload `woman.png` and `bbk.jpg`
3. Submit still-image generation
4. Poll progress/queue until complete
5. Download still
6. Submit video generation
7. Poll progress/queue until complete
8. Download video
9. Write rich monitoring/timing log

## Script

- `example_birkbeck_monitored_pipeline.py`

It calls `run_monitored(...)` from `examples/end_to_end_pipelines/common/pipeline_lib.py`.

## Inputs

From `.env`:

- `COMFY_INPUT_DIR/woman.png`
- `COMFY_INPUT_DIR/bbk.jpg`

## Outputs

From `.env` output directory (`COMFY_OUTPUT_DIR`):

- downloaded still image
- downloaded video

In this folder:

- `log.md` with status snapshots, progress snapshots, prompt IDs, and timings

## Run

```bash
PYTHONPATH=. python3 examples/end_to_end_pipelines/birkbeck_monitored/example_birkbeck_monitored_pipeline.py
```

## Notes

- If `/progress` is not available on your Comfy server, progress uses queue/history fallback logic.

