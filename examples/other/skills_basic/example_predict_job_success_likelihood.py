import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[3]))

from skills.predict_job_success_likelihood.skill import run


result = run(skill_id="curated_ltx_0_95_text2video")
print(result)
