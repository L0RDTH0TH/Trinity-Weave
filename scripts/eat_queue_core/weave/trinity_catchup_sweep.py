"""Phase 3 — partition-aware Trinity catch-up sweep (bones / bridges / provisionals)."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Literal

from .config import load_trinity_config
from .governance import append_metric_row, ensure_weave_paths
from .trinity_align import check, run_trinity_align
from .trinity_boundary_audit import run_trinity_boundary_audit
from .trinity_card import get_touch
from .trinity_card_paths import (
    component_proposals_dir,
    is_provisional_card,
    list_provisional_trinity_card_ids,
    load_trinity_card,
    resolve_trinity_card_path,
)
from .trinity_partition import load_maintenance_trinity_ids, load_partition_registry
from .trinity_dual_lock import is_maintenance_core_id
from .trinity_spine_guard import (
    maybe_recommend_provisional_core,
    respects_locked_spine,
)
from .trinity_touch_refresh import run_trinity_touch_refresh

AnatomyGroup = Literal["bones", "bridges", "unclassified"]
PLAYBOOK_REL = Path(".technical/weave/trinity-disconnect-playbook.yaml")


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


def playbook_path(vault_root: Path) -> Path:
    return vault_root / PLAYBOOK_REL


def load_disconnect_playbook(vault_root: Path) -> dict[str, Any]:
    path = playbook_path(vault_root)
    if not path.is_file():
        raise FileNotFoundError(f"disconnect playbook missing: {path}")
    return _load_yaml(path)


def _normalize_path(p: str) -> str:
    return str(p).strip().replace("\\", "/").lstrip("./")


def _primary_paths(card: dict[str, Any]) -> set[str]:
    touch = get_touch(card)
    raw = touch.get("primary_paths")
    if not isinstance(raw, list):
        return set()
    return {_normalize_path(str(x)) for x in raw if str(x).strip()}


@dataclass
class PlaybookAction:
    action: str
    disconnect_kind: str
    applies_to: str
    priority: int
    params: dict[str, Any] = field(default_factory=dict)


def resolve_playbook_actions(
    playbook: dict[str, Any],
    *,
    anatomy: str,
    disconnect_kinds: list[str],
) -> list[PlaybookAction]:
    """Match disconnect kinds to playbook entries (wildcard * supported)."""
    applies = "bridge" if anatomy == "bridge" else "bone"
    entries = playbook.get("entries") or []
    if not isinstance(entries, list):
        entries = []
    kinds = disconnect_kinds or ["stale_touch"]
    matched: list[PlaybookAction] = []
    seen: set[tuple[str, str]] = set()

    def consider(entry: dict[str, Any], kind: str) -> None:
        if str(entry.get("applies_to") or "") != applies:
            return
        dk = str(entry.get("disconnect_kind") or "")
        if dk not in (kind, "*"):
            return
        action = str(entry.get("action") or "").strip()
        if not action:
            return
        key = (action, kind)
        if key in seen:
            return
        seen.add(key)
        params = entry.get("params") if isinstance(entry.get("params"), dict) else {}
        matched.append(
            PlaybookAction(
                action=action,
                disconnect_kind=kind,
                applies_to=applies,
                priority=int(entry.get("priority") or 100),
                params=dict(params),
            )
        )

    for kind in kinds:
        for entry in entries:
            if isinstance(entry, dict):
                consider(entry, kind)

    if not matched:
        defaults = playbook.get("defaults") or {}
        fallback = (
            str(defaults.get("bridge_action") or "queue_TRINITY_SPINE_CATCHUP")
            if applies == "bridge"
            else str(defaults.get("bone_action") or "trinity_touch_refresh")
        )
        matched.append(
            PlaybookAction(
                action=fallback,
                disconnect_kind=kinds[0],
                applies_to=applies,
                priority=200,
                params={},
            )
        )

    matched.sort(key=lambda a: a.priority)
    return matched


def anatomy_for_card(
    vault_root: Path,
    trinity_id: str,
    card: dict[str, Any],
) -> str:
    meta = card.get("meta") if isinstance(card.get("meta"), dict) else {}
    raw = str(meta.get("anatomy") or "").strip().lower()
    if raw in ("component", "bridge", "meta"):
        return "component" if raw == "component" else raw
    try:
        reg = load_partition_registry(vault_root)
        a = reg.anatomy_for(trinity_id)
        if a in ("component", "bridge", "meta", "deferred"):
            return "component" if a == "component" else a
        return str(reg.provisionals_default_anatomy or "component")
    except (FileNotFoundError, OSError, ValueError):
        return "component"


def group_for_anatomy(anatomy: str) -> AnatomyGroup:
    if anatomy == "bridge":
        return "bridges"
    if anatomy == "component":
        return "bones"
    return "unclassified"


def _scope_ids(
    vault_root: Path,
    *,
    include_provisional: bool,
    maintenance_only: bool,
) -> list[tuple[str, str]]:
    """Return (trinity_id, tier) pairs in sweep order."""
    from .trinity_card_paths import list_locked_trinity_card_ids, list_trinity_card_ids

    out: list[tuple[str, str]] = []
    if maintenance_only:
        bundle = load_maintenance_trinity_ids(vault_root)
        for tid in bundle.components:
            out.append((tid, "locked"))
        for tid in bundle.bridges:
            if not any(x[0] == tid for x in out):
                out.append((tid, "locked"))
        if include_provisional:
            for tid in list_provisional_trinity_card_ids(vault_root):
                if not any(x[0] == tid for x in out):
                    out.append((tid, "provisional"))
        return out

    locked_set = set(list_locked_trinity_card_ids(vault_root))
    for tid in list_trinity_card_ids(
        vault_root, pilot_only=False, include_provisional=include_provisional
    ):
        tier = "locked" if tid in locked_set else "provisional"
        out.append((tid, tier))
    return out


def provisional_escalation_candidates(
    vault_root: Path,
    *,
    max_findings: int = 8,
) -> list[dict[str, Any]]:
    """Bounded escalations for provisionals (overlap / boundary — no auto-lock)."""
    vault_root = vault_root.resolve()
    prov_ids = list_provisional_trinity_card_ids(vault_root)
    if not prov_ids:
        return []

    cards: dict[str, dict[str, Any]] = {}
    paths_by_id: dict[str, set[str]] = {}
    for tid in prov_ids:
        try:
            card = load_trinity_card(vault_root, tid, prefer="provisional")
        except (OSError, ValueError, FileNotFoundError):
            continue
        cards[tid] = card
        paths_by_id[tid] = _primary_paths(card)

    escalations: list[dict[str, Any]] = []
    prov_list = sorted(cards.keys())
    for i, a in enumerate(prov_list):
        for b in prov_list[i + 1 :]:
            overlap = paths_by_id[a] & paths_by_id[b]
            if overlap:
                escalations.append(
                    {
                        "kind": "likely_merged_component",
                        "trinity_ids": [a, b],
                        "paths": sorted(overlap)[:6],
                        "detail": "Provisional cards share primary_paths — review before lock",
                    }
                )
            if len(escalations) >= max_findings:
                return escalations[:max_findings]

    try:
        audit = run_trinity_boundary_audit(
            vault_root,
            partition="maintenance",
            trinity_ids=prov_list,
            write_report=False,
        )
        for row in audit.get("cards") or []:
            if len(escalations) >= max_findings:
                break
            tid = str(row.get("trinity_id") or "")
            if tid not in prov_ids:
                continue
            for f in row.get("findings") or []:
                if not isinstance(f, dict):
                    continue
                sev = str(f.get("severity") or "")
                kind = str(f.get("kind") or "")
                if sev in ("error", "warn") and kind in (
                    "anchor_collision",
                    "primary_path_overlap",
                    "bridge_without_endpoints",
                    "bridge_owns_component_path",
                ):
                    escalations.append(
                        {
                            "kind": "anchor_collision_provisional"
                            if "collision" in kind or "overlap" in kind
                            else kind,
                            "trinity_id": tid,
                            "detail": str(f.get("detail") or kind),
                            "severity": sev,
                        }
                    )
                if len(escalations) >= max_findings:
                    break
    except (OSError, ValueError):
        pass

    return escalations[:max_findings]


def curate_stale_non_core(
    vault_root: Path,
    trinity_id: str,
    align: Any,
    *,
    dry_run: bool = False,
) -> dict[str, Any]:
    """Auto touch+align for stale_touch only on non-core cards that respect locked spine."""
    vault_root = vault_root.resolve()
    rec: dict[str, Any] = {"trinity_id": trinity_id, "curated": False}

    if is_maintenance_core_id(vault_root, trinity_id):
        rec["skipped"] = "maintenance_core"
        if not align.ok or align.stale_touch or align.disconnects:
            rec["provisional_core"] = maybe_recommend_provisional_core(
                vault_root, trinity_id, align, dry_run=dry_run
            )
        return rec

    guard = respects_locked_spine(vault_root, trinity_id)
    if not guard.ok:
        rec["skipped"] = "respects_locked_spine"
        rec["violations"] = guard.to_dict().get("violations") or []
        return rec

    kinds = [d.kind for d in align.disconnects]
    if align.stale_touch and "stale_touch" not in kinds:
        kinds.append("stale_touch")
    non_stale = [k for k in kinds if k != "stale_touch"]
    if non_stale:
        rec["skipped"] = "disconnects_present"
        rec["disconnect_kinds"] = non_stale
        return rec
    if not align.stale_touch:
        rec["skipped"] = "not_stale"
        return rec

    if dry_run:
        rec["dry_run"] = True
        rec["would_curate"] = True
        return rec

    touch = run_trinity_touch_refresh(
        vault_root,
        trinity_ids=[trinity_id],
        pilot_only=False,
        dry_run=False,
        apply_behavior_signals=False,
    )
    from .trinity_align import apply_trinity_align_gate

    gate = apply_trinity_align_gate(vault_root, trinity_id, update_meta=True)
    rec["curated"] = bool(touch.get("ok")) and bool(gate.get("ok"))
    rec["touch_refresh"] = {"ok": touch.get("ok")}
    rec["align_gate"] = {"ok": gate.get("ok"), "detail": gate.get("detail")}
    return rec


def _execute_playbook_action(
    vault_root: Path,
    *,
    trinity_id: str,
    action: PlaybookAction,
    disconnect_kinds: list[str],
    dry_run: bool,
) -> dict[str, Any]:
    rec: dict[str, Any] = {
        "trinity_id": trinity_id,
        "action": action.action,
        "disconnect_kind": action.disconnect_kind,
        "dry_run": dry_run,
    }
    if dry_run:
        rec["skipped"] = True
        return rec

    if action.action == "trinity_touch_refresh":
        out = run_trinity_touch_refresh(
            vault_root,
            trinity_ids=[trinity_id],
            pilot_only=False,
            dry_run=False,
            apply_behavior_signals=False,
        )
        rec["touch_refresh"] = {"ok": out.get("ok"), "card": trinity_id}
        return rec

    if action.action == "queue_OPERATOR_SURFACE_REPAIR":
        from ..maintenance_io import append_maintenance_entry

        params = {
            "meta_only": True,
            "trinity_id": trinity_id,
            "disconnect_kinds": disconnect_kinds,
            "source_file": str(PLAYBOOK_REL),
            **action.params,
        }
        fp = f"catchup-osr-{trinity_id}-{'-'.join(sorted(disconnect_kinds))}"
        params["fingerprint"] = fp
        q = append_maintenance_entry(
            vault_root,
            mode="OPERATOR_SURFACE_REPAIR",
            params=params,
            source="trinity_catchup_sweep",
        )
        rec["queued"] = q
        return rec

    if action.action == "queue_TRINITY_SPINE_CATCHUP":
        from ..maintenance_io import append_maintenance_entry

        params = {
            "meta_only": True,
            "trinity_id": "trinity_spine_maintenance",
            "affected_trinity_id": trinity_id,
            "disconnect_kinds": disconnect_kinds,
            "source_file": str(PLAYBOOK_REL),
        }
        params["fingerprint"] = (
            f"spine-catchup-{trinity_id}-{'-'.join(sorted(disconnect_kinds))}"
        )
        q = append_maintenance_entry(
            vault_root,
            mode="TRINITY_SPINE_CATCHUP",
            params=params,
            source="trinity_catchup_sweep",
        )
        rec["queued"] = q
        return rec

    rec["error"] = "unknown_playbook_action"
    return rec


def run_spine_catchup_handler(vault_root: Path, params: dict[str, Any]) -> dict[str, Any]:
    """TRINITY_SPINE_CATCHUP — Phase 9 full weave cycle or legacy touch+align."""
    vault_root = vault_root.resolve()
    affected = str(params.get("affected_trinity_id") or "").strip()
    kinds = params.get("disconnect_kinds") or []
    if isinstance(kinds, str):
        kinds = [kinds]

    handler = str(params.get("handler") or "").strip()
    weave_wrap = (
        handler == "run_trinity_weave_self_wrap"
        or bool(params.get("weave_self_wrap"))
        or "weave_clog" in kinds
        or (params.get("full_cycle") is True and "clog" in kinds)
    )
    if weave_wrap:
        from .trinity_weave_self_wrap import run_trinity_weave_self_wrap

        out = run_trinity_weave_self_wrap(
            vault_root,
            dry_run=bool(params.get("dry_run")),
            operator_mutation_on_core=bool(params.get("operator_mutation_on_core")),
            skip_observe=bool(params.get("skip_observe")),
        )
        return {
            "ok": bool(out.get("ok")),
            "summary": (
                f"weave_self_wrap ok={out.get('ok')} "
                f"violations={(out.get('enforce_in_weave') or {}).get('violation_count')}"
            ),
            "weave_self_wrap": out,
            "disconnect_kinds": kinds,
            "affected_trinity_id": affected or None,
        }

    from .trinity_dual_lock import filter_mutable_trinity_ids

    scope: list[str] = []
    try:
        bundle = load_maintenance_trinity_ids(vault_root)
        scope = list(bundle.all)
    except (FileNotFoundError, OSError, ValueError):
        pass
    if affected and affected not in scope:
        scope.append(affected)

    mutable_scope, skipped_core = filter_mutable_trinity_ids(vault_root, scope)

    touch = run_trinity_touch_refresh(
        vault_root,
        trinity_ids=mutable_scope or None,
        pilot_only=False,
        dry_run=False,
        apply_behavior_signals=False,
    )
    align = run_trinity_align(
        vault_root,
        trinity_ids=scope or None,
        pilot_only=False,
        update_meta=True,
    )
    return {
        "ok": bool(touch.get("ok")) and bool(align.get("ok")),
        "summary": (
            f"spine_catchup touch_ok={touch.get('ok')} align_ok={align.get('ok')} "
            f"scope={len(scope)} mutable={len(mutable_scope)} "
            f"skipped_core={len(skipped_core)} affected={affected or 'all'}"
        ),
        "touch_refresh": touch,
        "align": align,
        "skipped_core_ids": skipped_core,
        "disconnect_kinds": kinds,
    }


def run_trinity_catchup_sweep(
    vault_root: Path,
    *,
    include_provisional: bool = False,
    maintenance_only: bool = True,
    dry_run: bool = False,
    queue_actions: bool = True,
    max_escalations: int | None = None,
    write_report: bool = True,
    curate_non_core: bool | None = None,
) -> dict[str, Any]:
    """Align + playbook remediation sweep grouped by anatomy."""
    vault_root = vault_root.resolve()
    ensure_weave_paths(vault_root)
    cfg = load_trinity_config(vault_root)
    if not cfg.enabled:
        return {"ok": True, "skipped": True, "reason": "trinity_disabled"}

    playbook = load_disconnect_playbook(vault_root)
    prov_cfg = playbook.get("provisional_escalation") or {}
    esc_cap = int(max_escalations if max_escalations is not None else prov_cfg.get("max_per_run") or 8)
    do_curate = (
        cfg.curate_non_core_on_sweep
        if curate_non_core is None
        else bool(curate_non_core)
    )

    scope = _scope_ids(
        vault_root,
        include_provisional=include_provisional,
        maintenance_only=maintenance_only,
    )

    groups: dict[str, list[dict[str, Any]]] = {
        "bones": [],
        "bridges": [],
        "unclassified": [],
    }
    actions_taken: list[dict[str, Any]] = []
    curated: list[dict[str, Any]] = []
    queued: list[dict[str, Any]] = []

    for tid, tier in scope:
        try:
            card = load_trinity_card(vault_root, tid)
        except (OSError, ValueError, FileNotFoundError) as e:
            groups["unclassified"].append(
                {
                    "trinity_id": tid,
                    "tier": tier,
                    "ok": False,
                    "error": str(e),
                }
            )
            continue

        anatomy = anatomy_for_card(vault_root, tid, card)
        bucket = group_for_anatomy(anatomy)
        align = check(vault_root, tid, run_behavior_proofs=cfg.run_behavior_proofs)
        kinds = [d.kind for d in align.disconnects]
        if align.stale_touch and "stale_touch" not in kinds:
            kinds.append("stale_touch")

        pb_actions = resolve_playbook_actions(
            playbook, anatomy=anatomy, disconnect_kinds=kinds
        )
        row: dict[str, Any] = {
            "trinity_id": tid,
            "tier": tier,
            "anatomy": anatomy,
            "ok": align.ok,
            "stale_touch": align.stale_touch,
            "disconnects": [d.to_dict() for d in align.disconnects],
            "playbook_actions": [
                {
                    "action": a.action,
                    "kind": a.disconnect_kind,
                    "priority": a.priority,
                }
                for a in pb_actions
            ],
        }
        groups[bucket].append(row)

        if do_curate:
            crec = curate_stale_non_core(
                vault_root, tid, align, dry_run=dry_run or not queue_actions
            )
            if crec.get("curated") or crec.get("would_curate"):
                curated.append(crec)
                if crec.get("curated"):
                    continue

        if not queue_actions or dry_run:
            continue
        if align.ok and not align.stale_touch:
            continue

        for pact in pb_actions[:2]:
            ex = _execute_playbook_action(
                vault_root,
                trinity_id=tid,
                action=pact,
                disconnect_kinds=kinds,
                dry_run=dry_run,
            )
            actions_taken.append(ex)
            if ex.get("queued"):
                queued.append(ex["queued"])

    escalations: list[dict[str, Any]] = []
    if include_provisional:
        escalations = provisional_escalation_candidates(vault_root, max_findings=esc_cap)
        if queue_actions and not dry_run:
            from ..maintenance_io import append_maintenance_entry

            mode = str(prov_cfg.get("queue_mode") or "MAINTENANCE_NOTE")
            for esc in escalations:
                note = (
                    f"Provisional escalation [{esc.get('kind')}]: "
                    f"{esc.get('detail') or esc.get('trinity_ids')}"
                )[:400]
                append_maintenance_entry(
                    vault_root,
                    mode=mode,
                    params={
                        "meta_only": True,
                        "escalation_kind": esc.get("kind"),
                        "escalation": esc,
                        "notes": note,
                        "fingerprint": f"prov-esc-{esc.get('kind')}-{esc.get('trinity_id') or '-'.join(esc.get('trinity_ids') or [])}",
                    },
                    source="trinity_catchup_sweep",
                )

    summary = {
        "bones": len(groups["bones"]),
        "bridges": len(groups["bridges"]),
        "unclassified": len(groups["unclassified"]),
        "bones_gaps": sum(1 for r in groups["bones"] if not r.get("ok")),
        "bridges_gaps": sum(1 for r in groups["bridges"] if not r.get("ok")),
        "actions": len(actions_taken),
        "curated": len([c for c in curated if c.get("curated")]),
        "queued": len(queued),
        "escalations": len(escalations),
    }
    ok = summary["unclassified"] == 0 or all(
        r.get("ok") for r in groups["unclassified"] if "error" not in r
    )

    report: dict[str, Any] = {
        "ok": ok,
        "timestamp": _now_iso(),
        "include_provisional": include_provisional,
        "maintenance_only": maintenance_only,
        "dry_run": dry_run,
        "queue_actions": queue_actions,
        "groups": groups,
        "summary": summary,
        "actions_taken": actions_taken,
        "curated_non_core": curated,
        "curate_non_core": do_curate,
        "queued_ids": [q.get("id") for q in queued if isinstance(q, dict) and q.get("id")],
        "escalations": escalations,
        "run_command": (
            "PYTHONPATH=scripts python3 -m scripts.eat_queue_core.harness "
            "trinity_catchup_sweep --vault-root . --include-provisional"
        ),
    }

    if write_report and not dry_run:
        out_dir = vault_root / ".technical" / "weave" / "validation"
        out_dir.mkdir(parents=True, exist_ok=True)
        suffix = "provisional" if include_provisional else "maintenance"
        out_path = out_dir / f"trinity-catchup-sweep-{suffix}-{_stamp()}.json"
        out_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        report["report_path"] = str(out_path)
        append_metric_row(
            vault_root,
            {
                "metric_type": "trinity_catchup_sweep",
                "ok": ok,
                "include_provisional": include_provisional,
                **summary,
                "report_path": str(out_path),
            },
        )

    return report


def maybe_catchup_on_pseudo_clock(vault_root: Path) -> dict[str, Any] | None:
    """Optional pseudo_clock_tick hook — bounded catch-up + optional backlog assess."""
    cfg = load_trinity_config(vault_root)
    if not cfg.enabled or not cfg.catchup_on_pseudo_clock:
        return None
    out = run_trinity_catchup_sweep(
        vault_root,
        include_provisional=False,
        maintenance_only=True,
        dry_run=False,
        queue_actions=True,
        max_escalations=cfg.catchup_max_escalations_per_run,
        write_report=False,
    )
    try:
        from .trinity_card_backlog import maybe_backlog_on_pseudo_clock

        bl = maybe_backlog_on_pseudo_clock(vault_root)
        if bl is not None:
            out = dict(out)
            out["backlog_assess"] = {
                "ok": bl.get("ok"),
                "top_n": bl.get("top_n"),
                "ranked": (bl.get("ranked") or [])[: cfg.backlog_top_n],
            }
    except (OSError, ValueError):
        pass
    return out
