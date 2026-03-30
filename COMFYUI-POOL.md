# ComfyUI Pool Setup (Localhost + comfy-gate)

This guide shows how to run a local ComfyUI server, expose it with [`comfy-gate`](https://github.com/steliosot/comfy-gate), and register it in `.comfy_servers.yaml` for multi-server routing.

## 1) Start ComfyUI locally

Run ComfyUI so it is available on `http://localhost:8000`.

Quick check:

```bash
curl -s http://localhost:8000/object_info | head
```

If that returns JSON, ComfyUI is reachable.

## 2) Start comfy-gate (local proxy)

In your `comfy-gate` project:

```bash
python3 comfy_expose.py
```

Expected output (example):

```text
Starting Comfy Proxy...
Local: http://localhost:8000
Proxy: http://localhost:9000
...
Uvicorn running on http://0.0.0.0:9000
```

This means:
- ComfyUI upstream: `localhost:8000`
- Protected proxy endpoint: `localhost:9000`

## 3) Configure public URL and API key

From your running setup:

- Public URL: `https://mandate-citizens-urls-cocktail.trycloudflare.com`
- API key: `NKak1S2LqOWw98zvyygUpY33GQV540g_`

Store the key in env (recommended):

```bash
export COMFY_CLOUDA_KEY='NKak1S2LqOWw98zvyygUpY33GQV540g_'
```

## 4) Create/edit `.comfy_servers.yaml`

Use this pattern in your repo root:

```yaml
default_server: clouda

servers:
  # Direct local ComfyUI (no gateway auth)
  local_direct:
    url: http://localhost:8000
    api_prefix: /api
    manager_api_prefix: /manager
    resources:
      gpu_vram_gb: 32
      max_parallel_jobs: 2
      tier: local

  # Local comfy-gate proxy endpoint
  local_gate:
    url: http://localhost:9000
    headers:
      X-API-Key: ${COMFY_CLOUDA_KEY}
    api_prefix: /api
    manager_api_prefix: /manager
    resources:
      gpu_vram_gb: 32
      max_parallel_jobs: 2
      tier: local-gateway

  # Public endpoint (Cloudflare tunnel)
  clouda:
    url: https://mandate-citizens-urls-cocktail.trycloudflare.com
    headers:
      X-API-Key: ${COMFY_CLOUDA_KEY}
    api_prefix: /api
    manager_api_prefix: /manager
    resources:
      gpu_vram_gb: 32
      max_parallel_jobs: 2
      tier: public
      region: eu
```

Notes:
- `X-API-Key` is required for this comfy-gate setup (not `Authorization: Bearer ...`).
- `resources` is optional metadata for your own routing decisions; unknown keys are safe to keep.
- Keep `.comfy_servers.yaml` local and gitignored.

## 5) Verify with skill-based selection

```bash
COMFY_CLOUDA_KEY="$COMFY_CLOUDA_KEY" \
PYTHONPATH=. ./venv/bin/python skills/infra/select_comfy_server/scripts/run.py \
  --args '{"server_name":"clouda","require_ready":true}' --pretty
```

Expected:
- `status: "ok"`
- `ready: true`
- resolved `server/headers/api_prefix`

## 6) Use selected server explicitly per run

Pattern:
1. Call `select_comfy_server`
2. Pass returned `server`, `headers`, `api_prefix` into workflow/agentic skill runs

Example:

```bash
COMFY_CLOUDA_KEY="$COMFY_CLOUDA_KEY" COMFY_SERVER_NAME=clouda \
PYTHONPATH=. ./venv/bin/python examples/agents_agentic/example_agentic_select_server_then_execute.py
```

## 7) Resource thresholds for preflight checks

If you want automatic blockers/warnings in `assess_server_resources` / `prepare_workflow_dependencies`, set:

```bash
export COMFY_RESOURCE_MIN_FREE_VRAM_MB=12000
export COMFY_RESOURCE_MIN_FREE_STORAGE_GB=20
```

These are global thresholds. The per-server `resources:` block in YAML is for your own policy/routing logic.
