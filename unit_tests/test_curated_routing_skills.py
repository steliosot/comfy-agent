import unittest
from unittest.mock import patch

from skills.infra.list_curated_workflows.skill import run as list_curated_workflows
from skills.infra.match_curated_workflow.skill import run as match_curated_workflow
from skills.workflows.txt2img.run_curated_workflow.skill import run as run_curated_workflow


class CuratedRoutingSkillsTests(unittest.TestCase):
    def test_list_curated_workflows_returns_items(self):
        result = list_curated_workflows(limit=5)
        self.assertEqual(result["status"], "ok")
        self.assertGreaterEqual(result["count"], 1)
        self.assertLessEqual(result["count"], 5)

    def test_match_curated_workflow_prefers_video_family_for_video_prompt(self):
        result = match_curated_workflow(prompt="cinematic travel video of a greek island", top_k=3)
        self.assertEqual(result["status"], "ok")
        self.assertGreaterEqual(len(result["matches"]), 1)
        self.assertEqual(result["matches"][0]["family"], "video_t2v_i2v_avatar")

    def test_run_curated_workflow_by_id(self):
        matches = match_curated_workflow(prompt="cinematic portrait image", top_k=1)
        skill_id = matches["matches"][0]["id"]

        with patch(
            "skills.workflows.txt2img.run_curated_workflow.skill._run_curated",
            return_value={"status": "done", "prompt_id": "test-prompt", "output_images": []},
        ):
            result = run_curated_workflow(skill_id=skill_id, prompt="portrait photo")

        self.assertEqual(result["status"], "done")
        self.assertEqual(result["skill"], "run_curated_workflow")
        self.assertEqual(result["skill_id"], skill_id)


if __name__ == "__main__":
    unittest.main()
