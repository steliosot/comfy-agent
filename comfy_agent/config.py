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


def _normalize_base_url(base_url):
    text = str(base_url or "").strip()
    if not text:
        return "http://127.0.0.1:8000"
    if "://" in text:
        return text.rstrip("/")
    return f"http://{text}".rstrip("/")


def _normalize_prefix(prefix, default=None):
    value = str(prefix if prefix is not None else (default or "")).strip()
    if not value:
        return ""
    if not value.startswith("/"):
        value = f"/{value}"
    return value.rstrip("/")


def _resolve_servers_file(servers_file=None):
    if servers_file:
        candidate = Path(str(servers_file)).expanduser()
        if not candidate.is_absolute():
            candidate = Path.cwd() / candidate
        return candidate

    env_path = os.getenv("COMFY_SERVERS_FILE")
    if env_path:
        candidate = Path(env_path).expanduser()
        if not candidate.is_absolute():
            candidate = Path.cwd() / candidate
        return candidate

    default_name = ".comfy_servers.yaml"
    cwd_candidate = Path.cwd() / default_name
    if cwd_candidate.exists():
        return cwd_candidate

    repo_candidate = Path(__file__).resolve().parents[1] / default_name
    if repo_candidate.exists():
        return repo_candidate

    return None


def _expand_env(value):
    if isinstance(value, str):
        return os.path.expandvars(value)
    return value


def load_comfy_servers_registry(servers_file=None):
    path = _resolve_servers_file(servers_file=servers_file)
    if path is None or not path.exists():
        return {
            "path": str(path) if path is not None else None,
            "default_server": None,
            "servers": {},
        }

    try:
        import yaml  # type: ignore
    except Exception as exc:  # pragma: no cover
        raise RuntimeError(
            "PyYAML is required to parse COMFY_SERVERS_FILE/.comfy_servers.yaml."
        ) from exc

    raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(raw, dict):
        raise ValueError(f"Invalid servers file format in {path}: expected a mapping.")

    servers = raw.get("servers") or {}
    if not isinstance(servers, dict):
        raise ValueError(f"Invalid servers file format in {path}: 'servers' must be a mapping.")

    default_server = raw.get("default_server")
    if default_server is not None:
        default_server = str(default_server).strip() or None

    return {
        "path": str(path),
        "default_server": default_server,
        "servers": servers,
    }


def get_server_config(name=None, load_env=True, env_path=None, servers_file=None):
    """
    Resolve Comfy server settings from:
      1) explicit named server in YAML registry
      2) default named server in YAML registry
      3) classic single-server env vars
    """
    if load_env:
        load_comfy_env(env_path=env_path)

    fallback_server = _normalize_base_url(os.getenv("COMFY_URL", "http://127.0.0.1:8000"))
    fallback_api_prefix = os.getenv("COMFY_API_PREFIX") or None
    fallback_manager_prefix = _normalize_prefix(
        os.getenv("COMFY_MANAGER_API_PREFIX", "/manager"),
        default="/manager",
    )
    fallback_headers = {}
    fallback_auth = os.getenv("COMFY_AUTH_HEADER")
    if fallback_auth:
        fallback_headers["Authorization"] = fallback_auth

    registry = load_comfy_servers_registry(servers_file=servers_file)
    selected_name = str(name).strip() if name is not None else registry.get("default_server")
    selected_name = selected_name or None
    servers = registry.get("servers", {})

    if selected_name is None:
        return {
            "server_name": None,
            "server": fallback_server,
            "headers": fallback_headers,
            "api_prefix": _normalize_prefix(fallback_api_prefix) or None,
            "manager_api_prefix": fallback_manager_prefix or "/manager",
            "source": "env",
            "servers_file": registry.get("path"),
        }

    if selected_name not in servers:
        raise ValueError(
            f"Unknown server '{selected_name}' in servers registry."
        )

    entry = servers.get(selected_name)
    if not isinstance(entry, dict):
        raise ValueError(f"Server '{selected_name}' entry must be a mapping.")

    raw_url = _expand_env(entry.get("url"))
    if not raw_url or not str(raw_url).strip():
        raise ValueError(f"Server '{selected_name}' is missing required field 'url'.")

    raw_headers = entry.get("headers") or {}
    if not isinstance(raw_headers, dict):
        raise ValueError(f"Server '{selected_name}' field 'headers' must be a mapping.")

    headers = {}
    for key, value in raw_headers.items():
        headers[str(key)] = _expand_env(value)

    raw_api_prefix = _expand_env(entry.get("api_prefix"))
    raw_manager_prefix = _expand_env(entry.get("manager_api_prefix"))

    api_prefix = _normalize_prefix(raw_api_prefix, default="") or None
    manager_api_prefix = _normalize_prefix(
        raw_manager_prefix,
        default=fallback_manager_prefix or "/manager",
    ) or "/manager"

    return {
        "server_name": selected_name,
        "server": _normalize_base_url(raw_url),
        "headers": headers,
        "api_prefix": api_prefix,
        "manager_api_prefix": manager_api_prefix,
        "source": "servers_file",
        "servers_file": registry.get("path"),
    }


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
        resolved = get_server_config(name=None, load_env=load_env, env_path=env_path)
        server = resolved["server"]
        api_prefix = resolved["api_prefix"]
        manager_api_prefix = resolved["manager_api_prefix"]
        hf_token = os.getenv("HF_TOKEN") or None
        civitai_api_key = os.getenv("CIVITAI_API_KEY") or None
        raw_vram = os.getenv("COMFY_RESOURCE_MIN_FREE_VRAM_MB")
        raw_storage = os.getenv("COMFY_RESOURCE_MIN_FREE_STORAGE_GB")
        input_dir = os.getenv("COMFY_INPUT_DIR", "tmp/inputs")
        output_dir = os.getenv("COMFY_OUTPUT_DIR", "tmp/outputs")

        headers = dict(resolved["headers"])

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
