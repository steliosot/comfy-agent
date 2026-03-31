# comfy-agent Docs

`comfy-agent` is a skill-first Python toolkit for ComfyUI workflows.

It is designed to make image/video/audio generation easy to start, while still supporting advanced agentic orchestration, server routing, and optimization tuning.

## Quick Actions

- [Install in 2 minutes](getting-started/installation.md)
- [Run your first skill](getting-started/quickstart-skills.md)
- [Run with Python DSL](getting-started/quickstart-python-dsl.md)

## 3-Step First Image

1. Install + set `COMFY_URL`.
2. Run `generate_sd15_image`.
3. Download output by `prompt_id`.

```bash
export COMFY_URL=http://127.0.0.1:8000
PYTHONPATH=. python3 skills/workflows/txt2img/generate_sd15_image/scripts/run.py \
  --args '{"prompt":"cinematic product photo of a coffee mug"}' --pretty
```

## What You’ll Find Here

- **Get Started**: fastest paths for skills, Python DSL, and agentic usage.
- **Guides**: server setup, multi-server routing, optimizations, benchmarks.
- **Workflows**: practical library by modality.
- **Skills**: infra and workflow catalogs.
- **Reference**: API and config details.
- **Troubleshooting**: common setup/runtime fixes.
