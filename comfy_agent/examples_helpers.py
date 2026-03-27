from pathlib import Path

from skills.crop_image.skill import run as crop_run
from skills.download_image.skill import run as download_run
from skills.generate_flux_multi_input_img2img.skill import run as generate_flux_multi_input_run
from skills.upload_image.skill import run as upload_run


def _remote_name(run_id, index, image_path):
    suffix = Path(image_path).suffix or ".png"
    return f"{run_id}_ref{index}{suffix}"


def compose_flux_multi_input(
    *,
    cfg,
    run_id,
    image_paths,
    prompt,
    stage="final",
    engine="auto",
    history_retries_generate=120,
    history_delay_generate=1.0,
    history_retries_download=180,
    history_delay_download=1.0,
):
    headers = cfg.headers or None

    uploaded_names = []
    for index, image_path in enumerate(image_paths, start=1):
        image_path = Path(image_path)
        if not image_path.exists():
            raise FileNotFoundError(f"Missing input file: {image_path}")
        uploaded = upload_run(
            image_path=str(image_path),
            run_id=run_id,
            remote_name=_remote_name(run_id, index, image_path),
            server=cfg.server,
            headers=headers,
            api_prefix=cfg.api_prefix,
        )
        uploaded_names.append(uploaded["input_image_remote"])

    generated = generate_flux_multi_input_run(
        prompt=prompt,
        images=uploaded_names,
        run_id=run_id,
        server=cfg.server,
        headers=headers,
        api_prefix=cfg.api_prefix,
        history_retries=history_retries_generate,
        history_delay=history_delay_generate,
        engine=engine,
    )

    downloaded = download_run(
        prompt_id=generated["prompt_id"],
        run_id=run_id,
        stage=stage,
        output_dir=cfg.output_dir,
        history_retries=history_retries_download,
        history_delay=history_delay_download,
        server=cfg.server,
        headers=headers,
        api_prefix=cfg.api_prefix,
    )

    return {
        "run_id": run_id,
        "uploaded": uploaded_names,
        "generated": generated,
        "downloaded": downloaded,
    }


def compose_upload_crop_download(
    *,
    cfg,
    run_id,
    image_path,
    x=220,
    y=140,
    width=512,
    height=640,
    stage="final",
):
    headers = cfg.headers or None
    image_path = Path(image_path)
    if not image_path.exists():
        raise FileNotFoundError(f"Missing input file: {image_path}")

    uploaded = upload_run(
        image_path=str(image_path),
        run_id=run_id,
        remote_name=f"{run_id}_input{image_path.suffix or '.png'}",
        server=cfg.server,
        headers=headers,
        api_prefix=cfg.api_prefix,
    )

    cropped = crop_run(
        image=uploaded["input_image_remote"],
        x=x,
        y=y,
        width=width,
        height=height,
        run_id=run_id,
        server=cfg.server,
        headers=headers,
        api_prefix=cfg.api_prefix,
    )

    downloaded = download_run(
        prompt_id=cropped["prompt_id"],
        run_id=run_id,
        stage=stage,
        output_dir=cfg.output_dir,
        server=cfg.server,
        headers=headers,
        api_prefix=cfg.api_prefix,
    )

    return {
        "run_id": run_id,
        "uploaded": uploaded,
        "cropped": cropped,
        "downloaded": downloaded,
    }


class FluentSkillComposeFlow:
    def __init__(self, cfg, run_id):
        self.cfg = cfg
        self.run_id = run_id
        self.image_paths = []
        self.prompt_text = None
        self.stage_name = "final"
        self.result = None

    def ref(self, image_path):
        self.image_paths.append(image_path)
        return self

    def prompt(self, text):
        self.prompt_text = text
        return self

    def stage(self, stage_name):
        self.stage_name = stage_name
        return self

    def run(self):
        if not self.prompt_text:
            raise ValueError("prompt(...) is required before run()")
        self.result = compose_flux_multi_input(
            cfg=self.cfg,
            run_id=self.run_id,
            image_paths=self.image_paths,
            prompt=self.prompt_text,
            stage=self.stage_name,
        )
        return self
