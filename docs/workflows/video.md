# Video Workflows

## Recommended starters

- `skills/workflows/video_t2v_i2v_avatar/generate_video_clip`
- `skills/workflows/video_t2v_i2v_avatar/generate_ltxv_img2video`
- `skills/workflows/video_t2v_i2v_avatar/workflow_wan_2_1_text_to_video_1_3b_480p`

## Quickstart

```bash
PYTHONPATH=. python3 skills/workflows/video_t2v_i2v_avatar/generate_video_clip/scripts/run.py \
  --args '{"prompt":"cinematic drone shot over alpine lake at golden hour"}' --pretty
```

## Notes

- Video workloads are heavier than image workloads.
- Run dependency checks before execution.
- Prefer stronger servers for long clips/high resolutions.
