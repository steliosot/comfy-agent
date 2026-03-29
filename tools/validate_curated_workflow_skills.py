#!/usr/bin/env python3
import json
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
ROOT = REPO_ROOT / "skills" / "workflows"


def main():
    manifest_path = ROOT / "curated_manifest.json"
    if not manifest_path.exists():
        raise SystemExit("manifest.json is missing")

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    entries = manifest.get("entries", [])
    if len(entries) != 120:
        raise SystemExit(f"Expected 120 entries, found {len(entries)}")

    required_files = ["workflow.json", "SKILL.md", "skill.yaml", "skill.py", "scripts/run.py"]
    seen_ids = set()
    for item in entries:
        skill_id = item["id"]
        if skill_id in seen_ids:
            raise SystemExit(f"Duplicate skill id found: {skill_id}")
        seen_ids.add(skill_id)

        folder = Path(item["destination"])
        for rel in required_files:
            path = folder / rel
            if not path.exists():
                raise SystemExit(f"Missing required file: {path}")

        # Parse schema and frontmatter baseline fields
        skill_yaml = yaml.safe_load((folder / "skill.yaml").read_text(encoding="utf-8")) or {}
        if "name" not in skill_yaml or "inputs" not in skill_yaml or "outputs" not in skill_yaml:
            raise SystemExit(f"Invalid skill.yaml structure: {folder / 'skill.yaml'}")

        skill_md = (folder / "SKILL.md").read_text(encoding="utf-8")
        needed = [
            "metadata.clawdbot.os",
            "metadata.clawdbot.requires.bins",
            "metadata.clawdbot.requires.env",
            "metadata.clawdbot.input_type",
            "metadata.clawdbot.output_type",
        ]
        for token in needed:
            if token not in skill_md:
                raise SystemExit(f"Missing frontmatter token '{token}' in {folder / 'SKILL.md'}")

    print(json.dumps({"status": "ok", "entries": len(entries)}, indent=2))


if __name__ == "__main__":
    main()
