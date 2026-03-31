import os
import tempfile
import unittest
from unittest.mock import patch

from comfy_agent.config import ComfyConfig, get_server_config, load_env_file
from comfy_agent.workflow import Workflow


class ConfigTests(unittest.TestCase):
    def test_load_env_file_populates_variables(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            env_path = os.path.join(tmp_dir, ".env")
            with open(env_path, "w", encoding="utf-8") as f:
                f.write("COMFY_URL=http://34.27.83.101\n")
                f.write("COMFY_AUTH_HEADER='token123'\n")
                f.write("COMFY_OUTPUT_DIR=tmp/out\n")

            with patch.dict(
                os.environ,
                {"COMFY_SERVERS_FILE": "/tmp/nonexistent_comfy_servers.yaml"},
                clear=True,
            ):
                loaded = load_env_file(path=env_path, override=False)
                cfg = ComfyConfig.from_env(load_env=False)

        self.assertTrue(loaded)
        self.assertEqual(cfg.server, "http://34.27.83.101")
        self.assertEqual(cfg.headers.get("Authorization"), "token123")
        self.assertEqual(cfg.output_dir, "tmp/out")

    def test_workflow_uses_env_auth_header_when_headers_not_passed(self):
        captured = {"headers": None}

        def fake_get(url, *args, **kwargs):
            captured["headers"] = kwargs.get("headers")

            class Response:
                ok = True
                status_code = 200

                @staticmethod
                def json():
                    return {"CheckpointLoaderSimple": {"output": ["MODEL", "CLIP", "VAE"], "output_name": ["MODEL", "CLIP", "VAE"]}}

                @staticmethod
                def raise_for_status():
                    return None

            return Response()

        with patch.dict(
            os.environ,
            {
                "COMFY_URL": "localhost:8000",
                "COMFY_AUTH_HEADER": "secret-header",
                "COMFY_SERVERS_FILE": "/tmp/nonexistent_comfy_servers.yaml",
            },
            clear=True,
        ), patch("comfy_agent.workflow.requests.get", side_effect=fake_get):
            Workflow()

        self.assertEqual(captured["headers"], {"Authorization": "secret-header"})

    def test_get_server_config_from_yaml_named(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            servers_path = os.path.join(tmp_dir, ".comfy_servers.yaml")
            with open(servers_path, "w", encoding="utf-8") as f:
                f.write("default_server: local\n")
                f.write("servers:\n")
                f.write("  local:\n")
                f.write("    url: localhost:8188\n")
                f.write("    headers:\n")
                f.write("      Authorization: Bearer abc\n")
                f.write("    api_prefix: /api\n")
                f.write("    manager_api_prefix: /manager\n")
                f.write("  cloud:\n")
                f.write("    url: https://example.com/comfy\n")

            with patch.dict(
                os.environ,
                {
                    "COMFY_SERVERS_FILE": servers_path,
                    "COMFY_URL": "http://127.0.0.1:8000",
                },
                clear=True,
            ):
                resolved = get_server_config(name="local", load_env=False)

        self.assertEqual(resolved["server_name"], "local")
        self.assertEqual(resolved["server"], "http://localhost:8188")
        self.assertEqual(resolved["headers"]["Authorization"], "Bearer abc")
        self.assertEqual(resolved["api_prefix"], "/api")
        self.assertEqual(resolved["manager_api_prefix"], "/manager")
        self.assertEqual(resolved["source"], "servers_file")

    def test_get_server_config_default_server_fallback(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            servers_path = os.path.join(tmp_dir, ".comfy_servers.yaml")
            with open(servers_path, "w", encoding="utf-8") as f:
                f.write("default_server: cloud\n")
                f.write("servers:\n")
                f.write("  cloud:\n")
                f.write("    url: https://cloud.example.net\n")
                f.write("    api_prefix: api\n")

            with patch.dict(
                os.environ,
                {
                    "COMFY_SERVERS_FILE": servers_path,
                    "COMFY_URL": "http://127.0.0.1:8000",
                },
                clear=True,
            ):
                resolved = get_server_config(name=None, load_env=False)

        self.assertEqual(resolved["server_name"], "cloud")
        self.assertEqual(resolved["server"], "https://cloud.example.net")
        self.assertEqual(resolved["api_prefix"], "/api")
        self.assertEqual(resolved["source"], "servers_file")


    def test_get_server_config_yaml_without_default_falls_back_to_env(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            servers_path = os.path.join(tmp_dir, ".comfy_servers.yaml")
            with open(servers_path, "w", encoding="utf-8") as f:
                f.write("servers:\n")
                f.write("  local:\n")
                f.write("    url: localhost:8188\n")

            with patch.dict(
                os.environ,
                {
                    "COMFY_SERVERS_FILE": servers_path,
                    "COMFY_URL": "localhost:9000",
                    "COMFY_AUTH_HEADER": "Bearer env-token",
                },
                clear=True,
            ):
                resolved = get_server_config(name=None, load_env=False)

        self.assertIsNone(resolved["server_name"])
        self.assertEqual(resolved["server"], "http://localhost:9000")
        self.assertEqual(resolved["headers"].get("Authorization"), "Bearer env-token")
        self.assertEqual(resolved["source"], "env")

    def test_get_server_config_unknown_name_raises(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            servers_path = os.path.join(tmp_dir, ".comfy_servers.yaml")
            with open(servers_path, "w", encoding="utf-8") as f:
                f.write("default_server: local\n")
                f.write("servers:\n")
                f.write("  local:\n")
                f.write("    url: localhost:8188\n")

            with patch.dict(
                os.environ,
                {
                    "COMFY_SERVERS_FILE": servers_path,
                },
                clear=True,
            ):
                with self.assertRaises(ValueError):
                    get_server_config(name="missing", load_env=False)

    def test_from_env_uses_yaml_default_server_when_available(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            servers_path = os.path.join(tmp_dir, ".comfy_servers.yaml")
            with open(servers_path, "w", encoding="utf-8") as f:
                f.write("default_server: local\n")
                f.write("servers:\n")
                f.write("  local:\n")
                f.write("    url: localhost:8288\n")
                f.write("    headers:\n")
                f.write("      Authorization: Token 123\n")
                f.write("    api_prefix: /api\n")

            with patch.dict(
                os.environ,
                {
                    "COMFY_SERVERS_FILE": servers_path,
                    "COMFY_URL": "http://127.0.0.1:8000",
                },
                clear=True,
            ):
                cfg = ComfyConfig.from_env(load_env=False)

        self.assertEqual(cfg.server, "http://localhost:8288")
        self.assertEqual(cfg.headers.get("Authorization"), "Token 123")
        self.assertEqual(cfg.api_prefix, "/api")


if __name__ == "__main__":
    unittest.main()
