"""Schedule planes configuration — merged live config + curator-knobs overrides."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .merged_config import load_merged_yaml_blocks
from .pseudo_clock import load_knobs


@dataclass(frozen=True)
class GraduationPromotion:
    name: str
    requires: dict[str, Any]
    sets: dict[str, Any]
    rollback_on: dict[str, Any]


@dataclass(frozen=True)
class SchedulePlanesConfig:
    listener_enabled: bool = True
    scheduled_enabled: bool = True
    reactive_enabled: bool = True
    graduation_enabled: bool = False
    graduation_apply_enabled: bool = False
    maintain_wrap_every_n_ticks: int = 24
    memory_compact_every_n_eats: int = 10
    skill_gap_scan_max_per_day: int = 1
    maintain_wrap_streak_min: int = 3
    graduation_promotions: tuple[GraduationPromotion, ...] = ()


DEFAULT_LLM_APPLY_PROMOTION = GraduationPromotion(
    name="llm_apply_global",
    requires={
        "trial_gate.recommend_global_flip": True,
        "type2.pass_gate_ok": True,
        "charter.charter_aligned": True,
        "maintain_wrap_streak_min": 3,
    },
    sets={
        "trinity_corps_conduct_repair_auto_apply_enabled": True,
        "trinity_corps_llm_repair_host_apply_enabled": True,
    },
    rollback_on={
        "type2.pass_gate_ok": False,
        "charter.charter_aligned": False,
    },
)


def _coerce_bool(val: Any, default: bool) -> bool:
    if isinstance(val, bool):
        return val
    if isinstance(val, str):
        return val.lower() in ("true", "yes", "1")
    return default


def _coerce_int(val: Any, default: int) -> int:
    try:
        return int(val)
    except (TypeError, ValueError):
        return default


def _parse_promotion(row: dict[str, Any]) -> GraduationPromotion | None:
    name = str(row.get("name") or "").strip()
    if not name:
        return None
    requires = row.get("requires") if isinstance(row.get("requires"), dict) else {}
    sets = row.get("sets") if isinstance(row.get("sets"), dict) else {}
    rollback = row.get("rollback_on") if isinstance(row.get("rollback_on"), dict) else {}
    return GraduationPromotion(name=name, requires=dict(requires), sets=dict(sets), rollback_on=dict(rollback))


def _knobs_schedule_block(knobs: dict[str, Any]) -> dict[str, Any]:
    block = knobs.get("schedule_planes")
    if isinstance(block, dict):
        return block
    out: dict[str, Any] = {}
    prefix = "schedule_"
    for key, val in knobs.items():
        if isinstance(key, str) and key.startswith(prefix):
            out[key[len(prefix) :]] = val
    return out


def load_schedule_planes_config(vault_root: Path) -> SchedulePlanesConfig:
    vault_root = vault_root.resolve()
    blocks = load_merged_yaml_blocks(vault_root)
    sp = blocks.get("schedule_planes")
    if not isinstance(sp, dict):
        sp = {}
    knobs = load_knobs(vault_root)
    sp = {**sp, **_knobs_schedule_block(knobs)}

    grad_block = sp.get("graduation")
    if not isinstance(grad_block, dict):
        grad_block = {}

    promotions: list[GraduationPromotion] = []
    raw_promos = grad_block.get("promotions")
    if isinstance(raw_promos, list):
        for row in raw_promos:
            if isinstance(row, dict):
                p = _parse_promotion(row)
                if p:
                    promotions.append(p)
    if not promotions and grad_block.get("llm_apply_global") is not False:
        promotions.append(DEFAULT_LLM_APPLY_PROMOTION)

    return SchedulePlanesConfig(
        listener_enabled=_coerce_bool(sp.get("listener_enabled"), True),
        scheduled_enabled=_coerce_bool(sp.get("scheduled_enabled"), True),
        reactive_enabled=_coerce_bool(sp.get("reactive_enabled"), True),
        graduation_enabled=_coerce_bool(sp.get("graduation_enabled"), False),
        graduation_apply_enabled=_coerce_bool(
            grad_block.get("apply_enabled", sp.get("graduation_apply_enabled")),
            False,
        ),
        maintain_wrap_every_n_ticks=_coerce_int(sp.get("maintain_wrap_every_n_ticks"), 24),
        memory_compact_every_n_eats=_coerce_int(
            sp.get("memory_compact_every_n_eats"),
            _coerce_int(knobs.get("memory_compact_after_eat_completions"), 10),
        ),
        skill_gap_scan_max_per_day=_coerce_int(sp.get("skill_gap_scan_max_per_day"), 1),
        maintain_wrap_streak_min=_coerce_int(
            grad_block.get("maintain_wrap_streak_min", sp.get("maintain_wrap_streak_min")),
            3,
        ),
        graduation_promotions=tuple(promotions),
    )
