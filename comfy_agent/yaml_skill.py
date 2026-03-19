from pathlib import Path

import yaml

from .workflow import Workflow


def load_yaml_skill(
    path,
    *,
    workflow=None,
    comfy_url=None,
    server=None,
    headers=None,
    api_prefix=None,
    **inputs,
):
    config = yaml.safe_load(Path(path).read_text())
    if workflow is not None:
        wf = workflow
    else:
        wf = Workflow(
            comfy_url=comfy_url,
            server=server,
            headers=headers,
            api_prefix=api_prefix,
        )

    for step in config.get("graph", []):
        node = step["node"]
        params = dict(step.get("params", {}))

        input_name = step.get("input")
        if input_name:
            value = inputs[input_name]
            if node == "prompt":
                wf.prompt(value)
                continue
            if node == "negative":
                wf.negative(value)
                continue
            params[input_name] = value

        if node == "checkpoint":
            wf.checkpoint(params["ckpt_name"])
        elif node == "prompt":
            wf.prompt(params["text"])
        elif node == "negative":
            wf.negative(params["text"])
        elif node == "latent":
            wf.latent(
                params.get("width", 512),
                params.get("height", 512),
                params.get("batch_size", 1),
            )
        elif node == "sample":
            wf.sample(**params)
        elif node == "decode":
            wf.decode()
        elif node == "save":
            wf.save(params["filename_prefix"])
        elif node == "preview":
            wf.preview()
        else:
            raise ValueError(f"Unsupported YAML skill node '{node}'")

    return wf
