import os
from pathlib import Path

from comfy_agent.config import ComfyConfig
from comfy_agent.examples_helpers import compose_upload_crop_download


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

    result = compose_upload_crop_download(
        cfg=cfg,
        run_id=os.getenv("EXAMPLE_RUN_ID", "redhead_demo"),
        image_path=image_path,
        x=220,
        y=140,
        width=512,
        height=640,
        stage="final",
    )

    print("run_id:", result["run_id"])
    print("uploaded remote:", result["uploaded"]["input_image_remote"])
    print("prompt_id:", result["cropped"]["prompt_id"])
    print("downloaded:")
    for artifact in result["downloaded"]["artifacts"]:
        print(" -", artifact["downloaded_path"])


if __name__ == "__main__":
    main()
