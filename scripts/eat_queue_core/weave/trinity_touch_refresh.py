"""Trinity touch refresh — structural closure hash + proposed behavior_signals (Wave 2.5b)."""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .config import TrinityConfig, load_trinity_config, load_weave_config
from .governance import append_metric_row, ensure_weave_paths


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


from .trinity_card_paths import (  # noqa: E402 — re-export for callers
    component_proposals_dir,
    components_dir,
    ensure_trinity_storage_dirs,
    list_locked_trinity_card_ids,
    list_provisional_trinity_card_ids,
    list_trinity_card_ids,
    load_trinity_card,
    resolve_trinity_card_path,
    write_trinity_card,
)


def concept_map_path(vault_root: Path) -> Path:
    return vault_root / ".technical" / "weave" / "concept-trinity-map.yaml"


def _load_yaml(path: Path) -> dict[str, Any]:
    import yaml  # type: ignore[import-untyped]

    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"expected YAML object: {path}")
    return data


def _dump_yaml(data: dict[str, Any]) -> str:
    import yaml  # type: ignore[import-untyped]

    return yaml.safe_dump(data, sort_keys=False, allow_unicode=True)


def _touch_path_strings(card: dict[str, Any], vault_root: Path) -> list[str]:
    touch = card.get("touch") if isinstance(card.get("touch"), dict) else {}
    out: list[str] = []
    for key in ("primary_paths", "inbound", "outbound"):
        raw = touch.get(key)
        if isinstance(raw, list):
            for item in raw:
                s = str(item).strip()
                if s:
                    out.append(s)
    br = touch.get("blast_radius")
    if br:
        br_path = vault_root / str(br).strip()
        if br_path.is_file():
            try:
                br_data = _load_yaml(br_path)
                for c in br_data.get("consumers") or []:
                    if isinstance(c, str) and c.strip():
                        out.append(c.strip())
                for c in br_data.get("pre_read") or []:
                    if isinstance(c, str) and c.strip():
                        out.append(c.strip().replace(".", "/") + ".py")
            except (OSError, ValueError):
                pass
        out.append(str(br).strip())
    seen: set[str] = set()
    deduped: list[str] = []
    for s in out:
        if s not in seen:
            seen.add(s)
            deduped.append(s)
    return deduped


def _expand_path_pattern(vault_root: Path, pattern: str) -> list[Path]:
    pattern = pattern.strip()
    if not pattern:
        return []
    if "*" in pattern:
        return sorted(vault_root.glob(pattern))
    p = vault_root / pattern
    if p.is_file():
        return [p]
    if p.is_dir():
        return sorted(p.rglob("*.py"))[:50]
    return [p]


def _py_import_neighbors(py_path: Path, vault_root: Path) -> list[Path]:
    if not py_path.is_file() or py_path.suffix != ".py":
        return []
    try:
        text = py_path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return []
    found: list[Path] = []
    eat_root = vault_root / "scripts" / "eat_queue_core"
    for m in re.finditer(r"from\s+\.([\w]+)\s+import", text):
        mod = eat_root / f"{m.group(1)}.py"
        if mod.is_file():
            found.append(mod)
    for m in re.finditer(r"from\s+eat_queue_core\.([\w]+)\s+import", text):
        mod = eat_root / f"{m.group(1)}.py"
        if mod.is_file():
            found.append(mod)
    return found


def build_closure_manifest(
    vault_root: Path,
    card: dict[str, Any],
    *,
    max_hops: int = 3,
    max_paths: int = 21,
) -> dict[str, Any]:
    vault_root = vault_root.resolve()
    seeds = _touch_path_strings(card, vault_root)
    frontier: list[Path] = []
    for s in seeds:
        frontier.extend(_expand_path_pattern(vault_root, s))

    collected: list[Path] = []
    seen: set[str] = set()
    hop = 0
    while frontier and hop <= max_hops and len(collected) < max_paths:
        next_frontier: list[Path] = []
        for p in frontier:
            key = str(p.resolve()) if p.exists() else str(p)
            if key in seen:
                continue
            seen.add(key)
            collected.append(p)
            if len(collected) >= max_paths:
                break
            if p.is_file() and p.suffix == ".py" and hop < max_hops:
                next_frontier.extend(_py_import_neighbors(p, vault_root))
        frontier = next_frontier
        hop += 1

    entries: list[dict[str, Any]] = []
    for p in collected[:max_paths]:
        rel = p.relative_to(vault_root).as_posix() if p.is_relative_to(vault_root) else p.as_posix()
        if p.is_file():
            st = p.stat()
            entries.append(
                {
                    "path": rel,
                    "exists": True,
                    "mtime_ns": st.st_mtime_ns,
                    "size": st.st_size,
                }
            )
        else:
            entries.append({"path": rel, "exists": False})

    entries.sort(key=lambda e: e["path"])
    digest = hashlib.sha256(
        json.dumps(entries, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    return {
        "must_read": [e["path"] for e in entries],
        "hop_limit": max_hops,
        "path_cap": max_paths,
        "entries": entries,
        "touch_content_hash": digest,
    }


_IMPORT_TEST_RE = re.compile(r"^\s*def\s+(test_[\w]+)\s*\(", re.MULTILINE)


def propose_behavior_signals(vault_root: Path, card: dict[str, Any]) -> list[str]:
    from .trinity_card import contract_proof_paths

    proposed: list[str] = []
    seen: set[str] = set()

    def add(sig: str) -> None:
        s = sig.strip()
        if s and s not in seen:
            seen.add(s)
            proposed.append(s)

    for raw in contract_proof_paths(card):
        p = vault_root / str(raw).strip()
        if p.is_file() and "test" in p.name:
            try:
                text = p.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            for m in _IMPORT_TEST_RE.finditer(text):
                add(m.group(1))
        elif p.is_dir():
            for tf in sorted(p.rglob("test_*.py"))[:20]:
                try:
                    text = tf.read_text(encoding="utf-8", errors="replace")
                except OSError:
                    continue
                for m in _IMPORT_TEST_RE.finditer(text):
                    add(m.group(1))

    return proposed


def merge_behavior_signals(
    existing: list[str],
    locked: list[str],
    proposed: list[str],
    *,
    apply_proposed: bool,
) -> tuple[list[str], list[str]]:
    locked_set = {str(x).strip() for x in locked if str(x).strip()}
    base: list[str] = []
    seen: set[str] = set()
    for s in locked:
        st = str(s).strip()
        if st and st not in seen:
            seen.add(st)
            base.append(st)
    for s in existing:
        st = str(s).strip()
        if st and st not in seen and st not in locked_set:
            seen.add(st)
            base.append(st)
    new_only: list[str] = []
    if apply_proposed:
        for s in proposed:
            st = str(s).strip()
            if st and st not in seen:
                seen.add(st)
                base.append(st)
                new_only.append(st)
    else:
        for s in proposed:
            st = str(s).strip()
            if st and st not in seen:
                new_only.append(st)
    return base, new_only


@dataclass(frozen=True)
class CardRefreshResult:
    trinity_id: str
    ok: bool
    touch_content_hash: str
    must_read_count: int
    proposed_behavior_signals: tuple[str, ...]
    applied_behavior_signals: tuple[str, ...]
    dry_run: bool
    error: str | None = None


def refresh_trinity_card(
    vault_root: Path,
    trinity_id: str,
    cfg: TrinityConfig,
    *,
    dry_run: bool = False,
    apply_behavior_signals: bool = False,
) -> CardRefreshResult:
    try:
        card = load_trinity_card(vault_root, trinity_id)
        manifest = build_closure_manifest(
            vault_root,
            card,
            max_hops=cfg.max_closure_hops,
            max_paths=cfg.max_closure_paths,
        )
        touch = card.setdefault("touch", {})
        if not isinstance(touch, dict):
            touch = {}
            card["touch"] = touch

        existing = list(touch.get("behavior_signals") or [])
        locked = list(touch.get("behavior_signals_locked") or [])
        proposed = propose_behavior_signals(vault_root, card)
        merged, newly_applied = merge_behavior_signals(
            existing,
            locked,
            proposed,
            apply_proposed=apply_behavior_signals,
        )

        meta = card.setdefault("meta", {})
        if not isinstance(meta, dict):
            meta = {}
            card["meta"] = meta
        meta["touch_content_hash"] = manifest["touch_content_hash"]
        meta["touch_refreshed_at"] = _now_iso()
        meta["closure_must_read_count"] = len(manifest["must_read"])

        if apply_behavior_signals:
            touch["behavior_signals"] = merged

        if not dry_run:
            write_trinity_card(vault_root, trinity_id, card)
            # Re-hash after write so meta.touch_content_hash matches align's closure scan
            # (card/rules edits can shift neighbor mtimes between hash and persist).
            card = load_trinity_card(vault_root, trinity_id)
            manifest = build_closure_manifest(
                vault_root,
                card,
                max_hops=cfg.max_closure_hops,
                max_paths=cfg.max_closure_paths,
            )
            meta = card.setdefault("meta", {})
            if isinstance(meta, dict):
                meta["touch_content_hash"] = manifest["touch_content_hash"]
                meta["closure_must_read_count"] = len(manifest["must_read"])
            write_trinity_card(vault_root, trinity_id, card)

        return CardRefreshResult(
            trinity_id=trinity_id,
            ok=True,
            touch_content_hash=manifest["touch_content_hash"],
            must_read_count=len(manifest["must_read"]),
            proposed_behavior_signals=tuple(proposed),
            applied_behavior_signals=tuple(newly_applied),
            dry_run=dry_run,
        )
    except (OSError, ValueError, FileNotFoundError) as e:
        return CardRefreshResult(
            trinity_id=trinity_id,
            ok=False,
            touch_content_hash="",
            must_read_count=0,
            proposed_behavior_signals=(),
            applied_behavior_signals=(),
            dry_run=dry_run,
            error=str(e),
        )
    except Exception as e:
        from .trinity_dual_lock import SystemMutationForbidden

        if isinstance(e, SystemMutationForbidden):
            return CardRefreshResult(
                trinity_id=trinity_id,
                ok=False,
                touch_content_hash="",
                must_read_count=0,
                proposed_behavior_signals=(),
                applied_behavior_signals=(),
                dry_run=dry_run,
                error=str(e),
            )
        raise


def run_trinity_touch_refresh(
    vault_root: Path,
    *,
    trinity_ids: list[str] | None = None,
    dry_run: bool = False,
    apply_behavior_signals: bool = False,
    pilot_only: bool = True,
) -> dict[str, Any]:
    vault_root = vault_root.resolve()
    ensure_weave_paths(vault_root)
    weave_cfg = load_weave_config(vault_root)
    cfg = load_trinity_config(vault_root)
    if not weave_cfg.enabled or not cfg.enabled:
        return {"ok": True, "skipped": True, "reason": "weave or trinity disabled"}

    from .trinity_dual_lock import filter_mutable_trinity_ids

    ids = trinity_ids or list_trinity_card_ids(vault_root, pilot_only=pilot_only)
    mutable_ids, skipped_core = filter_mutable_trinity_ids(vault_root, ids)
    results: list[dict[str, Any]] = []
    ok_all = True
    for tid in skipped_core:
        results.append(
            {
                "trinity_id": tid,
                "ok": False,
                "skipped": True,
                "error": "maintenance_core_system_mutable_false",
            }
        )
    for tid in mutable_ids:
        r = refresh_trinity_card(
            vault_root,
            tid,
            cfg,
            dry_run=dry_run,
            apply_behavior_signals=apply_behavior_signals,
        )
        sig_key = (
            "applied_behavior_signals"
            if apply_behavior_signals
            else "pending_behavior_signals"
        )
        row = {
            "trinity_id": r.trinity_id,
            "ok": r.ok,
            "touch_content_hash": r.touch_content_hash,
            "must_read_count": r.must_read_count,
            "proposed_behavior_signals": list(r.proposed_behavior_signals),
            sig_key: list(r.applied_behavior_signals),
            "dry_run": r.dry_run,
        }
        if r.error:
            row["error"] = r.error
            ok_all = False
        results.append(row)

    out: dict[str, Any] = {
        "ok": ok_all and not skipped_core,
        "dry_run": dry_run,
        "apply_behavior_signals": apply_behavior_signals,
        "cards": results,
        "skipped_core_ids": skipped_core,
        "timestamp": _now_iso(),
    }
    if not dry_run:
        append_metric_row(
            vault_root,
            {
                "event": "trinity_touch_refresh",
                "ok": ok_all,
                "card_count": len(results),
                "apply_behavior_signals": apply_behavior_signals,
            },
        )
    return out


def maybe_refresh_on_pseudo_clock(vault_root: Path) -> dict[str, Any] | None:
    """Optional hook after pseudo_clock_tick when Config enables it."""
    cfg = load_trinity_config(vault_root)
    if not cfg.enabled or not cfg.touch_refresh_on_pseudo_clock:
        return None
    return run_trinity_touch_refresh(vault_root, dry_run=False, apply_behavior_signals=False)
