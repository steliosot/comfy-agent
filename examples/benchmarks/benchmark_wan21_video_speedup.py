#!/usr/bin/env python3
import argparse
import csv
import json
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import requests

from comfy_agent import Workflow


SERVER_DEFAULT = "http://34.27.83.101"
API_PREFIX_DEFAULT = "/api"

VIDEO_PROFILE = {
    "unet_name": "wan2.1/wan2.1_t2v_1.3B_fp16.safetensors",
    "clip_name": "umt5_xxl_fp8_e4m3fn_scaled.safetensors",
    "vae_name": "wan_2.1_vae.safetensors",
    "width": 848,
    "height": 480,
    "frame_rate": 8,
    "length": 40,
    "batch_size": 1,
    "steps": 8,
    "cfg": 8.0,
    "sampler_name": "uni_pc",
    "scheduler": "simple",
    "denoise": 1.0,
    "negative_prompt": "Overexposure, static, blurred details, low quality, artifacts",
}

BASE = {
    **VIDEO_PROFILE,
    "prompt": "a woman wearing a red hat",
    "seed": 226274808933316,
}

SCENARIOS = {
    "A_same": {
        "description": "Exact same prompt/settings to measure warm-path behavior.",
        "config": dict(BASE),
    },
    "B1_small_prompt_change": {
        "description": "Small prompt edit: add simple action/context.",
        "config": {**BASE, "prompt": "a woman wearing a red hat and walking in the street"},
    },
    "B2_large_prompt_change": {
        "description": "Large prompt shift to a different scene/composition.",
        "config": {
            **BASE,
            "prompt": "futuristic city skyline at sunset with flying cars, cinematic aerial shot",
        },
    },
    "C_seed_change": {
        "description": "Same prompt/settings with a different seed.",
        "config": {**BASE, "seed": 84572319877311},
    },
}

STAGE1_MODES: List[str] = [
    "None",
    "Cache",
    "Full",
    "Full+CPUOffload",
    "AttentionReuse_WAN21",
    "AttentionReuse_WAN21+CPUOffload",
]

MODE_NOTES = {
    "None": "No cache/memoization/attention reuse/model offload.",
    "Cache": "Deterministic cache enabled only.",
    "Full": "Cache + graph memoization.",
    "Full+CPUOffload": "Cache + memoization + ModelManager CPU offload.",
    "AttentionReuse_WAN21": "WAN21 attention-reuse profile (adapter-dependent) only.",
    "AttentionReuse_WAN21+CPUOffload": "WAN21 attention-reuse profile + CPU offload.",
}


@dataclass
class PreflightResult:
    ok: bool
    warnings: List[str]
    failures: List[str]


@dataclass
class Row:
    stage: str
    scenario: str
    mode: str
    run: int
    time_s: Optional[float]
    speedup_pct: Optional[float]
    executed_nodes: int
    skipped_nodes: int
    cache_hits: int
    cache_misses: int
    sampler_runs: int
    attn_store: int
    attn_reuse: int
    attn_fallback: int
    prompt_id: str
    outputs_count: int
    status: str
    reason: str


def wait_for_completion(wf: Workflow, prompt_id: str, timeout_s: int = 3600, poll_delay: float = 2.0) -> None:
    started = time.perf_counter()
    while (time.perf_counter() - started) < timeout_s:
        history = wf.history(prompt_id=prompt_id)
        entry = history.get(prompt_id, history) if isinstance(history, dict) else history
        status = entry.get("status", {}) if isinstance(entry, dict) else {}
        if status.get("completed") is True:
            return
        time.sleep(poll_delay)
    raise TimeoutError(f"Timed out waiting for completion: prompt_id={prompt_id}")


def build_wan21_workflow(server: str, api_prefix: str, cfg: Dict[str, object], filename_prefix: str) -> Workflow:
    wf = Workflow(server=server, api_prefix=api_prefix)

    model = wf.unetloader(unet_name=cfg["unet_name"], weight_dtype="default")[0]
    clip = wf.cliploader(clip_name=cfg["clip_name"], type="wan", device="default")[0]
    vae = wf.vaeloader(vae_name=cfg["vae_name"])[0]

    pos = wf.cliptextencode(clip=clip, text=cfg["prompt"])[0]
    neg = wf.cliptextencode(clip=clip, text=cfg["negative_prompt"])[0]

    latent = wf.emptyhunyuanlatentvideo(
        width=int(cfg["width"]),
        height=int(cfg["height"]),
        length=int(cfg["length"]),
        batch_size=int(cfg["batch_size"]),
    )[0]

    samples = wf.ksampler(
        model=model,
        positive=pos,
        negative=neg,
        latent_image=latent,
        seed=int(cfg["seed"]),
        steps=int(cfg["steps"]),
        cfg=float(cfg["cfg"]),
        sampler_name=str(cfg["sampler_name"]),
        scheduler=str(cfg["scheduler"]),
        denoise=float(cfg["denoise"]),
    )[0]

    images = wf.vaedecode(samples=samples, vae=vae)[0]

    wf.vhs_videocombine(
        images=images,
        vae=vae,
        frame_rate=int(cfg["frame_rate"]),
        loop_count=0,
        filename_prefix=filename_prefix,
        format="video/h264-mp4",
        pix_fmt="yuv420p",
        crf=19,
        save_metadata=True,
        trim_to_audio=False,
        pingpong=False,
        save_output=True,
    )

    return wf


def apply_mode(wf: Workflow, mode: str) -> None:
    wf.disable_cache()
    wf.disable_memoization()
    wf.disable_attention_reuse()

    if mode == "None":
        return

    if mode == "Cache":
        wf.enable_cache(policy="LRU", size=256)
        return

    if mode == "Full":
        wf.enable_cache(policy="LRU", size=256)
        wf.enable_memoization()
        return

    if mode == "Full+CPUOffload":
        wf.enable_cache(policy="LRU", size=256)
        wf.enable_memoization()
        wf.configure_model_manager(max_models_in_vram=1, enable_cpu_offload=True)
        return

    if mode == "AttentionReuse_WAN21":
        wf.enable_attention_reuse(
            threshold=0.6,
            cache_device="cpu",
            store_frequency=2,
            reuse_layers=["cross_attention", "temporal_attention", "transformer_attention"],
        )
        return

    if mode == "AttentionReuse_WAN21+CPUOffload":
        wf.configure_model_manager(max_models_in_vram=1, enable_cpu_offload=True)
        wf.enable_attention_reuse(
            threshold=0.6,
            cache_device="cpu",
            store_frequency=2,
            reuse_layers=["cross_attention", "temporal_attention", "transformer_attention"],
        )
        return

    raise ValueError(f"Unsupported mode: {mode}")


def preflight(server: str, api_prefix: str) -> PreflightResult:
    warnings: List[str] = []
    failures: List[str] = []

    wf = Workflow(server=server, api_prefix=api_prefix)

    # Model checks via /api/models/*
    try:
        diffusion_models = requests.get(f"{wf.url}/models/diffusion_models", headers=wf.headers, timeout=30).json()
        text_encoders = requests.get(f"{wf.url}/models/text_encoders", headers=wf.headers, timeout=30).json()
        vaes = requests.get(f"{wf.url}/models/vae", headers=wf.headers, timeout=30).json()
    except Exception as exc:
        failures.append(f"Failed to query model endpoints: {exc}")
        return PreflightResult(ok=False, warnings=warnings, failures=failures)

    if VIDEO_PROFILE["unet_name"] not in diffusion_models:
        failures.append(f"Missing UNet model: {VIDEO_PROFILE['unet_name']}")
    if VIDEO_PROFILE["clip_name"] not in text_encoders:
        warnings.append(f"Text encoder not found exactly: {VIDEO_PROFILE['clip_name']} (will still attempt run)")
    if VIDEO_PROFILE["vae_name"] not in vaes:
        failures.append(f"Missing VAE model: {VIDEO_PROFILE['vae_name']}")

    # Node checks
    required_nodes = [
        "UNETLoader",
        "CLIPLoader",
        "VAELoader",
        "CLIPTextEncode",
        "EmptyHunyuanLatentVideo",
        "KSampler",
        "VAEDecode",
        "VHS_VideoCombine",
    ]
    for node in required_nodes:
        if node not in wf.registry:
            failures.append(f"Missing required node: {node}")

    return PreflightResult(ok=not failures, warnings=warnings, failures=failures)


def run_single(
    server: str,
    api_prefix: str,
    output_root: Path,
    stage: str,
    scenario: str,
    mode: str,
    run_no: int,
    cfg: Dict[str, object],
    timeout_s: int,
) -> Row:
    row_dir = output_root / stage / scenario / mode.lower().replace("+", "_plus_") / f"run_{run_no}"
    row_dir.mkdir(parents=True, exist_ok=True)
    prefix = f"wan21_{scenario}_{mode.lower().replace('+','_plus_')}_run{run_no}_{int(time.time())}"

    try:
        wf = build_wan21_workflow(server=server, api_prefix=api_prefix, cfg=cfg, filename_prefix=prefix)
        apply_mode(wf, mode)

        # Warm-up only when cache is enabled to capture best-case repeat path.
        if wf.cache_enabled:
            warm_cfg = dict(cfg)
            warm_cfg["seed"] = int(cfg["seed"])
            warm_wf = build_wan21_workflow(server=server, api_prefix=api_prefix, cfg=warm_cfg, filename_prefix=prefix + "_warmup")
            apply_mode(warm_wf, mode)
            warm_wf.run(debug=False)

        started = time.perf_counter()
        result = wf.run(debug=False)
        prompt_id = result.get("prompt_id", "")
        if prompt_id:
            wait_for_completion(wf, prompt_id=prompt_id, timeout_s=timeout_s)
            downloaded = wf.download_saved_images(
                prompt_id=prompt_id,
                output_dir=str(row_dir),
                retries=12,
                delay=1.0,
            )
        else:
            downloaded = []
        elapsed = time.perf_counter() - started

        metrics = dict(result.get("execution_metrics", {}))
        if not wf.cache_enabled:
            metrics["cache_misses"] = metrics.get("executed_nodes", 0)

        return Row(
            stage=stage,
            scenario=scenario,
            mode=mode,
            run=run_no,
            time_s=elapsed,
            speedup_pct=None,
            executed_nodes=int(metrics.get("executed_nodes", 0)),
            skipped_nodes=int(metrics.get("skipped_nodes", 0)),
            cache_hits=int(metrics.get("cache_hits", 0)),
            cache_misses=int(metrics.get("cache_misses", 0)),
            sampler_runs=int(metrics.get("sampler_runs", 0)),
            attn_store=int(metrics.get("attn_store", 0)),
            attn_reuse=int(metrics.get("attn_reuse", 0)),
            attn_fallback=int(metrics.get("attn_fallback", 0)),
            prompt_id=str(prompt_id),
            outputs_count=len(downloaded),
            status="ok",
            reason="",
        )
    except Exception as exc:
        return Row(
            stage=stage,
            scenario=scenario,
            mode=mode,
            run=run_no,
            time_s=None,
            speedup_pct=None,
            executed_nodes=0,
            skipped_nodes=0,
            cache_hits=0,
            cache_misses=0,
            sampler_runs=0,
            attn_store=0,
            attn_reuse=0,
            attn_fallback=0,
            prompt_id="",
            outputs_count=0,
            status="error",
            reason=str(exc),
        )


def compute_speedups(rows: List[Row]) -> None:
    baseline: Dict[Tuple[str, str], float] = {}
    for row in rows:
        if row.status == "ok" and row.mode == "None" and row.time_s is not None:
            baseline[(row.stage, row.scenario)] = row.time_s

    for row in rows:
        row.speedup_pct = None
        if row.status != "ok" or row.time_s is None:
            continue
        base = baseline.get((row.stage, row.scenario))
        if base and base > 0:
            row.speedup_pct = ((base - row.time_s) / base) * 100.0


def pick_top3_from_stage1(rows: List[Row]) -> List[str]:
    stage1 = [r for r in rows if r.stage == "stage1" and r.scenario == "A_same" and r.status == "ok" and r.time_s is not None]
    if not stage1:
        return ["None"]

    by_mode: Dict[str, float] = {}
    for r in stage1:
        by_mode[r.mode] = r.time_s

    non_none = sorted([(m, t) for m, t in by_mode.items() if m != "None"], key=lambda x: x[1])
    selected = ["None"]
    for m, _ in non_none[:2]:
        selected.append(m)
    # ensure unique and deterministic fallback
    if len(selected) < 3:
        for m in STAGE1_MODES:
            if m not in selected:
                selected.append(m)
            if len(selected) == 3:
                break
    return selected[:3]


def render_table(rows: List[Row]) -> str:
    lines = [
        "| Scenario | Mode | Run | Time (s) | Speedup % | Exec Nodes | Skipped | Cache Hits | Cache Miss | Sampler Runs | Attn Store | Attn Reuse | Attn Fallback |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for r in rows:
        if r.status != "ok" or r.time_s is None:
            lines.append(
                f"| {r.scenario} | {r.mode} | {r.run} | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |"
            )
            continue
        speed = f"{r.speedup_pct:+.2f}%" if r.speedup_pct is not None else "n/a"
        lines.append(
            f"| {r.scenario} | {r.mode} | {r.run} | {r.time_s:.3f} | {speed} | "
            f"{r.executed_nodes} | {r.skipped_nodes} | {r.cache_hits} | {r.cache_misses} | {r.sampler_runs} | "
            f"{r.attn_store} | {r.attn_reuse} | {r.attn_fallback} |"
        )
    return "\n".join(lines)


def write_csv(rows: List[Row], csv_path: Path) -> None:
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "stage",
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
        "status",
        "reason",
    ]
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for r in rows:
            writer.writerow({
                "stage": r.stage,
                "scenario": r.scenario,
                "mode": r.mode,
                "run": r.run,
                "time_s": "" if r.time_s is None else f"{r.time_s:.6f}",
                "speedup_pct": "" if r.speedup_pct is None else f"{r.speedup_pct:.6f}",
                "executed_nodes": r.executed_nodes,
                "skipped_nodes": r.skipped_nodes,
                "cache_hits": r.cache_hits,
                "cache_misses": r.cache_misses,
                "sampler_runs": r.sampler_runs,
                "attn_store": r.attn_store,
                "attn_reuse": r.attn_reuse,
                "attn_fallback": r.attn_fallback,
                "prompt_id": r.prompt_id,
                "outputs_count": r.outputs_count,
                "status": r.status,
                "reason": r.reason,
            })


def summarize_best(rows: List[Row], selected_modes: List[str]) -> Tuple[str, str, str]:
    stage2 = [r for r in rows if r.stage == "stage2" and r.status == "ok" and r.time_s is not None]
    if not stage2:
        return ("n/a", "n/a", "No successful stage2 runs.")

    # Best absolute latency (across stage2 rows)
    best_row = min(stage2, key=lambda r: r.time_s or 1e18)
    best_abs = f"{best_row.mode} ({best_row.scenario}, {best_row.time_s:.2f}s)"

    # Best average speedup over B1/B2/C
    scenario_set = {"B1_small_prompt_change", "B2_large_prompt_change", "C_seed_change"}
    by_mode: Dict[str, List[float]] = {}
    for r in stage2:
        if r.scenario in scenario_set and r.speedup_pct is not None:
            by_mode.setdefault(r.mode, []).append(r.speedup_pct)

    best_mode = "n/a"
    best_avg = "n/a"
    if by_mode:
        ranked = sorted(((m, sum(v) / len(v)) for m, v in by_mode.items() if v), key=lambda x: x[1], reverse=True)
        if ranked:
            best_mode, avg = ranked[0]
            best_avg = f"{avg:+.2f}%"

    # Attention reuse fallback note
    attn_rows = [r for r in stage2 if "AttentionReuse" in r.mode]
    if attn_rows and all((r.attn_store == 0 and r.attn_reuse == 0) for r in attn_rows):
        attn_note = "Attention reuse stayed fallback-only on this server (no reuse hits observed)."
    elif attn_rows:
        attn_note = "Attention reuse produced non-zero store/reuse counters on this server."
    else:
        attn_note = "No attention-reuse mode in selected stage2 modes."

    return best_abs, f"{best_mode} ({best_avg})", attn_note


def estimate_runtime(rows: List[Row], stage1_modes_count: int, stage2_modes_count: int) -> str:
    ok_rows = [r for r in rows if r.status == "ok" and r.time_s is not None]
    if not ok_rows:
        return (
            "Estimated runtime for this benchmark shape is ~60-120 minutes total "
            "(per-run ~3-6 minutes for 5s WAN2.1 video), with queue contention potentially extending to ~2-3 hours."
        )
    avg = sum(r.time_s for r in ok_rows if r.time_s is not None) / len(ok_rows)
    planned_total_runs = stage1_modes_count + (len(SCENARIOS) * stage2_modes_count)
    est_total = avg * planned_total_runs
    return (
        f"Observed mean per-run time: {avg:.1f}s. "
        f"Estimated full staged benchmark time for {planned_total_runs} runs: ~{est_total/60:.1f} minutes "
        f"(~{est_total/3600:.2f} hours), excluding queue spikes."
    )


def write_markdown(
    rows: List[Row],
    md_path: Path,
    server: str,
    api_prefix: str,
    preflight_result: PreflightResult,
    selected_modes: List[str],
    runtime_note: str,
) -> None:
    md_path.parent.mkdir(parents=True, exist_ok=True)

    stage1_rows = [r for r in rows if r.stage == "stage1"]
    stage2_rows = [r for r in rows if r.stage == "stage2"]

    best_abs, best_avg, attn_note = summarize_best(rows, selected_modes)

    lines: List[str] = [
        "# WAN2.1 5s Video Speedup Benchmark Report",
        "",
        f"- Server: `{server}`",
        f"- API Prefix: `{api_prefix}`",
        (
            f"- Video profile: {VIDEO_PROFILE['width']}x{VIDEO_PROFILE['height']}, "
            f"{VIDEO_PROFILE['frame_rate']}fps, length={VIDEO_PROFILE['length']} frames "
            f"(~{VIDEO_PROFILE['length']/VIDEO_PROFILE['frame_rate']:.1f}s), "
            f"steps={VIDEO_PROFILE['steps']}, WAN2.1 1.3B"
        ),
        "- Timing mode: end-to-end completion (run + wait + output download).",
        "",
        "## Preflight",
    ]

    if preflight_result.ok:
        lines.append("- Status: PASS")
    else:
        lines.append("- Status: FAIL")

    for w in preflight_result.warnings:
        lines.append(f"- Warning: {w}")
    for f in preflight_result.failures:
        lines.append(f"- Failure: {f}")

    lines.extend([
        "",
        "## Scenarios",
        "- `A_same`: Exact same prompt/settings to measure warm-path behavior.",
        "- `B1_small_prompt_change`: Small prompt edit.",
        "- `B2_large_prompt_change`: Large prompt shift.",
        "- `C_seed_change`: Same prompt/settings with different seed.",
        "",
        "## Mode Notes",
    ])
    for mode in STAGE1_MODES:
        lines.append(f"- `{mode}`: {MODE_NOTES.get(mode, '')}")

    lines.extend([
        "",
        "## Stage 1 (A_same shortlist)",
        render_table(stage1_rows),
        "",
        f"Selected Stage 2 modes: `{', '.join(selected_modes)}`",
        "",
        "## Stage 2 (A/B1/B2/C)",
        render_table(stage2_rows),
        "",
        "## Recommendation",
        f"- Best absolute latency: {best_abs}",
        f"- Best average speedup on B1/B2/C: {best_avg}",
        f"- Attention reuse note: {attn_note}",
        "",
        "## Runtime Estimate",
        f"- {runtime_note}",
        "",
        "## Errors / Skips",
    ])

    bad_rows = [r for r in rows if r.status != "ok"]
    if bad_rows:
        for r in bad_rows:
            lines.append(f"- `{r.stage}` `{r.scenario}` `{r.mode}`: {r.status} - {r.reason}")
    else:
        lines.append("- None")

    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="WAN2.1 staged video benchmark for optimization speedups")
    parser.add_argument("--server", default=SERVER_DEFAULT)
    parser.add_argument("--api-prefix", default=API_PREFIX_DEFAULT)
    parser.add_argument("--output-root", default="tmp/outputs/benchmarks_wan21_video")
    parser.add_argument("--timeout-s", type=int, default=3600)
    args = parser.parse_args()

    output_root = Path(args.output_root)
    output_root.mkdir(parents=True, exist_ok=True)

    pre = preflight(server=args.server, api_prefix=args.api_prefix)

    rows: List[Row] = []
    if not pre.ok:
        # Save failure report even if we cannot run.
        runtime_note = (
            "Benchmark did not run due to preflight failures. "
            "Expected runtime for successful runs is typically 60-120 minutes total for this staged plan."
        )
        md_path = output_root / "benchmark_wan21_video_report.md"
        csv_path = output_root / "benchmark_wan21_video_report.csv"
        write_csv(rows, csv_path)
        write_markdown(rows, md_path, args.server, args.api_prefix, pre, ["None"], runtime_note)
        print(f"Preflight failed. Saved report: {md_path.resolve()}")
        print(f"Saved csv: {csv_path.resolve()}")
        return 1

    # Stage 1: A_same across all modes.
    for mode in STAGE1_MODES:
        print(f"[Stage1] scenario=A_same mode={mode}")
        row = run_single(
            server=args.server,
            api_prefix=args.api_prefix,
            output_root=output_root,
            stage="stage1",
            scenario="A_same",
            mode=mode,
            run_no=1,
            cfg=dict(SCENARIOS["A_same"]["config"]),
            timeout_s=args.timeout_s,
        )
        rows.append(row)
        print(f"  -> status={row.status} time={row.time_s}")

    # Pick top 3 (always include None)
    selected_modes = pick_top3_from_stage1(rows)

    # Stage 2: selected modes across all requested scenarios.
    for scenario in ["A_same", "B1_small_prompt_change", "B2_large_prompt_change", "C_seed_change"]:
        for mode in selected_modes:
            print(f"[Stage2] scenario={scenario} mode={mode}")
            row = run_single(
                server=args.server,
                api_prefix=args.api_prefix,
                output_root=output_root,
                stage="stage2",
                scenario=scenario,
                mode=mode,
                run_no=1,
                cfg=dict(SCENARIOS[scenario]["config"]),
                timeout_s=args.timeout_s,
            )
            rows.append(row)
            print(f"  -> status={row.status} time={row.time_s}")

    compute_speedups(rows)
    runtime_note = estimate_runtime(rows, stage1_modes_count=len(STAGE1_MODES), stage2_modes_count=len(selected_modes))

    md_path = output_root / "benchmark_wan21_video_report.md"
    csv_path = output_root / "benchmark_wan21_video_report.csv"

    write_csv(rows, csv_path)
    write_markdown(rows, md_path, args.server, args.api_prefix, pre, selected_modes, runtime_note)

    print(f"Saved report: {md_path.resolve()}")
    print(f"Saved csv: {csv_path.resolve()}")
    print(f"Selected modes for stage2: {selected_modes}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
