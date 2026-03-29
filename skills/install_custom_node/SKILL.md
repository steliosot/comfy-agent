---
name: install_custom_node
description: >
  Install a ComfyUI custom node package from a git URL through ComfyUI-Manager API and verify node availability.
homepage: https://github.com/steliosot/comfy-agent
metadata.clawdbot.os: ["darwin", "linux"]
metadata.clawdbot.requires.bins: ["python3"]
metadata.clawdbot.requires.env: ["COMFY_URL"]
metadata.clawdbot.files: ["skill.py", "skill.yaml", "scripts/*"]
metadata.clawdbot.tags: ["comfyui", "skill", "ops", "custom_nodes", "install"]
metadata.clawdbot.category: "ops"
metadata.clawdbot.input_type: "application/json"
metadata.clawdbot.output_type: "application/json"
metadata.clawdbot.output_can_feed_into: ["prepare_workflow_dependencies"]
metadata.clawdbot.accepts_input_from: []
metadata.clawdbot.priority: 90
---

# install_custom_node

Installs custom nodes by git URL and verifies expected node classes in `object_info`.
