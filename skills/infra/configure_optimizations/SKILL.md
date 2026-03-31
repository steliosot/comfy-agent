---
name: configure_optimizations
description: >
  Return explicit optimization mode config for cache, memoization, ModelManager, and attention reuse.
homepage: https://github.com/steliosot/comfy-agent
metadata.clawdbot.os: ["darwin", "linux"]
metadata.clawdbot.requires.bins: ["python3"]
metadata.clawdbot.requires.env: []
metadata.clawdbot.files: ["skill.py", "skill.yaml", "scripts/*"]
metadata.clawdbot.tags: ["comfyui", "skill", "ops", "optimization", "cache", "memoization", "model-manager", "attention-reuse"]
metadata.clawdbot.category: "ops"
metadata.clawdbot.input_type: "application/json"
metadata.clawdbot.output_type: "application/json"
metadata.clawdbot.output_can_feed_into: []
metadata.clawdbot.accepts_input_from: []
metadata.clawdbot.priority: 74
---

# configure_optimizations

Build an optimization profile for:
- no optimization
- deterministic node cache
- graph memoization
- model LRU
- CPU offload
- lazy loading
- attention reuse
- full stack

Returns:
- `workflow` flags (`cache_enabled`, `memoization_enabled`, policy/size)
- `model_manager` flags (`max_models_in_vram`, `enable_cpu_offload`, `lazy_loading`)
- `attention_reuse` flags (`threshold`, `cache_device`, `store_frequency`, `reuse_layers`)
- `python_snippet` you can paste in scripts.
