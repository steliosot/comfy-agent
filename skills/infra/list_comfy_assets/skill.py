from pathlib import Path

from comfy_agent import Workflow
from comfy_agent.config import ComfyConfig


def _extract_choices(registry, node_name, input_name):
    node_info = registry.get(node_name, {})
    required = node_info.get("input", {}).get("required", {})
    spec = required.get(input_name)
    if not spec:
        return []
    raw = spec[0] if isinstance(spec, (list, tuple)) and spec else spec
    if isinstance(raw, (list, tuple)):
        return sorted({str(item) for item in raw if str(item).strip()})
    return []


def _list_files(directory, extensions=None):
    path = Path(directory)
    if not path.exists() or not path.is_dir():
        return []
    files = []
    for item in path.iterdir():
        if not item.is_file():
            continue
        if extensions and item.suffix.lower() not in extensions:
            continue
        files.append(item.name)
    return sorted(files)


def run(
    server=None,
    headers=None,
    api_prefix=None,
    include_files=True,
):
    cfg = ComfyConfig.from_env(load_env=True)
    wf = Workflow(
        server=server or cfg.server,
        headers=headers if headers is not None else (cfg.headers or None),
        api_prefix=api_prefix if api_prefix is not None else cfg.api_prefix,
    )
    registry = wf.registry

    assets = {
        "checkpoints": _extract_choices(registry, "CheckpointLoaderSimple", "ckpt_name"),
        "vae": _extract_choices(registry, "VAELoader", "vae_name"),
        "clip": _extract_choices(registry, "CLIPLoader", "clip_name"),
        "lora": _extract_choices(registry, "LoraLoaderModelOnly", "lora_name"),
        "unet": _extract_choices(registry, "UNETLoader", "unet_name"),
        "input_files": [],
        "output_files": [],
    }

    if include_files:
        image_exts = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tiff"}
        assets["input_files"] = _list_files(cfg.input_dir, extensions=image_exts)
        assets["output_files"] = _list_files(cfg.output_dir, extensions=image_exts)

    counts = {k: len(v) for k, v in assets.items()}

    return {
        "status": "ok",
        "skill": "list_comfy_assets",
        "server": wf.url,
        "counts": counts,
        "assets": assets,
        "input_dir": str(Path(cfg.input_dir).resolve()),
        "output_dir": str(Path(cfg.output_dir).resolve()),
    }
