"""Phase 13 — MVL meta lens loader (locked trinity_prompt_context → conductor).

Read-only: loads locked maintenance-core meta YAML for Pull / Route / Query faces.
Host-agnostic bundles; no vault writes.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path
from typing import Any

from .config import load_trinity_config
from .trinity_card import get_conceptual, get_rules, get_touch
from .trinity_card_paths import load_trinity_card

PROMPT_CONTEXT_ID = "trinity_prompt_context"

_DEFAULT_META_PREPEND: tuple[str, ...] = (
    "conceptual_style_guide",
    "trinity_card_authoring",
    "trinity_prompt_context",
)

_DEFAULT_PULL_LEGS: dict[str, frozenset[str]] = {
    "conceptual_regen": frozenset({"touch", "rules", "conceptual_draft"}),
    "conduct_repair": frozenset({"touch", "rules", "contract", "conceptual_outcome"}),
    "generator_emit": frozenset({"touch", "rules", "conceptual", "contract"}),
    "audit_readonly": frozenset({"conceptual", "touch", "rules", "contract"}),
    "queue_recovery": frozenset({"touch", "rules", "contract"}),
    "acceptance_audit": frozenset({"touch", "contract"}),
    "regen_burn": frozenset({"touch", "rules", "contract"}),
    "roadmap_continue": frozenset({"touch", "rules", "conceptual"}),
    "weave_cycle": frozenset(),
    "architect_packet": frozenset(),
    "curator_capture": frozenset(),
    "prompt_crafter": frozenset({"touch"}),
    "weave_query": frozenset(),
    "redesign_factory": frozenset({"touch", "rules", "contract", "conceptual"}),
    "expand_self": frozenset({"touch", "rules", "contract"}),
    "unknown": frozenset({"touch"}),
}

_DEFAULT_FORBIDDEN: tuple[str, ...] = (
    "whole_vault_dump",
    "unrelated_trinity_ids",
    "green_wash_import_only",
    "deleted_asserts",
    "edit_outside_write_contract",
)


def _parse_leg_set(raw: Any) -> frozenset[str]:
    if raw is None:
        return frozenset()
    if isinstance(raw, str):
        parts = [p.strip() for p in raw.replace(",", " ").split() if p.strip()]
        return frozenset(parts)
    if isinstance(raw, (list, tuple)):
        return frozenset(str(x).strip() for x in raw if str(x).strip())
    return frozenset()


@dataclass(frozen=True)
class LensContract:
    """Resolved meta-lens contract from locked trinity_prompt_context."""

    meta_prepend_order: tuple[str, ...]
    task_meta_faces: dict[str, tuple[str, ...]]
    pull_leg_inclusion: dict[str, frozenset[str]]
    query_leg_inclusion: dict[str, frozenset[str]]
    forbidden: tuple[str, ...]
    query_kinds: tuple[str, ...]
    source: str  # locked | fallback

    def meta_prepend_for(self, task_kind: str) -> list[str]:
        kind = str(task_kind or "unknown").strip() or "unknown"
        out: list[str] = []
        seen: set[str] = set()
        for mid in self.meta_prepend_order:
            if mid not in seen:
                seen.add(mid)
                out.append(mid)
        for mid in self.task_meta_faces.get(kind, ()):
            if mid not in seen:
                seen.add(mid)
                out.append(mid)
        return out

    def pull_legs_for(self, task_kind: str) -> frozenset[str]:
        kind = str(task_kind or "unknown").strip() or "unknown"
        if kind in self.pull_leg_inclusion:
            return self.pull_leg_inclusion[kind]
        return _DEFAULT_PULL_LEGS.get(kind, _DEFAULT_PULL_LEGS["unknown"])

    def query_legs_for(self, query_kind: str) -> frozenset[str]:
        qk = str(query_kind or "").strip()
        if qk in self.query_leg_inclusion:
            return self.query_leg_inclusion[qk]
        if qk == "weave_query":
            return frozenset({"conceptual_outcome", "rules"})
        return frozenset({"touch", "rules"})


def _contract_from_card(card: dict[str, Any]) -> LensContract:
    touch = card.get("touch") if isinstance(card.get("touch"), dict) else {}
    rules = card.get("rules") if isinstance(card.get("rules"), dict) else {}

    prepend_raw = rules.get("meta_prepend_order") or touch.get("meta_prepend_order")
    if isinstance(prepend_raw, list) and prepend_raw:
        meta_prepend = tuple(str(x).strip() for x in prepend_raw if str(x).strip())
    else:
        meta_prepend = _DEFAULT_META_PREPEND

    faces_raw = touch.get("task_meta_faces") or {}
    task_meta_faces: dict[str, tuple[str, ...]] = {}
    if isinstance(faces_raw, dict):
        for k, v in faces_raw.items():
            if isinstance(v, list):
                task_meta_faces[str(k)] = tuple(str(x).strip() for x in v if str(x).strip())

    pull_raw = rules.get("pull_leg_inclusion") or {}
    pull: dict[str, frozenset[str]] = dict(_DEFAULT_PULL_LEGS)
    if isinstance(pull_raw, dict):
        for k, v in pull_raw.items():
            pull[str(k)] = _parse_leg_set(v)

    query_raw = rules.get("query_leg_inclusion") or {}
    query: dict[str, frozenset[str]] = {}
    if isinstance(query_raw, dict):
        for k, v in query_raw.items():
            query[str(k)] = _parse_leg_set(v)

    forbidden_raw = rules.get("forbidden") or []
    forbidden: list[str] = list(_DEFAULT_FORBIDDEN)
    if isinstance(forbidden_raw, list):
        for item in forbidden_raw:
            s = str(item).strip()
            if s and s not in forbidden:
                forbidden.append(s)

    qk_raw = touch.get("query_kinds") or {}
    query_kinds: tuple[str, ...] = ()
    if isinstance(qk_raw, dict):
        query_kinds = tuple(str(k).strip() for k in qk_raw if str(k).strip())

    return LensContract(
        meta_prepend_order=meta_prepend,
        task_meta_faces=task_meta_faces,
        pull_leg_inclusion=pull,
        query_leg_inclusion=query,
        forbidden=tuple(forbidden),
        query_kinds=query_kinds,
        source="locked",
    )


def _fallback_contract() -> LensContract:
    return LensContract(
        meta_prepend_order=_DEFAULT_META_PREPEND,
        task_meta_faces={},
        pull_leg_inclusion=dict(_DEFAULT_PULL_LEGS),
        query_leg_inclusion={},
        forbidden=_DEFAULT_FORBIDDEN,
        query_kinds=(),
        source="fallback",
    )


@lru_cache(maxsize=4)
def _cached_lens(vault_root_s: str, card_mtime_ns: int) -> LensContract:
    vault_root = Path(vault_root_s)
    try:
        card = load_trinity_card(vault_root, PROMPT_CONTEXT_ID, prefer="locked")
        return _contract_from_card(card)
    except (OSError, ValueError, FileNotFoundError):
        return _fallback_contract()


def get_lens_contract(vault_root: Path) -> LensContract:
    """Load MVL lens contract; cache invalidates when locked card mtime changes."""
    vault_root = vault_root.resolve()
    card_path = vault_root / ".technical" / "weave" / "components" / f"{PROMPT_CONTEXT_ID}.yaml"
    mtime_ns = card_path.stat().st_mtime_ns if card_path.is_file() else 0
    return _cached_lens(str(vault_root), mtime_ns)


def load_meta_lens_legs(
    vault_root: Path,
    meta_ids: list[str],
    *,
    max_ids: int = 12,
) -> dict[str, Any]:
    """Lightweight meta summaries for conductor prepend (read-only)."""
    vault_root = vault_root.resolve()
    out: dict[str, Any] = {}
    for mid in meta_ids[:max_ids]:
        try:
            card = load_trinity_card(vault_root, mid, prefer="locked")
        except (OSError, ValueError, FileNotFoundError):
            try:
                card = load_trinity_card(vault_root, mid, prefer="provisional")
            except (OSError, ValueError, FileNotFoundError):
                out[mid] = {"error": "meta_card_not_found"}
                continue
        con = get_conceptual(card)
        out[mid] = {
            "outcome": con.get("outcome"),
            "summary": con.get("summary"),
            "frame_anchor": con.get("frame_anchor"),
        }
    return out


def resolve_config_slice(vault_root: Path) -> dict[str, Any]:
    """Resolved weave/trinity config knobs for conductor (read-only)."""
    vault_root = vault_root.resolve()
    cfg = load_trinity_config(vault_root)
    return {
        "trinity_enabled": cfg.enabled,
        "corps_self_wrap_full_corpus": cfg.corps_self_wrap_full_corpus,
        "corps_proof_adequacy_strict": cfg.corps_proof_adequacy_strict,
        "weave_self_wrap_enabled": cfg.weave_self_wrap_enabled,
        "mvl_conductor_enabled": getattr(cfg, "mvl_conductor_enabled", True),
        "lens_informed_align_enabled": getattr(cfg, "lens_informed_align_enabled", True),
        "trinity_meta_corpus_enabled": getattr(cfg, "meta_corpus_enabled", False),
        "trinity_meta_corpus_charter_enabled": getattr(
            cfg, "meta_corpus_charter_enabled", False
        ),
        "trinity_queue_payload_meta_deferred": getattr(
            cfg, "queue_payload_meta_deferred", True
        ),
    }


@dataclass
class MvlConductorBundle:
    """Host-agnostic MVL bundle: lens + meta legs + target card legs + config slice."""

    trinity_id: str
    task_kind: str
    lens_source: str
    meta_prepend: list[str]
    meta_legs: dict[str, Any]
    legs: dict[str, Any]
    config_slice: dict[str, Any]
    forbidden: list[str]
    write_scope: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "trinity_id": self.trinity_id,
            "task_kind": self.task_kind,
            "lens_source": self.lens_source,
            "meta_prepend": self.meta_prepend,
            "meta_legs": self.meta_legs,
            "legs": self.legs,
            "config_slice": self.config_slice,
            "forbidden": self.forbidden,
            "write_scope": self.write_scope,
        }


def probe_mvl_lens(vault_root: Path) -> dict[str, Any]:
    """Self-wrap health check — lens loads and key meta cards resolve."""
    vault_root = vault_root.resolve()
    lens = get_lens_contract(vault_root)
    cfg = load_trinity_config(vault_root)
    if not getattr(cfg, "mvl_conductor_enabled", True):
        return {"ok": True, "skipped": True, "reason": "mvl_conductor_disabled"}

    required_meta = list(lens.meta_prepend_order)
    missing: list[str] = []
    for mid in required_meta:
        try:
            load_trinity_card(vault_root, mid, prefer="locked")
        except (OSError, ValueError, FileNotFoundError):
            missing.append(mid)

    sample_kinds = ("acceptance_audit", "regen_burn", "conduct_repair", "weave_query")
    prepend_samples = {k: lens.meta_prepend_for(k) for k in sample_kinds}

    return {
        "ok": len(missing) == 0,
        "lens_source": lens.source,
        "meta_prepend_order": list(lens.meta_prepend_order),
        "query_kinds": list(lens.query_kinds),
        "missing_meta_cards": missing,
        "prepend_samples": prepend_samples,
        "config_slice": resolve_config_slice(vault_root),
    }
