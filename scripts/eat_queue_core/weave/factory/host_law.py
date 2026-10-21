"""host-law.yaml evaluator — data rows only; harness does not recognize product cites.

Entry shape: {id, cite, refuse_code, applies_when}.
Absent file → not applicable (empty list). No YouTube / dual-grid special cases in Python.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .bindings import BindingMissingError, load_family, require_project_id


def load_host_law_entries(vault_root: Path, project_id: str) -> list[dict[str, Any]]:
    """Return host-law entries or [] when file absent (not applicable)."""
    pid = require_project_id(project_id)
    try:
        data = load_family(vault_root, pid, "host-law")
    except BindingMissingError:
        return []
    raw = data.get("entries")
    if not isinstance(raw, list):
        return []
    out: list[dict[str, Any]] = []
    for item in raw:
        if isinstance(item, dict) and str(item.get("id") or "").strip():
            out.append(item)
    return out


def matching_refuse_codes(
    vault_root: Path,
    project_id: str,
    *,
    context: dict[str, Any] | None = None,
) -> list[str]:
    """Return refuse_code values whose applies_when is satisfied by context."""
    ctx = context or {}
    codes: list[str] = []
    for entry in load_host_law_entries(vault_root, project_id):
        when = entry.get("applies_when")
        if when is None:
            codes.append(str(entry.get("refuse_code") or entry.get("id") or ""))
            continue
        if not isinstance(when, dict):
            continue
        if all(ctx.get(k) == v for k, v in when.items()):
            code = str(entry.get("refuse_code") or entry.get("id") or "").strip()
            if code:
                codes.append(code)
    return codes
