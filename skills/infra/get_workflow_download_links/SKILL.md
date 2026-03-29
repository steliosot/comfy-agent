---
name: get_workflow_download_links
description: >
  Extracts model/dependency links from notes embedded in workflow JSON files and groups them by provider.
homepage: https://github.com/steliosot/comfy-agent
metadata.clawdbot.os: ["darwin", "linux"]
metadata.clawdbot.requires.bins: ["python3"]
metadata.clawdbot.requires.env: []
metadata.clawdbot.files: ["skill.py", "skill.yaml", "scripts/*"]
metadata.clawdbot.tags: ["comfyui", "skill", "dependencies", "links", "huggingface", "civitai"]
metadata.clawdbot.category: "ops"
metadata.clawdbot.input_type: "application/json"
metadata.clawdbot.output_type: "application/json"
metadata.clawdbot.output_can_feed_into: ["download_model", "prepare_workflow_dependencies"]
metadata.clawdbot.accepts_input_from: ["match_curated_workflow", "list_curated_workflows"]
metadata.clawdbot.priority: 89
---

# get_workflow_download_links

Reads workflow notes directly from `workflow.json` and returns grouped links:

- `huggingface`
- `civitai`
- `github`
- `comfy_docs`
- `community`
- `other`

Use `skill_id` for curated workflows, or pass any `workflow_path`.
