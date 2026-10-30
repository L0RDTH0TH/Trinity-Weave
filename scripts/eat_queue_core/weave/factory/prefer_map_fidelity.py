"""Ticket-map Prefer fidelity — mechanical Gate A + harness Gate B₁ latch.

Gate A is form completeness only: row bind, verbatim product job, observe↔shape,
catalog ids exist, do_not_waive, no author hostile bits. A does not judge truth.

Third Gate A status ``incomplete_missing_observer``: empty checks + named
``missing_observer``, forms otherwise bindable → ``ok: false``, empty
violations, short-circuit before catalog empty-check. Not launchable. Not a pass.

Gate B₁ is factory-order Cursor senior (``cursor_senior_b1``). Author
``map_fidelity_hostile_ok`` is ignored.

Cite: Prefer-Authorship-Host-Law §C.3 · active ticket map via
factory-project.yaml ``ticket_map_runtime`` / discovery (no product hardwire).
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

from .ticket_map_schema import (
    MapTicketRow,
    SELECTABLE_TICKET_STATUS,
    load_ticket_map_rows,
    parse_ticket_map_rows,
    resolve_active_ticket_map_rel,
    section_open_neighbor_ids,
)

# Prefer packets for MAP rows (WORLD / GEN / VIS / LOOP / PACK / PLACE / DESK)
# must carry these refuse codes (Host-Law §C.3).
PRODUCT_MAP_DO_NOT_WAIVE: tuple[str, ...] = (
    "hotkey_as_product_ux",
    "config_meta_without_effect",
    "stub_as_hours",
    "map_job_name_only",
    "explicit_met_implicit_miss",
    "intent_collapsed_to_mechanics",
    # session-prep / clean-slate map (world-builder-session-prep)
    "separate_wiki_as_prep",
    "campaign_unscoped",
    "rail_collapsed",
    "inherited_prior_keep",
    "hidden_default_dial",
    "old_host_as_new_product",
)
# Back-compat alias for callers / tests.
WORLD_GEN_MAP_DO_NOT_WAIVE: tuple[str, ...] = PRODUCT_MAP_DO_NOT_WAIVE

STATUS_FORMS_OK = "forms_ok"
STATUS_FORMS_FAIL = "forms_fail"
STATUS_INCOMPLETE_MISSING_OBSERVER = "incomplete_missing_observer"

SUCCESS_OBJECT_DENY: tuple[str, ...] = (
    "contract_bound",
    "meta_written",
    "hotkey_bound",
    "map_job_name_only",
    "stub_ok",
    "chrome_only",
)

# Ticket-map id / mode prefixes — product-agnostic families (old + session-prep).
# Prefer always sets ticket_map_id; prefixes only catch Prefer-on without an id.
MAP_TICKET_PREFIXES: tuple[str, ...] = (
    "world_",
    "gen_",
    "world-",
    "gen-",
    "vis_",
    "vis-",
    "loop_",
    "loop-",
    "pack_",
    "pack-",
    "place_",
    "place-",
    "desk_",
    "desk-",
    "mini_hours",
    # world-builder-session-prep families
    "wb-",
    "wb_",
    "camp-",
    "camp_",
    "dial-",
    "dial_",
    "rail-",
    "rail_",
    "prep-",
    "prep_",
    "pf-",
    "pf_",
    "cont-",
    "cont_",
    "proof-",
    "proof_",
    "cam-",
    "cam_",
    "ctrl-",
    "ctrl_",
    "weld-",
    "weld_",
)

# Align with host-law / Prefer class PLACE|craft|dual signals (no baked markers).
PREFER_PRODUCT_SLICE_MARKERS: tuple[str, ...] = (
    "worldgen",
    "terrain3d_feed",
    "dualgrid",
    "dual_grid",
    "ux_world_generation",
    "townscaper",
    "tutorial_s",
    "occupancy",
    "stalberg",
    "organic_quad",
    "quad_kernel",
    "craft_plane",
    "dual_place",
    "dual_coast",
    "dual_visual",
    "dual_corner",
    "dual_lattice",
    "dual_offset",
    "dual_terrain",
    "owned_cell_place",
    "tri_cell_place",
)

# claim_class values that count as a Prefer/factory Success altitude (not skip).
_SUCCESS_CLAIM_CLASSES: frozenset[str] = frozenset(
    {
        "ask_success",
        "component",
        "keep",
        "keep_real",
        "success",
        "staging",
        "staging_awaiting_f5",
        "staging_incomplete",
        "",
    }
)

# Map tickets may only use these claim classes (never staging).
_MAP_ALLOWED_CLAIM_CLASSES: frozenset[str] = frozenset({"component", "ask_success"})

# Half-B / demo machine fields — Prefer may carry only if the map row names them.
_ROW_GATED_PREFER_FIELDS: tuple[str, ...] = (
    "template",
    "umbrella_ask_id",
    "prefer_class",
    "lane",
    "lane_id",
    "worldgen_entry_scene",
    "launch_scene",
    "catalog_row_id",
)

_HALF_B_FORBIDDEN_VALUES: frozenset[str] = frozenset(
    {
        "half-b-weld-brief-template",
        "alpha_architecture_implementation",
    }
)

# Registered contract classes — Prefer may set without the map row naming them.
# Worldgen / place / craft / Half-B values still require row naming.
_ROW_FREE_PREFER_CLASSES: frozenset[str] = frozenset(
    {"foundation", "contract", "component"}
)

# Positive weld declaration lines on the row (not mere substring mentions).
_EXPLICIT_WELD_LINE_RE = re.compile(
    r"(?m)^\s*W([1-9])\s*[:.—\-]",
)

# Behavior-key role classification (contract vs moment) — role patterns, not a
# two-string denylist of example keys.
_VISIBILITY_KEY_RE = re.compile(
    r"(?:^sees_|_sees_|^shows_|_shows_|^displays_|_displays_|"
    r"^watches_|_watches_|^points_at_|_points_at_|"
    r"_visible$|_watchable$|_shown$|stranger_sees|menu_opens)",
    re.I,
)
_INVARIANT_KEY_RE = re.compile(
    r"(?:identity|holds|unchanged|survives|persist|invariant|"
    r"round_?trip|equals?|_eq_|after_|under_|commit)",
    re.I,
)

def _load_proof_catalog_probes(
    vault_root: Path | None, project_id: str
) -> dict[str, Any] | None:
    if vault_root is None or not str(project_id or "").strip():
        return None
    try:
        from .bindings import load_family, require_project_id

        pid = require_project_id(project_id)
        catalog = load_family(vault_root, pid, "proof-catalog")
    except Exception:
        return None
    probes = catalog.get("probes") if isinstance(catalog, dict) else None
    return probes if isinstance(probes, dict) else None


def _author_set_hostile_bits(armed: dict[str, Any] | None) -> list[str]:
    """Gate A refuse: Prefer packet must not carry author-set hostile bits."""
    if not isinstance(armed, dict):
        return []
    out: list[str] = []
    if armed.get("map_fidelity_hostile_ok") is True:
        out.append("map_fidelity:author_set_map_fidelity_hostile_ok")
    if armed.get("weld_intent_hostile_ok") is True:
        out.append("map_fidelity:author_set_weld_intent_hostile_ok")
    nested_m = armed.get("map_fidelity_hostile")
    if isinstance(nested_m, dict) and nested_m.get("ok") is True:
        out.append("map_fidelity:author_set_map_fidelity_hostile")
    nested_w = armed.get("weld_intent_hostile")
    if isinstance(nested_w, dict) and nested_w.get("ok") is True:
        out.append("map_fidelity:author_set_weld_intent_hostile")
    return out


def _behavior_key_catalog_violations(
    vault_root: Path,
    armed: dict[str, Any],
    keys_list: list[str],
) -> list[str]:
    """Each behavior_key needs exactly one existing catalog id."""
    violations: list[str] = []
    checks = armed.get("behavior_key_checks")
    if not isinstance(checks, dict):
        checks = {}
    pid = str(armed.get("project_id") or "").strip()
    probes = _load_proof_catalog_probes(vault_root, pid)
    key_set = {str(x).strip() for x in keys_list if str(x).strip()}
    for key in keys_list:
        k = str(key).strip()
        if not k:
            continue
        if k not in checks:
            violations.append(f"map_fidelity:behavior_key_missing_check:{k}")
            continue
        cid = str(checks.get(k) or "").strip()
        if not cid:
            violations.append(f"map_fidelity:behavior_key_empty_probe_id:{k}")
            continue
        if probes is None or cid not in probes:
            violations.append(f"map_fidelity:behavior_key_probe_missing:{k}:{cid}")
    for ck in checks:
        cks = str(ck).strip()
        if cks and cks not in key_set:
            violations.append(f"map_fidelity:behavior_key_check_extra:{ck}")
    if key_set and (not isinstance(checks, dict) or not checks):
        violations.append("map_fidelity:behavior_key_checks_empty")
    return violations


def classify_behavior_key_role(key: str) -> str:
    """Return ``visibility`` | ``invariant`` | ``unknown`` for a behavior key."""
    k = str(key or "").strip()
    if not k:
        return "unknown"
    # Invariant wins when both match (e.g. pointed_solid_identity_holds).
    if _INVARIANT_KEY_RE.search(k):
        return "invariant"
    if _VISIBILITY_KEY_RE.search(k):
        return "visibility"
    return "unknown"


def row_explicit_weld_tokens(row: MapTicketRow) -> set[str]:
    """Weld tokens the row explicitly declares in the **Welds** column.

    Accepts ``W1:`` / ``W1.`` line forms and bare/bold ``W1`` tokens in that
    dedicated field. Does **not** scan product_job / free Notes (a note saying
    "do not invent W1" must not authorize W1).
    """
    text = str(getattr(row, "welds", "") or "")
    found = {f"W{m.group(1)}" for m in _EXPLICIT_WELD_LINE_RE.finditer(text)}
    for m in re.finditer(r"\bW([1-9])\b", text, re.I):
        found.add(f"W{m.group(1)}")
    return found


def prefer_invented_weld_tokens(armed: dict[str, Any]) -> set[str]:
    """Weld tokens Prefer invents via welds map or W1–W9 in structural Success."""
    found: set[str] = set()
    welds = armed.get("welds")
    if isinstance(welds, dict):
        for k in welds:
            ks = str(k).strip().upper()
            if re.fullmatch(r"W[1-9]", ks):
                found.add(ks)
    structural = str(
        armed.get("structural_success") or armed.get("intent_invariant") or ""
    )
    for m in re.finditer(r"\bW([1-9])\b", structural, re.I):
        found.add(f"W{m.group(1)}")
    return found


def row_names_field_value(row: MapTicketRow, field: str, value: str) -> bool:
    """True when the map row text names this field=value (exact token, not alias)."""
    if not value:
        return False
    blob = f"{row.product_job}\n{row.welds}\n".lower()
    v = str(value).strip().lower()
    f = str(field).strip().lower()
    if v in blob and (f in blob or f"`{v}`" in blob or f"[[{v}]]" in blob):
        return True
    # Row may name the value alone when it is a ticket-scoped catalog id / scene.
    if re.search(rf"(?<![a-z0-9_-]){re.escape(v)}(?![a-z0-9_-])", blob):
        # Require field name nearby for Half-B machine values; bare catalog ids ok.
        if v in _HALF_B_FORBIDDEN_VALUES or f in {
            "template",
            "umbrella_ask_id",
            "prefer_class",
            "lane",
            "lane_id",
            "worldgen_entry_scene",
            "launch_scene",
        }:
            return f in blob and v in blob
        return True
    return False


def launch_scene_from_armed_fields(armed: dict[str, Any] | None) -> str:
    """Resolve launch scene from Prefer **fields** only — never scan body prose."""
    armed = armed if isinstance(armed, dict) else {}
    for key in ("launch_scene", "worldgen_entry_scene"):
        raw = armed.get(key)
        if raw is not None and str(raw).strip():
            return str(raw).strip()
    return ""


def lane_id_from_armed_fields(armed: dict[str, Any] | None) -> str:
    """Resolve lane_id from Prefer **fields** only."""
    armed = armed if isinstance(armed, dict) else {}
    for key in ("lane_id", "lane"):
        raw = armed.get(key)
        if raw is not None and str(raw).strip():
            return str(raw).strip()
    return ""

@dataclass
class MapFidelityResult:
    ok: bool
    violations: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    ticket_map_id: str = ""
    applicable: bool = False
    gate_a_applicable: bool = False
    gate_b_applicable: bool = False
    status: str = STATUS_FORMS_OK

    def as_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "status": self.status,
            "applicable": self.applicable,
            "gate_a_applicable": self.gate_a_applicable,
            "gate_b_applicable": self.gate_b_applicable,
            "ticket_map_id": self.ticket_map_id,
            "violations": list(self.violations),
            "warnings": list(self.warnings),
        }


def behavior_key_checks_empty(armed: dict[str, Any] | None) -> bool:
    if not isinstance(armed, dict):
        return True
    checks = armed.get("behavior_key_checks")
    return not isinstance(checks, dict) or len(checks) == 0


def named_missing_observer(armed: dict[str, Any] | None) -> str:
    if not isinstance(armed, dict):
        return ""
    return str(armed.get("missing_observer") or "").strip()


def is_incomplete_missing_observer_packet(armed: dict[str, Any] | None) -> bool:
    """Empty checks + named missing_observer → incomplete candidate (Gate A)."""
    return behavior_key_checks_empty(armed) and bool(named_missing_observer(armed))


def _armed_blob(armed: dict[str, Any]) -> str:
    return " ".join(
        [
            str(armed.get("ticket_map_id") or ""),
            str(armed.get("ask_id") or ""),
            str(armed.get("slice_id") or ""),
            str(armed.get("mode") or ""),
            str(armed.get("catalog_row_id") or ""),
            str(armed.get("series_id") or ""),
            str(armed.get("success_object") or ""),
        ]
    ).lower()


def _has_map_ticket_prefix(text: str) -> bool:
    low = (text or "").lower()
    return any(p in low for p in MAP_TICKET_PREFIXES)


def _has_prefer_product_marker(text: str) -> bool:
    low = (text or "").lower()
    return any(m in low for m in PREFER_PRODUCT_SLICE_MARKERS)


def armed_requires_ticket_map_fidelity(armed: dict[str, Any] | None) -> bool:
    """Gate A — mechanical MAP↔Prefer bind when a map Prefer is in play.

    Broader than WORLD/GEN alone: PLACE / VIS / LOOP / PACK / DESK ticket
    prefixes count. Prefer-product slice markers (stalberg / craft) alone do
    **not** force Gate A — those use Gate B (hostile) via
    ``armed_requires_hostile_prefer`` until a ``ticket_map_id`` is armed.
    """
    if not isinstance(armed, dict) or not armed:
        return False
    if str(armed.get("ticket_map_id") or "").strip():
        return True
    prefer_on = bool(
        armed.get("prefer_authorship") or armed.get("prefer_concept_required")
    )
    # ask_id / mode may already be map-shaped (PLACE-coast, GEN-terrain, …)
    ask_or_mode = " ".join(
        [
            str(armed.get("ask_id") or ""),
            str(armed.get("mode") or ""),
            str(armed.get("ticket_map_id") or ""),
        ]
    )
    if prefer_on and _has_map_ticket_prefix(ask_or_mode):
        return True
    mode = str(armed.get("mode") or "").lower()
    if _has_map_ticket_prefix(mode) and prefer_on:
        return True
    return False


def armed_requires_hostile_prefer(armed: dict[str, Any] | None) -> bool:
    """Gate B — hostile Prefer required for any Prefer-applicable product slice.

    Aligns with ``slice_requires_prefer_authorship``: Prefer flags, ticket-map
    Prefer, or Prefer-product markers (PLACE / craft / stalberg / worldgen).
    """
    if not isinstance(armed, dict) or not armed:
        return False
    if armed.get("prefer_authorship") or armed.get("prefer_concept_required"):
        return True
    if armed_requires_ticket_map_fidelity(armed):
        return True
    blob = _armed_blob(armed)
    if _has_prefer_product_marker(blob) or _has_map_ticket_prefix(blob):
        # Product slice markers without Prefer flag still need hostile before
        # any Success claim that reaches this seat with an armed packet.
        return bool(
            armed.get("claim_class") is not None or armed.get("success_object")
        )
    return False


def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "").strip().lower())


# Content tokens for sibling-overlap (map-generic; no product word lists).
_STOPWORDS: frozenset[str] = frozenset(
    {
        "a",
        "an",
        "the",
        "and",
        "or",
        "of",
        "to",
        "in",
        "on",
        "at",
        "for",
        "as",
        "is",
        "be",
        "by",
        "with",
        "from",
        "that",
        "this",
        "these",
        "those",
        "when",
        "while",
        "where",
        "which",
        "who",
        "whom",
        "into",
        "onto",
        "over",
        "under",
        "than",
        "then",
        "them",
        "they",
        "their",
        "there",
        "here",
        "have",
        "has",
        "had",
        "having",
        "been",
        "being",
        "will",
        "can",
        "could",
        "should",
        "would",
        "may",
        "might",
        "must",
        "does",
        "did",
        "doing",
        "done",
        "not",
        "no",
        "nor",
        "only",
        "also",
        "both",
        "each",
        "every",
        "any",
        "all",
        "same",
        "other",
        "another",
        "such",
        "via",
        "per",
        "its",
        "it",
        "one",
        "two",
        "gm",
        "player",
        "foundation",
        "weld",
        "prep",
        "without",
        "within",
        "across",
        "against",
        "during",
        "after",
        "before",
        "between",
        "using",
        "used",
        "use",
        "able",
        "allowed",
        "still",
        "keep",
        "keeps",
        "kept",
        "open",
        "opens",
        "make",
        "makes",
        "made",
        "see",
        "sees",
        "seen",
        "read",
        "reads",
        "readable",
    }
)


def content_tokens(text: str) -> frozenset[str]:
    """Significant lowercase tokens for overlap (len>3, not stopwords)."""
    words = re.findall(r"[a-z0-9][a-z0-9_-]{3,}", _norm(text))
    return frozenset(w for w in words if w not in _STOPWORDS)


def jaccard_overlap(a: str, b: str) -> float:
    ta, tb = content_tokens(a), content_tokens(b)
    if not ta or not tb:
        return 0.0
    inter = len(ta & tb)
    union = len(ta | tb)
    return inter / union if union else 0.0


def claim_text_from_armed(armed: dict[str, Any]) -> str:
    """Prefer claim surface for sibling checks (success + behavior keys)."""
    parts = [
        str(armed.get("structural_success") or armed.get("intent_invariant") or ""),
        str(armed.get("success_object") or ""),
    ]
    keys = armed.get("behavior_keys") or armed.get("prefer_behavior_keys") or []
    if isinstance(keys, (list, tuple)):
        parts.extend(str(k) for k in keys)
    elif isinstance(keys, str):
        parts.append(keys)
    return " ".join(parts)


def sibling_job_consume_violations(
    claim: str,
    own_job: str,
    open_siblings: dict[str, MapTicketRow],
    *,
    prefix: str = "map_fidelity:job_consumes_sibling",
) -> list[str]:
    """Fail when claim overlaps a sibling open job more than its own job."""
    own_score = jaccard_overlap(claim, own_job)
    violations: list[str] = []
    for sid, srow in sorted(open_siblings.items()):
        sib_score = jaccard_overlap(claim, srow.product_job)
        # Strict: sibling beat own. Also catch near-ties when sibling is rich
        # and own_score is weak (claim barely binds this row).
        if sib_score > own_score + 1e-9:
            violations.append(f"{prefix}:{sid}")
        elif sib_score >= 0.22 and own_score < 0.12 and sib_score >= own_score:
            violations.append(f"{prefix}:{sid}")
    return violations


def behavior_key_sibling_violations(
    keys: list[str],
    own_job: str,
    open_siblings: dict[str, MapTicketRow],
) -> list[str]:
    """Each behavior key must match this job better than any sibling job."""
    violations: list[str] = []
    for key in keys:
        k = str(key).strip()
        if not k:
            continue
        # Meta keys never count as stranger-watchable product evidence.
        meta = {
            "file_exists",
            "compiles",
            "menu_opens",
            "contract_bound",
            "meta_written",
            "hotkey_bound",
            "play_path_matches_prefer_success",
            "prefer_refuses_not_violated_in_live",
        }
        if k.lower() in meta:
            violations.append(f"map_fidelity:behavior_key_meta:{k}")
            continue
        own_score = jaccard_overlap(k.replace("_", " "), own_job)
        for sid, srow in sorted(open_siblings.items()):
            sib_score = jaccard_overlap(k.replace("_", " "), srow.product_job)
            if sib_score > own_score + 1e-9 and sib_score >= 0.15:
                violations.append(f"map_fidelity:behavior_key_consumes_sibling:{sid}:{k}")
    return violations


def _proof_tokens(welds: str) -> list[str]:
    """Extract W1 / W2 … tokens when the map row actually lists them."""
    tokens: list[str] = []
    for m in re.finditer(r"\bW[1-9]\b", welds or "", re.I):
        tokens.append(m.group(0).upper())
    return tokens


def _hostile_ok(
    prefer_result: dict[str, Any] | None,
    *,
    armed: dict[str, Any] | None = None,
) -> bool:
    """True only for Trinity-stored Cursor senior B₁. Author/harness_b1 ignored."""
    from .prefer_senior_gates import senior_pass_ok

    return senior_pass_ok(prefer_result, gate="b1", armed=armed)


def _run_gate_a_mechanical(
    vault_root: Path,
    armed: dict[str, Any],
    *,
    map_rel: str | None,
    tid: str,
    violations: list[str],
    include_catalog: bool = True,
) -> str:
    """Gate A forms only. Mutate violations; return resolved ticket_map_id.

    When ``include_catalog`` is False, skip behavior_key catalog / empty-check
    (incomplete short-circuit path).
    """
    from .observe_class import (
        OBSERVE_VALUES,
        claim_class_for_observe,
        proof_shape_for_observe,
    )

    violations.extend(_author_set_hostile_bits(armed))

    if not tid:
        violations.append("map_fidelity:missing_ticket_map_id")
        return ""

    resolved_rel = map_rel or resolve_active_ticket_map_rel(
        vault_root, ticket_map_id=tid
    )
    rows = load_ticket_map_rows(
        vault_root, map_rel=resolved_rel, ticket_map_id=tid
    )
    if not rows:
        violations.append("map_fidelity:ticket_map_unreadable_or_missing")
        return tid

    row = rows.get(tid)
    if row is None:
        alt = tid.replace("_", "-")
        row = rows.get(alt)
    if row is None:
        violations.append(f"map_fidelity:ticket_map_id_not_on_map:{tid}")
        return tid
    tid = row.ticket_map_id

    if (row.status or "").lower() != SELECTABLE_TICKET_STATUS:
        violations.append(f"map_fidelity:ticket_map_id_not_open:{tid}")

    observe = str(getattr(row, "observe", "") or "").strip().lower()
    if observe not in OBSERVE_VALUES:
        violations.append("map_fidelity:missing_or_invalid_observe")

    touch = str(getattr(row, "touch", "") or "").strip().lower()
    if touch:
        from .ticket_map_schema import TOUCH_VALUES

        if touch not in TOUCH_VALUES:
            violations.append(f"map_fidelity:invalid_touch:{touch}")
        else:
            expect_touch = "f5" if observe == "person" else (
                "none" if observe == "record" else ""
            )
            if expect_touch and touch != expect_touch:
                violations.append(
                    f"map_fidelity:touch_observe_mismatch:{touch}:{observe}"
                )

    structural = str(
        armed.get("structural_success") or armed.get("intent_invariant") or ""
    ).strip()
    job = str(row.product_job or "").strip()
    if structural != job:
        violations.append("map_fidelity:structural_success_not_verbatim_product_job")

    expected_oos = section_open_neighbor_ids(rows, tid)
    raw_oos = armed.get("out_of_scope_ticket_ids")
    if raw_oos is None:
        violations.append("map_fidelity:missing_out_of_scope_ticket_ids")
    else:
        if isinstance(raw_oos, str):
            got = [raw_oos.strip()] if raw_oos.strip() else []
        elif isinstance(raw_oos, (list, tuple)):
            got = sorted({str(x).strip() for x in raw_oos if str(x).strip()})
        else:
            got = []
            violations.append("map_fidelity:out_of_scope_ticket_ids_bad_type")
        if got != expected_oos:
            violations.append(
                "map_fidelity:out_of_scope_ticket_ids_mismatch:"
                + ",".join(expected_oos[:12])
            )

    proof_shape = str(armed.get("proof_shape") or "").strip().lower()
    claim = str(armed.get("claim_class") or "").strip().lower()
    expect_shape = proof_shape_for_observe(observe) if observe in OBSERVE_VALUES else None
    expect_claim = claim_class_for_observe(observe) if observe in OBSERVE_VALUES else None
    if not proof_shape:
        violations.append("map_fidelity:missing_proof_shape")
    elif expect_shape and proof_shape != expect_shape:
        violations.append(
            f"map_fidelity:proof_shape_observe_mismatch:{proof_shape}:{observe}"
        )
    if not claim:
        violations.append("map_fidelity:missing_claim_class")
    elif expect_claim and claim != expect_claim:
        violations.append(
            f"map_fidelity:claim_class_observe_mismatch:{claim}:{observe}"
        )

    keys_raw = armed.get("behavior_keys") or armed.get("prefer_behavior_keys") or []
    if isinstance(keys_raw, str):
        keys_list = [keys_raw]
    elif isinstance(keys_raw, (list, tuple)):
        keys_list = [str(x) for x in keys_raw]
    else:
        keys_list = []
    if include_catalog:
        violations.extend(_behavior_key_catalog_violations(vault_root, armed, keys_list))

    dnw = armed.get("do_not_waive") or []
    if isinstance(dnw, str):
        dnw = [dnw]
    dnw_set = {str(x) for x in dnw}
    nested = armed.get("prefer_do_not_waive") or []
    if isinstance(nested, list):
        dnw_set |= {str(x) for x in nested}
    missing = [c for c in PRODUCT_MAP_DO_NOT_WAIVE if c not in dnw_set]
    if missing:
        violations.append(
            "map_fidelity:missing_do_not_waive:" + ",".join(missing)
        )

    return tid


def run_harness_b1(
    vault_root: Path,
    armed: dict[str, Any],
    *,
    map_rel: str | None = None,
    write_result: bool = True,
) -> dict[str, Any]:
    """DEPRECATED — Python classifier is not Gate B₁.

    Does not write a launchable latch. Factory order must call
    ``prefer_senior_gates.run_senior_gate`` instead. ``write_result`` ignored.
    """
    _ = (vault_root, armed, map_rel, write_result)
    return {
        "ok": False,
        "source": "harness_b1",
        "violations": [
            "b1:python_classifier_not_authoritative",
            "b1:use_factory_order_senior_gate",
        ],
        "classes": {},
    }


def validate_armed_map_fidelity(
    vault_root: Path,
    armed: dict[str, Any] | None,
    *,
    map_rel: str | None = None,
    prefer_result: dict[str, Any] | None = None,
    require_hostile_for_keep: bool = True,
) -> MapFidelityResult:
    """Gate A (forms) + Gate B₁ latch read. Incomplete is not a pass."""
    gate_a = armed_requires_ticket_map_fidelity(armed)
    gate_b = armed_requires_hostile_prefer(armed)
    if not gate_a and not gate_b:
        return MapFidelityResult(True, applicable=False, status=STATUS_FORMS_OK)

    assert isinstance(armed, dict)
    violations: list[str] = []
    warnings: list[str] = []
    tid = str(armed.get("ticket_map_id") or "").strip()
    incomplete_candidate = is_incomplete_missing_observer_packet(armed)

    if gate_a:
        # Incomplete short-circuit: skip catalog empty-check / allowlist so
        # Ticketment is not pushed to shop stubs to clear a red.
        tid = _run_gate_a_mechanical(
            vault_root,
            armed,
            map_rel=map_rel,
            tid=tid,
            violations=violations,
            include_catalog=not incomplete_candidate,
        )

    if gate_a and incomplete_candidate and not violations:
        return MapFidelityResult(
            ok=False,
            violations=[],
            warnings=sorted(set(warnings)),
            ticket_map_id=tid,
            applicable=True,
            gate_a_applicable=gate_a,
            gate_b_applicable=gate_b,
            status=STATUS_INCOMPLETE_MISSING_OBSERVER,
        )

    claim = str(armed.get("claim_class") or "").strip().lower()
    hostile_ok = _hostile_ok(prefer_result, armed=armed)
    if (
        require_hostile_for_keep
        and gate_b
        and claim in _SUCCESS_CLAIM_CLASSES
        and not incomplete_candidate
    ):
        if not hostile_ok:
            violations.append(
                "map_fidelity:hostile_prefer_required_before_success"
            )

    status = STATUS_FORMS_OK if not violations else STATUS_FORMS_FAIL
    return MapFidelityResult(
        ok=not violations,
        violations=sorted(set(violations)),
        warnings=sorted(set(warnings)),
        ticket_map_id=tid,
        applicable=True,
        gate_a_applicable=gate_a,
        gate_b_applicable=gate_b,
        status=status,
    )


def load_prefer_result(
    vault_root: Path,
    slice_id: str,
    *,
    project_id: str | None = None,
) -> dict[str, Any] | None:
    if not slice_id:
        return None
    from .bindings import factory_drb_rel

    candidates: list[Path] = []
    pid = str(project_id or "").strip()
    if pid:
        candidates.append(
            vault_root
            / factory_drb_rel(pid, "slice-briefs", f"{slice_id}.prefer-result.json")
        )
    else:
        # Fail soft: search under any project's slice-briefs (no baked slug).
        root = vault_root / "1-Projects"
        if root.is_dir():
            for proj in root.iterdir():
                if not proj.is_dir():
                    continue
                candidates.append(
                    proj
                    / "Factory-DRB"
                    / "slice-briefs"
                    / f"{slice_id}.prefer-result.json"
                )
    for p in candidates:
        if p.is_file():
            try:
                data = json.loads(p.read_text(encoding="utf-8"))
                return data if isinstance(data, dict) else None
            except (OSError, json.JSONDecodeError):
                return None
    return None


def load_armed_yaml(path: Path) -> dict[str, Any]:
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    return raw if isinstance(raw, dict) else {}


def keep_latch_allowed(
    vault_root: Path,
    armed: dict[str, Any],
    *,
    prefer_result: dict[str, Any] | None = None,
    operator_f5_ok: bool = False,
    evidence_pack: dict[str, Any] | None = None,
) -> MapFidelityResult:
    """Gate C/D helper — KEEP only if mechanical A (when map) + B₁ + B₂ (when welded) + F5.

    Operator F5 validates intended behavior/feel — not mechanical Prefer shape.
    Post-weld / greenlit KEEP also requires Gate B₂ behavior evidence (not stamp alone).
    """
    pr = prefer_result
    if pr is None:
        pr = load_prefer_result(vault_root, str(armed.get("slice_id") or ""))
    armed_keep = dict(armed)
    armed_keep["claim_class"] = "ask_success"
    result = validate_armed_map_fidelity(
        vault_root, armed_keep, prefer_result=pr, require_hostile_for_keep=True
    )
    if not operator_f5_ok:
        result.violations.append("map_fidelity:operator_f5_required_for_keep")
        result.ok = False

    # Gate B₂ — when LIVE weld / greenlit claimed, KEEP needs behavior evidence.
    from .prefer_weld_intent import (
        claims_factory_greenlit,
        extract_chat_receipt_blob,
        live_weld_claimed,
        scan_chat_hotfix_receipt,
        validate_weld_intent_latch,
    )

    if live_weld_claimed(armed_keep, pr) or claims_factory_greenlit(armed_keep, pr):
        chat = extract_chat_receipt_blob(armed_keep, pr)
        if isinstance(chat, str) and chat.strip():
            chat_scan = scan_chat_hotfix_receipt(
                chat,
                prefer_result=pr,
                armed=armed_keep,
                evidence_pack=evidence_pack,
            )
            if chat_scan.applicable and chat_scan.violations:
                result.violations.extend(chat_scan.violations)
                result.ok = False
        receipt_dict = chat if isinstance(chat, dict) else None
        b2 = validate_weld_intent_latch(
            armed_keep,
            prefer_result=pr,
            receipt=receipt_dict,
            evidence_pack=evidence_pack,
            vault_root=vault_root,
        )
        if b2.applicable and b2.violations:
            result.violations.extend(b2.violations)
            result.ok = False
        result.violations = sorted(set(result.violations))
    return result
