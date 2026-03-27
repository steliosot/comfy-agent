from comfy_agent.config import ComfyConfig
from comfy_agent.examples_helpers import compose_flux_multi_input


def main():
    cfg = ComfyConfig.from_env(load_env=True)
    result = compose_flux_multi_input(
        cfg=cfg,
        run_id="shared_compose_three_refs",
        image_paths=[
            f"{cfg.input_dir}/woman.png",
            f"{cfg.input_dir}/St-Pauls-Cathedral.png",
            f"{cfg.input_dir}/hat.jpeg",
        ],
        prompt=(
            "Keep the same woman identity and compose a realistic London scene near "
            "St Paul's Cathedral. Use the hat reference as styling influence, "
            "natural perspective and lighting."
        ),
        stage="final",
    )
    print("run_id:", result["run_id"])
    print("prompt_id:", result["generated"]["prompt_id"])
    print("downloaded:")
    for artifact in result["downloaded"]["artifacts"]:
        if artifact.get("downloaded_path"):
            print(" -", artifact["downloaded_path"])


if __name__ == "__main__":
    main()
