---
name: optimization_attention_reuse_wan21
description: >
  Enable attention reuse preset tuned for WAN2.1 video pipelines.
homepage: https://github.com/steliosot/comfy-agent
metadata.clawdbot.os: ["darwin", "linux"]
metadata.clawdbot.requires.bins: ["python3"]
metadata.clawdbot.requires.env: []
metadata.clawdbot.files: ["skill.py", "skill.yaml", "scripts/*"]
metadata.clawdbot.tags: ["comfyui", "skill", "ops", "optimization", "attention", "wan2.1"]
metadata.clawdbot.category: "ops"
metadata.clawdbot.input_type: "application/json"
metadata.clawdbot.output_type: "application/json"
metadata.clawdbot.output_can_feed_into: []
metadata.clawdbot.accepts_input_from: []
metadata.clawdbot.priority: 70
---

# optimization_attention_reuse_wan21

Enable attention reuse preset tuned for WAN2.1 video pipelines.

This skill wraps configure_optimizations with fixed mode: attention_reuse_wan21.
