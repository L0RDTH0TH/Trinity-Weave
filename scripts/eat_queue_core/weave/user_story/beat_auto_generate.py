"""Auto-generate beats from depth budget + catalog."""

from __future__ import annotations

import hashlib
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .catalog_io import (
    catalog_rows_by_id,
    load_json,
    load_yaml,
    normalize_pin,
    user_story_paths,
)


def _section_hash(body: str) -> str:
    return hashlib.sha256(body.encode("utf-8")).hexdigest()[:16]


def _operator_edited_marker(body: str) -> bool:
    return "<!-- operator-edited: true -->" in body


def _group_rows_for_beats(
    budget_rows: list[dict[str, Any]],
    catalog_by_id: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    """Group active rollout rows by dimension for beat files."""
    by_dim: dict[str, list[dict[str, Any]]] = {}
    for br in budget_rows:
        row_id = str(br.get("row_id") or "")
        target = int(br.get("target_depth") or 0)
        current = int(br.get("current_depth") or 0)
        if target <= 0 or current >= target:
            continue
        cat = catalog_by_id.get(row_id) or {}
        dim = str(cat.get("dimension") or "general")
        by_dim.setdefault(dim, []).append(
            {
                "row_id": row_id,
                "label": cat.get("label") or row_id,
                "target_depth": target,
                "current_depth": current,
                "execution_pins": cat.get("execution_pins") or [],
            }
        )
    groups: list[dict[str, Any]] = []
    for dim, items in sorted(by_dim.items()):
        groups.append({"dimension": dim, "rows": items})
    return groups


def _beat_body(
    *,
    rollout_version: int,
    dimension: str,
    rows: list[dict[str, Any]],
    charter_excerpt: str,
) -> str:
    lines = [
        "---",
        f"beat_id: beat-r{rollout_version}-{dimension}",
        f"rollout_version: {rollout_version}",
        f"dimension: {dimension}",
        "auto_generated: true",
        f"generated_at: {datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')}",
        "row_ids:",
    ]
    for r in rows:
        lines.append(f"  - {r['row_id']}")
    lines.extend(["---", "", f"# Beat — rollout {rollout_version} / {dimension}", ""])
    if charter_excerpt:
        lines.extend(["## Depth context", charter_excerpt[:600], ""])
    lines.append("## Rows")
    for r in rows:
        pins = ", ".join(str(normalize_pin(p)) for p in r.get("execution_pins") or [])
        lines.append(
            f"- **{r['label']}** (`{r['row_id']}`) — target depth {r['target_depth']}; pins: {pins or 'TBD'}"
        )
    lines.append("")
    lines.append("## Experiential narrative")
    lines.append("(Auto-generated scaffold — deepen via USER_STORY_DEEPEN.)")
    lines.append("")
    return "\n".join(lines)


def run_beat_auto_generate(
    vault_root: Path,
    *,
    project_id: str,
) -> dict[str, Any]:
    vault_root = vault_root.resolve()
    paths = user_story_paths(vault_root, project_id)
    budget = load_json(paths["budget"])
    catalog = load_yaml(paths["catalog"])
    catalog_by_id = catalog_rows_by_id(catalog)
    budget_rows = budget.get("rows") or []
    if not isinstance(budget_rows, list):
        budget_rows = []

    rv = int(budget.get("rollout_version") or 1)
    charter_text = ""
    if paths["depth_charter"].is_file():
        charter_text = paths["depth_charter"].read_text(encoding="utf-8", errors="replace")

    groups = _group_rows_for_beats(budget_rows, catalog_by_id)
    paths["beats_dir"].mkdir(parents=True, exist_ok=True)

    written: list[str] = []
    skipped: list[str] = []
    for g in groups:
        dim = str(g["dimension"])
        safe_dim = re.sub(r"[^a-zA-Z0-9_]+", "-", dim).strip("-") or "general"
        beat_name = f"beat-r{rv}-{safe_dim}.md"
        beat_path = paths["beats_dir"] / beat_name
        new_body = _beat_body(
            rollout_version=rv,
            dimension=dim,
            rows=g["rows"],
            charter_excerpt=charter_text,
        )
        if beat_path.is_file():
            old = beat_path.read_text(encoding="utf-8")
            if _operator_edited_marker(old):
                skipped.append(beat_name)
                continue
            old_hash = _section_hash(old)
            new_hash = _section_hash(new_body)
            if old_hash == new_hash:
                skipped.append(beat_name)
                continue
        beat_path.write_text(new_body, encoding="utf-8")
        written.append(beat_name)

    return {
        "ok": True,
        "written": written,
        "skipped_operator_or_unchanged": skipped,
        "beats_dir": str(paths["beats_dir"].relative_to(vault_root)),
    }
