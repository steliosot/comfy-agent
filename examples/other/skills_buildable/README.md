# Buildable Skill Examples

These examples show the new reversible skill style:

- `build(...)` returns a `Workflow`
- you can inspect or modify that workflow
- `run(...)` still works as a backward-compatible wrapper

Typical pattern:

```python
from skills.workflows.txt2img.generate_sd15_image.skill import build

wf = build(prompt="cinematic robot")
wf.run()
```

You can also keep the workflow object around, inspect `wf.nodes`, add more
nodes, or submit it later.

Additional example:

- `example_build_video_clip.py` (uses the generic `generate_video_clip` skill and exports `video/h264-mp4`)
