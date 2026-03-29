import os

from comfy_agent import Workflow
from comfy_agent.artifacts import build_artifact, ensure_run_id, make_stage_prefix


def _resolve_headers(headers):
    if headers is not None:
        return headers

    auth_header = os.getenv("COMFY_AUTH_HEADER")
    if auth_header:
        return {"Authorization": auth_header}

    return None


def build(prompt,
          negative_prompt="watermark, text",
          width=512,
          height=512,
          steps=35,
          server=None,
          headers=None,
          api_prefix=None,
          filename_prefix="generated",
          workflow=None,
          save=True,
          return_image=False):
    wf = workflow or Workflow(
        server or os.getenv("COMFY_URL"),
        headers=_resolve_headers(headers),
        api_prefix=api_prefix
    )

    model, clip, vae = wf.checkpointloadersimple(
        ckpt_name="sd1.5/juggernaut_reborn.safetensors"
    )

    pos = wf.cliptextencode(
        clip=clip,
        text=prompt
    )

    neg = wf.cliptextencode(
        clip=clip,
        text=negative_prompt
    )

    latent = wf.emptylatentimage(
        width=width,
        height=height,
        batch_size=1
    )

    samples = wf.ksampler(
        model=model,
        positive=pos,
        negative=neg,
        latent_image=latent,
        seed=1,
        steps=steps,
        cfg=7,
        sampler_name="euler",
        scheduler="normal",
        denoise=1
    )

    img = wf.vaedecode(
        samples=samples,
        vae=vae
    )

    if save:
        wf.saveimage(
            images=img,
            filename_prefix=filename_prefix
        )

    if return_image:
        return wf, img

    return wf


def run(prompt,
        negative_prompt="watermark, text",
        width=512,
        height=512,
        steps=35,
        server=None,
        headers=None,
        api_prefix=None,
        filename_prefix="generated",
        run_id=None):
    resolved_run_id = ensure_run_id(run_id)
    resolved_prefix = filename_prefix
    if filename_prefix == "generated":
        resolved_prefix = make_stage_prefix(resolved_run_id, "generate")

    wf = build(
        prompt=prompt,
        negative_prompt=negative_prompt,
        width=width,
        height=height,
        steps=steps,
        server=server,
        headers=headers,
        api_prefix=api_prefix,
        filename_prefix=resolved_prefix
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

    return {
        "status": "done",
        "skill": "generate_sd15_image",
        "run_id": resolved_run_id,
        "prompt_id": run_result.get("prompt_id"),
        "filename_prefix": resolved_prefix,
        "output_images": output_images,
        "artifacts": artifacts,
    }
