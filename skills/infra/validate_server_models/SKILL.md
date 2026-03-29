---
name: validate_server_models
description: >
  List all available server model names and validate whether requested models exist.
homepage: https://github.com/steliosot/comfy-agent
metadata.clawdbot.os: ["darwin", "linux"]
metadata.clawdbot.requires.bins: ["python3"]
metadata.clawdbot.requires.env: ["COMFY_URL", "COMFY_AUTH_HEADER"]
metadata.clawdbot.files: ["skill.py", "skill.yaml", "scripts/*"]
metadata.clawdbot.tags: ["comfyui", "skill", "validation", "models"]
metadata.clawdbot.category: "ops"
metadata.clawdbot.input_type: "application/json"
metadata.clawdbot.output_type: "application/json"
metadata.clawdbot.output_can_feed_into: []
metadata.clawdbot.accepts_input_from: []
metadata.clawdbot.priority: 75
---

# validate_server_models

Use this to preflight model references before running generation skills.

## Usage

```bash
python3 skills/infra/validate_server_models/scripts/run.py --args '{"model_names":["sd1.5/juggernaut_reborn.safetensors"]}' --pretty
```
