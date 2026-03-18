import unittest
from unittest.mock import patch

from comfy_agent.job import Executor, Job
from comfy_agent.skill_registry import SkillRegistry


class JobAndRegistryTests(unittest.TestCase):
    def test_job_run_returns_skill_result(self):
        job = Job(lambda prompt: {"prompt": prompt}, prompt="robot")
        self.assertEqual(job.run(), {"prompt": "robot"})

    def test_executor_run_parallel_returns_all_results(self):
        jobs = [
            Job(lambda value=i: value) for i in range(3)
        ]

        executor = Executor(workers=2)
        results = executor.run_parallel(jobs)

        self.assertEqual(results, [0, 1, 2])

    def test_skill_registry_register_and_get(self):
        SkillRegistry._skills = {}
        SkillRegistry.register("demo", lambda: "ok")
        self.assertEqual(SkillRegistry.get("demo")(), "ok")

    def test_skill_registry_load_skills_registers_run_functions(self):
        SkillRegistry._skills = {}

        fake_modules = {
            "skills.alpha.skill": type("M", (), {"run": staticmethod(lambda: "alpha")}),
            "skills.beta.skill": type("M", (), {"run": staticmethod(lambda: "beta")}),
        }

        with patch("comfy_agent.skill_registry.os.listdir", return_value=["alpha", "beta"]), patch(
            "comfy_agent.skill_registry.os.path.isdir", return_value=True
        ), patch(
            "comfy_agent.skill_registry.importlib.import_module",
            side_effect=lambda name: fake_modules[name],
        ):
            SkillRegistry.load_skills()

        self.assertEqual(SkillRegistry.get("alpha")(), "alpha")
        self.assertEqual(SkillRegistry.get("beta")(), "beta")
