---
name: download_model
description: >
  Install/download models via ComfyUI-Manager API, with source-aware token support for HuggingFace and Civitai.
homepage: https://github.com/steliosot/comfy-agent
metadata.clawdbot.os: ["darwin", "linux"]
metadata.clawdbot.requires.bins: ["python3"]
metadata.clawdbot.requires.env: ["COMFY_URL", "HF_TOKEN", "CIVITAI_API_KEY"]
metadata.clawdbot.files: ["skill.py", "skill.yaml", "scripts/*"]
metadata.clawdbot.tags: ["comfyui", "skill", "ops", "models", "huggingface", "civitai"]
metadata.clawdbot.category: "ops"
metadata.clawdbot.input_type: "application/json"
metadata.clawdbot.output_type: "application/json"
metadata.clawdbot.output_can_feed_into: ["prepare_workflow_dependencies"]
metadata.clawdbot.accepts_input_from: []
metadata.clawdbot.priority: 90
---

# download_model

Installs a model through ComfyUI-Manager and verifies availability in Comfy loader choices.
