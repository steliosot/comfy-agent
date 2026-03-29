import re
from dataclasses import dataclass

from .artifacts import build_artifact, ensure_run_id, make_stage_prefix
from .workflow import Workflow

PLAN_VERSION = "1.0"


@dataclass
class SkillChoice:
    name: str
    confidence: float
    reason: str


def _extract_choices(registry, node_name, input_name):
    node_info = registry.get(node_name, {})
    required = node_info.get("input", {}).get("required", {})
    spec = required.get(input_name)
    if not spec:
        return []
    values = spec[0] if isinstance(spec, (list, tuple)) and spec else spec
    if isinstance(values, (list, tuple)):
        return [str(v) for v in values if str(v).strip()]
    return []


def _build_asset_inventory(wf):
    registry = wf.registry
    inventory = {
        "checkpoints": _extract_choices(registry, "CheckpointLoaderSimple", "ckpt_name"),
        "vae": _extract_choices(registry, "VAELoader", "vae_name"),
        "clip": _extract_choices(registry, "CLIPLoader", "clip_name"),
        "unet": _extract_choices(registry, "UNETLoader", "unet_name"),
        "lora": _extract_choices(registry, "LoraLoaderModelOnly", "lora_name"),
    }
    counts = {name: len(values) for name, values in inventory.items()}
    return {"assets": inventory, "counts": counts}


def _preflight_required_assets(inventory, skill_names, ckpt_name):
    required = []
    if "generate_video_clip" in skill_names:
        required.extend(
            [
                ("unet", "wan2.1/wan2.1_t2v_1.3B_fp16.safetensors"),
                ("clip", "umt5_xxl_fp8_e4m3fn_scaled.safetensors"),
                ("vae", "wan_2.1_vae.safetensors"),
            ]
        )
    else:
        required.append(("checkpoints", ckpt_name))

    missing = []
    for group, name in required:
        options = inventory["assets"].get(group, [])
        if not options:
            # Unknown list from server/mock; do not hard-fail.
            continue
        if name not in options:
            missing.append({"group": group, "name": name})

    return {
        "required": required,
        "missing": missing,
        "ok": len(missing) == 0,
    }


def _build_agentic_dependency_requirements(skill_names, ckpt_name, dependency_requirements=None):
    user = dependency_requirements if isinstance(dependency_requirements, dict) else {}
    models = list(user.get("models", [])) if isinstance(user.get("models"), list) else []
    custom_nodes = (
        list(user.get("custom_nodes", [])) if isinstance(user.get("custom_nodes"), list) else []
    )

    # Ensure core requirements are present for the current plan.
    if "generate_video_clip" in skill_names:
        defaults = [
            {"name": "wan2.1/wan2.1_t2v_1.3B_fp16.safetensors", "model_type": "unet"},
            {"name": "umt5_xxl_fp8_e4m3fn_scaled.safetensors", "model_type": "clip"},
            {"name": "wan_2.1_vae.safetensors", "model_type": "vae"},
        ]
        for item in defaults:
            if not any(
                isinstance(existing, dict)
                and str(existing.get("name", "")).lower() == item["name"].lower()
                for existing in models
            ):
                models.append(item)
        if not any(
            isinstance(entry, dict)
            and "VHS_VideoCombine" in (entry.get("expected_node_classes") or [])
            for entry in custom_nodes
        ):
            custom_nodes.append({"repo_url": None, "expected_node_classes": ["VHS_VideoCombine"]})
    else:
        if not any(
            isinstance(existing, dict)
            and str(existing.get("name", "")).lower() == ckpt_name.lower()
            for existing in models
        ):
            models.append({"name": ckpt_name, "model_type": "checkpoint"})

    merged = {
        "models": models,
        "custom_nodes": custom_nodes,
        "min_vram_mb": user.get("min_vram_mb"),
        "min_storage_gb": user.get("min_storage_gb"),
    }
    return merged


def _extract_crop_params(prompt):
    text = prompt.lower()
    params = {"x": 0, "y": 0, "width": 256, "height": 256}

    size_match = re.search(r"(\d{2,4})\s*[xX]\s*(\d{2,4})", text)
    if size_match:
        params["width"] = int(size_match.group(1))
        params["height"] = int(size_match.group(2))

    x_match = re.search(r"\bx\s*[:=]?\s*(\d{1,4})\b", text)
    y_match = re.search(r"\by\s*[:=]?\s*(\d{1,4})\b", text)
    if x_match:
        params["x"] = int(x_match.group(1))
    if y_match:
        params["y"] = int(y_match.group(1))

    return params


def _extract_generation_prompt(prompt):
    lowered = prompt.lower()
    split_tokens = [" then crop", " and then crop", " crop it", " and crop"]
    split_index = -1
    for token in split_tokens:
        index = lowered.find(token)
        if index != -1:
            split_index = index if split_index == -1 else min(split_index, index)

    if split_index == -1:
        return prompt.strip()

    return prompt[:split_index].strip().rstrip(",.")


def reason_skills(prompt):
    text = prompt.lower()
    wants_video = any(
        key in text
        for key in [
            "video",
            "video clip",
            "animation",
            "gif",
            "mp4",
            "webm",
            "h264",
            "webp",
            "t2v",
            "text-to-video",
        ]
    )
    wants_generate = any(
        key in text for key in ["generate", "create", "make", "photo", "image", "portrait"]
    )
    wants_crop = "crop" in text

    choices = []
    if wants_video:
        choices.append(
            SkillChoice(
                name="prepare_workflow_dependencies",
                confidence=0.9,
                reason="Preflight dependency validation and auto-fix.",
            )
        )
        choices.append(
            SkillChoice(
                name="generate_video_clip",
                confidence=0.97,
                reason="Prompt asks for video generation.",
            )
        )
        if wants_crop:
            choices.append(
                SkillChoice(
                    name="crop_image",
                    confidence=0.42,
                    reason="Crop requested, but current crop tool is image-only.",
                )
            )
    elif wants_generate:
        choices.append(
            SkillChoice(
                name="prepare_workflow_dependencies",
                confidence=0.9,
                reason="Preflight dependency validation and auto-fix.",
            )
        )
        choices.append(
            SkillChoice(
                name="generate_sd15_image",
                confidence=0.95 if not wants_crop else 0.98,
                reason="Prompt asks to generate an image.",
            )
        )

    if wants_crop and not wants_video:
        choices.append(
            SkillChoice(
                name="crop_image",
                confidence=0.96 if wants_generate else 0.90,
                reason="Prompt includes a crop operation.",
            )
        )

    if not choices:
        choices.append(
            SkillChoice(
                name="prepare_workflow_dependencies",
                confidence=0.78,
                reason="Preflight dependency validation before fallback generation.",
            )
        )
        choices.append(
            SkillChoice(
                name="generate_sd15_image",
                confidence=0.62,
                reason="Fallback to image generation when intent is ambiguous.",
            )
        )

    return choices


def reasoning_agentic(prompt, print_output=True):
    choices = reason_skills(prompt)
    skill_names = [choice.name for choice in choices]
    video = "generate_video_clip" in skill_names
    chain = "crop_image" in skill_names and "generate_sd15_image" in skill_names

    if video:
        plan = {
            "steps": ["prepare_workflow_dependencies", "generate_video_clip"],
            "generation_prompt": _extract_generation_prompt(prompt),
        }
        if "crop_image" in skill_names:
            plan["note"] = (
                "Crop was requested, but crop_image currently applies to still images only; "
                "video is generated without crop."
            )
    elif chain:
        crop_params = _extract_crop_params(prompt)
        plan = {
            "steps": ["prepare_workflow_dependencies", "generate_sd15_image", "crop_image"],
            "crop": crop_params,
            "generation_prompt": _extract_generation_prompt(prompt),
        }
    else:
        plan = {
            "steps": ["prepare_workflow_dependencies", "generate_sd15_image"],
            "generation_prompt": _extract_generation_prompt(prompt),
        }

    result = {
        "choices": [
            {
                "skill": choice.name,
                "confidence": round(choice.confidence, 4),
                "reason": choice.reason,
            }
            for choice in choices
        ],
        "plan": plan,
    }

    if print_output:
        print("Reasoning:")
        for choice in result["choices"]:
            print(
                f"- {choice['skill']}: confidence={choice['confidence']:.2f} "
                f"({choice['reason']})"
            )
        if chain:
            crop = result["plan"]["crop"]
            print(
                "Plan: generate_sd15_image -> crop_image "
                f"(x={crop['x']}, y={crop['y']}, width={crop['width']}, height={crop['height']})"
            )
        elif video:
            line = "Plan: generate_video_clip"
            note = result["plan"].get("note")
            if note:
                line += f" ({note})"
            print(line)
        else:
            print("Plan: generate_sd15_image")

    return result


def _default_plan_params(negative_prompt, ckpt_name):
    return {
        "negative_prompt": negative_prompt,
        "ckpt_name": ckpt_name,
        "filename_prefix": "agentic_generated",
        "video": {
            "unet_name": "wan2.1/wan2.1_t2v_1.3B_fp16.safetensors",
            "clip_name": "umt5_xxl_fp8_e4m3fn_scaled.safetensors",
            "vae_name": "wan_2.1_vae.safetensors",
            "width": 848,
            "height": 480,
            "length": 25,
            "seed": 226274808933316,
            "steps": 10,
            "cfg": 8,
            "sampler_name": "uni_pc",
            "scheduler": "simple",
            "denoise": 1,
            "frame_rate": 16,
            "loop_count": 0,
            "format": "video/h264-mp4",
            "pix_fmt": "yuv420p",
            "crf": 19,
            "save_metadata": True,
            "trim_to_audio": False,
            "pingpong": False,
            "save_output": True,
        },
    }


def _validate_plan_payload(plan_payload):
    if not isinstance(plan_payload, dict):
        return {
            "status": "error",
            "error": "invalid_plan_payload",
            "message": "plan_payload must be a JSON object/dict.",
        }

    version = plan_payload.get("plan_version")
    if version != PLAN_VERSION:
        return {
            "status": "error",
            "error": "unsupported_plan_version",
            "message": f"Unsupported plan_version '{version}'. Expected '{PLAN_VERSION}'.",
        }

    required = ["prompt", "generation_prompt", "steps", "params", "choices"]
    missing = [key for key in required if key not in plan_payload]
    if missing:
        return {
            "status": "error",
            "error": "invalid_plan_payload",
            "message": f"plan_payload is missing required fields: {', '.join(missing)}",
        }

    steps = plan_payload.get("steps")
    if not isinstance(steps, list) or not steps:
        return {
            "status": "error",
            "error": "invalid_plan_payload",
            "message": "plan_payload.steps must be a non-empty list.",
        }

    return None


def agentic_plan(
    prompt,
    server=None,
    headers=None,
    api_prefix=None,
    negative_prompt="watermark, text",
    ckpt_name="sd1.5/juggernaut_reborn.safetensors",
    auto_prepare=True,
    dependency_requirements=None,
):
    reasoning = reasoning_agentic(prompt, print_output=False)
    choices = reasoning.get("choices", [])
    steps = list(reasoning.get("plan", {}).get("steps", []))
    generation_prompt = reasoning.get("plan", {}).get("generation_prompt") or _extract_generation_prompt(
        prompt
    )
    params = _default_plan_params(negative_prompt=negative_prompt, ckpt_name=ckpt_name)
    warnings = []

    crop = reasoning.get("plan", {}).get("crop")
    if isinstance(crop, dict):
        params["crop"] = crop

    note = reasoning.get("plan", {}).get("note")
    if note:
        warnings.append(note)

    preflight = None
    if auto_prepare:
        from skills.infra.prepare_workflow_dependencies.skill import run as prepare_dependencies

        skill_names = [choice.get("skill") for choice in choices]
        prepare_requirements = _build_agentic_dependency_requirements(
            skill_names=skill_names,
            ckpt_name=ckpt_name,
            dependency_requirements=dependency_requirements,
        )
        preflight = prepare_dependencies(
            requirements=prepare_requirements,
            auto_fix=False,
            warn_only=True,
            server=server,
            headers=headers,
            api_prefix=api_prefix,
        )
        if not preflight.get("ready_for_run", False):
            warnings.append(
                "Dependency preflight indicates missing requirements; execution may fail until resolved."
            )

    return {
        "status": "planned",
        "plan_version": PLAN_VERSION,
        "prompt": prompt,
        "generation_prompt": generation_prompt,
        "choices": choices,
        "steps": steps,
        "params": params,
        "preflight": preflight,
        "warnings": warnings,
    }


def agentic_execute(
    plan_payload,
    server=None,
    headers=None,
    api_prefix=None,
    run_id=None,
    context=None,
):
    validation_error = _validate_plan_payload(plan_payload)
    if validation_error:
        return validation_error

    preflight = plan_payload.get("preflight")
    if isinstance(preflight, dict) and not preflight.get("ready_for_run", True):
        return {
            "status": "error",
            "error": "dependencies_not_ready",
            "message": (
                "Plan preflight reports dependencies not ready. Resolve missing models/custom nodes "
                "or regenerate plan after fixing dependencies."
            ),
            "preflight": preflight,
        }

    prompt = str(plan_payload.get("prompt", ""))
    generation_prompt = str(plan_payload.get("generation_prompt", ""))
    steps = [str(step) for step in plan_payload.get("steps", [])]
    params = plan_payload.get("params") if isinstance(plan_payload.get("params"), dict) else {}
    negative_prompt = params.get("negative_prompt", "watermark, text")
    ckpt_name = params.get("ckpt_name", "sd1.5/juggernaut_reborn.safetensors")
    filename_prefix = params.get("filename_prefix", "agentic_generated")
    crop_params = params.get("crop") if isinstance(params.get("crop"), dict) else None

    context = context if context is not None else {}
    resolved_run_id = ensure_run_id(context.get("run_id") or run_id)
    context["run_id"] = resolved_run_id

    wf = Workflow(server=server, headers=headers, api_prefix=api_prefix)

    if "generate_video_clip" in steps:
        video = params.get("video") if isinstance(params.get("video"), dict) else {}
        model = wf.unetloader(
            unet_name=video.get("unet_name", "wan2.1/wan2.1_t2v_1.3B_fp16.safetensors"),
            weight_dtype="default",
        )[0]
        clip = wf.cliploader(
            clip_name=video.get("clip_name", "umt5_xxl_fp8_e4m3fn_scaled.safetensors"),
            type="wan",
            device="default",
        )[0]
        vae = wf.vaeloader(vae_name=video.get("vae_name", "wan_2.1_vae.safetensors"))[0]
        pos = wf.cliptextencode(clip=clip, text=generation_prompt)[0]
        neg = wf.cliptextencode(clip=clip, text=negative_prompt)[0]
        latent = wf.emptyhunyuanlatentvideo(
            width=int(video.get("width", 848)),
            height=int(video.get("height", 480)),
            length=int(video.get("length", 25)),
            batch_size=1,
        )[0]
        samples = wf.ksampler(
            model=model,
            positive=pos,
            negative=neg,
            latent_image=latent,
            seed=int(video.get("seed", 226274808933316)),
            steps=int(video.get("steps", 10)),
            cfg=float(video.get("cfg", 8)),
            sampler_name=video.get("sampler_name", "uni_pc"),
            scheduler=video.get("scheduler", "simple"),
            denoise=float(video.get("denoise", 1)),
        )[0]
        images = wf.vaedecode(samples=samples, vae=vae)[0]
        wf.vhs_videocombine(
            images=images,
            vae=vae,
            frame_rate=int(video.get("frame_rate", 16)),
            loop_count=int(video.get("loop_count", 0)),
            filename_prefix=f"{make_stage_prefix(resolved_run_id, 'video')}_h264",
            format=video.get("format", "video/h264-mp4"),
            pix_fmt=video.get("pix_fmt", "yuv420p"),
            crf=int(video.get("crf", 19)),
            save_metadata=bool(video.get("save_metadata", True)),
            trim_to_audio=bool(video.get("trim_to_audio", False)),
            pingpong=bool(video.get("pingpong", False)),
            save_output=bool(video.get("save_output", True)),
        )
        run_result = wf.run()
        output_images = wf.saved_images(run_result.get("prompt_id"))
        artifacts = [
            build_artifact(
                role="output",
                remote_name=item.get("filename"),
                source="comfy_history",
                node_id=item.get("node_id"),
                subfolder=item.get("subfolder", ""),
                type=item.get("type", "output"),
                downloaded_path=None,
            )
            for item in output_images
        ]
        context["prompt_id"] = run_result.get("prompt_id")
        context["output_images"] = output_images
        context["artifacts"] = artifacts
        result = {
            "status": "done",
            "run_id": resolved_run_id,
            "plan": steps,
            "prompt_id": run_result.get("prompt_id"),
            "filename_prefix": make_stage_prefix(resolved_run_id, "video"),
            "output_images": output_images,
            "artifacts": artifacts,
            "preflight": preflight,
            "context": context,
        }
        if "crop_image" in steps:
            result["note"] = "Crop request detected, but video crop is not yet implemented in run_agentic."
        return result

    resolved_prefix = filename_prefix
    if filename_prefix == "agentic_generated":
        resolved_prefix = make_stage_prefix(resolved_run_id, "generate")
    model, clip, vae = wf.checkpointloadersimple(ckpt_name=ckpt_name)
    pos = wf.cliptextencode(clip=clip, text=generation_prompt)
    neg = wf.cliptextencode(clip=clip, text=negative_prompt)
    latent = wf.emptylatentimage(width=512, height=512, batch_size=1)
    samples = wf.ksampler(
        model=model,
        positive=pos,
        negative=neg,
        latent_image=latent,
        seed=1,
        steps=35,
        cfg=7.0,
        sampler_name="euler",
        scheduler="normal",
        denoise=1.0,
    )
    image = wf.vaedecode(samples=samples, vae=vae)
    wf.saveimage(images=image, filename_prefix=resolved_prefix)

    if "generate_sd15_image" in steps and "crop_image" in steps and isinstance(crop_params, dict):
        cropped = wf.imagecrop(
            image=image,
            x=int(crop_params.get("x", 0)),
            y=int(crop_params.get("y", 0)),
            width=int(crop_params.get("width", 256)),
            height=int(crop_params.get("height", 256)),
        )
        crop_prefix = make_stage_prefix(resolved_run_id, "crop")
        wf.saveimage(images=cropped, filename_prefix=crop_prefix)
        run_result = wf.run()
        output_images = wf.saved_images(run_result.get("prompt_id"))
        artifacts = [
            build_artifact(
                role="output",
                remote_name=item.get("filename"),
                source="comfy_history",
                node_id=item.get("node_id"),
                subfolder=item.get("subfolder", ""),
                type=item.get("type", "output"),
                downloaded_path=None,
            )
            for item in output_images
        ]
        context["prompt_id"] = run_result.get("prompt_id")
        context["output_images"] = output_images
        context["artifacts"] = artifacts
        return {
            "status": "done",
            "run_id": resolved_run_id,
            "plan": steps,
            "prompt_id": run_result.get("prompt_id"),
            "filename_prefix": crop_prefix,
            "output_images": output_images,
            "artifacts": artifacts,
            "preflight": preflight,
            "context": context,
        }

    run_result = wf.run()
    output_images = wf.saved_images(run_result.get("prompt_id"))
    artifacts = [
        build_artifact(
            role="output",
            remote_name=item.get("filename"),
            source="comfy_history",
            node_id=item.get("node_id"),
            subfolder=item.get("subfolder", ""),
            type=item.get("type", "output"),
            downloaded_path=None,
        )
        for item in output_images
    ]
    context["prompt_id"] = run_result.get("prompt_id")
    context["output_images"] = output_images
    context["artifacts"] = artifacts
    return {
        "status": "done",
        "skill": "generate_sd15_image",
        "run_id": resolved_run_id,
        "prompt_id": run_result.get("prompt_id"),
        "filename_prefix": resolved_prefix,
        "output_images": output_images,
        "artifacts": artifacts,
        "preflight": preflight,
        "context": context,
    }


def agentic_command(command_text, plan_payload=None, **runtime_kwargs):
    text = str(command_text or "").strip()
    if not text:
        return {
            "status": "error",
            "error": "empty_command",
            "message": "command_text must not be empty. Use '/plan <prompt>' or '/execute'.",
        }

    if text.startswith("/plan"):
        prompt = text[len("/plan") :].strip()
        if not prompt:
            return {
                "status": "error",
                "error": "missing_prompt",
                "message": "Use '/plan <prompt>' with a non-empty prompt.",
            }
        return agentic_plan(prompt=prompt, **runtime_kwargs)

    if text.startswith("/execute"):
        if plan_payload is None:
            return {
                "status": "error",
                "error": "missing_plan_payload",
                "message": "Provide plan_payload returned by agentic_plan before calling /execute.",
            }
        return agentic_execute(plan_payload=plan_payload, **runtime_kwargs)

    return {
        "status": "error",
        "error": "unknown_command",
        "message": "Unknown command. Supported commands: '/plan <prompt>' and '/execute'.",
    }


def run_agentic(
    prompt,
    server=None,
    headers=None,
    api_prefix=None,
    negative_prompt="watermark, text",
    ckpt_name="sd1.5/juggernaut_reborn.safetensors",
    filename_prefix="agentic_generated",
    print_reasoning=True,
    run_id=None,
    context=None,
    asset_preflight=True,
    auto_prepare=True,
    dependency_requirements=None,
):
    reasoning = reasoning_agentic(prompt, print_output=print_reasoning)
    choices = reason_skills(prompt)
    context = context if context is not None else {}
    resolved_run_id = ensure_run_id(context.get("run_id") or run_id)
    context["run_id"] = resolved_run_id

    skill_names = [choice.name for choice in choices]
    preflight = None
    if auto_prepare:
        from skills.infra.prepare_workflow_dependencies.skill import run as prepare_dependencies

        prepare_requirements = _build_agentic_dependency_requirements(
            skill_names=skill_names,
            ckpt_name=ckpt_name,
            dependency_requirements=dependency_requirements,
        )
        preflight = prepare_dependencies(
            requirements=prepare_requirements,
            auto_fix=True,
            warn_only=True,
            server=server,
            headers=headers,
            api_prefix=api_prefix,
        )
        context["dependency_preflight"] = preflight
        if not preflight.get("ready_for_run", False):
            return {
                "status": "error",
                "skill": "prepare_workflow_dependencies",
                "run_id": resolved_run_id,
                "error": "dependencies_not_ready",
                "message": (
                    "Workflow dependencies are not ready. Provide model/custom-node install specs "
                    "or verify ComfyUI-Manager availability."
                ),
                "preflight": preflight,
                "context": context,
            }
    elif asset_preflight:
        wf = Workflow(server=server, headers=headers, api_prefix=api_prefix)
        inventory = _build_asset_inventory(wf)
        preflight = _preflight_required_assets(inventory, skill_names, ckpt_name)
        preflight["inventory"] = inventory
        context["asset_preflight"] = preflight
        if not preflight["ok"]:
            return {
                "status": "error",
                "skill": "list_comfy_assets",
                "run_id": resolved_run_id,
                "error": "missing_required_assets",
                "missing_assets": preflight["missing"],
                "preflight": preflight,
                "context": context,
            }
    wf = Workflow(server=server, headers=headers, api_prefix=api_prefix)

    generation_prompt = _extract_generation_prompt(prompt)
    if "generate_video_clip" in skill_names:
        model = wf.unetloader(
            unet_name="wan2.1/wan2.1_t2v_1.3B_fp16.safetensors",
            weight_dtype="default",
        )[0]
        clip = wf.cliploader(
            clip_name="umt5_xxl_fp8_e4m3fn_scaled.safetensors",
            type="wan",
            device="default",
        )[0]
        vae = wf.vaeloader(vae_name="wan_2.1_vae.safetensors")[0]
        pos = wf.cliptextencode(clip=clip, text=generation_prompt)[0]
        neg = wf.cliptextencode(clip=clip, text=negative_prompt)[0]
        latent = wf.emptyhunyuanlatentvideo(width=848, height=480, length=25, batch_size=1)[0]
        samples = wf.ksampler(
            model=model,
            positive=pos,
            negative=neg,
            latent_image=latent,
            seed=226274808933316,
            steps=10,
            cfg=8,
            sampler_name="uni_pc",
            scheduler="simple",
            denoise=1,
        )[0]
        images = wf.vaedecode(samples=samples, vae=vae)[0]
        wf.vhs_videocombine(
            images=images,
            vae=vae,
            frame_rate=16,
            loop_count=0,
            filename_prefix=f"{make_stage_prefix(resolved_run_id, 'video')}_h264",
            format="video/h264-mp4",
            pix_fmt="yuv420p",
            crf=19,
            save_metadata=True,
            trim_to_audio=False,
            pingpong=False,
            save_output=True,
        )
        run_result = wf.run()
        output_images = wf.saved_images(run_result.get("prompt_id"))
        artifacts = [
            build_artifact(
                role="output",
                remote_name=item.get("filename"),
                source="comfy_history",
                node_id=item.get("node_id"),
                subfolder=item.get("subfolder", ""),
                type=item.get("type", "output"),
                downloaded_path=None,
            )
            for item in output_images
        ]
        context["prompt_id"] = run_result.get("prompt_id")
        context["output_images"] = output_images
        context["artifacts"] = artifacts
        output = {
            "status": "done",
            "run_id": resolved_run_id,
            "plan": ["prepare_workflow_dependencies", "generate_video_clip"],
            "prompt_id": run_result.get("prompt_id"),
            "filename_prefix": make_stage_prefix(resolved_run_id, "video"),
            "output_images": output_images,
            "artifacts": artifacts,
            "preflight": preflight,
            "context": context,
        }
        if "crop_image" in skill_names:
            output["note"] = (
                "Crop request detected, but video crop is not yet implemented in run_agentic."
            )
        return output

    resolved_prefix = filename_prefix
    if filename_prefix == "agentic_generated":
        resolved_prefix = make_stage_prefix(resolved_run_id, "generate")
    model, clip, vae = wf.checkpointloadersimple(ckpt_name=ckpt_name)
    pos = wf.cliptextencode(clip=clip, text=generation_prompt)
    neg = wf.cliptextencode(clip=clip, text=negative_prompt)
    latent = wf.emptylatentimage(width=512, height=512, batch_size=1)
    samples = wf.ksampler(
        model=model,
        positive=pos,
        negative=neg,
        latent_image=latent,
        seed=1,
        steps=35,
        cfg=7.0,
        sampler_name="euler",
        scheduler="normal",
        denoise=1.0,
    )
    image = wf.vaedecode(samples=samples, vae=vae)
    wf.saveimage(images=image, filename_prefix=resolved_prefix)

    if "generate_sd15_image" in skill_names and "crop_image" in skill_names:
        crop_params = reasoning["plan"]["crop"]
        cropped = wf.imagecrop(
            image=image,
            x=crop_params["x"],
            y=crop_params["y"],
            width=crop_params["width"],
            height=crop_params["height"],
        )
        crop_prefix = make_stage_prefix(resolved_run_id, "crop")
        wf.saveimage(images=cropped, filename_prefix=crop_prefix)
        run_result = wf.run()
        output_images = wf.saved_images(run_result.get("prompt_id"))
        artifacts = [
            build_artifact(
                role="output",
                remote_name=item.get("filename"),
                source="comfy_history",
                node_id=item.get("node_id"),
                subfolder=item.get("subfolder", ""),
                type=item.get("type", "output"),
                downloaded_path=None,
            )
            for item in output_images
        ]
        context["prompt_id"] = run_result.get("prompt_id")
        context["output_images"] = output_images
        context["artifacts"] = artifacts
        return {
            "status": "done",
            "run_id": resolved_run_id,
            "plan": ["prepare_workflow_dependencies", "generate_sd15_image", "crop_image"],
            "prompt_id": run_result.get("prompt_id"),
            "filename_prefix": crop_prefix,
            "output_images": output_images,
            "artifacts": artifacts,
            "preflight": preflight,
            "context": context,
        }

    run_result = wf.run()
    output_images = wf.saved_images(run_result.get("prompt_id"))
    artifacts = [
        build_artifact(
            role="output",
            remote_name=item.get("filename"),
            source="comfy_history",
            node_id=item.get("node_id"),
            subfolder=item.get("subfolder", ""),
            type=item.get("type", "output"),
            downloaded_path=None,
        )
        for item in output_images
    ]
    context["prompt_id"] = run_result.get("prompt_id")
    context["output_images"] = output_images
    context["artifacts"] = artifacts
    return {
        "status": "done",
        "skill": "generate_sd15_image",
        "run_id": resolved_run_id,
        "prompt_id": run_result.get("prompt_id"),
        "filename_prefix": resolved_prefix,
        "output_images": output_images,
        "artifacts": artifacts,
        "preflight": preflight,
        "context": context,
    }
