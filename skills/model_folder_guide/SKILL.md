---
name: model_folder_guide
description: >
  Return model type placement guidance for ComfyUI (for example checkpoints vs diffusion_models).
homepage: https://github.com/steliosot/comfy-agent
metadata.clawdbot.os: ["darwin", "linux"]
metadata.clawdbot.requires.bins: ["python3"]
metadata.clawdbot.requires.env: []
metadata.clawdbot.files: ["skill.py", "skill.yaml", "scripts/*"]
metadata.clawdbot.tags: ["comfyui", "skill", "ops", "models", "folders"]
metadata.clawdbot.category: "ops"
metadata.clawdbot.input_type: "application/json"
metadata.clawdbot.output_type: "application/json"
metadata.clawdbot.output_can_feed_into: ["download_model", "prepare_workflow_dependencies"]
metadata.clawdbot.accepts_input_from: []
metadata.clawdbot.priority: 50
---

# model_folder_guide

Use this skill to answer where each model type should be placed in ComfyUI.
