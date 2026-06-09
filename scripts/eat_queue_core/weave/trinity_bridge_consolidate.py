"""Phase 7 — merge provisional bridge cards sharing tunnel_via into one locked bridge."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .governance import append_metric_row, ensure_weave_paths
from .trinity_card import get_conceptual, get_rules, get_touch, normalize_card
from .trinity_card_paths import (
    component_proposals_dir,
    components_dir,
    load_trinity_card,
    write_trinity_card,
)
from .trinity_dual_lock import apply_lock_kind_to_card, operator_mutation_ctx
from .trinity_partition import upsert_registry_bridge
from .trinity_spine_guard import is_provisional_bridge_card, normalize_provisional_bridge_card


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def _tunnel_via(card: dict[str, Any]) -> str:
    touch = get_touch(card)
    return str(touch.get("tunnel_via") or touch.get("tunnel_target") or "").strip()


def _list_str_union(cards: list[dict[str, Any]], key: str, subkey: str | None = None) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for card in cards:
        block = card.get(key) if subkey is None else (card.get(key) or {}).get(subkey)
        if not isinstance(block, list):
            continue
        for item in block:
            s = str(item).strip()
            if s and s not in seen:
                seen.add(s)
                out.append(s)
    return out


def find_provisional_bridges_for_tunnel(
    vault_root: Path,
    tunnel_via: str,
) -> list[tuple[str, Path, dict[str, Any]]]:
    """Return (trinity_id, path, card) for provisional bridges targeting tunnel_via."""
    vault_root = vault_root.resolve()
    tv = str(tunnel_via or "").strip()
    if not tv:
        return []
    base = component_proposals_dir(vault_root)
    if not base.is_dir():
        return []
    found: list[tuple[str, Path, dict[str, Any]]] = []
    for path in sorted(base.glob("*.yaml")):
        if path.name.startswith("_"):
            continue
        try:
            card = load_trinity_card(vault_root, path.stem, prefer="provisional")
        except (OSError, ValueError, FileNotFoundError):
            continue
        if not is_provisional_bridge_card(card):
            continue
        if _tunnel_via(card) != tv:
            continue
        tid = str(card.get("id") or path.stem).strip()
        found.append((tid, path, card))
    return found


def merge_bridge_cards(
    cards: list[dict[str, Any]],
    *,
    output_id: str,
    tunnel_via: str,
) -> dict[str, Any]:
    """Merge provisional bridge stubs into one normalized bridge card."""
    tv = str(tunnel_via).strip()
    pairs: set[str] = {tv}
    paths: set[str] = set()
    summaries: list[str] = []
    outcomes: list[str] = []
    forbidden: set[str] = set()

    for card in cards:
        touch = get_touch(card)
        for p in touch.get("pairs_with") or []:
            s = str(p).strip()
            if s:
                pairs.add(s)
        for p in touch.get("primary_paths") or []:
            s = str(p).strip().replace("\\", "/").lstrip("./")
            if s:
                paths.add(s)
        conc = get_conceptual(card)
        if conc.get("summary"):
            summaries.append(str(conc["summary"]).strip())
        if conc.get("outcome"):
            outcomes.append(str(conc["outcome"]).strip())
        rules = get_rules(card)
        for f in rules.get("forbidden") or []:
            s = str(f).strip()
            if s:
                forbidden.add(s)

    merged: dict[str, Any] = {
        "id": output_id,
        "meta": {
            "anatomy": "bridge",
            "provisional": False,
            "card_class": "consolidated_bridge",
            "consolidated_at": _now_iso(),
            "consolidated_from": [str(c.get("id") or "") for c in cards],
        },
        "touch": {
            "bridge_scope": True,
            "tunnel_via": tv,
            "pairs_with": sorted(pairs),
            "primary_paths": sorted(paths)[:24],
        },
        "conceptual": {
            "outcome": outcomes[0] if outcomes else f"Consolidated bridge for {tv}",
            "summary": " · ".join(summaries[:4]) if summaries else f"Merged bridge tunnel → {tv}",
        },
        "rules": {
            "forbidden": sorted(forbidden)[:16],
            "precedence": [],
            "acceptance": [
                "Consolidated from provisional bridges sharing tunnel_via",
            ],
        },
    }
    return normalize_provisional_bridge_card(merged)


def run_trinity_bridge_consolidate(
    vault_root: Path,
    *,
    tunnel_via: str,
    output_id: str | None = None,
    dry_run: bool = False,
    force: bool = False,
    lock_kind: str = "full",
) -> dict[str, Any]:
    """Operator-triggered merge of provisional bridges → locked bridge + registry row."""
    vault_root = vault_root.resolve()
    ensure_weave_paths(vault_root)
    tv = str(tunnel_via or "").strip()
    if not tv:
        return {"ok": False, "error": "tunnel_via required"}

    sources = find_provisional_bridges_for_tunnel(vault_root, tv)
    if len(sources) < 2 and not force:
        return {
            "ok": False,
            "error": "insufficient_provisional_bridges",
            "tunnel_via": tv,
            "count": len(sources),
            "hint": "Need ≥2 provisional bridges or pass --force",
            "found_ids": [s[0] for s in sources],
        }

    if not sources:
        return {"ok": False, "error": "no_provisional_bridges", "tunnel_via": tv}

    out_id = str(output_id or f"{tv}_bridge_consolidated").strip()
    locked_path = components_dir(vault_root) / f"{out_id}.yaml"
    if locked_path.is_file() and not force:
        return {
            "ok": False,
            "error": "output_exists",
            "trinity_id": out_id,
            "path": locked_path.relative_to(vault_root).as_posix(),
            "hint": "pass --force to overwrite",
        }

    cards = [c for _, _, c in sources]
    merged = merge_bridge_cards(cards, output_id=out_id, tunnel_via=tv)
    now = _now_iso()
    kind = str(lock_kind or "full").strip().lower()
    if kind not in ("full", "conceptual_spine"):
        kind = "full"
    merged = apply_lock_kind_to_card(merged, kind, now_iso=now)  # type: ignore[arg-type]

    source_ids = [s[0] for s in sources]
    result: dict[str, Any] = {
        "ok": True,
        "tunnel_via": tv,
        "output_trinity_id": out_id,
        "merged_from": source_ids,
        "dry_run": dry_run,
    }

    if dry_run:
        result["would_write"] = locked_path.relative_to(vault_root).as_posix()
        result["would_remove"] = [
            p.relative_to(vault_root).as_posix() for _, p, _ in sources
        ]
        reg = upsert_registry_bridge(
            vault_root,
            trinity_id=out_id,
            dry_run=True,
        )
        result["registry"] = reg
        return result

    token = operator_mutation_ctx.set(True)
    try:
        write_trinity_card(
            vault_root,
            out_id,
            merged,
            tier="locked",
            mutation_action="bridge_consolidate",
            operator_override=True,
        )
        for tid, path, _ in sources:
            if path.is_file() and path.stem != out_id:
                path.unlink()
    finally:
        operator_mutation_ctx.reset(token)

    reg = upsert_registry_bridge(vault_root, trinity_id=out_id, status="locked")
    result["locked_path"] = locked_path.relative_to(vault_root).as_posix()
    result["registry"] = reg
    result["removed_provisionals"] = [
        p.relative_to(vault_root).as_posix()
        for _, p, _ in sources
        if p.stem != out_id
    ]

    out_dir = vault_root / ".technical" / "weave" / "validation"
    out_dir.mkdir(parents=True, exist_ok=True)
    report_path = out_dir / f"trinity-bridge-consolidate-{_stamp()}.json"
    report_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    result["report_path"] = str(report_path)

    append_metric_row(
        vault_root,
        {
            "metric_type": "trinity_bridge_consolidate",
            "ok": True,
            "tunnel_via": tv,
            "trinity_id": out_id,
            "merged_from": source_ids,
        },
    )
    return result
