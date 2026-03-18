import runpy
import unittest
from unittest.mock import patch

from unit_tests.test_helpers import mocked_comfy_api


class AgentAndExampleTests(unittest.TestCase):
    def test_image_agent_parallel_example(self):
        import agent_examples.example_agent_parallel as example_module

        with patch.object(
            example_module, "generate_image", side_effect=lambda prompt: {"prompt": prompt}
        ):
            agent = example_module.ImageAgent()
            results = agent.run("greek island")

        self.assertEqual(len(results), 3)
        self.assertEqual(results[0]["prompt"], "greek island")
        self.assertEqual(results[1]["prompt"], "greek island cinematic lighting")

    def test_simple_pipelining_example_runs(self):
        with mocked_comfy_api() as posted:
            runpy.run_path(
                "workflow_examples_simple_pipelining/example_minimal_pipeline.py",
                run_name="__main__",
            )

        self.assertEqual(len(posted), 1)

    def test_buildable_skill_example_runs(self):
        with mocked_comfy_api() as posted:
            runpy.run_path(
                "skill_examples_buildable/example_build_then_run.py",
                run_name="__main__",
            )

        self.assertEqual(len(posted), 1)

    def test_editable_override_example_runs(self):
        with mocked_comfy_api() as posted:
            runpy.run_path(
                "workflow_examples_editable_skills/example_clone_override.py",
                run_name="__main__",
            )

        self.assertEqual(len(posted), 1)

    def test_inspect_json_example_runs(self):
        with mocked_comfy_api():
            runpy.run_path(
                "workflow_examples_editable_skills/example_inspect_and_json.py",
                run_name="__main__",
            )


if __name__ == "__main__":
    unittest.main()
