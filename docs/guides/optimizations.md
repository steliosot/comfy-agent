# Optimizations

This page summarizes the optimization modes available in `comfy-agent`.

## Modes

- `none`: baseline, full recompute.
- `cache`: deterministic node signature cache.
- `memoization`: graph-level run short-circuit for unchanged closure.
- `model_lru`: model LRU management.
- `cpu_offload`: move evicted models to CPU cache.
- `lazy_loading`: load models on demand.
- `attention_reuse`: optional attention reuse plugin (adapter-based).
- `attention_reuse_cpu_offload`: combine reuse mode with model offload profile.

## Typical safe combo

```python
from comfy_agent import Workflow, ModelManager

manager = ModelManager(max_models_in_vram=1, enable_cpu_offload=True)
wf = Workflow(model_manager=manager)
wf.enable_cache(policy="LRU", size=256)
wf.enable_memoization()
```

## Configure via infra skills

- `skills/infra/configure_optimizations`
- `skills/infra/optimization_cache`
- `skills/infra/optimization_memoization`
- `skills/infra/optimization_model_lru`
- `skills/infra/optimization_cpu_offload`
- `skills/infra/optimization_lazy_loading`
- `skills/infra/optimization_attention_reuse`

For full details, also see repository `OPTIMIZATIONS.md`.
