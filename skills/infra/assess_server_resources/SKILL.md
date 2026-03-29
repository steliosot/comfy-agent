---
name: assess_server_resources
description: >
  Assess queue load and hardware/resource compatibility (VRAM/storage) before installs or workflow runs.
homepage: https://github.com/steliosot/comfy-agent
metadata.clawdbot.os: ["darwin", "linux"]
metadata.clawdbot.requires.bins: ["python3"]
metadata.clawdbot.requires.env: ["COMFY_URL", "COMFY_AUTH_HEADER"]
metadata.clawdbot.files: ["skill.py", "skill.yaml", "scripts/*"]
metadata.clawdbot.tags: ["comfyui", "skill", "ops", "resources", "monitoring"]
metadata.clawdbot.category: "ops"
metadata.clawdbot.input_type: "application/json"
metadata.clawdbot.output_type: "application/json"
metadata.clawdbot.output_can_feed_into: ["prepare_workflow_dependencies"]
metadata.clawdbot.accepts_input_from: []
metadata.clawdbot.priority: 80
---

# assess_server_resources

Use this skill to verify queue pressure and resource thresholds (free VRAM/storage)
before dependency auto-repair or workflow execution.
