# Img2Img / Inpaint / Outpaint

## Recommended starters

- `skills/workflows/img2img_inpaint_outpaint/generate_sd15_img2img_remix`
- `skills/workflows/img2img_inpaint_outpaint/preview_sd15_img2img`
- `skills/workflows/img2img_inpaint_outpaint/crop_image`

## Quickstart

```bash
PYTHONPATH=. python3 skills/workflows/img2img_inpaint_outpaint/generate_sd15_img2img_remix/scripts/run.py \
  --args '{"image_path":"tmp/inputs/example.png","prompt":"cinematic remix with shallow depth of field"}' --pretty
```

## Typical use cases

- Product recolor.
- Style transfer.
- Object insertion/removal with inpainting.
- Background extension with outpainting.
