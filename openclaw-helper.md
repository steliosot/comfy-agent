# OpenClaw Helper Guide

This guide explains how to use this repository as a skill-driven ComfyUI automation toolkit.

It covers:

- environment setup
- skill packaging format
- running skills directly
- composing end-to-end pipelines
- monitoring progress / queue / status
- cleanup helpers
- troubleshooting

## 1) Prerequisites

- Python `3.10+`
- A reachable ComfyUI server (local or remote)
- Required models/nodes installed on ComfyUI side

Install project dependencies:

```bash
cd /Users/stelios/Documents/comfy-agent
pip install -r requirements.txt
```

For local editable development:

```bash
pip install -e .
```

## 2) Environment Configuration

Create `.env` from example:

```bash
cp .env.example .env
```

Typical remote config:

```env
COMFY_URL=http://34.27.83.101
COMFY_API_PREFIX=/api
COMFY_AUTH_HEADER=YOUR_AUTH_KEY
COMFY_INPUT_DIR=tmp/inputs
COMFY_OUTPUT_DIR=tmp/outputs
```

Notes:

- `COMFY_API_PREFIX` is usually `/api` for proxied deployments.
- `COMFY_INPUT_DIR` and `COMFY_OUTPUT_DIR` are local folders used by scripts.
- Skills load `.env` automatically through `ComfyConfig.from_env(...)`.

Optional health check:

```bash
comfy-agent-doctor
```

## 3) Skill Packaging Format

Each skill folder follows this structure:

```text
skills/<skill_name>/
  skill.py
  skill.yaml
  SKILL.md
  scripts/run.py
```

What each file does:

- `skill.py`: Python implementation (`run(...)`, sometimes `build(...)`)
- `skill.yaml`: I/O schema
- `SKILL.md`: metadata + usage notes (OpenClaw/Claw-style frontmatter)
- `scripts/run.py`: CLI wrapper for calling `run(...)` with JSON args

## 4) Running Skills Directly

General pattern:

```bash
python3 skills/<skill_name>/scripts/run.py --args '{"key":"value"}' --pretty
```

Examples:

```bash
python3 skills/get_server_status/scripts/run.py --args '{}' --pretty
python3 skills/get_queue_status/scripts/run.py --args '{}' --pretty
python3 skills/get_progress/scripts/run.py --args '{"prompt_id":"<id>"}' --pretty

python3 skills/upload_image/scripts/run.py --args '{"image_path":"tmp/inputs/woman.png"}' --pretty
python3 skills/download_image/scripts/run.py --args '{"prompt_id":"<id>","run_id":"demo"}' --pretty

python3 skills/download_video/scripts/run.py --args '{"prompt_id":"<id>","run_id":"demo"}' --pretty
python3 skills/delete_image_job/scripts/run.py --args '{"prompt_id":"<id>"}' --pretty
python3 skills/delete_video_job/scripts/run.py --args '{"prompt_id":"<id>"}' --pretty
```

## 5) Skill Composition Pattern (Recommended)

Use single-purpose composition:

1. upload
2. generate
3. download
4. monitor
5. cleanup

For image-to-video:

- `upload_image` refs
- `generate_flux_multi_input_img2img`
- `download_image`
- `generate_ltxv_img2video`
- `download_video`
- optional `delete_image_job` / `delete_video_job`

## 6) End-to-End Examples

### Basic

```bash
PYTHONPATH=. python3 examples/end_to_end_pipelines/birkbeck_basic/example_birkbeck_image_to_video.py
```

Artifacts/log:

- `examples/end_to_end_pipelines/birkbeck_basic/log.md`

### Monitored (status/queue/progress)

```bash
PYTHONPATH=. python3 examples/end_to_end_pipelines/birkbeck_monitored/example_birkbeck_monitored_pipeline.py
```

Artifacts/log:

- `examples/end_to_end_pipelines/birkbeck_monitored/log.md`

### Compose + Cleanup

```bash
PYTHONPATH=. python3 examples/end_to_end_pipelines/odeon_cleanup/example_odeon_compose_and_cleanup.py
```

Artifacts/log:

- `examples/end_to_end_pipelines/odeon_cleanup/log.md`

## 7) Monitoring Semantics

Some servers do not expose `/progress`.
In that case `get_progress` falls back to queue/history logic:

- pending: starts near `5%`
- running: starts near `20%` and ramps up over time
- complete: `100%`

Tune fallback ramp speed with:

```env
COMFY_PROGRESS_EXPECTED_SECONDS=900
```

## 8) Cleanup Semantics

`delete_image_job` and `delete_video_job` delete Comfy history entries by prompt/job ID.

Important:

- They validate output type first (image vs video/gif)
- Deletion target is job history entry (not local files)
- Local output files remain unless you delete them separately

## 9) Installing/Using Skills in Other Tools

If you integrate this repo with an external agent framework:

1. point it to this repo
2. expose `skills/*/SKILL.md`
3. execute `skills/*/scripts/run.py` with JSON args
4. parse JSON stdout

This is the easiest path because wrappers are stable and uniform.

## 10) Troubleshooting

### A) Always seeing fixed progress value

- server likely lacks `/progress`
- use monitored script (queue/history fallback)
- set `COMFY_PROGRESS_EXPECTED_SECONDS` for better ramp behavior

### B) 400 validation errors for missing assets

Run:

```bash
python3 skills/list_comfy_assets/scripts/run.py --args '{}' --pretty
```

Then match model names in generation skill args.

### C) Auth/route failures

Verify:

- `COMFY_URL`
- `COMFY_API_PREFIX`
- `COMFY_AUTH_HEADER`

### D) Pipelines too slow

Main bottleneck is video generation.
Lower `length`, `steps`, or output resolution.

## 11) Quick Command Index

```bash
# status
python3 skills/get_server_status/scripts/run.py --args '{}' --pretty
python3 skills/get_queue_status/scripts/run.py --args '{}' --pretty

# progress
python3 skills/get_progress/scripts/run.py --args '{"prompt_id":"<id>"}' --pretty

# delete jobs
python3 skills/delete_image_job/scripts/run.py --args '{"prompt_id":"<image_job_id>"}' --pretty
python3 skills/delete_video_job/scripts/run.py --args '{"prompt_id":"<video_job_id>"}' --pretty

# full monitored pipeline
PYTHONPATH=. python3 examples/end_to_end_pipelines/birkbeck_monitored/example_birkbeck_monitored_pipeline.py
```

## 12) Where to Look in Repo

- examples index: `examples/README.md`
- end-to-end index: `examples/end_to_end_pipelines/README.md`
- skill implementations: `skills/*/skill.py`
- shared monitoring/cleanup helpers:
  - `comfy_agent/monitoring.py`
  - `comfy_agent/cleanup.py`

