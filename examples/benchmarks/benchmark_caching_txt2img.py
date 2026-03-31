#!/usr/bin/env python3
import time
from pathlib import Path

from comfy_agent import Workflow


BASE = {
    "prompt": "robot",
    "seed": 111,
    "checkpoint": "sd1.5/juggernaut_reborn.safetensors",
}

SCENARIOS = {
    "A": {
        "title": "Same prompt (warm cache)",
        "description": "Same prompt, seed, and checkpoint. Measures best-case cache reuse.",
        "measure": dict(BASE),
    },
    "B1": {
        "title": "Small prompt change",
        "description": "Prompt changes from 'robot' to 'robot with hat'.",
        "measure": {**BASE, "prompt": "robot with hat"},
    },
    "B2": {
        "title": "Large prompt change",
        "description": "Prompt changes from 'robot' to 'portrait of a woman'.",
        "measure": {**BASE, "prompt": "portrait of a woman"},
    },
    "C": {
        "title": "Seed change",
        "description": "Prompt stays fixed, seed changes from baseline.",
        "measure": {**BASE, "seed": 222},
    },
    "D": {
        "title": "Model change",
        "description": "Checkpoint switches from SD1.5 Juggernaut to SDXL Juggernaut.",
        "measure": {**BASE, "checkpoint": "sdxl/juggernautXL_version2.safetensors"},
    },
}

MODES = [
    ("None", False, False, False, 1),
    ("Cache", True, False, False, 2),
    ("Full", True, True, False, 3),
    ("AttentionReuse", False, False, True, 5),
]


def build_workflow():
    wf = Workflow()
    (
        wf
        .checkpoint(BASE["checkpoint"])
        .prompt(BASE["prompt"])
        .latent(width=512, height=512)
        .sample(steps=20, cfg=8, sampler_name="euler", seed=BASE["seed"])
        .decode()
        .save("output")
    )
    return wf


def configure_mode(wf, use_cache, use_memo, use_attention_reuse):
    if use_cache:
        wf.enable_cache(policy="LRU", size=100)
    else:
        wf.disable_cache()
    if use_memo:
        wf.enable_memoization()
    else:
        wf.disable_memoization()
    if use_attention_reuse:
        wf.enable_attention_reuse()
    else:
        wf.disable_attention_reuse()
    wf.clear_cache()


def apply_config(wf, config):
    wf.override(
        {
            "checkpoint.ckpt_name": config["checkpoint"],
            "prompt.text": config["prompt"],
            "ksampler.seed": config["seed"],
        }
    )


def run_and_wait(wf, config):
    apply_config(wf, config)
    started = time.perf_counter()
    result = wf.run(target="save", debug=False)
    prompt_id = result.get("prompt_id")
    # Wait for completion status when a prompt was submitted.
    if prompt_id and result.get("execution_metrics", {}).get("executed_nodes", 0) > 0:
        wait_for_completion(wf, prompt_id=prompt_id, timeout_s=300, poll_delay=0.5)
    elapsed = time.perf_counter() - started
    metrics = dict(result.get("execution_metrics", {}))
    # For no-cache mode, treat all executed nodes as misses for reporting parity.
    if not wf.cache_enabled:
        metrics["cache_misses"] = metrics.get("executed_nodes", 0)
    # In this benchmark, "Skipped" means not executed in this run.
    metrics["skipped_nodes"] = metrics.get("cache_hits", 0) + metrics.get("skipped_nodes", 0)
    return {
        "time_s": elapsed,
        "executed_nodes": metrics.get("executed_nodes", 0),
        "skipped_nodes": metrics.get("skipped_nodes", 0),
        "cache_hits": metrics.get("cache_hits", 0),
        "cache_misses": metrics.get("cache_misses", 0),
        "sampler_runs": metrics.get("sampler_runs", 0),
    }


def wait_for_completion(wf, prompt_id, timeout_s=300, poll_delay=0.5):
    started = time.perf_counter()
    while (time.perf_counter() - started) < timeout_s:
        history = wf.history(prompt_id=prompt_id)
        entry = history.get(prompt_id, history) if isinstance(history, dict) else history
        status = entry.get("status", {}) if isinstance(entry, dict) else {}
        if status.get("completed") is True:
            return
        time.sleep(poll_delay)
    raise TimeoutError(f"Timed out waiting for prompt completion: {prompt_id}")


def run_scenario_mode(scenario_key, mode_tuple):
    mode_name, use_cache, use_memo, use_attention_reuse, run_num = mode_tuple
    wf = build_workflow()
    configure_mode(wf, use_cache=use_cache, use_memo=use_memo, use_attention_reuse=use_attention_reuse)
    # Warm-up baseline state once for cache/memo modes.
    if use_cache:
        run_and_wait(wf, BASE)
    measured = run_and_wait(wf, SCENARIOS[scenario_key]["measure"])
    return {
        "scenario": scenario_key,
        "mode": mode_name,
        "run": run_num,
        **measured,
    }


def speedups(rows):
    out = {}
    for scenario in SCENARIOS:
        base = next(r for r in rows if r["scenario"] == scenario and r["mode"] == "None")["time_s"]
        cache = next(r for r in rows if r["scenario"] == scenario and r["mode"] == "Cache")["time_s"]
        full = next(r for r in rows if r["scenario"] == scenario and r["mode"] == "Full")["time_s"]
        out[scenario] = {
            "cache": (base / cache) if cache > 0 else 0.0,
            "full": (base / full) if full > 0 else 0.0,
        }
    return out


def render_table(rows):
    lines = [
        "| Scenario | Mode   | Run | Time (s) | Speedup % | Exec Nodes | Skipped | Cache Hits | Cache Miss | Sampler Runs |",
        "|----------|--------|-----|----------|-----------|------------|---------|------------|------------|--------------|",
    ]
    for row in rows:
        lines.append(
            f"| {row['scenario']} | {row['mode']:<6} | {row['run']}   | "
            f"{row['time_s']:.3f}    | {row['executed_nodes']}          | {row['skipped_nodes']}       | "
            f"{row['cache_hits']}          | {row['cache_misses']}          | {row['sampler_runs']}            |"
        )
    return "\n".join(lines)


def main():
    rows = []
    for scenario_key in ["A", "B1", "B2", "C", "D"]:
        for mode in MODES:
            rows.append(run_scenario_mode(scenario_key, mode))

    table = render_table(rows)
    summary = speedups(rows)

    report_lines = [
        "# Caching Benchmark Report (txt2img)",
        "",
        "This benchmark runs on a real Comfy server and waits for generation completion (`saved_images`) when execution occurs.",
        "",
        "## Scenario Notes",
    ]
    for key in ["A", "B1", "B2", "C", "D"]:
        report_lines.append(f"- **{key} — {SCENARIOS[key]['title']}**: {SCENARIOS[key]['description']}")
    report_lines.extend(
        [
            "",
            "## Results",
            "",
            table,
            "",
            "## Speedup vs Baseline",
            "",
        ]
    )
    for key in ["A", "B1", "B2", "C", "D"]:
        report_lines.append(
            f"- **{key}**: Cache `{summary[key]['cache']:.2f}x`, Full `{summary[key]['full']:.2f}x`"
        )

    text = "\n".join(report_lines)
    print(text)
    out_path = Path("tmp/outputs/benchmark_caching_txt2img_report.md")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(text, encoding="utf-8")
    print(f"\nSaved report: {out_path.resolve()}")


if __name__ == "__main__":
    main()
