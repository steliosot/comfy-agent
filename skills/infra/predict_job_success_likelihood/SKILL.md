---
name: predict_job_success_likelihood
description: >
  Predicts the likelihood of successful workflow execution using installed dependencies, resource status, and similar historical jobs.
homepage: https://github.com/steliosot/comfy-agent
metadata.clawdbot.os: ["darwin", "linux"]
metadata.clawdbot.requires.bins: ["python3"]
metadata.clawdbot.requires.env: ["COMFY_URL", "COMFY_AUTH_HEADER"]
metadata.clawdbot.files: ["skill.py", "skill.yaml", "scripts/*"]
metadata.clawdbot.tags: ["comfyui", "skill", "ops", "prediction", "history", "preflight"]
metadata.clawdbot.category: "ops"
metadata.clawdbot.input_type: "application/json"
metadata.clawdbot.output_type: "application/json"
metadata.clawdbot.output_can_feed_into: ["prepare_workflow_dependencies", "run_curated_workflow"]
metadata.clawdbot.accepts_input_from: ["match_curated_workflow", "list_curated_workflows"]
metadata.clawdbot.priority: 93
---

# predict_job_success_likelihood

Returns:

- `likelihood`: estimated success probability (`0..1`)
- `confidence`: confidence in this estimate (`0..1`)
- `recommendation`: one of:
  - `safe_to_run`
  - `run_with_caution`
  - `fix_dependencies_first`

The estimate combines:

- dependency readiness from installed nodes/models
- historical success rate for similar workflows
- current queue/resource pressure
