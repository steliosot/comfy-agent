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


def build(image=None,
          x=0,
          y=0,
          width=256,
          height=256,
          server=None,
          headers=None,
          api_prefix=None,
          filename_prefix="crop_result",
          workflow=None,
          image_ref=None):
    wf = workflow or Workflow(
        server or os.getenv("COMFY_URL"),
        headers=_resolve_headers(headers),
        api_prefix=api_prefix
    )

    if image_ref is not None:
        img = image_ref
    else:
        if image is None:
            raise ValueError("image is required when image_ref is not provided")
        img = wf.loadimage(
            image=image
        )[0]  # IMAGE output

    cropped = wf.imagecrop(
        image=img,
        x=x,
        y=y,
        width=width,
        height=height
    )

    wf.saveimage(
        images=cropped,
        filename_prefix=filename_prefix
    )

    return wf


def run(image,
        x=0,
        y=0,
        width=256,
        height=256,
        server=None,
        headers=None,
        api_prefix=None,
        filename_prefix="crop_result",
        run_id=None):
    resolved_run_id = ensure_run_id(run_id)
    resolved_prefix = filename_prefix
    if filename_prefix == "crop_result":
        resolved_prefix = make_stage_prefix(resolved_run_id, "crop")

    wf = build(
        image=image,
        x=x,
        y=y,
        width=width,
        height=height,
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
        "status": "ok",
        "skill": "crop_image",
        "run_id": resolved_run_id,
        "prompt_id": run_result.get("prompt_id"),
        "filename_prefix": resolved_prefix,
        "output_images": output_images,
        "artifacts": artifacts,
    }
