"""Phase A — L4 adaptive policy validation drills (G1 replay → G2 bandit → Q3 promotion)."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from ..maintenance_handlers import handle_maintenance_entry
from ..maintenance_io import maintenance_pq_path
from ..plan import load_queue_file
from .adaptive_policy import (
    active_policy_path,
    bandit_update,
    collect_replay_episodes,
    load_active_policy,
    pending_promotion_path,
    propose_policy_promotion,
    recommend_profile,
    replay_report_path,
    render_l4_board_section,
    run_offline_replay,
    state_path,
)
from .config import load_l4_config
from .governance import append_metric_row, ensure_weave_paths, weave_dir


def _utc_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _utc_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


@dataclass
class PolicySnapshot:
    active: bytes | None = None
    pending: bytes | None = None
    metrics: bytes | None = None


def _snapshot_policy(vault_root: Path) -> PolicySnapshot:
    active_p = active_policy_path(vault_root)
    pending_p = pending_promotion_path(vault_root)
    metrics_p = weave_dir(vault_root) / "metrics.jsonl"
    return PolicySnapshot(
        active=active_p.read_bytes() if active_p.is_file() else None,
        pending=pending_p.read_bytes() if pending_p.is_file() else None,
        metrics=metrics_p.read_bytes() if metrics_p.is_file() else None,
    )


def _restore_policy(vault_root: Path, snap: PolicySnapshot) -> None:
    for path, content in (
        (active_policy_path(vault_root), snap.active),
        (pending_promotion_path(vault_root), snap.pending),
        (weave_dir(vault_root) / "metrics.jsonl", snap.metrics),
    ):
        if content is not None:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content)
        elif path.is_file():
            path.unlink()


def _seed_replay_episodes(vault_root: Path, *, min_episodes: int, source: str = "l4_validation_drill") -> dict[str, Any]:
    """Inject lane_board_refresh rows when vault lacks G1 replay input."""
    existing = collect_replay_episodes(vault_root)
    need = max(0, int(min_episodes) - len(existing))
    if need <= 0:
        return {"seeded": 0, "episodes_before": len(existing), "episodes_after": len(existing)}
    stamp = _utc_stamp()
    for i in range(need):
        append_metric_row(
            vault_root,
            {
                "metric_type": "lane_board_refresh",
                "integrity_ok": True,
                "system_attention": "green",
                "source": source,
                "fingerprint": f"l4-drill-replay-{stamp}-{i}",
            },
        )
    after = collect_replay_episodes(vault_root)
    return {"seeded": need, "episodes_before": len(existing), "episodes_after": len(after)}


def _parse_board_live_apply(section: str) -> str | None:
    m = re.search(r"\*\*Live apply:\*\*\s*(\S+)", section)
    return m.group(1).strip().lower() if m else None


def _pq_has_mode(vault_root: Path, mode: str) -> bool:
    pq = maintenance_pq_path(vault_root)
    if not pq.is_file():
        return False
    mode_u = mode.strip().upper()
    for entry in load_queue_file(pq):
        if str(entry.mode or "").strip().upper() == mode_u:
            return True
    return False


def _result(
    drill_id: str,
    *,
    passed: bool,
    checks: list[dict[str, Any]],
    detail: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "drill_id": drill_id,
        "passed": passed,
        "checks": checks,
        "detail": detail or {},
        "timestamp": _utc_iso(),
    }


def drill_l4_offline_replay(vault_root: Path, *, dry_run: bool = False) -> dict[str, Any]:
    checks: list[dict[str, Any]] = []
    if dry_run:
        return _result("l4_offline_replay", passed=True, checks=[{"name": "dry_run", "ok": True}])

    cfg = load_l4_config(vault_root)
    replay = run_offline_replay(vault_root, cfg=cfg)
    checks.append({"name": "replay_ok", "ok": bool(replay.get("ok")), "replay": replay})

    report_path = replay_report_path(vault_root)
    checks.append({"name": "report_file_written", "ok": report_path.is_file()})

    if replay.get("ok"):
        checks.append(
            {
                "name": "episodes_meet_minimum",
                "ok": int(replay.get("episodes") or 0) >= cfg.replay_min_episodes,
                "episodes": replay.get("episodes"),
                "required": cfg.replay_min_episodes,
            }
        )
        checks.append(
            {
                "name": "recommended_arm_present",
                "ok": str(replay.get("recommended_arm") or "") in ("quality", "balance", "speed"),
                "recommended_arm": replay.get("recommended_arm"),
            }
        )

    passed = bool(replay.get("ok")) and all(c.get("ok") for c in checks[1:])
    return _result("l4_offline_replay", passed=passed, checks=checks, detail={"replay": replay})


def drill_l4_bandit_update(vault_root: Path, *, dry_run: bool = False) -> dict[str, Any]:
    checks: list[dict[str, Any]] = []
    if dry_run:
        return _result("l4_bandit_update", passed=True, checks=[{"name": "dry_run", "ok": True}])

    upd = bandit_update(vault_root)
    checks.append({"name": "bandit_update_ok", "ok": bool(upd.get("ok")), "update": upd})
    rec = upd.get("recommendation") or {}
    checks.append(
        {
            "name": "recommendation_arm_valid",
            "ok": str(rec.get("arm") or "") in ("quality", "balance", "speed"),
            "recommendation": rec,
        }
    )
    checks.append(
        {
            "name": "recommendation_observe_only",
            "ok": rec.get("live") is False and rec.get("source") == "bandit_ucb",
            "recommendation": rec,
        }
    )
    checks.append({"name": "bandit_state_persisted", "ok": state_path(vault_root).is_file()})

    section = render_l4_board_section(vault_root)
    checks.append(
        {
            "name": "board_section_shows_recommendation",
            "ok": f"`{rec.get('arm')}`" in section,
            "section_excerpt": section[:280],
        }
    )

    passed = bool(upd.get("ok")) and all(c.get("ok") for c in checks[1:])
    return _result("l4_bandit_update", passed=passed, checks=checks, detail={"update": upd})


def drill_l4_promotion_proposal(vault_root: Path, *, dry_run: bool = False) -> dict[str, Any]:
    checks: list[dict[str, Any]] = []
    if dry_run:
        return _result("l4_promotion_proposal", passed=True, checks=[{"name": "dry_run", "ok": True}])

    cfg = load_l4_config(vault_root)
    proposal = propose_policy_promotion(vault_root, cfg=cfg)
    checks.append({"name": "proposal_call_ok", "ok": bool(proposal.get("ok")), "proposal": proposal})

    if proposal.get("skipped"):
        checks.append(
            {
                "name": "skip_reason_documented",
                "ok": proposal.get("reason") in ("uplift_below_threshold",),
                "reason": proposal.get("reason"),
                "uplift": proposal.get("uplift"),
                "threshold": proposal.get("threshold"),
            }
        )
        passed = bool(proposal.get("ok")) and all(c.get("ok") for c in checks)
        return _result(
            "l4_promotion_proposal",
            passed=passed,
            checks=checks,
            detail={"proposal": proposal, "note": "uplift below threshold — governance drill may reuse existing pending"},
        )

    checks.append({"name": "pending_file_written", "ok": pending_promotion_path(vault_root).is_file()})
    checks.append(
        {
            "name": "adaptive_policy_review_queued",
            "ok": _pq_has_mode(vault_root, "ADAPTIVE_POLICY_REVIEW"),
        }
    )
    pending = proposal.get("pending") or {}
    checks.append(
        {
            "name": "pending_requires_counselor",
            "ok": pending.get("requires_counselor") is True and pending.get("live_apply_enabled") is False,
            "pending": pending,
        }
    )

    passed = all(c.get("ok") for c in checks)
    return _result("l4_promotion_proposal", passed=passed, checks=checks, detail={"proposal": proposal})


def drill_l4_governance_promotion(
    vault_root: Path,
    *,
    dry_run: bool = False,
    live_apply: bool = False,
) -> dict[str, Any]:
    """Q3 counselor path — approve pending promotion; default observe-only (live_apply=false)."""
    vault_root = vault_root.resolve()
    checks: list[dict[str, Any]] = []
    if dry_run:
        return _result("l4_governance_promotion", passed=True, checks=[{"name": "dry_run", "ok": True}])

    pending_p = pending_promotion_path(vault_root)
    if not pending_p.is_file():
        pre = propose_policy_promotion(vault_root)
        if not pending_p.is_file() and pre.get("skipped"):
            version_id = f"l4-drill-gov-{_utc_stamp()}"
            rec = recommend_profile(vault_root)
            pending_doc = {
                "version_id": version_id,
                "proposed_at": _utc_iso(),
                "default_arm": rec.get("arm") or "balance",
                "bucket_arms": {rec.get("bucket") or "medium|yellow": rec.get("arm") or "balance"},
                "counselor_approved": False,
                "live_apply_enabled": False,
                "requires_counselor": True,
                "drill_synthetic": True,
                "proposal_skip_reason": pre.get("reason"),
            }
            weave_dir(vault_root).mkdir(parents=True, exist_ok=True)
            pending_p.write_text(json.dumps(pending_doc, indent=2) + "\n", encoding="utf-8")
            checks.append({"name": "synthetic_pending_for_q3", "ok": True, "version_id": version_id, "pre": pre})
        else:
            checks.append(
                {
                    "name": "ensure_pending_proposal",
                    "ok": pending_p.is_file() or bool(pre.get("skipped")),
                    "pre": pre,
                }
            )
        if not pending_p.is_file():
            return _result(
                "l4_governance_promotion",
                passed=False,
                checks=checks,
                detail={"error": "no_pending_promotion", "pre": pre},
            )

    try:
        pending = json.loads(pending_p.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return _result(
            "l4_governance_promotion",
            passed=False,
            checks=[{"name": "pending_parse", "ok": False}],
        )

    version_id = str(pending.get("version_id") or "")
    gov = handle_maintenance_entry(
        vault_root,
        {
            "id": f"l4-drill-gov-{_utc_stamp()}",
            "mode": "GOVERNANCE_REVIEW",
            "params": {
                "meta_only": True,
                "operator_pulse": "neutral",
                "items_cleared": ["l4_validation_drill"],
                "counselor_approve_adaptive_policy": True,
                "adaptive_policy_version_id": version_id,
                "adaptive_live_apply": live_apply,
                "fingerprint": f"l4-governance-drill-{version_id}",
            },
        },
    )
    checks.append({"name": "governance_review_ok", "ok": bool(gov.get("ok")), "gov": gov})
    gov_msg = str(gov.get("message") or gov.get("summary") or "")
    checks.append(
        {
            "name": "summary_mentions_policy_approved",
            "ok": "adaptive_policy_approved=" in gov_msg,
            "message": gov_msg,
        }
    )

    active = load_active_policy(vault_root)
    checks.append({"name": "active_policy_written", "ok": active is not None, "active": active})
    if active:
        checks.append(
            {
                "name": "counselor_approved_flag",
                "ok": active.get("counselor_approved") is True,
            }
        )
        checks.append(
            {
                "name": "live_apply_matches_drill",
                "ok": bool(active.get("live_apply_enabled")) == live_apply,
                "live_apply_enabled": active.get("live_apply_enabled"),
            }
        )

    section = render_l4_board_section(vault_root)
    board_live = _parse_board_live_apply(section)
    expected_live = "active" if live_apply else "observe-only"
    checks.append(
        {
            "name": "board_live_apply_label",
            "ok": board_live == expected_live,
            "board_live": board_live,
            "expected": expected_live,
        }
    )

    rec = recommend_profile(vault_root)
    if live_apply:
        checks.append(
            {
                "name": "recommend_uses_active_policy_when_live",
                "ok": rec.get("source") == "active_policy" and rec.get("live") is True,
                "recommendation": rec,
            }
        )
    else:
        checks.append(
            {
                "name": "recommend_stays_bandit_when_observe_only",
                "ok": rec.get("source") == "bandit_ucb" and rec.get("live") is False,
                "recommendation": rec,
            }
        )

    passed = all(c.get("ok") for c in checks)
    return _result(
        "l4_governance_promotion",
        passed=passed,
        checks=checks,
        detail={"version_id": version_id, "live_apply": live_apply, "active": active, "recommendation": rec},
    )


def drill_l4_config_board_reconcile(vault_root: Path, *, dry_run: bool = False) -> dict[str, Any]:
    """Document config knob vs active policy vs board display semantics."""
    checks: list[dict[str, Any]] = []
    if dry_run:
        return _result("l4_config_board_reconcile", passed=True, checks=[{"name": "dry_run", "ok": True}])

    cfg = load_l4_config(vault_root)
    active = load_active_policy(vault_root) or {}
    section = render_l4_board_section(vault_root)
    board_live = _parse_board_live_apply(section)
    active_live = bool(active.get("live_apply_enabled"))

    checks.append(
        {
            "name": "board_matches_active_policy_live_flag",
            "ok": (board_live == "active") == active_live,
            "board_live": board_live,
            "active_live_apply": active_live,
        }
    )
    checks.append(
        {
            "name": "config_knob_documented_separate",
            "ok": True,
            "config_l4_live_apply_enabled": cfg.live_apply_enabled,
            "note": (
                "Board/recommend live gating uses adaptive_policy_active.json after counselor approval; "
                "weave.l4_live_apply_enabled in Config is not wired directly to board label."
            ),
        }
    )
    if cfg.live_apply_enabled and not active_live:
        checks.append(
            {
                "name": "config_true_but_runtime_observe_only_ok",
                "ok": board_live == "observe-only",
                "explanation": "Config true without counselor-approved active policy still observe-only (expected)",
            }
        )

    passed = all(c.get("ok") for c in checks if c["name"] != "config_knob_documented_separate")
    return _result(
        "l4_config_board_reconcile",
        passed=passed,
        checks=checks,
        detail={
            "config": {"l4_live_apply_enabled": cfg.live_apply_enabled, "l4_adaptive_enabled": cfg.enabled},
            "active_policy": active,
            "board_live": board_live,
        },
    )


DRILL_FUNCS = {
    "offline_replay": drill_l4_offline_replay,
    "bandit_update": drill_l4_bandit_update,
    "promotion_proposal": drill_l4_promotion_proposal,
    "governance_promotion": drill_l4_governance_promotion,
    "config_board_reconcile": drill_l4_config_board_reconcile,
}


def run_l4_validation_drill(
    vault_root: Path,
    *,
    drill: str = "all",
    dry_run: bool = False,
    write_report: bool = True,
    governance_live_apply: bool = False,
) -> dict[str, Any]:
    vault_root = vault_root.resolve()
    ensure_weave_paths(vault_root)
    names = list(DRILL_FUNCS.keys()) if drill.strip().lower() == "all" else [drill.strip().lower()]
    unknown = [n for n in names if n not in DRILL_FUNCS]
    if unknown:
        return {"ok": False, "error": "unknown_drill", "unknown": unknown, "valid": list(DRILL_FUNCS.keys())}

    policy_snap = _snapshot_policy(vault_root)
    seed_info: dict[str, Any] | None = None
    results: list[dict[str, Any]] = []
    try:
        if not dry_run:
            cfg = load_l4_config(vault_root)
            seed_info = _seed_replay_episodes(vault_root, min_episodes=cfg.replay_min_episodes)
        for name in names:
            if name == "governance_promotion":
                results.append(
                    drill_l4_governance_promotion(
                        vault_root, dry_run=dry_run, live_apply=governance_live_apply
                    )
                )
            else:
                results.append(DRILL_FUNCS[name](vault_root, dry_run=dry_run))
    finally:
        if not dry_run and not governance_live_apply:
            _restore_policy(vault_root, policy_snap)

    all_passed = all(r.get("passed") for r in results)
    report = {
        "ok": all_passed,
        "phase": "A",
        "layer": "L4",
        "dry_run": dry_run,
        "governance_live_apply": governance_live_apply,
        "replay_seed": seed_info,
        "drills": results,
        "summary": {
            "total": len(results),
            "passed": sum(1 for r in results if r.get("passed")),
            "failed": sum(1 for r in results if not r.get("passed")),
        },
        "timestamp": _utc_iso(),
    }
    if write_report and not dry_run:
        out_dir = vault_root / ".technical" / "weave" / "validation"
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / f"l4-drill-{_utc_stamp()}.json"
        out_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        report["report_path"] = str(out_path)
        append_metric_row(
            vault_root,
            {
                "metric_type": "l4_validation_drill",
                "ok": all_passed,
                "passed": report["summary"]["passed"],
                "failed": report["summary"]["failed"],
                "report_path": str(out_path),
            },
        )
    return report
