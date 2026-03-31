# Quickstart (Python DSL)

All examples assume:

- `COMFY_URL` is set.
- You are in repo root with `PYTHONPATH=.`.

## 1) Minimal pipeline

Prerequisite: default SD1.5-compatible checkpoint available.

```bash
PYTHONPATH=. python3 examples/workflows_fluent_dsl/example_minimal_pipeline.py
```

Expected output: prompt submission + generated output metadata.

Common failure: missing checkpoint. Fix by running dependency prep or switching checkpoint name.

## 2) Fluent txt2img

Prerequisite: same as above.

```bash
PYTHONPATH=. python3 examples/workflows_fluent_dsl/example_txt2img.py
```

Expected output: image generation result JSON.

Common failure: validation issue from missing node/model. Fix with dependency checks.

## 3) Fluent video clip

Prerequisite: video models and enough VRAM/server capacity.

```bash
PYTHONPATH=. python3 examples/workflows_fluent_dsl/example_wan21_video_clip.py
```

Expected output: video prompt result and downloadable artifact.

Common failure: heavy runtime/timeout. Fix with shorter duration or stronger server.

## 4) Direct img2img remix

Prerequisite: input image available and compatible model.

```bash
PYTHONPATH=. python3 examples/workflows_direct_dsl/example_sd15_img2img_remix.py
```

Expected output: remixed image metadata.

Common failure: input file path invalid. Fix by providing a real local image path.
