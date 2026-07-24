"""Deterministic handlers for roadmap factory queue modes."""

from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from ..persona_handoff import build_persona_envelope, save_half_a_provenance_sidecar, synthetic_persona_attestation
from ..factory.factory_output_gate import parse_factory_orchestrator_yaml
from ..factory.factory_pq_stage import stage_factory_dispatch_to_pq
from .beat_auto_generate import run_beat_auto_generate
from .catalog_coverage import run_catalog_coverage, run_catalog_freeze_gate
from .catalog_mint_propose import propose_catalog_from_pmg
from .ux_mint_backlog import freeze_mint_backlog, generate_ux_mint_backlog
from .rollout_slicer import run_rollout_slicer
from .user_story_brief import write_user_story_brief

# Legacy alias — same handler as BOOTSTRAP (reset factory cursor + tick).
ROADMAP_FACTORY_RELAUNCH = "ROADMAP_FACTORY_RELAUNCH"
ROADMAP_FACTORY_BOOTSTRAP = "ROADMAP_FACTORY_BOOTSTRAP"

ROADMAP_FACTORY_MODE_ALIASES: dict[str, str] = {
    ROADMAP_FACTORY_RELAUNCH: ROADMAP_FACTORY_BOOTSTRAP,
}

ROADMAP_FACTORY_MODES = frozenset(
    {
        ROADMAP_FACTORY_BOOTSTRAP,
        ROADMAP_FACTORY_RELAUNCH,
        "PRODUCT_FACTORY_CONTINUE",
        "SET_ROLLOUT_BUDGET",
        "BEAT_GENERATE",
        "CATALOG_COVERAGE",
        "CATALOG_FREEZE_CHECK",
        "USER_STORY_BRIEF",
        "ROADMAP_FACTORY_STAGE_FACTORY",
        "CATALOG_MINT_PROPOSE",
        "UX_MINT_BACKLOG",
        "DEPTH_SLICE",
        "L5_SCOPE_AUTHOR",
    }
)


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _normalize_mode(mode: str) -> str:
    m = str(mode or "").strip().upper().replace(" ", "_").replace("-", "_")
    return ROADMAP_FACTORY_MODE_ALIASES.get(m, m)


def _project_id(entry: dict[str, Any]) -> str:
    params = entry.get("params") if isinstance(entry.get("params"), dict) else {}
    return str(entry.get("project_id") or params.get("project_id") or "genesis-mythos-master")


def _default_rollout(vault_root: Path, project_id: str) -> list[dict[str, Any]]:
    cfg = parse_factory_orchestrator_yaml(vault_root / "3-Resources/Second-Brain-Config.md")
    rf = cfg.get("roadmap_factory") if isinstance(cfg.get("roadmap_factory"), dict) else {}
    rows = rf.get("default_rollout")
    if isinstance(rows, list) and rows:
        return [dict(x) for x in rows if isinstance(x, dict)]
    return [{"row_id": "ui_presentation_shell", "target_depth": 2}]


def handle_roadmap_factory_entry(vault_root: Path, entry: dict[str, Any]) -> dict[str, Any]:
    """Process one roadmap-factory queue line (harness Layer 1, no Task subagent)."""
    vault_root = vault_root.resolve()
    eid = str(entry.get("id") or "")
    mode = _normalize_mode(str(entry.get("mode") or ""))
    params = entry.get("params") if isinstance(entry.get("params"), dict) else {}
    project_id = _project_id(entry)

    if mode not in ROADMAP_FACTORY_MODES:
        return {"ok": False, "id": eid, "error": "unknown_roadmap_factory_mode", "mode": mode}

    if mode in (ROADMAP_FACTORY_BOOTSTRAP, "PRODUCT_FACTORY_CONTINUE"):
        from .done_when_eval import loop2_exit_honestly_eligible

        action = str(params.get("action") or "tick").lower().replace("-", "_")
        if loop2_exit_honestly_eligible(vault_root, project_id) and action != "eat_factory_lanes":
            return {
                "ok": True,
                "id": eid,
                "mode": mode,
                "skipped": True,
                "reason": "loop2_exit_eligible",
            }

    if mode == "UX_MINT_BACKLOG":
        params.setdefault(
            "persona_handoff",
            build_persona_envelope(persona_id="half_a.catalog_ux_indexer"),
        )
        action = str(params.get("action") or "generate").lower().replace("-", "_")
        pmg = params.get("pmg_path")
        if action == "freeze":
            out = freeze_mint_backlog(vault_root, project_id)
            result = {"ok": bool(out.get("ok")), "id": eid, "mode": mode, "action": action, **out}
        else:
            gen = generate_ux_mint_backlog(
                vault_root,
                project_id=project_id,
                pmg_path=vault_root / str(pmg) if pmg else None,
            )
            result = {"ok": gen.ok, "id": eid, "mode": mode, "action": action, **gen.to_dict()}
            if params.get("freeze_after") is True and gen.coverage_ok:
                fr = freeze_mint_backlog(vault_root, project_id)
                result["freeze"] = fr
                result["ok"] = bool(fr.get("ok"))
        if result.get("ok"):
            from .catalog_mint_pack import emit_catalog_mint_pack

            if action == "freeze" or params.get("emit_pack") is True:
                pack = emit_catalog_mint_pack(vault_root, project_id=project_id)
                result["pack"] = pack.to_dict()
            backlog_rel = f"1-Projects/{project_id}/Roadmap/User-Story/MINT-BACKLOG.yaml"
            att = synthetic_persona_attestation(
                "half_a.catalog_ux_indexer",
                [backlog_rel],
            )
            save_half_a_provenance_sidecar(
                vault_root,
                project_id=project_id,
                phase="catalog_mint",
                persona_attestation=att,
                artifacts={"mint_backlog": backlog_rel},
            )
            result["persona_attestation"] = att
        return result

    if mode == "CATALOG_MINT_PROPOSE":
        params.setdefault(
            "persona_handoff",
            build_persona_envelope(persona_id="half_a.catalog_ux_indexer"),
        )
        pmg = params.get("pmg_path")
        out = propose_catalog_from_pmg(
            vault_root,
            project_id=project_id,
            pmg_path=vault_root / str(pmg) if pmg else None,
            dimension=str(params.get("dimension") or "system"),
            mint_batch=str(params.get("mint_batch") or "pmg_phases"),
        )
        result = {"ok": out.ok, "id": eid, "mode": mode, **out.to_dict()}
        if out.ok:
            from .catalog_moc_sync import sync_catalog_moc

            moc = sync_catalog_moc(vault_root, project_id=project_id)
            result["catalog_moc"] = moc
            catalog_rel = f"1-Projects/{project_id}/Roadmap/User-Story/slice-catalog.yaml"
            att = synthetic_persona_attestation(
                "half_a.catalog_ux_indexer",
                [catalog_rel],
            )
            save_half_a_provenance_sidecar(
                vault_root,
                project_id=project_id,
                phase="catalog_mint",
                persona_attestation=att,
                artifacts={"catalog": catalog_rel},
            )
            result["persona_attestation"] = att
        return result

    if mode == "L5_SCOPE_AUTHOR":
        from .l5_author import run_l5_scope_author, run_l5_scope_author_batch

        params.setdefault(
            "persona_handoff",
            build_persona_envelope(persona_id="half_a.catalog_ux_indexer"),
        )
        row_id = params.get("row_id")
        row_ids = params.get("row_ids")
        overwrite = params.get("overwrite_placeholder", True) is not False
        if row_id:
            out = run_l5_scope_author(
                vault_root,
                project_id=project_id,
                row_id=str(row_id),
                overwrite_placeholder=overwrite,
            )
        else:
            if isinstance(row_ids, str):
                row_ids = [x.strip() for x in row_ids.split(",") if x.strip()]
            out = run_l5_scope_author_batch(
                vault_root,
                project_id=project_id,
                row_ids=row_ids if isinstance(row_ids, list) else None,
                overwrite_placeholder=overwrite,
            )
        return {"ok": out.get("ok", False), "id": eid, "mode": mode, **out}

    if mode == "CATALOG_COVERAGE":
        cov = run_catalog_coverage(vault_root, project_id=project_id)
        return {"ok": cov.ok, "id": eid, "mode": mode, **cov.to_dict()}

    if mode == "CATALOG_FREEZE_CHECK":
        gate = run_catalog_freeze_gate(vault_root, project_id=project_id)
        return {"ok": gate.get("ok", False), "id": eid, "mode": mode, **gate}

    if mode == "DEPTH_SLICE":
        from .depth_slicer import run_depth_slicer

        row_id = params.get("row_id")
        row_ids = params.get("row_ids")
        if isinstance(row_ids, str):
            row_ids = [x.strip() for x in row_ids.split(",") if x.strip()]
        out = run_depth_slicer(
            vault_root,
            project_id=project_id,
            row_id=str(row_id) if row_id else None,
            row_ids=row_ids if isinstance(row_ids, list) else None,
            bootstrap_l5=params.get("bootstrap_l5", True) is not False,
        )
        return {"ok": out.get("ok", False), "id": eid, "mode": mode, **out}

    if mode == "SET_ROLLOUT_BUDGET":
        assignments = params.get("row_assignments")
        if isinstance(assignments, str):
            assignments = json.loads(assignments)
        if not isinstance(assignments, list):
            assignments = _default_rollout(vault_root, project_id)
        out = run_rollout_slicer(
            vault_root,
            project_id=project_id,
            rollout_version=params.get("rollout_version"),
            row_assignments=assignments,
            generate_beats=params.get("generate_beats", True) is not False,
        )
        return {"ok": out.ok, "id": eid, "mode": mode, **out.to_dict()}

    if mode == "BEAT_GENERATE":
        out = run_beat_auto_generate(vault_root, project_id=project_id)
        return {"ok": out.get("ok", False), "id": eid, "mode": mode, **out}

    if mode == "USER_STORY_BRIEF":
        out = write_user_story_brief(vault_root, project_id=project_id)
        return {"ok": out.ok, "id": eid, "mode": mode, **out.to_dict()}

    if mode == "ROADMAP_FACTORY_STAGE_FACTORY":
        from ...goal_authority_io import load_goal_authority

        lane = str(params.get("queue_lane") or entry.get("queue_lane") or "godot")
        packet = load_goal_authority(vault_root, lane, require_confirmed=False) or {
            "project_id": project_id,
            "planner_hints": {
                "feed_authority": "vault_roadmap",
                "effective_track": "implementation",
            },
        }
        hints = packet.setdefault("planner_hints", {})
        if isinstance(hints, dict):
            hints["feed_authority"] = "vault_roadmap"
        run_id = str(params.get("run_id") or uuid.uuid4().hex[:12])
        out = stage_factory_dispatch_to_pq(
            vault_root, lane, packet, run_id=run_id, dry_run=bool(params.get("dry_run"))
        )
        return {"ok": out.get("ok", False), "id": eid, "mode": mode, **out}

    if mode == ROADMAP_FACTORY_BOOTSTRAP:
        from .product_factory_pipeline import bootstrap as product_factory_bootstrap

        legacy_mode = str(entry.get("mode") or "").strip().upper().replace(" ", "_").replace("-", "_")
        out = product_factory_bootstrap(vault_root, project_id=project_id, params=params)
        result: dict[str, Any] = {
            "ok": out.get("ok", False),
            "id": eid,
            "mode": ROADMAP_FACTORY_BOOTSTRAP,
            **out,
        }
        if legacy_mode == ROADMAP_FACTORY_RELAUNCH:
            result["deprecated_mode"] = ROADMAP_FACTORY_RELAUNCH
            result["deprecated_replacement"] = ROADMAP_FACTORY_BOOTSTRAP
        return result

    if mode == "PRODUCT_FACTORY_CONTINUE":
        action = str(params.get("action") or "tick").lower().replace("-", "_")
        if action == "eat_factory_lanes":
            from .factory_eat_handoff import handle_factory_eat_handoff

            harness_ctx = bool(params.get("harness_context"))
            return handle_factory_eat_handoff(vault_root, entry, harness_context=harness_ctx)
        from .product_factory_pipeline import tick as product_factory_tick

        out = product_factory_tick(vault_root, project_id=project_id, params=params)
        return {"ok": out.ok, "id": eid, "mode": mode, **out.to_dict()}

    return {"ok": False, "id": eid, "error": "unhandled", "mode": mode}
