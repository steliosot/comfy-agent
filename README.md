# comfy-agent

A Python toolkit for running ComfyUI through reusable **skills**, workflow builders, and lightweight agentic planning/execution.

This repository is organized around practical automation:
- infra skills (server selection, health, dependencies, upload/download, cleanup)
- workflow skills (txt2img, img2img, video, upscaling, audio)
- examples for direct, fluent, and agentic usage

## Repository Layout

- `comfy_agent/` core library (`Workflow`, monitoring, config, agentic helpers)
- `skills/infra/` operational skills
- `skills/workflows/` generation/editing workflow skills
- `examples/` runnable examples grouped by pattern
- `unit_tests/` test suite
- `documentation.md` deeper API/usage documentation
- `COMFYUI-POOL.md` localhost + comfy-gate + multi-server setup

## Installation

### Option A: Use from GitHub

```bash
pip install git+https://github.com/steliosot/comfy-agent.git
```

### Option B: Local Development

```bash
git clone https://github.com/steliosot/comfy-agent.git
cd comfy-agent
python3 -m venv venv
source venv/bin/activate
pip install -e .
```

Requirements:
- Python `>=3.10`
- Running ComfyUI server

## Quickstart (Single Server)

1. Point to your ComfyUI server.

```bash
export COMFY_URL=http://127.0.0.1:8000
# optional auth if your gateway requires it
export COMFY_AUTH_HEADER=
```

2. Check server status.

```bash
PYTHONPATH=. python3 skills/infra/get_server_status/scripts/run.py --args '{}' --pretty
```

3. Run a simple txt2img skill.

```bash
PYTHONPATH=. python3 skills/workflows/txt2img/generate_sd15_image/scripts/run.py \
  --args '{"prompt":"cinematic product photo of a coffee mug"}' --pretty
```

4. Download output image(s) using prompt id.

```bash
PYTHONPATH=. python3 skills/infra/download_image/scripts/run.py \
  --args '{"prompt_id":"<PROMPT_ID>","run_id":"quickstart"}' --pretty
```

## Quickstart (Multi Server via YAML)

Create `.comfy_servers.yaml` (or set `COMFY_SERVERS_FILE`):

```yaml
default_server: clouda
servers:
  local:
    url: http://localhost:8000
    api_prefix: /api
    manager_api_prefix: /manager
  clouda:
    url: https://your-public-url.example
    headers:
      X-API-Key: ${COMFY_CLOUDA_KEY}
    api_prefix: /api
    manager_api_prefix: /manager
```

Then resolve a server explicitly:

```bash
export COMFY_SERVERS_FILE=.comfy_servers.yaml
export COMFY_CLOUDA_KEY=YOUR_KEY

PYTHONPATH=. python3 skills/infra/select_comfy_server/scripts/run.py \
  --args '{"server_name":"clouda","require_ready":true}' --pretty
```

Use the returned `server`, `headers`, and `api_prefix` per run.

## Skills Overview

### Infra Skills (`skills/infra/`)

Core operations include:
- `select_comfy_server`
- `get_server_status`, `get_queue_status`, `get_progress`
- `prepare_workflow_dependencies`, `assess_server_resources`
- `download_model`, `install_custom_node`, `remove_model`
- `upload_image`, `download_image`, `upload_video`, `download_video`
- `delete_image_job`, `delete_video_job`
- `agentic_plan`, `agentic_execute`

Examples:

```bash
# Dependency preflight (warn only)
PYTHONPATH=. python3 skills/infra/prepare_workflow_dependencies/scripts/run.py \
  --args '{"required_models":[{"name":"sd1.5/juggernaut_reborn.safetensors","model_type":"checkpoint"}],"warn_only":true}' --pretty

# Upload an input image
PYTHONPATH=. python3 skills/infra/upload_image/scripts/run.py \
  --args '{"image_path":"tmp/inputs/example.png","run_id":"demo"}' --pretty
```

### Workflow Skills (`skills/workflows/`)

Families:
- `txt2img`
- `img2img_inpaint_outpaint`
- `video_t2v_i2v_avatar`
- `upscaling`
- `editing_restyle`
- `audio`

Run any skill via its `scripts/run.py` with JSON `--args`.

## Agentic Usage

Agentic examples live in `examples/agents_agentic/`.

Start here:
- `example_agentic_plan_then_execute.py`
- `example_agentic_select_server_then_execute.py` (server selection first)
- `example_agentic_slash_commands.py`

Run:

```bash
PYTHONPATH=. python3 examples/agents_agentic/example_agentic_select_server_then_execute.py
```

## Development

Run targeted tests:

```bash
./venv/bin/python -m unittest unit_tests.test_config unit_tests.test_monitoring_skills
```

Run all tests:

```bash
./venv/bin/python -m unittest
```

## Notes

- Keep `.comfy_servers.yaml` local (already gitignored).
- If using comfy-gate, prefer `X-API-Key` header.
- For full setup docs, see [documentation.md](documentation.md) and [COMFYUI-POOL.md](COMFYUI-POOL.md).

## License

MIT. See [LICENSE](LICENSE).
