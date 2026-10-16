"""Ticket-map Prefer fidelity — mechanical Gate A + hostile Gate B latch.

Prefer Success must equal the ticket MAP row's product job + weld proofs when a
map row is armed. Mechanical harness catches missing fields, deny-listed
success_object, and incomplete do_not_waive.

Hostile Prefer (Gate B) is required on **every** Prefer-applicable Success
claim — staging **and** KEEP. Mechanical-shape alone must never green.

Cite: Prefer-Authorship-Host-Law §C.3 · World-Builder-Mini-Game-Ticket-Map.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

DEFAULT_TICKET_MAP_REL = (
    "1-Projects/genesis-mythos-master/Factory-DRB/World-Builder-Mini-Game-Ticket-Map.md"
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
)
# Back-compat alias for callers / tests.
WORLD_GEN_MAP_DO_NOT_WAIVE: tuple[str, ...] = PRODUCT_MAP_DO_NOT_WAIVE

SUCCESS_OBJECT_DENY: tuple[str, ...] = (
    "contract_bound",
    "meta_written",
    "hotkey_bound",
    "map_job_name_only",
    "stub_ok",
    "chrome_only",
)

# Ticket-map id / mode prefixes — WORLD/GEN plus PLACE / craft / VIS / LOOP / PACK / DESK.
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
)

# Align with prefer_authorship_contract.WORLDGEN_SLICE_MARKERS + PLACE / craft / dual.
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
        "keep",
        "keep_real",
        "success",
        "staging",
        "staging_awaiting_f5",
        "staging_incomplete",
        "",
    }
)

_TICKET_ROW_RE = re.compile(
    r"^\|\s*`(?P<id>[A-Za-z0-9][A-Za-z0-9_-]*)`(?:\s*\([^)]*\))?\s*\|"
    r"\s*(?P<job>[^|]*?)\s*\|"
    r"\s*(?P<welds>[^|]*?)\s*\|\s*$",
    re.M,
)


@dataclass
class MapTicketRow:
    ticket_map_id: str
    product_job: str
    welds: str

    @property
    def proof_blob(self) -> str:
        return f"{self.product_job} {self.welds}".strip()


@dataclass
class MapFidelityResult:
    ok: bool
    violations: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    ticket_map_id: str = ""
    applicable: bool = False
    gate_a_applicable: bool = False
    gate_b_applicable: bool = False

    def as_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "applicable": self.applicable,
            "gate_a_applicable": self.gate_a_applicable,
            "gate_b_applicable": self.gate_b_applicable,
            "ticket_map_id": self.ticket_map_id,
            "violations": list(self.violations),
            "warnings": list(self.warnings),
        }


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


def parse_ticket_map_rows(map_text: str) -> dict[str, MapTicketRow]:
    """Parse markdown table rows with ticket id in backticks (3+ columns)."""
    rows: dict[str, MapTicketRow] = {}
    for m in _TICKET_ROW_RE.finditer(map_text or ""):
        tid = m.group("id").strip()
        job = " ".join(m.group("job").split())
        welds = " ".join(m.group("welds").split())
        # Skip pure fidelity tables that repeat id without a real job
        if job.lower() in {"product job", "fidelity", "was", "now", "ticket"}:
            continue
        rows[tid] = MapTicketRow(ticket_map_id=tid, product_job=job, welds=welds)
    return rows


def load_ticket_map_rows(
    vault_root: Path, *, map_rel: str | None = None
) -> dict[str, MapTicketRow]:
    rel = (map_rel or DEFAULT_TICKET_MAP_REL).strip().lstrip("/")
    path = vault_root / rel
    if not path.is_file():
        return {}
    return parse_ticket_map_rows(path.read_text(encoding="utf-8", errors="replace"))


def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "").strip().lower())


def _proof_tokens(welds: str) -> list[str]:
    """Extract W1 / W2 … tokens and a few keywords for containment checks."""
    tokens: list[str] = []
    for m in re.finditer(r"\bW[1-9]\b", welds or "", re.I):
        tokens.append(m.group(0).upper())
    for kw in (
        "generate",
        "dial",
        "height",
        "river",
        "land",
        "water",
        "control",
        "hotkey",
    ):
        if kw in (welds or "").lower():
            tokens.append(kw)
    return tokens


def _hostile_ok(prefer_result: dict[str, Any] | None) -> bool:
    if not isinstance(prefer_result, dict):
        return False
    if prefer_result.get("map_fidelity_hostile_ok") is True:
        return True
    nested = prefer_result.get("map_fidelity_hostile")
    return isinstance(nested, dict) and nested.get("ok") is True


def _run_gate_a_mechanical(
    vault_root: Path,
    armed: dict[str, Any],
    *,
    map_rel: str | None,
    tid: str,
    violations: list[str],
) -> str:
    """Mutate violations; return resolved ticket_map_id (may be empty)."""
    if not tid:
        violations.append("map_fidelity:missing_ticket_map_id")
        return ""

    rows = load_ticket_map_rows(vault_root, map_rel=map_rel)
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

    structural = str(
        armed.get("structural_success") or armed.get("intent_invariant") or ""
    )
    if len(structural.strip()) < 40:
        violations.append("map_fidelity:structural_success_too_thin")

    job_norm = _norm(row.product_job)
    struct_norm = _norm(structural)
    job_stem = re.sub(r"\*+", "", job_norm)
    job_stem = re.sub(r"^\(superseded\)\s*", "", job_stem)
    words = [w for w in job_stem.split() if len(w) > 3][:10]
    if words:
        hits = sum(1 for w in words if w in struct_norm)
        if hits < max(3, len(words) // 3):
            violations.append(
                "map_fidelity:structural_success_misses_map_product_job"
            )

    for tok in _proof_tokens(row.welds):
        if tok.startswith("W") and tok[1:].isdigit():
            if tok.lower() not in struct_norm and tok not in structural:
                welds_field = armed.get("welds")
                if isinstance(welds_field, dict) and tok in {
                    str(k).upper() for k in welds_field
                }:
                    continue
                if isinstance(welds_field, str) and tok in welds_field.upper():
                    continue
                violations.append(f"map_fidelity:missing_weld_proof:{tok}")

    so = str(armed.get("success_object") or "").strip().lower()
    if not so:
        violations.append("map_fidelity:missing_success_object")
    elif so in SUCCESS_OBJECT_DENY or any(d in so for d in SUCCESS_OBJECT_DENY):
        violations.append(f"map_fidelity:success_object_denied:{so}")

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


def validate_armed_map_fidelity(
    vault_root: Path,
    armed: dict[str, Any] | None,
    *,
    map_rel: str | None = None,
    prefer_result: dict[str, Any] | None = None,
    require_hostile_for_keep: bool = True,
) -> MapFidelityResult:
    """Gate A (mechanical) + Gate B (hostile) — binding on staging and KEEP.

    ``require_hostile_for_keep`` retained for CLI compatibility; when True,
    hostile Prefer is required for **all** Success claim classes including
    staging (mechanical-shape Success must never green).
    """
    gate_a = armed_requires_ticket_map_fidelity(armed)
    gate_b = armed_requires_hostile_prefer(armed)
    if not gate_a and not gate_b:
        return MapFidelityResult(True, applicable=False)

    assert isinstance(armed, dict)
    violations: list[str] = []
    warnings: list[str] = []
    tid = str(armed.get("ticket_map_id") or "").strip()

    if gate_a:
        # Prefer-product without explicit ticket_map_id still needs MAP bind when
        # Gate A fired via markers — missing id is a hard violation.
        tid = _run_gate_a_mechanical(
            vault_root, armed, map_rel=map_rel, tid=tid, violations=violations
        )

    # Gate B — required on staging AND KEEP. Never warning-only.
    claim = str(armed.get("claim_class") or "").strip().lower()
    hostile_ok = _hostile_ok(prefer_result)
    if require_hostile_for_keep and gate_b and claim in _SUCCESS_CLAIM_CLASSES:
        if not hostile_ok:
            violations.append(
                "map_fidelity:hostile_prefer_required_before_success"
            )

    return MapFidelityResult(
        ok=not violations,
        violations=sorted(set(violations)),
        warnings=sorted(set(warnings)),
        ticket_map_id=tid,
        applicable=True,
        gate_a_applicable=gate_a,
        gate_b_applicable=gate_b,
    )


def load_prefer_result(vault_root: Path, slice_id: str) -> dict[str, Any] | None:
    if not slice_id:
        return None
    candidates = [
        vault_root
        / "1-Projects/genesis-mythos-master/Factory-DRB/slice-briefs"
        / f"{slice_id}.prefer-result.json",
    ]
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
) -> MapFidelityResult:
    """Gate C/D helper — KEEP only if mechanical A (when map) + hostile B + operator F5.

    Operator F5 validates intended behavior/feel — not mechanical Prefer shape.
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
    return result
