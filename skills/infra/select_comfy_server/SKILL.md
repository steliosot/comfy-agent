---
name: select_comfy_server
description: >
  Resolve a named Comfy server from YAML registry and return run-ready connection params.
homepage: https://github.com/steliosot/comfy-agent
metadata.clawdbot.os: ["darwin", "linux"]
metadata.clawdbot.requires.bins: ["python3"]
metadata.clawdbot.requires.env: ["COMFY_URL", "COMFY_AUTH_HEADER", "COMFY_SERVERS_FILE"]
metadata.clawdbot.files: ["skill.py", "skill.yaml", "scripts/*"]
metadata.clawdbot.tags: ["comfyui", "skill", "ops", "servers", "routing"]
metadata.clawdbot.category: "ops"
metadata.clawdbot.input_type: "application/json"
metadata.clawdbot.output_type: "application/json"
metadata.clawdbot.output_can_feed_into: ["prepare_workflow_dependencies"]
metadata.clawdbot.accepts_input_from: []
metadata.clawdbot.priority: 75
---

# select_comfy_server

Select a Comfy server configuration by name from `.comfy_servers.yaml`
or `COMFY_SERVERS_FILE`.

Returns explicit run-time fields:
- `server`
- `headers`
- `api_prefix`
- `manager_api_prefix`

Use this output and pass it into other skills per-run.
No global env mutation is performed.
