import os
from dataclasses import dataclass
from pathlib import Path


def _strip_quotes(value):
    text = str(value).strip()
    if len(text) >= 2 and text[0] == text[-1] and text[0] in {"'", '"'}:
        return text[1:-1]
    return text


def load_env_file(path=".env", override=False):
    env_path = Path(path)
    if not env_path.exists() or not env_path.is_file():
        return False

    for raw_line in env_path.read_text().splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        if not key:
            continue
        if key in os.environ and not override:
            continue
        os.environ[key] = _strip_quotes(value)
    return True


def load_comfy_env(env_path=None, override=False):
    try:
        from dotenv import load_dotenv  # type: ignore
    except Exception:
        path = env_path or ".env"
        return load_env_file(path=path, override=override)

    return bool(load_dotenv(dotenv_path=env_path or ".env", override=override))


@dataclass
class ComfyConfig:
    server: str
    headers: dict
    api_prefix: str | None
    manager_api_prefix: str
    hf_token: str | None
    civitai_api_key: str | None
    resource_min_free_vram_mb: float | None
    resource_min_free_storage_gb: float | None
    input_dir: str
    output_dir: str

    @classmethod
    def from_env(cls, load_env=True, env_path=None):
        if load_env:
            load_comfy_env(env_path=env_path)

        server = os.getenv("COMFY_URL", "http://127.0.0.1:8000")
        auth_header = os.getenv("COMFY_AUTH_HEADER")
        api_prefix = os.getenv("COMFY_API_PREFIX") or None
        manager_api_prefix = os.getenv("COMFY_MANAGER_API_PREFIX", "/manager")
        hf_token = os.getenv("HF_TOKEN") or None
        civitai_api_key = os.getenv("CIVITAI_API_KEY") or None
        raw_vram = os.getenv("COMFY_RESOURCE_MIN_FREE_VRAM_MB")
        raw_storage = os.getenv("COMFY_RESOURCE_MIN_FREE_STORAGE_GB")
        input_dir = os.getenv("COMFY_INPUT_DIR", "tmp/inputs")
        output_dir = os.getenv("COMFY_OUTPUT_DIR", "tmp/outputs")

        headers = {}
        if auth_header:
            headers["Authorization"] = auth_header

        min_vram = None
        min_storage = None
        try:
            min_vram = float(raw_vram) if raw_vram not in {None, ""} else None
        except ValueError:
            min_vram = None
        try:
            min_storage = float(raw_storage) if raw_storage not in {None, ""} else None
        except ValueError:
            min_storage = None

        return cls(
            server=server,
            headers=headers,
            api_prefix=api_prefix,
            manager_api_prefix=manager_api_prefix,
            hf_token=hf_token,
            civitai_api_key=civitai_api_key,
            resource_min_free_vram_mb=min_vram,
            resource_min_free_storage_gb=min_storage,
            input_dir=input_dir,
            output_dir=output_dir,
        )
