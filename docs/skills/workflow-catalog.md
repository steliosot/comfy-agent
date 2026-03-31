# Workflow Skill Catalog

`comfy-agent` includes a large catalog (hundreds) of workflow skills.

## Families and entry points

| Family | Path Prefix | Best First Skill |
|---|---|---|
| txt2img | `skills/workflows/txt2img` | `generate_sd15_image` |
| img2img/inpaint/outpaint | `skills/workflows/img2img_inpaint_outpaint` | `generate_sd15_img2img_remix` |
| video t2v/i2v/avatar | `skills/workflows/video_t2v_i2v_avatar` | `generate_video_clip` |
| audio | `skills/workflows/audio` | `curated_ep47_acestep_v1_3_5b_text_to_music_lyrics` |
| upscaling | `skills/workflows/upscaling` | `workflow_simple_upscale_with_model` |
| editing/restyle | `skills/workflows/editing_restyle` | `curated_qwen_image_edit_transform_to_pencil_drawing` |

## Discovery files

- `skills/workflows/skills_index.json`
- `skills/workflows/all_workflows_manifest.json`

These files can be used to build custom selectors, UI catalogs, and recommendation logic.
