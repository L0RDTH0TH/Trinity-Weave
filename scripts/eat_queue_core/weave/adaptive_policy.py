"""Wave 4 L4 adaptive policy — G1 schema/replay spec + G2 offline bandit pilot (no live apply by default)."""

from __future__ import annotations

import json
import math
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Literal

from .config import L4Config, load_l4_config
from .governance import append_metric_row, weave_dir
from .predictive import assess_maintenance_risk, calibrate_predictive_tiers

ArmName = Literal["quality", "balance", "speed"]

DEFAULT_ARMS: tuple[ArmName, ...] = ("quality", "balance", "speed")

# G1 counterfactual heuristic — not live RL; offline uplift estimates only.
ARM_EFFECTS: dict[str, dict[str, float]] = {
    "quality": {"integrity_delta": 0.05, "heal_penalty": 0.08, "speed_bonus": -0.03},
    "balance": {"integrity_delta": 0.0, "heal_penalty": 0.0, "speed_bonus": 0.0},
    "speed": {"integrity_delta": -0.05, "heal_penalty": -0.05, "speed_bonus": 0.04},
}


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _parse_iso(ts: str) -> datetime | None:
    try:
        if ts.endswith("Z"):
            ts = ts[:-1] + "+00:00"
        return datetime.fromisoformat(ts)
    except (ValueError, TypeError):
        return None


def state_path(vault_root: Path) -> Path:
    return weave_dir(vault_root) / "adaptive_policy_state.json"


def replay_report_path(vault_root: Path) -> Path:
    return weave_dir(vault_root) / "adaptive_replay_report.json"


def pending_promotion_path(vault_root: Path) -> Path:
    return weave_dir(vault_root) / "adaptive_policy_pending.json"


def active_policy_path(vault_root: Path) -> Path:
    return weave_dir(vault_root) / "adaptive_policy_active.json"


def policy_versions_dir(vault_root: Path) -> Path:
    return weave_dir(vault_root) / "adaptive_policy_versions"


@dataclass(frozen=True)
class PolicySchema:
    """G1 — auditable policy version (maps to validator_profiles / pipeline_mode)."""

    version_id: str
    default_arm: ArmName
    bucket_arms: dict[str, ArmName]
    live_apply_enabled: bool
    counselor_approved: bool
    created_at: str
    notes: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "version_id": self.version_id,
            "default_arm": self.default_arm,
            "bucket_arms": dict(self.bucket_arms),
            "live_apply_enabled": self.live_apply_enabled,
            "counselor_approved": self.counselor_approved,
            "created_at": self.created_at,
            "notes": self.notes,
            "schema": "weave_l4_policy_v1",
        }


@dataclass
class ReplayEpisode:
    timestamp: str
    features: dict[str, Any]
    outcome: dict[str, Any]
    attributed_arm: ArmName
    base_reward: float


def _empty_arm_stats(arms: tuple[ArmName, ...]) -> dict[str, dict[str, float]]:
    return {a: {"n": 0.0, "reward_sum": 0.0} for a in arms}


def load_bandit_state(vault_root: Path) -> dict[str, Any]:
    p = state_path(vault_root)
    if not p.is_file():
        return {
            "arms": list(DEFAULT_ARMS),
            "global_counts": _empty_arm_stats(DEFAULT_ARMS),
            "bucket_counts": {},
            "last_replay_at": None,
            "epsilon": 0.1,
        }
    try:
        raw = json.loads(p.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        raw = {}
    if not isinstance(raw, dict):
        raw = {}
    raw.setdefault("arms", list(DEFAULT_ARMS))
    raw.setdefault("global_counts", _empty_arm_stats(tuple(raw["arms"])))
    raw.setdefault("bucket_counts", {})
    return raw


def save_bandit_state(vault_root: Path, state: dict[str, Any]) -> Path:
    weave_dir(vault_root).mkdir(parents=True, exist_ok=True)
    p = state_path(vault_root)
    p.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
    return p


def _feature_bucket(features: dict[str, Any]) -> str:
    tier = str(features.get("risk_tier") or "medium")
    att = str(features.get("system_attention") or "yellow")
    return f"{tier}|{att}"


def compute_episode_reward(outcome: dict[str, Any]) -> float:
    """G1 reward — lower recurrence, higher first-pass pass, lower MTTR proxy."""
    reward = 0.0
    if outcome.get("integrity_ok") is True:
        reward += 1.0
    elif outcome.get("integrity_ok") is False:
        reward -= 0.8
    if outcome.get("l3_heal") is True:
        reward -= 0.25
    att = str(outcome.get("system_attention") or "")
    if att == "green":
        reward += 0.15
    elif att == "red":
        reward -= 0.2
    if outcome.get("recurrence") is True:
        reward -= 0.5
    return round(reward, 4)


def _counterfactual_reward(base: float, arm: ArmName, episode: ReplayEpisode) -> float:
    eff = ARM_EFFECTS.get(arm, ARM_EFFECTS["balance"])
    r = base
    if episode.outcome.get("integrity_ok") is not None:
        if episode.outcome.get("integrity_ok"):
            r += eff["integrity_delta"]
        else:
            r -= eff["integrity_delta"] * 0.5
    if episode.outcome.get("l3_heal"):
        r -= eff["heal_penalty"]
    r += eff["speed_bonus"]
    return round(r, 4)


def collect_replay_episodes(vault_root: Path, *, max_rows: int = 500) -> list[ReplayEpisode]:
    """Build episodes from weave metrics (G1 offline replay input)."""
    metrics = weave_dir(vault_root) / "metrics.jsonl"
    if not metrics.is_file():
        return []

    episodes: list[ReplayEpisode] = []
    prev_integrity: bool | None = None
    lines = metrics.read_text(encoding="utf-8", errors="replace").splitlines()
    for line in lines[-max_rows:]:
        line = line.strip()
        if not line:
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        if not isinstance(row, dict):
            continue
        mtype = row.get("metric_type")
        if mtype not in ("lane_board_refresh", "l3_self_heal", "predictive_calibration"):
            continue

        ts = str(row.get("timestamp") or _now_iso())
        attention = str(row.get("system_attention") or "")
        integrity_ok = row.get("integrity_ok")
        if mtype == "l3_self_heal":
            integrity_ok = row.get("verifier_ok") if row.get("verifier_ok") is not None else integrity_ok

        recurrence = prev_integrity is True and integrity_ok is False
        prev_integrity = integrity_ok if integrity_ok is not None else prev_integrity

        calibrate_predictive_tiers(vault_root)
        assessment = assess_maintenance_risk(vault_root)
        features = {
            "risk_tier": assessment.risk_tier,
            "system_attention": attention or assessment.signals.get("system_attention"),
            "metric_type": mtype,
        }
        outcome = {
            "integrity_ok": integrity_ok,
            "system_attention": attention,
            "l3_heal": mtype == "l3_self_heal",
            "recurrence": recurrence,
        }
        base = compute_episode_reward(outcome)
        episodes.append(
            ReplayEpisode(
                timestamp=ts,
                features=features,
                outcome=outcome,
                attributed_arm="balance",
                base_reward=base,
            )
        )
    return episodes


def run_offline_replay(vault_root: Path, *, cfg: L4Config | None = None) -> dict[str, Any]:
    """G1 — score arms on historical episodes; no live policy mutation."""
    cfg = cfg or load_l4_config(vault_root)
    episodes = collect_replay_episodes(vault_root)
    if len(episodes) < cfg.replay_min_episodes:
        report = {
            "ok": False,
            "reason": "insufficient_episodes",
            "episodes": len(episodes),
            "required": cfg.replay_min_episodes,
            "generated_at": _now_iso(),
        }
        replay_report_path(vault_root).write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        return report

    arm_scores: dict[str, dict[str, float]] = {}
    for arm in DEFAULT_ARMS:
        total = 0.0
        for ep in episodes:
            total += _counterfactual_reward(ep.base_reward, arm, ep)
        arm_scores[arm] = {
            "mean_reward": round(total / len(episodes), 4),
            "total_reward": round(total, 4),
            "episodes": len(episodes),
        }

    baseline = arm_scores["balance"]["mean_reward"]
    uplifts = {
        a: round(arm_scores[a]["mean_reward"] - baseline, 4) for a in DEFAULT_ARMS if a != "balance"
    }
    best_arm = max(DEFAULT_ARMS, key=lambda a: arm_scores[a]["mean_reward"])

    report = {
        "ok": True,
        "generated_at": _now_iso(),
        "episodes": len(episodes),
        "arm_scores": arm_scores,
        "baseline_arm": "balance",
        "uplifts_vs_balance": uplifts,
        "recommended_arm": best_arm,
        "safety_note": "Counterfactual heuristic only — counselor approval required before live_apply.",
    }
    weave_dir(vault_root).mkdir(parents=True, exist_ok=True)
    replay_report_path(vault_root).write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    append_metric_row(
        vault_root,
        {"metric_type": "l4_offline_replay", "episodes": len(episodes), "recommended_arm": best_arm},
    )
    return report


def _ucb_score(mean: float, n: float, total_n: float, exploration: float) -> float:
    if n <= 0:
        return float("inf")
    bonus = exploration * math.sqrt(math.log(max(total_n, 1)) / n)
    return mean + bonus


def bandit_update(vault_root: Path, *, cfg: L4Config | None = None) -> dict[str, Any]:
    """G2 — update bandit state from offline replay (still no live apply unless approved)."""
    cfg = cfg or load_l4_config(vault_root)
    replay = run_offline_replay(vault_root, cfg=cfg)
    if not replay.get("ok"):
        return {"ok": False, "replay": replay}

    state = load_bandit_state(vault_root)
    episodes = collect_replay_episodes(vault_root)
    arms = tuple(state.get("arms") or DEFAULT_ARMS)

    for ep in episodes:
        bucket = _feature_bucket(ep.features)
        bcounts = state["bucket_counts"].setdefault(bucket, _empty_arm_stats(arms))
        for arm in arms:
            r = _counterfactual_reward(ep.base_reward, arm, ep)  # type: ignore[arg-type]
            g = state["global_counts"].setdefault(arm, {"n": 0.0, "reward_sum": 0.0})
            g["n"] = float(g.get("n", 0)) + 1
            g["reward_sum"] = float(g.get("reward_sum", 0)) + r
            ba = bcounts.setdefault(arm, {"n": 0.0, "reward_sum": 0.0})
            ba["n"] = float(ba.get("n", 0)) + 1
            ba["reward_sum"] = float(ba.get("reward_sum", 0)) + r

    state["last_replay_at"] = _now_iso()
    state["epsilon"] = cfg.bandit_epsilon
    save_bandit_state(vault_root, state)

    recommendation = recommend_profile(vault_root, cfg=cfg)
    append_metric_row(
        vault_root,
        {
            "metric_type": "l4_bandit_update",
            "recommended_arm": recommendation.get("arm"),
            "bucket": recommendation.get("bucket"),
        },
    )
    return {"ok": True, "replay": replay, "recommendation": recommendation, "episodes": len(episodes)}


def recommend_profile(
    vault_root: Path,
    *,
    context: dict[str, Any] | None = None,
    cfg: L4Config | None = None,
) -> dict[str, Any]:
    """Recommend workflow profile arm for current state (pilot — does not mutate queue)."""
    cfg = cfg or load_l4_config(vault_root)
    active = load_active_policy(vault_root)
    if active and active.get("live_apply_enabled") and active.get("counselor_approved"):
        bucket = _feature_bucket(context or _current_features(vault_root))
        arm = active.get("bucket_arms", {}).get(bucket) or active.get("default_arm", "balance")
        return {
            "arm": arm,
            "source": "active_policy",
            "version_id": active.get("version_id"),
            "bucket": bucket,
            "live": True,
        }

    calibrate_predictive_tiers(vault_root)
    assessment = assess_maintenance_risk(vault_root, context=context)
    features = dict(context or {})
    features.setdefault("risk_tier", assessment.risk_tier)
    bucket = _feature_bucket(features)

    state = load_bandit_state(vault_root)
    arms = tuple(state.get("arms") or DEFAULT_ARMS)
    bcounts = state.get("bucket_counts", {}).get(bucket) or state.get("global_counts", {})
    total_n = sum(float(bcounts.get(a, {}).get("n", 0)) for a in arms)
    eps = float(state.get("epsilon") or cfg.bandit_epsilon)

    best_arm = "balance"
    best_score = -1e9
    for arm in arms:
        st = bcounts.get(arm, {"n": 0, "reward_sum": 0})
        n = float(st.get("n", 0))
        mean = float(st.get("reward_sum", 0)) / n if n > 0 else 0.0
        score = _ucb_score(mean, n, total_n, eps)
        if score > best_score:
            best_score = score
            best_arm = arm

    return {
        "arm": best_arm,
        "source": "bandit_ucb",
        "bucket": bucket,
        "live": False,
        "risk_tier": assessment.risk_tier,
        "note": "Pilot observe-only until counselor approves pending promotion.",
    }


def _current_features(vault_root: Path) -> dict[str, Any]:
    assessment = assess_maintenance_risk(vault_root)
    return {
        "risk_tier": assessment.risk_tier,
        "system_attention": assessment.signals.get("system_attention"),
    }


def propose_policy_promotion(vault_root: Path, *, cfg: L4Config | None = None) -> dict[str, Any]:
    """G2 — write pending promotion for counselor (Q3); does not activate."""
    cfg = cfg or load_l4_config(vault_root)
    replay = run_offline_replay(vault_root, cfg=cfg)
    if not replay.get("ok"):
        return {"ok": False, "replay": replay}

    rec = recommend_profile(vault_root, cfg=cfg)
    best = str(replay.get("recommended_arm") or "balance")
    uplift = (replay.get("uplifts_vs_balance") or {}).get(best, 0.0)

    if uplift < cfg.min_uplift_for_proposal:
        return {
            "ok": True,
            "skipped": True,
            "reason": "uplift_below_threshold",
            "uplift": uplift,
            "threshold": cfg.min_uplift_for_proposal,
        }

    version_id = f"l4-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}"
    pending = {
        "version_id": version_id,
        "proposed_at": _now_iso(),
        "default_arm": best,
        "bucket_arms": {rec.get("bucket", "medium|yellow"): best},
        "replay_summary": {
            "episodes": replay.get("episodes"),
            "arm_scores": replay.get("arm_scores"),
            "uplifts_vs_balance": replay.get("uplifts_vs_balance"),
        },
        "counselor_approved": False,
        "live_apply_enabled": False,
        "requires_counselor": cfg.counselor_required_for_promotion,
    }
    weave_dir(vault_root).mkdir(parents=True, exist_ok=True)
    pending_promotion_path(vault_root).write_text(json.dumps(pending, indent=2) + "\n", encoding="utf-8")

    versions = policy_versions_dir(vault_root)
    versions.mkdir(parents=True, exist_ok=True)
    (versions / f"{version_id}.json").write_text(json.dumps(pending, indent=2) + "\n", encoding="utf-8")

    from ..maintenance_io import append_maintenance_entry

    append_maintenance_entry(
        vault_root,
        mode="ADAPTIVE_POLICY_REVIEW",
        params={
            "meta_only": True,
            "version_id": version_id,
            "proposed_arm": best,
            "uplift": uplift,
            "fingerprint": f"adaptive-policy:{version_id}",
        },
        source="l4_propose_promotion",
    )
    return {"ok": True, "pending": pending, "maintenance_queued": True}


def load_active_policy(vault_root: Path) -> dict[str, Any] | None:
    p = active_policy_path(vault_root)
    if not p.is_file():
        return None
    try:
        raw = json.loads(p.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None
    return raw if isinstance(raw, dict) else None


def approve_policy_promotion(
    vault_root: Path,
    *,
    version_id: str | None = None,
    counselor_approved: bool = True,
    live_apply: bool = False,
) -> dict[str, Any]:
    """Q3 counselor path — activate audited policy version."""
    pending_p = pending_promotion_path(vault_root)
    if not pending_p.is_file():
        return {"ok": False, "error": "no_pending_promotion"}
    try:
        pending = json.loads(pending_p.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"ok": False, "error": "pending_corrupt"}

    vid = version_id or pending.get("version_id")
    if vid != pending.get("version_id"):
        return {"ok": False, "error": "version_mismatch", "expected": pending.get("version_id")}

    policy = PolicySchema(
        version_id=str(vid),
        default_arm=pending.get("default_arm", "balance"),
        bucket_arms=dict(pending.get("bucket_arms") or {}),
        live_apply_enabled=bool(live_apply),
        counselor_approved=counselor_approved,
        created_at=_now_iso(),
        notes="Activated via counselor approval (G2).",
    )
    payload = policy.to_dict()
    active_policy_path(vault_root).write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    pending["counselor_approved"] = counselor_approved
    pending["approved_at"] = _now_iso()
    pending_p.write_text(json.dumps(pending, indent=2) + "\n", encoding="utf-8")
    append_metric_row(
        vault_root,
        {
            "metric_type": "l4_policy_approved",
            "version_id": vid,
            "live_apply_enabled": live_apply,
        },
    )
    return {"ok": True, "active": payload}


def render_l4_board_section(vault_root: Path, *, cfg: L4Config | None = None) -> str:
    cfg = cfg or load_l4_config(vault_root)
    rec = recommend_profile(vault_root, cfg=cfg)
    replay_p = replay_report_path(vault_root)
    replay_note = ""
    if replay_p.is_file():
        try:
            rep = json.loads(replay_p.read_text(encoding="utf-8"))
            if rep.get("ok"):
                replay_note = (
                    f"\n> Offline replay: {rep.get('episodes')} episodes · "
                    f"best `{rep.get('recommended_arm')}` · uplift vs balance "
                    f"`{(rep.get('uplifts_vs_balance') or {}).get(rep.get('recommended_arm'), 0)}`"
                )
        except json.JSONDecodeError:
            pass
    pending = pending_promotion_path(vault_root)
    pending_note = "none"
    if pending.is_file():
        pending_note = "awaiting counselor"
    active = load_active_policy(vault_root)
    live = "active" if active and active.get("live_apply_enabled") else "observe-only"
    return (
        f"> [!info] L4 adaptive pilot (G1→G2)\n"
        f"> **Enabled:** {cfg.enabled} · **Live apply:** {live} · **Pending:** {pending_note}\n"
        f"> **Recommend:** `{rec.get('arm')}` ({rec.get('source')}) · bucket `{rec.get('bucket')}`\n"
        f"> Arms: quality / balance / speed (validator_profiles) — promotion requires counselor (Q3)."
        f"{replay_note}"
    )
