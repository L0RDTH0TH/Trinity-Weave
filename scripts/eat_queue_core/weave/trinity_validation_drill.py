"""Phase B — Trinity validation drills (Conceptual / Touch / Rules; component-scoped)."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from unittest.mock import patch

from .config import load_trinity_config
from .governance import append_metric_row, ensure_weave_paths
from .trinity_align import apply_trinity_align_gate, check, run_trinity_align
from .trinity_card import (
    SCHEMA_VERSION,
    get_conceptual,
    get_rules,
    get_touch,
    normalize_card,
)
from .trinity_pack import (
    build_trinity_pack,
    resolve_trinity_id,
    resolve_trinity_id_for_mode,
    trinity_pack_required,
)
from .trinity_partition import load_maintenance_trinity_ids
from .trinity_touch_refresh import (
    components_dir,
    list_trinity_card_ids,
    load_trinity_card,
    run_trinity_touch_refresh,
)

PILOT_IDS = frozenset({"lane_status_board", "lane_activity", "launch_registry_reconcile"})
_WIKI_REF_RE = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]")


def _utc_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _utc_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


@dataclass
class CardsSnapshot:
    files: dict[str, bytes]


@dataclass(frozen=True)
class DrillProfile:
    name: str
    component_ids: tuple[str, ...]
    bridge_ids: tuple[str, ...]

    @property
    def all_ids(self) -> tuple[str, ...]:
        return self.component_ids + self.bridge_ids


def drill_profile_for(vault_root: Path, profile: str = "pilot") -> DrillProfile:
    name = (profile or "pilot").strip().lower()
    if name in ("maintenance_set", "maintenance"):
        bundle = load_maintenance_trinity_ids(vault_root)
        return DrillProfile(
            name="maintenance_set",
            component_ids=bundle.components,
            bridge_ids=bundle.bridges,
        )
    return DrillProfile(
        name="pilot",
        component_ids=tuple(sorted(PILOT_IDS)),
        bridge_ids=(),
    )


def _snapshot_cards(vault_root: Path, profile: DrillProfile) -> CardsSnapshot:
    files: dict[str, bytes] = {}
    base = components_dir(vault_root)
    for tid in profile.all_ids:
        path = base / f"{tid}.yaml"
        if path.is_file():
            files[tid] = path.read_bytes()
    return CardsSnapshot(files=files)


def _restore_cards(vault_root: Path, snap: CardsSnapshot) -> None:
    base = components_dir(vault_root)
    base.mkdir(parents=True, exist_ok=True)
    for tid, content in snap.files.items():
        (base / f"{tid}.yaml").write_bytes(content)


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


def drill_trinity_schema_v2(
    vault_root: Path,
    *,
    dry_run: bool = False,
    profile: DrillProfile | None = None,
) -> dict[str, Any]:
    checks: list[dict[str, Any]] = []
    ctx = profile or drill_profile_for(vault_root, "pilot")
    if dry_run:
        return _result("trinity_schema_v2", passed=True, checks=[{"name": "dry_run", "ok": True}])

    ids = list_trinity_card_ids(vault_root, pilot_only=(ctx.name == "pilot"))
    if ctx.name == "pilot":
        checks.append({"name": "pilot_ids_present", "ok": set(ids) >= PILOT_IDS, "ids": ids})
    else:
        missing = [tid for tid in ctx.all_ids if tid not in ids]
        checks.append(
            {
                "name": "maintenance_ids_present",
                "ok": not missing,
                "missing": missing,
                "count": len(ctx.all_ids),
            }
        )

    for tid in sorted(ctx.all_ids):
        try:
            card = normalize_card(load_trinity_card(vault_root, tid))
        except (OSError, ValueError, FileNotFoundError) as e:
            checks.append({"name": f"card_load_{tid}", "ok": False, "error": str(e)})
            continue
        meta = card.get("meta") if isinstance(card.get("meta"), dict) else {}
        sv = meta.get("schema_version")
        has_v2 = all(k in card for k in ("conceptual", "touch", "rules", "contract"))
        checks.append(
            {
                "name": f"schema_v2_{tid}",
                "ok": has_v2 and str(card.get("id")) == tid,
                "schema_version": sv,
                "has_legs": has_v2,
            }
        )
        conceptual = get_conceptual(card)
        rules = get_rules(card)
        checks.append(
            {
                "name": f"conceptual_rules_nonempty_{tid}",
                "ok": bool(conceptual.get("summary"))
                and bool(conceptual.get("primary_case"))
                and (bool(rules.get("forbidden")) or bool(rules.get("precedence"))),
            }
        )

    passed = all(c.get("ok") for c in checks)
    return _result("trinity_schema_v2", passed=passed, checks=checks)


def drill_trinity_touch_refresh(
    vault_root: Path,
    *,
    dry_run: bool = False,
    profile: DrillProfile | None = None,
) -> dict[str, Any]:
    checks: list[dict[str, Any]] = []
    ctx = profile or drill_profile_for(vault_root, "pilot")
    if dry_run:
        return _result(
            "trinity_touch_refresh",
            passed=True,
            checks=[{"name": "dry_run", "ok": True}],
            detail={"would": f"run trinity_touch_refresh profile={ctx.name}"},
        )

    scope_ids = list(ctx.all_ids) if ctx.name != "pilot" else None
    out = run_trinity_touch_refresh(
        vault_root,
        trinity_ids=scope_ids,
        pilot_only=(ctx.name == "pilot"),
        dry_run=False,
        apply_behavior_signals=False,
    )
    checks.append({"name": "refresh_ok", "ok": bool(out.get("ok")), "refresh": out})
    scope = set(ctx.all_ids)
    for row in out.get("results") or []:
        tid = row.get("trinity_id")
        if tid not in scope:
            continue
        card = load_trinity_card(vault_root, str(tid))
        meta = card.get("meta") if isinstance(card.get("meta"), dict) else {}
        checks.append(
            {
                "name": f"hash_written_{tid}",
                "ok": bool(meta.get("touch_content_hash")) and bool(meta.get("touch_refreshed_at")),
                "hash": meta.get("touch_content_hash"),
            }
        )

    passed = bool(out.get("ok")) and all(c.get("ok") for c in checks)
    return _result("trinity_touch_refresh", passed=passed, checks=checks, detail={"refresh": out})


def drill_trinity_align_green(
    vault_root: Path,
    *,
    dry_run: bool = False,
    profile: DrillProfile | None = None,
) -> dict[str, Any]:
    checks: list[dict[str, Any]] = []
    ctx = profile or drill_profile_for(vault_root, "pilot")
    if dry_run:
        return _result("trinity_align_green", passed=True, checks=[{"name": "dry_run", "ok": True}])

    out = run_trinity_align(
        vault_root,
        trinity_ids=list(ctx.all_ids) if ctx.name != "pilot" else None,
        pilot_only=(ctx.name == "pilot"),
        update_meta=False,
    )
    checks.append({"name": "align_run_ok", "ok": bool(out.get("ok")), "align": out})
    for row in out.get("results") or []:
        tid = row.get("trinity_id")
        checks.append(
            {
                "name": f"align_card_{tid}",
                "ok": bool(row.get("ok")),
                "legs": row.get("legs"),
                "disconnects": row.get("disconnects"),
            }
        )

    passed = bool(out.get("ok")) and all(c.get("ok") for c in checks)
    return _result("trinity_align_green", passed=passed, checks=checks, detail={"align": out})


def drill_trinity_pack_envelope(
    vault_root: Path,
    *,
    dry_run: bool = False,
    profile: DrillProfile | None = None,
) -> dict[str, Any]:
    checks: list[dict[str, Any]] = []
    ctx = profile or drill_profile_for(vault_root, "pilot")
    if dry_run:
        return _result("trinity_pack_envelope", passed=True, checks=[{"name": "dry_run", "ok": True}])

    cfg = load_trinity_config(vault_root)
    bridge_set = set(ctx.bridge_ids)
    for tid in sorted(ctx.all_ids):
        pack = build_trinity_pack(vault_root, tid)
        must_read = pack.get("touch", {}).get("must_read") or []
        is_bridge = tid in bridge_set
        checks.append({"name": f"pack_{tid}", "ok": pack.get("trinity_id") == tid})
        checks.append(
            {
                "name": f"pack_anatomy_{tid}",
                "ok": pack.get("anatomy") == ("bridge" if is_bridge else "component"),
                "anatomy": pack.get("anatomy"),
            }
        )
        checks.append(
            {
                "name": f"pack_legs_{tid}",
                "ok": all(k in pack for k in ("conceptual", "rules", "touch"))
                and pack.get("component_scope") is (not is_bridge),
            }
        )
        rules_block = pack.get("rules") or {}
        checks.append(
            {
                "name": f"pack_rules_forbidden_{tid}",
                "ok": bool(rules_block.get("forbidden")) or bool(rules_block.get("precedence")),
            }
        )
        checks.append(
            {
                "name": f"closure_cap_{tid}",
                "ok": len(must_read) <= cfg.max_closure_paths,
                "must_read_count": len(must_read),
                "cap": cfg.max_closure_paths,
            }
        )

    maint_tid = resolve_trinity_id(vault_root, lane="maintenance")
    checks.append(
        {
            "name": "maintenance_default_trinity",
            "ok": maint_tid == "lane_status_board",
            "resolved": maint_tid,
        }
    )
    checks.append(
        {
            "name": "pack_required_on_maintenance",
            "ok": trinity_pack_required(vault_root, lane="maintenance", queue_mode="REFRESH_LANE_BOARD"),
        }
    )
    gov_tid = resolve_trinity_id_for_mode(vault_root, "GOVERNANCE_REVIEW")
    checks.append(
        {
            "name": "mode_governance_review",
            "ok": gov_tid in ("invariant_registry", "weave_governance"),
            "resolved": gov_tid,
        }
    )
    checks.append(
        {
            "name": "mode_spine_catchup",
            "ok": resolve_trinity_id_for_mode(vault_root, "TRINITY_SPINE_CATCHUP")
            == "trinity_spine_maintenance",
        }
    )
    checks.append(
        {
            "name": "mode_ghost_audit",
            "ok": resolve_trinity_id_for_mode(vault_root, "GHOST_SKILL_AUDIT") == "ghost_skill_audit",
        }
    )

    passed = all(c.get("ok") for c in checks)
    return _result("trinity_pack_envelope", passed=passed, checks=checks, detail={"profile": ctx.name})


def _resolve_wiki_ref(vault_root: Path, ref: str) -> bool:
    raw = ref.strip()
    m = _WIKI_REF_RE.fullmatch(raw)
    path = m.group(1).strip() if m else raw
    if not path:
        return False
    if not path.endswith((".md", ".yaml", ".yml")):
        path = f"{path}.md"
    return (vault_root / path).is_file()


def drill_trinity_conceptual_refs(
    vault_root: Path,
    *,
    dry_run: bool = False,
    profile: DrillProfile | None = None,
) -> dict[str, Any]:
    checks: list[dict[str, Any]] = []
    ctx = profile or drill_profile_for(vault_root, "pilot")
    if dry_run:
        return _result("trinity_conceptual_refs", passed=True, checks=[{"name": "dry_run", "ok": True}])

    missing: list[str] = []
    deferred_refs = ("l5_sandbox",)
    for tid in sorted(ctx.component_ids):
        card = normalize_card(load_trinity_card(vault_root, tid))
        refs = get_conceptual(card).get("refs") or []
        for ref in refs:
            ref_s = str(ref)
            if any(d in ref_s for d in deferred_refs):
                continue
            if not _resolve_wiki_ref(vault_root, ref_s):
                missing.append(f"{tid}:{ref}")
        checks.append(
            {
                "name": f"refs_resolve_{tid}",
                "ok": not any(m.startswith(f"{tid}:") for m in missing),
                "refs_count": len(refs) if isinstance(refs, list) else 0,
            }
        )

    passed = not missing and all(c.get("ok") for c in checks)
    return _result(
        "trinity_conceptual_refs",
        passed=passed,
        checks=checks,
        detail={"missing_refs": missing},
    )


def drill_trinity_enforcement_fault(
    vault_root: Path,
    *,
    dry_run: bool = False,
    profile: DrillProfile | None = None,
) -> dict[str, Any]:
    """Inject stale touch hash; confirm align fails closed (restore in run_* finally)."""
    checks: list[dict[str, Any]] = []
    target = "lane_status_board"
    if dry_run:
        return _result(
            "trinity_enforcement_fault",
            passed=True,
            checks=[{"name": "dry_run", "ok": True}],
            detail={"would": f"corrupt meta.touch_content_hash on {target}"},
        )

    cfg_live = load_trinity_config(vault_root)
    if not cfg_live.checks_enabled:
        return _result(
            "trinity_enforcement_fault",
            passed=True,
            checks=[
                {
                    "name": "checks_disabled_phase2_advisory",
                    "ok": True,
                    "note": "trinity_checks_enabled false until Phase 4; stale gate not exercised",
                }
            ],
            detail={"profile": (profile or drill_profile_for(vault_root, "pilot")).name},
        )

    card = load_trinity_card(vault_root, target)
    meta = card.setdefault("meta", {})
    if not isinstance(meta, dict):
        meta = {}
        card["meta"] = meta
    original_hash = meta.get("touch_content_hash")
    meta["touch_content_hash"] = "trinity-drill-stale-deadbeee"
    path = components_dir(vault_root) / f"{target}.yaml"
    import yaml  # type: ignore[import-untyped]

    path.write_text(yaml.safe_dump(card, sort_keys=False), encoding="utf-8")

    align = check(vault_root, target)
    checks.append({"name": "stale_detected", "ok": align.stale_touch and not align.ok})
    checks.append({"name": "legs_report_stale", "ok": align.legs.get("touch_fresh") is False})

    with patch("eat_queue_core.weave.trinity_align.load_trinity_config") as mock_cfg:
        real = load_trinity_config(vault_root)
        mock_cfg.return_value = type(real)(
            enabled=True,
            checks_enabled=True,
            block_on_stale_touch=real.block_on_stale_touch,
            block_on_disconnect=real.block_on_disconnect,
            touch_refresh_on_pseudo_clock=real.touch_refresh_on_pseudo_clock,
            pack_mandatory_on_maintenance_lane=real.pack_mandatory_on_maintenance_lane,
            max_closure_paths=real.max_closure_paths,
            max_closure_hops=real.max_closure_hops,
        )
        gate = apply_trinity_align_gate(vault_root, target, update_meta=False)

    checks.append({"name": "gate_blocks_stale", "ok": gate.get("blocked") is True and gate.get("ok") is False})
    checks.append({"name": "gate_not_skipped", "ok": gate.get("skipped") is not True})

    if original_hash:
        meta["touch_content_hash"] = original_hash
        path.write_text(yaml.safe_dump(card, sort_keys=False), encoding="utf-8")

    passed = all(c.get("ok") for c in checks)
    return _result(
        "trinity_enforcement_fault",
        passed=passed,
        checks=checks,
        detail={"target": target, "gate": gate, "align": align.to_dict()},
    )


def drill_trinity_component_scope(
    vault_root: Path,
    *,
    dry_run: bool = False,
    profile: DrillProfile | None = None,
) -> dict[str, Any]:
    checks: list[dict[str, Any]] = []
    ctx = profile or drill_profile_for(vault_root, "pilot")
    if dry_run:
        return _result("trinity_component_scope", passed=True, checks=[{"name": "dry_run", "ok": True}])

    lane_like = {"institute", "godot", "sandbox", "maintenance", "default", "shared", "core"}
    ids = list(ctx.component_ids)
    checks.append(
        {
            "name": "ids_are_components_not_lanes",
            "ok": not (set(ids) & lane_like),
            "ids": ids,
        }
    )
    checks.append(
        {
            "name": "cards_under_components_dir",
            "ok": components_dir(vault_root).is_dir(),
            "path": str(components_dir(vault_root)),
        }
    )
    for tid in ids:
        card = load_trinity_card(vault_root, tid)
        touch = get_touch(card)
        checks.append(
            {
                "name": f"primary_paths_code_{tid}",
                "ok": all(
                    str(p).startswith(
                        ("scripts/", "Ingest/", ".technical/weave/", ".cursor/skills/")
                    )
                    for p in (touch.get("primary_paths") or [])
                ),
            }
        )

    passed = all(c.get("ok") for c in checks)
    return _result("trinity_component_scope", passed=passed, checks=checks)


DRILL_FUNCS = {
    "schema_v2": drill_trinity_schema_v2,
    "touch_refresh": drill_trinity_touch_refresh,
    "align_green": drill_trinity_align_green,
    "pack_envelope": drill_trinity_pack_envelope,
    "conceptual_refs": drill_trinity_conceptual_refs,
    "enforcement_fault": drill_trinity_enforcement_fault,
    "component_scope": drill_trinity_component_scope,
}


def run_trinity_validation_drill(
    vault_root: Path,
    *,
    drill: str = "all",
    profile: str = "pilot",
    dry_run: bool = False,
    write_report: bool = True,
    skip_touch_refresh: bool = False,
) -> dict[str, Any]:
    """Phase B — full Trinity validation sequence (component-scoped)."""
    vault_root = vault_root.resolve()
    ensure_weave_paths(vault_root)
    ctx = drill_profile_for(vault_root, profile)
    names = list(DRILL_FUNCS.keys()) if drill.strip().lower() == "all" else [drill.strip().lower()]
    if skip_touch_refresh and "touch_refresh" in names:
        names = [n for n in names if n != "touch_refresh"]

    unknown = [n for n in names if n not in DRILL_FUNCS]
    if unknown:
        return {"ok": False, "error": "unknown_drill", "unknown": unknown, "valid": list(DRILL_FUNCS.keys())}

    snap = _snapshot_cards(vault_root, ctx)
    results: list[dict[str, Any]] = []
    try:
        for name in names:
            results.append(DRILL_FUNCS[name](vault_root, dry_run=dry_run, profile=ctx))
    finally:
        if not dry_run:
            _restore_cards(vault_root, snap)

    all_passed = all(r.get("passed") for r in results)
    report = {
        "ok": all_passed,
        "phase": "B",
        "layer": "Trinity",
        "profile": ctx.name,
        "component_count": len(ctx.component_ids),
        "bridge_count": len(ctx.bridge_ids),
        "schema_version": SCHEMA_VERSION,
        "dry_run": dry_run,
        "skip_touch_refresh": skip_touch_refresh,
        "drills": results,
        "summary": {
            "total": len(results),
            "passed": sum(1 for r in results if r.get("passed")),
            "failed": sum(1 for r in results if not r.get("passed")),
        },
        "run_command": (
            "PYTHONPATH=scripts python3 -m scripts.eat_queue_core.harness "
            f"trinity_validation_drill --vault-root . --profile {ctx.name}"
        ),
        "timestamp": _utc_iso(),
    }
    if write_report and not dry_run:
        out_dir = vault_root / ".technical" / "weave" / "validation"
        out_dir.mkdir(parents=True, exist_ok=True)
        suffix = ctx.name if ctx.name != "pilot" else "pilot"
        out_path = out_dir / f"trinity-drill-{suffix}-{_utc_stamp()}.json"
        out_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        report["report_path"] = str(out_path)
        append_metric_row(
            vault_root,
            {
                "metric_type": "trinity_validation_drill",
                "ok": all_passed,
                "profile": ctx.name,
                "passed": report["summary"]["passed"],
                "failed": report["summary"]["failed"],
                "report_path": str(out_path),
            },
        )
    return report
