import json
import re
from pathlib import Path

from comfy_agent.curated_catalog import load_curated_manifest


URL_RX = re.compile(r"https?://[^\s)\]>\"']+")


def _classify_link(url):
    lowered = url.lower()
    if "huggingface.co" in lowered:
        return "huggingface"
    if "civitai.com" in lowered:
        return "civitai"
    if "github.com" in lowered:
        return "github"
    if "docs.comfy.org" in lowered:
        return "comfy_docs"
    if "discord." in lowered:
        return "community"
    return "other"


def _extract_text(widget_values):
    if isinstance(widget_values, str):
        return widget_values
    if isinstance(widget_values, list):
        return " ".join(str(v) for v in widget_values if isinstance(v, (str, int, float, bool)))
    if isinstance(widget_values, dict):
        return " ".join(str(v) for v in widget_values.values())
    return ""


def _extract_from_workflow_json(workflow_path):
    payload = json.loads(Path(workflow_path).read_text(encoding="utf-8"))
    nodes = payload.get("nodes") or []
    grouped = {
        "huggingface": set(),
        "civitai": set(),
        "github": set(),
        "comfy_docs": set(),
        "community": set(),
        "other": set(),
    }

    for node in nodes:
        if not isinstance(node, dict):
            continue
        text = _extract_text(node.get("widgets_values"))
        for url in URL_RX.findall(text):
            provider = _classify_link(url)
            grouped[provider].add(url)

    return {k: sorted(v) for k, v in grouped.items() if v}


def _resolve_workflow_path(skill_id=None, workflow_path=None):
    if workflow_path:
        path = Path(workflow_path)
        if not path.exists():
            raise FileNotFoundError(f"workflow_path does not exist: {workflow_path}")
        return path, None

    if not skill_id:
        raise ValueError("Provide either skill_id or workflow_path")

    manifest = load_curated_manifest()
    for entry in manifest.get("entries", []):
        if entry.get("id") == skill_id:
            destination = entry.get("destination")
            if not destination:
                break
            path = Path(destination) / "workflow.json"
            if path.exists():
                return path, entry
            raise FileNotFoundError(f"workflow.json missing for skill_id={skill_id}")
    raise ValueError(f"Unknown skill_id: {skill_id}")


def run(skill_id=None, workflow_path=None):
    resolved_path, manifest_entry = _resolve_workflow_path(skill_id=skill_id, workflow_path=workflow_path)
    links = _extract_from_workflow_json(resolved_path)
    all_links = sorted({url for values in links.values() for url in values})

    return {
        "status": "ok",
        "skill": "get_workflow_download_links",
        "skill_id": skill_id,
        "workflow_path": str(resolved_path),
        "family": manifest_entry.get("family") if isinstance(manifest_entry, dict) else None,
        "total_links": len(all_links),
        "links_by_provider": links,
        "links": all_links,
    }
