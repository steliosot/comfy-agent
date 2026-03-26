import unittest
from unittest.mock import patch

from comfy_agent.doctor import run_checks
from unit_tests.test_helpers import mocked_comfy_api


class DoctorTests(unittest.TestCase):
    def test_doctor_checks_connectivity_and_upload_download(self):
        with patch("pathlib.Path.exists", return_value=True), mocked_comfy_api():
            result = run_checks(
                env_path=".env",
                server="http://127.0.0.1:8000",
                skip_upload_download=False,
                verbose=False,
            )

        self.assertTrue(result["connectivity_ok"])
        self.assertTrue(result["upload_download_ok"])
        self.assertTrue(result["ok"])
        self.assertTrue(result["probe_download_path"])


if __name__ == "__main__":
    unittest.main()
