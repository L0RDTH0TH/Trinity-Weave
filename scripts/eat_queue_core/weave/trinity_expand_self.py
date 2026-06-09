"""Phase 14 — expand_self delta wrap (scoped onboarding for new factories/segments)."""

from __future__ import annotations

import fnmatch
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .config import load_trinity_config
from .trinity_card_paths import list_provisional_trinity_card_ids, load_trinity_card
from .trinity_dual_lock import is_maintenance_core_id, is_usage_proven_id

ARTIFACT_DIR = Path(".technical/weave/validation")


def _now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def parse_scope_ids(raw: str | list[str] | tuple[str, ...] | None) -> tuple[str, ...]:
    if raw is None:
        return ()
    if isinstance(raw, str):
        parts = [p.strip() for p in raw.split(",") if p.strip()]
        return tuple(dict.fromkeys(parts))
    out: list[str] = []
    for item in raw:
        s = str(item or "").strip()
        if s and s not in out:
            out.append(s)
    return tuple(out)


def _filter_cluster_ids(ids: list[str], cluster: str | None) -> list[str]:
    if not cluster:
        return ids
    pat = cluster.strip()
    if pat.endswith("*"):
        return [tid for tid in ids if fnmatch.fnmatch(tid, pat)]
    if "*" in pat or "?" in pat:
        return [tid for tid in ids if fnmatch.fnmatch(tid, pat)]
    return [tid for tid in ids if tid == pat or tid.startswith(f"{pat}_")]


def resolve_expand_self_scope(
    vault_root: Path,
    *,
    scope_ids: tuple[str, ...] | None = None,
    corps_cluster: str | None = None,
) -> dict[str, Any]:
    """Resolve delta ids from explicit scope and/or cluster glob."""
    vault_root = vault_root.resolve()
    provisional = list_provisional_trinity_card_ids(vault_root)

    if scope_ids:
        wanted = set(scope_ids)
        missing = sorted(wanted - set(provisional))
        resolved = [tid for tid in provisional if tid in wanted]
    else:
        missing = []
        resolved = list(provisional)

    if corps_cluster:
        resolved = _filter_cluster_ids(resolved, corps_cluster)

    resolved = sorted(dict.fromkeys(resolved))
    return {
        "scope_ids_requested": list(scope_ids or ()),
        "corps_cluster": corps_cluster,
        "resolved_ids": resolved,
        "missing_ids": missing,
        "provisional_pool_size": len(provisional),
    }


def validate_expand_self_scope(
    vault_root: Path,
    resolved_ids: list[str],
    *,
    operator_override_scope: bool = False,
) -> dict[str, Any]:
    """Hard stops: maintenance_core / usage_proven without operator override."""
    blocked: list[dict[str, str]] = []
    for tid in resolved_ids:
        if is_maintenance_core_id(vault_root, tid) and not operator_override_scope:
            blocked.append(
                {
                    "trinity_id": tid,
                    "reason": "maintenance_core",
                    "hint": "Use --operator-override-scope with --operator-mutation for core ids",
                }
            )
        elif is_usage_proven_id(vault_root, tid) and not operator_override_scope:
            blocked.append(
                {
                    "trinity_id": tid,
                    "reason": "usage_proven",
                    "hint": "Operator unfreeze required before expand_self on usage_proven ids",
                }
            )
    return {
        "ok": len(blocked) == 0,
        "blocked": blocked,
        "operator_override_scope": operator_override_scope,
        "resolved_count": len(resolved_ids),
    }


def run_expand_self_delta_wrap(
    vault_root: Path,
    *,
    scope_ids: tuple[str, ...] | None = None,
    corps_cluster: str | None = None,
    operator_override_scope: bool = False,
    operator_mutation_on_core: bool = False,
    dry_run: bool = False,
    skip_align: bool = False,
    skip_corps: bool = False,
    skip_enforce: bool = False,
    skip_unclog: bool = False,
    skip_observe: bool = False,
    write_report: bool = True,
) -> dict[str, Any]:
    """Phase 14 — scoped self-wrap for new factory/segment delta only."""
    vault_root = vault_root.resolve()
    cfg = load_trinity_config(vault_root)

    if not getattr(cfg, "expand_self_enabled", True):
        return {"ok": True, "skipped": True, "reason": "expand_self_disabled"}

    resolution = resolve_expand_self_scope(
        vault_root,
        scope_ids=scope_ids,
        corps_cluster=corps_cluster,
    )
    resolved = list(resolution.get("resolved_ids") or [])
    if not resolved:
        return {
            "ok": False,
            "phase": "14-expand_self",
            "error": "empty_scope",
            "resolution": resolution,
            "hint": "Provide --scope-ids or --corps-cluster matching provisional cards",
        }

    validation = validate_expand_self_scope(
        vault_root,
        resolved,
        operator_override_scope=operator_override_scope,
    )
    if not validation.get("ok"):
        return {
            "ok": False,
            "phase": "14-expand_self",
            "error": "scope_blocked",
            "resolution": resolution,
            "validation": validation,
        }

    from .trinity_weave_self_wrap import run_trinity_weave_self_wrap

    report = run_trinity_weave_self_wrap(
        vault_root,
        dry_run=dry_run,
        skip_align=skip_align,
        skip_enforce=skip_enforce,
        skip_unclog=skip_unclog,
        skip_corps=skip_corps,
        skip_observe=skip_observe,
        operator_mutation_on_core=operator_mutation_on_core or operator_override_scope,
        write_graph=False,
        write_report=write_report,
        expand_self=True,
        expand_self_scope_ids=tuple(resolved),
        corps_cluster=corps_cluster,
    )
    report["phase"] = "14-expand_self"
    report["expand_self_resolution"] = resolution
    report["expand_self_validation"] = validation

    if write_report and not dry_run:
        val_dir = vault_root / ARTIFACT_DIR
        val_dir.mkdir(parents=True, exist_ok=True)
        artifact = val_dir / f"expand-self-{_stamp()}.json"
        artifact.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        report["expand_self_artifact"] = str(artifact.relative_to(vault_root))

    return report
