import os
import tempfile
import unittest
from unittest.mock import patch

from comfy_agent.config import ComfyConfig, load_env_file
from comfy_agent.workflow import Workflow


class ConfigTests(unittest.TestCase):
    def test_load_env_file_populates_variables(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            env_path = os.path.join(tmp_dir, ".env")
            with open(env_path, "w", encoding="utf-8") as f:
                f.write("COMFY_URL=http://34.27.83.101\n")
                f.write("COMFY_AUTH_HEADER='token123'\n")
                f.write("COMFY_OUTPUT_DIR=tmp/out\n")

            with patch.dict(os.environ, {}, clear=True):
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
            },
            clear=True,
        ), patch("comfy_agent.workflow.requests.get", side_effect=fake_get):
            Workflow()

        self.assertEqual(captured["headers"], {"Authorization": "secret-header"})


if __name__ == "__main__":
    unittest.main()
