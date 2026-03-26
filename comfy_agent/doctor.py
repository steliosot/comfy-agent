import argparse
import json
import time
from pathlib import Path

from .config import ComfyConfig, load_comfy_env
from .workflow import Workflow


_PROBE_PNG_BYTES = (
    b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01"
    b"\x08\x04\x00\x00\x00\xb5\x1c\x0c\x02\x00\x00\x00\x0bIDATx\xdac\xfc\xff"
    b"\x1f\x00\x03\x03\x02\x00\xee\xd9\xef$\x00\x00\x00\x00IEND\xaeB`\x82"
)


def run_checks(
    env_path=".env",
    server=None,
    auth_header=None,
    skip_upload_download=False,
    verbose=True,
):
    load_comfy_env(env_path=env_path, override=False)
    cfg = ComfyConfig.from_env(load_env=False)
    resolved_server = server or cfg.server
    resolved_headers = dict(cfg.headers)
    if auth_header is not None:
        if auth_header:
            resolved_headers["Authorization"] = auth_header
        else:
            resolved_headers.pop("Authorization", None)

    env_exists = Path(env_path).exists()
    input_dir = Path(cfg.input_dir)
    output_dir = Path(cfg.output_dir)
    input_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)

    result = {
        "ok": False,
        "env_file": str(Path(env_path).resolve()),
        "env_exists": env_exists,
        "server": resolved_server,
        "auth_header_set": "Authorization" in resolved_headers,
        "input_dir": str(input_dir.resolve()),
        "output_dir": str(output_dir.resolve()),
        "object_info_nodes": 0,
        "connectivity_ok": False,
        "upload_download_ok": None if skip_upload_download else False,
        "probe_download_path": None,
        "errors": [],
    }

    try:
        wf = Workflow(
            server=resolved_server,
            headers=resolved_headers or None,
            api_prefix=cfg.api_prefix,
        )
        result["connectivity_ok"] = True
        result["object_info_nodes"] = len(wf.registry)
    except Exception as exc:  # pragma: no cover
        result["errors"].append(f"connectivity: {exc}")
        if verbose:
            print("[FAIL] Connectivity check failed")
            print(f"  reason: {exc}")
        return result

    if not skip_upload_download:
        try:
            probe_local = input_dir / f"doctor_probe_{int(time.time())}.png"
            probe_local.write_bytes(_PROBE_PNG_BYTES)
            uploaded = wf.upload_image(
                local_path=str(probe_local),
                remote_name=probe_local.name,
                overwrite=True,
                type="input",
            )

            downloaded = wf.download_image(
                image_meta={
                    "filename": uploaded["remote_name"],
                    "subfolder": uploaded.get("subfolder", ""),
                    "type": uploaded.get("type", "input"),
                },
                output_path=str(output_dir / f"{probe_local.stem}_download.png"),
            )
            download_path = Path(downloaded["downloaded_path"])
            if download_path.exists() and download_path.stat().st_size > 0:
                result["upload_download_ok"] = True
                result["probe_download_path"] = str(download_path.resolve())
            else:
                result["errors"].append("upload_download: download file missing or empty")
        except Exception as exc:  # pragma: no cover
            result["errors"].append(f"upload_download: {exc}")

    result["ok"] = result["connectivity_ok"] and (
        True if skip_upload_download else bool(result["upload_download_ok"])
    )

    if verbose:
        print("[PASS] Connectivity" if result["connectivity_ok"] else "[FAIL] Connectivity")
        print(f"  server: {result['server']}")
        print(f"  object_info nodes: {result['object_info_nodes']}")
        print("[PASS] .env file" if result["env_exists"] else "[WARN] .env file missing")
        if not skip_upload_download:
            if result["upload_download_ok"]:
                print("[PASS] Upload/Download probe")
                print(f"  downloaded: {result['probe_download_path']}")
            else:
                print("[FAIL] Upload/Download probe")
        if result["errors"]:
            print("Errors:")
            for err in result["errors"]:
                print(f"  - {err}")

    return result


def main():
    parser = argparse.ArgumentParser(
        description="Validate Comfy Agent config and ComfyUI connectivity."
    )
    parser.add_argument("--env-file", default=".env")
    parser.add_argument("--server", default=None)
    parser.add_argument("--auth-header", default=None)
    parser.add_argument("--skip-upload-download", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    result = run_checks(
        env_path=args.env_file,
        server=args.server,
        auth_header=args.auth_header,
        skip_upload_download=args.skip_upload_download,
        verbose=not args.json,
    )
    if args.json:
        print(json.dumps(result, indent=2))
    raise SystemExit(0 if result.get("ok") else 1)


if __name__ == "__main__":
    main()
