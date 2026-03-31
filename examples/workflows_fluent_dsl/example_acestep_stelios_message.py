"""Fluent DSL example: generate a short spoken/sung audio clip for
"hello there I am Stelios" on localhost using AceStep nodes.

This example intentionally uses infra dependency preflight first.
"""

from __future__ import annotations

import json
import time

from comfy_agent import Workflow
from skills.infra.prepare_workflow_dependencies.skill import run as prepare_dependencies


SERVER = "http://localhost:8000"
API_PREFIX = "/api"
MESSAGE = "hello there I am Stelios"
MODEL_NAME = "ace_step_v1_3.5b.safetensors"
MODEL_URL = (
    "https://huggingface.co/Comfy-Org/ACE-Step_ComfyUI_repackaged/resolve/main/"
    "all_in_one/ace_step_v1_3.5b.safetensors?download=true"
)


def ensure_dependencies():
    requirements = {
        "models": [
            {
                "name": MODEL_NAME,
                "filename": MODEL_NAME,
                "model_type": "checkpoint",
                "source": "huggingface",
                "model_id_or_url": MODEL_URL,
            }
        ]
    }
    result = prepare_dependencies(
        requirements=requirements,
        auto_fix=True,
        warn_only=True,
        server=SERVER,
        api_prefix=API_PREFIX,
    )
    print("[dependencies]", json.dumps(result, indent=2)[:1500])
    return result


def wait_for_completion(wf: Workflow, prompt_id: str, timeout_s: int = 600):
    started = time.perf_counter()
    while (time.perf_counter() - started) < timeout_s:
        entry = wf.history(prompt_id=prompt_id).get(prompt_id, {})
        status = entry.get("status", {}) if isinstance(entry, dict) else {}
        if status.get("completed") is True:
            return entry
        if status.get("status_str") == "error":
            return entry
        time.sleep(2)
    return {}


def main():
    ensure_dependencies()

    wf = Workflow(server=SERVER, api_prefix=API_PREFIX)

    ckpt = wf.checkpointloadersimple(ckpt_name=MODEL_NAME)
    model = wf.modelsamplingsd3(model=ckpt.MODEL, shift=4.0)
    pos = wf.textencodeacestepaudio(
        clip=ckpt.CLIP,
        tags="spoken word, clear voice, minimal background music",
        lyrics=MESSAGE,
        lyrics_strength=1,
    )
    neg = wf.conditioningzeroout(conditioning=pos.CONDITIONING)
    latent = wf.emptyacesteplatentaudio(seconds=16.0, batch_size=1)
    samples = wf.ksampler(
        model=model.MODEL,
        positive=pos.CONDITIONING,
        negative=neg.CONDITIONING,
        latent_image=latent.LATENT,
        seed=123456,
        steps=8,
        cfg=4,
        sampler_name="res_multistep",
        scheduler="simple",
        denoise=1,
    )
    audio = wf.vaedecodeaudio(samples=samples.LATENT, vae=ckpt.VAE)
    wf.saveaudio(audio=audio.AUDIO, filename_prefix="stelios_hello")

    result = wf.run(debug=False)
    prompt_id = result.get("prompt_id")
    print("[run]", json.dumps(result, indent=2))

    if not prompt_id:
        print("No prompt_id returned.")
        return

    entry = wait_for_completion(wf, prompt_id=prompt_id)
    status = entry.get("status", {}) if isinstance(entry, dict) else {}
    print("[history_status]", json.dumps(status, indent=2)[:2000])

    outputs = wf.saved_images(prompt_id=prompt_id, retries=6, delay=1)
    print("[outputs]", json.dumps(outputs, indent=2))

    for item in outputs:
        artifact = wf.download_image(item, output_dir="tmp/outputs")
        print("[downloaded]", json.dumps(artifact, indent=2))


if __name__ == "__main__":
    main()
