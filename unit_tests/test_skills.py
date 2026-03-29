import unittest
import tempfile
from unittest.mock import patch

from unit_tests.test_helpers import mocked_comfy_api


class SkillTests(unittest.TestCase):
    def test_generate_sd15_image_build_returns_workflow(self):
        from skills.workflows.txt2img.generate_sd15_image.skill import build

        with mocked_comfy_api():
            wf = build(prompt="cinematic robot")

        self.assertTrue(hasattr(wf, "run"))
        self.assertGreater(len(wf.nodes), 0)

    def test_generate_sd15_image_run_executes(self):
        from skills.workflows.txt2img.generate_sd15_image.skill import run

        with mocked_comfy_api() as posted:
            result = run(prompt="cinematic robot")

        self.assertEqual(result["status"], "done")
        self.assertIn("run_id", result)
        self.assertIn("artifacts", result)
        self.assertEqual(len(posted), 1)

    def test_preview_skill_build_is_editable(self):
        from skills.workflows.txt2img.preview_sd15_image.skill import build

        with mocked_comfy_api():
            wf = build(prompt="robot preview")
            wf.override({"ksampler.steps": 12})
            payload = wf.to_json()

        self.assertIn('"steps": 12', payload)

    def test_img2img_skill_build_contains_load_image(self):
        from skills.workflows.img2img_inpaint_outpaint.generate_sd15_img2img_remix.skill import build

        with mocked_comfy_api():
            wf = build(image="remix_source.png", prompt="robot remix")
            summary = wf.inspect(print_output=False)

        self.assertIn("LoadImage [load_image]", summary)
        self.assertIn("VAEEncode [vaeencode]", summary)

    def test_agent_ad_skill_run_executes(self):
        from skills.workflows.txt2img.generate_sd15_stelios_shoe_ad.skill import run

        with mocked_comfy_api() as posted:
            result = run(prompt="shoe ad")

        self.assertEqual(result["output"], "stelios_shoe_ad")
        self.assertEqual(len(posted), 1)

    def test_lora_skill_build_contains_lora_loader(self):
        from skills.workflows.txt2img.generate_sd15_lora.skill import build

        with mocked_comfy_api():
            wf = build(prompt="robot", lora="sd15/CakeStyle.safetensors", strength=0.8)
            summary = wf.inspect(print_output=False)

        self.assertIn("LoraLoaderModelOnly [lora_loader_model_only]", summary)

    def test_animated_webp_skill_build_contains_export_node(self):
        from skills.workflows.video_t2v_i2v_avatar.generate_sd15_animated_webp.skill import build

        with mocked_comfy_api():
            wf = build(prompt="robot animation", batch_size=4, fps=8)
            payload = wf.to_json()

        self.assertIn('"SaveAnimatedWEBP"', payload)

    def test_crop_skill_build_contains_crop_node(self):
        from skills.workflows.img2img_inpaint_outpaint.crop_image.skill import build

        with mocked_comfy_api():
            wf = build(image="rosie.jpg", x=10, y=20, width=128, height=128)
            summary = wf.inspect(print_output=False)

        self.assertIn("ImageCrop [image_crop]", summary)

    def test_crop_skill_run_returns_artifacts(self):
        from skills.workflows.img2img_inpaint_outpaint.crop_image.skill import run

        with mocked_comfy_api():
            result = run(image="rosie.jpg")

        self.assertEqual(result["status"], "ok")
        self.assertIn("run_id", result)
        self.assertIn("artifacts", result)

    def test_flux_multi_input_build_supports_two_images(self):
        from skills.workflows.img2img_inpaint_outpaint.generate_flux_multi_input_img2img.skill import build

        with mocked_comfy_api():
            wf, run_id, prefix, artifacts, engine = build(
                prompt="test prompt",
                images=["a.png", "b.png"],
            )
            summary = wf.inspect(print_output=False)

        self.assertIn("ReferenceLatent", summary)
        self.assertEqual(len(artifacts), 2)
        self.assertTrue(run_id)
        self.assertTrue(prefix)
        self.assertIn(engine, {"flux", "checkpoint"})

    def test_flux_multi_input_run_returns_output_metadata(self):
        from skills.workflows.img2img_inpaint_outpaint.generate_flux_multi_input_img2img.skill import run

        with mocked_comfy_api():
            result = run(
                prompt="test prompt",
                images=["a.png", "b.png", "c.png"],
            )

        self.assertEqual(result["status"], "done")
        self.assertEqual(result["image_count"], 3)
        self.assertIn("output_images", result)
        self.assertIn("artifacts", result)
        self.assertGreaterEqual(len(result["artifacts"]), 3)

    def test_flux_multi_input_build_rejects_upload_stage(self):
        from skills.workflows.img2img_inpaint_outpaint.generate_flux_multi_input_img2img.skill import build

        with self.assertRaises(ValueError):
            build(prompt="x", images=["a.png", "b.png"], upload_inputs=True)

    def test_flux_multi_input_run_rejects_download_stage(self):
        from skills.workflows.img2img_inpaint_outpaint.generate_flux_multi_input_img2img.skill import run

        with self.assertRaises(ValueError):
            run(prompt="x", images=["a.png", "b.png"], download_output=True)

    def test_list_comfy_assets_returns_structure(self):
        from skills.infra.list_comfy_assets.skill import run

        with tempfile.TemporaryDirectory() as tmp_in, tempfile.TemporaryDirectory() as tmp_out:
            with open(f"{tmp_in}/a.png", "wb") as f:
                f.write(b"x")
            with open(f"{tmp_out}/b.png", "wb") as f:
                f.write(b"y")
            with patch.dict(
                "os.environ",
                {
                    "COMFY_INPUT_DIR": tmp_in,
                    "COMFY_OUTPUT_DIR": tmp_out,
                },
                clear=False,
            ), mocked_comfy_api():
                result = run(include_files=True)

        self.assertEqual(result["status"], "ok")
        self.assertIn("assets", result)
        self.assertIn("counts", result)
        self.assertIn("input_files", result["assets"])
        self.assertIn("output_files", result["assets"])

    def test_upload_video_returns_remote_name(self):
        from skills.infra.upload_video.skill import run

        with tempfile.TemporaryDirectory() as tmp_dir:
            video_path = f"{tmp_dir}/clip.mp4"
            with open(video_path, "wb") as f:
                f.write(b"video")
            with mocked_comfy_api():
                result = run(video_path=video_path, run_id="vidrun")

        self.assertEqual(result["status"], "ok")
        self.assertEqual(result["run_id"], "vidrun")
        self.assertIn("input_video_remote", result)

    def test_download_video_with_video_meta_downloads_mp4(self):
        from skills.infra.download_video.skill import run

        with tempfile.TemporaryDirectory() as tmp_dir, mocked_comfy_api():
            result = run(
                video_meta={"filename": "clip.mp4", "subfolder": "", "type": "output"},
                run_id="vidrun",
                output_dir=tmp_dir,
            )

        self.assertEqual(result["status"], "ok")
        self.assertEqual(len(result["artifacts"]), 1)
        self.assertTrue(result["artifacts"][0]["downloaded_path"].endswith(".mp4"))

    def test_validate_server_models_returns_validation_shape(self):
        from skills.infra.validate_server_models.skill import run

        with mocked_comfy_api():
            result = run(model_names=["modelA.safetensors"])

        self.assertEqual(result["status"], "ok")
        self.assertIn("models", result)
        self.assertIn("all_model_names", result)
        self.assertIn("exists", result)
        self.assertIn("missing", result)


if __name__ == "__main__":
    unittest.main()
