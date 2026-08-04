"""Conceptual pin derive pack — pin-before-L5 first-class MO.

Cursor drafts PIN-DERIVE cards from PIN-INDEX + SERIES (no live L5).
Grok validates via PIN-DERIVE-VALIDATION. Operator apply_pins is a follow-on.
"""

from __future__ import annotations

import hashlib
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

from .catalog_io import catalog_rows_by_id, load_yaml, user_story_paths
from .catalog_mint_pack import _collect_pin_titles
from .ux_mint_walk_files import parse_walk_card

_WIKI_RE = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]")
_PLACEHOLDER_PINS = frozenset({"", "needs pin", "needs_pin"})


def _utc_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _utc_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def is_placeholder_pin(pin: str | None) -> bool:
    p = str(pin or "").strip()
    if not p:
        return True
    low = p.lower()
    return low in _PLACEHOLDER_PINS or "needs pin" in low


def normalize_pin_title(pin: str) -> str:
    p = str(pin or "").strip()
    m = _WIKI_RE.search(p)
    if m:
        return m.group(1).strip()
    if p.startswith("[[") and p.endswith("]]"):
        return p[2:-2].split("|", 1)[0].split("#", 1)[0].strip()
    return p


def legal_pin_titles(vault_root: Path, project_id: str) -> set[str]:
    return {normalize_pin_title(t) for t in _collect_pin_titles(vault_root, project_id)}


def row_pin_waived(row: dict[str, Any]) -> bool:
    return bool(
        row.get("pin_waived") is True
        or str(row.get("pin_waived") or "").lower() in {"true", "1", "yes"}
    )


def pin_gate_ok(
    row: dict[str, Any] | None, *, series_pin: str | None = None
) -> tuple[bool, str]:
    """Pass if resolved pin or recorded waive. Fail on silent needs_pin."""
    row = row or {}
    pin = str(series_pin if series_pin is not None else row.get("conceptual_pin") or "").strip()
    if row_pin_waived(row):
        return True, "waived"
    if is_placeholder_pin(pin):
        return False, "needs_pin_unresolved"
    return True, "pinned"


def render_pin_derive_card(
    *,
    row_id: str,
    label: str,
    series_summary: str,
    candidates: list[str],
    recommended: str,
    pin_focus: str,
    rationale: str,
    alt: str = "",
) -> str:
    cands = candidates[:3] if candidates else ([recommended] if recommended else [])
    lines = [
        f"# PIN-DERIVE — `{row_id}`",
        "",
        f"- label: {label}",
        f"- status: proposed",
        (
            f"- recommended: [[{normalize_pin_title(recommended)}]]"
            if recommended
            else "- recommended: _(empty)_"
        ),
        f"- pin_focus: {pin_focus or '_(empty)_'}",
        f"- alternate: [[{normalize_pin_title(alt)}]]" if alt else "- alternate: _(none)_",
        "",
        "## Series contract (Pass B locked)",
        "",
        (series_summary or label).strip()[:800],
        "",
        "## Candidates (PIN-INDEX only)",
        "",
    ]
    for i, c in enumerate(cands, 1):
        lines.append(f"{i}. [[{normalize_pin_title(c)}]]")
    lines.extend(
        [
            "",
            "## Rationale",
            "",
            (rationale or "_TBD_").strip(),
            "",
            "## Operator",
            "",
            "- [ ] confirm recommended",
            "- [ ] confirm alternate",
            "- [ ] waive (reason below)",
            "",
            "waive_reason:",
            "",
        ]
    )
    return "\n".join(lines)


def emit_pin_derive_status(
    vault_root: Path,
    project_id: str,
    results: list[dict[str, Any]],
) -> Path:
    paths = user_story_paths(vault_root, project_id)
    status_path = paths["scopes_dir"].parent / "PIN-DERIVE-STATUS.md"
    lines = [
        f"# PIN-DERIVE-STATUS — `{project_id}`",
        "",
        f"emitted_at: {_utc_iso()}",
        "",
        "_Pin-before-L5. Live L5 must be absent/archived. Grok: PIN-DERIVE-VALIDATION._",
        "",
        "## Per-row",
        "",
        "| row_id | recommended | pin_focus | status |",
        "|--------|-------------|-----------|--------|",
    ]
    for r in results:
        lines.append(
            f"| `{r.get('row_id')}` | `{r.get('recommended') or '—'}` | "
            f"{(r.get('pin_focus') or '—')[:48]} | {r.get('status') or 'proposed'} |"
        )
    lines.extend(
        [
            "",
            "## Operator close",
            "",
            "After Grok receipt: confirm/waive → `apply_pins` (follow-on) → L5 mint (follow-on).",
            "",
        ]
    )
    status_path.write_text("\n".join(lines), encoding="utf-8")
    return status_path


def write_pin_derive_card(
    vault_root: Path,
    project_id: str,
    *,
    row_id: str,
    label: str,
    series_summary: str,
    candidates: list[str],
    recommended: str,
    pin_focus: str,
    rationale: str,
    alt: str = "",
) -> dict[str, Any]:
    legal = legal_pin_titles(vault_root, project_id)
    rec = normalize_pin_title(recommended)
    violations: list[str] = []
    if rec and rec not in legal:
        violations.append("recommended_not_in_pin_index")
    for c in candidates:
        if normalize_pin_title(c) not in legal:
            violations.append(f"candidate_not_in_pin_index:{normalize_pin_title(c)}")
    alt_n = normalize_pin_title(alt) if alt else ""
    if alt_n and alt_n not in legal:
        violations.append("alternate_not_in_pin_index")

    text = render_pin_derive_card(
        row_id=row_id,
        label=label,
        series_summary=series_summary,
        candidates=candidates,
        recommended=rec,
        pin_focus=pin_focus,
        rationale=rationale,
        alt=alt_n,
    )
    out = user_story_paths(vault_root, project_id)["scopes_dir"] / row_id / "PIN-DERIVE.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding="utf-8")
    return {
        "ok": not violations,
        "row_id": row_id,
        "path": str(out.relative_to(vault_root.resolve())),
        "recommended": rec,
        "pin_focus": pin_focus,
        "status": "proposed",
        "violations": violations,
    }


def emit_pin_derive_batch(
    vault_root: Path,
    project_id: str,
    proposals: list[dict[str, Any]],
) -> dict[str, Any]:
    """Write PIN-DERIVE cards + STATUS from proposal dicts."""
    vault_root = vault_root.resolve()
    paths = user_story_paths(vault_root, project_id)
    catalog = load_yaml(paths["catalog"])
    by_id = catalog_rows_by_id(catalog)
    results: list[dict[str, Any]] = []
    for prop in proposals:
        rid = str(prop.get("row_id") or "").strip()
        if not rid:
            continue
        series_path = paths["scopes_dir"] / rid / "SERIES.md"
        label = str(prop.get("label") or (by_id.get(rid) or {}).get("label") or rid)
        summary = str(prop.get("summary") or "")
        if series_path.is_file():
            card = parse_walk_card(series_path.read_text(encoding="utf-8"), fallback_id=rid)
            label = str(card.get("label") or label)
            summary = summary or str(card.get("summary") or "")
        cands = [str(x) for x in (prop.get("candidates") or []) if str(x).strip()]
        rec = str(prop.get("recommended") or (cands[0] if cands else ""))
        if rec and rec not in cands:
            cands = [rec] + cands
        out = write_pin_derive_card(
            vault_root,
            project_id,
            row_id=rid,
            label=label,
            series_summary=summary,
            candidates=cands[:3],
            recommended=rec,
            pin_focus=str(prop.get("pin_focus") or ""),
            rationale=str(prop.get("rationale") or ""),
            alt=str(prop.get("alt") or (cands[1] if len(cands) > 1 else "")),
        )
        results.append(out)
    status = emit_pin_derive_status(vault_root, project_id, results)
    return {
        "ok": all(r.get("ok") for r in results) if results else False,
        "row_count": len(results),
        "status_path": str(status.relative_to(vault_root)),
        "results": results,
        "detail": "pin_derive_emitted",
    }


def apply_pins(
    vault_root: Path,
    project_id: str,
    decisions: list[dict[str, Any]],
) -> dict[str, Any]:
    """Apply operator pin decisions to slice-catalog (+ series cards when present)."""
    vault_root = vault_root.resolve()
    paths = user_story_paths(vault_root, project_id)
    cat_path = paths["catalog"]
    catalog = load_yaml(cat_path)
    rows = catalog.get("rows") if isinstance(catalog.get("rows"), list) else []
    by_id = {str(r.get("id") or ""): r for r in rows if isinstance(r, dict)}
    legal = legal_pin_titles(vault_root, project_id)
    applied: list[str] = []
    errors: list[str] = []
    for dec in decisions:
        rid = str(dec.get("row_id") or "").strip()
        row = by_id.get(rid)
        if not row:
            errors.append(f"missing_row:{rid}")
            continue
        waived = bool(dec.get("pin_waived"))
        pin = normalize_pin_title(str(dec.get("conceptual_pin") or ""))
        if waived:
            row["pin_waived"] = True
            row["pin_waive_reason"] = str(dec.get("pin_waive_reason") or "operator_waive")
            row["conceptual_pin"] = "needs pin"
        else:
            if not pin or pin not in legal:
                errors.append(f"illegal_pin:{rid}:{pin}")
                continue
            row["conceptual_pin"] = f"[[{pin}]]"
            row.pop("pin_waived", None)
            row.pop("pin_waive_reason", None)
        if dec.get("pin_focus"):
            row["pin_focus"] = str(dec.get("pin_focus"))
        series_path = paths["scopes_dir"] / rid / "SERIES.md"
        if series_path.is_file():
            text = series_path.read_text(encoding="utf-8")
            pin_line = f"- conceptual_pin: {row.get('conceptual_pin')}"
            if re.search(r"(?m)^- conceptual_pin:.*$", text):
                text = re.sub(r"(?m)^- conceptual_pin:.*$", pin_line, text, count=1)
            else:
                text = text.rstrip() + "\n" + pin_line + "\n"
            if waived:
                text = re.sub(r"(?m)^- pin_waived:.*$\n?", "", text)
                text = re.sub(r"(?m)^- pin_waive_reason:.*$\n?", "", text)
                text = text.rstrip() + (
                    f"\n- pin_waived: true\n"
                    f"- pin_waive_reason: {row.get('pin_waive_reason')}\n"
                )
            series_path.write_text(text, encoding="utf-8")
        applied.append(rid)
    cat_path.write_text(
        yaml.safe_dump(catalog, sort_keys=False, allow_unicode=True), encoding="utf-8"
    )
    return {
        "ok": not errors,
        "applied": applied,
        "errors": errors,
        "detail": "pins_applied" if not errors else "pins_apply_partial",
    }


def archive_l5_pre_pin_lens(
    vault_root: Path,
    *,
    project_id: str,
    row_ids: list[str] | None = None,
    stamp: str | None = None,
) -> dict[str, Any]:
    """Archive L5.md + L5-AFFIRM-DIGEST.md under Versions/l5-pre-pin-lens-<stamp>/."""
    vault_root = vault_root.resolve()
    paths = user_story_paths(vault_root, project_id)
    catalog = load_yaml(paths["catalog"])
    by_id = catalog_rows_by_id(catalog)
    ids = row_ids or [rid for rid, r in by_id.items() if r.get("planned") is True]
    ts = stamp or _utc_stamp()
    dest = paths["scopes_dir"].parent / "Versions" / f"l5-pre-pin-lens-{ts}"
    dest.mkdir(parents=True, exist_ok=True)
    manifest: list[str] = [f"# L5 pre-pin-lens archive — {project_id}", f"stamp: {ts}", ""]
    copied: list[str] = []
    live_paths: list[Path] = []
    for rid in ids:
        for name in ("L5.md", "L5-AFFIRM-DIGEST.md"):
            src = paths["scopes_dir"] / rid / name
            if not src.is_file():
                continue
            text = src.read_text(encoding="utf-8")
            digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
            out = dest / rid / name
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(text, encoding="utf-8")
            rel = str(src.relative_to(vault_root))
            manifest.append(f"{digest}  {rel}")
            copied.append(rel)
            live_paths.append(src)
    status = paths["scopes_dir"].parent / "L5-AFFIRM-STATUS.md"
    if status.is_file():
        text = status.read_text(encoding="utf-8")
        digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
        (dest / "L5-AFFIRM-STATUS.md").write_text(text, encoding="utf-8")
        manifest.append(f"{digest}  {status.relative_to(vault_root)}")
        copied.append(str(status.relative_to(vault_root)))
        live_paths.append(status)
    (dest / "MANIFEST.sha256").write_text("\n".join(manifest) + "\n", encoding="utf-8")
    return {
        "ok": True,
        "archive_dir": str(dest.relative_to(vault_root)),
        "copied": copied,
        "live_paths": [str(p) for p in live_paths],
        "stamp": ts,
    }
