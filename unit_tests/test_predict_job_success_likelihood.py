import unittest
from types import SimpleNamespace
from unittest.mock import patch

from unit_tests.test_helpers import FAKE_REGISTRY


class PredictJobSuccessLikelihoodTests(unittest.TestCase):
    def test_predict_high_likelihood_with_good_dependencies_and_history(self):
        from skills.infra.predict_job_success_likelihood.skill import run

        fake_registry = {
            **FAKE_REGISTRY,
            "CheckpointLoaderSimple": {
                "output": ["MODEL", "CLIP", "VAE"],
                "output_name": ["MODEL", "CLIP", "VAE"],
                "input": {"required": {"ckpt_name": [["sd1.5/juggernaut_reborn.safetensors"], {}]}},
            },
        }

        workflow_payload = {
            "prompt": {
                "1": {
                    "class_type": "CheckpointLoaderSimple",
                    "inputs": {"ckpt_name": "sd1.5/juggernaut_reborn.safetensors"},
                },
                "2": {"class_type": "CLIPTextEncode", "inputs": {}},
                "3": {"class_type": "KSampler", "inputs": {}},
            }
        }

        history_payload = {
            "data": {
                "a": {
                    "prompt": workflow_payload["prompt"],
                    "outputs": {"7": {"images": [{"filename": "a.png"}]}},
                },
                "b": {
                    "prompt": workflow_payload["prompt"],
                    "outputs": {"7": {"images": [{"filename": "b.png"}]}},
                },
            }
        }

        with patch(
            "skills.infra.predict_job_success_likelihood.skill.Workflow",
            return_value=SimpleNamespace(registry=fake_registry),
        ), patch(
            "skills.infra.predict_job_success_likelihood.skill.fetch_json",
            return_value={"ok": True, **history_payload},
        ), patch(
            "skills.infra.predict_job_success_likelihood.skill.fetch_queue",
            return_value={"ok": True, "running": [], "pending": []},
        ), patch(
            "skills.infra.predict_job_success_likelihood.skill.fetch_system_stats",
            return_value={
                "ok": True,
                "stats": {"devices": [{"vram_free": 8 * 1024 * 1024 * 1024}]},
            },
        ):
            result = run(workflow_payload=workflow_payload, server="http://127.0.0.1:8000")

        self.assertEqual(result["status"], "ok")
        self.assertGreater(result["likelihood"], 0.7)
        self.assertEqual(result["recommendation"], "safe_to_run")

    def test_predict_low_likelihood_when_dependencies_missing(self):
        from skills.infra.predict_job_success_likelihood.skill import run

        fake_registry = {
            **FAKE_REGISTRY,
            "CheckpointLoaderSimple": {
                "output": ["MODEL", "CLIP", "VAE"],
                "output_name": ["MODEL", "CLIP", "VAE"],
                "input": {"required": {"ckpt_name": [["sd1.5/another_model.safetensors"], {}]}},
            },
        }

        workflow_payload = {
            "prompt": {
                "1": {
                    "class_type": "CheckpointLoaderSimple",
                    "inputs": {"ckpt_name": "sd1.5/missing_model.safetensors"},
                },
                "2": {"class_type": "MissingCustomNode", "inputs": {}},
                "3": {"class_type": "KSampler", "inputs": {}},
            }
        }

        with patch(
            "skills.infra.predict_job_success_likelihood.skill.Workflow",
            return_value=SimpleNamespace(registry=fake_registry),
        ), patch(
            "skills.infra.predict_job_success_likelihood.skill.fetch_json",
            return_value={"ok": True, "data": {}},
        ), patch(
            "skills.infra.predict_job_success_likelihood.skill.fetch_queue",
            return_value={"ok": True, "running": [], "pending": []},
        ), patch(
            "skills.infra.predict_job_success_likelihood.skill.fetch_system_stats",
            return_value={
                "ok": True,
                "stats": {"devices": [{"vram_free": 4 * 1024 * 1024 * 1024}]},
            },
        ):
            result = run(workflow_payload=workflow_payload, server="http://127.0.0.1:8000")

        self.assertEqual(result["status"], "ok")
        self.assertLess(result["likelihood"], 0.6)
        self.assertIn(result["recommendation"], {"run_with_caution", "fix_dependencies_first"})
        self.assertGreaterEqual(len(result["breakdown"]["dependencies"]["missing_class_types"]), 1)


if __name__ == "__main__":
    unittest.main()
