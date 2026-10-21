"""host-law.yaml evaluator — opt-in only via Prefer host_law_ids list.

Empty host_law_ids → no cites, no refuses. Flags like prefer_authorship do not opt in.
Absent file → not applicable (empty). Harness does not recognize product video ids.
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


def host_law_ids_from_job_or_armed(
    job: dict[str, Any] | None = None,
    armed: dict[str, Any] | None = None,
) -> list[str]:
    """Explicit Prefer opt-in list only."""
    for blob in (job, armed):
        if not isinstance(blob, dict):
            continue
        raw = blob.get("host_law_ids")
        if isinstance(raw, list):
            return [str(x).strip() for x in raw if str(x).strip()]
    return []


def matching_refuse_codes(
    vault_root: Path,
    project_id: str,
    *,
    context: dict[str, Any] | None = None,
) -> list[str]:
    """Refuse codes for entries whose id is in context host_law_ids.

    Empty or missing host_law_ids → []. Prefer flags are ignored.
    """
    ctx = context or {}
    wanted_raw = ctx.get("host_law_ids")
    if not isinstance(wanted_raw, list) or not wanted_raw:
        return []
    wanted = {str(x).strip() for x in wanted_raw if str(x).strip()}
    if not wanted:
        return []

    codes: list[str] = []
    for entry in load_host_law_entries(vault_root, project_id):
        eid = str(entry.get("id") or "").strip()
        rcode = str(entry.get("refuse_code") or eid).strip()
        if eid in wanted or rcode in wanted:
            if rcode:
                codes.append(rcode)
    return codes


def matching_cites(
    vault_root: Path,
    project_id: str,
    *,
    host_law_ids: list[str] | None = None,
) -> list[str]:
    """Cite strings for opted-in host_law ids only."""
    wanted = {str(x).strip() for x in (host_law_ids or []) if str(x).strip()}
    if not wanted:
        return []
    cites: list[str] = []
    for entry in load_host_law_entries(vault_root, project_id):
        eid = str(entry.get("id") or "").strip()
        rcode = str(entry.get("refuse_code") or "").strip()
        if eid not in wanted and rcode not in wanted:
            continue
        cite = str(entry.get("cite") or "").strip()
        if cite:
            cites.append(cite)
    return cites
