"""Config loader for lightweight weave controls."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from ..config_loader import resolve_config_path


@dataclass(frozen=True)
class WeaveConfig:
    enabled: bool = True
    governance_interval_days: int = 14
    operator_max_hours_per_week: int = 10
    governance_bypass_until: str | None = None


@dataclass(frozen=True)
class TrinityConfig:
    """Wave 2.5b — Component Trinity touch refresh and alignment gates (2.5d)."""

    enabled: bool = True
    checks_enabled: bool = False
    block_on_stale_touch: bool = True
    block_on_disconnect: bool = True
    touch_refresh_on_pseudo_clock: bool = False
    pack_mandatory_on_maintenance_lane: bool = True
    max_closure_paths: int = 21
    max_closure_hops: int = 3
    run_behavior_proofs: bool = True
    catchup_on_pseudo_clock: bool = False
    catchup_max_escalations_per_run: int = 8
    curate_non_core_on_sweep: bool = True
    backlog_top_n: int = 8
    backlog_on_pseudo_clock: bool = False
    backlog_usage_weight: float = 0.05
    weave_self_wrap_enabled: bool = True
    spine_enforcement_strict: bool = True
    clog_pass_before_board: bool = True
    weave_self_wrap_on_pseudo_clock: bool = False
    stale_inflight_max_minutes: float = 180.0
    corps_sweep_enabled: bool = True
    corps_sweep_before_enforce: bool = True
    corps_sweep_auto_hygiene: bool = False
    corps_nerve_test_enabled: bool = True
    corps_conduct_pending_ok: bool = False
    corps_cluster_batch_size: int = 7
    corps_self_wrap_full_corpus: bool = True
    corps_self_wrap_max_laps: int = 3
    corps_max_laps: int = 3
    corps_max_llm_laps: int = 2
    corps_auto_repair_enabled: bool = True
    corps_llm_repair_enabled: bool = False
    corps_llm_repair_trial_enabled: bool = False
    corps_llm_repair_trial_max_cards_per_run: int = 7
    corps_llm_repair_trial_profiles: tuple[str, ...] = ("balance",)
    corps_llm_repair_host_apply_enabled: bool = False
    corps_llm_repair_host_apply_trial_enabled: bool = False
    corps_llm_repair_host_apply_timeout_sec: int = 300
    corps_skip_conduct_on_semantic_fail: bool = True
    corps_conduct_repair_enabled: bool = True
    corps_max_conduct_laps: int = 2
    corps_regenerate_complete_enabled: bool = False
    corps_corpus_archive_root: str = "4-Archives/Weave/Trinity-Corpus"
    corps_regenerate_require_11a: bool = True
    corps_proof_adequacy_strict: bool = False
    corps_regenerate_test_compensation_enabled: bool = True
    corps_regenerate_test_compensation_mode: str = "paired"
    corps_shared_test_surgical_adapt: bool = True
    corps_max_test_compensation_laps: int = 2
    corps_test_code_repair_enabled: bool = True
    corps_max_test_code_repair_cards: int = 12
    corps_conduct_repair_pack_enabled: bool = True
    corps_max_conduct_repair_pack_attempts: int = 1
    corps_conduct_repair_auto_apply_enabled: bool = False
    mvl_conductor_enabled: bool = True
    corps_regen_meta_lens_force_align_enabled: bool = False
    lens_informed_align_enabled: bool = True
    meta_corpus_enabled: bool = False
    meta_corpus_charter_enabled: bool = False
    meta_generation_load_ids: tuple[str, ...] = ()
    queue_payload_meta_deferred: bool = True
    host_weld_sync_enabled: bool = True
    knob_parity_enabled: bool = True
    honesty_anchor_enabled: bool = True
    redesign_factory_enabled: bool = False
    expand_self_enabled: bool = True
    usage_proven_on_pseudo_clock: bool = False
    usage_proven_min_usage_count: int = 3
    usage_proven_min_green_streak: int = 3
    usage_proven_lookback_days: int = 30
    corps_conduct_repair_auto_apply_trial_enabled: bool = False
    corps_conduct_repair_auto_apply_trial_max_per_run: int = 3


@dataclass(frozen=True)
class PredictiveConfig:
    enabled: bool = True
    calibration_valid_runs: int = 14
    calibration_max_age_days: int = 30
    enforcement_enabled: bool = False
    auto_enable_enforcement_when_ready: bool = True
    min_integrity_pass_rate_for_enforcement: float = 0.9


@dataclass(frozen=True)
class SymbolicConfig:
    enabled: bool = True
    enforcement_enabled: bool = False
    observe_only: bool = True
    auto_bootstrap_n2: bool = True


@dataclass(frozen=True)
class L3Config:
    enabled: bool = True
    rollout_phase: str = "f4"
    max_heal_attempts_per_stall: int = 2
    post_heal_verifier_required: bool = True
    require_new_evidence: bool = True
    auto_rollback_on_verifier_fail: bool = True


@dataclass(frozen=True)
class L4Config:
    enabled: bool = True
    live_apply_enabled: bool = False
    bandit_epsilon: float = 0.1
    replay_min_episodes: int = 10
    min_uplift_for_proposal: float = 0.03
    counselor_required_for_promotion: bool = True


@dataclass(frozen=True)
class L5Config:
    enabled: bool = True
    ac2_timebox_days: int = 7
    require_l3_green: bool = False
    l3_green_min_pass_rate: float = 0.8
    max_loop_iterations_per_run: int = 5
    max_consecutive_verifier_fails: int = 3
    auto_downgrade_on_instability: bool = True
    post_tick_verifier: bool = True
    # Optional secondary lane pass (plumbing only — default maintenance).
    secondary_lanes_enabled: bool = False
    secondary_lanes: tuple[str, ...] = ("maintenance",)
    secondary_eat_enabled: bool = False
    block_on_user_escalation: bool = True


def load_l5_config(vault_root: Path) -> L5Config:
    raw = _parse_weave_config(vault_root)
    sec_raw = raw.get("l5_secondary_lanes")
    if isinstance(sec_raw, list):
        secondary_lanes = tuple(str(x).strip().lower() for x in sec_raw if str(x).strip())
    else:
        secondary_lanes = ("maintenance",)
    if not secondary_lanes:
        secondary_lanes = ("maintenance",)
    return L5Config(
        enabled=bool(raw.get("l5_sandbox_enabled", True)),
        ac2_timebox_days=int(raw.get("l5_ac2_timebox_days", 7)),
        require_l3_green=bool(raw.get("l5_require_l3_green", False)),
        l3_green_min_pass_rate=float(raw.get("l5_l3_green_min_pass_rate", 0.8)),
        max_loop_iterations_per_run=int(raw.get("l5_max_loop_iterations", 5)),
        max_consecutive_verifier_fails=int(raw.get("l5_max_consecutive_verifier_fails", 3)),
        auto_downgrade_on_instability=bool(raw.get("l5_auto_downgrade_on_instability", True)),
        post_tick_verifier=bool(raw.get("l5_post_tick_verifier", True)),
        secondary_lanes_enabled=bool(raw.get("l5_secondary_lanes_enabled", False)),
        secondary_lanes=secondary_lanes,
        secondary_eat_enabled=bool(raw.get("l5_secondary_eat_enabled", False)),
        block_on_user_escalation=bool(raw.get("l5_block_on_user_escalation", True)),
    )


def load_l4_config(vault_root: Path) -> L4Config:
    raw = _parse_weave_config(vault_root)
    return L4Config(
        enabled=bool(raw.get("l4_adaptive_enabled", True)),
        live_apply_enabled=bool(raw.get("l4_live_apply_enabled", False)),
        bandit_epsilon=float(raw.get("l4_bandit_epsilon", 0.1)),
        replay_min_episodes=int(raw.get("l4_replay_min_episodes", 10)),
        min_uplift_for_proposal=float(raw.get("l4_min_uplift_for_proposal", 0.03)),
        counselor_required_for_promotion=bool(raw.get("l4_counselor_required_for_promotion", True)),
    )


def load_l3_config(vault_root: Path) -> L3Config:
    raw = _parse_weave_config(vault_root)
    phase = str(raw.get("l3_rollout_phase", "f4")).strip().lower()
    if phase not in ("f2", "f3", "f4"):
        phase = "f4"
    return L3Config(
        enabled=bool(raw.get("l3_self_heal_enabled", True)),
        rollout_phase=phase,
        max_heal_attempts_per_stall=int(raw.get("l3_max_heal_attempts_per_stall", 2)),
        post_heal_verifier_required=bool(raw.get("l3_post_heal_verifier_required", True)),
        require_new_evidence=bool(raw.get("l3_require_new_evidence", True)),
        auto_rollback_on_verifier_fail=bool(raw.get("l3_auto_rollback_on_verifier_fail", True)),
    )


def load_symbolic_config(vault_root: Path) -> SymbolicConfig:
    raw = _parse_weave_config(vault_root)
    observe = bool(raw.get("symbolic_observe_only", True))
    enforce = bool(raw.get("symbolic_enforcement_enabled", False))
    if observe:
        enforce = False
    return SymbolicConfig(
        enabled=bool(raw.get("symbolic_enabled", True)),
        enforcement_enabled=enforce,
        observe_only=observe,
        auto_bootstrap_n2=bool(raw.get("symbolic_auto_bootstrap_n2", True)),
    )


def load_predictive_config(vault_root: Path) -> PredictiveConfig:
    raw = _parse_weave_config(vault_root)
    enforcement = bool(raw.get("predictive_enforcement_enabled", False))
    auto = bool(raw.get("predictive_auto_enable_enforcement", True))
    if auto:
        cal_path = vault_root / ".technical" / "weave" / "predictive_calibration.json"
        if cal_path.is_file():
            try:
                import json

                cal_raw = json.loads(cal_path.read_text(encoding="utf-8"))
                if cal_raw.get("enforcement_ready"):
                    enforcement = True
            except (json.JSONDecodeError, OSError):
                pass
    return PredictiveConfig(
        enabled=bool(raw.get("predictive_enabled", True)),
        calibration_valid_runs=int(raw.get("predictive_calibration_valid_runs", 14)),
        calibration_max_age_days=int(raw.get("predictive_calibration_max_age_days", 30)),
        enforcement_enabled=enforcement,
        auto_enable_enforcement_when_ready=auto,
        min_integrity_pass_rate_for_enforcement=float(
            raw.get("predictive_min_integrity_pass_rate", 0.9)
        ),
    )


def skill_proposals_enabled(vault_root: Path) -> bool:
    """
    Master kill for skill-proposal spam (gap stubs, SKILL_PROPOSAL_REVIEW → lane INGEST lines).
    weave.skill_proposals_enabled in Second-Brain-Config wins; else curator-knobs auto_pilot_skills.
    """
    raw = _parse_weave_config(vault_root)
    if "skill_proposals_enabled" in raw:
        return bool(raw.get("skill_proposals_enabled"))
    try:
        from ..pseudo_clock import load_knobs

        return bool(load_knobs(vault_root).get("auto_pilot_skills", True))
    except Exception:
        return True


def load_weave_config(vault_root: Path) -> WeaveConfig:
    weave_raw = _parse_weave_config(vault_root)
    return WeaveConfig(
        enabled=bool(weave_raw.get("enabled", True)),
        governance_interval_days=int(weave_raw.get("governance_interval_days", 14)),
        operator_max_hours_per_week=int(weave_raw.get("operator_max_hours_per_week", 10)),
        governance_bypass_until=(
            str(weave_raw["governance_bypass_until"]).strip()
            if weave_raw.get("governance_bypass_until")
            else None
        ),
    )


def load_trinity_config(vault_root: Path) -> TrinityConfig:
    raw = _parse_weave_config(vault_root)
    cfg = TrinityConfig(
        enabled=bool(raw.get("trinity_enabled", True)),
        checks_enabled=bool(raw.get("trinity_checks_enabled", False)),
        block_on_stale_touch=bool(raw.get("trinity_block_on_stale_touch", True)),
        block_on_disconnect=bool(raw.get("trinity_block_on_disconnect", True)),
        touch_refresh_on_pseudo_clock=bool(raw.get("trinity_touch_refresh_on_pseudo_clock", False)),
        pack_mandatory_on_maintenance_lane=bool(
            raw.get("trinity_pack_mandatory_on_maintenance_lane", True)
        ),
        max_closure_paths=int(raw.get("trinity_max_closure_paths", 21)),
        max_closure_hops=int(raw.get("trinity_max_closure_hops", 3)),
        run_behavior_proofs=bool(raw.get("trinity_run_behavior_proofs", True)),
        catchup_on_pseudo_clock=bool(raw.get("trinity_catchup_on_pseudo_clock", False)),
        catchup_max_escalations_per_run=int(
            raw.get("trinity_catchup_max_escalations_per_run", 8)
        ),
        curate_non_core_on_sweep=bool(raw.get("trinity_curate_non_core_on_sweep", True)),
        backlog_top_n=int(raw.get("trinity_backlog_top_n", 8)),
        backlog_on_pseudo_clock=bool(raw.get("trinity_backlog_on_pseudo_clock", False)),
        backlog_usage_weight=float(raw.get("trinity_backlog_usage_weight", 0.05)),
        weave_self_wrap_enabled=bool(raw.get("trinity_weave_self_wrap_enabled", True)),
        spine_enforcement_strict=bool(raw.get("trinity_spine_enforcement_strict", True)),
        clog_pass_before_board=bool(raw.get("trinity_clog_pass_before_board", True)),
        weave_self_wrap_on_pseudo_clock=bool(
            raw.get("trinity_weave_self_wrap_on_pseudo_clock", False)
        ),
        stale_inflight_max_minutes=float(raw.get("trinity_stale_inflight_max_minutes", 180)),
        corps_sweep_enabled=bool(raw.get("trinity_corps_sweep_enabled", True)),
        corps_sweep_before_enforce=bool(raw.get("trinity_corps_sweep_before_enforce", True)),
        corps_sweep_auto_hygiene=bool(raw.get("trinity_corps_sweep_auto_hygiene", False)),
        corps_nerve_test_enabled=bool(raw.get("trinity_corps_nerve_test_enabled", True)),
        corps_conduct_pending_ok=bool(raw.get("trinity_corps_conduct_pending_ok", False)),
        corps_cluster_batch_size=int(raw.get("trinity_corps_cluster_batch_size", 7)),
        corps_self_wrap_full_corpus=bool(raw.get("trinity_corps_self_wrap_full_corpus", True)),
        corps_self_wrap_max_laps=int(raw.get("trinity_corps_self_wrap_max_laps", 3)),
        corps_max_laps=int(
            raw.get(
                "trinity_corps_max_laps",
                raw.get("trinity_corps_self_wrap_max_laps", 3),
            )
        ),
        corps_max_llm_laps=int(raw.get("trinity_corps_max_llm_laps", 2)),
        corps_auto_repair_enabled=bool(raw.get("trinity_corps_auto_repair_enabled", True)),
        corps_llm_repair_enabled=bool(raw.get("trinity_corps_llm_repair_enabled", False)),
        corps_llm_repair_trial_enabled=bool(
            raw.get("trinity_corps_llm_repair_trial_enabled", False)
        ),
        corps_llm_repair_trial_max_cards_per_run=int(
            raw.get("trinity_corps_llm_repair_trial_max_cards_per_run", 7)
        ),
        corps_llm_repair_trial_profiles=_parse_trinity_id_list(
            raw.get("trinity_corps_llm_repair_trial_profiles", "balance")
        )
        or ("balance",),
        corps_llm_repair_host_apply_enabled=bool(
            raw.get("trinity_corps_llm_repair_host_apply_enabled", False)
        ),
        corps_llm_repair_host_apply_trial_enabled=bool(
            raw.get("trinity_corps_llm_repair_host_apply_trial_enabled", False)
        ),
        corps_llm_repair_host_apply_timeout_sec=int(
            raw.get("trinity_corps_llm_repair_host_apply_timeout_sec", 300)
        ),
        corps_skip_conduct_on_semantic_fail=bool(
            raw.get("trinity_corps_skip_conduct_on_semantic_fail", True)
        ),
        corps_conduct_repair_enabled=bool(
            raw.get("trinity_corps_conduct_repair_enabled", True)
        ),
        corps_max_conduct_laps=int(raw.get("trinity_corps_max_conduct_laps", 2)),
        corps_regenerate_complete_enabled=bool(
            raw.get("trinity_corps_regenerate_complete_enabled", False)
        ),
        corps_corpus_archive_root=str(
            raw.get("trinity_corpus_archive_root", "4-Archives/Weave/Trinity-Corpus")
        ),
        corps_regenerate_require_11a=bool(
            raw.get("trinity_corps_regenerate_require_11a", True)
        ),
        corps_proof_adequacy_strict=bool(
            raw.get("trinity_corps_proof_adequacy_strict", False)
        ),
        corps_regenerate_test_compensation_enabled=bool(
            raw.get("trinity_corps_regenerate_test_compensation_enabled", True)
        ),
        corps_regenerate_test_compensation_mode=str(
            raw.get("trinity_corps_regenerate_test_compensation_mode", "paired")
        ),
        corps_shared_test_surgical_adapt=bool(
            raw.get("trinity_corps_shared_test_surgical_adapt", True)
        ),
        corps_max_test_compensation_laps=int(
            raw.get("trinity_corps_max_test_compensation_laps", 2)
        ),
        corps_test_code_repair_enabled=bool(
            raw.get("trinity_corps_test_code_repair_enabled", True)
        ),
        corps_max_test_code_repair_cards=int(
            raw.get("trinity_corps_max_test_code_repair_cards", 12)
        ),
        corps_conduct_repair_pack_enabled=bool(
            raw.get("trinity_corps_conduct_repair_pack_enabled", True)
        ),
        corps_max_conduct_repair_pack_attempts=int(
            raw.get("trinity_corps_max_conduct_repair_pack_attempts", 1)
        ),
        corps_conduct_repair_auto_apply_enabled=bool(
            raw.get("trinity_corps_conduct_repair_auto_apply_enabled", False)
        ),
        mvl_conductor_enabled=bool(raw.get("trinity_mvl_conductor_enabled", True)),
        corps_regen_meta_lens_force_align_enabled=bool(
            raw.get("trinity_corps_regen_meta_lens_force_align_enabled", False)
        ),
        lens_informed_align_enabled=bool(
            raw.get("trinity_lens_informed_align_enabled", True)
        ),
        meta_corpus_enabled=bool(raw.get("trinity_meta_corpus_enabled", False)),
        meta_corpus_charter_enabled=bool(
            raw.get("trinity_meta_corpus_charter_enabled", False)
        ),
        meta_generation_load_ids=_parse_trinity_id_list(
            raw.get("trinity_meta_generation_load_ids")
        ),
        queue_payload_meta_deferred=bool(
            raw.get("trinity_queue_payload_meta_deferred", True)
        ),
        host_weld_sync_enabled=bool(
            raw.get(
                "trinity_host_weld_sync_enabled",
                raw.get("trinity_mvl_conductor_enabled", True),
            )
        ),
        knob_parity_enabled=bool(raw.get("trinity_knob_parity_enabled", True)),
        honesty_anchor_enabled=bool(raw.get("trinity_honesty_anchor_enabled", True)),
        redesign_factory_enabled=bool(raw.get("trinity_redesign_factory_enabled", False)),
        expand_self_enabled=bool(raw.get("trinity_expand_self_enabled", True)),
        usage_proven_on_pseudo_clock=bool(
            raw.get("trinity_usage_proven_on_pseudo_clock", False)
        ),
        usage_proven_min_usage_count=int(
            raw.get("trinity_usage_proven_min_usage_count", 3)
        ),
        usage_proven_min_green_streak=int(
            raw.get("trinity_usage_proven_min_green_streak", 3)
        ),
        usage_proven_lookback_days=int(raw.get("trinity_usage_proven_lookback_days", 30)),
        corps_conduct_repair_auto_apply_trial_enabled=bool(
            raw.get("trinity_corps_conduct_repair_auto_apply_trial_enabled", False)
        ),
        corps_conduct_repair_auto_apply_trial_max_per_run=int(
            raw.get("trinity_corps_conduct_repair_auto_apply_trial_max_per_run", 3)
        ),
    )
    return _apply_graduation_overrides(vault_root, cfg)


def _apply_graduation_overrides(vault_root: Path, cfg: TrinityConfig) -> TrinityConfig:
    """Merge graduation-overrides.yaml (Phase 17) into trinity flags when present."""
    try:
        from dataclasses import replace

        from .trinity_graduation_evaluator import load_graduation_overrides

        overrides = load_graduation_overrides(vault_root)
        if not overrides:
            return cfg
        field_map = {
            "trinity_corps_conduct_repair_auto_apply_enabled": "corps_conduct_repair_auto_apply_enabled",
            "trinity_corps_llm_repair_host_apply_enabled": "corps_llm_repair_host_apply_enabled",
            "trinity_corps_llm_repair_enabled": "corps_llm_repair_enabled",
            "trinity_corps_llm_repair_trial_enabled": "corps_llm_repair_trial_enabled",
        }
        kwargs: dict[str, Any] = {}
        for yaml_key, attr in field_map.items():
            if yaml_key in overrides:
                kwargs[attr] = bool(overrides[yaml_key])
        if kwargs:
            return replace(cfg, **kwargs)
    except Exception:
        pass
    return cfg


def _parse_trinity_id_list(raw: str | int | bool | None) -> tuple[str, ...]:
    if raw is None or raw == "":
        return ()
    if isinstance(raw, str):
        return tuple(x.strip() for x in raw.split(",") if x.strip())
    return ()


def _parse_weave_config(vault_root: Path) -> dict[str, str | int | bool | None]:
    out: dict[str, str | int | bool | None] = {}
    cfg_path = resolve_config_path(vault_root, None)
    if not cfg_path.is_file():
        return out
    text = cfg_path.read_text(encoding="utf-8", errors="replace")
    in_weave = False
    indent_weave: int | None = None
    for line in text.splitlines():
        stripped = line.lstrip()
        if not stripped or stripped.startswith("#"):
            continue
        if re.match(r"^weave:\s*$", stripped):
            in_weave = True
            indent_weave = len(line) - len(line.lstrip())
            continue
        if in_weave:
            assert indent_weave is not None
            indent = len(line) - len(line.lstrip())
            if indent <= indent_weave and stripped and not stripped.startswith("#"):
                break
            m = re.match(r"^(\s*)([a-z0-9_]+):\s*(.+?)\s*$", line)
            if not m:
                continue
            key, val = m.group(2), m.group(3).strip()
            if val in ("true", "false"):
                out[key] = val == "true"
            elif val == "null":
                out[key] = None
            elif val.isdigit() or (val.startswith("-") and val[1:].isdigit()):
                out[key] = int(val)
            else:
                out[key] = val.strip("\"'")
    return out
