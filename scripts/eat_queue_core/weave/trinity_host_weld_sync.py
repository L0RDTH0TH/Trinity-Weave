"""Phase 13 — host_weld_sync: surgical mint/patch of host-weld/live/ from locked meta."""

from __future__ import annotations

import hashlib
import re
from datetime import date
from pathlib import Path
from typing import Any

import yaml  # type: ignore[import-untyped]

from .config import load_trinity_config
from .trinity_card_paths import load_trinity_card

HOST_WELD_DIR = Path(".technical/weave/host-weld")
MANIFEST_NAME = "manifest.yaml"
LIVE_DIR = "live"
PROPOSALS_DIR = "proposals"
REFURBISH_DRIFT_SECTION_THRESHOLD = 3


def _manifest_path(vault_root: Path) -> Path:
    return vault_root / HOST_WELD_DIR / MANIFEST_NAME


def load_host_weld_manifest(vault_root: Path) -> dict[str, Any] | None:
    """Load host-weld manifest, or None when missing/unreadable (fail-safe for self-wrap)."""
    path = _manifest_path(vault_root)
    if not path.is_file():
        return None
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, yaml.YAMLError):
        return None
    if not isinstance(data, dict):
        return None
    return data


def _norm_rel(path: str) -> str:
    p = path.replace("\\", "/").strip()
    if p.startswith("./"):
        return p[2:]
    return p


def count_production_legacy_mdc(
    vault_root: Path,
    *,
    socket_retained: list[str] | None = None,
) -> dict[str, Any]:
    """Count .mdc under .cursor/rules/ not in socket_retained."""
    vault_root = vault_root.resolve()
    retained = {_norm_rel(p) for p in (socket_retained or [])}
    rules_root = vault_root / ".cursor" / "rules"
    legacy: list[str] = []
    socket: list[str] = []
    if rules_root.is_dir():
        for path in sorted(rules_root.rglob("*.mdc")):
            rel = _norm_rel(str(path.relative_to(vault_root)))
            if rel in retained:
                socket.append(rel)
            else:
                legacy.append(rel)
    return {
        "count": len(legacy),
        "legacy_paths": legacy,
        "socket_paths": socket,
    }


def _split_frontmatter(text: str) -> tuple[str | None, str]:
    if not text.startswith("---"):
        return None, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return None, text
    return parts[1], parts[2]


def _normalize_body(text: str) -> str:
    _, body = _split_frontmatter(text)
    body = body.strip()
    body = re.sub(r"\r\n?", "\n", body)
    body = re.sub(r"[ \t]+\n", "\n", body)
    body = re.sub(r"\n{3,}", "\n\n", body)
    return body.strip().lower()


def _body_hash(text: str) -> str:
    return hashlib.sha256(_normalize_body(text).encode("utf-8")).hexdigest()[:16]


def render_safety_md_from_meta(
    card: dict[str, Any],
    *,
    trinity_ref: str,
    archive_stamp: str | None = None,
) -> str:
    """Canonical surgical digest of host_execution_safety_contract meta."""
    conceptual = card.get("conceptual") or {}
    rules = card.get("rules") or {}
    touch = card.get("touch") or {}
    summary = (conceptual.get("summary") or "").strip()
    outcome = (conceptual.get("outcome") or "").strip()
    forbidden = rules.get("forbidden") or []
    precedence = rules.get("precedence") or []
    protected = touch.get("protected_path_globs") or []
    delete_policy = touch.get("delete_policy") or "move_to_trash_only"
    primary_paths = touch.get("primary_paths") or []
    bands = touch.get("confidence_bands") or {}
    high = bands.get("high_threshold", 85)
    mid = bands.get("mid") or [68, 84]
    refs = conceptual.get("refs") or []

    trash_path = next(
        (p for p in primary_paths if "move-to-trash" in str(p)),
        "scripts/move-to-trash.sh",
    )

    lines: list[str] = [
        "---",
        "title: Host execution safety (live law)",
        f"created: {date.today().isoformat()}",
        "tags: [host-weld, safety, second-brain]",
        f'source: "[[.technical/weave/components/{trinity_ref}.yaml]]"',
        f"trinity_ref: {trinity_ref}",
        "status: active",
    ]
    if archive_stamp:
        lines.append(f"legacy_archive_stamp: {archive_stamp}")
    lines.extend(["---", "", "# Host execution safety", ""])
    lines.append(
        "Digest of locked **`host_execution_safety_contract`** meta. "
        "**Not** the same as **`maintenance_honesty_anchor`** "
        "(claim honesty vs mutation authorization)."
    )
    if outcome:
        lines.extend(["", "## Outcome", "", outcome])
    if summary:
        lines.extend(["", "## Summary", "", summary])

    lines.extend(["", "## Non-negotiable", ""])
    if protected:
        lines.append(
            "- **Protected paths** — do not autonomously move/rename/delete: "
            + ", ".join(f"`{p}`" for p in protected) + "."
        )
    lines.append(
        f"- **Delete intent** — use **`./{trash_path.lstrip('./')}`** → "
        "`.trash/<timestamp>/` + manifest. **Never** shell `rm`, `rmdir`, "
        "`find -delete`, or vault **`cp`** to mutate content."
    )
    lines.append(
        "- **Backups/snapshots append-only** — do not overwrite "
        "`Backups/Per-Change`, `Backups/Batch`, or external `BACKUP_DIR`."
    )
    if delete_policy:
        lines.append(f"- **Delete policy:** `{delete_policy}`.")

    lines.extend(["", "## Before destructive work", ""])
    lines.append(
        "Destructive = move, rename, delete, structural rewrite, "
        "large cross-note append, major overwrite."
    )
    lines.extend(
        [
            "",
            "| Gate | Rule |",
            "|------|------|",
            f"| **Confidence** | High band (default ≥{high}%) required for destructive steps. "
            f"Mid band ({mid[0]}–{mid[1]}%): **one** non-destructive refinement loop only; "
            "no destructive. Low band: proposals/wrappers only. |",
            "| **Decay** | If `post_loop_conf <= pre_loop_conf`, stop destructive; "
            "route to user decision. |",
            "| **Backup** | `obsidian_ensure_backup` / `obsidian_create_backup` before batch "
            "or stale gap; abort destructive if backup fails. |",
            "| **Snapshot** | Per-change snapshot (`.cursor/skills/obsidian-snapshot`) "
            "**before** each destructive step when in high band. |",
            "| **MCP moves** | `obsidian_ensure_structure` → `obsidian_move_note` dry_run "
            "→ snapshot → commit. |",
            "| **MCP-less hosts** | Inline file edits allowed with **same intent**; "
            "trash policy and bands still apply. |",
            "",
            "## After vault mutations",
            "",
            'Before reporting **Success** or ending the session: '
            '**`./scripts/curator_snapshot.sh "<summary>"`** when the working tree has changes. '
            "Curator failure → **`task_error`**, do not claim Success.",
            "",
            "## On gate failure",
            "",
            "Log to **`3-Resources/Errors.md`**, flag **`#review-needed`**, optional Decision "
            "Wrapper under **`Ingest/Decisions/Errors/`**. Continue batch with non-destructive "
            "work when safe.",
        ]
    )

    if precedence:
        lines.extend(["", "## Precedence (engine)", ""])
        for item in precedence:
            lines.append(f"- {item}")

    if forbidden:
        lines.extend(["", "## Forbidden (engine ids)", ""])
        for item in forbidden:
            lines.append(f"- `{item}`")

    if refs:
        lines.extend(["", "## Pointers (full detail)", ""])
        for ref in refs:
            lines.append(f"- {ref}")

    lines.append("")
    return "\n".join(lines)


def _section_titles(body: str) -> list[str]:
    return re.findall(r"^## .+$", body, flags=re.MULTILINE)


def classify_slug_surgery(
    *,
    slug: str,
    live_path: Path,
    canonical: str,
    bootstrap_all: bool,
) -> dict[str, Any]:
    if not live_path.is_file():
        return {"slug": slug, "class": "missing_slug", "live_exists": False}

    existing = live_path.read_text(encoding="utf-8", errors="replace")
    if _body_hash(existing) == _body_hash(canonical):
        return {"slug": slug, "class": "aligned", "live_exists": True}

    existing_norm = _normalize_body(existing)
    canonical_norm = _normalize_body(canonical)
    existing_sections = {s.lower() for s in _section_titles(existing_norm)}
    canonical_sections = {s.lower() for s in _section_titles(canonical_norm)}
    missing_in_existing = sorted(canonical_sections - existing_sections)
    missing_in_canonical = sorted(existing_sections - canonical_sections)
    drift_sections = sorted(existing_sections ^ canonical_sections)

    # Manual bootstrap digest missing meta sections → surgical patch, not refurbish.
    if missing_in_existing and not missing_in_canonical:
        return {
            "slug": slug,
            "class": "section_drift",
            "live_exists": True,
            "drift_sections": drift_sections,
            "additive_from_meta": True,
        }

    if len(drift_sections) >= REFURBISH_DRIFT_SECTION_THRESHOLD and not bootstrap_all:
        return {
            "slug": slug,
            "class": "refurbish_deferred",
            "live_exists": True,
            "drift_sections": drift_sections,
        }
    return {
        "slug": slug,
        "class": "section_drift",
        "live_exists": True,
        "drift_sections": drift_sections,
    }


def _merge_frontmatter_preserve_created(existing: str, canonical: str) -> str:
    existing_fm, _ = _split_frontmatter(existing)
    canonical_fm, canonical_body = _split_frontmatter(canonical)
    if not canonical_fm:
        return canonical
    if not existing_fm:
        return canonical
    created_match = re.search(r"^created:\s*.+$", existing_fm, flags=re.MULTILINE)
    if created_match:
        canonical_fm = re.sub(
            r"^created:\s*.+$",
            created_match.group(0),
            canonical_fm,
            count=1,
            flags=re.MULTILINE,
        )
    return f"---{canonical_fm}---{canonical_body}"


def _write_proposal(
    vault_root: Path,
    *,
    stamp: str,
    slug: str,
    candidate: dict[str, Any],
) -> Path:
    prop_dir = vault_root / HOST_WELD_DIR / PROPOSALS_DIR / stamp
    prop_dir.mkdir(parents=True, exist_ok=True)
    path = prop_dir / f"{slug}.md"
    body = (
        f"# Host weld refurbish proposal — `{slug}`\n\n"
        f"**Class:** `{candidate.get('class')}`\n\n"
        f"**Drift sections:** {candidate.get('drift_sections') or []}\n\n"
        "Operator: promote to `pilots/` or run explicit refurbish — not auto on full corpus.\n"
    )
    path.write_text(body, encoding="utf-8")
    return path


def run_host_weld_sync(
    vault_root: Path,
    *,
    dry_run: bool = False,
    full_corpus: bool = True,
    bootstrap_all: bool = False,
) -> dict[str, Any]:
    """Surgical sync of host-weld/live/ from locked meta (never writes .cursor/rules/)."""
    vault_root = vault_root.resolve()
    cfg = load_trinity_config(vault_root)

    if not full_corpus:
        return {"ok": True, "skipped": True, "reason": "not_full_corpus"}

    mvl_on = getattr(cfg, "mvl_conductor_enabled", True)
    sync_enabled = getattr(cfg, "host_weld_sync_enabled", mvl_on)
    if not sync_enabled:
        return {"ok": True, "skipped": True, "reason": "host_weld_sync_disabled"}

    manifest = load_host_weld_manifest(vault_root)
    if manifest is None:
        return {"ok": True, "skipped": True, "reason": "no_manifest"}
    archive_root = str(manifest.get("legacy_archive_root") or "")
    archive_stamp = str(manifest.get("legacy_archive_stamp") or "")
    socket_retained = list(manifest.get("socket_retained") or [])
    rules_map = manifest.get("rules") or {}
    if not isinstance(rules_map, dict):
        raise ValueError("manifest.rules must be a mapping")

    legacy_scan = count_production_legacy_mdc(vault_root, socket_retained=socket_retained)
    legacy_count = legacy_scan["count"]

    report: dict[str, Any] = {
        "ok": True,
        "dry_run": dry_run,
        "host_weld_manifest_stamp": archive_stamp,
        "legacy_archive_root": archive_root,
        "host_weld_production_legacy_count": legacy_count,
        "host_weld_production_legacy_paths": legacy_scan["legacy_paths"],
        "host_weld_surgery_candidates": [],
        "host_weld_surgeries_applied": [],
        "host_weld_surgeries_skipped": [],
        "host_weld_refurbish_deferred": [],
        "host_weld_proposal_pending_apply": [],
        "host_weld_aligned": [],
        "host_weld_cutover_bootstrap": legacy_count == 0 and not any(
            (vault_root / _norm_rel(str(entry.get("path") or ""))).is_file()
            for entry in rules_map.values()
            if isinstance(entry, dict)
        ),
    }

    if legacy_count > 0:
        report["ok"] = False
        report["blocked"] = True
        report["reason"] = "production_legacy_mdc_present"
        return report

    for slug, entry in rules_map.items():
        if not isinstance(entry, dict):
            continue
        status = str(entry.get("status") or "active")
        if status not in ("active", "trialing"):
            report["host_weld_surgeries_skipped"].append(
                {"slug": slug, "reason": f"status_{status}"}
            )
            continue

        rel_live = _norm_rel(str(entry.get("path") or ""))
        if not rel_live:
            continue
        live_path = vault_root / rel_live
        trinity_ref = str(entry.get("trinity_ref") or slug)

        try:
            card = load_trinity_card(vault_root, trinity_ref, prefer="locked")
        except (OSError, ValueError) as exc:
            report["ok"] = False
            report["host_weld_surgery_candidates"].append(
                {"slug": slug, "class": "error", "error": str(exc)}
            )
            continue

        if slug == "safety" or trinity_ref == "host_execution_safety_contract":
            canonical = render_safety_md_from_meta(
                card, trinity_ref=trinity_ref, archive_stamp=archive_stamp or None
            )
        else:
            report["host_weld_refurbish_deferred"].append(
                {"slug": slug, "reason": "renderer_not_implemented"}
            )
            continue

        candidate = classify_slug_surgery(
            slug=slug,
            live_path=live_path,
            canonical=canonical,
            bootstrap_all=bootstrap_all,
        )
        report["host_weld_surgery_candidates"].append(candidate)
        surgery_class = candidate["class"]

        if surgery_class == "aligned":
            report["host_weld_aligned"].append(slug)
            report["host_weld_surgeries_skipped"].append(
                {"slug": slug, "reason": "aligned"}
            )
            continue

        if surgery_class == "refurbish_deferred":
            report["host_weld_refurbish_deferred"].append(candidate)
            if not dry_run:
                prop_path = _write_proposal(
                    vault_root, stamp=archive_stamp or "deferred", slug=slug, candidate=candidate
                )
                report["host_weld_proposal_pending_apply"].append(str(prop_path))
            continue

        if dry_run:
            report["host_weld_surgeries_applied"].append(
                {"slug": slug, "class": surgery_class, "dry_run": True}
            )
            continue

        live_path.parent.mkdir(parents=True, exist_ok=True)
        if surgery_class == "missing_slug":
            live_path.write_text(canonical, encoding="utf-8")
        elif surgery_class == "section_drift" and live_path.is_file():
            merged = _merge_frontmatter_preserve_created(
                live_path.read_text(encoding="utf-8", errors="replace"),
                canonical,
            )
            live_path.write_text(merged, encoding="utf-8")
        else:
            live_path.write_text(canonical, encoding="utf-8")

        report["host_weld_surgeries_applied"].append(
            {"slug": slug, "class": surgery_class, "path": rel_live}
        )

    report["host_weld_aligned"] = sorted(set(report["host_weld_aligned"]))
    if report["host_weld_refurbish_deferred"] and not dry_run:
        report["ok"] = False
        report["reason"] = "refurbish_deferred_pending"

    return report
