"""Phase 10e-b / 13 — meta-lens force-align during regenerate-complete.

When enabled, regen merges locked maintenance-core meta doctrine into Rules/Touch
on each regenerated provisional card. Conceptual leg stays archived (operator-owned
narrative); engine law wins on structural legs.
"""

from __future__ import annotations

from typing import Any

from .trinity_card import get_rules, get_touch
from .trinity_card_paths import load_trinity_card
from .trinity_mvl_lens import get_lens_contract, load_meta_lens_legs, probe_mvl_lens

META_LENS_REGEN_TASK_KIND = "regen_burn"

# Cap injected precedence lines per meta card (deterministic, structural only).
_MAX_PRECEDENCE_PER_META = 4


def validate_meta_lens_regen_prerequisites(vault_root: Any) -> dict[str, Any]:
    """Gate — lens must load before force-align burn."""
    from pathlib import Path

    probe = probe_mvl_lens(Path(vault_root))
    if probe.get("skipped"):
        return {
            "ok": False,
            "reason": "mvl_conductor_disabled",
            "hint": "Enable trinity_mvl_conductor_enabled before meta-lens force-align",
        }
    if not probe.get("ok"):
        return {
            "ok": False,
            "reason": "mvl_lens_probe_failed",
            "missing_meta_cards": probe.get("missing_meta_cards") or [],
            "hint": "Lock all meta_prepend_order cards before --meta-lens-force-align",
        }
    return {"ok": True, "lens_source": probe.get("lens_source"), "probe": probe}


def _dedupe_preserve_order(lines: list[str]) -> list[str]:
    out: list[str] = []
    seen: set[str] = set()
    for raw in lines:
        line = str(raw).strip()
        if not line or line in seen:
            continue
        seen.add(line)
        out.append(line)
    return out


def _lens_precedence_lines(vault_root: Any, meta_ids: list[str]) -> list[str]:
    from pathlib import Path

    root = Path(vault_root).resolve()
    lines: list[str] = [
        "policy: meta_lens_force_align — regen under locked maintenance_core doctrine",
        "policy: maintenance_core meta cards are read-only during regen",
    ]
    for mid in meta_ids:
        try:
            card = load_trinity_card(root, mid, prefer="locked")
        except (OSError, ValueError, FileNotFoundError):
            lines.append(f"policy: lens/{mid} — meta card missing at regen (review required)")
            continue
        prec = get_rules(card).get("precedence") or []
        if not isinstance(prec, list):
            continue
        for row in prec[:_MAX_PRECEDENCE_PER_META]:
            s = str(row).strip()
            if s:
                lines.append(f"policy: lens/{mid} — {s}")
    return lines


def _resolve_card_kind(trinity_id: str) -> str:
    tid = str(trinity_id or "").strip()
    if tid.startswith("harness_"):
        return "harness_entrypoint"
    if tid in ("trinity_spine_maintenance", "trinity_upgrade_integration"):
        return "provisional_bridge"
    return "component"


def apply_meta_lens_force_align(
    vault_root: Any,
    card: dict[str, Any],
    archived_card: dict[str, Any],
    trinity_id: str,
) -> dict[str, Any]:
    """Merge lens doctrine into regenerated card (Rules/Touch/meta; Conceptual preserved)."""
    from pathlib import Path

    root = Path(vault_root).resolve()
    tid = str(trinity_id).strip()
    lens = get_lens_contract(root)
    meta_ids = lens.meta_prepend_for(META_LENS_REGEN_TASK_KIND)

    out = dict(card)
    archived_rules = get_rules(archived_card)
    rules = dict(out.get("rules") or {})

    lens_prec = _lens_precedence_lines(root, meta_ids)
    archived_prec = archived_rules.get("precedence") or []
    if not isinstance(archived_prec, list):
        archived_prec = []
    existing_prec = rules.get("precedence") or []
    if not isinstance(existing_prec, list):
        existing_prec = []

    rules["precedence"] = _dedupe_preserve_order(
        lens_prec + list(existing_prec) + list(archived_prec)
    )

    forbidden = list(rules.get("forbidden") or [])
    arch_forbidden = archived_rules.get("forbidden") or []
    if isinstance(arch_forbidden, list):
        forbidden.extend(str(x).strip() for x in arch_forbidden if str(x).strip())
    forbidden.extend(lens.forbidden)
    forbidden = _dedupe_preserve_order(forbidden)

    arch_touch = get_touch(archived_card)
    touch = dict(out.get("touch") or {})
    if arch_touch.get("primary_paths"):
        touch["primary_paths"] = list(arch_touch["primary_paths"])
    if arch_touch.get("harness_commands"):
        touch["harness_commands"] = list(arch_touch["harness_commands"])
    if arch_touch.get("primary_paths_modes"):
        touch["primary_paths_modes"] = dict(arch_touch["primary_paths_modes"])
    touch["meta_lens_force_align"] = True
    out["touch"] = touch

    from .trinity_align import filter_forbidden_list_for_primary_code

    mint_card = dict(out)
    mint_card["rules"] = dict(rules)
    kept_forbidden, dropped_forbidden = filter_forbidden_list_for_primary_code(
        root, mint_card, forbidden
    )
    if dropped_forbidden:
        prec = list(rules.get("precedence") or [])
        for phrase in dropped_forbidden:
            prec.append(
                f"policy: meta_lens mint — forbidden omitted (present in primary code): {phrase}"
            )
        rules["precedence"] = _dedupe_preserve_order(prec)
    rules["forbidden"] = kept_forbidden
    if dropped_forbidden:
        rules["meta_lens_forbidden_code_filtered"] = dropped_forbidden[:12]
    rules["meta_lens_force_align"] = True
    rules["meta_lens_task_kind"] = META_LENS_REGEN_TASK_KIND

    meta = dict(out.get("meta") or {})
    src = dict(meta.get("source") or {}) if isinstance(meta.get("source"), dict) else {}
    src["meta_lens_force_align"] = True
    src["meta_lens_prepend"] = meta_ids
    src["lens_source"] = lens.source
    src["meta_lens_task_kind"] = META_LENS_REGEN_TASK_KIND
    meta["source"] = src
    meta["card_kind"] = _resolve_card_kind(tid)

    out["conceptual"] = archived_card.get("conceptual") or out.get("conceptual")
    out["rules"] = rules
    out["touch"] = touch
    out["meta"] = meta

    # Attach lightweight meta summaries for downstream conductor (not full card dump).
    out.setdefault("_meta_lens_overlay", load_meta_lens_legs(root, meta_ids, max_ids=8))

    return out


def summarize_force_align_delta(
    before: dict[str, Any],
    after: dict[str, Any],
) -> dict[str, Any]:
    """Dry-run / audit helper — what changed on Rules/Touch."""
    b_rules = get_rules(before)
    a_rules = get_rules(after)
    b_prec = b_rules.get("precedence") or []
    a_prec = a_rules.get("precedence") or []
    if not isinstance(b_prec, list):
        b_prec = []
    if not isinstance(a_prec, list):
        a_prec = []
    b_set = set(str(x) for x in b_prec)
    added_prec = [str(x) for x in a_prec if str(x) not in b_set]
    return {
        "precedence_added_count": len(added_prec),
        "precedence_added_sample": added_prec[:6],
        "forbidden_count": len(a_rules.get("forbidden") or []),
        "card_kind": (after.get("meta") or {}).get("card_kind"),
        "meta_lens_force_align": bool(a_rules.get("meta_lens_force_align")),
    }
