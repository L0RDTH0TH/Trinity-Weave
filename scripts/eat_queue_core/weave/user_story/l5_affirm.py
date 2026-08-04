"""Pass-B-aligned L5 affirm gate + digest/STATUS emit (first-class Loop 2 MO)."""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .catalog_io import catalog_rows_by_id, load_yaml, user_story_paths
from .depth_scope import scope_path
from .l5_thin_config import is_thin_l5_parent, thin_min_moments
from .l5_voice import validate_l5_voice

_REQUIRED_HEADINGS = (
    "What it is",
    "Moment inventory",
    "Full vision",
    "Early / PoC cut",
    "Hard dependencies",
    "Out of scope",
    "Alternatives not banned",
    "does_not_mandate",
    "Source anchors",
)

_PACK_SMELL = re.compile(
    r"(?i)\b("
    r"spell\s+list|class\s+list|subclass\s+roster|monster\s+manual|"
    r"merchant\s+table|full\s+srd\s+roster|complete\s+spell\s+compendium|"
    r"every\s+class\s+and\s+subclass"
    r")\b"
)

_MOMENT_BULLET = re.compile(r"(?m)^-\s+")
_SECTION_RE = re.compile(r"(?im)^##\s+(.+?)\s*$")


def _utc_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _strip_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    import yaml

    try:
        fm = yaml.safe_load(text[3:end].strip()) or {}
    except Exception:
        fm = {}
    body = text[end + 4 :].lstrip("\n")
    return fm if isinstance(fm, dict) else {}, body


def _section_body(text: str, heading: str) -> str:
    _, body = _strip_frontmatter(text)
    matches = list(_SECTION_RE.finditer(body))
    for i, m in enumerate(matches):
        if m.group(1).strip().lower() == heading.lower():
            start = m.end()
            end = matches[i + 1].start() if i + 1 < len(matches) else len(body)
            return body[start:end].strip()
    return ""


def _count_moment_bullets(text: str) -> int:
    inv = _section_body(text, "Moment inventory")
    return len(_MOMENT_BULLET.findall(inv))


def _known_row_ids(vault_root: Path, project_id: str) -> set[str]:
    paths = user_story_paths(vault_root, project_id)
    ids: set[str] = set()
    catalog = load_yaml(paths["catalog"])
    ids.update(catalog_rows_by_id(catalog).keys())
    try:
        from .ux_mint_backlog import load_mint_backlog

        bl = load_mint_backlog(vault_root, project_id)
        for it in bl.get("items") or []:
            if isinstance(it, dict) and it.get("id"):
                ids.add(str(it["id"]))
    except Exception:
        pass
    return ids


@dataclass
class L5AffirmResult:
    ok: bool
    row_id: str
    violations: tuple[str, ...] = field(default_factory=tuple)
    warnings: tuple[str, ...] = field(default_factory=tuple)
    needs_pin: bool = False
    moment_count: int = 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "row_id": self.row_id,
            "violations": list(self.violations),
            "warnings": list(self.warnings),
            "needs_pin": self.needs_pin,
            "moment_count": self.moment_count,
        }


def validate_l5_affirm(
    vault_root: Path,
    *,
    project_id: str,
    row_id: str,
    text: str | None = None,
) -> L5AffirmResult:
    """Fail-closed Pass-B L5 affirm checks for one row."""
    vault_root = vault_root.resolve()
    rid = str(row_id).strip()
    if text is None:
        l5 = scope_path(vault_root, project_id, rid, 5)
        if not l5.is_file():
            return L5AffirmResult(False, rid, ("l5_missing",))
        text = l5.read_text(encoding="utf-8", errors="replace")

    fm, body = _strip_frontmatter(text)
    violations: list[str] = []
    warnings: list[str] = []

    origin = str(fm.get("l5_origin") or "")
    if origin == "factory_draft":
        violations.append("stale_factory_draft_origin")
    elif origin != "pass_b_aligned":
        violations.append(f"l5_origin_not_pass_b_aligned:{origin or 'missing'}")

    for h in _REQUIRED_HEADINGS:
        if not _section_body(text, h):
            violations.append(f"missing_section:{h}")

    voice = validate_l5_voice(text)
    for v in voice.violations:
        if v.startswith("missing_section:"):
            continue  # new schema supersedes Complete vision / Core loop
        violations.append(f"voice:{v}")

    if _PACK_SMELL.search(body):
        violations.append("pack_content_smell")

    moments = _count_moment_bullets(text)
    min_m = thin_min_moments(vault_root, project_id, rid)
    if min_m and moments < min_m:
        violations.append(f"thin_moment_floor:{moments}<{min_m}")

    full = _section_body(text, "Full vision")
    poc = _section_body(text, "Early / PoC cut")
    if poc and full and poc.strip() == full.strip():
        violations.append("poc_identical_to_full_vision")
    if not poc:
        violations.append("missing_section:Early / PoC cut")

    anchors = _section_body(text, "Source anchors")
    scopes = user_story_paths(vault_root, project_id)["scopes_dir"]
    series_rel = f"scopes/{rid}/SERIES.md"
    series_path = scopes / rid / "SERIES.md"
    if series_path.is_file():
        if series_rel not in anchors and f"scopes/{rid}/SERIES.md" not in anchors:
            # also accept vault-relative full path fragment
            if f"{rid}/SERIES.md" not in anchors:
                violations.append("source_anchors_missing_series")
        digest_path = scopes / rid / "BATCH-DIGEST.md"
        children = list((scopes / rid).glob("children-of-*/*/WALK.md"))
        if (digest_path.is_file() or children) and "BATCH-DIGEST.md" not in anchors and children:
            # require digest path when children exist
            if "BATCH-DIGEST" not in anchors:
                violations.append("source_anchors_missing_batch_digest")

    # Hard deps: soft-warn unknown row ids
    deps_sec = _section_body(text, "Hard dependencies")
    known = _known_row_ids(vault_root, project_id)
    for m in re.finditer(r"`([a-z][a-z0-9_]*)`", deps_sec):
        dep = m.group(1)
        if dep == rid:
            continue
        if known and dep not in known and dep.startswith("ux_"):
            warnings.append(f"unknown_hard_dep:{dep}")

    needs_pin = False
    pin = str(fm.get("conceptual_pin") or "")
    pin_waived = str(fm.get("pin_waived") or "").lower() in {"true", "1", "yes"}
    if "needs pin" in pin.lower() or pin.strip() in ("", "needs_pin"):
        needs_pin = True
        if pin_waived:
            warnings.append("needs_pin_waived")
        else:
            # Pin-before-L5: unresolved placeholder without waive is hard fail
            violations.append("needs_pin_unresolved")

    # Anti-mandate when SERIES has them
    if series_path.is_file():
        from .ux_mint_walk_files import parse_walk_card

        series = parse_walk_card(series_path.read_text(encoding="utf-8"), fallback_id=rid)
        if series.get("does_not_mandate") and not _section_body(text, "does_not_mandate"):
            violations.append("missing_inherited_does_not_mandate")
        if series.get("alternatives_not_banned") and not _section_body(text, "Alternatives not banned"):
            violations.append("missing_alternatives_not_banned")

    # Dedupe while preserving order
    seen: set[str] = set()
    uniq_v: list[str] = []
    for v in violations:
        if v not in seen:
            seen.add(v)
            uniq_v.append(v)

    return L5AffirmResult(
        ok=not uniq_v,
        row_id=rid,
        violations=tuple(uniq_v),
        warnings=tuple(warnings),
        needs_pin=needs_pin,
        moment_count=moments,
    )


def render_l5_affirm_digest(
    vault_root: Path,
    *,
    project_id: str,
    row_id: str,
    affirm: L5AffirmResult | None = None,
) -> str:
    l5 = scope_path(vault_root, project_id, row_id, 5)
    text = l5.read_text(encoding="utf-8", errors="replace") if l5.is_file() else ""
    fm, _ = _strip_frontmatter(text)
    aff = affirm or validate_l5_affirm(vault_root, project_id=project_id, row_id=row_id, text=text)
    label = str(fm.get("label") or row_id)
    status = "green" if aff.ok else "red"
    if aff.ok and aff.warnings:
        status = "yellow"
    lines = [
        f"# L5-AFFIRM-DIGEST — `{row_id}`",
        "",
        f"- label: {label}",
        f"- affirm_status: {status}",
        f"- l5_origin: {fm.get('l5_origin')}",
        f"- needs_pin: {str(aff.needs_pin).lower()}",
        f"- moment_count: {aff.moment_count}",
        f"- thin_floor: {thin_min_moments(vault_root, project_id, row_id)}",
        "",
        "## Contract (What it is)",
        "",
        _section_body(text, "What it is")[:1200] or "_(missing)_",
        "",
        "## Moments",
        "",
        _section_body(text, "Moment inventory")[:2400] or "_(missing)_",
        "",
        "## PoC cut",
        "",
        _section_body(text, "Early / PoC cut")[:900] or "_(missing)_",
        "",
        "## Gate",
        "",
        f"- ok: {aff.ok}",
        f"- violations: {list(aff.violations)}",
        f"- warnings: {list(aff.warnings)}",
        "",
    ]
    return "\n".join(lines)


def emit_l5_affirm_digests(
    vault_root: Path,
    *,
    project_id: str,
    row_ids: list[str] | None = None,
) -> dict[str, Any]:
    vault_root = vault_root.resolve()
    paths = user_story_paths(vault_root, project_id)
    catalog = load_yaml(paths["catalog"])
    by_id = catalog_rows_by_id(catalog)
    ids = row_ids or [rid for rid, r in by_id.items() if r.get("planned") is True]
    if not ids:
        ids = [rid for rid, r in by_id.items() if r.get("planned") is not False]

    results: list[dict[str, Any]] = []
    for rid in ids:
        aff = validate_l5_affirm(vault_root, project_id=project_id, row_id=rid)
        digest = render_l5_affirm_digest(
            vault_root, project_id=project_id, row_id=rid, affirm=aff
        )
        dpath = paths["scopes_dir"] / rid / "L5-AFFIRM-DIGEST.md"
        dpath.parent.mkdir(parents=True, exist_ok=True)
        dpath.write_text(digest, encoding="utf-8")
        results.append({**aff.to_dict(), "digest": str(dpath.relative_to(vault_root))})

    status_path = paths["scopes_dir"].parent / "L5-AFFIRM-STATUS.md"
    status_path.write_text(
        _render_status_board(project_id, results),
        encoding="utf-8",
    )
    return {
        "ok": all(r.get("ok") for r in results) if results else False,
        "row_count": len(results),
        "status_path": str(status_path.relative_to(vault_root)),
        "results": results,
        "detail": "l5_affirm_digests_emitted",
    }


def _render_status_board(project_id: str, results: list[dict[str, Any]]) -> str:
    lines = [
        f"# L5-AFFIRM-STATUS — `{project_id}`",
        "",
        f"emitted_at: {_utc_iso()}",
        "",
        "## Per-row",
        "",
        "| row_id | status | moments | needs_pin | violations |",
        "|--------|--------|---------|-----------|------------|",
    ]
    for r in results:
        st = "green" if r.get("ok") else "red"
        if r.get("ok") and r.get("warnings"):
            st = "yellow"
        viol = ",".join(r.get("violations") or [])[:60]
        lines.append(
            f"| `{r.get('row_id')}` | {st} | {r.get('moment_count')} | "
            f"{r.get('needs_pin')} | {viol or '—'} |"
        )
    lines.extend(
        [
            "",
            "## Cross-row flags (max 3)",
            "",
            "_Operator fills after digest batch is green — before attest/sign._",
            "",
            "1. _(empty)_",
            "2. _(empty)_",
            "3. _(empty)_",
            "",
            "Suggested checks: world ≠ campaign; dual-rail seats agree; "
            "rules consumed not owned by UX row; living-world as readable residue.",
            "",
        ]
    )
    return "\n".join(lines)


def archive_l5_set_with_manifest(
    vault_root: Path,
    *,
    project_id: str,
    row_ids: list[str],
    stamp: str | None = None,
) -> dict[str, Any]:
    """Copy L5s to Versions/l5-pre-passb-align-<stamp>/ with sha256 MANIFEST."""
    vault_root = vault_root.resolve()
    paths = user_story_paths(vault_root, project_id)
    ts = stamp or datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    dest = paths["scopes_dir"].parent / "Versions" / f"l5-pre-passb-align-{ts}"
    dest.mkdir(parents=True, exist_ok=True)
    manifest: list[str] = [f"# L5 pre-passb-align archive — {project_id}", f"stamp: {ts}", ""]
    copied: list[str] = []
    for rid in row_ids:
        src = scope_path(vault_root, project_id, rid, 5)
        if not src.is_file():
            continue
        text = src.read_text(encoding="utf-8")
        digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
        out = dest / rid / "L5.md"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text, encoding="utf-8")
        rel = str(src.relative_to(vault_root))
        manifest.append(f"{digest}  {rel}")
        copied.append(rel)
    (dest / "MANIFEST.sha256").write_text("\n".join(manifest) + "\n", encoding="utf-8")
    return {
        "ok": True,
        "archive_dir": str(dest.relative_to(vault_root)),
        "copied": copied,
        "stamp": ts,
    }
