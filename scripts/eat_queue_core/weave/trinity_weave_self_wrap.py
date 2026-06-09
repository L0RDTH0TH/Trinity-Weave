"""Phase 9/10 — weave self-wrap: align → unclog → corps sweep → enforce → observe."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .config import load_trinity_config
from .governance import append_metric_row, ensure_weave_paths
from .trinity_align import apply_maintenance_trinity_align_gate, check, run_trinity_align
from .trinity_card_paths import list_provisional_trinity_card_ids
from .trinity_partition import load_maintenance_trinity_ids
from .trinity_spine_guard import respects_locked_spine

GRAPH_REL = Path(".technical/weave/spine-enforcement-graph.yaml")
PLAYBOOK_REL = Path(".technical/weave/trinity-disconnect-playbook.yaml")

# Weave entry points × cards × invariants (Phase 9 audit map).
SPINE_ENFORCEMENT_GRAPH: dict[str, Any] = {
    "schema_version": 1,
    "phase": 9,
    "charter": (
        "Maintenance aligns the Trinity spine, clears weave clogs so gauges stay truthful, "
        "and enforces that the running system never violates the locked spine — "
        "so a written card becomes the live center of the weave around it."
    ),
    "entry_points": [
        {
            "id": "write_lane_status_board",
            "module": "lane_status_board",
            "callable": "write_lane_status_board",
            "trinity_ids": [
                "lane_status_board",
                "lane_activity",
                "launch_registry_reconcile",
                "operator_surface_verifier",
            ],
            "pre_read_steps": ["reconcile_launch_registry"],
            "invariants": [
                "registry_reconcile_pre_read",
                "lane_run_authoritative_activity",
                "cq_lanesnapshot_canonical",
            ],
            "risk_tier": "low",
        },
        {
            "id": "headless_fanout_launch",
            "module": "headless_fanout",
            "callable": "headless_fanout",
            "trinity_ids": ["trinity_spine_maintenance", "launch_registry_reconcile"],
            "pre_read_steps": ["reconcile_launch_registry"],
            "invariants": ["registry_reconcile_pre_read"],
            "risk_tier": "medium",
        },
        {
            "id": "maintenance_eat_dispatch",
            "module": "maintenance_handlers",
            "callable": "handle_maintenance_entry",
            "trinity_ids": ["trinity_spine_maintenance", "weave_governance"],
            "pre_read_steps": [],
            "invariants": ["trinity_pack_consumable_only"],
            "risk_tier": "medium",
        },
        {
            "id": "trinity_spine_catchup",
            "module": "trinity_catchup_sweep",
            "callable": "run_spine_catchup_handler",
            "trinity_ids": ["trinity_spine_maintenance"],
            "pre_read_steps": [],
            "invariants": [],
            "risk_tier": "low",
            "delegates_to": "run_trinity_weave_self_wrap",
        },
        {
            "id": "trinity_pack_resolve",
            "module": "trinity_pack",
            "callable": "resolve_consumable_trinity_id",
            "trinity_ids": ["lane_status_board"],
            "pre_read_steps": [],
            "invariants": ["trinity_pack_consumable_only"],
            "risk_tier": "medium",
        },
        {
            "id": "write_trinity_card",
            "module": "trinity_card_paths",
            "callable": "write_trinity_card",
            "trinity_ids": ["trinity_spine_maintenance"],
            "pre_read_steps": [],
            "invariants": ["respects_locked_spine_on_write"],
            "risk_tier": "high",
        },
    ],
    "disconnect_classes": {
        "spine_drift": "Card legs misalign vs code — align_spine",
        "spine_violation_weave": "Runtime or corps breaks locked spine — block/repair",
        "clog": "Runtime plumbing blocks spine-required pre_read/resolvers — unclog",
        "gap": "Missing card for path — advisory only",
    },
}


def _now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def _load_yaml(path: Path) -> dict[str, Any]:
    import yaml  # type: ignore[import-untyped]

    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"expected YAML object: {path}")
    return data


def _dump_yaml(data: dict[str, Any]) -> str:
    import yaml  # type: ignore[import-untyped]

    return yaml.safe_dump(data, sort_keys=False, allow_unicode=True)


def spine_enforcement_graph_path(vault_root: Path) -> Path:
    return vault_root / GRAPH_REL


def build_spine_enforcement_graph() -> dict[str, Any]:
    graph = dict(SPINE_ENFORCEMENT_GRAPH)
    graph["generated_at"] = _now_iso()
    return graph


def write_spine_enforcement_graph(vault_root: Path, *, dry_run: bool = False) -> dict[str, Any]:
    vault_root = vault_root.resolve()
    ensure_weave_paths(vault_root)
    path = spine_enforcement_graph_path(vault_root)
    graph = build_spine_enforcement_graph()
    if not dry_run:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(_dump_yaml(graph), encoding="utf-8")
    return {
        "ok": True,
        "path": str(path.relative_to(vault_root)),
        "entry_point_count": len(graph.get("entry_points") or []),
        "dry_run": dry_run,
    }


def load_spine_enforcement_graph(vault_root: Path) -> dict[str, Any]:
    path = spine_enforcement_graph_path(vault_root)
    if path.is_file():
        return _load_yaml(path)
    return build_spine_enforcement_graph()


def _execute_pre_read_steps(vault_root: Path, steps: list[str]) -> list[str]:
    """Run declared pre_read steps; return completed step ids."""
    vault_root = vault_root.resolve()
    done: list[str] = []
    for step in steps:
        if step == "reconcile_launch_registry":
            from ..launch_registry_reconcile import reconcile_launch_registry

            reconcile_launch_registry(vault_root)
            done.append(step)
    return done


def _build_entry_point_probe_context(vault_root: Path, ep: dict[str, Any]) -> dict[str, Any]:
    """Build symbolic probe context; run graph pre_read_steps first."""
    eid = str(ep.get("id") or "")
    pre_reads = list(ep.get("pre_read_steps") or [])
    done = _execute_pre_read_steps(vault_root, pre_reads)
    ctx: dict[str, Any] = {
        "pre_read_steps": done,
        "integrity_ok": True,
    }
    if eid == "write_lane_status_board":
        ctx["resolver_used"] = "resolve_lane_activity"
        ctx["kernel_used"] = "build_lane_snapshots"
    return ctx


def _entry_point_invariant_ids(ep: dict[str, Any]) -> frozenset[str] | None:
    """Scope symbolic checks to invariants declared on the entry point."""
    raw = ep.get("invariants")
    if raw is None:
        return None
    if not isinstance(raw, list):
        return frozenset()
    return frozenset(str(x).strip() for x in raw if str(x).strip())


def _provisional_enforce_sample(vault_root: Path, *, limit: int = 12) -> list[str]:
    """Ids to spine-guard during enforce — prefer red nerves from last corps map."""
    from .trinity_provisional_corps_sweep import load_corps_nerve_map

    nmap = load_corps_nerve_map(vault_root)
    nerves = nmap.get("nerves") or []
    if isinstance(nerves, list) and nerves:
        red = [
            str(n.get("trinity_id"))
            for n in nerves
            if isinstance(n, dict) and n.get("status") == "red" and n.get("trinity_id")
        ]
        if red:
            return red[:limit]
        tested = [
            str(n.get("trinity_id"))
            for n in nerves
            if isinstance(n, dict) and n.get("trinity_id")
        ]
        if tested:
            return tested[:limit]
    return list_provisional_trinity_card_ids(vault_root)[:limit]


def _stale_inflight_max_minutes(vault_root: Path) -> float:
    cfg = load_trinity_config(vault_root)
    raw = getattr(cfg, "stale_inflight_max_minutes", None)
    if raw is not None:
        return float(raw)
    from ..merged_config import load_merged_yaml_blocks
    from ..overnight_config import load_overnight_config

    overnight = load_overnight_config(vault_root)
    max_min = float(overnight.get("stale_inflight_max_minutes") or 180)
    hd = load_merged_yaml_blocks(vault_root).get("harness_daemon")
    if isinstance(hd, dict) and hd.get("stale_inflight_max_minutes") is not None:
        max_min = float(hd["stale_inflight_max_minutes"])
    return max_min


def run_align_spine(
    vault_root: Path,
    *,
    dry_run: bool = False,
    operator_mutation_on_core: bool = False,
    lens_context: dict[str, Any] | None = None,
    align_scope_ids: list[str] | None = None,
) -> dict[str, Any]:
    """Pass 1 — align maintenance partition cards (core read-only unless operator flag).

    When align_scope_ids is set (expand_self), align only those ids.
    """
    vault_root = vault_root.resolve()
    cfg = load_trinity_config(vault_root)
    if not cfg.enabled:
        return {"ok": True, "skipped": True, "reason": "trinity_disabled"}

    if align_scope_ids is not None:
        scope = list(align_scope_ids)
    else:
        try:
            bundle = load_maintenance_trinity_ids(vault_root)
            scope = list(bundle.all)
        except (FileNotFoundError, OSError, ValueError) as e:
            return {"ok": False, "error": str(e)}

    if dry_run:
        out: dict[str, Any] = {"ok": True, "dry_run": True, "scope_count": len(scope)}
        if lens_context and not lens_context.get("skipped"):
            out["lens_context"] = {
                "lens_source": lens_context.get("lens_source"),
                "steering_tags": lens_context.get("steering_tags") or [],
                "meta_corpus_wiring": lens_context.get("meta_corpus_wiring"),
            }
        return out

    token = None
    if operator_mutation_on_core:
        from .trinity_dual_lock import operator_mutation_ctx

        token = operator_mutation_ctx.set(True)
    try:
        align = run_trinity_align(
            vault_root,
            trinity_ids=scope,
            pilot_only=False,
            update_meta=True,
        )
    finally:
        if token is not None:
            from .trinity_dual_lock import operator_mutation_ctx

            operator_mutation_ctx.reset(token)

    gate = apply_maintenance_trinity_align_gate(vault_root)
    failures = [
        r for r in (gate.get("maintenance_results") or gate.get("pilot_results") or [])
        if not r.get("ok", True) and not r.get("skipped")
    ]
    gate_ok = bool(gate.get("ok", True) or gate.get("skipped"))
    ok = gate_ok and len(failures) == 0
    result: dict[str, Any] = {
        "ok": ok,
        "align": align,
        "gate": gate,
        "failure_count": len(failures),
        "scope_count": len(scope),
        "align_scope_ids": align_scope_ids,
    }
    if lens_context and not lens_context.get("skipped"):
        result["lens_context"] = {
            "lens_source": lens_context.get("lens_source"),
            "steering_tags": lens_context.get("steering_tags") or [],
            "meta_corpus_wiring": lens_context.get("meta_corpus_wiring"),
        }
        wiring = lens_context.get("meta_corpus_wiring") or {}
        if not wiring.get("ok", True):
            result["lens_wiring_advisory"] = True
    return result


def run_weave_compliance_audit(
    vault_root: Path,
    *,
    strict: bool | None = None,
) -> dict[str, Any]:
    """Pass 2 — symbolic + pack consumable + spine guard sample."""
    vault_root = vault_root.resolve()
    cfg = load_trinity_config(vault_root)
    if strict is None:
        strict = bool(getattr(cfg, "spine_enforcement_strict", True))

    from .invariant_registry import bootstrap_phase9_invariants
    from .symbolic_conflict import evaluate_symbolic_conflict
    from ..lane_status_board import resolve_board_lanes
    from ..maintenance_io import MAINTENANCE_MODES
    from .trinity_pack import resolve_consumable_trinity_id

    inv_bootstrap = bootstrap_phase9_invariants(vault_root)
    graph = load_spine_enforcement_graph(vault_root)
    violations: list[dict[str, Any]] = []
    entry_results: list[dict[str, Any]] = []

    # Pack consumable for each maintenance mode.
    pack_rows: list[dict[str, Any]] = []
    for mode in sorted(MAINTENANCE_MODES):
        tid, extras = resolve_consumable_trinity_id(vault_root, queue_mode=mode)
        row = {"mode": mode, "trinity_id": tid}
        if extras.get("trinity_id_advisory"):
            row["advisory"] = extras["trinity_id_advisory"]
            violations.append(
                {
                    "class": "spine_violation_weave",
                    "check": "trinity_pack_consumable_only",
                    "detail": f"{mode} → non-consumable {extras['trinity_id_advisory']}",
                }
            )
        pack_rows.append(row)

    # Provisional spine guard sample (prefer red nerves from Phase 10 map).
    prov_violations = 0
    conduct_pending_ok = bool(getattr(cfg, "corps_conduct_pending_ok", False))
    for pid in _provisional_enforce_sample(vault_root, limit=12):
        guard = respects_locked_spine(vault_root, pid)
        if guard.ok:
            continue
        kinds = [v.kind for v in guard.violations]
        if conduct_pending_ok and kinds and all(
            k in ("disconnect_precedence_collapse", "disconnect_error_narrative_drift")
            for k in kinds
        ):
            # Shape-only debt — nerve test yellow; not enforce-hard-fail when conduct pending OK.
            continue
        prov_violations += 1
        violations.append(
            {
                "class": "spine_violation_weave",
                "check": "respects_locked_spine",
                "trinity_id": pid,
                "detail": str(guard.to_dict().get("violations") or [])[:400],
            }
        )

    # Per entry-point symbolic probe (invariant-scoped + pre_read executed).
    for ep in graph.get("entry_points") or []:
        if not isinstance(ep, dict):
            continue
        eid = str(ep.get("id") or "")
        inv_ids = _entry_point_invariant_ids(ep)
        if inv_ids is not None and len(inv_ids) == 0:
            entry_results.append(
                {
                    "entry_point": eid,
                    "decision": "proceed",
                    "blocked": False,
                    "skipped": True,
                    "reason": "no_symbolic_invariants",
                }
            )
            continue
        ctx = _build_entry_point_probe_context(vault_root, ep)
        sym = evaluate_symbolic_conflict(
            vault_root,
            context=ctx,
            risk_tier=str(ep.get("risk_tier") or "low"),
            invariant_ids=inv_ids,
        )
        row = {
            "entry_point": eid,
            "decision": sym.decision,
            "blocked": sym.blocked,
            "temporal": sym.temporal_inconsistencies,
            "drift": sym.cross_surface_drift_risks,
            "invariants_checked": sorted(inv_ids) if inv_ids is not None else None,
        }
        entry_results.append(row)
        if sym.temporal_inconsistencies or sym.cross_surface_drift_risks:
            violations.append(
                {
                    "class": "spine_violation_weave",
                    "entry_point": eid,
                    "decision": sym.decision,
                    "detail": (sym.temporal_inconsistencies or sym.cross_surface_drift_risks)[:3],
                }
            )
        elif sym.decision == "block" and strict:
            violations.append(
                {
                    "class": "spine_violation_weave",
                    "entry_point": eid,
                    "decision": sym.decision,
                    "detail": sym.violated_invariants[:3],
                }
            )

    # Live board-path probe after reconcile.
    try:
        from ..launch_registry_reconcile import reconcile_launch_registry

        reconcile_launch_registry(vault_root)
        from ..lane_activity import resolve_lane_activity

        for ln in resolve_board_lanes(vault_root):
            act = resolve_lane_activity(vault_root, ln)
            if act.get("run_status") == "running" and not act.get("why_hint"):
                violations.append(
                    {
                        "class": "clog",
                        "lane": ln,
                        "detail": "running without why_hint after reconcile",
                    }
                )
    except OSError as e:
        violations.append({"class": "clog", "detail": f"activity_probe_failed: {e}"})

    ok = len(violations) == 0
    if strict and violations:
        ok = False

    return {
        "ok": ok,
        "strict": strict,
        "invariant_bootstrap": inv_bootstrap,
        "pack_modes_checked": len(pack_rows),
        "provisional_spine_violations": prov_violations,
        "entry_points": entry_results,
        "violations": violations,
        "violation_count": len(violations),
    }


def run_unclog_weave(
    vault_root: Path,
    *,
    dry_run: bool = False,
) -> dict[str, Any]:
    """Pass 3 — registry reconcile, stale in_flight, per-lane lock/orchestration clears."""
    vault_root = vault_root.resolve()
    if dry_run:
        return {"ok": True, "dry_run": True}

    from ..harness_daemon import clear_stale_in_flight
    from ..launch_registry_reconcile import reconcile_launch_registry
    from ..lane_activity import auto_clear_stale_lane_locks
    from ..lane_status_board import resolve_board_lanes

    out: dict[str, Any] = {"ok": True}
    max_min = _stale_inflight_max_minutes(vault_root)
    out["registry"] = reconcile_launch_registry(vault_root)
    out["stale_inflight"] = clear_stale_in_flight(vault_root, max_minutes=max_min)
    per_lane: list[dict[str, Any]] = []
    for ln in resolve_board_lanes(vault_root):
        per_lane.append(auto_clear_stale_lane_locks(vault_root, ln))
    out["per_lane"] = per_lane
    return out


def ensure_phase9_playbook_clog_entries(vault_root: Path) -> dict[str, Any]:
    """Merge clog / weave_clog disconnect kinds into playbook if missing."""
    vault_root = vault_root.resolve()
    path = vault_root / PLAYBOOK_REL
    if not path.is_file():
        return {"ok": False, "skipped": True, "reason": "playbook_missing"}

    data = _load_yaml(path)
    entries = list(data.get("entries") or [])
    if not isinstance(entries, list):
        entries = []

    clog_actions = (
        {
            "disconnect_kind": "clog",
            "applies_to": "bone",
            "action": "weave_unclog",
            "priority": 5,
            "params": {"steps": ["reconcile_launch_registry", "clear_stale_in_flight", "auto_clear_stale_lane_locks"]},
        },
        {
            "disconnect_kind": "weave_clog",
            "applies_to": "bridge",
            "action": "queue_TRINITY_SPINE_CATCHUP",
            "priority": 4,
            "params": {"handler": "run_trinity_weave_self_wrap"},
        },
    )
    existing_kinds = {
        (str(e.get("disconnect_kind")), str(e.get("applies_to")), str(e.get("action")))
        for e in entries
        if isinstance(e, dict)
    }
    added: list[str] = []
    for spec in clog_actions:
        key = (spec["disconnect_kind"], spec["applies_to"], spec["action"])
        if key in existing_kinds:
            continue
        entries.append(spec)
        added.append(spec["disconnect_kind"])
    if added:
        data["entries"] = entries
        if "disconnect_classes" not in data:
            data["disconnect_classes"] = {}
        dc = data["disconnect_classes"]
        if isinstance(dc, dict):
            dc.setdefault(
                "clog",
                "Spine correct; runtime plumbing blocks pre_read/resolvers (Phase 9)",
            )
        path.write_text(_dump_yaml(data), encoding="utf-8")
    return {"ok": True, "added": added}


def run_observe(
    vault_root: Path,
    *,
    dry_run: bool = False,
    skip_board: bool = False,
) -> dict[str, Any]:
    """Pass 4 — board refresh as observatory (after unclog)."""
    if dry_run or skip_board:
        return {"ok": True, "skipped": True, "dry_run": dry_run}
    from ..lane_status_board import write_lane_status_board

    board = write_lane_status_board(vault_root)
    ok = bool(board.get("ok")) and bool(board.get("integrity_ok"))
    return {
        "ok": ok,
        "integrity_ok": board.get("integrity_ok"),
        "trinity_align": board.get("trinity_align"),
        "system_attention": board.get("system_attention"),
    }


def _operator_next_steps(
    *,
    operator_mode: str,
    cycle_ok: bool,
    pass_gate_ok: bool,
    regen_requested: bool,
    red_ids: list[str],
    scope_ids: list[str] | None = None,
) -> list[str]:
    if not cycle_ok:
        return [
            "Fix operator_outcome.infra_failures first, then re-run the same command.",
        ]
    if operator_mode == "expand_self_delta":
        steps = [
            "expand_self delta wrap completed for scoped ids only.",
            "Review pass_gate for scope — full corpus unchanged.",
            "When stable, operator may lock cards or queue usage_proven candidacy (not auto).",
        ]
        if scope_ids:
            steps.append(
                f"Scope ({len(scope_ids)}): "
                + ", ".join(scope_ids[:8])
                + ("…" if len(scope_ids) > 8 else "")
            )
        if red_ids:
            steps.append(f"Scope reds ({len(red_ids)}): " + ", ".join(red_ids[:8]))
        return steps
    if pass_gate_ok:
        return [
            "Full corpus pass_gate is green; enforcement ran if conduct_ok was true.",
        ]
    if operator_mode == "acceptance_audit_only":
        steps = [
            "You ran acceptance audit only (no --regenerate-complete). "
            "ok:false means the corpus is not fully green — not that the harness crashed.",
            "Do not re-run --regenerate-complete unless you want another scorched-earth burn.",
            "Fix red_ids (conduct tests, contract.proof wiring, stale touch), then re-run self-wrap.",
        ]
    else:
        steps = [
            "Scorched-earth: mint as close to perfect as possible; repair loop owns green.",
            "Post-regen reds are expected — Honest Green requires pass_gate_ok after repair laps.",
            "If repair_loop stop_reason is repair_stuck_* or manual_required, automation exhausted (burn failed).",
            "Re-run self-wrap WITHOUT --regenerate-complete only to verify fixes after a successful burn.",
        ]
    if red_ids:
        steps.append(f"Red cards ({len(red_ids)}): " + ", ".join(red_ids[:8]) + ("…" if len(red_ids) > 8 else ""))
    return steps


def build_operator_outcome(report: dict[str, Any]) -> dict[str, Any]:
    """Plain readout: cycle infra vs corpus pass_gate (operator trust contract)."""
    dry_run = bool(report.get("dry_run"))
    regen_requested = bool(report.get("regenerate_complete_requested"))
    rc = report.get("regenerate_complete") or {}
    pg = report.get("pass_gate") or {}
    cs = report.get("corps_sweep") or {}

    infra_failures: list[str] = []
    for step in ("align_spine", "unclog", "host_weld_sync", "knob_parity", "honesty_anchor"):
        block = report.get(step) or {}
        if block and not block.get("ok", True) and not block.get("skipped"):
            infra_failures.append(step)

    if regen_requested and not dry_run:
        if not rc:
            infra_failures.append("regenerate_complete:missing_block")
        elif not rc.get("skipped") and not rc.get("ok", True):
            infra_failures.append(f"regenerate_complete:{rc.get('reason') or 'failed'}")
        tc = rc.get("test_compensation") or {}
        if tc and not tc.get("skipped") and tc.get("compensation_ok") is False:
            vf = len(tc.get("verification_failures") or tc.get("pytest_failures") or [])
            infra_failures.append(f"test_compensation:{vf}_proof_verification_failures")

    enforce = report.get("enforce_in_weave") or {}
    if enforce and not enforce.get("ok", True) and not enforce.get("skipped"):
        reason = str(enforce.get("reason") or "")
        if "conduct_ok_false" not in reason:
            infra_failures.append("enforce_in_weave")

    cycle_ok = len(infra_failures) == 0
    full_corpus = bool(report.get("corps_full_corpus"))
    scope_locked_report = bool(report.get("scope_locked"))
    if scope_locked_report:
        pass_gate_ok = bool(pg.get("ok")) if pg else False
    else:
        pass_gate_ok = bool(pg.get("ok")) if pg else (not full_corpus and not dry_run)

    if regen_requested and rc and not dry_run and not rc.get("skipped"):
        archived_n = int(rc.get("archived_card_count") or rc.get("eligible_card_count") or 0)
        regen_n = int(rc.get("regenerated_count") or 0)
        if not rc.get("ok", True) or (archived_n > 0 and regen_n == 0):
            pass_gate_ok = False

    if dry_run:
        operator_mode = "dry_run_preview"
    elif report.get("expand_self"):
        operator_mode = "expand_self_delta"
    elif regen_requested:
        operator_mode = "regen_burn_plus_acceptance"
    else:
        operator_mode = "acceptance_audit_only"

    counts = dict(pg.get("counts") or {})
    red_ids = list(pg.get("red_ids") or [])
    green_n = counts.get("green")
    red_n = counts.get("red", len(red_ids))

    if dry_run:
        summary = "Dry run — no vault writes. See dry_run_preview for pass_gate estimate."
    elif not cycle_ok:
        summary = (
            "Infrastructure failure — cycle did not finish cleanly "
            f"({'; '.join(infra_failures)}). Not a corpus readiness score."
        )
    elif pass_gate_ok and report.get("expand_self"):
        summary = (
            f"expand_self scope pass_gate GREEN ({green_n} green in scope). "
            "Full corpus not re-tested."
        )
    elif report.get("expand_self"):
        summary = (
            f"expand_self scope NOT green: {green_n} green / {red_n} red in scope. "
            "Fix scope cards, re-run expand_self."
        )
    elif pass_gate_ok:
        summary = f"Cycle OK; full corpus pass_gate GREEN ({green_n} green)."
    elif operator_mode == "acceptance_audit_only":
        summary = (
            f"Cycle OK (acceptance audit only — no regen). Corpus NOT green: "
            f"{green_n} green / {red_n} red. This is expected until red cards are fixed."
        )
    else:
        baseline = rl.get("gen_red_baseline") or report.get("gen_red_baseline") or {}
        baseline_note = ""
        if baseline.get("red_count") is not None:
            baseline_note = (
                f" Post-gen baseline: {baseline.get('green_count', '?')} green / "
                f"{baseline.get('red_count')} red ({baseline.get('gen_green_pct', '?')}% green)."
            )
        repair_note = ""
        if repair_stop == "pass_gate_green":
            repair_note = " Repair loop reached Honest Green."
        elif repair_stop:
            repair_note = f" Repair loop stopped: {repair_stop}."
        summary = (
            f"Regen burn finished; corpus NOT green: {green_n} green / {red_n} red."
            f"{baseline_note}{repair_note}"
        )

    tc = rc.get("test_compensation") or {}
    rl = cs.get("repair_loop") or {}
    repair_stop = rl.get("stop_reason")
    lens_align = bool(report.get("meta_lens_force_align_requested")) or bool(
        rc.get("meta_lens_force_align")
    )
    if lens_align and regen_requested and cycle_ok and not dry_run:
        summary = summary + " Meta-lens force-align applied on regen."
    manual_test_ids: list[str] = []
    if rl.get("laps"):
        last_repair = (rl["laps"][-1].get("repair") or {})
        manual_test_ids = list(
            (last_repair.get("test_code") or {}).get("manual_required_ids")
            or last_repair.get("manual_required_ids")
            or []
        )
    return {
        "cycle_ok": cycle_ok,
        "pass_gate_ok": pass_gate_ok,
        "operator_mode": operator_mode,
        "summary": summary,
        "infra_failures": infra_failures,
        "regenerate_complete_requested": regen_requested,
        "meta_lens_force_align": lens_align,
        "regenerate_complete_ok": rc.get("ok") if rc else None,
        "compensation_ok": tc.get("compensation_ok") if tc else None,
        "nerve_tested": pg.get("tested") or (cs.get("nerve_test") or {}).get("tested"),
        "counts": counts,
        "red_ids": red_ids,
        "repair_loop_stop_reason": repair_stop,
        "gen_red_baseline": rl.get("gen_red_baseline") or report.get("gen_red_baseline"),
        "test_code_manual_required_ids": manual_test_ids[:12],
        "next_steps": _operator_next_steps(
            operator_mode=operator_mode,
            cycle_ok=cycle_ok,
            pass_gate_ok=pass_gate_ok,
            regen_requested=regen_requested,
            red_ids=red_ids,
            scope_ids=list(report.get("expand_self_scope_ids") or ()),
        ),
        "legacy_ok_field": "pass_gate_ok",
    }


def run_trinity_weave_self_wrap(
    vault_root: Path,
    *,
    dry_run: bool = False,
    skip_align: bool = False,
    skip_enforce: bool = False,
    skip_unclog: bool = False,
    skip_corps: bool = False,
    skip_observe: bool = False,
    operator_mutation_on_core: bool = False,
    write_graph: bool = True,
    write_report: bool = True,
    corps_cluster: str | None = None,
    corps_full_corpus: bool | None = None,
    corps_sample_only: bool = False,
    corps_max_laps: int | None = None,
    corps_max_llm_laps: int | None = None,
    corps_auto_repair: bool | None = None,
    corps_llm_repair: bool | None = None,
    corps_llm_repair_force: bool = False,
    corps_speed_mode: str | None = None,
    regenerate_complete: bool = False,
    meta_lens_force_align: bool = False,
    host_weld_bootstrap_all: bool = False,
    expand_self: bool = False,
    expand_self_scope_ids: tuple[str, ...] | None = None,
) -> dict[str, Any]:
    """Combined maintenance cycle: load_mvl_bundle → align → unclog → corps → enforce → observe."""
    vault_root = vault_root.resolve()
    cfg = load_trinity_config(vault_root)
    if not getattr(cfg, "weave_self_wrap_enabled", True):
        return {"ok": True, "skipped": True, "reason": "weave_self_wrap_disabled"}

    if expand_self and regenerate_complete:
        return {
            "ok": False,
            "error": "expand_self_forbids_regenerate_complete",
            "hint": "Scorched earth is operator-initiated only; use full self-wrap without --expand-self",
        }

    if expand_self and not getattr(cfg, "expand_self_enabled", True):
        return {"ok": True, "skipped": True, "reason": "expand_self_disabled"}

    scope_locked = bool(expand_self and expand_self_scope_ids)

    if expand_self:
        full_corpus = False
    elif corps_sample_only:
        full_corpus = False
    elif corps_full_corpus is not None:
        full_corpus = bool(corps_full_corpus)
    else:
        full_corpus = bool(getattr(cfg, "corps_self_wrap_full_corpus", True))

    ensure_weave_paths(vault_root)
    report: dict[str, Any] = {
        "ok": True,
        "phase": "14-expand_self" if expand_self else "9+10",
        "expand_self": bool(expand_self),
        "expand_self_scope_ids": list(expand_self_scope_ids or ()),
        "scope_locked": scope_locked,
        "pass_gate_articulation": (
            "Scoped delta: every id in expand_self scope has touch, rules, and conduct aligned."
            if expand_self
            else (
                "Spine aligned on maintenance core; every non-maintenance-core provisional "
                "has touch, rules, and conduct aligned to its card."
            )
        ),
        "corps_full_corpus": full_corpus,
        "regenerate_complete_requested": bool(regenerate_complete),
        "meta_lens_force_align_requested": bool(meta_lens_force_align),
        "cycle_order": [
            "load_mvl_bundle",
            "align_spine",
            "mvl_lens",
            "meta_corpus_charter",
            "host_weld_sync",
            "knob_parity",
            "honesty_anchor",
            "unclog",
            "regenerate_complete",
            "corps_sweep",
            "enforce_in_weave",
            "observe",
        ],
        "dry_run": dry_run,
        "started_at": _now_iso(),
    }

    if write_graph:
        report["graph"] = write_spine_enforcement_graph(vault_root, dry_run=dry_run)

    if not dry_run:
        report["playbook_clog"] = ensure_phase9_playbook_clog_entries(vault_root)

    lens_bundle: dict[str, Any] = {}
    if not dry_run and getattr(cfg, "mvl_conductor_enabled", True):
        from .trinity_lens_informed_align import load_mvl_bundle

        lens_bundle = load_mvl_bundle(vault_root)
        report["load_mvl_bundle"] = lens_bundle
        if not lens_bundle.get("ok", True) and not lens_bundle.get("skipped"):
            report["ok"] = False

    if not skip_align:
        report["align_spine"] = run_align_spine(
            vault_root,
            dry_run=dry_run,
            operator_mutation_on_core=operator_mutation_on_core,
            lens_context=lens_bundle if lens_bundle and not lens_bundle.get("skipped") else None,
            align_scope_ids=list(expand_self_scope_ids) if expand_self_scope_ids else None,
        )
        if not report["align_spine"].get("ok"):
            report["ok"] = False

    if not dry_run and getattr(cfg, "mvl_conductor_enabled", True):
        from .trinity_lens_informed_align import run_lens_informed_align_gate

        report["mvl_lens"] = run_lens_informed_align_gate(vault_root)
        if not report["mvl_lens"].get("ok", True) and not report["mvl_lens"].get("skipped"):
            report["ok"] = False

    if not dry_run:
        from .trinity_meta_corpus import meta_corpus_charter_status

        report["meta_corpus_charter"] = meta_corpus_charter_status(vault_root)

    if full_corpus and not expand_self and getattr(cfg, "host_weld_sync_enabled", True):
        from .trinity_host_weld_sync import run_host_weld_sync

        report["host_weld_sync"] = run_host_weld_sync(
            vault_root,
            dry_run=dry_run,
            full_corpus=True,
            bootstrap_all=bool(host_weld_bootstrap_all),
        )
        hw = report["host_weld_sync"]
        if hw and not hw.get("ok", True) and not hw.get("skipped"):
            report["ok"] = False
            if hw.get("blocked"):
                report["host_weld_blocked"] = True

    if full_corpus and not expand_self and getattr(cfg, "knob_parity_enabled", True):
        from .trinity_knob_parity import run_knob_parity_proofs

        report["knob_parity"] = run_knob_parity_proofs(
            vault_root,
            dry_run=dry_run,
            write_artifact=not dry_run,
        )
        kp = report["knob_parity"]
        if kp and not kp.get("ok", True) and not kp.get("skipped"):
            report["ok"] = False

    if full_corpus and not expand_self and getattr(cfg, "honesty_anchor_enabled", True):
        from .trinity_honesty_anchor import run_honesty_anchor_proofs

        report["honesty_anchor"] = run_honesty_anchor_proofs(
            vault_root,
            dry_run=dry_run,
            write_artifact=not dry_run,
        )
        ha = report["honesty_anchor"]
        if ha and not ha.get("ok", True) and not ha.get("skipped"):
            report["ok"] = False

    if not skip_unclog:
        report["unclog"] = run_unclog_weave(vault_root, dry_run=dry_run)
        if not report["unclog"].get("ok", True):
            report["ok"] = False

    if regenerate_complete:
        if dry_run:
            report["regenerate_complete"] = {
                "ok": True,
                "skipped": True,
                "reason": "dry_run",
            }
        else:
            from .corps_corpus_regenerate import run_regenerate_complete

            report["regenerate_complete"] = run_regenerate_complete(
                vault_root,
                dry_run=False,
                operator_mutation_on_core=operator_mutation_on_core,
                cli_requested=True,
                meta_lens_force_align=bool(meta_lens_force_align),
            )
            rc = report["regenerate_complete"]
            if not rc.get("ok", True) and not rc.get("skipped"):
                report["ok"] = False

    run_corps = (
        not skip_corps
        and cfg.corps_sweep_enabled
        and cfg.corps_sweep_before_enforce
        and not dry_run
    )
    if run_corps:
        from .corps_auto_repair import run_corps_sweep_with_repair_loop
        from .corps_llm_repair import LlmRepairRunContext

        do_repair = (
            bool(getattr(cfg, "corps_auto_repair_enabled", True))
            if corps_auto_repair is None
            else bool(corps_auto_repair)
        )
        llm_ctx = LlmRepairRunContext(
            cluster=corps_cluster,
            speed_mode=corps_speed_mode or "balance",
            harness_enable_llm=bool(corps_llm_repair),
            harness_force=bool(corps_llm_repair_force),
        )
        if do_repair and full_corpus and not expand_self:
            regen_ok = bool(
                (report.get("regenerate_complete") or {}).get("ok")
                and not (report.get("regenerate_complete") or {}).get("skipped")
            )
            report["corps_sweep"] = run_corps_sweep_with_repair_loop(
                vault_root,
                dry_run=False,
                cluster=corps_cluster,
                apply_hygiene=cfg.corps_sweep_auto_hygiene,
                full_corpus=True,
                max_laps=corps_max_laps,
                max_llm_laps=corps_max_llm_laps,
                auto_repair=True,
                llm_repair_enabled=corps_llm_repair,
                llm_repair_context=llm_ctx,
                llm_repair_speed_mode=corps_speed_mode,
                llm_repair_force=corps_llm_repair_force,
                write_map=True,
                capture_gen_red_baseline=bool(regenerate_complete and regen_ok),
            )
            baseline = (report["corps_sweep"].get("repair_loop") or {}).get(
                "gen_red_baseline"
            )
            if baseline:
                report["gen_red_baseline"] = baseline
        else:
            from .trinity_provisional_corps_sweep import run_trinity_provisional_corps_sweep

            expand_laps = 2 if expand_self else None
            report["corps_sweep"] = run_trinity_provisional_corps_sweep(
                vault_root,
                dry_run=False,
                cluster=corps_cluster,
                scope_ids=expand_self_scope_ids if expand_self else None,
                apply_hygiene=cfg.corps_sweep_auto_hygiene,
                full_corpus=full_corpus,
                scope_locked=scope_locked,
                write_map=True,
                lap=1,
                max_llm_attempts=corps_max_llm_laps,
                llm_repair_enabled=corps_llm_repair,
                llm_repair_context=llm_ctx,
            )
            if expand_self and expand_laps and expand_laps > 1:
                pg = report["corps_sweep"].get("pass_gate") or {}
                if not pg.get("ok") and do_repair:
                    lap2 = run_trinity_provisional_corps_sweep(
                        vault_root,
                        dry_run=False,
                        cluster=corps_cluster,
                        scope_ids=expand_self_scope_ids,
                        apply_hygiene=False,
                        full_corpus=False,
                        scope_locked=scope_locked,
                        write_map=True,
                        lap=2,
                        max_llm_attempts=corps_max_llm_laps,
                        llm_repair_enabled=corps_llm_repair,
                        llm_repair_context=llm_ctx,
                    )
                    report["corps_sweep_lap2"] = lap2
                    report["corps_sweep"] = lap2
        report["pass_gate"] = report["corps_sweep"].get("pass_gate") or {}
        if not report["corps_sweep"].get("ok", True) and not report["corps_sweep"].get("skipped"):
            report["ok"] = False
        elif full_corpus and not report.get("pass_gate", {}).get("ok", True):
            report["ok"] = False
    elif dry_run and not skip_corps:
        report["corps_sweep"] = {"ok": True, "skipped": True, "reason": "dry_run"}
    elif skip_corps:
        report["corps_sweep"] = {"ok": True, "skipped": True, "reason": "skip_corps"}

    if not skip_enforce and not dry_run:
        pass_gate = report.get("pass_gate") or {}
        conduct_ok = pass_gate.get("conduct_ok")
        if conduct_ok is False:
            report["provisional_enforcement_untrusted"] = True
            report["enforce_in_weave"] = {
                "ok": True,
                "skipped": True,
                "reason": "conduct_ok_false_provisional_enforcement_untrusted",
                "conduct_red_count": pass_gate.get("tier_failures", {}).get("conduct"),
            }
        else:
            report["enforce_in_weave"] = run_weave_compliance_audit(vault_root)
            if not report["enforce_in_weave"].get("ok"):
                report["ok"] = False
    elif dry_run and not skip_enforce:
        report["enforce_in_weave"] = {"ok": True, "skipped": True, "reason": "dry_run"}

    if not skip_observe:
        report["observe"] = run_observe(vault_root, dry_run=dry_run)

    if dry_run:
        from .weave_dry_run_preview import build_weave_dry_run_preview

        report["dry_run_preview"] = build_weave_dry_run_preview(
            vault_root,
            full_corpus=full_corpus,
            regenerate_complete=bool(regenerate_complete),
            meta_lens_force_align=bool(meta_lens_force_align),
        )
        pg = report["dry_run_preview"].get("pass_gate") or {}
        if pg:
            report["pass_gate"] = pg
        report["ok"] = True

    report["operator_outcome"] = build_operator_outcome(report)

    if not dry_run and write_report:
        val_dir = vault_root / ".technical" / "weave" / "validation"
        val_dir.mkdir(parents=True, exist_ok=True)
        rp = val_dir / f"trinity-weave-self-wrap-{_stamp()}.json"
        rp.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        report["report_path"] = str(rp)

    append_metric_row(
        vault_root,
        {
            "metric_type": "trinity_weave_self_wrap",
            "ok": report.get("ok"),
            "dry_run": dry_run,
            "violation_count": (report.get("enforce_in_weave") or {}).get("violation_count"),
        },
    )
    report["completed_at"] = _now_iso()
    return report


def maybe_pre_render_weave_hygiene(vault_root: Path) -> dict[str, Any] | None:
    """Hook before board write when Phase 9 pre-render hygiene enabled."""
    cfg = load_trinity_config(vault_root)
    if not cfg.enabled or not getattr(cfg, "weave_self_wrap_enabled", True):
        return None
    if not getattr(cfg, "clog_pass_before_board", True):
        return None
    return run_unclog_weave(vault_root, dry_run=False)


def assert_weave_entry_point(
    vault_root: Path,
    entry_point_id: str,
    *,
    context: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Entry-point gate (headless fanout, etc.) — returns blocked + decision."""
    vault_root = vault_root.resolve()
    cfg = load_trinity_config(vault_root)
    if not cfg.enabled or not getattr(cfg, "weave_self_wrap_enabled", True):
        return {"ok": True, "skipped": True}

    graph = load_spine_enforcement_graph(vault_root)
    ep = next(
        (e for e in (graph.get("entry_points") or []) if isinstance(e, dict) and e.get("id") == entry_point_id),
        None,
    )
    if not ep:
        return {"ok": True, "skipped": True, "reason": "unknown_entry_point"}

    from .symbolic_conflict import evaluate_symbolic_conflict

    ctx = dict(context or {})
    inv_ids = _entry_point_invariant_ids(ep) if ep else None
    declared = list(ep.get("pre_read_steps") or []) if ep else []
    done = _execute_pre_read_steps(vault_root, declared)
    ctx["pre_read_steps"] = list(dict.fromkeys(list(ctx.get("pre_read_steps") or []) + done))

    sym = evaluate_symbolic_conflict(
        vault_root,
        context=ctx,
        risk_tier=str(ep.get("risk_tier") or "medium") if ep else "medium",
        invariant_ids=inv_ids,
    )
    strict = bool(getattr(cfg, "spine_enforcement_strict", True))
    blocked = sym.blocked or (strict and sym.decision == "block")
    return {
        "ok": not blocked,
        "entry_point": entry_point_id,
        "decision": sym.decision,
        "blocked": blocked,
        "violations": sym.temporal_inconsistencies + sym.cross_surface_drift_risks,
    }


def maybe_weave_self_wrap_on_pseudo_clock(vault_root: Path) -> dict[str, Any] | None:
    """Optional pseudo_clock_tick hook — full Phase 9 cycle (observe includes board)."""
    cfg = load_trinity_config(vault_root)
    if not cfg.enabled:
        return None
    if not getattr(cfg, "weave_self_wrap_on_pseudo_clock", False):
        return None
    return run_trinity_weave_self_wrap(
        vault_root,
        dry_run=False,
        operator_mutation_on_core=False,
        write_graph=False,
    )

