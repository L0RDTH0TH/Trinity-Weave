"""Tier C mediated fulfill — fail-closed gate; resolve map stays vault-local."""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .grok_bridge_config import load_grok_bridge, project_branch_name, project_dir
from .live_config import load_live_config
from .project_bridge_sync import verify_trinity_remote
from .weave.project_tertiary_index import DEFAULT_DENY_PREFIXES

AUDIT_REL = Path("3-Resources/Second-Brain/Docs/grok-fulfill-audit.md")
PACK_DIR_REL = Path(".technical/grok-bridge/fulfill-packs")

NEED_VALUES = frozenset({"summary", "excerpt", "full"})


@dataclass
class FulfillBrokerResult:
    status: str  # completed | rejected | failed
    exit_code: int
    payload: dict[str, Any]


def _utc_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _parse_request(raw: str | dict[str, Any]) -> dict[str, Any]:
    if isinstance(raw, dict):
        return raw
    text = raw.strip()
    if text.startswith("{"):
        data = json.loads(text)
        return data if isinstance(data, dict) else {}
    try:
        import yaml  # type: ignore[import-untyped]

        data = yaml.safe_load(text)
        return data if isinstance(data, dict) else {}
    except (ValueError, ImportError, json.JSONDecodeError):
        return {}


def _load_resolve_map(vault_root: Path, project_id: str) -> dict[str, str]:
    path = vault_root / ".technical/grok-bridge" / project_id / "tertiary-resolve.json"
    if not path.is_file():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except (OSError, json.JSONDecodeError):
        return {}


def _load_tertiary_index(project_root: Path) -> dict[str, Any]:
    path = project_root / "TERTIARY-INDEX.json"
    if not path.is_file():
        return {"entries": []}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {"entries": []}
    except (OSError, json.JSONDecodeError):
        return {"entries": []}


def _entry_by_id(index: dict[str, Any], node_id: str) -> dict[str, Any] | None:
    for entry in index.get("entries") or []:
        if isinstance(entry, dict) and entry.get("id") == node_id:
            return entry
    return None


def _catalog_row_path(project_root: Path, row_id: str) -> Path | None:
    catalog = project_root / "Roadmap/User-Story/slice-catalog.yaml"
    if not catalog.is_file():
        return None
    try:
        import yaml  # type: ignore[import-untyped]

        data = yaml.safe_load(catalog.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            return None
        rows = data.get("rows") or data.get("catalog") or []
        if not isinstance(rows, list):
            return None
        for row in rows:
            if not isinstance(row, dict):
                continue
            rid = str(row.get("id") or row.get("row_id") or "")
            if rid == row_id:
                scope = project_root / "Roadmap/User-Story/scopes" / row_id / "L5.md"
                if scope.is_file():
                    return scope
                return catalog
    except (OSError, ValueError, ImportError):
        return None
    return None


def _resolve_node(
    node_id: str,
    *,
    vault_root: Path,
    project_root: Path,
    resolve_map: dict[str, str],
    index: dict[str, Any],
) -> tuple[str | None, str | None]:
    if node_id.startswith("catalog:"):
        row_id = node_id.split(":", 1)[1]
        path = _catalog_row_path(project_root, row_id)
        if path is None:
            return None, f"catalog row not found: {row_id}"
        rel = path.resolve().relative_to(vault_root.resolve()).as_posix()
        return rel, None

    if node_id.startswith("tert_"):
        rel = resolve_map.get(node_id)
        if not rel:
            return None, f"unknown tertiary id: {node_id}"
        entry = _entry_by_id(index, node_id)
        if entry and not entry.get("fulfill_allowed_default", True):
            return None, f"tertiary id denied by sensitivity: {node_id}"
        return rel, None

    return None, f"unsupported node id format: {node_id}"


def _denied_path(rel: str, deny_globs: list[str]) -> bool:
    for prefix in DEFAULT_DENY_PREFIXES:
        if rel.startswith(prefix):
            return True
    for g in deny_globs:
        g = g.replace("\\", "/").strip()
        if g and rel.startswith(g):
            return True
    return False


def _extract_body(path: Path, need: str, max_chars: int) -> str:
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""
    if need == "summary":
        lines = [ln.strip() for ln in text.splitlines() if ln.strip() and not ln.startswith("#")]
        body = " ".join(lines[:12])
    elif need == "excerpt":
        body = text[: max_chars * 2]
    else:
        body = text
    if len(body) > max_chars:
        body = body[: max_chars - 3].rstrip() + "..."
    return body


def validate_fulfill_request(
    request: dict[str, Any],
    *,
    cfg: dict[str, Any],
    operator_ack: bool,
) -> tuple[bool, list[str]]:
    errors: list[str] = []
    if not operator_ack:
        errors.append("operator_ack_required")
    if not request.get("request_id"):
        errors.append("missing request_id")
    if not request.get("project_id"):
        errors.append("missing project_id")
    if not request.get("purpose"):
        errors.append("missing purpose")
    node_ids = request.get("node_ids")
    if not isinstance(node_ids, list) or not node_ids:
        errors.append("node_ids must be non-empty list")
    elif len(node_ids) > int(cfg.get("max_nodes_per_fulfill") or 5):
        errors.append("too_many_nodes")
    need = str(request.get("need") or "summary")
    if need not in NEED_VALUES:
        errors.append(f"invalid need: {need}")
    max_chars = int(request.get("max_chars") or cfg.get("max_chars_per_node") or 2000)
    if max_chars > int(cfg.get("max_chars_per_node") or 2000):
        errors.append("max_chars exceeds cap")
    pid = str(request.get("project_id") or "")
    expected = str(cfg.get("pilot_project_id") or "")
    if pid and expected and pid != expected:
        errors.append(f"project_id not in pilot scope: {pid}")
    return len(errors) == 0, errors


def build_fulfill_pack(
    vault_root: Path,
    request: dict[str, Any],
    *,
    cfg: dict[str, Any],
    operator_ack: bool = False,
) -> dict[str, Any]:
    vault_root = vault_root.resolve()
    ok, errors = validate_fulfill_request(request, cfg=cfg, operator_ack=operator_ack)
    if not ok:
        return {"ok": False, "errors": errors}

    project_id = str(request["project_id"])
    project_root = project_dir(vault_root, project_id)
    resolve_map = _load_resolve_map(vault_root, project_id)
    index = _load_tertiary_index(project_root)
    deny_globs = list(cfg.get("deny_globs") or [])
    need = str(request.get("need") or "summary")
    max_chars = int(request.get("max_chars") or cfg.get("max_chars_per_node") or 2000)

    export_root = Path(cfg["export_repo_root"])
    remote_ok, remote_actual = verify_trinity_remote(export_root, cfg["remote_url"]) if export_root.is_dir() else (False, "")

    nodes: list[dict[str, Any]] = []
    for node_id in request.get("node_ids") or []:
        node_id = str(node_id)
        rel, err = _resolve_node(
            node_id,
            vault_root=vault_root,
            project_root=project_root,
            resolve_map=resolve_map,
            index=index,
        )
        if err or not rel:
            return {"ok": False, "errors": [err or "resolve_failed"], "node_id": node_id}
        if _denied_path(rel, deny_globs):
            return {"ok": False, "errors": ["denied_path"], "path": rel}

        path = vault_root / rel
        if not path.is_file():
            return {"ok": False, "errors": ["missing_vault_file"], "path": rel}

        body = _extract_body(path, need, max_chars)
        content_hash = hashlib.sha256(body.encode("utf-8")).hexdigest()
        nodes.append(
            {
                "node_id": node_id,
                "vault_ref": rel,
                "need": need,
                "char_count": len(body),
                "content_hash": f"sha256:{content_hash}",
                "body": body,
            }
        )

    pack = {
        "schema_version": 1,
        "request_id": str(request["request_id"]),
        "project_id": project_id,
        "purpose": str(request["purpose"]),
        "generated_utc": _utc_iso(),
        "operator_ack": operator_ack,
        "bridge": {
            "trinity_repo": "L0RDTH0TH/Trinity-Weave",
            "remote_url": cfg["remote_url"],
            "remote_verified": remote_ok,
            "remote_actual": remote_actual,
            "main_branch": cfg.get("main_branch") or "main",
            "project_branch": project_branch_name(cfg, project_id),
        },
        "nodes": nodes,
        "pack_fingerprint": "",
    }
    pack["pack_fingerprint"] = hashlib.sha256(
        json.dumps({k: v for k, v in pack.items() if k != "pack_fingerprint"}, sort_keys=True).encode("utf-8")
    ).hexdigest()
    return {"ok": True, "pack": pack}


def _append_audit(vault_root: Path, line: str) -> None:
    path = vault_root / AUDIT_REL
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.is_file():
        path.write_text("# Grok fulfill audit\n\n", encoding="utf-8")
    with path.open("a", encoding="utf-8") as fh:
        fh.write(line + "\n")


def run_grok_fulfill_broker(
    vault_root: Path,
    config_path: Path,
    *,
    request_raw: str | dict[str, Any],
    operator_ack: bool = False,
    write_pack: bool = True,
) -> FulfillBrokerResult:
    vault_root = vault_root.resolve()
    cfg = load_grok_bridge(vault_root, config_path)

    if not cfg.get("enabled", True):
        return FulfillBrokerResult("skipped", 0, {"reason": "grok_bridge_disabled"})

    try:
        request = _parse_request(request_raw)
        inner = request.get("grok_fulfill_request")
        if isinstance(inner, dict):
            request = inner
    except Exception as exc:  # noqa: BLE001
        return FulfillBrokerResult("failed", 1, {"error": "parse_failed", "detail": str(exc)})

    result = build_fulfill_pack(vault_root, request, cfg=cfg, operator_ack=operator_ack)
    if not result.get("ok"):
        _append_audit(
            vault_root,
            f"- {_utc_iso()} | **rejected** | request_id={request.get('request_id', '?')} | errors={result.get('errors')}",
        )
        return FulfillBrokerResult("rejected", 1, result)

    pack = result["pack"]
    pack_path = None
    if write_pack:
        pack_dir = vault_root / PACK_DIR_REL
        pack_dir.mkdir(parents=True, exist_ok=True)
        safe_id = re.sub(r"[^a-zA-Z0-9_-]", "_", str(pack["request_id"]))[:80]
        pack_path = pack_dir / f"{safe_id}.json"
        pack_path.write_text(json.dumps(pack, indent=2) + "\n", encoding="utf-8")

    _append_audit(
        vault_root,
        f"- {_utc_iso()} | **completed** | request_id={pack['request_id']} | fingerprint={pack['pack_fingerprint'][:16]}… | nodes={len(pack['nodes'])}",
    )

    payload = {"pack": pack, "pack_path": pack_path.relative_to(vault_root).as_posix() if pack_path else None}
    return FulfillBrokerResult("completed", 0, payload)
