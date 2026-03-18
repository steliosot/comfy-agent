import json
import os
import requests
import uuid

from .node import Node
from .refs import DataRef, NodeResult


class Workflow:
    """Spark-style lazy DAG builder for ComfyUI"""

    def __init__(self, comfy_url=None, server=None):
        base_url = server or comfy_url
        if not base_url:
            base_url = os.getenv("COMFY_URL", "http://127.0.0.1:8000")

        self.url = base_url.rstrip("/")
        r = requests.get(f"{self.url}/object_info")
        r.raise_for_status()
        self.registry = r.json()
        self.nodes = []
        self.next_id = 1
        self._last_checkpoint = None
        self._reset_pipeline_state()
        print("Loaded nodes:", len(self.registry))

    def _resolve(self, value):
        if isinstance(value, DataRef):
            # Comfy API link format
            return [str(value.node_id), int(value.output_index)]

        if isinstance(value, NodeResult):
            return self._resolve(value.primary())

        if isinstance(value, list):
            return [self._resolve(v) for v in value]

        if isinstance(value, tuple):
            return [self._resolve(v) for v in value]

        if isinstance(value, dict):
            return {k: self._resolve(v) for k, v in value.items()}

        return value

    def _add_node(self, class_type, **kwargs):
        kwargs = self._prepare_inputs(class_type, kwargs)

        node_id = str(self.next_id)
        self.next_id += 1

        # store inputs lazily (do not resolve DataRef yet)
        node = Node(node_id, class_type, kwargs)
        self.nodes.append(node)

        # inspect outputs from Comfy registry
        node_info = self.registry.get(class_type, {})
        outputs = node_info.get("output", [])
        output_names = node_info.get("output_name", outputs)

        # create DataRef objects for each output
        refs = tuple(DataRef(node_id, i) for i in range(len(outputs)))
        normalized_names = tuple(
            self._normalize_output_name(name, i) for i, name in enumerate(output_names)
        )

        if len(refs) == 0:
            return None

        result = NodeResult(refs, normalized_names)

        if class_type == "CheckpointLoaderSimple":
            self._last_checkpoint = result

        return result

    def _prepare_inputs(self, class_type, kwargs):
        prepared = dict(kwargs)

        if class_type == "CLIPTextEncode":
            if "clip" not in prepared and self._last_checkpoint is not None:
                prepared["clip"] = self._last_checkpoint.CLIP

        if class_type in {"VAEEncode", "VAEDecode"}:
            if "vae" not in prepared and self._last_checkpoint is not None:
                prepared["vae"] = self._last_checkpoint.VAE

        if class_type == "KSampler":
            if "model" not in prepared and self._last_checkpoint is not None:
                prepared["model"] = self._last_checkpoint.MODEL

            if "negative" not in prepared and self._last_checkpoint is not None:
                negative = self._add_node(
                    "CLIPTextEncode",
                    clip=self._last_checkpoint.CLIP,
                    text=""
                )
                prepared["negative"] = negative.CONDITIONING

            prepared.setdefault("seed", 1)
            prepared.setdefault("steps", 20)
            prepared.setdefault("cfg", 7.0)
            prepared.setdefault("sampler_name", "euler")
            prepared.setdefault("scheduler", "normal")
            prepared.setdefault("denoise", 1.0)

        return prepared

    def _reset_pipeline_state(self):
        self._current_checkpoint = None
        self._current_model = None
        self._current_clip = None
        self._current_vae = None
        self._current_positive = None
        self._current_negative = None
        self._current_latent = None
        self._current_image = None
        self._current_mask = None

    def checkpoint(self, ckpt_name):
        checkpoint = self.CheckpointLoaderSimple(ckpt_name=ckpt_name)
        self._current_checkpoint = checkpoint
        self._current_model = checkpoint.MODEL
        self._current_clip = checkpoint.CLIP
        self._current_vae = checkpoint.VAE
        return self

    def lora(self, lora_name, strength=1.0):
        if self._current_model is None:
            raise RuntimeError("Call .checkpoint(...) before .lora(...)")

        model = self.LoraLoaderModelOnly(
            model=self._current_model,
            lora_name=lora_name,
            strength_model=strength,
        )
        self._current_model = model.MODEL
        return self

    def prompt(self, text):
        if self._current_clip is None:
            raise RuntimeError("Call .checkpoint(...) before .prompt(...)")

        conditioning = self.CLIPTextEncode(
            clip=self._current_clip,
            text=text,
        )
        self._current_positive = conditioning.CONDITIONING
        return self

    def negative(self, text):
        if self._current_clip is None:
            raise RuntimeError("Call .checkpoint(...) before .negative(...)")

        conditioning = self.CLIPTextEncode(
            clip=self._current_clip,
            text=text,
        )
        self._current_negative = conditioning.CONDITIONING
        return self

    def latent(self, width, height, batch_size=1):
        latent = self.EmptyLatentImage(
            width=width,
            height=height,
            batch_size=batch_size,
        )
        self._current_latent = latent.LATENT
        return self

    def load_image(self, image):
        result = self.LoadImage(image=image)
        self._current_image = result.IMAGE
        if hasattr(result, "MASK"):
            self._current_mask = result.MASK
        return self

    def crop(self, x, y, width, height):
        if self._current_image is None:
            raise RuntimeError("Call .load_image(...) before .crop(...)")

        cropped = self.ImageCrop(
            image=self._current_image,
            x=x,
            y=y,
            width=width,
            height=height,
        )
        self._current_image = cropped.IMAGE
        return self

    def encode(self):
        if self._current_image is None:
            raise RuntimeError("Call .load_image(...) before .encode()")
        if self._current_vae is None:
            raise RuntimeError("Call .checkpoint(...) before .encode()")

        latent = self.VAEEncode(
            pixels=self._current_image,
            vae=self._current_vae,
        )
        self._current_latent = latent.LATENT
        return self

    def sample(
        self,
        seed=1,
        steps=20,
        cfg=7.0,
        sampler_name="euler",
        scheduler="normal",
        denoise=1.0,
    ):
        if self._current_model is None:
            raise RuntimeError("Call .checkpoint(...) before .sample()")
        if self._current_positive is None:
            raise RuntimeError("Call .prompt(...) before .sample()")
        if self._current_latent is None:
            raise RuntimeError("Call .latent(...) or .encode() before .sample()")

        negative = self._current_negative
        if negative is None:
            negative = self.CLIPTextEncode(
                clip=self._current_clip,
                text="",
            ).CONDITIONING
            self._current_negative = negative

        sample = self.KSampler(
            model=self._current_model,
            positive=self._current_positive,
            negative=negative,
            latent_image=self._current_latent,
            seed=seed,
            steps=steps,
            cfg=cfg,
            sampler_name=sampler_name,
            scheduler=scheduler,
            denoise=denoise,
        )
        self._current_latent = sample.LATENT
        return self

    def decode(self):
        if self._current_latent is None:
            raise RuntimeError("Call .sample(...) or .encode() before .decode()")
        if self._current_vae is None:
            raise RuntimeError("Call .checkpoint(...) before .decode()")

        image = self.VAEDecode(
            samples=self._current_latent,
            vae=self._current_vae,
        )
        self._current_image = image.IMAGE
        return self

    def preview(self):
        if self._current_image is None:
            raise RuntimeError("Call .decode() before .preview()")

        self.PreviewImage(images=self._current_image)
        return self

    def save(self, filename_prefix):
        if self._current_image is None:
            raise RuntimeError("Call .decode() before .save(...)")

        self.SaveImage(
            images=self._current_image,
            filename_prefix=filename_prefix,
        )
        return self

    def save_animated_webp(
        self,
        filename_prefix,
        fps=6,
        lossless=False,
        quality=80,
        method="default",
    ):
        if self._current_image is None:
            raise RuntimeError("Call .decode() before .save_animated_webp(...)")

        self.SaveAnimatedWEBP(
            images=self._current_image,
            filename_prefix=filename_prefix,
            fps=fps,
            lossless=lossless,
            quality=quality,
            method=method,
        )
        return self

    def _normalize_output_name(self, name, index):
        if not name:
            return f"OUTPUT_{index}"

        normalized = []
        previous_was_separator = False

        for char in str(name):
            if char.isalnum():
                normalized.append(char.upper())
                previous_was_separator = False
            elif not previous_was_separator:
                normalized.append("_")
                previous_was_separator = True

        result = "".join(normalized).strip("_")
        if not result:
            result = f"OUTPUT_{index}"
        if result[0].isdigit():
            result = f"OUTPUT_{result}"
        return result

    def __getattr__(self, name):
        for node_name in self.registry:
            if node_name.lower() == name.lower():
                def wrapper(**kwargs):
                    return self._add_node(node_name, **kwargs)
                return wrapper
        raise AttributeError(name)

    def node(self, name, **kwargs):
        return self._add_node(name, **kwargs)

    def _build_dag(self):
        dag = {}
        for node in self.nodes:
            dag[node.node_id] = {
                "class_type": node.class_type,
                "inputs": {k: self._resolve(v) for k, v in node.inputs.items()},
            }
        return dag

    def validate(self):
        if not self.nodes:
            raise RuntimeError("Workflow is empty")

        produced = set()

        for node in self.nodes:
            for value in node.inputs.values():
                self._validate_refs(value, produced)
            produced.add(node.node_id)

        print("Workflow validation passed")

    def _validate_refs(self, value, produced):
        if isinstance(value, DataRef):
            if value.node_id not in produced:
                raise RuntimeError(
                    f"Invalid reference: node {value.node_id} not defined before use"
                )
            return

        if isinstance(value, NodeResult):
            self._validate_refs(value.primary(), produced)
            return

        if isinstance(value, (list, tuple)):
            for v in value:
                self._validate_refs(v, produced)
            return

        if isinstance(value, dict):
            for v in value.values():
                self._validate_refs(v, produced)

    def run(self, debug=False):
        self.validate()
        dag = self._build_dag()

        payload = {
            "prompt": dag,
            "client_id": str(uuid.uuid4())
        }

        if debug:
            print(json.dumps(payload, indent=2))

        r = requests.post(f"{self.url}/prompt", json=payload)
        if not r.ok:
            message = f"ComfyUI prompt request failed with {r.status_code}"
            try:
                detail = r.json()
                message += f": {json.dumps(detail, indent=2)}"
            except ValueError:
                message += f": {r.text}"
            raise requests.HTTPError(message, response=r)
        print(r.json())
