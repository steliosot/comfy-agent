---
name: match_curated_workflow
description: >
  Match user intent to the most appropriate curated workflow skills.
homepage: https://github.com/steliosot/comfy-agent
metadata.clawdbot.os: ["darwin", "linux"]
metadata.clawdbot.requires.bins: ["python3"]
metadata.clawdbot.requires.env: []
metadata.clawdbot.files: ["skill.py", "skill.yaml", "scripts/*"]
metadata.clawdbot.tags: ["comfyui", "skill", "routing", "workflow-selection"]
metadata.clawdbot.category: "ops"
metadata.clawdbot.input_type: "text"
metadata.clawdbot.output_type: "application/json"
metadata.clawdbot.output_can_feed_into: ["run_curated_workflow"]
metadata.clawdbot.accepts_input_from: []
metadata.clawdbot.priority: 88
---

# match_curated_workflow

Selects the best curated workflow candidates based on prompt intent and optional filters.
