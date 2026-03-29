#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path


THIS = Path(__file__).resolve()
REPO_ROOT = THIS.parents[4]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from skills.workflows.txt2img.workflow_05_z_image_turbo_txt2img_bf16_lora.skill import run


def main():
    parser = argparse.ArgumentParser(description="Run workflow skill: workflow_05_z_image_turbo_txt2img_bf16_lora")
    parser.add_argument("--args", default="{}", help="JSON object with kwargs for run(...)")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output")
    args = parser.parse_args()

    kwargs = json.loads(args.args)
    result = run(**kwargs)
    if args.pretty:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(json.dumps(result))


if __name__ == "__main__":
    main()
