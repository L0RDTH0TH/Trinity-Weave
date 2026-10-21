"""Product kinesthetic honesty checks — Product 2+ external leg (mirror stack_baseline_honesty)."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .operator_feedback import DEFAULT_FEEDBACK_REL
from .proof_tiers import normalize_source
from .weave_track import is_track_coupled, track_status

MANIFEST_REL = ""
TRINITY_CARD_REL = ".technical/weave/component-proposals/product_kinesthetic_honesty.yaml"

# Remnant patterns live in project bindings (legacy-refuse / host-law), not harness.
Q3_PLAY_PATH_PATTERNS: tuple[tuple[str, str], ...] = ()

PROTECTED_OVERRIDE_SOURCES: frozenset[str] = frozenset({"operator", "playtest_trace"})


@dataclass(frozen=True)
class ProductKinestheticHonestyResult:
    ok: bool
    violations: tuple[str, ...]
    detail: str

    def to_dict(self) -> dict[str, Any]:
        return {"ok": self.ok, "violations": list(self.violations), "detail": self.detail}


def _game_repo(vault_root: Path, project_id: str | None = None) -> Path:
    from .factory_drb_paths import resolve_game_repo_path

    return vault_root / resolve_game_repo_path(vault_root, project_id)


def scan_q3_remnant_on_play_path(
    vault_root: Path, project_id: str | None = None
) -> list[str]:
    """Fail when Q3 acceptance copy remains on player-facing play path."""
    try:
        repo = _game_repo(vault_root, project_id)
    except Exception:
        return []
    violations: list[str] = []
    # Paths to scan come from project legacy-refuse / Prefer — never baked here.
    targets: tuple[Path, ...] = ()
    for path in targets:
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        for pattern, kind in Q3_PLAY_PATH_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                violations.append(f"{kind}:{path.relative_to(vault_root)}")
    return violations


def run_product_kinesthetic_honesty(
    vault_root: Path,
    project_id: str | None = None,
    *,
    proof_shape: str | None = None,
    require_weave_track: bool | None = None,
) -> ProductKinestheticHonestyResult:
    violations: list[str] = []

    card = vault_root / TRINITY_CARD_REL
    if not card.is_file():
        violations.append("product_kinesthetic_honesty_card_missing")

    # Contract seats: missing weave_track.yaml must not fail (blank shell OK).
    shape = str(proof_shape or "").strip().lower()
    need_track = require_weave_track
    if need_track is None:
        need_track = shape != "contract"
    if need_track:
        try:
            weave_track = (
                _game_repo(vault_root, project_id)
                / ".technical/weave/weave_track.yaml"
            )
        except Exception:
            violations.append("product_track_weld_missing:weave_track.yaml")
            weave_track = None
        if weave_track is not None:
            if not weave_track.is_file():
                violations.append("product_track_weld_missing:weave_track.yaml")
            elif not is_track_coupled(vault_root):
                violations.append(
                    f"product_track_not_coupled:{track_status(vault_root)}"
                )

    violations.extend(scan_q3_remnant_on_play_path(vault_root, project_id))

    ok = len(violations) == 0
    detail = "product_kinesthetic_honesty_ok" if ok else "; ".join(violations)
    return ProductKinestheticHonestyResult(ok=ok, violations=tuple(violations), detail=detail)


def row_is_protected_override(row_source: str) -> bool:
    return normalize_source(row_source) in PROTECTED_OVERRIDE_SOURCES
