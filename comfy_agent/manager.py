import json
from urllib import error, request
from urllib.parse import urlparse

try:
    import requests
except ImportError:  # pragma: no cover
    class _Response:
        def __init__(self, status_code=200, text="", payload=None):
            self.status_code = status_code
            self.text = text
            self._payload = payload
            self.ok = 200 <= status_code < 300

        def json(self):
            if self._payload is not None:
                return self._payload
            return json.loads(self.text)

    class _RequestsCompat:
        @staticmethod
        def request(method, url, headers=None, timeout=30, json=None):
            body = None
            req_headers = dict(headers or {})
            if json is not None:
                body = __import__("json").dumps(json).encode("utf-8")
                req_headers["Content-Type"] = "application/json"
            req = request.Request(
                url=url,
                data=body,
                headers=req_headers,
                method=method.upper(),
            )
            try:
                with request.urlopen(req, timeout=timeout) as resp:
                    text = resp.read().decode("utf-8")
                    return _Response(status_code=resp.status, text=text)
            except error.HTTPError as exc:
                text = exc.read().decode("utf-8")
                return _Response(status_code=exc.code, text=text)
            except Exception as exc:
                return _Response(status_code=599, text=str(exc))

    requests = _RequestsCompat()


def _normalize_base_url(base_url):
    text = str(base_url).strip()
    if "://" in text:
        parsed = urlparse(text)
        if parsed.scheme:
            return text.rstrip("/")
    return f"http://{text}".rstrip("/")


def _normalize_prefix(prefix, default=""):
    value = (prefix or default or "").strip()
    if value and not value.startswith("/"):
        value = f"/{value}"
    return value.rstrip("/")


def _candidate_base_roots(server, api_prefix=None):
    base = _normalize_base_url(server)
    normalized_api = _normalize_prefix(api_prefix, default="")

    roots = []
    if normalized_api:
        roots.append(f"{base}{normalized_api}")
    roots.append(base)
    if not normalized_api:
        roots.append(f"{base}/api")

    seen = set()
    unique = []
    for item in roots:
        if item not in seen:
            seen.add(item)
            unique.append(item)
    return unique


def manager_roots(server, api_prefix=None, manager_api_prefix="/manager"):
    manager_prefix = _normalize_prefix(manager_api_prefix, default="/manager")
    return [f"{root}{manager_prefix}" for root in _candidate_base_roots(server, api_prefix=api_prefix)]


def _request_json(method, url, headers=None, payload=None, timeout=30):
    kwargs = {"headers": headers or {}, "timeout": timeout}
    if payload is not None:
        kwargs["json"] = payload
    try:
        response = requests.request(method=method.upper(), url=url, **kwargs)
    except Exception as exc:  # pragma: no cover - defensive for unexpected transports
        return {
            "ok": False,
            "status_code": 599,
            "url": url,
            "json": None,
            "text": str(exc),
        }
    ok = response.ok
    text = response.text
    parsed = None
    try:
        parsed = response.json()
    except ValueError:
        parsed = None
    return {
        "ok": ok,
        "status_code": response.status_code,
        "url": url,
        "json": parsed,
        "text": text,
    }


def manager_probe(server, headers=None, api_prefix=None, manager_api_prefix="/manager"):
    """
    Probe manager roots and infer what install operations appear supported.
    """
    roots = manager_roots(server, api_prefix=api_prefix, manager_api_prefix=manager_api_prefix)
    probes = ["/status", "/health", "/version", ""]

    reachable = None
    probe_attempts = []
    for root in roots:
        for suffix in probes:
            url = f"{root}{suffix}"
            result = _request_json("GET", url, headers=headers)
            probe_attempts.append(result)
            if result["ok"]:
                reachable = {"root": root, "probe_url": url, "probe_result": result}
                break
        if reachable:
            break

    if not reachable:
        message = "ComfyUI-Manager API not reachable. Check COMFY_MANAGER_API_PREFIX or install ComfyUI-Manager."
        return {
            "ok": False,
            "manager_available": False,
            "root": None,
            "probe_url": None,
            "supported_operations": {
                "model_install": [],
                "custom_node_install": [],
            },
            "attempts": probe_attempts,
            "error": message,
        }

    # Endpoint candidates (operation aliases across manager builds/custom integrations).
    supported = {
        "model_install": [
            "/model/install",
            "/models/install",
            "/install_model",
        ],
        "model_remove": [
            "/model/remove",
            "/models/remove",
            "/uninstall_model",
            "/model/uninstall",
        ],
        "custom_node_install": [
            "/custom_nodes/install",
            "/node/install",
            "/install_custom_node",
        ],
    }

    return {
        "ok": True,
        "manager_available": True,
        "root": reachable["root"],
        "probe_url": reachable["probe_url"],
        "supported_operations": supported,
        "attempts": probe_attempts,
        "error": None,
    }


def manager_install(
    operation,
    payload,
    server,
    headers=None,
    api_prefix=None,
    manager_api_prefix="/manager",
):
    """
    Attempt install operation through ComfyUI-Manager API.
    Returns actionable diagnostics even when unavailable.
    """
    probe = manager_probe(
        server=server,
        headers=headers,
        api_prefix=api_prefix,
        manager_api_prefix=manager_api_prefix,
    )
    if not probe["ok"]:
        return {
            "ok": False,
            "operation": operation,
            "manager_available": False,
            "error": probe["error"],
            "probe": probe,
            "attempts": [],
        }

    endpoints = probe["supported_operations"].get(operation, [])
    attempts = []
    for endpoint in endpoints:
        url = f"{probe['root']}{endpoint}"
        result = _request_json("POST", url, headers=headers, payload=payload)
        attempts.append(result)
        if result["ok"]:
            return {
                "ok": True,
                "operation": operation,
                "manager_available": True,
                "endpoint": endpoint,
                "url": url,
                "response_json": result["json"],
                "response_text": result["text"],
                "probe": probe,
                "attempts": attempts,
            }

    error = (
        f"Manager reachable at {probe['root']} but install operation '{operation}' failed "
        "for all known endpoints."
    )
    return {
        "ok": False,
        "operation": operation,
        "manager_available": True,
        "endpoint": None,
        "url": None,
        "response_json": None,
        "response_text": None,
        "probe": probe,
        "attempts": attempts,
        "error": error,
    }


def pretty_attempts(result):
    """
    Helper for concise logging/testing diagnostics.
    """
    attempts = result.get("attempts", [])
    compact = []
    for item in attempts:
        compact.append(
            {
                "url": item.get("url"),
                "status_code": item.get("status_code"),
                "ok": item.get("ok"),
                "body": item.get("json") if item.get("json") is not None else item.get("text"),
            }
        )
    return json.dumps(compact, indent=2)
