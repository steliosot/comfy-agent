import tempfile
import unittest
from pathlib import Path

from comfy_agent import Workflow, run_agentic
from unit_tests.test_helpers import mocked_comfy_api


class TransportAndComposableSkillsTests(unittest.TestCase):
    def test_workflow_upload_image_posts_file(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            image_path = Path(tmp_dir) / "input.png"
            image_path.write_bytes(b"png-bytes")

            with mocked_comfy_api() as posted:
                wf = Workflow()
                result = wf.upload_image(
                    local_path=str(image_path),
                    remote_name="rid_input.png",
                )

            self.assertEqual(result["remote_name"], "rid_input.png")
            self.assertEqual(posted[0]["url"].endswith("/upload/image"), True)
            self.assertIsNotNone(posted[0]["files"])

    def test_workflow_download_image_writes_local_file(self):
        with tempfile.TemporaryDirectory() as tmp_dir, mocked_comfy_api():
            wf = Workflow()
            downloaded = wf.download_image(
                image_meta={"filename": "ComfyUI_00001_.png", "subfolder": "", "type": "output"},
                output_dir=tmp_dir,
            )

            path = Path(downloaded["downloaded_path"])
            self.assertTrue(path.exists())
            self.assertEqual(path.read_bytes(), b"fake-bytes:ComfyUI_00001_.png")

    def test_workflow_download_saved_images_uses_deterministic_names(self):
        with tempfile.TemporaryDirectory() as tmp_dir, mocked_comfy_api():
            wf = Workflow()
            records = wf.download_saved_images(
                prompt_id="test-prompt",
                output_dir=tmp_dir,
                filename_strategy=lambda meta, index: f"rid_download_{index}.png",
            )

            self.assertEqual(len(records), 1)
            self.assertTrue(Path(records[0]["downloaded_path"]).name.startswith("rid_download_"))

    def test_workflow_transfer_output_to_input_returns_remote_name(self):
        with mocked_comfy_api() as posted:
            wf = Workflow()
            transferred = wf.transfer_output_to_input(
                image_meta={"filename": "ComfyUI_00001_.png", "subfolder": "", "type": "output"},
                remote_name="copied_input.png",
            )

        self.assertEqual(transferred["remote_name"], "copied_input.png")
        self.assertEqual(posted[-1]["url"].endswith("/upload/image"), True)

    def test_upload_and_download_skills_chain_with_shared_run_id(self):
        from skills.crop_image.skill import run as crop_run
        from skills.download_image.skill import run as download_run
        from skills.upload_image.skill import run as upload_run

        with tempfile.TemporaryDirectory() as tmp_dir:
            image_path = Path(tmp_dir) / "source.png"
            image_path.write_bytes(b"source")

            with mocked_comfy_api():
                upload_result = upload_run(
                    image_path=str(image_path),
                    run_id="chain123",
                )

                crop_result = crop_run(
                    image=upload_result["input_image_remote"],
                    run_id=upload_result["run_id"],
                )

                download_result = download_run(
                    prompt_id=crop_result["prompt_id"],
                    run_id=crop_result["run_id"],
                    output_dir=tmp_dir,
                )

            self.assertEqual(upload_result["run_id"], "chain123")
            self.assertEqual(crop_result["run_id"], "chain123")
            self.assertEqual(download_result["run_id"], "chain123")
            self.assertTrue(download_result["artifacts"][0]["downloaded_path"].endswith(".png"))

    def test_download_skill_requires_image_meta_or_prompt_id(self):
        from skills.download_image.skill import run as download_run

        with self.assertRaises(ValueError):
            download_run()

    def test_agentic_run_preserves_run_id_in_context(self):
        context = {}
        with mocked_comfy_api():
            result = run_agentic(
                prompt="generate a robot and crop it to 256x256",
                run_id="agentic123",
                context=context,
                print_reasoning=False,
            )

        self.assertEqual(result["run_id"], "agentic123")
        self.assertEqual(result["context"]["run_id"], "agentic123")
        self.assertIn("artifacts", result)
        self.assertIn("preflight", result)
        self.assertTrue(result["preflight"]["ready_for_run"])


if __name__ == "__main__":
    unittest.main()
