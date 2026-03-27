import unittest
from pathlib import Path


class SkillPackagingTests(unittest.TestCase):
    def test_all_skills_have_docs_and_cli_wrapper(self):
        repo_root = Path(__file__).resolve().parents[1]
        skills_root = repo_root / "skills"

        missing = []
        for skill_py in sorted(skills_root.glob("*/skill.py")):
            skill_dir = skill_py.parent
            expected = [
                skill_dir / "skill.yaml",
                skill_dir / "SKILL.md",
                skill_dir / "scripts" / "run.py",
            ]
            for path in expected:
                if not path.exists():
                    missing.append(str(path))

        if missing:
            self.fail("Missing required skill package files:\n" + "\n".join(missing))


if __name__ == "__main__":
    unittest.main()
