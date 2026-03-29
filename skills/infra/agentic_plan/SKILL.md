---
name: agentic_plan
description: >
  Build a structured plan for agentic generation before execution.
homepage: https://github.com/steliosot/comfy-agent
metadata.clawdbot.os: ["darwin", "linux"]
metadata.clawdbot.requires.bins: ["python3"]
metadata.clawdbot.requires.env: ["COMFY_URL", "COMFY_AUTH_HEADER"]
metadata.clawdbot.files: ["skill.py", "skill.yaml", "scripts/*"]
metadata.clawdbot.tags: ["comfyui", "agentic", "planning", "workflow"]
metadata.clawdbot.category: "ops"
metadata.clawdbot.input_type: "application/json"
metadata.clawdbot.output_type: "application/json"
metadata.clawdbot.output_can_feed_into: ["agentic_execute"]
metadata.clawdbot.accepts_input_from: []
metadata.clawdbot.priority: 90
---

# agentic_plan

Builds a decision-safe plan payload with:

- chosen skills and confidence
- ordered steps
- resolved execution parameters
- optional dependency preflight summary
- warnings for risky flows (for example: video + crop mismatch)
