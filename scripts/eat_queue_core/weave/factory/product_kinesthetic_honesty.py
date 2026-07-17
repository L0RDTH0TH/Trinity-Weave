"""Product kinesthetic honesty checks — Product 2+ external leg (mirror stack_baseline_honesty)."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .operator_feedback import DEFAULT_FEEDBACK_REL
from .proof_tiers import normalize_source
from .weave_track import is_track_coupled, track_status

MANIFEST_REL = "1-Projects/godot-genesis-mythos-master/Factory-DRB/Tech-Stack-Manifest-v1.yaml"
DEFAULT_GAME_REPO_REL = "5-Attachments/Code-Repos/genesis-mythos-demo"
TRINITY_CARD_REL = ".technical/weave/component-proposals/product_kinesthetic_honesty.yaml"

Q3_PLAY_PATH_PATTERNS: tuple[tuple[str, str], ...] = (
    (r"Horizon-Q3\s+demo", "q3_acceptance_remnant_on_main"),
    (r"Horizon-Q3\s+graybox", "q3_acceptance_remnant_on_main"),
)

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


def scan_q3_remnant_on_play_path(vault_root: Path) -> list[str]:
    """Fail when Q3 acceptance copy remains on player-facing play path."""
    repo = _game_repo(vault_root)
    violations: list[str] = []
    targets = (
        repo / "UI/GameHud.cs",
        repo / "PlayRegion.cs",
        repo / "LaunchShell.cs",
    )
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
) -> ProductKinestheticHonestyResult:
    violations: list[str] = []

    card = vault_root / TRINITY_CARD_REL
    if not card.is_file():
        violations.append("product_kinesthetic_honesty_card_missing")

    weave_track = _game_repo(vault_root) / ".technical/weave/weave_track.yaml"
    if not weave_track.is_file():
        violations.append("product_track_weld_missing:weave_track.yaml")
    elif not is_track_coupled(vault_root):
        violations.append(f"product_track_not_coupled:{track_status(vault_root)}")

    violations.extend(scan_q3_remnant_on_play_path(vault_root))

    ok = len(violations) == 0
    detail = "product_kinesthetic_honesty_ok" if ok else "; ".join(violations)
    return ProductKinestheticHonestyResult(ok=ok, violations=tuple(violations), detail=detail)


def row_is_protected_override(row_source: str) -> bool:
    return normalize_source(row_source) in PROTECTED_OVERRIDE_SOURCES
