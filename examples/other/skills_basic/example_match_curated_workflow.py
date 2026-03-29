import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[3]))

from skills.infra.match_curated_workflow.skill import run


result = run(
    prompt="cinematic product video ad for running shoes",
    top_k=3,
)
print(result)
