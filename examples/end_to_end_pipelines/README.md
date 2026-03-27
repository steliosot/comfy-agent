# End-to-End Pipelines

This folder is organized by pipeline:

- `birkbeck_basic/`
  - `example_birkbeck_image_to_video.py`
  - `log.md`
- `birkbeck_monitored/`
  - `example_birkbeck_monitored_pipeline.py`
  - `log.md`
- `odeon_cleanup/`
  - `example_odeon_compose_and_cleanup.py`
  - `log.md`
- `common/`
  - shared pipeline helpers (`pipeline_lib.py`)

## Run

```bash
PYTHONPATH=. python3 examples/end_to_end_pipelines/birkbeck_basic/example_birkbeck_image_to_video.py
PYTHONPATH=. python3 examples/end_to_end_pipelines/birkbeck_monitored/example_birkbeck_monitored_pipeline.py
PYTHONPATH=. python3 examples/end_to_end_pipelines/odeon_cleanup/example_odeon_compose_and_cleanup.py
```

All scripts use `.env` (`COMFY_URL`, `COMFY_AUTH_HEADER`, `COMFY_INPUT_DIR`, `COMFY_OUTPUT_DIR`) and keep their outputs/logs within their own subfolder.
