#!/usr/bin/env python3
"""CLI wrapper for skills.workflows.video_t2v_i2v_avatar.curated_wan_2_2_i2i_14b_gguf_4_step_lora_upscale.skill.run"""

import argparse
import json
import sys
from pathlib import Path


THIS = Path(__file__).resolve()
REPO_ROOT = THIS.parents[4]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from skills.workflows.video_t2v_i2v_avatar.curated_wan_2_2_i2i_14b_gguf_4_step_lora_upscale.skill import run


def main():
    parser = argparse.ArgumentParser(description="Run curated workflow skill: curated_wan_2_2_i2i_14b_gguf_4_step_lora_upscale")
    parser.add_argument("--args", default="{}", help="JSON object with kwargs for run(...)")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output")
    args = parser.parse_args()

    try:
        kwargs = json.loads(args.args)
    except json.JSONDecodeError as exc:
        print(f"Invalid --args JSON: {exc}", file=sys.stderr)
        sys.exit(2)

    if not isinstance(kwargs, dict):
        print("--args must decode to a JSON object", file=sys.stderr)
        sys.exit(2)

    result = run(**kwargs)
    if args.pretty:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(json.dumps(result))


if __name__ == "__main__":
    main()
