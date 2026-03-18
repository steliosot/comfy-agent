# Cloud Server Workflow Examples

These examples are for ComfyUI deployed behind Nginx or another reverse proxy.

They demonstrate:

- plain local connection (no headers)
- cloud connection with optional auth headers

If your server is proxied under `/api`, `Workflow(...)` now auto-detects that path.

## Run

```bash
PYTHONPATH=. python3 workflow_examples_cloud_server/example_local_crop.py
PYTHONPATH=. python3 workflow_examples_cloud_server/example_cloud_crop_with_headers.py
PYTHONPATH=. python3 workflow_examples_cloud_server/example_cloud_sd15_txt2img_preview.py
```

## Cloud env vars

```bash
export COMFY_URL=http://34.30.216.121
export COMFY_AUTH_HEADER="XXXXXX"
export COMFY_INPUT_IMAGE="rosie.jpg"
```

`COMFY_INPUT_IMAGE` must exist in the remote ComfyUI `input/` folder.
