"""Trinity boundary audit — read-only component vs bridge overlap checks (Phase 0)."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .trinity_card import get_conceptual, get_touch
from .trinity_card_paths import components_dir, is_locked_card, load_trinity_card
from .trinity_partition import load_partition_registry

Severity = str  # error | warn | info


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def _normalize_path(p: str) -> str:
    return str(p).strip().replace("\\", "/").lstrip("./")


def _primary_paths(card: dict[str, Any]) -> list[str]:
    touch = get_touch(card)
    raw = touch.get("primary_paths")
    if not isinstance(raw, list):
        return []
    return [_normalize_path(str(x)) for x in raw if str(x).strip()]


def _pairs_with(card: dict[str, Any]) -> list[str]:
    for key in ("pairs_with",):
        raw = card.get(key)
        if isinstance(raw, list):
            return [str(x).strip() for x in raw if str(x).strip()]
    touch = get_touch(card)
    raw = touch.get("pairs_with")
    if isinstance(raw, list):
        return [str(x).strip() for x in raw if str(x).strip()]
    return []


def _bridge_targets(card: dict[str, Any]) -> list[str]:
    touch = get_touch(card)
    raw = touch.get("bridges")
    if isinstance(raw, list):
        return [str(x).strip() for x in raw if str(x).strip()]
    conc = get_conceptual(card)
    refs = conc.get("refs")
    if isinstance(refs, list):
        return [str(x).strip() for x in refs if str(x).strip()]
    return []


@dataclass
class BoundaryFinding:
    kind: str
    severity: Severity
    trinity_id: str
    detail: str
    peer_id: str = ""
    paths: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class CardBoundaryRow:
    trinity_id: str
    anatomy: str
    locked: bool
    primary_anchor: str
    primary_paths: list[str]
    anchor_in_primary_paths: bool
    findings: list[BoundaryFinding] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "trinity_id": self.trinity_id,
            "anatomy": self.anatomy,
            "locked": self.locked,
            "primary_anchor": self.primary_anchor,
            "primary_paths": self.primary_paths,
            "anchor_in_primary_paths": self.anchor_in_primary_paths,
            "findings": [f.to_dict() for f in self.findings],
        }


def _validation_dir(vault_root: Path) -> Path:
    return vault_root / ".technical" / "weave" / "validation"


def run_trinity_boundary_audit(
    vault_root: Path,
    *,
    partition: str = "maintenance",
    trinity_ids: list[str] | None = None,
    write_report: bool = True,
) -> dict[str, Any]:
    """Audit locked component cards for path/anchor overlap (read-only)."""
    vault_root = vault_root.resolve()
    reg = load_partition_registry(vault_root)

    if partition != "maintenance":
        scope_ids = trinity_ids or []
    else:
        scope_ids = trinity_ids or reg.maintenance_component_ids()

    cards: dict[str, dict[str, Any]] = {}
    rows: list[CardBoundaryRow] = []
    global_findings: list[BoundaryFinding] = []

    for tid in scope_ids:
        entry = reg.entry_for(tid)
        anatomy = reg.anatomy_for(tid)
        try:
            card = load_trinity_card(vault_root, tid, prefer="locked")
        except FileNotFoundError:
            global_findings.append(
                BoundaryFinding(
                    kind="card_missing",
                    severity="error",
                    trinity_id=tid,
                    detail="Expected locked component card not found under components/",
                )
            )
            continue
        cards[tid] = card
        paths = _primary_paths(card)
        anchor = entry.primary_anchor if entry else ""
        anchor_norm = _normalize_path(anchor) if anchor else ""
        row = CardBoundaryRow(
            trinity_id=tid,
            anatomy=anatomy,
            locked=is_locked_card(card),
            primary_anchor=anchor,
            primary_paths=paths,
            anchor_in_primary_paths=bool(anchor_norm and anchor_norm in paths),
        )
        if anatomy == "component" and anchor_norm and anchor_norm not in paths:
            row.findings.append(
                BoundaryFinding(
                    kind="anchor_not_in_primary_paths",
                    severity="warn",
                    trinity_id=tid,
                    detail=f"Registry primary_anchor not listed in touch.primary_paths: {anchor_norm}",
                    paths=[anchor_norm],
                )
            )
        if not is_locked_card(card):
            row.findings.append(
                BoundaryFinding(
                    kind="not_locked",
                    severity="error",
                    trinity_id=tid,
                    detail="Component in maintenance scope lacks lock stamps",
                )
            )
        rows.append(row)

    # Primary path overlap between component pairs
    path_index: dict[str, list[str]] = {}
    for tid, card in cards.items():
        for p in _primary_paths(card):
            path_index.setdefault(p, []).append(tid)

    watch_pairs: set[frozenset[str]] = set()
    for risk in reg.known_overlap_risks:
        ids = risk.get("ids") or []
        if isinstance(ids, list) and len(ids) >= 2:
            watch_pairs.add(frozenset(str(x) for x in ids[:2]))

    for path, owners in sorted(path_index.items()):
        if len(owners) < 2:
            continue
        pair = frozenset(owners[:2]) if len(owners) == 2 else frozenset(owners)
        sev: Severity = "warn"
        detail = f"Shared touch.primary_paths entry: {path}"
        if pair in watch_pairs or any(
            pair == frozenset(r.get("ids") or []) for r in reg.known_overlap_risks
        ):
            detail += " (known overlap-watch pair — verify intentional closure vs merged ownership)"
        for tid in owners:
            for row in rows:
                if row.trinity_id == tid:
                    row.findings.append(
                        BoundaryFinding(
                            kind="primary_path_overlap",
                            severity=sev,
                            trinity_id=tid,
                            detail=detail,
                            peer_id=next((o for o in owners if o != tid), ""),
                            paths=[path],
                        )
                    )

    # Anchor collision — two components, same registry anchor
    anchor_index: dict[str, list[str]] = {}
    for tid in scope_ids:
        entry = reg.entry_for(tid)
        if not entry or not entry.primary_anchor:
            continue
        anchor_index.setdefault(_normalize_path(entry.primary_anchor), []).append(tid)
    for anchor, owners in anchor_index.items():
        if len(owners) < 2:
            continue
        for tid in owners:
            for row in rows:
                if row.trinity_id == tid:
                    row.findings.append(
                        BoundaryFinding(
                            kind="anchor_collision",
                            severity="error",
                            trinity_id=tid,
                            detail=f"Registry primary_anchor shared with {owners}: {anchor}",
                            peer_id=next((o for o in owners if o != tid), ""),
                            paths=[anchor],
                        )
                    )

    # pairs_with recommendations for overlap-watch peers
    for risk in reg.known_overlap_risks:
        ids = [str(x) for x in (risk.get("ids") or [])]
        if len(ids) != 2:
            continue
        a, b = ids[0], ids[1]
        if a not in cards or b not in cards:
            continue
        pa = _pairs_with(cards[a])
        pb = _pairs_with(cards[b])
        if b not in pa and a not in pb:
            for tid in (a, b):
                for row in rows:
                    if row.trinity_id == tid:
                        row.findings.append(
                            BoundaryFinding(
                                kind="pairs_with_missing",
                                severity="info",
                                trinity_id=tid,
                                detail=f"No pairs_with link to peer {b if tid == a else a} (optional documentation)",
                                peer_id=b if tid == a else a,
                            )
                        )

    # Planned bridges without card file
    for bid, entry in reg.bridges.items():
        bridge_path = components_dir(vault_root) / f"{bid}.yaml"
        if not bridge_path.is_file():
            global_findings.append(
                BoundaryFinding(
                    kind="bridge_card_missing",
                    severity="info" if entry.status == "planned" else "warn",
                    trinity_id=bid,
                    detail=f"Bridge listed in registry (status={entry.status}) but no locked card yet",
                )
            )
            continue
        try:
            bcard = load_trinity_card(vault_root, bid, prefer="locked")
        except FileNotFoundError:
            continue
        targets = _bridge_targets(bcard)
        if len(targets) < 2:
            global_findings.append(
                BoundaryFinding(
                    kind="bridge_without_endpoints",
                    severity="error",
                    trinity_id=bid,
                    detail="Bridge card must list >=2 component ids in touch.bridges or conceptual.refs",
                )
            )
        bpaths = _primary_paths(bcard)
        for tid, card in cards.items():
            anchor = _normalize_path(reg.entry_for(tid).primary_anchor) if reg.entry_for(tid) else ""
            if anchor and anchor in bpaths:
                global_findings.append(
                    BoundaryFinding(
                        kind="bridge_owns_component_path",
                        severity="error",
                        trinity_id=bid,
                        detail=f"Bridge primary_paths includes component anchor {anchor} ({tid})",
                        peer_id=tid,
                        paths=[anchor],
                    )
                )

    # Conceptual cross-claim heuristic: component id of peer in outcome
    for risk in reg.known_overlap_risks:
        ids = [str(x) for x in (risk.get("ids") or [])]
        if len(ids) != 2:
            continue
        a, b = ids[0], ids[1]
        if a not in cards or b not in cards:
            continue
        for tid, peer in ((a, b), (b, a)):
            conc = get_conceptual(cards[tid])
            text = " ".join(
                str(conc.get(k) or "")
                for k in ("outcome", "summary", "primary_case")
            ).lower()
            peer_human = peer.replace("_", " ")
            if peer in text or peer_human in text:
                for row in rows:
                    if row.trinity_id == tid:
                        row.findings.append(
                            BoundaryFinding(
                                kind="conceptual_peer_reference",
                                severity="info",
                                trinity_id=tid,
                                detail=f"Conceptual text references peer '{peer}' — verify boundary not merged",
                                peer_id=peer,
                            )
                        )

    errors = sum(
        1
        for row in rows
        for f in row.findings
        if f.severity == "error"
    ) + sum(1 for f in global_findings if f.severity == "error")
    warns = sum(
        1
        for row in rows
        for f in row.findings
        if f.severity == "warn"
    ) + sum(1 for f in global_findings if f.severity == "warn")

    out: dict[str, Any] = {
        "ok": errors == 0,
        "stamp": _stamp(),
        "completed_at": _now_iso(),
        "partition": partition,
        "scope_ids": scope_ids,
        "summary": {
            "cards_audited": len(rows),
            "errors": errors,
            "warnings": warns,
            "global_findings": len(global_findings),
        },
        "rows": [r.to_dict() for r in rows],
        "global_findings": [f.to_dict() for f in global_findings],
        "known_overlap_risks": reg.known_overlap_risks,
    }

    if write_report:
        vdir = _validation_dir(vault_root)
        vdir.mkdir(parents=True, exist_ok=True)
        json_path = vdir / f"trinity-boundary-{out['stamp']}.json"
        json_path.write_text(json.dumps(out, indent=2), encoding="utf-8")
        md_path = vdir / f"trinity-boundary-{out['stamp']}.md"
        md_path.write_text(_format_markdown_report(out), encoding="utf-8")
        out["report_json"] = str(json_path.relative_to(vault_root))
        out["report_md"] = str(md_path.relative_to(vault_root))

    return out


def _format_markdown_report(data: dict[str, Any]) -> str:
    lines = [
        "# Trinity boundary audit",
        "",
        f"- **Completed:** {data.get('completed_at')}",
        f"- **Partition:** {data.get('partition')}",
        f"- **OK:** {data.get('ok')}",
        f"- **Summary:** {json.dumps(data.get('summary') or {})}",
        "",
        "## Per card",
        "",
        "| trinity_id | anatomy | locked | anchor OK | errors | warnings |",
        "|------------|---------|--------|-----------|--------|----------|",
    ]
    for row in data.get("rows") or []:
        tid = row.get("trinity_id")
        findings = row.get("findings") or []
        ec = sum(1 for f in findings if f.get("severity") == "error")
        wc = sum(1 for f in findings if f.get("severity") == "warn")
        lines.append(
            f"| {tid} | {row.get('anatomy')} | {row.get('locked')} | "
            f"{row.get('anchor_in_primary_paths')} | {ec} | {wc} |"
        )
    lines.extend(["", "## Findings (detail)", ""])
    for row in data.get("rows") or []:
        tid = row.get("trinity_id")
        for f in row.get("findings") or []:
            if f.get("severity") == "info":
                continue
            lines.append(
                f"- **{tid}** [{f.get('severity')}] `{f.get('kind')}`: {f.get('detail')}"
            )
    for f in data.get("global_findings") or []:
        if f.get("severity") == "info":
            continue
        lines.append(
            f"- **{f.get('trinity_id')}** [{f.get('severity')}] `{f.get('kind')}`: {f.get('detail')}"
        )
    lines.extend(["", "## Operator sign-off", "", "- [ ] Phase 0 boundary audit reviewed", ""])
    return "\n".join(lines)
