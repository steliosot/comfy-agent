import unittest
from unittest.mock import patch


class CleanupSkillTests(unittest.TestCase):
    def test_delete_image_job_rejects_non_image_prompt(self):
        from skills.delete_image_job.skill import run

        with patch(
            "skills.delete_image_job.skill.fetch_history_entry",
            return_value={"ok": True, "entry": {"outputs": {"1": {"gifs": [{"filename": "x.mp4"}]}}}},
        ):
            result = run(prompt_id="pid", server="http://x", headers={})

        self.assertEqual(result["status"], "error")
        self.assertEqual(result["error"], "prompt_has_no_image_outputs")

    def test_delete_video_job_rejects_non_video_prompt(self):
        from skills.delete_video_job.skill import run

        with patch(
            "skills.delete_video_job.skill.fetch_history_entry",
            return_value={"ok": True, "entry": {"outputs": {"1": {"images": [{"filename": "x.png"}]}}}},
        ):
            result = run(prompt_id="pid", server="http://x", headers={})

        self.assertEqual(result["status"], "error")
        self.assertEqual(result["error"], "prompt_has_no_video_outputs")


if __name__ == "__main__":
    unittest.main()
