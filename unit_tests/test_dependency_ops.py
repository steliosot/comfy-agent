import os
import unittest
from types import SimpleNamespace
from unittest.mock import patch

from comfy_agent import run_agentic
from comfy_agent.config import ComfyConfig
from comfy_agent.manager import manager_probe
from unit_tests.test_helpers import FAKE_REGISTRY, mocked_comfy_api


class _FakeHTTPResponse:
    def __init__(self, ok, status_code=200, payload=None, text=""):
        self.ok = ok
        self.status_code = status_code
        self._payload = payload
        self.text = text

    def json(self):
        if self._payload is None:
            raise ValueError("no-json")
        return self._payload


class DependencyOpsTests(unittest.TestCase):
    def test_config_reads_dependency_env_vars(self):
        with patch.dict(
            os.environ,
            {
                "COMFY_URL": "localhost:8000",
                "COMFY_SERVERS_FILE": "/tmp/nonexistent_comfy_servers.yaml",
                "COMFY_MANAGER_API_PREFIX": "/manager",
                "HF_TOKEN": "hf_test",
                "CIVITAI_API_KEY": "cv_test",
                "COMFY_RESOURCE_MIN_FREE_VRAM_MB": "4096",
                "COMFY_RESOURCE_MIN_FREE_STORAGE_GB": "120",
            },
            clear=True,
        ):
            cfg = ComfyConfig.from_env(load_env=False)

        self.assertEqual(cfg.server, "http://localhost:8000")
        self.assertEqual(cfg.manager_api_prefix, "/manager")
        self.assertEqual(cfg.hf_token, "hf_test")
        self.assertEqual(cfg.civitai_api_key, "cv_test")
        self.assertEqual(cfg.resource_min_free_vram_mb, 4096.0)
        self.assertEqual(cfg.resource_min_free_storage_gb, 120.0)

    def test_manager_probe_missing(self):
        def fake_request(method, url, **kwargs):
            return _FakeHTTPResponse(ok=False, status_code=404, text="not found")

        with patch("comfy_agent.manager.requests.request", side_effect=fake_request):
            result = manager_probe(server="http://127.0.0.1:8000")

        self.assertFalse(result["ok"])
        self.assertFalse(result["manager_available"])

    def test_manager_probe_available(self):
        def fake_request(method, url, **kwargs):
            if url.endswith("/status"):
                return _FakeHTTPResponse(ok=True, status_code=200, payload={"ok": True})
            return _FakeHTTPResponse(ok=False, status_code=404, text="not found")

        with patch("comfy_agent.manager.requests.request", side_effect=fake_request):
            result = manager_probe(server="http://127.0.0.1:8000")

        self.assertTrue(result["ok"])
        self.assertTrue(result["manager_available"])
        self.assertIn("model_install", result["supported_operations"])

    def test_assess_server_resources_warn_and_block_modes(self):
        from skills.infra.assess_server_resources.skill import run

        stats_payload = {
            "ok": True,
            "stats": {
                "devices": [{"vram_total": 8 * 1024 * 1024 * 1024, "vram_free": 1024}],
                "system": {"free_disk_gb": 2.0},
            },
        }
        queue_payload = {"ok": True, "running": [1], "pending": [2]}

        with patch("skills.infra.assess_server_resources.skill.fetch_system_stats", return_value=stats_payload), patch(
            "skills.infra.assess_server_resources.skill.fetch_queue", return_value=queue_payload
        ):
            warn_result = run(min_vram_mb=2048, min_storage_gb=5, warn_only=True, server="x")
            block_result = run(min_vram_mb=2048, min_storage_gb=5, warn_only=False, server="x")

        self.assertEqual(warn_result["status"], "ok")
        self.assertGreater(len(warn_result["warnings"]), 0)
        self.assertEqual(block_result["status"], "blocked")
        self.assertGreater(len(block_result["blockers"]), 0)

    def test_download_model_success(self):
        from skills.infra.download_model.skill import run

        fake_cfg = SimpleNamespace(
            server="http://127.0.0.1:8000",
            headers={},
            api_prefix=None,
            manager_api_prefix="/manager",
            hf_token="hf_test_token",
            civitai_api_key=None,
            resource_min_free_vram_mb=None,
            resource_min_free_storage_gb=None,
            input_dir="tmp/inputs",
            output_dir="tmp/outputs",
        )

        fake_registry = {
            **FAKE_REGISTRY,
            "CheckpointLoaderSimple": {
                "output": ["MODEL", "CLIP", "VAE"],
                "output_name": ["MODEL", "CLIP", "VAE"],
                "input": {"required": {"ckpt_name": [["sd1.5/test_model.safetensors"], {}]}},
            },
        }

        class FakeWorkflow:
            def __init__(self, *args, **kwargs):
                self.registry = fake_registry

        with patch("skills.infra.download_model.skill.ComfyConfig.from_env", return_value=fake_cfg), patch(
            "skills.infra.download_model.skill.manager_install",
            return_value={"ok": True, "manager_available": True, "endpoint": "/model/install"},
        ), patch("skills.infra.download_model.skill.Workflow", FakeWorkflow):
            result = run(
                source="huggingface",
                model_id_or_url="owner/repo",
                filename="sd1.5/test_model.safetensors",
                model_type="checkpoint",
                server="http://127.0.0.1:8000",
            )

        self.assertEqual(result["status"], "ok")
        self.assertTrue(result["verification"]["verified"])
        self.assertTrue(result["token_used"])

    def test_download_model_diffusion_model_maps_to_diffusion_models_folder(self):
        from skills.infra.download_model.skill import run

        fake_cfg = SimpleNamespace(
            server="http://127.0.0.1:8000",
            headers={},
            api_prefix=None,
            manager_api_prefix="/manager",
            hf_token="hf_test_token",
            civitai_api_key=None,
            resource_min_free_vram_mb=None,
            resource_min_free_storage_gb=None,
            input_dir="tmp/inputs",
            output_dir="tmp/outputs",
        )

        fake_registry = {
            **FAKE_REGISTRY,
            "UNETLoader": {
                "output": ["MODEL"],
                "output_name": ["MODEL"],
                "input": {
                    "required": {
                        "unet_name": [["wan2.1/lightweight_unet.safetensors"], {}],
                    }
                },
            },
        }

        class FakeWorkflow:
            def __init__(self, *args, **kwargs):
                self.registry = fake_registry

        with patch("skills.infra.download_model.skill.ComfyConfig.from_env", return_value=fake_cfg), patch(
            "skills.infra.download_model.skill.manager_install",
            return_value={"ok": True, "manager_available": True, "endpoint": "/model/install"},
        ) as install_mock, patch("skills.infra.download_model.skill.Workflow", FakeWorkflow):
            result = run(
                source="huggingface",
                model_id_or_url="owner/repo",
                filename="wan2.1/lightweight_unet.safetensors",
                model_type="diffusion_model",
                server="http://127.0.0.1:8000",
            )

        self.assertEqual(result["status"], "ok")
        self.assertEqual(result["target_subfolder"], "models/diffusion_models")
        self.assertTrue(result["verification"]["verified"])
        payload = install_mock.call_args.kwargs["payload"]
        self.assertEqual(payload["subfolder"], "models/diffusion_models")

    def test_install_custom_node_success(self):
        from skills.infra.install_custom_node.skill import run

        fake_cfg = SimpleNamespace(
            server="http://127.0.0.1:8000",
            headers={},
            api_prefix=None,
            manager_api_prefix="/manager",
            hf_token=None,
            civitai_api_key=None,
            resource_min_free_vram_mb=None,
            resource_min_free_storage_gb=None,
            input_dir="tmp/inputs",
            output_dir="tmp/outputs",
        )

        class FakeWorkflow:
            def __init__(self, *args, **kwargs):
                self.registry = {**FAKE_REGISTRY, "VHS_VideoCombine": {"output": [], "output_name": []}}

        with patch("skills.infra.install_custom_node.skill.ComfyConfig.from_env", return_value=fake_cfg), patch(
            "skills.infra.install_custom_node.skill.manager_install",
            return_value={"ok": True, "manager_available": True, "endpoint": "/custom_nodes/install"},
        ), patch("skills.infra.install_custom_node.skill.Workflow", FakeWorkflow):
            result = run(
                repo_url="https://github.com/Kosinkadink/ComfyUI-VideoHelperSuite",
                expected_node_classes=["VHS_VideoCombine"],
            )

        self.assertEqual(result["status"], "ok")
        self.assertTrue(result["verification"]["verified"])

    def test_model_folder_guide_for_unet(self):
        from skills.infra.model_folder_guide.skill import run

        result = run(model_type="unet")
        self.assertEqual(result["status"], "ok")
        self.assertEqual(result["entry"]["folder"], "models/diffusion_models")
        self.assertEqual(result["entry"]["loader"], "UNETLoader")

    def test_remove_model_success(self):
        from skills.infra.remove_model.skill import run

        fake_cfg = SimpleNamespace(
            server="http://127.0.0.1:8000",
            headers={},
            api_prefix=None,
            manager_api_prefix="/manager",
            hf_token=None,
            civitai_api_key=None,
            resource_min_free_vram_mb=None,
            resource_min_free_storage_gb=None,
            input_dir="tmp/inputs",
            output_dir="tmp/outputs",
        )

        fake_registry = {
            **FAKE_REGISTRY,
            "LoraLoaderModelOnly": {
                "output": ["MODEL"],
                "output_name": ["MODEL"],
                "input": {"required": {"lora_name": [["existing_lora.safetensors"], {}]}},
            },
        }

        class FakeWorkflow:
            def __init__(self, *args, **kwargs):
                self.registry = fake_registry

        with patch("skills.infra.remove_model.skill.ComfyConfig.from_env", return_value=fake_cfg), patch(
            "skills.infra.remove_model.skill.manager_install",
            return_value={"ok": True, "manager_available": True, "endpoint": "/model/remove"},
        ), patch("skills.infra.remove_model.skill.Workflow", FakeWorkflow):
            result = run(
                filename="missing_now.safetensors",
                model_type="lora",
                server="http://127.0.0.1:8000",
            )

        self.assertEqual(result["status"], "ok")
        self.assertFalse(result["verification"]["present_after_remove"])
        self.assertTrue(result["verification"]["verified_removed"])

    def test_prepare_workflow_dependencies_all_present(self):
        from skills.infra.prepare_workflow_dependencies.skill import run

        class FakeWorkflow:
            def __init__(self, *args, **kwargs):
                self.registry = {
                    **FAKE_REGISTRY,
                    "CheckpointLoaderSimple": {
                        "output": ["MODEL", "CLIP", "VAE"],
                        "output_name": ["MODEL", "CLIP", "VAE"],
                        "input": {"required": {"ckpt_name": [["sd1.5/existing.safetensors"], {}]}},
                    },
                }

        workflow_payload = {
            "prompt": {
                "1": {
                    "class_type": "CheckpointLoaderSimple",
                    "inputs": {"ckpt_name": "sd1.5/existing.safetensors"},
                }
            }
        }

        with patch("skills.infra.prepare_workflow_dependencies.skill.Workflow", FakeWorkflow), patch(
            "skills.infra.prepare_workflow_dependencies.skill.assess_resources",
            return_value={"warnings": [], "blockers": [], "ready_for_install": True},
        ):
            result = run(workflow_payload=workflow_payload, auto_fix=False)

        self.assertTrue(result["ready_for_run"])
        self.assertEqual(result["still_missing"]["models"], [])
        self.assertEqual(result["still_missing"]["custom_nodes"], [])

    def test_prepare_workflow_dependencies_missing_both_then_fixed(self):
        from skills.infra.prepare_workflow_dependencies.skill import run

        registry_before = {
            **FAKE_REGISTRY,
            "CheckpointLoaderSimple": {
                "output": ["MODEL", "CLIP", "VAE"],
                "output_name": ["MODEL", "CLIP", "VAE"],
                "input": {"required": {"ckpt_name": [["sd1.5/other.safetensors"], {}]}},
            },
        }
        registry_after = {**registry_before, "VHS_VideoCombine": {"output": [], "output_name": []}}
        calls = {"count": 0}

        def fake_workflow(*args, **kwargs):
            calls["count"] += 1
            registry = registry_before if calls["count"] == 1 else registry_after
            return SimpleNamespace(registry=registry)

        workflow_payload = {
            "prompt": {
                "1": {
                    "class_type": "CheckpointLoaderSimple",
                    "inputs": {"ckpt_name": "sd1.5/new.safetensors"},
                },
                "2": {"class_type": "VHS_VideoCombine", "inputs": {}},
            }
        }

        requirements = {
            "models": [
                {
                    "name": "sd1.5/new.safetensors",
                    "model_type": "checkpoint",
                    "source": "huggingface",
                    "model_id_or_url": "owner/repo",
                    "filename": "sd1.5/new.safetensors",
                }
            ],
            "custom_nodes": [
                {
                    "repo_url": "https://github.com/Kosinkadink/ComfyUI-VideoHelperSuite",
                    "expected_node_classes": ["VHS_VideoCombine"],
                }
            ],
        }

        with patch("skills.infra.prepare_workflow_dependencies.skill.Workflow", side_effect=fake_workflow), patch(
            "skills.infra.prepare_workflow_dependencies.skill.assess_resources",
            return_value={"warnings": [], "blockers": [], "ready_for_install": True},
        ), patch(
            "skills.infra.prepare_workflow_dependencies.skill.download_model",
            return_value={"status": "ok", "verification": {"verified": True}},
        ), patch(
            "skills.infra.prepare_workflow_dependencies.skill.install_custom_node",
            return_value={"status": "ok"},
        ):
            result = run(workflow_payload=workflow_payload, requirements=requirements, auto_fix=True)

        self.assertTrue(result["ready_for_run"])
        self.assertEqual(result["still_missing"]["models"], [])
        self.assertEqual(result["still_missing"]["custom_nodes"], [])
        self.assertGreaterEqual(len(result["fixed"]["models"]), 1)
        self.assertGreaterEqual(len(result["fixed"]["custom_nodes"]), 1)

    def test_prepare_workflow_dependencies_handles_connectivity_error(self):
        from skills.infra.prepare_workflow_dependencies.skill import run

        with patch("skills.infra.prepare_workflow_dependencies.skill.Workflow", side_effect=RuntimeError("offline")):
            result = run(auto_fix=False)

        self.assertEqual(result["status"], "error")
        self.assertFalse(result["ready_for_run"])
        self.assertEqual(result["error"], "workflow_connectivity_failed")

    def test_run_agentic_preflight_error_is_actionable(self):
        with mocked_comfy_api(), patch(
            "skills.infra.prepare_workflow_dependencies.skill.run",
            return_value={"ready_for_run": False, "status": "degraded", "warnings": ["manager unavailable"]},
        ):
            result = run_agentic(prompt="generate an image of a robot", print_reasoning=False)

        self.assertEqual(result["status"], "error")
        self.assertEqual(result["skill"], "prepare_workflow_dependencies")
        self.assertIn("preflight", result)
        self.assertEqual(result["error"], "dependencies_not_ready")

    def test_run_agentic_preflight_warn_path_proceeds(self):
        with mocked_comfy_api(), patch(
            "skills.infra.prepare_workflow_dependencies.skill.run",
            return_value={"ready_for_run": True, "status": "ok", "warnings": ["low vram"]},
        ):
            result = run_agentic(prompt="generate an image of a robot", print_reasoning=False)

        self.assertEqual(result["status"], "done")
        self.assertIn("preflight", result)


if __name__ == "__main__":
    unittest.main()
