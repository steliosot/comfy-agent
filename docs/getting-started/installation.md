# Installation

## Requirements

- Python `>=3.10`
- A running ComfyUI server
- Optional: comfy-gate/API key if your server is behind auth

## Install

### Option A: from GitHub

```bash
pip install git+https://github.com/steliosot/comfy-agent.git
```

### Option B: local development

```bash
git clone https://github.com/steliosot/comfy-agent.git
cd comfy-agent
python3 -m venv venv
source venv/bin/activate
pip install -e .
```

## Basic environment

```bash
export COMFY_URL=http://127.0.0.1:8000
# optional if needed by your gateway
export COMFY_AUTH_HEADER=
```

## Verify server

```bash
PYTHONPATH=. python3 skills/infra/get_server_status/scripts/run.py --args '{}' --pretty
```

If this succeeds, continue to [Quickstart (Skills)](quickstart-skills.md).
