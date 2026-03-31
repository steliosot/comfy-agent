# Server Setup

## Localhost (ComfyUI)

```bash
export COMFY_URL=http://127.0.0.1:8000
```

Health check:

```bash
PYTHONPATH=. python3 skills/infra/get_server_status/scripts/run.py --args '{}' --pretty
```

## Cloud/comfy-gate setup

If your server is exposed via a gateway:

```bash
export COMFY_URL=https://your-public-comfy-url.example
export COMFY_AUTH_HEADER='{"X-API-Key":"YOUR_KEY"}'
```

Then run the same health check.

## Dependency preflight

```bash
PYTHONPATH=. python3 skills/infra/prepare_workflow_dependencies/scripts/run.py \
  --args '{"required_models":[{"name":"sd1.5/juggernaut_reborn.safetensors","model_type":"checkpoint"}],"warn_only":true}' --pretty
```

Use this before heavy workflows to avoid late failures.
