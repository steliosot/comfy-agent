# Editing / Restyle Workflows

The `editing_restyle` family includes many curated style and edit pipelines.

## Recommended starters

- `skills/workflows/editing_restyle/curated_qwen_image_edit_transform_to_pencil_drawing`
- `skills/workflows/editing_restyle/workflow_qwen_image_edit_one_image_edit`
- `skills/workflows/editing_restyle/curated_ep06_basic_sdxl_txt2img_with_styles_workflow`

## Example

```bash
PYTHONPATH=. python3 skills/workflows/editing_restyle/curated_qwen_image_edit_transform_to_pencil_drawing/scripts/run.py \
  --args '{"image_path":"tmp/inputs/example.png"}' --pretty
```

## Notes

- Many editing skills are model/custom-node sensitive.
- Use preflight checks for reliable runs.
