# Workflow Library Overview

`comfy-agent` ships a large workflow skill library grouped by family.

## Families

- `txt2img`
- `img2img_inpaint_outpaint`
- `video_t2v_i2v_avatar`
- `audio`
- `upscaling`
- `editing_restyle`

## Which family to choose

- Start from `txt2img` for first outputs.
- Use `img2img_inpaint_outpaint` for edits/restyles.
- Use `video_t2v_i2v_avatar` for text/image-to-video.
- Use `audio` for text/music/speech pipelines.
- Use `upscaling` for quality and resolution upgrades.

## Source indexes

- `skills/workflows/skills_index.json`
- `skills/workflows/all_workflows_manifest.json`

These indexes are useful for automation and discovery.
