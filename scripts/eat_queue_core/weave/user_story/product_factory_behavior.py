"""Harness behavior_signals for product-factory Trinity gates (Half B)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ...models import QueueEntry
from .product_factory_ux_context import (
    is_product_factory_execution_resume,
    merge_ux_context_into_params,
    validate_ux_context,
)


def behavior_signals_for_entry(entry: QueueEntry, vault_root: Path) -> list[str]:
    """Signals prove envelope / enrichment for Trinity maintenance checks."""
    vault_root = vault_root.resolve()
    params = dict(entry.params) if isinstance(entry.params, dict) else {}
    mode = (entry.mode or "").upper().replace("-", "_")
    signals: list[str] = []

    if mode == "RESUME_ROADMAP" and is_product_factory_execution_resume(params):
        merged = merge_ux_context_into_params(
            vault_root,
            project_id=str(params.get("project_id") or entry.project_id or ""),
            params=params,
        )
        if validate_ux_context(merged).ok:
            signals.append("ux_context_envelope_present")
        if merged.get("research_context"):
            signals.append("research_context_attached")
        if merged.get("tech_level"):
            signals.append("tech_level_injected")
        if isinstance(merged.get("persona_handoff"), dict):
            signals.append("persona_handoff_present")

    if mode == "PRODUCT_FACTORY_CONTINUE":
        action = str(params.get("action") or "tick").lower().replace("-", "_")
        if action == "eat_factory_lanes":
            signals.append("factory_eat_handoff_ack")
        else:
            signals.append("product_factory_continue_scheduled")

    return signals


def behavior_signal_report(entries: list[QueueEntry], vault_root: Path) -> dict[str, Any]:
    out: dict[str, list[str]] = {}
    for e in entries:
        sigs = behavior_signals_for_entry(e, vault_root)
        if sigs:
            out[str(e.id)] = sigs
    return {"ok": True, "signals_by_entry": out}
