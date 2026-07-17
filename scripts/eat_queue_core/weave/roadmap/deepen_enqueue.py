"""Merge Config sticky params into RESUME_ROADMAP deepen queue lines (factory + standalone)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .branch_depth import load_deepen_traversal_config
from .roadmap_path_resolver import attach_deepen_path_hint, load_path_resolver_config


def sticky_deepen_params(vault_root: Path, *, track: str) -> dict[str, Any]:
    """Config → queue params; no cursor / split logic."""
    cfg = load_deepen_traversal_config(vault_root)
    path_cfg = load_path_resolver_config(vault_root)
    out: dict[str, Any] = {}
    traversal = str(cfg.get("deepen_traversal") or "").lower()
    if traversal == "depth_first":
        out["deepen_traversal"] = "depth_first"
    if cfg.get("child_before_sibling_exit") is True:
        out["child_before_sibling_exit"] = True
    if track:
        out["roadmap_track"] = track
    if path_cfg.get("path_resolver_enforced"):
        out["roadmap_path_resolver_enforced"] = True
    return out


def merge_deepen_params(
    vault_root: Path,
    params: dict[str, Any],
    *,
    track: str,
) -> dict[str, Any]:
    """Operator/queue params win over Config sticky defaults."""
    merged = dict(sticky_deepen_params(vault_root, track=track))
    merged.update(params)
    if str(track).lower() == "conceptual":
        pid = str(merged.get("project_id") or "").strip()
        if pid and not merged.get("harness_gate_authority"):
            from ..user_story.conceptual_dispatch_authority import (
                build_conceptual_dispatch_verdict,
                stamp_harness_gate_params,
            )

            verdict = build_conceptual_dispatch_verdict(vault_root, pid)
            if verdict.deepen_required:
                merged = stamp_harness_gate_params(merged, verdict)
    return attach_deepen_path_hint(vault_root, merged)
