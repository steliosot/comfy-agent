# Benchmarks

Benchmark scripts live in `examples/benchmarks/`.

## Available scripts

- `benchmark_caching_txt2img.py`
- `benchmark_caching_multitask.py`
- `benchmark_ltxv_video_attention.py`

## What to track

- `Time (s)`
- `Speedup %`
- `Exec Nodes`
- `Skipped`
- `Cache Hits`
- `Cache Miss`
- `Sampler Runs`

## Good benchmark practice

- Use fixed seeds when comparing cache modes.
- Separate artifacts by task/scenario/mode/run.
- Run multiple repetitions (>=3) per scenario.
- Report baseline (`None`) and speedup against baseline.
