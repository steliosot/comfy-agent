import os
from pathlib import Path

from comfy_agent.config import ComfyConfig
from skills.crop_image.skill import run as crop_run
from skills.download_image.skill import run as download_run
from skills.upload_image.skill import run as upload_run


def main():
    cfg = ComfyConfig.from_env(load_env=True)
    root = Path(__file__).resolve().parent
    default_input = Path(cfg.input_dir) / "redhead_portrait.png"
    if not default_input.exists():
        default_input = root / "assets" / "redhead_portrait.png"
    image_path = Path(os.getenv("EXAMPLE_INPUT_IMAGE", str(default_input))).resolve()

    if not image_path.exists():
        raise FileNotFoundError(
            f"Input image not found at {image_path}. "
            "Set EXAMPLE_INPUT_IMAGE to your local portrait image path."
        )

    run_id = os.getenv("EXAMPLE_RUN_ID", "redhead_demo")

    upload_result = upload_run(
        image_path=str(image_path),
        run_id=run_id,
        server=os.getenv("COMFY_URL"),
        headers={"Authorization": os.getenv("COMFY_AUTH_HEADER")} if os.getenv("COMFY_AUTH_HEADER") else None,
    )

    crop_result = crop_run(
        image=upload_result["input_image_remote"],
        x=220,
        y=140,
        width=512,
        height=640,
        run_id=upload_result["run_id"],
        server=os.getenv("COMFY_URL"),
        headers={"Authorization": os.getenv("COMFY_AUTH_HEADER")} if os.getenv("COMFY_AUTH_HEADER") else None,
    )

    download_result = download_run(
        prompt_id=crop_result["prompt_id"],
        run_id=crop_result["run_id"],
        stage="final",
        output_dir=os.getenv("EXAMPLE_OUTPUT_DIR", cfg.output_dir),
        server=os.getenv("COMFY_URL"),
        headers={"Authorization": os.getenv("COMFY_AUTH_HEADER")} if os.getenv("COMFY_AUTH_HEADER") else None,
    )

    print("run_id:", download_result["run_id"])
    print("uploaded remote:", upload_result["input_image_remote"])
    print("prompt_id:", crop_result["prompt_id"])
    print("downloaded:")
    for artifact in download_result["artifacts"]:
        print(" -", artifact["downloaded_path"])


if __name__ == "__main__":
    main()
