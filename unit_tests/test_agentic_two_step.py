import unittest
from unittest.mock import patch

from comfy_agent import agentic_command, agentic_execute, agentic_plan


class _FakeWorkflow:
    def __init__(self, server=None, headers=None, api_prefix=None):
        self.server = server
        self.headers = headers
        self.api_prefix = api_prefix

    def checkpointloadersimple(self, ckpt_name):
        return ("model", "clip", "vae")

    def cliptextencode(self, clip, text):
        return "conditioning"

    def emptylatentimage(self, width, height, batch_size):
        return "latent"

    def ksampler(self, **kwargs):
        return "samples"

    def vaedecode(self, samples, vae):
        return "image"

    def saveimage(self, images, filename_prefix):
        return None

    def imagecrop(self, image, x, y, width, height):
        return "cropped"

    def run(self):
        return {"prompt_id": "plan-exec-test"}

    def saved_images(self, prompt_id):
        return [
            {
                "filename": "ComfyUI_00001_.png",
                "subfolder": "",
                "type": "output",
                "node_id": "7",
                "output_kind": "images",
            }
        ]


class AgenticTwoStepTests(unittest.TestCase):
    def test_plan_image_prompt(self):
        result = agentic_plan("generate an image of a robot", auto_prepare=False)
        self.assertEqual(result["status"], "planned")
        self.assertIn("prepare_workflow_dependencies", result["steps"])
        self.assertIn("generate_sd15_image", result["steps"])
        self.assertIn("params", result)
        self.assertEqual(result["plan_version"], "1.0")

    def test_plan_video_prompt(self):
        result = agentic_plan("generate a short video clip of a robot in the city", auto_prepare=False)
        self.assertEqual(result["status"], "planned")
        self.assertIn("generate_video_clip", result["steps"])

    def test_plan_generate_then_crop_prompt(self):
        result = agentic_plan("generate a robot then crop to 1280x720", auto_prepare=False)
        self.assertEqual(result["status"], "planned")
        self.assertEqual(result["params"]["crop"]["width"], 1280)
        self.assertEqual(result["params"]["crop"]["height"], 720)
        self.assertIn("crop_image", result["steps"])

    def test_execute_rejects_malformed_payload(self):
        result = agentic_execute({"plan_version": "1.0"})
        self.assertEqual(result["status"], "error")
        self.assertEqual(result["error"], "invalid_plan_payload")

    def test_execute_rejects_plan_version_mismatch(self):
        result = agentic_execute(
            {
                "plan_version": "0.1",
                "prompt": "test",
                "generation_prompt": "test",
                "steps": ["generate_sd15_image"],
                "params": {},
                "choices": [],
            }
        )
        self.assertEqual(result["status"], "error")
        self.assertEqual(result["error"], "unsupported_plan_version")

    def test_execute_valid_plan_runs(self):
        plan = agentic_plan("generate an image of a robot", auto_prepare=False)
        with patch("comfy_agent.agentic.Workflow", _FakeWorkflow):
            result = agentic_execute(plan)
        self.assertEqual(result["status"], "done")
        self.assertEqual(result["prompt_id"], "plan-exec-test")
        self.assertIsInstance(result.get("output_images"), list)

    def test_slash_plan_routes(self):
        with patch("comfy_agent.agentic.agentic_plan", return_value={"status": "planned"}) as mocked:
            result = agentic_command("/plan generate a robot")
            self.assertEqual(result["status"], "planned")
            mocked.assert_called_once()

    def test_slash_execute_without_payload_fails(self):
        result = agentic_command("/execute")
        self.assertEqual(result["status"], "error")
        self.assertEqual(result["error"], "missing_plan_payload")

    def test_slash_execute_with_payload_routes(self):
        payload = {"plan_version": "1.0", "prompt": "x", "generation_prompt": "x", "steps": ["a"], "params": {}, "choices": []}
        with patch("comfy_agent.agentic.agentic_execute", return_value={"status": "done"}) as mocked:
            result = agentic_command("/execute", plan_payload=payload)
            self.assertEqual(result["status"], "done")
            mocked.assert_called_once()

    def test_plan_skill_wrapper(self):
        from skills.infra.agentic_plan.skill import run as plan_skill

        result = plan_skill(prompt="generate an image", auto_prepare=False)
        self.assertEqual(result["status"], "planned")

    def test_execute_skill_wrapper(self):
        from skills.infra.agentic_execute.skill import run as execute_skill

        plan = agentic_plan("generate an image of a robot", auto_prepare=False)
        with patch("comfy_agent.agentic.Workflow", _FakeWorkflow):
            result = execute_skill(plan_payload=plan)
        self.assertEqual(result["status"], "done")


if __name__ == "__main__":
    unittest.main()
