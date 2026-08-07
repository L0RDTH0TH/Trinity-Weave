"""Conceptual pin derive pack — pin-before-L5 first-class MO (v2 fidelity).

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

from .catalog_io import catalog_rows_by_id, load_yaml, project_root, user_story_paths
from .catalog_mint_pack import _collect_pin_titles
from .ux_mint_walk_files import parse_walk_card

_WIKI_RE = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]")
_PLACEHOLDER_PINS = frozenset({"", "needs pin", "needs_pin"})
_HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$", re.MULTILINE)
EXCERPT_SOFT_MAX = 1200
VALID_ROLES = frozenset({"primary", "supporting", "contrast"})


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


def find_roadmap_note_by_title(vault_root: Path, project_id: str, title: str) -> Path | None:
    title = normalize_pin_title(title)
    if not title:
        return None
    roadmap = project_root(vault_root, project_id) / "Roadmap"
    if not roadmap.is_dir():
        return None
    hits = sorted(roadmap.rglob(f"{title}.md"))

    def score(p: Path) -> tuple[int, str]:
        s = str(p)
        pen = 0
        if "/Versions/" in s:
            pen += 10
        if ".pre-" in p.name:
            pen += 5
        if "Roll-up" in p.name:
            pen += 2
        return (pen, s)

    if not hits:
        return None
    return sorted(hits, key=score)[0]


def extract_heading_excerpt(text: str, heading: str, *, soft_max: int = EXCERPT_SOFT_MAX) -> str:
    """Excerpt = weld; heading = locator. Empty heading → soft lead of note body."""
    heading = str(heading or "").strip()
    body = text
    if body.lstrip().startswith("---"):
        end = body.find("\n---", 3)
        if end != -1:
            body = body[end + 4 :]

    if not heading:
        return body.strip()[:soft_max].strip()

    want = heading.lstrip("#").strip().lower()
    matches = list(_HEADING_RE.finditer(body))
    for i, m in enumerate(matches):
        level = len(m.group(1))
        title = m.group(2).strip()
        if title.lower() != want:
            continue
        start = m.end()
        end = len(body)
        for j in range(i + 1, len(matches)):
            if len(matches[j].group(1)) <= level:
                end = matches[j].start()
                break
        chunk = body[start:end].strip()
        if len(chunk) > soft_max:
            return chunk[:soft_max].rstrip() + "\n\n_…excerpt truncated (soft budget)…_\n"
        return chunk
    return ""


def normalize_refs(raw: list[Any] | None, *, recommended: str = "") -> list[dict[str, str]]:
    refs: list[dict[str, str]] = []
    for item in raw or []:
        if not isinstance(item, dict):
            continue
        title = normalize_pin_title(str(item.get("title") or ""))
        if not title:
            continue
        role = str(item.get("role") or "supporting").strip().lower()
        if role not in VALID_ROLES:
            role = "supporting"
        refs.append(
            {
                "title": title,
                "heading": str(item.get("heading") or "").strip(),
                "role": role,
                "excerpt_note": str(item.get("excerpt_note") or "").strip(),
                "color_key": str(item.get("color_key") or "").strip(),
            }
        )
    if not refs and recommended:
        refs.append(
            {
                "title": normalize_pin_title(recommended),
                "heading": "",
                "role": "primary",
                "excerpt_note": "",
                "color_key": "",
            }
        )
    return refs


def validate_refs(refs: list[dict[str, str]], legal: set[str]) -> list[str]:
    violations: list[str] = []
    if not any(r.get("role") == "primary" for r in refs):
        violations.append("missing_primary_ref")
    for r in refs:
        if r["title"] not in legal:
            violations.append(f"ref_not_in_pin_index:{r['title']}")
    return violations


def first_emit_shared_primary_violations(proposals: list[dict[str, Any]]) -> list[str]:
    """If ≥2 planned series recommend the same PIN-INDEX title as primary → violation."""
    primary_owners: dict[str, list[str]] = {}
    for prop in proposals:
        rid = str(prop.get("row_id") or "").strip()
        refs = normalize_refs(
            prop.get("conceptual_pin_refs") or prop.get("refs"),
            recommended=str(prop.get("recommended") or ""),
        )
        primary = next((r for r in refs if r.get("role") == "primary"), None)
        if not primary:
            continue
        title = primary["title"]
        primary_owners.setdefault(title, []).append(rid)
    return [
        f"shared_primary_first_emit:{title}:{','.join(ids)}"
        for title, ids in primary_owners.items()
        if len(ids) >= 2
    ]


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
    refs: list[dict[str, str]] | None = None,
    vision_drift: bool = False,
    vision_drift_cite: str = "",
    mint_target: dict[str, Any] | None = None,
) -> str:
    cands = candidates[:3] if candidates else ([recommended] if recommended else [])
    refs = refs or normalize_refs(None, recommended=recommended)
    lines = [
        f"# PIN-DERIVE — `{row_id}`",
        "",
        f"- label: {label}",
        f"- status: proposed",
        f"- schema: pin_v2",
        (
            f"- recommended: [[{normalize_pin_title(recommended)}]]"
            if recommended
            else "- recommended: _(empty)_"
        ),
        f"- pin_focus: {pin_focus or '_(empty)_'}",
        f"- alternate: [[{normalize_pin_title(alt)}]]" if alt else "- alternate: _(none)_",
        f"- vision_drift: {'true' if vision_drift else 'false'}",
        f"- vision_drift_cite: {vision_drift_cite or '_(none)_'}",
        "",
        "## conceptual_pin_refs",
        "",
    ]
    if not refs:
        lines.append("_(none)_")
    else:
        for r in refs:
            lines.append(
                f"- title: [[{r['title']}]] | heading: {r['heading'] or '(whole note)'} | "
                f"role: {r['role']} | excerpt_note: {r['excerpt_note'] or '—'} | "
                f"color_key: {r['color_key'] or '—'}"
            )
    lines.extend(["", "## mint_target", ""])
    if mint_target:
        minted = bool(mint_target.get("minted"))
        path = str(mint_target.get("path") or "").strip()
        reject = str(mint_target.get("reject_reason") or "").strip()
        lines.append(
            f"- parent: {mint_target.get('parent') or '—'} | "
            f"proposed_title: {mint_target.get('proposed_title') or '—'} | "
            f"path_class: {mint_target.get('path_class') or 'amendment'} | "
            f"minted: {'true' if minted else 'false'} | "
            f"path: {path or '—'}"
        )
        if reject:
            lines.append(f"- reject_reason: {reject}")
    else:
        lines.append("_(none — Grok mint gate owns volume)_")
    lines.extend(
        [
            "",
            "## Series contract (Pass A / Trinity published)",
            "",
            (series_summary or label).strip()[:800],
            "",
            "## Candidates (PIN-INDEX only)",
            "",
        ]
    )
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
            "_Excerpt = weld; heading = locator. Pack PIN-EXCERPTS must match cited spans._",
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
        "_Pin-before-L5 v2. Live L5 must be absent/archived. Grok: PIN-DERIVE-VALIDATION "
        "(same-span PIN-EXCERPTS; mint gate; ≥1 primary)._",
        "",
        "## Per-row",
        "",
        "| row_id | recommended | primary_heading | pin_focus | status |",
        "|--------|-------------|-----------------|-----------|--------|",
    ]
    for r in results:
        refs = r.get("conceptual_pin_refs") or []
        primary = next((x for x in refs if x.get("role") == "primary"), None) or (
            refs[0] if refs else {}
        )
        heading = (primary.get("heading") or "whole")[:40] if isinstance(primary, dict) else "—"
        lines.append(
            f"| `{r.get('row_id')}` | `{r.get('recommended') or '—'}` | "
            f"{heading} | {(r.get('pin_focus') or '—')[:40]} | {r.get('status') or 'proposed'} |"
        )
    lines.extend(
        [
            "",
            "## Operator close",
            "",
            "After Grok receipt (judgment on same excerpts): confirm/waive → "
            "`apply_pins` (follow-on) → L5 mint (follow-on). "
            "Yellow weak pins → Grok pass-to-Cursor (loop cap: one re-derive).",
            "",
        ]
    )
    status_path.write_text("\n".join(lines), encoding="utf-8")
    return status_path


def materialize_pin_excerpts(
    vault_root: Path,
    project_id: str,
    *,
    row_id: str,
    refs: list[dict[str, str]],
    dest_dir: Path | None = None,
) -> tuple[list[str], list[str]]:
    """Write plain-text PIN-EXCERPTS for cited spans. Returns (paths, warnings)."""
    vault_root = vault_root.resolve()
    paths = user_story_paths(vault_root, project_id)
    out_dir = dest_dir or (paths["scopes_dir"].parent / "PIN-EXCERPTS")
    out_dir.mkdir(parents=True, exist_ok=True)
    written: list[str] = []
    warnings: list[str] = []
    for r in refs:
        title = r["title"]
        heading = r.get("heading") or ""
        note = find_roadmap_note_by_title(vault_root, project_id, title)
        if not note or not note.is_file():
            warnings.append(f"excerpt_source_missing:{row_id}:{title}")
            continue
        text = note.read_text(encoding="utf-8")
        excerpt = extract_heading_excerpt(text, heading)
        if heading and not excerpt.strip():
            warnings.append(f"excerpt_empty_for_heading:{row_id}:{title}:{heading}")
            continue
        if len(excerpt) > EXCERPT_SOFT_MAX and "_…excerpt truncated" not in excerpt:
            warnings.append(f"excerpt_soft_oversize:{row_id}:{title}:{len(excerpt)}")
        stem = f"{row_id}__{title}"
        if heading:
            hslug = re.sub(r"[^a-zA-Z0-9]+", "-", heading.lstrip("#").strip())[:48].strip("-")
            stem = f"{stem}__{hslug}"
        out = out_dir / f"{stem}.md"
        body = (
            f"# PIN-EXCERPT — `{row_id}` → [[{title}]]\n\n"
            f"- heading: {heading or '(whole note)'}\n"
            f"- role: {r.get('role')}\n"
            f"- excerpt_note: {r.get('excerpt_note') or '—'}\n"
            f"- source: `{note.relative_to(vault_root)}`\n"
            f"- weld_rule: excerpt text is the weld; heading is the locator\n\n"
            f"---\n\n"
            f"{excerpt.strip()}\n"
        )
        out.write_text(body, encoding="utf-8")
        written.append(str(out.relative_to(vault_root)))
    return written, warnings


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
    refs: list[dict[str, str]] | None = None,
    vision_drift: bool = False,
    vision_drift_cite: str = "",
    mint_target: dict[str, Any] | None = None,
) -> dict[str, Any]:
    legal = legal_pin_titles(vault_root, project_id)
    rec = normalize_pin_title(recommended)
    refs_n = normalize_refs(refs, recommended=rec)
    violations: list[str] = []
    if rec and rec not in legal:
        violations.append("recommended_not_in_pin_index")
    for c in candidates:
        if normalize_pin_title(c) not in legal:
            violations.append(f"candidate_not_in_pin_index:{normalize_pin_title(c)}")
    alt_n = normalize_pin_title(alt) if alt else ""
    if alt_n and alt_n not in legal:
        violations.append("alternate_not_in_pin_index")
    violations.extend(validate_refs(refs_n, legal))

    text = render_pin_derive_card(
        row_id=row_id,
        label=label,
        series_summary=series_summary,
        candidates=candidates,
        recommended=rec,
        pin_focus=pin_focus,
        rationale=rationale,
        alt=alt_n,
        refs=refs_n,
        vision_drift=vision_drift,
        vision_drift_cite=vision_drift_cite,
        mint_target=mint_target,
    )
    out = user_story_paths(vault_root, project_id)["scopes_dir"] / row_id / "PIN-DERIVE.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding="utf-8")
    excerpt_paths, excerpt_warn = materialize_pin_excerpts(
        vault_root, project_id, row_id=row_id, refs=refs_n
    )
    violations.extend(excerpt_warn)
    hard = [v for v in violations if not v.startswith("excerpt_soft_oversize")]
    return {
        "ok": not hard,
        "row_id": row_id,
        "path": str(out.relative_to(vault_root.resolve())),
        "recommended": rec,
        "pin_focus": pin_focus,
        "conceptual_pin_refs": refs_n,
        "vision_drift": vision_drift,
        "mint_target": mint_target,
        "excerpt_paths": excerpt_paths,
        "status": "proposed",
        "violations": violations,
    }


def emit_pin_derive_batch(
    vault_root: Path,
    project_id: str,
    proposals: list[dict[str, Any]],
) -> dict[str, Any]:
    """Write PIN-DERIVE cards + STATUS + PIN-EXCERPTS from proposal dicts."""
    vault_root = vault_root.resolve()
    paths = user_story_paths(vault_root, project_id)
    catalog = load_yaml(paths["catalog"])
    by_id = catalog_rows_by_id(catalog)
    results: list[dict[str, Any]] = []
    shared = first_emit_shared_primary_violations(proposals)
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
        refs_raw = prop.get("conceptual_pin_refs") or prop.get("refs")
        mint = prop.get("mint_target")
        if mint is not None and not isinstance(mint, dict):
            mint = None
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
            refs=list(refs_raw) if isinstance(refs_raw, list) else None,
            vision_drift=bool(prop.get("vision_drift")),
            vision_drift_cite=str(prop.get("vision_drift_cite") or ""),
            mint_target=mint,
        )
        results.append(out)
    status = emit_pin_derive_status(vault_root, project_id, results)
    return {
        "ok": all(r.get("ok") for r in results) if results else False,
        "row_count": len(results),
        "status_path": str(status.relative_to(vault_root)),
        "results": results,
        "first_emit_shared_primary_violations": shared,
        "detail": "pin_derive_emitted_v2",
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
        refs = normalize_refs(dec.get("conceptual_pin_refs") or dec.get("refs"), recommended=pin)
        if waived:
            row["pin_waived"] = True
            row["pin_waive_reason"] = str(dec.get("pin_waive_reason") or "operator_waive")
            row["conceptual_pin"] = "needs pin"
            row.pop("conceptual_pin_refs", None)
        else:
            if not pin or pin not in legal:
                errors.append(f"illegal_pin:{rid}:{pin}")
                continue
            if not refs:
                refs = normalize_refs(None, recommended=pin)
            ref_viol = validate_refs(refs, legal)
            if any(
                v.startswith("ref_not_in_pin_index") or v == "missing_primary_ref"
                for v in ref_viol
            ):
                errors.append(f"illegal_refs:{rid}:{','.join(ref_viol)}")
                continue
            row["conceptual_pin"] = f"[[{pin}]]"
            row["conceptual_pin_refs"] = refs
            row.pop("pin_waived", None)
            row.pop("pin_waive_reason", None)
            row.pop("mint_target", None)
        if dec.get("pin_focus"):
            row["pin_focus"] = str(dec.get("pin_focus"))
        if dec.get("vision_drift") is not None:
            row["vision_drift"] = bool(dec.get("vision_drift"))
        if dec.get("vision_drift_cite"):
            row["vision_drift_cite"] = str(dec.get("vision_drift_cite"))
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
