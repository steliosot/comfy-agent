# Txt2Img Workflows

## Recommended starters

- `skills/workflows/txt2img/generate_sd15_image`
- `skills/workflows/txt2img/preview_sd15_image`

## Quickstart

```bash
PYTHONPATH=. python3 skills/workflows/txt2img/generate_sd15_image/scripts/run.py \
  --args '{"prompt":"cinematic portrait, soft dramatic light"}' --pretty
```

## Useful variations

- Lower latency: use preview/low-step presets.
- Better detail: increase steps and resolution.
- Style control: use curated style workflows under `editing_restyle`.
