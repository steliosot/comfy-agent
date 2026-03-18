import unittest

from unit_tests.test_helpers import mocked_comfy_api


class SkillTests(unittest.TestCase):
    def test_generate_sd15_image_build_returns_workflow(self):
        from skills.generate_sd15_image.skill import build

        with mocked_comfy_api():
            wf = build(prompt="cinematic robot")

        self.assertTrue(hasattr(wf, "run"))
        self.assertGreater(len(wf.nodes), 0)

    def test_generate_sd15_image_run_executes(self):
        from skills.generate_sd15_image.skill import run

        with mocked_comfy_api() as posted:
            result = run(prompt="cinematic robot")

        self.assertEqual(result["status"], "done")
        self.assertEqual(len(posted), 1)

    def test_preview_skill_build_is_editable(self):
        from skills.preview_sd15_image.skill import build

        with mocked_comfy_api():
            wf = build(prompt="robot preview")
            wf.override({"ksampler.steps": 12})
            payload = wf.to_json()

        self.assertIn('"steps": 12', payload)

    def test_img2img_skill_build_contains_load_image(self):
        from skills.generate_sd15_img2img_remix.skill import build

        with mocked_comfy_api():
            wf = build(image="remix_source.png", prompt="robot remix")
            summary = wf.inspect(print_output=False)

        self.assertIn("LoadImage [load_image]", summary)
        self.assertIn("VAEEncode [vaeencode]", summary)

    def test_agent_ad_skill_run_executes(self):
        from skills.generate_sd15_stelios_shoe_ad.skill import run

        with mocked_comfy_api() as posted:
            result = run(prompt="shoe ad")

        self.assertEqual(result["output"], "stelios_shoe_ad")
        self.assertEqual(len(posted), 1)

    def test_lora_skill_build_contains_lora_loader(self):
        from skills.generate_sd15_lora.skill import build

        with mocked_comfy_api():
            wf = build(prompt="robot", lora="sd15/CakeStyle.safetensors", strength=0.8)
            summary = wf.inspect(print_output=False)

        self.assertIn("LoraLoaderModelOnly [lora_loader_model_only]", summary)

    def test_animated_webp_skill_build_contains_export_node(self):
        from skills.generate_sd15_animated_webp.skill import build

        with mocked_comfy_api():
            wf = build(prompt="robot animation", batch_size=4, fps=8)
            payload = wf.to_json()

        self.assertIn('"SaveAnimatedWEBP"', payload)

    def test_crop_skill_build_contains_crop_node(self):
        from skills.crop_image.skill import build

        with mocked_comfy_api():
            wf = build(image="rosie.jpg", x=10, y=20, width=128, height=128)
            summary = wf.inspect(print_output=False)

        self.assertIn("ImageCrop [image_crop]", summary)


if __name__ == "__main__":
    unittest.main()
