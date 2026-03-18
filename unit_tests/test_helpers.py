from contextlib import contextmanager
from unittest.mock import patch


FAKE_REGISTRY = {
    "CheckpointLoaderSimple": {
        "output": ["MODEL", "CLIP", "VAE"],
        "output_name": ["MODEL", "CLIP", "VAE"],
    },
    "CLIPTextEncode": {
        "output": ["CONDITIONING"],
        "output_name": ["CONDITIONING"],
    },
    "EmptyLatentImage": {
        "output": ["LATENT"],
        "output_name": ["LATENT"],
    },
    "KSampler": {
        "output": ["LATENT"],
        "output_name": ["LATENT"],
    },
    "VAEDecode": {
        "output": ["IMAGE"],
        "output_name": ["IMAGE"],
    },
    "SaveImage": {"output": [], "output_name": []},
    "PreviewImage": {"output": [], "output_name": []},
    "LoadImage": {
        "output": ["IMAGE", "MASK"],
        "output_name": ["IMAGE", "MASK"],
    },
    "ImageCrop": {
        "output": ["IMAGE"],
        "output_name": ["IMAGE"],
    },
    "VAEEncode": {
        "output": ["LATENT"],
        "output_name": ["LATENT"],
    },
    "LoraLoaderModelOnly": {
        "output": ["MODEL"],
        "output_name": ["MODEL"],
    },
    "SaveAnimatedWEBP": {"output": [], "output_name": []},
}


class FakeResponse:
    def __init__(self, payload, ok=True, status_code=200, text=""):
        self._payload = payload
        self.ok = ok
        self.status_code = status_code
        self.text = text

    def json(self):
        return self._payload

    def raise_for_status(self):
        if not self.ok:
            raise RuntimeError(f"HTTP {self.status_code}: {self.text}")


@contextmanager
def mocked_comfy_api():
    posted = []

    def fake_get(url, *args, **kwargs):
        return FakeResponse(FAKE_REGISTRY)

    def fake_post(url, json=None, *args, **kwargs):
        posted.append({"url": url, "json": json})
        return FakeResponse({"prompt_id": "test-prompt"})

    with patch("comfy_agent.workflow.requests.get", side_effect=fake_get), patch(
        "comfy_agent.workflow.requests.post", side_effect=fake_post
    ):
        yield posted
