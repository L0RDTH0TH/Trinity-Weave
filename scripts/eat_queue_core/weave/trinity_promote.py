"""Promote reviewed proposal stubs → provisional component-proposals (ghost gate pattern)."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

from .trinity_card import SCHEMA_VERSION, normalize_card
from .trinity_card_generate import LOCKED_SKIP_IDS
from .trinity_card_paths import SCHEMA_CARD, is_locked_card
from .trinity_card_paths import (
    META_CARD_ID,
    component_proposals_dir,
    components_dir,
    ensure_trinity_storage_dirs,
    is_provisional_card,
    list_locked_trinity_card_ids,
)

DEFAULT_PROMOTION_STAMP = "I-did-it-right"


@dataclass
class PromoteRecord:
    trinity_id: str
    source_path: str
    output_path: str
    action: str  # promoted | skipped_locked | skipped_exists | skipped_invalid
    detail: str = ""


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"not a mapping: {path}")
    return data


def _dump_yaml(card: dict[str, Any]) -> str:
    return yaml.dump(card, sort_keys=False, allow_unicode=True, default_flow_style=False)


def proposal_stubs_dir(vault_root: Path, stamp: str) -> Path:
    return vault_root / ".technical" / "weave" / "proposals" / stamp.strip().strip("/") / "stubs"


def prepare_provisional_card(
    card: dict[str, Any],
    *,
    stamp: str,
    source_rel: str,
) -> dict[str, Any]:
    """Strip lock stamps; mark provisional tier (production-usable, not doctrine-locked)."""
    out = normalize_card(dict(card))
    tid = str(out.get("id") or "").strip()
    if tid:
        out["id"] = tid
    meta = dict(out.get("meta") or {})
    meta["schema_version"] = SCHEMA_VERSION
    meta["provisional"] = True
    meta["promotion_tier"] = "provisional"
    meta["card_class"] = "promoted_provisional"
    meta.pop("conceptual_confirmed_at", None)
    meta.pop("rules_confirmed_at", None)
    src = dict(meta.get("source") or {})
    src["promoted_from"] = stamp
    src["promoted_at"] = _now_iso()
    src["promotion_method"] = "trinity_promote_proposals"
    src["source_stub"] = source_rel
    meta["source"] = src
    out["meta"] = meta
    return out


def run_trinity_promote_proposals(
    vault_root: Path,
    *,
    stamp: str = DEFAULT_PROMOTION_STAMP,
    dry_run: bool = False,
    force: bool = False,
    trinity_id: str | None = None,
) -> dict[str, Any]:
    """
    Copy reviewed stubs into `.technical/weave/component-proposals/`.

    Locked manual cards stay in `components/` only. Operator lock gate:
    `trinity_lock_card` (future harness) moves provisional → components + stamps.
    """
    vault_root = vault_root.resolve()
    ensure_trinity_storage_dirs(vault_root)
    src_dir = proposal_stubs_dir(vault_root, stamp)
    if not src_dir.is_dir():
        return {
            "ok": False,
            "error": "proposal_stamp_not_found",
            "path": str(src_dir),
        }

    dest_dir = component_proposals_dir(vault_root)
    locked_ids = set(list_locked_trinity_card_ids(vault_root))
    records: list[PromoteRecord] = []

    paths = sorted(src_dir.glob("*.yaml"))
    if trinity_id:
        paths = [p for p in paths if p.stem == trinity_id]

    for path in paths:
        if path.name.startswith("_"):
            continue
        rel_src = path.relative_to(vault_root).as_posix()
        try:
            card = _load_yaml(path)
        except (OSError, ValueError, yaml.YAMLError) as e:
            records.append(
                PromoteRecord(
                    path.stem,
                    rel_src,
                    "",
                    "skipped_invalid",
                    str(e),
                )
            )
            continue
        tid = str(card.get("id") or path.stem).strip()
        if not tid or tid in (SCHEMA_CARD, META_CARD_ID):
            records.append(PromoteRecord(tid or path.stem, rel_src, "", "skipped_invalid", "reserved id"))
            continue

        try:
            from .trinity_dual_lock import is_maintenance_core_id

            if is_maintenance_core_id(vault_root, tid):
                records.append(
                    PromoteRecord(
                        tid,
                        rel_src,
                        "",
                        "skipped_maintenance_core",
                        "maintenance core ids are not promoted via proposals",
                    )
                )
                continue
        except (OSError, ValueError):
            pass

        locked_path = components_dir(vault_root) / f"{tid}.yaml"
        if tid in LOCKED_SKIP_IDS or tid in locked_ids:
            if locked_path.is_file():
                try:
                    if _is_locked(_load_yaml(locked_path)):
                        records.append(
                            PromoteRecord(
                                tid,
                                rel_src,
                                locked_path.relative_to(vault_root).as_posix(),
                                "skipped_locked",
                                "manual locked card in components/",
                            )
                        )
                        continue
                except (OSError, ValueError, yaml.YAMLError):
                    pass

        dest = dest_dir / f"{tid}.yaml"
        rel_dest = dest.relative_to(vault_root).as_posix()
        if dest.is_file() and not force:
            records.append(
                PromoteRecord(tid, rel_src, rel_dest, "skipped_exists", "provisional already present")
            )
            continue

        prepared = prepare_provisional_card(card, stamp=stamp, source_rel=rel_src)
        if not dry_run:
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(_dump_yaml(prepared), encoding="utf-8")
        records.append(PromoteRecord(tid, rel_src, rel_dest, "promoted", ""))

    promoted = [r for r in records if r.action == "promoted"]
    manifest = {
        "ok": True,
        "stamp": stamp,
        "dry_run": dry_run,
        "force": force,
        "generated_at": _now_iso(),
        "source_dir": src_dir.relative_to(vault_root).as_posix(),
        "dest_dir": dest_dir.relative_to(vault_root).as_posix(),
        "promoted_count": len(promoted),
        "skipped_locked": sum(1 for r in records if r.action == "skipped_locked"),
        "skipped_exists": sum(1 for r in records if r.action == "skipped_exists"),
        "skipped_invalid": sum(1 for r in records if r.action == "skipped_invalid"),
        "records": [asdict(r) for r in records],
    }

    if not dry_run:
        manifest_path = dest_dir / "promotion-manifest.json"
        manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
        index_lines = [
            "# Component proposals (provisional)",
            "",
            "Promoted from reviewed stubs — **not** operator-locked. Use in production;",
            "run `trinity_lock_card` when Conceptual + Rules are ready for `components/`.",
            "",
            f"**Stamp:** `{stamp}` · **Promoted:** {len(promoted)}",
            "",
            "| trinity_id | source |",
            "|------------|--------|",
        ]
        for r in promoted[:200]:
            index_lines.append(f"| `{r.trinity_id}` | `{r.source_path}` |")
        if len(promoted) > 200:
            index_lines.append(f"| … | +{len(promoted) - 200} more |")
        (dest_dir / "README.md").write_text("\n".join(index_lines) + "\n", encoding="utf-8")

    return manifest


def run_trinity_lock_card(
    vault_root: Path,
    trinity_id: str,
    *,
    dry_run: bool = False,
    lock_kind: str = "full",
) -> dict[str, Any]:
    """Operator gate — move provisional card to locked `components/` with lock stamps."""
    vault_root = vault_root.resolve()
    ensure_trinity_storage_dirs(vault_root)
    prov_path = component_proposals_dir(vault_root) / f"{trinity_id}.yaml"
    if not prov_path.is_file():
        return {"ok": False, "error": "provisional_not_found", "trinity_id": trinity_id}

    card = _load_yaml(prov_path)
    if not is_provisional_card(card):
        return {
            "ok": False,
            "error": "not_provisional",
            "trinity_id": trinity_id,
            "hint": "card missing meta.provisional / promotion_tier",
        }

    locked_path = components_dir(vault_root) / f"{trinity_id}.yaml"
    if locked_path.is_file():
        try:
            existing = _load_yaml(locked_path)
            if is_locked_card(existing):
                return {
                    "ok": False,
                    "error": "already_locked",
                    "trinity_id": trinity_id,
                    "path": locked_path.relative_to(vault_root).as_posix(),
                }
        except (OSError, ValueError, yaml.YAMLError):
            pass

    from .trinity_dual_lock import (
        apply_lock_kind_to_card,
        is_maintenance_core_id,
    )

    kind = str(lock_kind or "full").strip().lower()
    if kind in ("full", "operator", "default"):
        kind = "full"
    elif kind in ("core", "maintenance_core"):
        kind = "maintenance_core"
    elif kind in ("conceptual", "conceptual_spine", "spine"):
        kind = "conceptual_spine"
    else:
        return {
            "ok": False,
            "error": "invalid_lock_kind",
            "trinity_id": trinity_id,
            "hint": "use full | conceptual_spine | maintenance_core",
        }

    if kind == "maintenance_core" and not is_maintenance_core_id(vault_root, trinity_id):
        return {
            "ok": False,
            "error": "not_maintenance_core_id",
            "trinity_id": trinity_id,
            "hint": "maintenance_core lock_kind only for registry maintenance core ids",
        }

    now = _now_iso()
    card = apply_lock_kind_to_card(card, kind, now_iso=now)  # type: ignore[arg-type]

    if dry_run:
        return {
            "ok": True,
            "dry_run": True,
            "trinity_id": trinity_id,
            "would_write": locked_path.relative_to(vault_root).as_posix(),
            "would_remove": prov_path.relative_to(vault_root).as_posix(),
        }

    from .trinity_dual_lock import operator_mutation_ctx

    token = operator_mutation_ctx.set(True)
    try:
        locked_path.parent.mkdir(parents=True, exist_ok=True)
        locked_path.write_text(_dump_yaml(normalize_card(card)), encoding="utf-8")
    finally:
        operator_mutation_ctx.reset(token)
    prov_path.unlink()
    return {
        "ok": True,
        "trinity_id": trinity_id,
        "lock_kind": kind,
        "locked_path": locked_path.relative_to(vault_root).as_posix(),
        "removed_provisional": prov_path.relative_to(vault_root).as_posix(),
    }
