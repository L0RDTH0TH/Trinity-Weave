"""Phase 11b + 13 — Prompt ↔ Trinity contract (Pull + Route + Query).

Meta card: trinity_prompt_context (locked components/).
MVL lens: locked meta YAML drives prepend order, leg inclusion, forbidden patterns.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Literal

from .trinity_card import get_conceptual, get_contract, get_rules, get_touch
from .trinity_card_paths import load_trinity_card
from .trinity_mvl_lens import (
    MvlConductorBundle,
    get_lens_contract,
    load_meta_lens_legs,
    probe_mvl_lens,
    resolve_config_slice,
)

TaskKind = Literal[
    "conceptual_regen",
    "conduct_repair",
    "generator_emit",
    "audit_readonly",
    "queue_recovery",
    "acceptance_audit",
    "regen_burn",
    "roadmap_continue",
    "weave_cycle",
    "architect_packet",
    "curator_capture",
    "prompt_crafter",
    "weave_query",
    "redesign_factory",
    "expand_self",
    "unknown",
]

QueryKind = Literal[
    "nerve_status",
    "consumable_check",
    "knob_parity",
    "factory_lifecycle",
    "closure_read",
]

IngressClass = Literal["question", "command", "mixed"]

# Back-compat aliases (tests / imports).
META_PREPEND_ORDER: tuple[str, ...] = (
    "conceptual_style_guide",
    "trinity_card_authoring",
    "trinity_prompt_context",
)

FORBIDDEN_PROMPT_PATTERNS: tuple[str, ...] = (
    "whole_vault_dump",
    "unrelated_trinity_ids",
    "green_wash_import_only",
    "deleted_asserts",
    "edit_outside_write_contract",
)

_TRIGGER_PATTERNS: list[tuple[re.Pattern[str], str, TaskKind, str | None]] = [
    (re.compile(r"(?i)\bEAT-QUEUE\b|\bProcess queue\b|\beat cache\b"), "weave_cycle", "weave_cycle", None),
    (
        re.compile(r"(?i)we are making a (?:code |roadmap )?prompt"),
        "prompt_crafter",
        "prompt_crafter",
        None,
    ),
    (re.compile(r"(?i)\bRESUME_ROADMAP\b|Resume roadmap"), "roadmap", "roadmap_continue", None),
    (
        re.compile(r"(?i)trinity_weave_self_wrap.*--regenerate-complete"),
        "regen_burn",
        "regen_burn",
        None,
    ),
    (
        re.compile(r"(?i)trinity_weave_self_wrap"),
        "acceptance_audit",
        "acceptance_audit",
        "trinity_spine_maintenance",
    ),
    (
        re.compile(r"(?i)\b(goal packet|goal-authority|headless|overnight)\b"),
        "architect_packet",
        "architect_packet",
        None,
    ),
    (
        re.compile(r"(?i)\b(museum|curator|institute lane|capture)\b"),
        "curator_capture",
        "curator_capture",
        None,
    ),
    (
        re.compile(r"(?i)\b(?:conduct|proof)\b.*\b(harness_[a-z0-9_]+)\b"),
        "conduct_repair",
        "conduct_repair",
        None,
    ),
    (re.compile(r"(?i)\bREPAIR CRAFT\b|\bPROMPT CRAFT RECOVERY\b"), "queue_recovery", "queue_recovery", None),
]

_QUERY_PATTERNS: list[tuple[re.Pattern[str], QueryKind]] = [
    (
        re.compile(r"(?i)\b(conduct red|which cards are red|nerve status|what is red)\b"),
        "nerve_status",
    ),
    (
        re.compile(r"(?i)\b(can i pack|consumable check|is .+ consumable)\b"),
        "consumable_check",
    ),
    (
        re.compile(r"(?i)\b(knob parity|speed_mode parity|matrix gap)\b"),
        "knob_parity",
    ),
    (
        re.compile(
            r"(?i)\b(refurb or redesign|factory lifecycle|rust grade|redesign_factory)\b"
        ),
        "factory_lifecycle",
    ),
    (
        re.compile(r"(?i)\b(closure read|what paths|primary_paths for)\b"),
        "closure_read",
    ),
]

_LANE_RE = re.compile(r"(?i)\blane\s+([a-z0-9_-]+)\b")
_EXPLICIT_HARNESS_RE = re.compile(r"\b(harness_[a-z][a-z0-9_]+)\b")
_EXPLICIT_COMPONENT_RE = re.compile(
    r"\b(trinity_[a-z][a-z0-9_]+|lane_[a-z][a-z0-9_]+|l[234]_[a-z][a-z0-9_]+)\b"
)
_STOPWORDS = frozenset(
    {
        "there",
        "their",
        "making",
        "prompt",
        "roadmap",
        "resume",
        "conduct",
        "fix",
        "full",
        "corpus",
        "vault",
        "queue",
        "process",
        "lane",
        "godot",
        "sandbox",
        "institute",
        "maintenance",
        "shared",
        "default",
    }
)


@dataclass
class TrinityRouteResult:
    trigger_class: str
    task_kind: TaskKind
    trinity_id: str | None
    lane: str | None = None
    layer: str | None = None
    consumable_required: bool = False
    clarifying_question: str | None = None
    route_notes: list[str] = field(default_factory=list)
    ingress_class: IngressClass | None = None
    query_kind: QueryKind | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "trigger_class": self.trigger_class,
            "task_kind": self.task_kind,
            "trinity_id": self.trinity_id,
            "lane": self.lane,
            "layer": self.layer,
            "consumable_required": self.consumable_required,
            "clarifying_question": self.clarifying_question,
            "route_notes": self.route_notes,
            "ingress_class": self.ingress_class,
            "query_kind": self.query_kind,
        }


@dataclass
class TrinityQueryResult:
    query_kind: QueryKind | str
    ingress_class: IngressClass
    meta_prepend: list[str]
    meta_legs: dict[str, Any]
    legs: dict[str, Any]
    forbidden: list[str]
    write_scope: str
    scope: dict[str, Any] = field(default_factory=dict)
    claim_tier: str = "structural"

    def to_dict(self) -> dict[str, Any]:
        return {
            "query_kind": self.query_kind,
            "ingress_class": self.ingress_class,
            "meta_prepend": self.meta_prepend,
            "meta_legs": self.meta_legs,
            "legs": self.legs,
            "forbidden": self.forbidden,
            "write_scope": self.write_scope,
            "scope": self.scope,
            "claim_tier": self.claim_tier,
        }


@dataclass
class PromptContextBundle:
    trinity_id: str
    task_kind: TaskKind
    tier: str
    meta_prepend: list[str]
    legs: dict[str, Any]
    forbidden: list[str]
    write_scope: str
    meta_legs: dict[str, Any] = field(default_factory=dict)
    config_slice: dict[str, Any] = field(default_factory=dict)
    lens_source: str = "fallback"

    def to_dict(self) -> dict[str, Any]:
        return {
            "trinity_id": self.trinity_id,
            "task_kind": self.task_kind,
            "tier": self.tier,
            "meta_prepend": self.meta_prepend,
            "meta_legs": self.meta_legs,
            "legs": self.legs,
            "forbidden": list(self.forbidden),
            "write_scope": self.write_scope,
            "config_slice": self.config_slice,
            "lens_source": self.lens_source,
        }


def _write_scope_for(task_kind: str) -> str:
    if task_kind == "conceptual_regen":
        return "conceptual_only"
    if task_kind == "conduct_repair":
        return "contract_proof_paths_only"
    if task_kind == "generator_emit":
        return "provisional_card_fields"
    if task_kind == "queue_recovery":
        return "advisory_no_vault_write"
    if task_kind == "weave_query":
        return "read_only"
    if task_kind in ("redesign_factory", "expand_self"):
        return "provisional_card_fields"
    return "read_only"


def _extract_explicit_id(text: str, *, lane: str | None = None) -> str | None:
    for m in _EXPLICIT_HARNESS_RE.finditer(text):
        return m.group(1)
    for m in _EXPLICIT_COMPONENT_RE.finditer(text):
        tok = m.group(1).lower()
        if tok in _STOPWORDS or (lane and tok == lane):
            continue
        return tok
    return None


def _conduct_harness_id(text: str) -> str | None:
    m = re.search(r"(?i)\b(?:conduct|proof)\b.*\b(harness_[a-z0-9_]+)\b", text)
    return m.group(1) if m else None


def _detect_query_kind(text: str) -> QueryKind | None:
    for pattern, qk in _QUERY_PATTERNS:
        if pattern.search(text):
            return qk
    return None


def _classify_ingress(text: str) -> IngressClass:
    has_query = _detect_query_kind(text) is not None
    has_command = any(p.search(text) for p, *_ in _TRIGGER_PATTERNS)
    if not has_command:
        has_command = bool(_extract_explicit_id(text)) or bool(
            re.search(r"(?i)\b(fix|repair|run|deepen|ingest|distill)\b", text)
        )
    if has_query and has_command:
        return "mixed"
    if has_query:
        return "question"
    return "command"


def _build_legs_from_card(card: dict[str, Any], include: frozenset[str]) -> dict[str, Any]:
    legs: dict[str, Any] = {}
    if "conceptual" in include or "conceptual_draft" in include or "conceptual_outcome" in include:
        con = get_conceptual(card)
        if "conceptual_draft" in include:
            legs["conceptual_draft"] = con
        elif "conceptual_outcome" in include:
            legs["conceptual_outcome"] = {
                k: con.get(k) for k in ("outcome", "summary", "frame_anchor") if con.get(k)
            }
        else:
            legs["conceptual"] = con
    if "touch" in include:
        legs["touch"] = get_touch(card)
    if "rules" in include:
        legs["rules"] = get_rules(card)
    if "contract" in include:
        legs["contract"] = get_contract(card)
    return legs


def resolve_trinity_route(
    vault_root: Path,
    user_prompt: str,
    *,
    host_hints: dict[str, Any] | None = None,
) -> TrinityRouteResult:
    """Face B — given user/operator prompt, how to traverse Trinity."""
    vault_root = vault_root.resolve()
    text = (user_prompt or "").strip()
    hints = host_hints or {}
    notes: list[str] = []

    lane_m = _LANE_RE.search(text)
    lane = lane_m.group(1).lower() if lane_m else None
    ingress = _classify_ingress(text)
    query_kind = _detect_query_kind(text)

    if ingress in ("question", "mixed") and query_kind:
        notes.append("Route → Query (read-only); Pull only when mixed action half resolved")
        return TrinityRouteResult(
            trigger_class="weave_query",
            task_kind="weave_query",
            trinity_id=hints.get("trinity_id") or _extract_explicit_id(text, lane=lane),
            lane=lane,
            ingress_class=ingress,
            query_kind=query_kind,
            route_notes=notes,
        )

    if hints.get("trinity_id"):
        explicit_id: str | None = str(hints["trinity_id"])
    else:
        explicit_id = _extract_explicit_id(text, lane=lane)

    for pattern, trigger_class, task_kind, default_id in _TRIGGER_PATTERNS:
        if pattern.search(text):
            tid = default_id
            if trigger_class == "conduct_repair":
                tid = _conduct_harness_id(text) or explicit_id or default_id
            elif trigger_class not in (
                "weave_cycle",
                "prompt_crafter",
                "architect_packet",
                "curator_capture",
            ):
                tid = explicit_id or default_id
            layer = None
            consumable = False
            if trigger_class == "weave_cycle":
                tid = None
                layer = "layer1_queue"
                notes.append("dispatcher: Task(queue); no single consumable card id")
            elif trigger_class == "prompt_crafter":
                notes.append("system-funnels: full Q&A before queue append")
            elif trigger_class == "architect_packet":
                layer = "layer0_architect"
                notes.append("architect-goal-packet-shield: no inline pipeline until packet confirmed")
            elif trigger_class == "curator_capture":
                layer = "layer0_curator"
                notes.append("curator-agent: institute PQ prep; lane curator invalid")
            elif trigger_class == "conduct_repair" and tid:
                consumable = False
                notes.append("10g overlay after Pull; respect write_scope contract.proof")
            elif trigger_class == "acceptance_audit":
                layer = "harness"
                tid = tid or "trinity_spine_maintenance"
            return TrinityRouteResult(
                trigger_class=trigger_class,
                task_kind=task_kind,
                trinity_id=tid,
                lane=lane,
                layer=layer or hints.get("layer"),
                consumable_required=consumable,
                ingress_class="command",
                route_notes=notes,
            )

    if explicit_id and explicit_id not in _STOPWORDS:
        return TrinityRouteResult(
            trigger_class="explicit_trinity_id",
            task_kind="audit_readonly",
            trinity_id=explicit_id,
            lane=lane,
            ingress_class="command",
            route_notes=["explicit id in message; default task_kind audit_readonly"],
        )

    return TrinityRouteResult(
        trigger_class="ambiguous_chat",
        task_kind="unknown",
        trinity_id=None,
        lane=lane,
        ingress_class="command",
        clarifying_question=(
            "Are we routing through Trinity (give trinity_id or mode phrase), "
            "or is this general chat?"
        ),
        route_notes=["do not guess trinity_id on low confidence"],
    )


def resolve_trinity_query(
    vault_root: Path,
    query_kind: QueryKind | str,
    *,
    scope: dict[str, Any] | None = None,
    trinity_id: str | None = None,
    prefer: str = "locked",
) -> TrinityQueryResult:
    """Face C — read-only weave introspection; never Pull write scope."""
    vault_root = vault_root.resolve()
    qk = str(query_kind or "nerve_status").strip()
    lens = get_lens_contract(vault_root)
    scope_d = dict(scope or {})
    if trinity_id:
        scope_d.setdefault("trinity_id", trinity_id)

    meta_prepend = lens.meta_prepend_for("weave_query")
    meta_legs = load_meta_lens_legs(vault_root, meta_prepend)

    legs: dict[str, Any] = {}
    leg_keys = lens.query_legs_for(qk)
    if trinity_id and leg_keys:
        try:
            card = load_trinity_card(vault_root, trinity_id, prefer=prefer)
            legs = _build_legs_from_card(card, leg_keys)
        except (OSError, ValueError, FileNotFoundError):
            legs = {"error": f"trinity_id_not_found:{trinity_id}"}

    if qk == "nerve_status":
        nerve_path = vault_root / ".technical" / "weave" / "corps-nerve-map.json"
        if nerve_path.is_file():
            import json

            try:
                legs["nerve_map_summary"] = {
                    "path": nerve_path.relative_to(vault_root).as_posix(),
                    "loaded": True,
                }
            except (OSError, ValueError, json.JSONDecodeError):
                legs["nerve_map_summary"] = {"loaded": False}

    forbidden = list(lens.forbidden) + [
        "pull_write_scope",
        "regen_or_conduct_repair",
        "external_research",
    ]

    return TrinityQueryResult(
        query_kind=qk,  # type: ignore[arg-type]
        ingress_class="question",
        meta_prepend=meta_prepend,
        meta_legs=meta_legs,
        legs=legs,
        forbidden=forbidden,
        write_scope="read_only",
        scope=scope_d,
        claim_tier="structural",
    )


def resolve_prompt_context(
    vault_root: Path,
    trinity_id: str,
    task_kind: TaskKind | str,
    *,
    prefer: str = "provisional",
    extra_meta_ids: list[str] | None = None,
) -> PromptContextBundle:
    """Face A — given trinity_id, what goes into the agent prompt (MVL lens-aware)."""
    vault_root = vault_root.resolve()
    tid = str(trinity_id).strip()
    kind = str(task_kind) if task_kind else "unknown"
    lens = get_lens_contract(vault_root)

    card = load_trinity_card(vault_root, tid, prefer=prefer)
    tier = "provisional" if prefer == "provisional" else "locked"

    include = lens.pull_legs_for(kind)
    legs = _build_legs_from_card(card, include)

    meta_prepend = lens.meta_prepend_for(kind)
    if extra_meta_ids:
        seen = set(meta_prepend)
        for mid in extra_meta_ids:
            if mid not in seen:
                meta_prepend.append(mid)
                seen.add(mid)

    meta_legs = load_meta_lens_legs(vault_root, meta_prepend)
    forbidden = list(lens.forbidden)

    return PromptContextBundle(
        trinity_id=tid,
        task_kind=kind,  # type: ignore[arg-type]
        tier=tier,
        meta_prepend=meta_prepend,
        meta_legs=meta_legs,
        legs=legs,
        forbidden=forbidden,
        write_scope=_write_scope_for(kind),
        config_slice=resolve_config_slice(vault_root),
        lens_source=lens.source,
    )


def build_mvl_conductor_bundle(
    vault_root: Path,
    trinity_id: str,
    task_kind: TaskKind | str,
    *,
    prefer: str = "provisional",
) -> MvlConductorBundle:
    """Full MVL conductor bundle for self-wrap / corps / host hand-off."""
    pull = resolve_prompt_context(vault_root, trinity_id, task_kind, prefer=prefer)
    return MvlConductorBundle(
        trinity_id=pull.trinity_id,
        task_kind=str(pull.task_kind),
        lens_source=pull.lens_source,
        meta_prepend=pull.meta_prepend,
        meta_legs=pull.meta_legs,
        legs=pull.legs,
        config_slice=pull.config_slice,
        forbidden=pull.forbidden,
        write_scope=pull.write_scope,
    )


# Re-export for self-wrap probe.
run_mvl_lens_probe = probe_mvl_lens
