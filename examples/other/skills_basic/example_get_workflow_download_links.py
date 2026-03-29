import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[3]))

from skills.get_workflow_download_links.skill import run


print(run(skill_id="curated_ltx_0_95_text2video"))
