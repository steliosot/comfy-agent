from pathlib import Path

from comfy_agent.config import ComfyConfig
from skills.download_image.skill import run as download_run
from skills.generate_flux_multi_input_img2img.skill import run as generate_run
from skills.upload_image.skill import run as upload_run


class SkillFlow:
    def __init__(self, cfg, run_id):
        self.cfg = cfg
        self.run_id = run_id
        self.headers = cfg.headers or None
        self.remote_images = []
        self.generated = None
        self.downloaded = None

    def upload(self, path):
        image_path = Path(path)
        if not image_path.exists():
            raise FileNotFoundError(f"Missing input file: {image_path}")
        idx = len(self.remote_images) + 1
        result = upload_run(
            image_path=str(image_path),
            run_id=self.run_id,
            remote_name=f"{self.run_id}_ref{idx}{image_path.suffix}",
            server=self.cfg.server,
            headers=self.headers,
            api_prefix=self.cfg.api_prefix,
        )
        self.remote_images.append(result["input_image_remote"])
        return self

    def generate(self, prompt):
        self.generated = generate_run(
            prompt=prompt,
            images=self.remote_images,
            upload_inputs=False,
            download_output=False,
            run_id=self.run_id,
            server=self.cfg.server,
            headers=self.headers,
            api_prefix=self.cfg.api_prefix,
            history_retries=120,
            history_delay=1.0,
            engine="auto",
        )
        return self

    def download(self):
        self.downloaded = download_run(
            prompt_id=self.generated["prompt_id"],
            run_id=self.run_id,
            stage="final",
            output_dir=self.cfg.output_dir,
            history_retries=180,
            history_delay=1.0,
            server=self.cfg.server,
            headers=self.headers,
            api_prefix=self.cfg.api_prefix,
        )
        return self


cfg = ComfyConfig.from_env(load_env=True)

flow = (
    SkillFlow(cfg, run_id="fluent_skills_three_refs")
    .upload(Path(cfg.input_dir) / "woman.png")
    .upload(Path(cfg.input_dir) / "St-Pauls-Cathedral.png")
    .upload(Path(cfg.input_dir) / "hat.jpeg")
    .generate(
        "Keep the same woman identity, compose naturally with St Paul's Cathedral, "
        "and apply the hat reference influence with realistic lighting and perspective."
    )
    .download()
)

print("run_id:", flow.run_id)
print("prompt_id:", flow.generated["prompt_id"])
print("downloaded:")
for artifact in flow.downloaded["artifacts"]:
    if artifact.get("downloaded_path"):
        print(" -", artifact["downloaded_path"])
