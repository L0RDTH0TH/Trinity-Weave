"""Tiered self-heal for factory mutable band — L0 retry, L1 barrier refresh, L2 escalate."""

from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .agent_changed_paths import collect_git_artifact_paths, is_vault_handoff_path
from .drop_contract_base import load_drop_manifest, DROP_CONTRACTS
from .merge_barrier import check_job_allowed

ESCALATION_LOG_REL = ".technical/factory/escalations.jsonl"
REQUEUE_LOG_REL = ".technical/factory/self-heal-requeue.jsonl"


@dataclass(frozen=True)
class SelfHealResult:
    attempted: bool
    healed: bool
    tier: str
    action: str
    detail: str


def _extract_orphan_path(violation: str) -> str | None:
    marker = "orphan_path_no_zone:"
    idx = violation.find(marker)
    if idx == -1:
        return None
    return violation[idx + len(marker) :].strip()


def _is_lint_evidence_overreach(
    vault_root: Path,
    rel_path: str,
    *,
    game_repo_rel: str,
) -> bool:
    """
    orphan_path_no_zone from handoff/log mention, not a git artifact in the game repo.
    Real cross-zone git writes remain failures (path in collect_git_artifact_paths).
    """
    if not rel_path:
        return False
    if is_vault_handoff_path(rel_path):
        return True
    if not game_repo_rel:
        return False
    repo = vault_root / game_repo_rel.strip("/")
    artifacts = collect_git_artifact_paths(repo)
    return rel_path not in artifacts


def attempt_self_heal(
    vault_root: Path,
    violation: str,
    *,
    game_repo_rel: str = "",
    job: dict[str, Any] | None = None,
) -> SelfHealResult:
    """Single-violation heal attempt."""
    v = violation.strip()
    _ = job  # reserved for future lane-scoped heal rules

    orphan_rel = _extract_orphan_path(v)
    if orphan_rel and _is_lint_evidence_overreach(vault_root, orphan_rel, game_repo_rel=game_repo_rel):
        return SelfHealResult(
            attempted=True,
            healed=True,
            tier="L0",
            action="lint_evidence_overreach_reclassify",
            detail=f"Handoff-mentioned path excluded from lane artifact set: {orphan_rel}",
        )

    # L0 — transient / parse retry
    if v.startswith("manifest_read_error") or v.startswith("yaml_parse"):
        return SelfHealResult(
            attempted=True,
            healed=True,
            tier="L0",
            action="retry_manifest_read",
            detail=f"Marked for retry: {v}",
        )

    if v.startswith("missing:") and "project.godot" in v and game_repo_rel:
        repo = vault_root / game_repo_rel.strip("/")
        if (repo / "project.godot").is_file():
            return SelfHealResult(
                attempted=True,
                healed=True,
                tier="L0",
                action="stale_missing_project_godot",
                detail="project.godot present on retry",
            )

    # L1 — merge barrier / drop dependency refresh
    if v.startswith("blocked_until_drop:") or v.startswith("depends_on_drop_missing:"):
        return SelfHealResult(
            attempted=True,
            healed=False,
            tier="L1",
            action="wait_upstream_lane",
            detail=f"Upstream drop required — re-dispatch after producer lane completes: {v}",
        )

    if v.startswith("cdc_empty") or v.endswith("_empty"):
        ctype = v.replace("_empty", "").replace("cdc_empty", "cdc")
        if game_repo_rel and ctype in DROP_CONTRACTS:
            data = load_drop_manifest(vault_root / game_repo_rel.strip("/"), ctype)
            if data.get("drops"):
                return SelfHealResult(
                    attempted=True,
                    healed=True,
                    tier="L1",
                    action="drop_manifest_refreshed",
                    detail=f"{ctype} drops now present",
                )

    # L2 — build / integrate escalation
    if v == "dotnet_build_fail" and game_repo_rel:
        repo = vault_root / game_repo_rel.strip("/")
        csprojs = list(repo.glob("*.csproj"))
        if csprojs:
            try:
                r = subprocess.run(
                    ["dotnet", "build", str(csprojs[0])],
                    cwd=repo,
                    capture_output=True,
                    text=True,
                    timeout=180,
                )
                if r.returncode == 0:
                    return SelfHealResult(
                        attempted=True,
                        healed=True,
                        tier="L2",
                        action="dotnet_build_retry",
                        detail="dotnet build passed on L2 retry",
                    )
            except (subprocess.TimeoutExpired, OSError) as e:
                return SelfHealResult(
                    attempted=True,
                    healed=False,
                    tier="L2",
                    action="escalate",
                    detail=f"dotnet retry failed: {e}",
                )

    if v.startswith("unwelded_vendor"):
        return SelfHealResult(
            attempted=True,
            healed=False,
            tier="L2",
            action="escalate",
            detail="Spine adapter required — see ICameraRig DRB",
        )

    if v.startswith("seat_fail:") or v.startswith("unknown_exit_gate:"):
        return SelfHealResult(
            attempted=True,
            healed=False,
            tier="L2",
            action="escalate_review_seat",
            detail=f"Review seat failure requires lane rework or operator: {v}",
        )

    return SelfHealResult(attempted=False, healed=False, tier="none", action="none", detail=f"no heal rule for {v}")


def attempt_self_heal_chain(
    vault_root: Path,
    violations: list[str],
    *,
    game_repo_rel: str = "",
    job: dict[str, Any] | None = None,
) -> list[SelfHealResult]:
    """Run heal chain for each violation; stop early if L1 barrier still blocks."""
    results: list[SelfHealResult] = []
    for v in violations:
        results.append(
            attempt_self_heal(vault_root, v, game_repo_rel=game_repo_rel, job=job)
        )
    if job and game_repo_rel:
        check = check_job_allowed(vault_root, job, game_repo_rel=game_repo_rel)
        if check.allowed and any(r.healed for r in results):
            results.append(
                SelfHealResult(
                    attempted=True,
                    healed=True,
                    tier="L1",
                    action="merge_barrier_clear",
                    detail="merge_barrier allows job after heal",
                )
            )
    return results


def _utc_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def append_escalation(
    vault_root: Path,
    *,
    slice_id: str,
    lane_id: str,
    violations: list[str],
    tier: str,
    action: str,
    detail: str,
    run_id: str | None = None,
    requeue: bool = False,
) -> Path:
    vault_root = vault_root.resolve()
    path = vault_root / ESCALATION_LOG_REL
    path.parent.mkdir(parents=True, exist_ok=True)
    row = {
        "ts": _utc_iso(),
        "slice_id": slice_id,
        "lane_id": lane_id,
        "violations": violations,
        "tier": tier,
        "action": action,
        "detail": detail,
        "run_id": run_id,
        "requeue_requested": requeue,
    }
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")
    return path


def handle_seat_failure_escalation(
    vault_root: Path,
    *,
    slice_id: str,
    lane_id: str,
    violations: list[str],
    game_repo_rel: str = "",
    job: dict[str, Any] | None = None,
    run_id: str | None = None,
    queue_lane: str = "godot",
) -> dict[str, Any]:
    """
    Run self-heal chain; L2 failures append escalation log.
    L0 heals may append a single-lane requeue marker for next orchestrator pass.
    """
    heals = attempt_self_heal_chain(
        vault_root, violations, game_repo_rel=game_repo_rel, job=job
    )
    any_healed = any(h.healed for h in heals)
    max_tier = max(
        (int(h.tier[1]) for h in heals if h.tier.startswith("L") and h.tier[1:].isdigit()),
        default=0,
    )
    escalated = any(h.tier == "L2" and not h.healed for h in heals) or (
        not any_healed and bool(violations)
    )

    requeue = False
    if any_healed and max_tier <= 1 and job:
        requeue = True
        rq_path = vault_root / REQUEUE_LOG_REL
        rq_path.parent.mkdir(parents=True, exist_ok=True)
        with rq_path.open("a", encoding="utf-8") as f:
            f.write(
                json.dumps(
                    {
                        "ts": _utc_iso(),
                        "slice_id": slice_id,
                        "lane_id": lane_id,
                        "queue_lane": queue_lane,
                        "run_id": run_id,
                        "reason": "self_heal_l0_l1",
                    },
                    ensure_ascii=False,
                )
                + "\n"
            )

    esc_path = None
    if escalated:
        top = heals[-1] if heals else None
        esc_path = append_escalation(
            vault_root,
            slice_id=slice_id,
            lane_id=lane_id,
            violations=violations,
            tier=top.tier if top else "L2",
            action=top.action if top else "escalate_operator",
            detail=top.detail if top else "seat_failure_unhealed",
            run_id=run_id,
            requeue=requeue,
        )

    return {
        "heals": [h.__dict__ for h in heals],
        "any_healed": any_healed,
        "escalated": escalated,
        "requeue_marked": requeue,
        "escalation_path": str(esc_path.relative_to(vault_root)) if esc_path else None,
    }
