import unittest
from unittest.mock import patch


class MonitoringSkillTests(unittest.TestCase):
    def test_get_server_status_reports_counts(self):
        from skills.infra.get_server_status.skill import run

        with patch("skills.infra.get_server_status.skill.fetch_queue", return_value={"ok": True, "running": [[1, "a"]], "pending": [], "url": "u"}), patch(
            "skills.infra.get_server_status.skill.fetch_system_stats",
            return_value={"ok": True, "stats": {"system": {"os": "linux"}}, "url": "s"},
        ):
            result = run(server="http://x", headers={})

        self.assertEqual(result["status"], "ok")
        self.assertEqual(result["running_count"], 1)
        self.assertEqual(result["pending_count"], 0)
        self.assertTrue(result["busy"])

    def test_get_progress_queue_heuristic_running_ramps_up(self):
        from skills.infra.get_progress.skill import run

        with patch("skills.infra.get_progress.skill.fetch_progress", return_value={"ok": False, "error": "404"}), patch(
            "skills.infra.get_progress.skill.fetch_queue",
            return_value={"ok": True, "running": [[1, "pid1"]], "pending": []},
        ), patch(
            "skills.infra.get_progress.skill.fetch_history_entry",
            return_value={"ok": True, "entry": None},
        ), patch(
            "skills.infra.get_progress.skill.time.monotonic",
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

    def test_select_comfy_server_resolves_without_readiness_probe(self):
        from skills.infra.select_comfy_server.skill import run

        resolved = {
            "server_name": "cloud",
            "server": "https://cloud.example.net",
            "headers": {"Authorization": "Bearer test"},
            "api_prefix": "/api",
            "manager_api_prefix": "/manager",
            "source": "servers_file",
            "servers_file": "/tmp/.comfy_servers.yaml",
        }

        with patch("skills.infra.select_comfy_server.skill.get_server_config", return_value=resolved):
            result = run(server_name="cloud", require_ready=False)

        self.assertEqual(result["status"], "ok")
        self.assertIsNone(result["ready"])
        self.assertEqual(result["server"], "https://cloud.example.net")
        self.assertEqual(result["api_prefix"], "/api")

    def test_select_comfy_server_require_ready_blocked_when_object_info_fails(self):
        from skills.infra.select_comfy_server.skill import run

        resolved = {
            "server_name": "cloud",
            "server": "https://cloud.example.net",
            "headers": {},
            "api_prefix": "/api",
            "manager_api_prefix": "/manager",
            "source": "servers_file",
            "servers_file": "/tmp/.comfy_servers.yaml",
        }

        with patch("skills.infra.select_comfy_server.skill.get_server_config", return_value=resolved), patch(
            "skills.infra.select_comfy_server.skill.fetch_json",
            return_value={"ok": False, "url": "https://cloud.example.net/api/object_info", "error": "HTTP 404"},
        ), patch(
            "skills.infra.select_comfy_server.skill.manager_probe",
            return_value={"ok": False, "manager_available": False, "root": None, "error": "missing"},
        ):
            result = run(server_name="cloud", require_ready=True)

        self.assertEqual(result["status"], "blocked")
        self.assertFalse(result["ready"])
        self.assertIn("/object_info", result["message"])


if __name__ == "__main__":
    unittest.main()
