"""Trinity card batch generator — discovery, provenance, proposals (Wave 3).

Reads inventory, concept map, existing cards, harness commands, rules, and skills.
Emits drafts under `.technical/weave/proposals/<stamp>/` — never sets operator lock stamps.
"""

from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Literal

from .trinity_card import SCHEMA_VERSION, contract_proof_paths, normalize_card
from .trinity_card_paths import components_dir, load_trinity_card
from .trinity_touch_refresh import concept_map_path, propose_behavior_signals

CardClass = Literal["complete_draft", "incomplete", "orphan"]
Pile = Literal["green", "incomplete", "orphan"]
LegState = Literal["missing", "draft", "confirmed", "present", "stale", "orphan"]

INVENTORY_REL = Path("3-Resources/Second-Brain/Docs/Weave-Component-Inventory.md")
META_CARD_ID = "trinity_card_authoring"
SCHEMA_CARD = "_schema"

# Prefer stable trinity_id slugs for known inventory components.
INVENTORY_TRINITY_ALIASES: dict[str, str] = {
    "l5 sandbox (h2)": "l5_sandbox",
    "l4 adaptive policy": "l4_adaptive_policy",
    "little val structural check": "little_val_structural",
    "ghost audit machinery": "ghost_skill_audit",
    "recoverable handlers": "recoverable_handlers",
    "l3 self-healing policy": "l3_self_heal",
    "lane status board renderer": "lane_status_board",
    "lane activity reconciler": "lane_activity",
    "launch registry reconcile": "launch_registry_reconcile",
    "l2 symbolic conflict gate": "l2_symbolic_conflict",
    "l2 predictive maintenance": "l2_predictive_maintenance",
    "invariant registry (k3)": "invariant_registry",
    "operator surface verifier": "operator_surface_verifier",
    "weave governance metrics": "weave_governance",
}

# Weave modules that are Trinity meta/tooling — skip module scan (not weave components).
WEAVE_MODULE_SKIP = frozenset(
    {
        "__init__",
        "trinity_card",
        "trinity_card_generate",
        "trinity_align",
        "trinity_touch_refresh",
        "trinity_pack",
        "trinity_behavior_proof",
        "trinity_validation_drill",
    }
)

# Top-level eat_queue_core modules that are glue/tests — skip wide core scan.
CORE_MODULE_SKIP = frozenset(
    {
        "__init__",
        "harness",
        "plan",
        "full_cycle",
        "merged_config",
        "config_loader",
        "live_config",
        "lanes",
    }
)

MODULE_TRINITY_ALIASES: dict[str, str] = {
    "adaptive_policy": "l4_adaptive_policy",
    "l3_self_heal": "l3_self_heal",
    "symbolic_conflict": "l2_symbolic_conflict",
    "predictive": "l2_predictive_maintenance",
}

# Production cards with both lock stamps — skipped unless include_locked.
LOCKED_SKIP_IDS = frozenset(
    {
        "lane_status_board",
        "lane_activity",
        "launch_registry_reconcile",
        "recoverable_handlers",
        "l3_self_heal",
        "harness_headless_eat",
        "harness_rewrite_consumed",
        "harness_append_entries",
        "harness_pseudo_clock_tick",
        "harness_post_queue_memory_pass",
        "harness_headless_architect",
        "harness_post_queue_gitforge",
        "harness_snapshot",
        "harness_verify",
        "harness_lane_recovery_retry",
        "invariant_registry",
        "l2_symbolic_conflict",
        "l2_predictive_maintenance",
        "weave_governance",
        "operator_surface_verifier",
        "little_val_structural",
        "l4_adaptive_policy",
        "ghost_skill_audit",
        "skill_gap",
    }
)

_HARNESS_CMD_RE = re.compile(r'sub\.add_parser\(\s*["\']([\w_]+)["\']')
_INVENTORY_ROW_RE = re.compile(
    r"^\|\s*(?P<component>[^|]+)\|\s*`(?P<path>[^`]+)`\s*\|\s*(?P<trinity>[^|]*)\|\s*(?P<decision>[^|]+)\|",
    re.MULTILINE,
)
_MAINTENANCE_MODE_RE = re.compile(
    r"\b(GOVERNANCE_REVIEW|OPERATOR_SURFACE_REPAIR|REFRESH_LANE_BOARD|REPAIR_PLAYBOOK|GHOST_SKILL_AUDIT|MAINTENANCE_\w+)\b"
)
_SKILL_DIR = Path(".cursor/skills")


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _default_stamp_dir(wide_net: bool) -> str:
    """Human-readable proposals folder name, e.g. 2026-05-31-wide-net."""
    date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    mode = "wide-net" if wide_net else "narrow-net"
    return f"{date}-{mode}"


def _resolve_proposals_dir(vault_root: Path, stamp: str | None, *, wide_net: bool) -> tuple[str, Path]:
    """Pick stamp string and output path; suffix -2, -3, … if same-day folder exists."""
    base = (stamp or _default_stamp_dir(wide_net)).strip()
    root = proposals_root(vault_root)
    candidate = base
    n = 2
    while (root / candidate).exists():
        candidate = f"{base}-{n}"
        n += 1
    return candidate, root / candidate


def _load_yaml(path: Path) -> dict[str, Any]:
    import yaml  # type: ignore[import-untyped]

    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def _dump_yaml(data: dict[str, Any]) -> str:
    import yaml  # type: ignore[import-untyped]

    return yaml.safe_dump(data, sort_keys=False, allow_unicode=True)


def proposals_root(vault_root: Path) -> Path:
    return vault_root / ".technical" / "weave" / "proposals"


@dataclass
class InventoryRow:
    component: str
    path: str
    trinity_id: str | None
    decision: str
    note: str = ""


@dataclass
class DiscoveryAnchor:
    path: str
    role: str


@dataclass
class LegStatus:
    conceptual: LegState
    touch: LegState
    rules: LegState
    contract: LegState


@dataclass
class ProposalRecord:
    trinity_id: str
    card_class: CardClass
    pile: Pile
    source_kind: str
    leg_status: LegStatus
    anchors: list[DiscoveryAnchor] = field(default_factory=list)
    operator_question: str | None = None
    output_path: str = ""


def parse_inventory_table(vault_root: Path) -> list[InventoryRow]:
    inv_path = vault_root / INVENTORY_REL
    if not inv_path.is_file():
        return []
    text = inv_path.read_text(encoding="utf-8", errors="replace")
    rows: list[InventoryRow] = []
    for m in _INVENTORY_ROW_RE.finditer(text):
        comp = m.group("component").strip()
        if comp.lower() == "component":
            continue
        path = m.group("path").strip()
        tri_raw = m.group("trinity").strip()
        trinity_id: str | None = None
        if tri_raw and tri_raw not in ("—", "-", ""):
            trinity_id = tri_raw.strip("`").strip()
        decision = m.group("decision").strip().strip("`")
        rows.append(InventoryRow(component=comp, path=path, trinity_id=trinity_id, decision=decision))
    return rows


def build_provisional_bridge_stub(
    trinity_id: str,
    *,
    tunnel_via: str,
    pairs_with: list[str] | None = None,
    outcome: str | None = None,
) -> dict[str, Any]:
    """Phase 6 — provisional bridge card with tunnel_via / pairs_with (no core writes)."""
    from .trinity_spine_guard import normalize_provisional_bridge_card

    tv = str(tunnel_via or "").strip()
    pw = [str(x).strip() for x in (pairs_with or [tv]) if str(x).strip()]
    card: dict[str, Any] = {
        "id": str(trinity_id).strip(),
        "meta": {
            "anatomy": "bridge",
            "provisional": True,
            "promotion_tier": "provisional",
            "card_class": "provisional_bridge",
            "schema_version": SCHEMA_VERSION,
        },
        "touch": {
            "bridge_scope": True,
            "tunnel_via": tv,
            "pairs_with": pw,
            "primary_paths": [],
        },
        "conceptual": {
            "outcome": outcome
            or f"Bridge harness changes toward core via {tv} without editing core YAML",
            "summary": "Provisional bridge stub (Phase 6)",
        },
        "rules": {
            "forbidden": [
                "Do not mutate maintenance core component YAML from this bridge card",
            ],
            "precedence": [],
            "acceptance": [],
        },
    }
    return normalize_provisional_bridge_card(card)


def slug_trinity_id(component: str, path: str) -> str:
    key = component.strip().lower()
    if key in INVENTORY_TRINITY_ALIASES:
        return INVENTORY_TRINITY_ALIASES[key]
    base = key
    base = re.sub(r"[^a-z0-9]+", "_", base).strip("_")
    if base:
        return base[:64]
    stem = Path(path).stem.lower()
    return re.sub(r"[^a-z0-9]+", "_", stem).strip("_") or "unnamed_component"


def list_harness_commands(vault_root: Path) -> list[str]:
    harness = vault_root / "scripts/eat_queue_core/harness.py"
    if not harness.is_file():
        return []
    text = harness.read_text(encoding="utf-8", errors="replace")
    cmds = sorted(set(_HARNESS_CMD_RE.findall(text)))
    return [c for c in cmds if not c.startswith("_")]


def list_existing_card_ids(vault_root: Path) -> set[str]:
    base = components_dir(vault_root)
    if not base.is_dir():
        return set()
    out: set[str] = set()
    for p in base.glob("*.yaml"):
        if p.name.startswith("_"):
            continue
        out.add(p.stem)
    return out


def _path_exists(vault_root: Path, rel: str) -> bool:
    s = str(rel).strip()
    if not s:
        return False
    p = vault_root / s
    if p.exists():
        return True
    if "*" in s:
        parent = s.rsplit("*", 1)[0].rstrip("/")
        return (vault_root / parent).is_dir()
    return False


def _guess_test_proof(vault_root: Path, primary_path: str) -> list[str]:
    rel = primary_path.strip()
    proofs = [rel] if _path_exists(vault_root, rel) else []
    stem = Path(rel).stem
    if stem.endswith(".py"):
        mod = rel.replace("/", ".").removesuffix(".py")
        candidates = [
            f"scripts/eat_queue_core/tests/test_{stem}.py",
            f"scripts/eat_queue_core/tests/test_weave_{stem.replace('l3_', '').replace('l4_', '').replace('l5_', '')}.py",
        ]
        if "weave/" in rel:
            short = Path(rel).name
            candidates.append(f"scripts/eat_queue_core/tests/test_weave_{short.replace('.py', '')}.py")
        for c in candidates:
            if _path_exists(vault_root, c) and c not in proofs:
                proofs.append(c)
    return proofs


def _is_locked(card: dict[str, Any]) -> bool:
    meta = card.get("meta") if isinstance(card.get("meta"), dict) else {}
    return bool(meta.get("conceptual_confirmed_at") and meta.get("rules_confirmed_at"))


def assess_leg_status(vault_root: Path, card: dict[str, Any]) -> LegStatus:
    meta = card.get("meta") if isinstance(card.get("meta"), dict) else {}
    conceptual = card.get("conceptual") if isinstance(card.get("conceptual"), dict) else {}
    touch = card.get("touch") if isinstance(card.get("touch"), dict) else {}
    rules = card.get("rules") if isinstance(card.get("rules"), dict) else {}
    contract = card.get("contract") if isinstance(card.get("contract"), dict) else {}

    if meta.get("conceptual_confirmed_at"):
        c_state: LegState = "confirmed"
    elif conceptual.get("outcome") or conceptual.get("summary"):
        c_state = "draft"
    else:
        c_state = "missing"

    primary = touch.get("primary_paths") if isinstance(touch.get("primary_paths"), list) else []
    if not primary:
        t_state: LegState = "missing"
    else:
        missing = [p for p in primary if not _path_exists(vault_root, str(p))]
        if missing and len(missing) == len(primary):
            t_state = "stale"
        elif missing:
            t_state = "stale"
        else:
            stored = meta.get("touch_content_hash")
            t_state = "present" if stored else "draft"

    forbidden = rules.get("forbidden") if isinstance(rules.get("forbidden"), list) else []
    if meta.get("rules_confirmed_at"):
        r_state: LegState = "confirmed"
    elif forbidden:
        r_state = "present"
    else:
        r_state = "missing"

    proof = contract.get("proof") if isinstance(contract.get("proof"), list) else []
    if not proof:
        k_state: LegState = "missing"
    else:
        k_state = "present" if all(_path_exists(vault_root, str(p)) for p in proof) else "stale"

    return LegStatus(conceptual=c_state, touch=t_state, rules=r_state, contract=k_state)


def _pile_for(card_class: CardClass) -> Pile:
    if card_class == "complete_draft":
        return "green"
    if card_class == "incomplete":
        return "incomplete"
    return "orphan"


def _card_class_from_legs(legs: LegStatus, *, orphan: bool = False) -> CardClass:
    if orphan:
        return "orphan"
    if legs.conceptual == "missing" or legs.touch in ("missing", "stale"):
        return "incomplete"
    if legs.rules in ("missing", "orphan") or legs.contract in ("missing", "stale"):
        return "incomplete"
    return "complete_draft"


def build_draft_card(
    vault_root: Path,
    *,
    trinity_id: str,
    component: str,
    primary_path: str,
    source_kind: str,
    anchors: list[DiscoveryAnchor],
    operator_question: str | None = None,
    decision: str = "wrap",
) -> tuple[dict[str, Any], LegStatus, CardClass]:
    slug = trinity_id
    proofs = _guess_test_proof(vault_root, primary_path)
    touch_paths = [primary_path] if primary_path else []

    summary = (
        f"Generated draft for {component}. Defines weave component scope for "
        f"`{primary_path}`. Operator must validate Conceptual before promotion."
    )
    if decision == "defer":
        summary += " Inventory decision: defer — confirm whether a Trinity card is required."

    card: dict[str, Any] = {
        "id": slug,
        "conceptual": {
            "outcome": f"TODO — operator: one-line achievement for {component}.",
            "summary": summary,
            "primary_case": f"TODO — operator: primary runtime case for `{primary_path}`.",
            "edge_cases": [],
            "misread_risks": [],
        },
        "touch": {
            "primary_paths": touch_paths,
            "inbound": [],
            "outbound": [],
            "behavior_signals": [],
        },
        "rules": {
            "forbidden": [],
            "fixtures": [],
            "precedence": [],
            "acceptance": [],
        },
        "contract": {"proof": proofs, "invariant_ids": []},
        "meta": {
            "schema_version": SCHEMA_VERSION,
            "card_class": "complete_draft",
            "source": {
                "kind": source_kind,
                "anchors": [asdict(a) for a in anchors],
                "generated_at": _now_iso(),
            },
        },
    }

    if proofs:
        try:
            proposed = propose_behavior_signals(vault_root, card)
            if proposed:
                card["touch"]["behavior_signals"] = proposed[:12]
        except Exception:
            pass

    legs = assess_leg_status(vault_root, card)
    card_class = _card_class_from_legs(legs)
    card["meta"]["card_class"] = card_class
    card["meta"]["leg_status"] = asdict(legs)
    if operator_question:
        card["meta"]["source"]["operator_question"] = operator_question

    resolved_primary = primary_path
    try:
        from .trinity_harness_backfill import (
            analyze_module,
            apply_backfill_to_card,
            resolve_primary_path_for_trinity_id,
        )

        resolved_primary = resolve_primary_path_for_trinity_id(
            vault_root, trinity_id, primary_path
        )
        if resolved_primary and resolved_primary != primary_path:
            card["touch"]["primary_paths"] = [resolved_primary]
        backfill = None
        if trinity_id.startswith("harness_"):
            cmd = trinity_id.removeprefix("harness_")
            from .trinity_harness_backfill import analyze_harness_command

            backfill = analyze_harness_command(vault_root, cmd)
        if backfill is None:
            backfill = analyze_module(vault_root, resolved_primary or primary_path)
        if backfill:
            card = apply_backfill_to_card(card, backfill)
            card["meta"]["source"]["backfill_applied"] = True
    except Exception:
        card["meta"]["source"]["backfill_applied"] = False

    legs = assess_leg_status(vault_root, card)
    card_class = _card_class_from_legs(legs)
    card["meta"]["card_class"] = card_class
    card["meta"]["leg_status"] = asdict(legs)

    # Never operator lock stamps on generated output.
    card["meta"].pop("conceptual_confirmed_at", None)
    card["meta"].pop("rules_confirmed_at", None)

    return normalize_card(card), legs, card_class


def discover_concept_map_orphans(vault_root: Path) -> list[tuple[str, str]]:
    path = concept_map_path(vault_root)
    if not path.is_file():
        return []
    data = _load_yaml(path)
    concepts = data.get("concepts") if isinstance(data.get("concepts"), dict) else {}
    existing = list_existing_card_ids(vault_root)
    out: list[tuple[str, str]] = []
    for concept_key, row in concepts.items():
        if not isinstance(row, dict):
            continue
        tid = str(row.get("trinity_id") or "").strip()
        if tid and tid not in existing:
            out.append((concept_key, tid))
    return out


def discover_inventory_gaps(rows: list[InventoryRow], existing: set[str]) -> list[InventoryRow]:
    gaps: list[InventoryRow] = []
    for row in rows:
        if row.decision == "defer":
            continue
        tid = row.trinity_id or slug_trinity_id(row.component, row.path)
        if tid in existing and tid in LOCKED_SKIP_IDS:
            continue
        if row.trinity_id and row.trinity_id in existing:
            # Has card file — partial pass handles
            continue
        if not row.trinity_id and tid in existing:
            continue
        gaps.append(row)
    return gaps


def discover_partial_cards(vault_root: Path, *, include_locked: bool) -> list[tuple[str, dict[str, Any], LegStatus]]:
    out: list[tuple[str, dict[str, Any], LegStatus]] = []
    for tid in sorted(list_existing_card_ids(vault_root)):
        if tid in (SCHEMA_CARD, META_CARD_ID):
            continue
        if tid in LOCKED_SKIP_IDS and not include_locked:
            continue
        path = components_dir(vault_root) / f"{tid}.yaml"
        try:
            card = load_trinity_card(vault_root, tid)
        except (FileNotFoundError, ValueError, OSError):
            continue
        if _is_locked(card) and not include_locked:
            continue
        legs = assess_leg_status(vault_root, card)
        if legs.conceptual != "confirmed" or legs.rules != "confirmed":
            out.append((tid, card, legs))
        elif any(v in ("missing", "stale", "orphan") for v in (legs.touch, legs.contract)):
            out.append((tid, card, legs))
    return out


def discover_harness_orphans(vault_root: Path, existing: set[str]) -> list[DiscoveryAnchor]:
    """Harness commands with no plausible trinity card mapping (narrow mode aggregate)."""
    per = discover_per_harness_commands(vault_root, existing)
    return [
        DiscoveryAnchor(path=path, role="orphan_harness")
        for _tid, path in per
    ]


def discover_rule_orphans(vault_root: Path) -> list[DiscoveryAnchor]:
    rules_root = vault_root / ".cursor/rules"
    if not rules_root.is_dir():
        return []
    orphans: list[DiscoveryAnchor] = []
    for p in sorted(rules_root.rglob("*.mdc")):
        try:
            text = p.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        modes = sorted(set(_MAINTENANCE_MODE_RE.findall(text)))
        if not modes:
            continue
        rel = p.relative_to(vault_root).as_posix()
        orphans.append(
            DiscoveryAnchor(
                path=rel,
                role="orphan_rule",
            )
        )
    return orphans


def _already_emitted(records: list[ProposalRecord], trinity_id: str) -> bool:
    return any(r.trinity_id == trinity_id for r in records)


def _module_trinity_id(stem: str) -> str:
    if stem in MODULE_TRINITY_ALIASES:
        return MODULE_TRINITY_ALIASES[stem]
    if stem in LOCKED_SKIP_IDS:
        return stem
    return stem


def _covered_primary_paths(vault_root: Path, rows: list[InventoryRow], existing: set[str]) -> set[str]:
    covered: set[str] = {row.path for row in rows}
    for tid in existing:
        try:
            card = load_trinity_card(vault_root, tid)
        except (FileNotFoundError, ValueError, OSError):
            continue
        touch = card.get("touch") if isinstance(card.get("touch"), dict) else {}
        for key in ("primary_paths", "inbound", "outbound"):
            raw = touch.get(key)
            if isinstance(raw, list):
                for item in raw:
                    s = str(item).strip()
                    if s and not s.endswith("*"):
                        covered.add(s)
    return covered


def discover_weave_module_gaps(
    vault_root: Path,
    *,
    existing: set[str],
    covered: set[str],
) -> list[tuple[str, str]]:
    weave_dir = vault_root / "scripts/eat_queue_core/weave"
    if not weave_dir.is_dir():
        return []
    gaps: list[tuple[str, str]] = []
    for p in sorted(weave_dir.glob("*.py")):
        stem = p.stem
        if stem in WEAVE_MODULE_SKIP:
            continue
        rel = p.relative_to(vault_root).as_posix()
        if rel in covered:
            continue
        tid = _module_trinity_id(stem)
        if tid in existing and tid in LOCKED_SKIP_IDS:
            continue
        if tid in existing and (components_dir(vault_root) / f"{tid}.yaml").is_file():
            # Card file exists — partial pass handles unless wide net wants weave scan for un-inventoried
            if rel in covered or any(rel in c for c in covered if not c.endswith("/**")):
                continue
        gaps.append((tid, rel))
    return gaps


def discover_core_module_gaps(
    vault_root: Path,
    *,
    existing: set[str],
    covered: set[str],
) -> list[tuple[str, str]]:
    core_dir = vault_root / "scripts/eat_queue_core"
    gaps: list[tuple[str, str]] = []
    for p in sorted(core_dir.glob("*.py")):
        stem = p.stem
        if stem in CORE_MODULE_SKIP:
            continue
        rel = p.relative_to(vault_root).as_posix()
        if rel in covered:
            continue
        tid = _module_trinity_id(stem)
        if tid in LOCKED_SKIP_IDS:
            continue
        if (components_dir(vault_root) / f"{tid}.yaml").is_file() and tid in existing:
            continue
        gaps.append((tid, rel))
    return gaps


def discover_per_harness_commands(vault_root: Path, existing: set[str]) -> list[tuple[str, str]]:
    """Each harness command without card mapping → own proposal id."""
    infra = frozenset(
        {
            "trinity_align",
            "trinity_touch_refresh",
            "trinity_pack_preview",
            "trinity_validation_drill",
            "trinity_card_generate",
        }
    )
    out: list[tuple[str, str]] = []
    for cmd in list_harness_commands(vault_root):
        if cmd in infra:
            continue
        if any(cmd == tid or cmd.startswith(f"{tid}_") or tid in cmd for tid in existing):
            continue
        tid = f"harness_{cmd}"
        out.append((tid, f"scripts/eat_queue_core/harness.py#cmd:{cmd}"))
    return out


def discover_per_rule_files(vault_root: Path) -> list[tuple[str, str]]:
    rules_root = vault_root / ".cursor/rules"
    out: list[tuple[str, str]] = []
    if not rules_root.is_dir():
        return out
    for p in sorted(rules_root.rglob("*.mdc")):
        try:
            text = p.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if not _MAINTENANCE_MODE_RE.findall(text) and "weave" not in text.lower() and "trinity" not in text.lower():
            continue
        rel = p.relative_to(vault_root).as_posix()
        slug = p.stem.replace(".", "_")
        tid = f"rule_{slug}"
        out.append((tid, rel))
    return out


def discover_all_skill_stubs(vault_root: Path, existing: set[str]) -> list[tuple[str, str]]:
    skills_root = vault_root / _SKILL_DIR
    out: list[tuple[str, str]] = []
    if not skills_root.is_dir():
        return out
    for p in sorted(skills_root.glob("*/SKILL.md")):
        skill_name = p.parent.name.replace("-", "_")
        if skill_name in existing or f"skill_{skill_name}" in existing:
            continue
        if skill_name == "little_val_structural" and "little_val_structural" in existing:
            continue
        rel = p.relative_to(vault_root).as_posix()
        tid = f"skill_{skill_name}"
        out.append((tid, rel))
    return out


def discover_skill_gaps(vault_root: Path, existing: set[str]) -> list[DiscoveryAnchor]:
    """Mandatory pipeline skills without a trinity card."""
    gaps: list[DiscoveryAnchor] = []
    skill_path = vault_root / _SKILL_DIR / "little-val-structural" / "SKILL.md"
    if skill_path.is_file() and "little_val" not in existing and "little_val_structural" not in existing:
        gaps.append(
            DiscoveryAnchor(
                path=skill_path.relative_to(vault_root).as_posix(),
                role="pair_gap",
            )
        )
    return gaps


def _write_index_md(out_dir: Path, records: list[ProposalRecord]) -> None:
    piles: dict[Pile, list[ProposalRecord]] = {"green": [], "incomplete": [], "orphan": []}
    for r in records:
        piles[r.pile].append(r)

    lines = [
        "# Trinity card proposals",
        "",
        f"Folder: `{out_dir.name}`",
        "",
        "## Green drafts",
        "",
    ]
    for r in piles["green"]:
        lines.append(f"- `{r.trinity_id}` — `{r.output_path}` ({r.source_kind})")
    if not piles["green"]:
        lines.append("- _(none)_")
    lines.extend(["", "## Incomplete", ""])
    for r in piles["incomplete"]:
        q = f" — {r.operator_question}" if r.operator_question else ""
        lines.append(f"- `{r.trinity_id}` — `{r.output_path}`{q}")
    if not piles["incomplete"]:
        lines.append("- _(none)_")
    lines.extend(["", "## Orphans", ""])
    for r in piles["orphan"]:
        q = f" — {r.operator_question}" if r.operator_question else ""
        lines.append(f"- `{r.trinity_id}` — `{r.output_path}`{q}")
    if not piles["orphan"]:
        lines.append("- _(none)_")
    lines.append("")
    (out_dir / "index.md").write_text("\n".join(lines), encoding="utf-8")


def run_trinity_card_generate(
    vault_root: Path,
    *,
    dry_run: bool = False,
    include_locked: bool = False,
    stamp: str | None = None,
    wide_net: bool = True,
    skip_rule_orphans: bool = False,
) -> dict[str, Any]:
    vault_root = vault_root.resolve()
    stamp, out_dir = _resolve_proposals_dir(vault_root, stamp, wide_net=wide_net)
    cards_dir = out_dir / "cards"
    stubs_dir = out_dir / "stubs"

    rows = parse_inventory_table(vault_root)
    existing = list_existing_card_ids(vault_root)
    covered = _covered_primary_paths(vault_root, rows, existing)
    records: list[ProposalRecord] = []
    written: list[str] = []
    skipped_locked: list[str] = []

    def emit(
        trinity_id: str,
        card: dict[str, Any],
        *,
        source_kind: str,
        legs: LegStatus,
        card_class: CardClass,
        anchors: list[DiscoveryAnchor],
        operator_question: str | None = None,
        subdir: str = "cards",
    ) -> None:
        nonlocal records, written
        pile = _pile_for(card_class)
        rel_name = f"{subdir}/{trinity_id}.yaml"
        out_path = out_dir / rel_name
        rec = ProposalRecord(
            trinity_id=trinity_id,
            card_class=card_class,
            pile=pile,
            source_kind=source_kind,
            leg_status=legs,
            anchors=anchors,
            operator_question=operator_question,
            output_path=rel_name,
        )
        records.append(rec)
        if not dry_run:
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(_dump_yaml(card), encoding="utf-8")
            written.append(rel_name)

    # Inventory gaps → drafts
    for row in discover_inventory_gaps(rows, existing):
        tid = row.trinity_id or slug_trinity_id(row.component, row.path)
        if tid in LOCKED_SKIP_IDS and not include_locked:
            skipped_locked.append(tid)
            continue
        anchors = [DiscoveryAnchor(path=row.path, role="inventory_row")]
        card, legs, card_class = build_draft_card(
            vault_root,
            trinity_id=tid,
            component=row.component,
            primary_path=row.path,
            source_kind="inventory_row",
            anchors=anchors,
            decision=row.decision,
        )
        emit(tid, card, source_kind="inventory_row", legs=legs, card_class=card_class, anchors=anchors)

    if wide_net:
        # Weave package modules not in inventory / locked cards
        for tid, rel in discover_weave_module_gaps(vault_root, existing=existing, covered=covered):
            if _already_emitted(records, tid):
                continue
            if tid in LOCKED_SKIP_IDS and not include_locked:
                skipped_locked.append(tid)
                continue
            anchors = [DiscoveryAnchor(path=rel, role="weave_module_orphan")]
            card, legs, card_class = build_draft_card(
                vault_root,
                trinity_id=tid,
                component=tid.replace("_", " "),
                primary_path=rel,
                source_kind="weave_module_orphan",
                anchors=anchors,
                operator_question=f"Weave module `{rel}` has no Trinity card — add to inventory or merge?",
            )
            emit(tid, card, source_kind="weave_module_orphan", legs=legs, card_class=card_class, anchors=anchors)

        # Top-level eat_queue_core modules
        for tid, rel in discover_core_module_gaps(vault_root, existing=existing, covered=covered):
            if _already_emitted(records, tid):
                continue
            anchors = [DiscoveryAnchor(path=rel, role="core_module_orphan")]
            card, legs, card_class = build_draft_card(
                vault_root,
                trinity_id=tid,
                component=tid.replace("_", " "),
                primary_path=rel,
                source_kind="core_module_orphan",
                anchors=anchors,
                operator_question=f"Core module `{rel}` has no Trinity card — component or glue?",
            )
            card_class = "orphan"
            card["meta"]["card_class"] = card_class
            emit(
                tid,
                card,
                source_kind="core_module_orphan",
                legs=legs,
                card_class=card_class,
                anchors=anchors,
                operator_question=card["meta"]["source"]["operator_question"],
                subdir="stubs",
            )

    # Partial existing cards → incomplete proposals (copy + provenance overlay)
    for tid, card, legs in discover_partial_cards(vault_root, include_locked=include_locked):
        card_class = _card_class_from_legs(legs)
        overlay = dict(card)
        meta = dict(overlay.get("meta") or {})
        meta["card_class"] = card_class
        meta["leg_status"] = asdict(legs)
        meta["source"] = {
            "kind": "existing_partial",
            "anchors": [{"path": f".technical/weave/components/{tid}.yaml", "role": "partial_card"}],
            "generated_at": _now_iso(),
        }
        meta.pop("conceptual_confirmed_at", None)
        meta.pop("rules_confirmed_at", None)
        overlay["meta"] = meta
        q = None
        if legs.rules == "missing":
            q = f"Card `{tid}` exists but Rules leg empty — author forbidden/precedence or defer."
        elif legs.conceptual == "draft":
            q = f"Card `{tid}` Conceptual not confirmed — operator validation required."
        emit(
            tid,
            normalize_card(overlay),
            source_kind="existing_partial",
            legs=legs,
            card_class=card_class,
            anchors=[DiscoveryAnchor(path=f".technical/weave/components/{tid}.yaml", role="partial_card")],
            operator_question=q,
        )

    # Concept map orphans
    for concept_key, tid in discover_concept_map_orphans(vault_root):
        if tid in existing and _is_locked(load_trinity_card(vault_root, tid)) and not include_locked:
            skipped_locked.append(tid)
            continue
        anchors = [
            DiscoveryAnchor(path=".technical/weave/concept-trinity-map.yaml", role="orphan_concept"),
            DiscoveryAnchor(path=f"concept:{concept_key}", role="concept_key"),
        ]
        card, legs, card_class = build_draft_card(
            vault_root,
            trinity_id=tid,
            component=concept_key.replace("_", " "),
            primary_path="",
            source_kind="orphan_concept",
            anchors=anchors,
            operator_question=f"Concept `{concept_key}` maps to trinity_id `{tid}` but no component YAML exists.",
        )
        card_class = "orphan" if not card.get("touch", {}).get("primary_paths") else card_class
        emit(
            tid,
            card,
            source_kind="orphan_concept",
            legs=legs,
            card_class=card_class,
            anchors=anchors,
            operator_question=card["meta"]["source"].get("operator_question"),
            subdir="stubs" if card_class == "orphan" else "cards",
        )

    # Defer inventory rows → orphan stubs (pair_gap / incomplete)
    for row in rows:
        if row.decision != "defer":
            continue
        tid = row.trinity_id or slug_trinity_id(row.component, row.path)
        if any(r.trinity_id == tid for r in records):
            continue
        anchors = [DiscoveryAnchor(path=row.path, role="inventory_defer")]
        card, legs, _ = build_draft_card(
            vault_root,
            trinity_id=tid,
            component=row.component,
            primary_path=row.path if _path_exists(vault_root, row.path) else "",
            source_kind="inventory_defer",
            anchors=anchors,
            operator_question=f"Inventory marks `{row.component}` as defer — card needed or documentation-only?",
            decision="defer",
        )
        card_class: CardClass = "orphan"
        card["meta"]["card_class"] = card_class
        emit(
            tid,
            card,
            source_kind="inventory_defer",
            legs=legs,
            card_class=card_class,
            anchors=anchors,
            operator_question=card["meta"]["source"].get("operator_question"),
            subdir="stubs",
        )

    # Skill stubs — wide net: every skill; narrow: little-val pair gap only
    if wide_net:
        for tid, rel in discover_all_skill_stubs(vault_root, existing):
            if _already_emitted(records, tid):
                continue
            anchors = [DiscoveryAnchor(path=rel, role="skill_orphan")]
            card, legs, card_class = build_draft_card(
                vault_root,
                trinity_id=tid,
                component=tid.removeprefix("skill_").replace("_", " "),
                primary_path=rel,
                source_kind="skill_orphan",
                anchors=anchors,
                operator_question="Pipeline skill has no Trinity card — defer, merge, or author?",
            )
            card_class = "orphan"
            card["meta"]["card_class"] = card_class
            emit(
                tid,
                card,
                source_kind="skill_orphan",
                legs=legs,
                card_class=card_class,
                anchors=anchors,
                operator_question=card["meta"]["source"]["operator_question"],
                subdir="stubs/skills",
            )
    else:
        for anchor in discover_skill_gaps(vault_root, existing):
            tid = "little_val_structural"
            if _already_emitted(records, tid):
                continue
            card, legs, card_class = build_draft_card(
                vault_root,
                trinity_id=tid,
                component="little val structural check",
                primary_path=anchor.path,
                source_kind="pair_gap",
                anchors=[anchor],
                operator_question="Mandatory pipeline guard skill has no Trinity card — create card or defer?",
            )
            card_class = "orphan"
            card["meta"]["card_class"] = card_class
            emit(
                tid,
                card,
                source_kind="pair_gap",
                legs=legs,
                card_class=card_class,
                anchors=[anchor],
                operator_question=card["meta"]["source"]["operator_question"],
                subdir="stubs",
            )

    if wide_net:
        for tid, path in discover_per_harness_commands(vault_root, existing):
            if _already_emitted(records, tid):
                continue
            cmd = path.split("#cmd:", 1)[-1]
            anchors = [DiscoveryAnchor(path=path, role="orphan_harness")]
            card, legs, card_class = build_draft_card(
                vault_root,
                trinity_id=tid,
                component=f"harness command {cmd}",
                primary_path="scripts/eat_queue_core/harness.py",
                source_kind="orphan_harness",
                anchors=anchors,
                operator_question=f"Harness `{cmd}` lacks Trinity card pairing — map to component or defer.",
            )
            card_class = "orphan"
            card["meta"]["card_class"] = card_class
            emit(
                tid,
                card,
                source_kind="orphan_harness",
                legs=legs,
                card_class=card_class,
                anchors=anchors,
                operator_question=card["meta"]["source"]["operator_question"],
                subdir="stubs/harness",
            )
    else:
        harness_orphans = discover_harness_orphans(vault_root, existing)
        if harness_orphans and not _already_emitted(records, "orphan_harness_commands"):
            tid = "orphan_harness_commands"
            anchors = harness_orphans[:40]
            card, legs, card_class = build_draft_card(
                vault_root,
                trinity_id=tid,
                component="orphan harness commands",
                primary_path="scripts/eat_queue_core/harness.py",
                source_kind="orphan_harness",
                anchors=anchors,
                operator_question="Harness commands lack Trinity card pairing — split into components or extend inventory.",
            )
            card["meta"]["card_class"] = "orphan"
            card["touch"]["outbound"] = [a.path for a in anchors[:15]]
            emit(
                tid,
                card,
                source_kind="orphan_harness",
                legs=legs,
                card_class="orphan",
                anchors=anchors,
                operator_question=card["meta"]["source"]["operator_question"],
                subdir="stubs",
            )

    if not skip_rule_orphans:
        if wide_net:
            for tid, rel in discover_per_rule_files(vault_root):
                if _already_emitted(records, tid):
                    continue
                anchors = [DiscoveryAnchor(path=rel, role="orphan_rule")]
                card, legs, card_class = build_draft_card(
                    vault_root,
                    trinity_id=tid,
                    component=f"rule surface {Path(rel).stem}",
                    primary_path=rel,
                    source_kind="orphan_rule",
                    anchors=anchors,
                    operator_question=f"Rule `{rel}` references maintenance/weave — pair to harness and Trinity card.",
                )
                card_class = "orphan"
                card["meta"]["card_class"] = card_class
                emit(
                    tid,
                    card,
                    source_kind="orphan_rule",
                    legs=legs,
                    card_class=card_class,
                    anchors=anchors,
                    operator_question=card["meta"]["source"]["operator_question"],
                    subdir="stubs/rules",
                )
        else:
            rule_orphans = discover_rule_orphans(vault_root)
            if rule_orphans and not _already_emitted(records, "orphan_maintenance_rules"):
                tid = "orphan_maintenance_rules"
                anchors = rule_orphans[:30]
                card, legs, card_class = build_draft_card(
                    vault_root,
                    trinity_id=tid,
                    component="maintenance rule surfaces",
                    primary_path=".cursor/rules/agents/queue.mdc",
                    source_kind="orphan_rule",
                    anchors=anchors,
                    operator_question="Rules reference maintenance modes — pair each mode to harness handler and Trinity card.",
                )
                card["meta"]["card_class"] = "orphan"
                emit(
                    tid,
                    card,
                    source_kind="orphan_rule",
                    legs=legs,
                    card_class="orphan",
                    anchors=anchors,
                    operator_question=card["meta"]["source"]["operator_question"],
                    subdir="stubs",
                )

    counts = {"green": 0, "incomplete": 0, "orphan": 0}
    for r in records:
        counts[r.pile] += 1

    manifest = {
        "ok": True,
        "stamp": stamp,
        "generated_at": _now_iso(),
        "dry_run": dry_run,
        "wide_net": wide_net,
        "skip_rule_orphans": skip_rule_orphans,
        "output_dir": out_dir.relative_to(vault_root).as_posix(),
        "counts": counts,
        "total": len(records),
        "skipped_locked": skipped_locked,
        "proposals": [
            {
                "trinity_id": r.trinity_id,
                "card_class": r.card_class,
                "pile": r.pile,
                "source_kind": r.source_kind,
                "output_path": r.output_path,
                "leg_status": asdict(r.leg_status),
                "operator_question": r.operator_question,
            }
            for r in records
        ],
        "written": written,
    }

    if not dry_run:
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
        _write_index_md(out_dir, records)

    return manifest
