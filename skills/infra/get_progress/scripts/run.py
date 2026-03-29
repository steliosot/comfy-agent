#!/usr/bin/env python3
"""CLI wrapper for skills.infra.get_progress.skill.run"""

import argparse
import json
import sys
from pathlib import Path

THIS = Path(__file__).resolve()
REPO_ROOT = THIS.parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from skills.infra.get_progress.skill import run


def main():
    parser = argparse.ArgumentParser(description="Run get_progress skill")
    parser.add_argument("--args", default="{}", help="JSON object with kwargs passed to run(...)")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON result")
    args = parser.parse_args()

    kwargs = json.loads(args.args)
    if not isinstance(kwargs, dict):
        raise SystemExit("--args must decode to a JSON object")
    result = run(**kwargs)
    print(json.dumps(result, indent=2 if args.pretty else None, sort_keys=args.pretty))


if __name__ == "__main__":
    main()
