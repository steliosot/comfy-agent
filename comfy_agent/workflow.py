import copy
import json
import os
import time
import uuid
from urllib import error, request

try:
    import requests
except ImportError:  # pragma: no cover
    class _HTTPError(Exception):
        def __init__(self, message, response=None):
            super().__init__(message)
            self.response = response

    class _Response:
        def __init__(self, payload, status_code=200, text=None):
            self._payload = payload
            self.status_code = status_code
            self.ok = 200 <= status_code < 300
            self.text = text if text is not None else json.dumps(payload)

        def json(self):
            return self._payload

        def raise_for_status(self):
            if not self.ok:
                raise _HTTPError(self.text, response=self)

    class _RequestsCompat:
        HTTPError = _HTTPError

        @staticmethod
        def get(url, headers=None):
            req = request.Request(
                url,
                headers=headers or {},
                method="GET",
            )
            try:
                with request.urlopen(req) as response:
                    payload = json.loads(response.read().decode("utf-8"))
                    return _Response(payload, status_code=response.status)
            except error.HTTPError as exc:
                return _Response({}, status_code=exc.code, text=exc.read().decode("utf-8"))

        @staticmethod
        def post(url, json=None, headers=None):
            data = None if json is None else __import__("json").dumps(json).encode("utf-8")
            merged_headers = {"Content-Type": "application/json"}
            if headers:
                merged_headers.update(headers)
            req = request.Request(
                url,
                data=data,
                headers=merged_headers,
                method="POST",
            )
            try:
                with request.urlopen(req) as response:
                    payload = __import__("json").loads(response.read().decode("utf-8"))
                    return _Response(payload, status_code=response.status)
            except error.HTTPError as exc:
                body = exc.read().decode("utf-8")
                try:
                    payload = __import__("json").loads(body)
                except ValueError:
                    payload = {}
                return _Response(payload, status_code=exc.code, text=body)

    requests = _RequestsCompat()

from .node import Node
from .refs import DataRef, NodeResult


class Workflow:
    """Spark-style lazy DAG builder for ComfyUI"""

    def __init__(self, comfy_url=None, server=None, headers=None, api_prefix=None):
        base_url = server or comfy_url
        if not base_url:
            base_url = os.getenv("COMFY_URL", "http://127.0.0.1:8000")

        self.base_url = base_url.rstrip("/")
        self.headers = dict(headers or {})

        env_api_prefix = os.getenv("COMFY_API_PREFIX")
        if api_prefix is None:
            api_prefix = env_api_prefix

        normalized_prefix = (api_prefix or "").strip()
        if normalized_prefix and not normalized_prefix.startswith("/"):
            normalized_prefix = f"/{normalized_prefix}"
        normalized_prefix = normalized_prefix.rstrip("/")

        candidates = []
        if normalized_prefix:
            candidates.append(f"{self.base_url}{normalized_prefix}")
        candidates.append(self.base_url)
        if not normalized_prefix:
            candidates.append(f"{self.base_url}/api")

        seen = set()
        ordered_candidates = []
        for candidate in candidates:
            if candidate not in seen:
                seen.add(candidate)
                ordered_candidates.append(candidate)

        last_response = None
        self.url = None
        for candidate in ordered_candidates:
            response = requests.get(f"{candidate}/object_info", headers=self.headers)
            last_response = response
            if response.ok:
                self.url = candidate
                self.registry = response.json()
                break

        if self.url is None:
            if last_response is not None:
                last_response.raise_for_status()
            raise RuntimeError("Unable to connect to ComfyUI /object_info endpoint")

        self.nodes = []
        self.next_id = 1
        self._last_checkpoint = None
        self.last_prompt_id = None
        self._reset_pipeline_state()
        print("Loaded nodes:", len(self.registry), "via", self.url)

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
        alias = kwargs.pop("__alias", None)
        kwargs = self._prepare_inputs(class_type, kwargs)

        node_id = str(self.next_id)
        self.next_id += 1

        # store inputs lazily (do not resolve DataRef yet)
        node = Node(node_id, class_type, kwargs, alias=alias)
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
        checkpoint = self._add_node(
            "CheckpointLoaderSimple",
            __alias="checkpoint",
            ckpt_name=ckpt_name,
        )
        self._current_checkpoint = checkpoint
        self._current_model = checkpoint.MODEL
        self._current_clip = checkpoint.CLIP
        self._current_vae = checkpoint.VAE
        return self

    def lora(self, lora_name, strength=1.0):
        if self._current_model is None:
            raise RuntimeError("Call .checkpoint(...) before .lora(...)")

        model = self._add_node(
            "LoraLoaderModelOnly",
            __alias="lora",
            model=self._current_model,
            lora_name=lora_name,
            strength_model=strength,
        )
        self._current_model = model.MODEL
        return self

    def prompt(self, text):
        if self._current_clip is None:
            raise RuntimeError("Call .checkpoint(...) before .prompt(...)")

        conditioning = self._add_node(
            "CLIPTextEncode",
            __alias="prompt",
            clip=self._current_clip,
            text=text,
        )
        self._current_positive = conditioning.CONDITIONING
        return self

    def negative(self, text):
        if self._current_clip is None:
            raise RuntimeError("Call .checkpoint(...) before .negative(...)")

        conditioning = self._add_node(
            "CLIPTextEncode",
            __alias="negative",
            clip=self._current_clip,
            text=text,
        )
        self._current_negative = conditioning.CONDITIONING
        return self

    def latent(self, width, height, batch_size=1):
        latent = self._add_node(
            "EmptyLatentImage",
            __alias="latent",
            width=width,
            height=height,
            batch_size=batch_size,
        )
        self._current_latent = latent.LATENT
        return self

    def load_image(self, image):
        result = self._add_node("LoadImage", __alias="load_image", image=image)
        self._current_image = result.IMAGE
        if hasattr(result, "MASK"):
            self._current_mask = result.MASK
        return self

    def crop(self, x, y, width, height):
        if self._current_image is None:
            raise RuntimeError("Call .load_image(...) before .crop(...)")

        cropped = self._add_node(
            "ImageCrop",
            __alias="crop",
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

        latent = self._add_node(
            "VAEEncode",
            __alias="encode",
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
            negative = self._add_node(
                "CLIPTextEncode",
                __alias="negative",
                clip=self._current_clip,
                text="",
            ).CONDITIONING
            self._current_negative = negative

        sample = self._add_node(
            "KSampler",
            __alias="ksampler",
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

        image = self._add_node(
            "VAEDecode",
            __alias="decode",
            samples=self._current_latent,
            vae=self._current_vae,
        )
        self._current_image = image.IMAGE
        return self

    def preview(self):
        if self._current_image is None:
            raise RuntimeError("Call .decode() before .preview()")

        self._add_node("PreviewImage", __alias="preview", images=self._current_image)
        return self

    def save(self, filename_prefix):
        if self._current_image is None:
            raise RuntimeError("Call .decode() before .save(...)")

        self._add_node(
            "SaveImage",
            __alias="save",
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

        self._add_node(
            "SaveAnimatedWEBP",
            __alias="save_animated_webp",
            images=self._current_image,
            filename_prefix=filename_prefix,
            fps=fps,
            lossless=lossless,
            quality=quality,
            method=method,
        )
        return self

    def clone(self):
        cloned = self.__class__.__new__(self.__class__)
        for key, value in self.__dict__.items():
            setattr(cloned, key, copy.deepcopy(value))
        return cloned

    def override(self, overrides):
        for path, value in overrides.items():
            selector, input_name = path.rsplit(".", 1)
            node = self._find_node(selector)
            if input_name not in node.inputs:
                raise KeyError(f"Node '{selector}' has no input '{input_name}'")
            node.inputs[input_name] = value
        return self

    def inspect(self, print_output=True):
        lines = []
        for index, node in enumerate(self.nodes):
            outputs = self._output_names(node.class_type)
            label = node.alias or self._normalize_node_name(node.class_type)
            if outputs:
                lines.append(
                    f"{index}. {node.class_type} [{label}] -> {', '.join(outputs)}"
                )
            else:
                lines.append(f"{index}. {node.class_type} [{label}]")

        summary = "\n".join(lines)
        if print_output:
            print(summary)
        return summary

    def to_json(self, indent=2):
        return json.dumps(self._build_dag(), indent=indent)

    def then(self, other):
        combined = self.clone()
        mapping = {}

        for node in other.nodes:
            new_id = str(combined.next_id)
            combined.next_id += 1
            mapping[node.node_id] = new_id

            combined.nodes.append(
                Node(
                    new_id,
                    node.class_type,
                    combined._remap_value(copy.deepcopy(node.inputs), mapping),
                    alias=node.alias,
                )
            )

        combined._remap_pipeline_state_from(other, mapping)
        return combined

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

    def _normalize_node_name(self, name):
        normalized = []
        previous_upper = False

        for char in name:
            if char.isupper() and normalized and not previous_upper:
                normalized.append("_")
            normalized.append(char.lower())
            previous_upper = char.isupper()

        return "".join(normalized)

    def _output_names(self, class_type):
        node_info = self.registry.get(class_type, {})
        names = node_info.get("output_name") or node_info.get("output") or []
        return [self._normalize_output_name(name, index) for index, name in enumerate(names)]

    def _find_node(self, selector):
        index = None
        if selector.endswith("]") and "[" in selector:
            selector, raw_index = selector[:-1].split("[", 1)
            index = int(raw_index)

        matches = []
        normalized_selector = selector.lower()

        for node in self.nodes:
            alias = (node.alias or "").lower()
            class_name = self._normalize_node_name(node.class_type)
            candidates = {alias, class_name, node.class_type.lower()}
            if normalized_selector in candidates:
                matches.append(node)
                continue

            if alias and alias.startswith(normalized_selector):
                matches.append(node)
                continue

            if class_name.startswith(normalized_selector):
                matches.append(node)

        if not matches:
            raise KeyError(f"No node matched selector '{selector}'")

        if index is None:
            return matches[-1]

        try:
            return matches[index]
        except IndexError as exc:
            raise IndexError(f"Selector '{selector}' has no match at index {index}") from exc

    def _remap_value(self, value, mapping):
        if isinstance(value, DataRef):
            return DataRef(mapping[value.node_id], value.output_index)
        if isinstance(value, NodeResult):
            refs = tuple(self._remap_value(ref, mapping) for ref in value)
            return NodeResult(refs, value._output_names)
        if isinstance(value, list):
            return [self._remap_value(v, mapping) for v in value]
        if isinstance(value, tuple):
            return tuple(self._remap_value(v, mapping) for v in value)
        if isinstance(value, dict):
            return {k: self._remap_value(v, mapping) for k, v in value.items()}
        return value

    def _remap_pipeline_state_from(self, other, mapping):
        state_fields = [
            "_current_checkpoint",
            "_current_model",
            "_current_clip",
            "_current_vae",
            "_current_positive",
            "_current_negative",
            "_current_latent",
            "_current_image",
            "_current_mask",
            "_last_checkpoint",
        ]

        for field in state_fields:
            value = getattr(other, field)
            setattr(self, field, self._remap_value(copy.deepcopy(value), mapping) if value is not None else None)

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

        r = requests.post(f"{self.url}/prompt", json=payload, headers=self.headers)
        if not r.ok:
            message = f"ComfyUI prompt request failed with {r.status_code}"
            try:
                detail = r.json()
                message += f": {json.dumps(detail, indent=2)}"
            except ValueError:
                message += f": {r.text}"
            raise requests.HTTPError(message, response=r)
        result = r.json()
        self.last_prompt_id = result.get("prompt_id")
        print(result)
        return result

    def history(self, prompt_id=None):
        target = prompt_id or self.last_prompt_id
        if not target:
            raise ValueError("prompt_id is required when no run() has been executed")

        response = requests.get(f"{self.url}/history/{target}", headers=self.headers)
        response.raise_for_status()
        return response.json()

    def saved_images(self, prompt_id=None, retries=12, delay=0.5):
        target = prompt_id or self.last_prompt_id
        if not target:
            raise ValueError("prompt_id is required when no run() has been executed")

        for attempt in range(max(1, retries)):
            history = self.history(target)
            entry = history.get(target, history) if isinstance(history, dict) else history
            outputs = entry.get("outputs", {}) if isinstance(entry, dict) else {}

            images = []
            for node_id, node_output in outputs.items():
                for image in node_output.get("images", []):
                    item = dict(image)
                    item["node_id"] = str(node_id)
                    images.append(item)

            if images:
                return images

            if attempt < retries - 1:
                time.sleep(delay)

        return []
