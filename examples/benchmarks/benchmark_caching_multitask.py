#!/usr/bin/env python3
import argparse
import copy
import csv
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from comfy_agent import Workflow


SCENARIO_ORDER = [
    "A_same",
    "B1_small_prompt_change",
    "B2_large_prompt_change",
    "C_seed_change",
    "D_model_change",
]

MODES = [
    ("None", False, False, False, 1),
    ("Cache", True, False, False, 2),
    ("Full", True, True, False, 3),
    ("AttentionReuse", False, False, True, 5),
]


@dataclass
class TaskSpec:
    name: str
    pipeline_note: str
    scenario_notes: Dict[str, str]
    base_config: Dict[str, object]
    scenarios: Dict[str, Dict[str, object]]
    skip_reasons: Dict[str, str]
    base_prefix: str


def now_ts() -> int:
    return int(time.time())


def mode_key(mode_name: str) -> str:
    return mode_name.lower()


def required_keys(registry: Dict[str, dict], class_type: str) -> List[str]:
    info = registry.get(class_type) or {}
    input_schema = info.get("input") if isinstance(info, dict) else {}
    required = input_schema.get("required", {}) if isinstance(input_schema, dict) else {}
    if not isinstance(required, dict):
        return []
    return list(required.keys())


def extract_options(registry: Dict[str, dict], class_type: str, input_name: str) -> List[str]:
    info = registry.get(class_type) or {}
    input_schema = info.get("input") if isinstance(info, dict) else {}
    required = input_schema.get("required", {}) if isinstance(input_schema, dict) else {}
    spec = required.get(input_name) if isinstance(required, dict) else None
    if not isinstance(spec, (list, tuple)) or not spec:
        return []
    first = spec[0]
    return first if isinstance(first, list) else []


def select_checkpoint_pair(ckpts: List[str]) -> Tuple[Optional[str], Optional[str]]:
    if not ckpts:
        return None, None
    base = ckpts[0]
    alt = None
    for candidate in ckpts:
        low = candidate.lower()
        if "sd1.5" in low or "sd15" in low or "juggernaut" in low:
            base = candidate
            break
    for candidate in ckpts:
        if candidate == base:
            continue
        low = candidate.lower()
        if "sdxl" in low or "xl" in low:
            alt = candidate
            break
    if alt is None:
        for candidate in ckpts:
            if candidate != base:
                alt = candidate
                break
    return base, alt


def find_input_image(user_path: Optional[str]) -> Path:
    if user_path:
        candidate = Path(user_path)
        if candidate.exists() and candidate.is_file():
            return candidate
    candidates = [
        Path("tmp/inputs/woman.png"),
        Path("tmp/inputs/St-Pauls-Cathedral.png"),
        Path("tmp/inputs/hat.jpeg"),
        Path("tmp/inputs/big_ben.jpeg"),
    ]
    for candidate in candidates:
        if candidate.exists() and candidate.is_file():
            return candidate
    for path in sorted(Path("tmp/inputs").glob("*")):
        if path.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"} and path.is_file():
            return path
    raise FileNotFoundError("No input image found. Provide --input-image or place one in tmp/inputs.")


def prepare_remote_image(local_path: Path) -> Dict[str, str]:
    wf = Workflow()
    remote_name = f"benchmark_multitask_{now_ts()}_{local_path.name}"
    uploaded = wf.upload_image(str(local_path), remote_name=remote_name, overwrite=True, type="input")
    return uploaded


def choose_upscale_capability(registry: Dict[str, dict]) -> Dict[str, object]:
    result = {
        "has_model_upscale": False,
        "has_scale_by": "ImageScaleBy" in registry,
        "has_scale": "ImageScale" in registry,
        "upscale_models": [],
    }
    if "UpscaleModelLoader" in registry and "ImageUpscaleWithModel" in registry:
        models = extract_options(registry, "UpscaleModelLoader", "model_name")
        if models:
            result["has_model_upscale"] = True
            result["upscale_models"] = models
    return result


def add_upscale_stage(wf: Workflow, config: Dict[str, object], registry: Dict[str, dict]) -> Tuple[bool, str]:
    caps = choose_upscale_capability(registry)
    image_ref = wf._current_image
    if image_ref is None:
        return False, "No image available for upscale stage."

    if caps["has_model_upscale"]:
        up_model = wf.node(
            "UpscaleModelLoader",
            __alias="upscale_model_loader",
            model_name=config["upscale_model_name"],
        )
        upscaled = wf.node(
            "ImageUpscaleWithModel",
            __alias="upscale_model",
            image=image_ref,
            upscale_model=up_model[0],
        )
        wf._current_image = upscaled[0]
        image_ref = wf._current_image

    if caps["has_scale_by"]:
        method = config.get("upscale_method", "lanczos")
        scale_by = float(config.get("scale_by", 1.0))
        scaled = wf.node(
            "ImageScaleBy",
            __alias="upscale",
            image=image_ref,
            upscale_method=method,
            scale_by=scale_by,
        )
        wf._current_image = scaled[0]
        return True, ""

    if caps["has_scale"]:
        method = config.get("upscale_method", "lanczos")
        width = int(config.get("target_width", 1024))
        height = int(config.get("target_height", 1024))
        kwargs = {
            "image": image_ref,
            "upscale_method": method,
            "width": width,
            "height": height,
        }
        req = set(required_keys(registry, "ImageScale"))
        if "crop" in req:
            kwargs["crop"] = "disabled"
        scaled = wf.node("ImageScale", __alias="upscale", **kwargs)
        wf._current_image = scaled[0]
        return True, ""

    if caps["has_model_upscale"]:
        return True, ""
    return False, "No upscale nodes available (expected ImageScaleBy/ImageScale/UpscaleModelLoader)."


def build_task_spec(task_name: str, registry: Dict[str, dict], remote_image_name: str) -> TaskSpec:
    ckpts = extract_options(registry, "CheckpointLoaderSimple", "ckpt_name")
    ckpt_base, ckpt_alt = select_checkpoint_pair(ckpts)
    upscale_caps = choose_upscale_capability(registry)
    up_models = upscale_caps["upscale_models"]
    up_model_base = up_models[0] if up_models else None
    up_model_alt = up_models[1] if len(up_models) > 1 else None

    skip_reasons: Dict[str, str] = {}

    if task_name in {"img2img", "inpaint", "img2img_then_upscale"} and not ckpt_base:
        for scenario in SCENARIO_ORDER:
            skip_reasons[scenario] = "No checkpoint models available on server."

    if task_name in {"upscale", "img2img_then_upscale"}:
        if not (
            upscale_caps["has_model_upscale"]
            or upscale_caps["has_scale_by"]
            or upscale_caps["has_scale"]
        ):
            for scenario in SCENARIO_ORDER:
                skip_reasons[scenario] = "No supported upscale node path available."

    if task_name == "img2img":
        base = {
            "checkpoint": ckpt_base,
            "prompt": "cinematic portrait of the same subject, soft lighting",
            "seed": 111,
            "denoise": 0.55,
            "source_image": remote_image_name,
        }
        scenarios = {
            "A_same": copy.deepcopy(base),
            "B1_small_prompt_change": {**base, "prompt": "cinematic portrait of the same subject, soft lighting, subtle hat"},
            "B2_large_prompt_change": {**base, "prompt": "futuristic neon cyberpunk portrait at night"},
            "C_seed_change": {**base, "seed": 222},
            "D_model_change": {**base, "checkpoint": ckpt_alt},
        }
        if not ckpt_alt:
            skip_reasons["D_model_change"] = "No alternate checkpoint found for model-change scenario."
        notes = {
            "A_same": "Same image, prompt, seed, denoise, and checkpoint for warm-cache behavior.",
            "B1_small_prompt_change": "Small prompt tweak while preserving composition style intent.",
            "B2_large_prompt_change": "Large prompt shift to force broader downstream recomputation.",
            "C_seed_change": "Same prompt and model, but different seed to isolate sampler-sensitive changes.",
            "D_model_change": "Switch checkpoint to force broad invalidation and full recompute pressure.",
        }
        return TaskSpec(
            name=task_name,
            pipeline_note="Load image -> VAE encode -> KSampler img2img -> decode -> save.",
            scenario_notes=notes,
            base_config=base,
            scenarios=scenarios,
            skip_reasons=skip_reasons,
            base_prefix="benchmark_multitask_img2img",
        )

    if task_name == "inpaint":
        base = {
            "checkpoint": ckpt_base,
            "prompt": "remove the foreground logo and preserve realistic fabric texture",
            "seed": 333,
            "denoise": 0.65,
            "grow_mask_by": 6,
            "source_image": remote_image_name,
        }
        scenarios = {
            "A_same": copy.deepcopy(base),
            "B1_small_prompt_change": {
                **base,
                "prompt": "remove small foreground logo, preserve realistic fabric texture",
                "grow_mask_by": 8,
            },
            "B2_large_prompt_change": {
                **base,
                "prompt": "replace foreground region with a clean futuristic metallic badge",
                "grow_mask_by": 18,
            },
            "C_seed_change": {**base, "seed": 444},
            "D_model_change": {**base, "checkpoint": ckpt_alt},
        }
        if "VAEEncodeForInpaint" not in registry:
            for scenario in SCENARIO_ORDER:
                skip_reasons[scenario] = "VAEEncodeForInpaint not available on server."
        if not ckpt_alt:
            skip_reasons["D_model_change"] = "No alternate checkpoint found for model-change scenario."
        notes = {
            "A_same": "Same inpaint setup and mask growth for warm-cache baseline.",
            "B1_small_prompt_change": "Small edit instruction change plus modest mask growth adjustment.",
            "B2_large_prompt_change": "Large edit instruction change with broader mask growth.",
            "C_seed_change": "Same edit instruction/mask setup, different seed for stochastic variation.",
            "D_model_change": "Switch checkpoint to force model-path invalidation.",
        }
        return TaskSpec(
            name=task_name,
            pipeline_note="Load image (+mask) -> VAEEncodeForInpaint -> KSampler -> decode -> save.",
            scenario_notes=notes,
            base_config=base,
            scenarios=scenarios,
            skip_reasons=skip_reasons,
            base_prefix="benchmark_multitask_inpaint",
        )

    if task_name == "upscale":
        base = {
            "source_image": remote_image_name,
            "upscale_model_name": up_model_base,
            "scale_by": 1.0,
            "upscale_method": "lanczos",
            "target_width": 1024,
            "target_height": 1024,
        }
        scenarios = {
            "A_same": copy.deepcopy(base),
            "B1_small_prompt_change": {**base, "scale_by": 1.2},
            "B2_large_prompt_change": {**base, "scale_by": 1.8},
            "C_seed_change": {**base, "upscale_method": "nearest-exact"},
            "D_model_change": {**base, "upscale_model_name": up_model_alt},
        }
        if not up_model_base and not (upscale_caps["has_scale_by"] or upscale_caps["has_scale"]):
            for scenario in SCENARIO_ORDER:
                skip_reasons[scenario] = "No usable upscale path available."
        if up_model_base and not up_model_alt:
            skip_reasons["D_model_change"] = "Only one upscaler model found; cannot run model-change scenario."
        if not up_model_base and (upscale_caps["has_scale_by"] or upscale_caps["has_scale"]):
            skip_reasons["D_model_change"] = "No upscaler model loader available for model-change scenario."
        notes = {
            "A_same": "Same source and upscale controls for warm-cache baseline.",
            "B1_small_prompt_change": "Small upscale-control change (`scale_by` slight increase).",
            "B2_large_prompt_change": "Large upscale-control change (`scale_by` larger increase).",
            "C_seed_change": "Non-seeded track: changed deterministic upscale control (`upscale_method`).",
            "D_model_change": "Switch upscaler model when available to force model-path invalidation.",
        }
        return TaskSpec(
            name=task_name,
            pipeline_note="Load image -> model upscaler and/or scale node -> save.",
            scenario_notes=notes,
            base_config=base,
            scenarios=scenarios,
            skip_reasons=skip_reasons,
            base_prefix="benchmark_multitask_upscale",
        )

    if task_name == "img2img_then_upscale":
        base = {
            "checkpoint": ckpt_base,
            "prompt": "studio portrait remix, preserve identity and upscale cleanly",
            "seed": 555,
            "denoise": 0.5,
            "source_image": remote_image_name,
            "upscale_model_name": up_model_base,
            "scale_by": 1.25,
            "upscale_method": "lanczos",
            "target_width": 1280,
            "target_height": 1280,
        }
        scenarios = {
            "A_same": copy.deepcopy(base),
            "B1_small_prompt_change": {**base, "prompt": "studio portrait remix, preserve identity, slight glossy skin retouch"},
            "B2_large_prompt_change": {**base, "prompt": "dramatic cyberpunk portrait remix with neon reflections and rain"},
            "C_seed_change": {**base, "seed": 666},
            "D_model_change": {**base, "checkpoint": ckpt_alt},
        }
        if not ckpt_alt:
            skip_reasons["D_model_change"] = "No alternate checkpoint found for model-change scenario."
        if not (
            upscale_caps["has_model_upscale"]
            or upscale_caps["has_scale_by"]
            or upscale_caps["has_scale"]
        ):
            for scenario in SCENARIO_ORDER:
                skip_reasons[scenario] = "No upscale stage available for combo pipeline."
        notes = {
            "A_same": "Same img2img + upscale stack to measure best-case reuse in a deeper graph.",
            "B1_small_prompt_change": "Small prompt change in img2img branch; upscale branch unchanged.",
            "B2_large_prompt_change": "Large prompt shift to trigger heavier img2img recomputation before upscale.",
            "C_seed_change": "Seed change at sampler; verifies stochastic invalidation in combo pipeline.",
            "D_model_change": "Checkpoint switch to force broad invalidation across combo pipeline.",
        }
        return TaskSpec(
            name=task_name,
            pipeline_note="Load image -> img2img branch -> decode -> upscale stage -> save.",
            scenario_notes=notes,
            base_config=base,
            scenarios=scenarios,
            skip_reasons=skip_reasons,
            base_prefix="benchmark_multitask_img2img_upscale",
        )

    raise ValueError(f"Unsupported task: {task_name}")


def build_workflow_for_task(task: str, config: Dict[str, object]) -> Workflow:
    wf = Workflow()
    if task in {"img2img", "img2img_then_upscale", "inpaint"}:
        wf.checkpoint(str(config["checkpoint"]))
        wf.prompt(str(config["prompt"]))
        wf.load_image(str(config["source_image"]))

    if task == "img2img":
        wf.encode()
        wf.sample(seed=int(config["seed"]), steps=20, cfg=8, sampler_name="euler", denoise=float(config["denoise"]))
        wf.decode()
    elif task == "inpaint":
        if "VAEEncodeForInpaint" not in wf.registry:
            raise RuntimeError("VAEEncodeForInpaint not available.")
        inpaint_latent = wf.node(
            "VAEEncodeForInpaint",
            __alias="inpaint_encode",
            pixels=wf._current_image,
            mask=wf._current_mask,
            vae=wf._current_vae,
            grow_mask_by=int(config["grow_mask_by"]),
        )
        wf._current_latent = inpaint_latent[0]
        wf.sample(seed=int(config["seed"]), steps=20, cfg=8, sampler_name="euler", denoise=float(config["denoise"]))
        wf.decode()
    elif task == "upscale":
        wf.load_image(str(config["source_image"]))
        ok, reason = add_upscale_stage(wf, config=config, registry=wf.registry)
        if not ok:
            raise RuntimeError(reason)
    elif task == "img2img_then_upscale":
        wf.encode()
        wf.sample(seed=int(config["seed"]), steps=20, cfg=8, sampler_name="euler", denoise=float(config["denoise"]))
        wf.decode()
        ok, reason = add_upscale_stage(wf, config=config, registry=wf.registry)
        if not ok:
            raise RuntimeError(reason)
    else:
        raise ValueError(f"Unsupported task: {task}")

    wf.save("benchmark_placeholder")
    return wf


def apply_overrides(task: str, wf: Workflow, config: Dict[str, object], filename_prefix: str) -> None:
    overrides = {"save.filename_prefix": filename_prefix}
    if task in {"img2img", "inpaint", "img2img_then_upscale"}:
        overrides["checkpoint.ckpt_name"] = config["checkpoint"]
        overrides["prompt.text"] = config["prompt"]
        overrides["load_image.image"] = config["source_image"]
    if task in {"img2img", "img2img_then_upscale"}:
        overrides["ksampler.seed"] = int(config["seed"])
        overrides["ksampler.denoise"] = float(config["denoise"])
    if task == "inpaint":
        overrides["inpaint_encode.grow_mask_by"] = int(config["grow_mask_by"])
        overrides["ksampler.seed"] = int(config["seed"])
        overrides["ksampler.denoise"] = float(config["denoise"])

    if task in {"upscale", "img2img_then_upscale"}:
        if "upscale_model_loader" in [n.alias for n in wf.nodes]:
            overrides["upscale_model_loader.model_name"] = config.get("upscale_model_name")
        if "upscale" in [n.alias for n in wf.nodes]:
            node = wf._find_node("upscale")
            if "scale_by" in node.inputs:
                overrides["upscale.scale_by"] = float(config.get("scale_by", 1.0))
            if "upscale_method" in node.inputs:
                overrides["upscale.upscale_method"] = str(config.get("upscale_method", "lanczos"))
            if "width" in node.inputs:
                overrides["upscale.width"] = int(config.get("target_width", 1024))
            if "height" in node.inputs:
                overrides["upscale.height"] = int(config.get("target_height", 1024))

    wf.override(overrides)


def configure_mode(
    wf: Workflow,
    use_cache: bool,
    use_memo: bool,
    use_attention_reuse: bool,
) -> None:
    if use_cache:
        wf.enable_cache(policy="LRU", size=256)
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


def wait_for_completion(wf: Workflow, prompt_id: str, timeout_s: int, poll_delay: float) -> None:
    started = time.perf_counter()
    while (time.perf_counter() - started) < timeout_s:
        history = wf.history(prompt_id=prompt_id)
        entry = history.get(prompt_id, history) if isinstance(history, dict) else history
        status = entry.get("status", {}) if isinstance(entry, dict) else {}
        if status.get("completed") is True:
            return
        time.sleep(poll_delay)
    raise TimeoutError(f"Timed out waiting for prompt completion: {prompt_id}")


def run_one(
    task: str,
    wf: Workflow,
    config: Dict[str, object],
    mode_name: str,
    run_no: int,
    output_root: Path,
    timeout_s: int,
    poll_delay: float,
    scenario: str,
) -> Dict[str, object]:
    row_output_dir = output_root / task / scenario / mode_key(mode_name) / f"run_{run_no}"
    row_output_dir.mkdir(parents=True, exist_ok=True)
    prefix = f"{task}_{scenario}_{mode_key(mode_name)}_run{run_no}_{now_ts()}"

    apply_overrides(task=task, wf=wf, config=config, filename_prefix=prefix)
    started = time.perf_counter()
    result = wf.run(target="save", debug=False)
    prompt_id = result.get("prompt_id")
    metrics = dict(result.get("execution_metrics", {}))

    downloaded = []
    status = "ok"
    reason = ""
    try:
        if prompt_id:
            wait_for_completion(wf, prompt_id=prompt_id, timeout_s=timeout_s, poll_delay=poll_delay)
            downloaded = wf.download_saved_images(
                prompt_id=prompt_id,
                output_dir=str(row_output_dir),
                filename_strategy="{index}_{filename}",
                retries=max(3, int(timeout_s / max(1, int(poll_delay * 10)))),
                delay=poll_delay,
            )
    except Exception as exc:
        status = "error"
        reason = str(exc)

    elapsed = time.perf_counter() - started
    if not wf.cache_enabled:
        metrics["cache_misses"] = metrics.get("executed_nodes", 0)
    metrics["skipped_nodes"] = metrics.get("skipped_nodes", 0) + metrics.get("cache_hits", 0)
    return {
        "task": task,
        "scenario": scenario,
        "mode": mode_name,
        "run": run_no,
        "time_s": elapsed,
        "speedup_pct": 0.0,
        "executed_nodes": int(metrics.get("executed_nodes", 0)),
        "skipped_nodes": int(metrics.get("skipped_nodes", 0)),
        "cache_hits": int(metrics.get("cache_hits", 0)),
        "cache_misses": int(metrics.get("cache_misses", 0)),
        "sampler_runs": int(metrics.get("sampler_runs", 0)),
        "status": status,
        "reason": reason,
        "output_dir": str(row_output_dir.resolve()),
        "downloaded_count": len(downloaded),
        "prompt_id": prompt_id or "",
    }


def run_task_scenario(
    spec: TaskSpec,
    scenario: str,
    mode: Tuple[str, bool, bool, int],
    output_root: Path,
    timeout_s: int,
    poll_delay: float,
) -> Dict[str, object]:
    mode_name, use_cache, use_memo, use_attention_reuse, run_no = mode
    if scenario in spec.skip_reasons:
        return {
            "task": spec.name,
            "scenario": scenario,
            "mode": mode_name,
            "run": run_no,
            "time_s": None,
            "speedup_pct": None,
            "executed_nodes": 0,
            "skipped_nodes": 0,
            "cache_hits": 0,
            "cache_misses": 0,
            "sampler_runs": 0,
            "status": "skipped",
            "reason": spec.skip_reasons[scenario],
            "output_dir": "",
            "downloaded_count": 0,
            "prompt_id": "",
        }

    wf = build_workflow_for_task(spec.name, spec.base_config)
    configure_mode(
        wf=wf,
        use_cache=use_cache,
        use_memo=use_memo,
        use_attention_reuse=use_attention_reuse,
    )

    if use_cache:
        warmup = copy.deepcopy(spec.base_config)
        run_one(
            task=spec.name,
            wf=wf,
            config=warmup,
            mode_name=mode_name,
            run_no=0,
            output_root=output_root,
            timeout_s=timeout_s,
            poll_delay=poll_delay,
            scenario="warmup",
        )

    scenario_cfg = copy.deepcopy(spec.scenarios[scenario])
    return run_one(
        task=spec.name,
        wf=wf,
        config=scenario_cfg,
        mode_name=mode_name,
        run_no=run_no,
        output_root=output_root,
        timeout_s=timeout_s,
        poll_delay=poll_delay,
        scenario=scenario,
    )


def compute_speedups(rows: List[Dict[str, object]]) -> None:
    index = {}
    for row in rows:
        if row["status"] != "ok" or row["time_s"] is None:
            continue
        index[(row["task"], row["scenario"], row["mode"])] = row

    for row in rows:
        if row["status"] != "ok" or row["time_s"] is None:
            row["speedup_pct"] = None
            continue
        baseline = index.get((row["task"], row["scenario"], "None"))
        if not baseline or not baseline.get("time_s"):
            row["speedup_pct"] = None
            continue
        base_time = float(baseline["time_s"])
        this_time = float(row["time_s"])
        if base_time <= 0:
            row["speedup_pct"] = None
            continue
        row["speedup_pct"] = ((base_time - this_time) / base_time) * 100.0


def row_sort_key(row: Dict[str, object]) -> Tuple[int, int, int]:
    scenario_idx = SCENARIO_ORDER.index(row["scenario"]) if row["scenario"] in SCENARIO_ORDER else 99
    mode_idx = next((i for i, m in enumerate(MODES) if m[0] == row["mode"]), 99)
    run_no = int(row["run"])
    return scenario_idx, mode_idx, run_no


def format_table(rows: List[Dict[str, object]]) -> str:
    lines = [
        "| Scenario | Mode   | Run | Time (s) | Speedup % | Exec Nodes | Skipped | Cache Hits | Cache Miss | Sampler Runs |",
        "|----------|--------|-----|----------|-----------|------------|---------|------------|------------|--------------|",
    ]
    for row in sorted(rows, key=row_sort_key):
        if row["status"] != "ok" or row["time_s"] is None:
            lines.append(
                f"| {row['scenario']} | {row['mode']:<6} | {row['run']} | n/a | n/a | n/a | n/a | n/a | n/a | n/a |"
            )
            continue
        speed = row["speedup_pct"]
        speed_text = f"{speed:+.1f}%" if speed is not None else "n/a"
        lines.append(
            f"| {row['scenario']} | {row['mode']:<6} | {row['run']} | "
            f"{float(row['time_s']):.3f} | {speed_text} | "
            f"{row['executed_nodes']} | {row['skipped_nodes']} | "
            f"{row['cache_hits']} | {row['cache_misses']} | {row['sampler_runs']} |"
        )
    return "\n".join(lines)


def write_csv(rows: List[Dict[str, object]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "task",
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
                "status",
                "reason",
                "downloaded_count",
                "prompt_id",
                "output_dir",
            ],
        )
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def build_report(
    task_specs: Dict[str, TaskSpec],
    rows: List[Dict[str, object]],
    output_root: Path,
    local_input: Path,
    remote_image_name: str,
) -> str:
    lines = [
        "# Multi-Task Caching Benchmark Report",
        "",
        f"- Generated at: `{datetime.now(timezone.utc).isoformat()}`",
        f"- Local input image: `{local_input.resolve()}`",
        f"- Uploaded remote input: `{remote_image_name}`",
        "- Timing mode: end-to-end completion (run + wait + output download).",
        "",
        "## Scenario Definitions",
        "",
        "- `A_same`: exact same inputs/settings (warm-cache best case).",
        "- `B1_small_prompt_change`: small prompt/control change.",
        "- `B2_large_prompt_change`: large prompt/control change.",
        "- `C_seed_change`: seed change or closest stochastic/control equivalent.",
        "- `D_model_change`: model/upscaler model switch for broad invalidation.",
    ]

    for task_name in [name for name in ["img2img", "upscale", "inpaint", "img2img_then_upscale"] if name in task_specs]:
        spec = task_specs[task_name]
        task_rows = [row for row in rows if row["task"] == task_name]
        lines.extend(
            [
                "",
                f"## Task: `{task_name}`",
                "",
                f"- Pipeline: {spec.pipeline_note}",
                "- Scenario notes:",
            ]
        )
        for scenario in SCENARIO_ORDER:
            lines.append(f"  - `{scenario}`: {spec.scenario_notes[scenario]}")
        lines.extend(["", format_table(task_rows)])

        skipped = [r for r in task_rows if r["status"] == "skipped"]
        errors = [r for r in task_rows if r["status"] == "error"]
        if skipped or errors:
            lines.extend(["", "- Notes:"])
            for row in skipped:
                lines.append(f"  - Skipped `{row['scenario']}` / `{row['mode']}`: {row['reason']}")
            for row in errors:
                lines.append(f"  - Error `{row['scenario']}` / `{row['mode']}`: {row['reason']}")

        lines.extend(["", "- Speedup summary vs `None`:"])
        for scenario in SCENARIO_ORDER:
            base = next((r for r in task_rows if r["scenario"] == scenario and r["mode"] == "None"), None)
            cache = next((r for r in task_rows if r["scenario"] == scenario and r["mode"] == "Cache"), None)
            full = next((r for r in task_rows if r["scenario"] == scenario and r["mode"] == "Full"), None)
            if not base or not cache or not full:
                lines.append(f"  - `{scenario}`: n/a")
                continue
            lines.append(
                f"  - `{scenario}`: Cache `{speedup_cell(cache)}`, Full `{speedup_cell(full)}`"
            )

    lines.extend(
        [
            "",
            "## Output Files",
            "",
            f"- Markdown report: `{(output_root / 'benchmark_caching_multitask_report.md').resolve()}`",
            f"- CSV report: `{(output_root / 'benchmark_caching_multitask_report.csv').resolve()}`",
        ]
    )
    return "\n".join(lines)


def speedup_cell(row: Dict[str, object]) -> str:
    value = row.get("speedup_pct")
    if value is None:
        return "n/a"
    return f"{float(value):+.1f}%"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Benchmark cache/memoization across multiple image tasks.")
    parser.add_argument(
        "--tasks",
        nargs="+",
        default=["img2img", "upscale", "inpaint", "img2img_then_upscale"],
        choices=["img2img", "upscale", "inpaint", "img2img_then_upscale"],
        help="Task tracks to run.",
    )
    parser.add_argument("--input-image", default="", help="Local image path for image-based tasks.")
    parser.add_argument("--output-root", default="tmp/outputs/benchmarks_multitask", help="Output root folder.")
    parser.add_argument("--timeout-s", type=int, default=300, help="Per-run wait timeout in seconds.")
    parser.add_argument("--poll-delay", type=float, default=0.5, help="Completion poll interval seconds.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output_root = Path(args.output_root)
    output_root.mkdir(parents=True, exist_ok=True)

    local_input = find_input_image(args.input_image)
    uploaded = prepare_remote_image(local_input)
    remote_image_name = uploaded["remote_name"]

    bootstrap = Workflow()
    task_specs = {
        task_name: build_task_spec(task_name, registry=bootstrap.registry, remote_image_name=remote_image_name)
        for task_name in args.tasks
    }

    rows: List[Dict[str, object]] = []
    for task_name in args.tasks:
        spec = task_specs[task_name]
        for scenario in SCENARIO_ORDER:
            for mode in MODES:
                rows.append(
                    run_task_scenario(
                        spec=spec,
                        scenario=scenario,
                        mode=mode,
                        output_root=output_root,
                        timeout_s=args.timeout_s,
                        poll_delay=args.poll_delay,
                    )
                )

    compute_speedups(rows)

    md_path = output_root / "benchmark_caching_multitask_report.md"
    csv_path = output_root / "benchmark_caching_multitask_report.csv"
    report = build_report(
        task_specs=task_specs,
        rows=rows,
        output_root=output_root,
        local_input=local_input,
        remote_image_name=remote_image_name,
    )
    md_path.write_text(report, encoding="utf-8")
    write_csv(rows, csv_path)

    print(report)
    print(f"\nSaved markdown: {md_path.resolve()}")
    print(f"Saved csv: {csv_path.resolve()}")


if __name__ == "__main__":
    main()
