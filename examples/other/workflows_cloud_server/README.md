# Cloud Server Workflow Examples

These examples are for ComfyUI deployed behind Nginx or another reverse proxy.

They demonstrate:

- plain local connection (no headers)
- cloud connection with optional auth headers

If your server is proxied under `/api`, `Workflow(...)` now auto-detects that path.

## Run

```bash
PYTHONPATH=. python3 examples/other/workflows_cloud_server/example_local_crop.py
PYTHONPATH=. python3 examples/other/workflows_cloud_server/example_cloud_crop_with_headers.py
PYTHONPATH=. python3 examples/other/workflows_cloud_server/example_cloud_sd15_txt2img_preview.py
PYTHONPATH=. python3 examples/other/workflows_cloud_server/example_cloud_wan21_video_clip.py
```

`example_cloud_wan21_video_clip.py` exports `video/h264-mp4` (`pix_fmt=yuv420p`, `crf=19`).

## Cloud env vars

```bash
export COMFY_URL=http://34.27.83.101
export COMFY_AUTH_HEADER="YOUR_AUTH_KEY"
export COMFY_INPUT_IMAGE="rosie.jpg"
export COMFY_CKPT="sd1.5/juggernaut_reborn.safetensors"
```

`COMFY_INPUT_IMAGE` must exist in the remote ComfyUI `input/` folder.
