---
name: prepare_workflow_dependencies
description: >
  Detect workflow dependency gaps (models/custom nodes), assess server resources, and auto-fix through install skills.
homepage: https://github.com/steliosot/comfy-agent
metadata.clawdbot.os: ["darwin", "linux"]
metadata.clawdbot.requires.bins: ["python3"]
metadata.clawdbot.requires.env: ["COMFY_URL"]
metadata.clawdbot.files: ["skill.py", "skill.yaml", "scripts/*"]
metadata.clawdbot.tags: ["comfyui", "skill", "ops", "dependencies", "auto-fix"]
metadata.clawdbot.category: "ops"
metadata.clawdbot.input_type: "application/json"
metadata.clawdbot.output_type: "application/json"
metadata.clawdbot.output_can_feed_into: []
metadata.clawdbot.accepts_input_from: []
metadata.clawdbot.priority: 95
---

# prepare_workflow_dependencies

This skill is the dependency preflight orchestrator.
Use it before submitting prompts when models or custom nodes may be missing.
