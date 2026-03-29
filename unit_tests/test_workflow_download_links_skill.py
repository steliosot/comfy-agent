import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from skills.get_workflow_download_links.skill import run as get_workflow_download_links


class WorkflowDownloadLinksSkillTests(unittest.TestCase):
    def test_extract_links_from_workflow_path(self):
        with TemporaryDirectory() as tmpdir:
            workflow_path = Path(tmpdir) / "workflow.json"
            workflow_path.write_text(
                json.dumps(
                    {
                        "nodes": [
                            {
                                "id": 1,
                                "type": "Note",
                                "widgets_values": [
                                    "https://huggingface.co/foo/bar "
                                    "https://civitai.com/models/1234 "
                                    "https://github.com/foo/bar"
                                ],
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )

            result = get_workflow_download_links(workflow_path=str(workflow_path))
            self.assertEqual(result["status"], "ok")
            self.assertEqual(result["total_links"], 3)
            self.assertIn("huggingface", result["links_by_provider"])
            self.assertIn("civitai", result["links_by_provider"])
            self.assertIn("github", result["links_by_provider"])

    def test_extract_links_from_curated_skill_id(self):
        manifest_path = Path(__file__).resolve().parents[1] / "skills" / "curated_workflows" / "manifest.json"
        if not manifest_path.exists():
            self.skipTest("curated manifest not found")

        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        entries = manifest.get("entries", [])
        if not entries:
            self.skipTest("no curated entries found")

        skill_id = entries[0]["id"]
        result = get_workflow_download_links(skill_id=skill_id)
        self.assertEqual(result["status"], "ok")
        self.assertEqual(result["skill_id"], skill_id)
        self.assertIn("workflow_path", result)
        self.assertIsInstance(result["links"], list)


if __name__ == "__main__":
    unittest.main()
