"""Tertiary vault index — metadata only; private resolve map stays local."""

from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

DEFAULT_DENY_PREFIXES = (
    "Ingest/Decisions/",
    ".technical/parallel/",
    ".technical/grok-bridge/",
    ".trash/",
    "4-Archives/",
)

HIGH_SENSITIVITY_PREFIXES = (
    "2-Areas/",
)


def _utc_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _stable_tert_id(vault_ref: str) -> str:
    digest = hashlib.sha256(vault_ref.encode("utf-8")).hexdigest()
    return f"tert_{digest[:12]}"


def _canonical_ref(vault_root: Path, path: Path) -> str:
    return path.resolve().relative_to(vault_root.resolve()).as_posix()


def _role_from_path(rel: str) -> str:
    parts = rel.split("/")
    if len(parts) >= 2:
        return f"{parts[0]} resource"
    return "vault note"


def _sensitivity(rel: str, frontmatter: dict[str, Any]) -> str:
    if frontmatter.get("grok_deny") is True:
        return "high"
    if str(frontmatter.get("sensitivity") or "").lower() == "high":
        return "high"
    for prefix in HIGH_SENSITIVITY_PREFIXES:
        if rel.startswith(prefix):
            return "amber"
    return "low"


def _parse_frontmatter(text: str) -> dict[str, Any]:
    m = re.match(r"^---\n(.*?)\n---\n", text, flags=re.DOTALL)
    if not m:
        return {}
    try:
        import yaml  # type: ignore[import-untyped]

        data = yaml.safe_load(m.group(1))
        return data if isinstance(data, dict) else {}
    except (ValueError, ImportError, Exception):
        return {}


def _denied(rel: str, deny_globs: list[str]) -> bool:
    for prefix in DEFAULT_DENY_PREFIXES:
        if rel.startswith(prefix):
            return True
    for g in deny_globs:
        g = g.replace("\\", "/").strip()
        if g and rel.startswith(g):
            return True
    return False


def _collect_wiki_links(text: str) -> list[str]:
    return re.findall(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]", text)


def _seed_paths(project_root: Path, vault_root: Path, project_id: str) -> set[str]:
    refs: set[str] = set()
    if not project_root.is_dir():
        return refs
    for md in project_root.rglob("*.md"):
        if not md.is_file():
            continue
        try:
            text = md.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for link in _collect_wiki_links(text):
            link = link.strip()
            if link.startswith("Roadmap/") or link.startswith("3-Resources/"):
                refs.add(link.split("#", 1)[0])
    catalog = project_root / "Roadmap/User-Story/slice-catalog.yaml"
    if catalog.is_file():
        try:
            text = catalog.read_text(encoding="utf-8", errors="replace")
            refs.update(_collect_wiki_links(text))
        except OSError:
            pass
    # Project-scoped resources
    res = vault_root / "3-Resources"
    if res.is_dir():
        for p in res.rglob("*.md"):
            if project_id.replace("-", " ") in p.name.lower() or project_id in p.read_text(encoding="utf-8", errors="replace")[:500]:
                try:
                    refs.add(_canonical_ref(vault_root, p))
                except ValueError:
                    pass
    return refs


def build_tertiary_index(
    vault_root: Path,
    project_id: str,
    *,
    deny_globs: list[str] | None = None,
) -> tuple[dict[str, Any], dict[str, str]]:
    vault_root = vault_root.resolve()
    project_root = vault_root / "1-Projects" / project_id
    deny = deny_globs or []
    refs = _seed_paths(project_root, vault_root, project_id)

    entries: list[dict[str, Any]] = []
    resolve_map: dict[str, str] = {}

    for rel in sorted(refs):
        if _denied(rel, deny):
            continue
        path = vault_root / rel
        if not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        fm = _parse_frontmatter(text)
        if fm.get("grok_deny") is True:
            continue
        canonical = _canonical_ref(vault_root, path)
        tid = _stable_tert_id(canonical)
        sens = _sensitivity(rel, fm)
        vault_hash = hashlib.sha256(text.encode("utf-8")).hexdigest()
        kind = "resource"
        if rel.startswith("2-Areas/"):
            kind = "area"
        elif rel.startswith("5-Attachments/"):
            kind = "attachment_meta"
        entries.append(
            {
                "id": tid,
                "kind": kind,
                "role": _role_from_path(rel)[:120],
                "project_id": project_id,
                "sensitivity": sens,
                "edges": [],
                "vault_ref_hash": f"sha256:{vault_hash}",
                "last_indexed_utc": _utc_iso(),
                "fulfill_allowed_default": sens == "low",
            }
        )
        resolve_map[tid] = canonical

    index = {
        "schema_version": 1,
        "project_id": project_id,
        "last_generated_utc": _utc_iso(),
        "entry_count": len(entries),
        "entries": entries,
    }
    fingerprint = hashlib.sha256(json.dumps(index, sort_keys=True).encode("utf-8")).hexdigest()
    index["fingerprint"] = fingerprint
    return index, resolve_map


def write_tertiary_artifacts(
    vault_root: Path,
    project_id: str,
    *,
    deny_globs: list[str] | None = None,
) -> dict[str, Any]:
    index, resolve_map = build_tertiary_index(vault_root, project_id, deny_globs=deny_globs)
    project_root = vault_root / "1-Projects" / project_id
    project_root.mkdir(parents=True, exist_ok=True)

    index_path = project_root / "TERTIARY-INDEX.json"
    index_path.write_text(json.dumps(index, indent=2) + "\n", encoding="utf-8")

    resolve_dir = vault_root / ".technical/grok-bridge" / project_id
    resolve_dir.mkdir(parents=True, exist_ok=True)
    resolve_path = resolve_dir / "tertiary-resolve.json"
    resolve_path.write_text(json.dumps(resolve_map, indent=2) + "\n", encoding="utf-8")

    return {
        "ok": True,
        "index_path": index_path.relative_to(vault_root).as_posix(),
        "resolve_path": resolve_path.relative_to(vault_root).as_posix(),
        "fingerprint": index.get("fingerprint"),
        "entry_count": index.get("entry_count"),
    }
