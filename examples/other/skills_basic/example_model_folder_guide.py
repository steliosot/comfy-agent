import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[3]))

from skills.model_folder_guide.skill import run as model_folder_guide


print(model_folder_guide(model_type="checkpoint"))
print(model_folder_guide(model_type="lora"))
print(model_folder_guide(model_type="diffusion_model"))
