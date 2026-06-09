"""Alternative C — LLM repair trial convergence gate (10c / 10g; globals stay off until passed)."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .config import load_trinity_config
from .corps_repair_audit import corps_repair_audit_path, read_recent_repair_metrics
from .governance import append_metric_row

ARTIFACT_DIR = Path(".technical/weave/validation")

# Cutover gates (service era — conservative; operator flips Config manually after pass).
_CUTOVER_MIN_SEMANTIC_APPLY_OK = 3
_CUTOVER_MIN_CONDUCT_APPLY_OK = 3
_CUTOVER_MAX_MANUAL_REQUIRED_30D = 0
_CUTOVER_MIN_REPAIR_LOOP_GREEN_OR_BASELINE = 1


def _now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def _read_audit_rows(vault_root: Path, *, max_rows: int = 500) -> list[dict[str, Any]]:
    path = corps_repair_audit_path(vault_root)
    if not path.is_file():
        return []
    rows: list[dict[str, Any]] = []
    for ln in path.read_text(encoding="utf-8", errors="replace").splitlines()[-max_rows:]:
        try:
            rows.append(json.loads(ln))
        except json.JSONDecodeError:
            continue
    return rows


def summarize_llm_repair_trials(vault_root: Path, *, max_rows: int = 500) -> dict[str, Any]:
    """Aggregate 10c / 10g trial events from corps-repair-audit.jsonl."""
    rows = _read_audit_rows(vault_root, max_rows=max_rows)
    semantic_apply_ok = 0
    semantic_apply_fail = 0
    conduct_apply_ok = 0
    conduct_apply_fail = 0
    regen_packs = 0
    conduct_packs = 0
    manual_required = 0
    drift_reconcile = 0

    for row in rows:
        event = str(row.get("event") or "")
        repair_type = str(row.get("repair_type") or "")
        if event == "corps_repair":
            if repair_type == "semantic_host_apply":
                if row.get("changed"):
                    semantic_apply_ok += 1
                else:
                    semantic_apply_fail += 1
            elif repair_type == "conduct_repair_apply":
                if row.get("changed") or row.get("apply_ok"):
                    conduct_apply_ok += 1
                else:
                    conduct_apply_fail += 1
            elif repair_type == "error_narrative_drift_reconcile":
                if row.get("changed"):
                    drift_reconcile += 1
        if event == "regen_pack_written":
            regen_packs += 1
        if event == "conduct_repair_pack_written":
            conduct_packs += 1
        if row.get("manual_required"):
            manual_required += 1

    return {
        "semantic_host_apply_ok": semantic_apply_ok,
        "semantic_host_apply_fail": semantic_apply_fail,
        "conduct_apply_ok": conduct_apply_ok,
        "conduct_apply_fail": conduct_apply_fail,
        "regen_pack_count": regen_packs,
        "conduct_pack_count": conduct_packs,
        "manual_required_events": manual_required,
        "drift_reconcile_changed": drift_reconcile,
        "rows_scanned": len(rows),
    }


def _latest_self_wrap_baseline(vault_root: Path) -> dict[str, Any] | None:
    val_dir = vault_root / ARTIFACT_DIR
    if not val_dir.is_dir():
        return None
    files = sorted(val_dir.glob("trinity-weave-self-wrap-*.json"), reverse=True)
    if not files:
        return None
    try:
        data = json.loads(files[0].read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    rl = (data.get("corps_sweep") or {}).get("repair_loop") or {}
    return {
        "report": files[0].name,
        "pass_gate_ok": (data.get("operator_outcome") or {}).get("pass_gate_ok"),
        "gen_red_baseline": rl.get("gen_red_baseline"),
        "repair_stop_reason": rl.get("stop_reason"),
    }


def evaluate_trial_cutover_gates(vault_root: Path) -> dict[str, Any]:
    """Recommend whether global 10c/10g apply flags may flip (default: no)."""
    vault_root = vault_root.resolve()
    cfg = load_trinity_config(vault_root)
    trials = summarize_llm_repair_trials(vault_root)
    repair_metrics = read_recent_repair_metrics(vault_root)
    baseline = _latest_self_wrap_baseline(vault_root)

    checks: list[dict[str, Any]] = []

    def add(name: str, ok: bool, detail: str) -> None:
        checks.append({"gate": name, "ok": ok, "detail": detail})

    add(
        "semantic_apply_ok_min",
        trials["semantic_host_apply_ok"] >= _CUTOVER_MIN_SEMANTIC_APPLY_OK,
        f"{trials['semantic_host_apply_ok']}/{_CUTOVER_MIN_SEMANTIC_APPLY_OK} ok applies",
    )
    add(
        "conduct_apply_ok_min",
        trials["conduct_apply_ok"] >= _CUTOVER_MIN_CONDUCT_APPLY_OK,
        f"{trials['conduct_apply_ok']}/{_CUTOVER_MIN_CONDUCT_APPLY_OK} ok applies",
    )
    add(
        "no_manual_required_recent",
        trials["manual_required_events"] <= _CUTOVER_MAX_MANUAL_REQUIRED_30D,
        f"manual_required_events={trials['manual_required_events']}",
    )
    baseline_green = bool(
        baseline and baseline.get("pass_gate_ok") is True
    ) or bool(
        baseline
        and (baseline.get("gen_red_baseline") or {}).get("pass_gate_ok") is True
    )
    add(
        "recent_burn_or_type2_green",
        baseline_green,
        f"latest wrap: {baseline.get('report') if baseline else 'none'}",
    )
    add(
        "trial_switches_on",
        llm_trial_on(cfg) and conduct_trial_on(cfg),
        "10c/10g trial enabled; globals intentionally off",
    )

    all_ok = all(c["ok"] for c in checks)
    return {
        "ok": all_ok,
        "recommend_global_flip": False if not all_ok else "operator_manual_only",
        "phase": "llm_repair_trial_gate",
        "trials": trials,
        "repair_metrics": repair_metrics,
        "latest_self_wrap": baseline,
        "config_snapshot": {
            "trinity_corps_llm_repair_enabled": bool(
                getattr(cfg, "corps_llm_repair_enabled", False)
            ),
            "trinity_corps_llm_repair_trial_enabled": llm_trial_on(cfg),
            "trinity_corps_llm_repair_host_apply_trial_enabled": bool(
                getattr(cfg, "corps_llm_repair_host_apply_trial_enabled", False)
            ),
            "trinity_corps_conduct_repair_auto_apply_enabled": bool(
                getattr(cfg, "corps_conduct_repair_auto_apply_enabled", False)
            ),
            "trinity_corps_conduct_repair_auto_apply_trial_enabled": conduct_trial_on(
                cfg
            ),
        },
        "cutover_gates": checks,
        "next_steps": _cutover_next_steps(all_ok, trials),
    }


def llm_trial_on(cfg: Any) -> bool:
    return bool(getattr(cfg, "corps_llm_repair_trial_enabled", False))


def conduct_trial_on(cfg: Any) -> bool:
    return bool(getattr(cfg, "corps_conduct_repair_auto_apply_trial_enabled", False))


def _cutover_next_steps(all_gates_ok: bool, trials: dict[str, Any]) -> list[str]:
    if all_gates_ok:
        return [
            "All cutover gates pass — operator may consider flipping global 10c/10g apply flags in Second-Brain-Config after one more MOW cycle.",
            "Keep trinity_corps_llm_repair_enabled false until explicit operator decision.",
        ]
    steps = [
        "Global LLM repair apply stays OFF — continue trial-on path.",
        "Run fixture trials: trinity_llm_repair_trial + trinity_conduct_repair_apply_trial.",
        "Re-run after MOW passes that produce semantic/conduct reds.",
    ]
    if trials["semantic_host_apply_ok"] < _CUTOVER_MIN_SEMANTIC_APPLY_OK:
        steps.append(
            f"Need {_CUTOVER_MIN_SEMANTIC_APPLY_OK - trials['semantic_host_apply_ok']} more successful 10c-B host applies."
        )
    if trials["conduct_apply_ok"] < _CUTOVER_MIN_CONDUCT_APPLY_OK:
        steps.append(
            f"Need {_CUTOVER_MIN_CONDUCT_APPLY_OK - trials['conduct_apply_ok']} more successful 10g apply trials."
        )
    return steps


def run_llm_repair_trial_track(
    vault_root: Path,
    *,
    cluster: str | None = "harness_*",
    speed_mode: str = "balance",
    run_fixture_trials: bool = True,
    write_artifact: bool = True,
) -> dict[str, Any]:
    """Alternative C entry — assess + optional fixture trials + cutover gate report."""
    vault_root = vault_root.resolve()
    started = _now_iso()
    from .corps_llm_repair import assess_llm_repair_trial, run_llm_repair_trial

    assess: dict[str, Any] | None = None
    if cluster:
        assess = assess_llm_repair_trial(
            vault_root,
            cluster=cluster,
            speed_mode=speed_mode,
            dry_run=True,
        )

    fixture_runs: list[dict[str, Any]] = []
    if run_fixture_trials:
        for tid, weaken in (
            ("harness_llm_repair_trial", True),
        ):
            try:
                fixture_runs.append(
                    run_llm_repair_trial(
                        vault_root,
                        cluster=cluster or "harness_*",
                        speed_mode=speed_mode,
                        trinity_id=tid,
                        dry_run=False,
                        write_artifact=True,
                        trial_weaken_id=tid if weaken else None,
                        ensure_fixture=weaken,
                        restore_after=weaken,
                    )
                )
            except (OSError, ValueError) as e:
                fixture_runs.append({"ok": False, "trinity_id": tid, "error": str(e)})

        from .corps_conduct_repair_apply import run_conduct_repair_apply_trial

        try:
            fixture_runs.append(
                run_conduct_repair_apply_trial(
                    vault_root,
                    trinity_id=None,
                    max_apply=1,
                    dry_run=False,
                )
            )
        except (OSError, ValueError) as e:
            fixture_runs.append({"ok": False, "phase": "conduct_apply_trial", "error": str(e)})

    gate = evaluate_trial_cutover_gates(vault_root)
    report: dict[str, Any] = {
        "ok": gate.get("ok") is not False,
        "phase": "alternative_c_llm_repair_trial_track",
        "started_at": started,
        "completed_at": _now_iso(),
        "cluster_assess": assess,
        "fixture_runs": fixture_runs,
        "cutover_gate": gate,
    }

    if write_artifact:
        out_dir = vault_root / ARTIFACT_DIR
        out_dir.mkdir(parents=True, exist_ok=True)
        artifact = out_dir / f"llm-repair-trial-gate-{_stamp()}.json"
        artifact.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        report["artifact_path"] = str(artifact.relative_to(vault_root))

    append_metric_row(
        vault_root,
        {
            "metric_type": "llm_repair_trial_gate",
            "ok": report.get("ok"),
            "recommend_global_flip": gate.get("recommend_global_flip"),
        },
    )
    return report
