import unittest
from unittest.mock import patch


class MonitoringSkillTests(unittest.TestCase):
    def test_get_server_status_reports_counts(self):
        from skills.get_server_status.skill import run

        with patch("skills.get_server_status.skill.fetch_queue", return_value={"ok": True, "running": [[1, "a"]], "pending": [], "url": "u"}), patch(
            "skills.get_server_status.skill.fetch_system_stats",
            return_value={"ok": True, "stats": {"system": {"os": "linux"}}, "url": "s"},
        ):
            result = run(server="http://x", headers={})

        self.assertEqual(result["status"], "ok")
        self.assertEqual(result["running_count"], 1)
        self.assertEqual(result["pending_count"], 0)
        self.assertTrue(result["busy"])

    def test_get_progress_queue_heuristic_running_ramps_up(self):
        from skills.get_progress.skill import run

        with patch("skills.get_progress.skill.fetch_progress", return_value={"ok": False, "error": "404"}), patch(
            "skills.get_progress.skill.fetch_queue",
            return_value={"ok": True, "running": [[1, "pid1"]], "pending": []},
        ), patch(
            "skills.get_progress.skill.fetch_history_entry",
            return_value={"ok": True, "entry": None},
        ), patch(
            "skills.get_progress.skill.time.monotonic",
            side_effect=[0.0, 120.0],
        ), patch.dict(
            "os.environ",
            {"COMFY_PROGRESS_EXPECTED_SECONDS": "600"},
            clear=False,
        ):
            result1 = run(prompt_id="pid1", server="http://x", headers={})
            result2 = run(prompt_id="pid1", server="http://x", headers={})

        self.assertEqual(result1["source"], "queue_heuristic")
        self.assertEqual(result1["state"], "running")
        self.assertGreaterEqual(result1["progress_percent"], 20.0)
        self.assertGreater(result2["progress_percent"], result1["progress_percent"])


if __name__ == "__main__":
    unittest.main()
