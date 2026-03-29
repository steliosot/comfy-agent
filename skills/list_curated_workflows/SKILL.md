---
name: list_curated_workflows
description: >
  List curated workflow skills and filter them by capability family or model family hints.
homepage: https://github.com/steliosot/comfy-agent
metadata.clawdbot.os: ["darwin", "linux"]
metadata.clawdbot.requires.bins: ["python3"]
metadata.clawdbot.requires.env: []
metadata.clawdbot.files: ["skill.py", "skill.yaml", "scripts/*"]
metadata.clawdbot.tags: ["comfyui", "skill", "catalog", "workflow-selection"]
metadata.clawdbot.category: "ops"
metadata.clawdbot.input_type: "application/json"
metadata.clawdbot.output_type: "application/json"
metadata.clawdbot.output_can_feed_into: ["match_curated_workflow", "run_curated_workflow"]
metadata.clawdbot.accepts_input_from: []
metadata.clawdbot.priority: 82
---

# list_curated_workflows

Returns curated workflow entries from `skills/curated_workflows/manifest.json`.
