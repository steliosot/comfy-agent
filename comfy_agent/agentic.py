import re
from dataclasses import dataclass

from .workflow import Workflow


@dataclass
class SkillChoice:
    name: str
    confidence: float
    reason: str


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
    wants_generate = any(
        key in text for key in ["generate", "create", "make", "photo", "image", "portrait"]
    )
    wants_crop = "crop" in text

    choices = []
    if wants_generate:
        choices.append(
            SkillChoice(
                name="generate_sd15_image",
                confidence=0.95 if not wants_crop else 0.98,
                reason="Prompt asks to generate an image.",
            )
        )

    if wants_crop:
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
                name="generate_sd15_image",
                confidence=0.62,
                reason="Fallback to image generation when intent is ambiguous.",
            )
        )

    return choices


def run_agentic(
    prompt,
    server=None,
    headers=None,
    api_prefix=None,
    negative_prompt="watermark, text",
    ckpt_name="sd1.5/juggernaut_reborn.safetensors",
    filename_prefix="agentic_generated",
):
    choices = reason_skills(prompt)
    print("Reasoning:")
    for choice in choices:
        print(f"- {choice.name}: confidence={choice.confidence:.2f} ({choice.reason})")

    wf = Workflow(server=server, headers=headers, api_prefix=api_prefix)
    skill_names = [choice.name for choice in choices]

    generation_prompt = _extract_generation_prompt(prompt)
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
    wf.saveimage(images=image, filename_prefix=filename_prefix)

    if "generate_sd15_image" in skill_names and "crop_image" in skill_names:
        crop_params = _extract_crop_params(prompt)
        print(
            "Plan: generate_sd15_image -> crop_image "
            f"(x={crop_params['x']}, y={crop_params['y']}, "
            f"width={crop_params['width']}, height={crop_params['height']})"
        )
        cropped = wf.imagecrop(
            image=image,
            x=crop_params["x"],
            y=crop_params["y"],
            width=crop_params["width"],
            height=crop_params["height"],
        )
        wf.saveimage(images=cropped, filename_prefix="agentic_cropped")
        run_result = wf.run()
        return {
            "status": "done",
            "plan": ["generate_sd15_image", "crop_image"],
            "prompt_id": run_result.get("prompt_id"),
            "output_images": wf.saved_images(run_result.get("prompt_id")),
        }

    print("Plan: generate_sd15_image")
    run_result = wf.run()
    return {
        "status": "done",
        "skill": "generate_sd15_image",
        "prompt_id": run_result.get("prompt_id"),
        "filename_prefix": filename_prefix,
        "output_images": wf.saved_images(run_result.get("prompt_id")),
    }

