"""Inject tech_level / granularity on product-factory RESUME_ROADMAP (Half A)."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from ..factory.factory_output_gate import parse_factory_orchestrator_yaml

_PHASE_NUM = re.compile(r"phase[-_]?(\d+)", re.I)


def infer_phase_number(linked_phase: str | None) -> int:
    text = str(linked_phase or "").strip()
    if not text:
        return 0
    m = _PHASE_NUM.search(text.replace(" ", "-"))
    if m:
        return int(m.group(1))
    for part in text.split("."):
        part = part.strip()
        if part.isdigit():
            return int(part)
    return 0


def load_tech_progression_config(vault_root: Path) -> dict[str, Any]:
    cfg_path = vault_root / "3-Resources/Second-Brain-Config.md"
    if not cfg_path.is_file():
        return {"roadmap_tech_progression": True, "tech_levels": {}}
    doc = parse_factory_orchestrator_yaml(cfg_path)
    levels = doc.get("tech_levels") if isinstance(doc.get("tech_levels"), dict) else {}
    return {
        "roadmap_tech_progression": doc.get("roadmap_tech_progression", True) is not False,
        "tech_levels": levels,
    }


def resolve_tech_level_params(
    params: dict[str, Any],
    *,
    vault_root: Path | None = None,
    track: str | None = None,
) -> dict[str, Any]:
    """Map phase depth → tech_level + granularity + guidance snippet."""
    out = dict(params)
    cfg: dict[str, Any] = {"roadmap_tech_progression": True, "tech_levels": {}}
    if vault_root is not None:
        cfg = load_tech_progression_config(vault_root)
    if not cfg.get("roadmap_tech_progression"):
        return out

    levels = cfg.get("tech_levels") or {}
    phase_num = infer_phase_number(
        str(out.get("linked_phase") or out.get("phase") or out.get("target_phase") or "")
    )
    roadmap_track = str(track or out.get("roadmap_track") or "execution").lower()

    if phase_num >= 5 or roadmap_track == "execution":
        tech = str(levels.get("level_3") or "pseudo-code")
        guidance = (
            "Structural depth ≥ 4 requires fenced pseudo-code, data shapes, and edge cases "
            "per roadmap-deepen handoff rules."
        )
    elif phase_num >= 3:
        tech = str(levels.get("level_2") or "mid-tech")
        guidance = "Mid-technical depth: interfaces, data flows, tradeoffs — no stubs-only handoff."
    else:
        tech = str(levels.get("level_1") or "high-concept")
        guidance = "High-concept depth: user impacts and architecture nouns — defer pseudo-code."

    if roadmap_track == "conceptual":
        tech = str(levels.get("level_1") or "high-concept")
        guidance = "Conceptual deepen: NL completeness and touchstone alignment — no pseudo-code gate."

    out["tech_level"] = tech
    out.setdefault("granularity", tech)
    existing = str(out.get("user_guidance") or "").strip()
    if guidance and guidance not in existing:
        out["user_guidance"] = (existing + "\n\n" + guidance).strip() if existing else guidance
    return out
