# Buildable Skill Examples

These examples show the new reversible skill style:

- `build(...)` returns a `Workflow`
- you can inspect or modify that workflow
- `run(...)` still works as a backward-compatible wrapper

Typical pattern:

```python
from skills.generate_sd15_image.skill import build

wf = build(prompt="cinematic robot")
wf.run()
```

You can also keep the workflow object around, inspect `wf.nodes`, add more
nodes, or submit it later.

Additional example:

- `example_build_wan21_cat_gif.py` (exports `video/h264-mp4` animation)
