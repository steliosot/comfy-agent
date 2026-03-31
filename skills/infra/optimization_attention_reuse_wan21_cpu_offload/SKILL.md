---
name: optimization_attention_reuse_wan21_cpu_offload
description: >
  Enable WAN2.1 attention reuse preset with CPU offload.
homepage: https://github.com/steliosot/comfy-agent
metadata.clawdbot.os: ["darwin", "linux"]
metadata.clawdbot.requires.bins: ["python3"]
metadata.clawdbot.requires.env: []
metadata.clawdbot.files: ["skill.py", "skill.yaml", "scripts/*"]
metadata.clawdbot.tags: ["comfyui", "skill", "ops", "optimization", "attention", "wan2.1", "cpu-offload"]
metadata.clawdbot.category: "ops"
metadata.clawdbot.input_type: "application/json"
metadata.clawdbot.output_type: "application/json"
metadata.clawdbot.output_can_feed_into: []
metadata.clawdbot.accepts_input_from: []
metadata.clawdbot.priority: 70
---

# optimization_attention_reuse_wan21_cpu_offload

Enable WAN2.1 attention reuse preset with CPU offload.

This skill wraps configure_optimizations with fixed mode: attention_reuse_wan21_cpu_offload.
