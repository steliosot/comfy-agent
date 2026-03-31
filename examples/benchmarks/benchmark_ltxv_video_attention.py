#!/usr/bin/env python3
import argparse
import csv
import json
import time
from pathlib import Path

from comfy_agent.node import Node
from comfy_agent.refs import DataRef
from comfy_agent.workflow import Workflow
from comfy_agent.curated_workflow_runtime import _convert_exported_to_prompt


WORKFLOW_JSON = Path(
    "skills/workflows/video_t2v_i2v_avatar/workflow_ep25_ltxv_text_to_video_mp4/workflow.json"
)

BASE = {
    "prompt": "a woman wearing a red hat",
    "negative_prompt": "low quality, worst quality, deformed, distorted, disfigured",
    "seed": 164647606918121,
    "checkpoint": "ltx-video-2b-v0.9.5.safetensors",
    "text_encoder": "t5xxl_fp16.safetensors",
    "steps": 8,
    "length": 17,
    "cfg": 1.0,
}

SCENARIOS = {
    "A_same": {
        "description": "Exact same prompt and settings to show warm-path behavior.",
        "measure": dict(BASE),
    },
    "B1_small_prompt_change": {
        "description": "Small prompt edit adds action/context.",
        "measure": {**BASE, "prompt": "a woman wearing a red hat and walking in the street"},
    },
    "B2_large_prompt_change": {
        "description": "Large prompt shift to a different scene/composition.",
        "measure": {**BASE, "prompt": "a futuristic city with flying cars at night, cinematic aerial shot"},
    },
    "C_seed_change": {
        "description": "Same prompt but different seed to force stochastic variation.",
        "measure": {**BASE, "seed": 91234567890123},
    },
    "D_model_change": {
        "description": "Change text encoder model (acts as model-path invalidation here).",
        "measure": {**BASE, "text_encoder": "t5xxl_fp8.safetensors"},
    },
}

MODES = [
    ("None", False, False),
    ("AttentionReuse", True, False),
    ("AttentionReuse+CPUOffload", True, True),
]


def is_link(value):
    return (
        isinstance(value, list)
        and len(value) == 2
        and str(value[0]).isdigit()
        and isinstance(value[1], int)
    )


def convert_refs(value, id_map):
    if is_link(value):
        return DataRef(id_map[str(value[0])], int(value[1]))
    if isinstance(value, list):
        return [convert_refs(v, id_map) for v in value]
    if isinstance(value, tuple):
        return tuple(convert_refs(v, id_map) for v in value)
    if isinstance(value, dict):
        return {k: convert_refs(v, id_map) for k, v in value.items()}
    return value


def build_prompt_map(wf, cfg):
    exported = json.loads(WORKFLOW_JSON.read_text(encoding="utf-8"))
    prompt_map = _convert_exported_to_prompt(exported, wf.registry)

    # Remove unknown/disconnected utility nodes (e.g. "Note") for strict servers.
    prompt_map = {
        node_id: node
        for node_id, node in prompt_map.items()
        if node.get("class_type") in wf.registry
    }

    for node in prompt_map.values():
        class_type = node.get("class_type")
        inputs = node.get("inputs", {})

        if class_type == "CheckpointLoaderSimple" and "ckpt_name" in inputs:
            inputs["ckpt_name"] = cfg["checkpoint"]
        if class_type == "CLIPLoader":
            if "clip_name" in inputs:
                inputs["clip_name"] = cfg["text_encoder"]
            if "text_encoder" in inputs:
                inputs["text_encoder"] = cfg["text_encoder"]
            if "model" in inputs:
                inputs["model"] = cfg["text_encoder"]
        if class_type == "CLIPTextEncode" and "text" in inputs:
            text_val = str(inputs["text"]).lower()
            if "worst quality" in text_val or "low quality" in text_val:
                inputs["text"] = cfg["negative_prompt"]
            else:
                inputs["text"] = cfg["prompt"]
        if class_type == "EmptyLTXVLatentVideo":
            if "length" in inputs:
                inputs["length"] = int(cfg["length"])
        if class_type == "LTXVScheduler":
            if "steps" in inputs:
                inputs["steps"] = int(cfg["steps"])
        if class_type == "SamplerCustom":
            if "noise_seed" in inputs:
                inputs["noise_seed"] = int(cfg["seed"])
            if "cfg" in inputs:
                inputs["cfg"] = float(cfg["cfg"])
        if class_type == "VHS_VideoCombine":
            if "filename_prefix" in inputs:
                inputs["filename_prefix"] = cfg["filename_prefix"]

    return prompt_map


def load_prompt_into_workflow(wf, prompt_map):
    wf.nodes = []
    wf.next_id = 1
    wf._reset_pipeline_state()
    wf._last_checkpoint = None

    ordered = list(prompt_map.items())
    id_map = {str(orig_id): str(i + 1) for i, (orig_id, _) in enumerate(ordered)}

    for orig_id, node in ordered:
        node_id = id_map[str(orig_id)]
        inputs = convert_refs(node.get("inputs", {}), id_map)
        wf.nodes.append(Node(node_id, node["class_type"], inputs, alias=None))

    wf.next_id = len(wf.nodes) + 1


def maybe_bind_checkpoint_for_plugin(wf, prompt_map):
    for node in prompt_map.values():
        if node.get("class_type") == "CheckpointLoaderSimple":
            ckpt = node.get("inputs", {}).get("ckpt_name")
            if ckpt:
                wf._active_checkpoint_name = str(ckpt)
                wf._active_checkpoint_model_object = wf.model_manager.get_model(str(ckpt))
                return


def configure_mode(wf, use_attention_reuse, use_cpu_offload):
    wf.disable_cache()
    wf.disable_memoization()

    if use_cpu_offload:
        wf.configure_model_manager(max_models_in_vram=1, enable_cpu_offload=True)

    if use_attention_reuse:
        wf.enable_attention_reuse(
            threshold=0.6,
            cache_device="cpu",
            store_frequency=2,
            reuse_layers=["cross_attention", "temporal_attention", "transformer_attention"],
            debug=False,
        )
    else:
        wf.disable_attention_reuse()


def wait_for_completion(wf, prompt_id, timeout_s=1800, poll_delay=2.0):
    started = time.perf_counter()
    while (time.perf_counter() - started) < timeout_s:
        history = wf.history(prompt_id=prompt_id)
        entry = history.get(prompt_id, history) if isinstance(history, dict) else history
        status = entry.get("status", {}) if isinstance(entry, dict) else {}
        if status.get("completed") is True:
            return
        time.sleep(poll_delay)
    raise TimeoutError(f"Timed out waiting for prompt completion: {prompt_id}")


def run_one(server, api_prefix, scenario_key, mode_name, use_attention_reuse, use_cpu_offload):
    wf = Workflow(server=server, api_prefix=api_prefix)
    cfg = dict(SCENARIOS[scenario_key]["measure"])
    cfg["filename_prefix"] = (
        f"bench_ltxv_{scenario_key}_{mode_name.lower().replace('+', '_').replace(' ', '_')}"
    )

    prompt_map = build_prompt_map(wf, cfg)
    load_prompt_into_workflow(wf, prompt_map)
    configure_mode(wf, use_attention_reuse=use_attention_reuse, use_cpu_offload=use_cpu_offload)
    maybe_bind_checkpoint_for_plugin(wf, prompt_map)

    started = time.perf_counter()
    result = wf.run(debug=False)
    prompt_id = result.get("prompt_id")
    if prompt_id:
        wait_for_completion(wf, prompt_id=prompt_id)
    elapsed = time.perf_counter() - started

    outputs = wf.saved_images(prompt_id=prompt_id, retries=8, delay=1.0) if prompt_id else []

    metrics = dict(result.get("execution_metrics", {}))
    if not wf.cache_enabled:
        metrics["cache_misses"] = metrics.get("executed_nodes", 0)

    return {
        "scenario": scenario_key,
        "mode": mode_name,
        "run": 1,
        "time_s": elapsed,
        "speedup_pct": 0.0,
        "executed_nodes": metrics.get("executed_nodes", 0),
        "skipped_nodes": metrics.get("skipped_nodes", 0),
        "cache_hits": metrics.get("cache_hits", 0),
        "cache_misses": metrics.get("cache_misses", 0),
        "sampler_runs": metrics.get("sampler_runs", 0),
        "attn_store": metrics.get("attn_store", 0),
        "attn_reuse": metrics.get("attn_reuse", 0),
        "attn_fallback": metrics.get("attn_fallback", 0),
        "prompt_id": prompt_id,
        "outputs_count": len(outputs),
    }


def compute_speedups(rows):
    baseline = {}
    for row in rows:
        if row["mode"] == "None":
            baseline[row["scenario"]] = row["time_s"]

    for row in rows:
        base = baseline.get(row["scenario"])
        if base and base > 0:
            row["speedup_pct"] = ((base - row["time_s"]) / base) * 100.0
        else:
            row["speedup_pct"] = 0.0


def render_table(rows):
    lines = [
        "| Scenario | Mode | Run | Time (s) | Speedup % | Exec Nodes | Skipped | Cache Hits | Cache Miss | Sampler Runs | Attn Store | Attn Reuse | Attn Fallback |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in rows:
        lines.append(
            f"| {row['scenario']} | {row['mode']} | {row['run']} | {row['time_s']:.3f} | {row['speedup_pct']:+.2f}% | "
            f"{row['executed_nodes']} | {row['skipped_nodes']} | {row['cache_hits']} | {row['cache_misses']} | "
            f"{row['sampler_runs']} | {row['attn_store']} | {row['attn_reuse']} | {row['attn_fallback']} |"
        )
    return "\n".join(lines)


def write_csv(rows, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "scenario",
        "mode",
        "run",
        "time_s",
        "speedup_pct",
        "executed_nodes",
        "skipped_nodes",
        "cache_hits",
        "cache_misses",
        "sampler_runs",
        "attn_store",
        "attn_reuse",
        "attn_fallback",
        "prompt_id",
        "outputs_count",
    ]
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def write_report(rows, path, server, api_prefix):
    lines = [
        "# LTXV Video Benchmark Report",
        "",
        f"Server: `{server}`",
        f"API prefix: `{api_prefix}`",
        "",
        "This benchmark runs true end-to-end video generation with `workflow_ep25_ltxv_text_to_video_mp4` and waits for completion before timing each run.",
        "",
        "## Scenarios",
    ]
    for key in ["A_same", "B1_small_prompt_change", "B2_large_prompt_change", "C_seed_change", "D_model_change"]:
        lines.append(f"- **{key}**: {SCENARIOS[key]['description']}")

    lines.extend([
        "",
        "## Results",
        "",
        render_table(rows),
        "",
        "## Notes",
        "",
        "- `D_model_change` uses text encoder change (`t5xxl_fp16` -> `t5xxl_fp8`) because only one LTXV checkpoint is available on this server.",
        "- `AttentionReuse` counters depend on compatible backend adapter interception. In this repo v1 compatibility mode, remote Comfy server execution may still show fallback-only counters.",
    ])

    text = "\n".join(lines)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Benchmark LTXV video generation with attention reuse modes.")
    parser.add_argument("--server", default="http://34.27.83.101")
    parser.add_argument("--api-prefix", default="/api")
    parser.add_argument("--output-root", default="tmp/outputs/benchmarks_ltxv_video")
    args = parser.parse_args()

    rows = []
    for scenario in ["A_same", "B1_small_prompt_change", "B2_large_prompt_change", "C_seed_change", "D_model_change"]:
        for mode_name, use_attention_reuse, use_cpu_offload in MODES:
            print(f"Running scenario={scenario} mode={mode_name}...")
            row = run_one(
                server=args.server,
                api_prefix=args.api_prefix,
                scenario_key=scenario,
                mode_name=mode_name,
                use_attention_reuse=use_attention_reuse,
                use_cpu_offload=use_cpu_offload,
            )
            rows.append(row)
            print(
                f"Done scenario={scenario} mode={mode_name} time={row['time_s']:.3f}s "
                f"attn(store/reuse/fallback)={row['attn_store']}/{row['attn_reuse']}/{row['attn_fallback']}"
            )

    compute_speedups(rows)

    output_root = Path(args.output_root)
    md_path = output_root / "benchmark_ltxv_video_attention_report.md"
    csv_path = output_root / "benchmark_ltxv_video_attention_report.csv"

    write_report(rows, md_path, args.server, args.api_prefix)
    write_csv(rows, csv_path)

    print(f"\nSaved report: {md_path.resolve()}")
    print(f"Saved csv: {csv_path.resolve()}")


if __name__ == "__main__":
    main()
