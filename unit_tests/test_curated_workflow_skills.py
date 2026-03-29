import importlib
import json
import unittest
from pathlib import Path
from unittest.mock import patch


REPO_ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = REPO_ROOT / "skills" / "workflows" / "curated_manifest.json"


class CuratedWorkflowSkillsTests(unittest.TestCase):
    def test_manifest_and_required_files(self):
        self.assertTrue(MANIFEST_PATH.exists(), "skills/workflows/curated_manifest.json is missing")
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        entries = manifest.get("entries", [])
        self.assertEqual(len(entries), 120)

        for entry in entries:
            folder = Path(entry["destination"])
            self.assertTrue((folder / "workflow.json").exists())
            self.assertTrue((folder / "SKILL.md").exists())
            self.assertTrue((folder / "skill.yaml").exists())
            self.assertTrue((folder / "skill.py").exists())
            self.assertTrue((folder / "scripts" / "run.py").exists())

    def test_smoke_run_12_skills_with_mocked_runtime(self):
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        entries = manifest.get("entries", [])[:12]
        self.assertEqual(len(entries), 12)

        for entry in entries:
            skill_id = entry["id"]
            family = entry["family"]
            module_name = f"skills.workflows.{family}.{skill_id}.skill"
            module = importlib.import_module(module_name)
            with patch.object(
                module,
                "run_curated_workflow",
                return_value={"status": "done", "prompt_id": "test", "output_images": []},
            ) as mocked:
                result = module.run(prompt="test prompt")
                self.assertEqual(result["status"], "done")
                self.assertIn("prompt_id", result)
                mocked.assert_called_once()


if __name__ == "__main__":
    unittest.main()
