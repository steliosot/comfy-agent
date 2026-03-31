# Upscaling Workflows

## Recommended starters

- `skills/workflows/upscaling/workflow_simple_upscale_with_model`
- `skills/workflows/upscaling/workflow_ep46_juggernaut_reborn_sd1_5_txt2img_with_upscaler`

## Quickstart

```bash
PYTHONPATH=. python3 skills/workflows/upscaling/workflow_simple_upscale_with_model/scripts/run.py \
  --args '{"image_path":"tmp/inputs/example.png"}' --pretty
```

## Notes

- Upscaling is a good post-step after txt2img/img2img.
- For large outputs, monitor VRAM and runtime.
