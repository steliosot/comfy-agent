from comfy_agent.config import ComfyConfig
from comfy_agent.examples_helpers import FluentSkillComposeFlow

cfg = ComfyConfig.from_env(load_env=True)

flow = (
    FluentSkillComposeFlow(cfg, run_id="shared_compose_three_refs")
    .ref(f"{cfg.input_dir}/woman.png")
    .ref(f"{cfg.input_dir}/St-Pauls-Cathedral.png")
    .ref(f"{cfg.input_dir}/hat.jpeg")
    .prompt(
        "Keep the same woman identity, compose naturally with St Paul's Cathedral, "
        "and apply hat reference influence with realistic lighting and perspective."
    )
    .stage("final")
    .run()
)

result = flow.result
print("run_id:", flow.run_id)
print("prompt_id:", result["generated"]["prompt_id"])
print("downloaded:")
for artifact in result["downloaded"]["artifacts"]:
    if artifact.get("downloaded_path"):
        print(" -", artifact["downloaded_path"])
