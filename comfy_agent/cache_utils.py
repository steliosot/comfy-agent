import hashlib
import json

from .refs import DataRef, NodeResult


def _tensor_like_summary(value):
    shape = getattr(value, "shape", None)
    dtype = getattr(value, "dtype", None)
    device = getattr(value, "device", None)

    if shape is None and dtype is None and device is None:
        return None

    return {
        "__kind__": "tensor_like",
        "type": f"{type(value).__module__}.{type(value).__name__}",
        "shape": tuple(shape) if shape is not None else None,
        "dtype": str(dtype) if dtype is not None else None,
        "device": str(device) if device is not None else None,
    }


def _normalize_scalar(value):
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float, str)) or value is None:
        return value
    return None


def _summarize_large_mapping(value):
    keys = sorted(str(k) for k in value.keys())
    return {
        "__kind__": "large_mapping",
        "type": f"{type(value).__module__}.{type(value).__name__}",
        "size": len(value),
        "keys": keys[:64],
    }


def _summarize_large_sequence(value):
    sample = value[:16] if isinstance(value, list) else list(value)[:16]
    return {
        "__kind__": "large_sequence",
        "type": f"{type(value).__module__}.{type(value).__name__}",
        "size": len(value),
        "sample": [_normalize_value(v, depth=0) for v in sample],
    }


def _normalize_value(value, depth=0):
    if depth > 12:
        return {
            "__kind__": "max_depth",
            "type": f"{type(value).__module__}.{type(value).__name__}",
        }

    scalar = _normalize_scalar(value)
    if scalar is not None or value is None:
        return scalar

    if isinstance(value, DataRef):
        return {"__kind__": "data_ref", "node_id": str(value.node_id), "output_index": int(value.output_index)}

    if isinstance(value, NodeResult):
        return {"__kind__": "node_result", "refs": [_normalize_value(ref, depth + 1) for ref in value]}

    tensor_summary = _tensor_like_summary(value)
    if tensor_summary is not None:
        return tensor_summary

    if isinstance(value, dict):
        if len(value) > 128:
            return _summarize_large_mapping(value)
        items = []
        for key in sorted(value.keys(), key=lambda x: str(x)):
            items.append([str(key), _normalize_value(value[key], depth + 1)])
        return {"__kind__": "dict", "items": items}

    if isinstance(value, (list, tuple)):
        if len(value) > 512:
            return _summarize_large_sequence(list(value))
        return {
            "__kind__": "list" if isinstance(value, list) else "tuple",
            "items": [_normalize_value(v, depth + 1) for v in value],
        }

    return {
        "__kind__": "object",
        "type": f"{type(value).__module__}.{type(value).__name__}",
        "repr": repr(value)[:256],
    }


def hash_value(value):
    normalized = _normalize_value(value)
    payload = json.dumps(normalized, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def hash_node(class_type, inputs, upstream_signatures):
    normalized_inputs = _normalize_value(inputs)
    normalized_upstream = _normalize_value(upstream_signatures)
    payload = {
        "class_type": str(class_type),
        "inputs": normalized_inputs,
        "upstream_signatures": normalized_upstream,
    }
    return hash_value(payload)
