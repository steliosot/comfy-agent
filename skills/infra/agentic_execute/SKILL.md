---
name: agentic_execute
description: >
  Execute a precomputed agentic plan payload.
homepage: https://github.com/steliosot/comfy-agent
metadata.clawdbot.os: ["darwin", "linux"]
metadata.clawdbot.requires.bins: ["python3"]
metadata.clawdbot.requires.env: ["COMFY_URL", "COMFY_AUTH_HEADER"]
metadata.clawdbot.files: ["skill.py", "skill.yaml", "scripts/*"]
metadata.clawdbot.tags: ["comfyui", "agentic", "execution", "workflow"]
metadata.clawdbot.category: "ops"
metadata.clawdbot.input_type: "application/json"
metadata.clawdbot.output_type: "application/json"
metadata.clawdbot.output_can_feed_into: []
metadata.clawdbot.accepts_input_from: ["agentic_plan"]
metadata.clawdbot.priority: 90
---

# agentic_execute

Executes a plan payload produced by `agentic_plan`.

The skill validates plan schema/version before execution and returns structured outputs:

- `prompt_id`
- `output_images`
- `artifacts`
- execution context (`run_id`, etc.)
