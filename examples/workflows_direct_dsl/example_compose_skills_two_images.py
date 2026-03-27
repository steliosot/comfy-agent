from comfy_agent.config import ComfyConfig
from comfy_agent.examples_helpers import compose_flux_multi_input

cfg = ComfyConfig.from_env(load_env=True)
result = compose_flux_multi_input(
    cfg=cfg,
    run_id="shared_compose_two_refs",
    image_paths=[
        f"{cfg.input_dir}/woman.png",
        f"{cfg.input_dir}/St-Pauls-Cathedral.png",
    ],
    prompt=(
        "Keep the same woman identity from the portrait reference and blend naturally "
        "in front of St Paul's Cathedral in London. Ultra realistic style."
    ),
    stage="final",
)
print("run_id:", result["run_id"])
print("prompt_id:", result["generated"]["prompt_id"])
print("downloaded:")
for artifact in result["downloaded"]["artifacts"]:
    if artifact.get("downloaded_path"):
        print(" -", artifact["downloaded_path"])
