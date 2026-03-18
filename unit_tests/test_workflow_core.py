import importlib.util
import json
import unittest

from comfy_agent import Workflow, load_yaml_skill

from unit_tests.test_helpers import mocked_comfy_api


class WorkflowCoreTests(unittest.TestCase):
    def test_basic_workflow_run_posts_prompt(self):
        with mocked_comfy_api() as posted:
            wf = Workflow()
            model, clip, vae = wf.checkpointloadersimple(
                ckpt_name="sd1.5/juggernaut_reborn.safetensors"
            )
            pos = wf.cliptextencode(clip=clip, text="rusty robot")
            neg = wf.cliptextencode(clip=clip, text="bad quality")
            latent = wf.emptylatentimage(width=512, height=512, batch_size=1)
            samples = wf.ksampler(
                model=model,
                positive=pos,
                negative=neg,
                latent_image=latent,
                steps=20,
            )
            img = wf.vaedecode(samples=samples, vae=vae)
            wf.saveimage(images=img, filename_prefix="robot")
            wf.run()

        self.assertEqual(len(posted), 1)
        dag = posted[0]["json"]["prompt"]
        self.assertEqual(dag["1"]["class_type"], "CheckpointLoaderSimple")
        self.assertEqual(dag["7"]["class_type"], "SaveImage")

    def test_fluent_api_clone_override_and_inspect(self):
        with mocked_comfy_api():
            wf = Workflow()
            (
                wf
                .checkpoint("sd1.5/juggernaut_reborn.safetensors")
                .prompt("robot")
                .negative("bad")
                .latent(512, 512)
                .sample()
                .decode()
                .save("robot")
            )
            clone = wf.clone().override(
                {
                    "ksampler.cfg": 12,
                    "ksampler.steps": 30,
                    "save.filename_prefix": "robot_override",
                }
            )

            summary = clone.inspect(print_output=False)
            payload = clone.to_json()

        self.assertIn("KSampler [ksampler]", summary)
        self.assertIn('"cfg": 12', payload)
        self.assertIn('"filename_prefix": "robot_override"', payload)

    def test_clone_is_independent_from_original(self):
        with mocked_comfy_api():
            wf = (
                Workflow()
                .checkpoint("sd1.5/juggernaut_reborn.safetensors")
                .prompt("robot")
                .negative("bad")
                .latent(512, 512)
                .sample(steps=20, cfg=7.0)
                .decode()
                .save("robot")
            )
            clone = wf.clone().override({"ksampler.cfg": 14})

        self.assertIn('"cfg": 7.0', wf.to_json())
        self.assertIn('"cfg": 14', clone.to_json())

    def test_override_supports_indexed_selector(self):
        with mocked_comfy_api():
            wf = Workflow()
            model, clip, _vae = wf.checkpointloadersimple(
                ckpt_name="sd1.5/juggernaut_reborn.safetensors"
            )
            wf.cliptextencode(clip=clip, text="first")
            wf.cliptextencode(clip=clip, text="second")
            wf.emptylatentimage(width=512, height=512, batch_size=1)
            wf.override({"cliptext_encode[0].text": "updated first"})

        payload = json.loads(wf.to_json())
        self.assertEqual(payload["2"]["inputs"]["text"], "updated first")

    def test_to_json_returns_valid_json(self):
        with mocked_comfy_api():
            wf = Workflow().checkpoint("sd1.5/juggernaut_reborn.safetensors").prompt(
                "robot"
            ).latent(512, 512)
            parsed = json.loads(wf.to_json())

        self.assertIsInstance(parsed, dict)
        self.assertEqual(parsed["1"]["class_type"], "CheckpointLoaderSimple")

    def test_then_combines_two_workflows(self):
        with mocked_comfy_api():
            wf1 = (
                Workflow()
                .checkpoint("sd1.5/juggernaut_reborn.safetensors")
                .prompt("robot")
                .latent(512, 512)
                .sample()
                .decode()
                .save("robot_a")
                .clone()
            )
            wf2 = (
                Workflow()
                .checkpoint("sd1.5/juggernaut_reborn.safetensors")
                .prompt("robot_b")
                .latent(512, 512)
                .sample()
                .decode()
                .save("robot_b")
                .clone()
            )

            combined = wf1.then(wf2)
            summary = combined.inspect(print_output=False)

        self.assertGreater(len(combined.nodes), len(wf1.nodes))
        self.assertIn("SaveImage [save]", summary)

    @unittest.skipUnless(importlib.util.find_spec("yaml"), "PyYAML not installed")
    def test_yaml_skill_loader_builds_workflow(self):
        with mocked_comfy_api():
            wf = load_yaml_skill(
                "workflow_examples_editable_skills/generate_sd15_image.yaml",
                prompt="robot",
                negative_prompt="bad",
            )
            summary = wf.inspect(print_output=False)

        self.assertIn("CheckpointLoaderSimple [checkpoint]", summary)
        self.assertIn("SaveImage [save]", summary)

    @unittest.skipIf(importlib.util.find_spec("yaml"), "PyYAML installed")
    def test_yaml_skill_loader_fallback_raises_clear_error(self):
        with self.assertRaises(ImportError) as context:
            load_yaml_skill("workflow_examples_editable_skills/generate_sd15_image.yaml")

        self.assertIn("PyYAML", str(context.exception))


if __name__ == "__main__":
    unittest.main()
