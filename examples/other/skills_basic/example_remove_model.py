import os
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[3]))

from skills.infra.remove_model.skill import run as remove_model

# Optional:
# export COMFY_URL=http://34.30.216.121
# export COMFY_AUTH_HEADER=XXXXXX

server = os.getenv("COMFY_URL", "http://127.0.0.1:8000")
auth = os.getenv("COMFY_AUTH_HEADER", "")
headers = {"Authorization": auth} if auth else None

result = remove_model(
    filename="example_light_lora.safetensors",
    model_type="lora",
    server=server,
    headers=headers,
)

print(result)
