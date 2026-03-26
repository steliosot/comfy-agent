import re
import uuid
from pathlib import Path


def ensure_run_id(run_id=None):
    if run_id:
        return re.sub(r"[^a-zA-Z0-9_-]+", "_", str(run_id)).strip("_") or "run"
    return uuid.uuid4().hex[:10]


def make_remote_input_name(run_id, local_path):
    suffix = Path(local_path).suffix or ".png"
    return f"{run_id}_input{suffix}"


def make_stage_prefix(run_id, stage):
    return f"{run_id}_{stage}"


def make_download_filename(run_id, stage, index, source_filename=""):
    suffix = Path(source_filename).suffix or ".png"
    return f"{run_id}_{stage}_{index}{suffix}"


def build_artifact(
    *,
    role,
    local_path=None,
    remote_name=None,
    source=None,
    node_id=None,
    subfolder="",
    type="output",
    downloaded_path=None,
):
    return {
        "role": role,
        "local_path": local_path,
        "remote_name": remote_name,
        "source": source,
        "node_id": node_id,
        "subfolder": subfolder,
        "type": type,
        "downloaded_path": downloaded_path,
    }
