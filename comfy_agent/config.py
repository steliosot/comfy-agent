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
    input_dir: str
    output_dir: str

    @classmethod
    def from_env(cls, load_env=True, env_path=None):
        if load_env:
            load_comfy_env(env_path=env_path)

        server = os.getenv("COMFY_URL", "http://127.0.0.1:8000")
        auth_header = os.getenv("COMFY_AUTH_HEADER")
        api_prefix = os.getenv("COMFY_API_PREFIX") or None
        input_dir = os.getenv("COMFY_INPUT_DIR", "tmp/inputs")
        output_dir = os.getenv("COMFY_OUTPUT_DIR", "tmp/outputs")

        headers = {}
        if auth_header:
            headers["Authorization"] = auth_header

        return cls(
            server=server,
            headers=headers,
            api_prefix=api_prefix,
            input_dir=input_dir,
            output_dir=output_dir,
        )
