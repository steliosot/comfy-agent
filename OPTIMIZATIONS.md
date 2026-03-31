# Optimizations Guide

This guide describes the optimization modes available in `comfy-agent`, what each does, and when to use them.

## 1) No Optimization

What it does:
- Baseline mode. Every run submits a fresh prompt and recomputes all required nodes.

When it helps:
- Correctness checks.
- First-time workflow debugging.

When it will not help:
- Repeated runs with similar inputs.

How to use:
```python
wf.disable_cache()
wf.disable_memoization()
```

Expected pattern:
- Stable behavior.
- Highest repeated-run latency.

## 2) Deterministic Node Cache

What it does:
- Computes deterministic signatures for nodes.
- Reuses cached node state metadata for unchanged node signatures.

When it helps:
- Re-running similar workflows.
- Cases where only part of the graph changes.

When it will not help:
- Full prompt/model/input changes that invalidate most signatures.

How to use:
```python
wf.enable_cache(policy="LRU", size=256)  # or policy="FULL"
wf.disable_memoization()
```

Expected pattern:
- Faster partial re-runs.
- Cache-hit events for unchanged nodes.

## 3) Graph Memoization

What it does:
- Adds run-level short-circuiting for unchanged target closure signatures.
- If closure is unchanged and cached, skips a new `/prompt` submission.

When it helps:
- Repeated identical runs on the same target.

When it will not help:
- Any signature change in the target closure.

How to use:
```python
wf.enable_cache()
wf.enable_memoization()
```

Expected pattern:
- Largest gains for exact repeats (`A_same` style scenarios).

## 4) Model LRU (ModelManager)

What it does:
- Tracks model objects in an LRU structure (`vram_models`).
- Most recently used models stay resident in the configured VRAM slot count.

When it helps:
- Frequent model reuse across workflows.
- Repeated checkpoint switching within a small model set.

When it will not help:
- Constantly changing to many unique models beyond cache capacity.

How to use:
```python
from comfy_agent import Workflow, ModelManager

manager = ModelManager(max_models_in_vram=1, enable_cpu_offload=True)
wf = Workflow(model_manager=manager)
```

Expected pattern:
- Fastest for repeated same-model access (`[VRAM HIT]`).

## 5) CPU Offload

What it does:
- On LRU eviction, moves older models to `cpu_models` instead of dropping them.
- Reload path becomes CPU->GPU transfer rather than disk load.

When it helps:
- Alternating between a few large models.

When it will not help:
- CPU memory limits are tight, or models are used only once.

How to use:
```python
manager = ModelManager(max_models_in_vram=1, enable_cpu_offload=True)
```

Expected pattern:
- `[CPU HIT -> GPU]` for previously evicted models.
- Lower reload cost than disk loads in many cases.

## 6) Lazy Loading

What it does:
- Models are loaded only on demand via `get_model(...)`.
- No eager model preloading at startup.

When it helps:
- Faster startup.
- Lower initial memory pressure.

When it will not help:
- First request for each model still pays cold-load cost.

How to use:
- Default behavior in `ModelManager`.
- Triggered on first `wf.checkpoint("...")` call.

Expected pattern:
- First call: `[LOAD DISK]`.
- Follow-up calls: `[VRAM HIT]` or `[CPU HIT -> GPU]`.

## 7) Attention Reuse (Optional Plugin)

What it does:
- Enables the optional attention-reuse plugin wrapper in `Workflow`.
- Applies strict safe-gating policy for reuse candidates (model/prompt/layer/step checks).
- Falls back safely if no compatible backend adapter is attached.

When it helps:
- Environments with a compatible attention backend adapter.
- Late-step attention reuse scenarios where prompt/model are stable.

When it will not help:
- Default remote-only setup without an adapter (plugin will fallback by design).
- Early diffusion steps or disallowed layer kinds.

How to use:
```python
wf.enable_attention_reuse(
    threshold=0.6,
    cache_device="cpu",
    store_frequency=2,
    reuse_layers=["cross_attention"],
)
```

Expected pattern:
- With compatible adapter: `[ATTN STORE]` / `[ATTN REUSE]`.
- Without adapter: `[ATTN FALLBACK]` and normal generation behavior.

## 8) Attention Reuse + CPU Offload

What it does:
- Combines attention-reuse plugin mode with `ModelManager` CPU offload profile.
- Keeps model transitions cheaper while attention plugin remains available.

When it helps:
- Multi-model workloads where you also want attention-reuse capability enabled.

When it will not help:
- No adapter is present (attention remains fallback-only).

How to use:
```python
from comfy_agent import Workflow, ModelManager

wf = Workflow(model_manager=ModelManager(max_models_in_vram=1, enable_cpu_offload=True))
wf.enable_attention_reuse()
```

Expected pattern:
- Model side: `[VRAM HIT]` / `[CPU HIT -> GPU]`.
- Attention side: reuse events only when adapter/hook is available.

## Safe Combinations

Recommended combined setup:
```python
from comfy_agent import Workflow, ModelManager

manager = ModelManager(max_models_in_vram=1, enable_cpu_offload=True)
wf = Workflow(model_manager=manager)
wf.enable_cache(policy="LRU", size=256)
wf.enable_memoization()
```

Why this is safe:
- Node cache + memoization optimize DAG execution planning/submission.
- ModelManager optimizes client-side model-resolution reuse behavior.
- Current server-side ComfyUI execution semantics remain unchanged.

Attention plugin caveat:
- Attention reuse is compatibility-first and optional.
- Real attention interception/reuse requires a compatible backend adapter.
- Without adapter, the plugin is still safe and non-breaking (fallback mode).

## Optimization Skills

You can also configure modes using infra skills:
- `optimization_none`
- `optimization_cache`
- `optimization_memoization`
- `optimization_model_lru`
- `optimization_cpu_offload`
- `optimization_lazy_loading`
- `optimization_attention_reuse`
- `optimization_attention_reuse_cpu_offload`
- `optimization_full_stack`

## Debug Signals

ModelManager logs:
- `[VRAM HIT] <model>`
- `[CPU HIT -> GPU] <model>`
- `[LOAD DISK] <model>`
- `[EVICT -> CPU] <model>`

Workflow debug:
- `[EXECUTE] <NodeClass>#<id>`
- `[CACHE HIT] <NodeClass>#<id>`
- `[SKIP] <NodeClass>#<id> (outside target)`

Attention plugin debug:
- `[ATTN ENABLED]`
- `[ATTN STORE] step=<s> layer=<l>`
- `[ATTN REUSE] step=<s> layer=<l>`
- `[ATTN FALLBACK] step=<s> layer=<l> reason=<...>`
