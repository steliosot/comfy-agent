# Python API Reference (Practical)

## Core class: `Workflow`

Typical methods:

- Graph building:
  - `checkpoint(...)`
  - `prompt(...)`
  - `negative(...)`
  - `latent(...)`
  - `sample(...)`
  - `decode()`
  - `save(...)`
- Execution:
  - `run(target=None, debug=False)`
  - `saved_images(...)`

## Caching + memoization

- `enable_cache(policy="FULL"|"LRU", size=None)`
- `disable_cache()`
- `clear_cache()`
- `enable_memoization()`
- `disable_memoization()`

## Model manager integration

- `Workflow(model_manager=...)`
- `set_model_manager(...)`
- `configure_model_manager(max_models_in_vram=..., enable_cpu_offload=...)`

`ModelManager`:

- `get_model(model_name)`
- `stats()`

## Attention reuse controls

- `enable_attention_reuse(...)`
- `disable_attention_reuse()`
- `set_attention_reuse_adapter(adapter)`

Key fields:

- `attn_reuse_threshold`
- `attn_cache_device`
- `attn_store_frequency`
- `attn_reuse_layers`

For deeper details, see `documentation.md` in the main repository.
