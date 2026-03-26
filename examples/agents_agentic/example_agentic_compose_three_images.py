from pathlib import Path

from comfy_agent.config import ComfyConfig
from skills.download_image.skill import run as download_run
from skills.generate_flux_multi_input_img2img.skill import run as generate_run
from skills.upload_image.skill import run as upload_run


def main():
    cfg = ComfyConfig.from_env(load_env=True)
    headers = cfg.headers or None
    run_id = "compose_three_refs"

    image_paths = [
        Path(cfg.input_dir) / "woman.png",
        Path(cfg.input_dir) / "St-Pauls-Cathedral.png",
        Path(cfg.input_dir) / "hat.jpeg",
    ]
    for path in image_paths:
        if not path.exists():
            raise FileNotFoundError(f"Missing input: {path}")

    uploaded_names = []
    for index, image_path in enumerate(image_paths, start=1):
        uploaded = upload_run(
            image_path=str(image_path),
            run_id=run_id,
            remote_name=f"{run_id}_ref{index}{image_path.suffix}",
            server=cfg.server,
            headers=headers,
            api_prefix=cfg.api_prefix,
        )
        uploaded_names.append(uploaded["input_image_remote"])

    generated = generate_run(
        prompt=(
            "Keep the same woman identity and compose a realistic London scene near "
            "St Paul's Cathedral. Use the hat reference as styling influence, "
            "natural perspective and lighting."
        ),
        images=uploaded_names,
        upload_inputs=False,
        download_output=False,
        run_id=run_id,
        server=cfg.server,
        headers=headers,
        api_prefix=cfg.api_prefix,
        history_retries=120,
        history_delay=1.0,
        engine="auto",
    )

    downloaded = download_run(
        prompt_id=generated["prompt_id"],
        run_id=run_id,
        stage="final",
        output_dir=cfg.output_dir,
        history_retries=180,
        history_delay=1.0,
        server=cfg.server,
        headers=headers,
        api_prefix=cfg.api_prefix,
    )

    print("run_id:", run_id)
    print("prompt_id:", generated["prompt_id"])
    print("downloaded:")
    for artifact in downloaded["artifacts"]:
        if artifact.get("downloaded_path"):
            print(" -", artifact["downloaded_path"])


if __name__ == "__main__":
    main()
