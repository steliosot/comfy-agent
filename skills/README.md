# Skills Navigation

The `skills/` folder is now organized into two primary groups:

- `skills/infra/`: infrastructure and operations skills (server checks, queue/progress, upload/download, dependency setup, model/node install/remove, workflow routing helpers).
- `skills/workflows/`: workflow execution skills.

Workflow skills include:

- `skills/workflows/<family>/`: all workflow skills grouped by capability family (audio, txt2img, img2img/inpaint, editing/restyle, video, upscaling).
- Curated index: `skills/workflows/curated_manifest.json` (`120` workflows).
- Full-library index: `skills/workflows/all_workflows_manifest.json` (`360` workflows).
