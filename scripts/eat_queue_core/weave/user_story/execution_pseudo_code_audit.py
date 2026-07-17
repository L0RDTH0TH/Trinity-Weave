"""Deterministic pseudo-code gate before loop 3 (Half A)."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .catalog_io import catalog_rows_by_id, load_yaml, user_story_paths
from .product_factory_budget import budget_row_ids

_GAP_MARKERS = re.compile(
    r"(?:\bTODO\b|\bTBD\b|\bGAP\b:|#review-needed|pseudo-code\s*:\s*$)",
    re.I,
)
_PSEUDO_FENCE = re.compile(r"```(?:pseudo|pseudocode)?", re.I)
_PSEUDO_HEADING = re.compile(r"^#+\s*(pseudo[- ]?code|implementation sketch)", re.I | re.M)
_PHASE_DEPTH = re.compile(r"phase[-_]?(\d+)", re.I)


@dataclass(frozen=True)
class PseudoCodeAuditResult:
    ok: bool
    violations: tuple[str, ...]
    gaps: tuple[str, ...]
    pins_checked: int

    def to_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "violations": list(self.violations),
            "gaps": list(self.gaps),
            "pins_checked": self.pins_checked,
        }


def _pin_paths(vault_root: Path, row: dict[str, Any]) -> list[Path]:
    pins = row.get("execution_pins") or []
    out: list[Path] = []
    if not isinstance(pins, list):
        return out
    for pin in pins:
        rel = str(pin).strip()
        if not rel:
            continue
        p = vault_root / rel
        if p.is_file():
            out.append(p)
            continue
        p_md = vault_root / (rel if rel.endswith(".md") else f"{rel}.md")
        if p_md.is_file():
            out.append(p_md)
    return out


def _phase_depth_from_path(path: Path) -> int:
    m = _PHASE_DEPTH.search(str(path).replace(" ", "-"))
    if m:
        return int(m.group(1))
    return 0


def _note_has_pseudo_code(text: str) -> bool:
    if _PSEUDO_FENCE.search(text) or _PSEUDO_HEADING.search(text):
        return True
    lowered = text.lower()
    if "pseudo-code" in lowered and len(text.strip()) > 400:
        return True
    return False


def _note_has_gap_markers(text: str) -> bool:
    return bool(_GAP_MARKERS.search(text))


def audit_pin_note(path: Path) -> tuple[bool, list[str]]:
    text = path.read_text(encoding="utf-8", errors="replace")
    violations: list[str] = []
    depth = _phase_depth_from_path(path)
    has_pseudo = _note_has_pseudo_code(text)
    if depth >= 4 and not has_pseudo:
        violations.append(f"pseudo_code_missing:depth={depth}")
    if len(text.strip()) < 120:
        violations.append("pin_note_too_thin")
    if _note_has_gap_markers(text) and not has_pseudo:
        violations.append("gap_markers_without_pseudo_code")
    return len(violations) == 0, violations


def run_execution_pseudo_code_audit(
    vault_root: Path,
    *,
    project_id: str,
) -> PseudoCodeAuditResult:
    """Pins resolve; depth ≥ 4 notes need pseudo-code; thin gap-only notes fail."""
    vault_root = vault_root.resolve()
    paths = user_story_paths(vault_root, project_id)
    catalog = load_yaml(paths["catalog"])
    rows = catalog_rows_by_id(catalog)
    row_ids = budget_row_ids(vault_root, project_id) or [
        rid for rid, r in rows.items() if r.get("planned")
    ]

    violations: list[str] = []
    gaps: list[str] = []
    pins_checked = 0

    for rid in row_ids:
        row = rows.get(rid) or {}
        pin_paths = _pin_paths(vault_root, row)
        if not pin_paths:
            violations.append(f"no_resolving_pins:{rid}")
            gaps.append(f"execution_pin_missing:{rid}")
            continue
        for pin_path in pin_paths:
            pins_checked += 1
            ok, pin_v = audit_pin_note(pin_path)
            if not ok:
                for v in pin_v:
                    violations.append(f"{rid}:{pin_path.name}:{v}")
                    if "pseudo_code" in v or "gap_markers" in v:
                        gaps.append(f"{rid}:{v}")

    ok = len(violations) == 0
    return PseudoCodeAuditResult(
        ok=ok,
        violations=tuple(violations),
        gaps=tuple(gaps),
        pins_checked=pins_checked,
    )
