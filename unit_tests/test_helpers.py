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
    "UNETLoader": {"output": ["MODEL"], "output_name": ["MODEL"]},
    "CLIPLoader": {"output": ["CLIP"], "output_name": ["CLIP"]},
    "VAELoader": {"output": ["VAE"], "output_name": ["VAE"]},
    "EmptyFlux2LatentImage": {"output": ["LATENT"], "output_name": ["LATENT"]},
    "ReferenceLatent": {"output": ["CONDITIONING"], "output_name": ["CONDITIONING"]},
    "ConditioningZeroOut": {"output": ["CONDITIONING"], "output_name": ["CONDITIONING"]},
    "ImageScaleToTotalPixels": {"output": ["IMAGE"], "output_name": ["IMAGE"]},
}


class FakeResponse:
    def __init__(self, payload, ok=True, status_code=200, text="", content=None):
        self._payload = payload
        self.ok = ok
        self.status_code = status_code
        self.text = text
        self.content = content if content is not None else str(payload).encode("utf-8")

    def json(self):
        return self._payload

    def raise_for_status(self):
        if not self.ok:
            raise RuntimeError(f"HTTP {self.status_code}: {self.text}")


@contextmanager
def mocked_comfy_api():
    posted = []

    def fake_get(url, *args, **kwargs):
        params = kwargs.get("params") or {}
        if url.endswith("/object_info"):
            return FakeResponse(FAKE_REGISTRY)
        if "/history/" in url:
            prompt_id = url.rsplit("/", 1)[-1]
            return FakeResponse(
                {
                    prompt_id: {
                        "outputs": {
                            "7": {
                                "images": [
                                    {
                                        "filename": "ComfyUI_00001_.png",
                                        "subfolder": "",
                                        "type": "output",
                                    }
                                ]
                            }
                        }
                    }
                }
            )
        if url.endswith("/view"):
            filename = params.get("filename", "image.png")
            return FakeResponse(
                {},
                content=f"fake-bytes:{filename}".encode("utf-8")
            )
        return FakeResponse(FAKE_REGISTRY)

    def fake_post(url, json=None, *args, **kwargs):
        posted.append({
            "url": url,
            "json": json,
            "files": kwargs.get("files"),
            "data": kwargs.get("data"),
        })
        if url.endswith("/upload/image"):
            image_tuple = (kwargs.get("files") or {}).get("image")
            if image_tuple:
                filename = image_tuple[0]
            else:
                filename = "uploaded.png"
            return FakeResponse(
                {"name": filename, "subfolder": "", "type": "input"}
            )
        return FakeResponse({"prompt_id": "test-prompt"})

    with patch("comfy_agent.workflow.requests.get", side_effect=fake_get), patch(
        "comfy_agent.workflow.requests.post", side_effect=fake_post
    ):
        yield posted
