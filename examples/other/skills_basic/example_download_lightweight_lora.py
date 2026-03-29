import os
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[3]))

from skills.download_model.skill import run as download_model

# Optional:
# export COMFY_URL=http://34.30.216.121
# export COMFY_AUTH_HEADER=XXXXXX
# export HF_TOKEN=XXXXXX
# export CIVITAI_API_KEY=XXXXXX

server = os.getenv("COMFY_URL", "http://127.0.0.1:8000")
auth = os.getenv("COMFY_AUTH_HEADER", "")
headers = {"Authorization": auth} if auth else None

result = download_model(
    source="civitai",
    model_id_or_url="https://civitai.com/api/download/models/12345",
    filename="example_light_lora.safetensors",
    model_type="lora",
    server=server,
    headers=headers,
)

print(result)
