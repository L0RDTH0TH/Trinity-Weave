"""Loop 2 operator surface — budget, substantive L5 drafts, L4..L1 slice."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from .catalog_io import catalog_rows_by_id, load_yaml, normalize_pin, user_story_paths
from .catalog_mint_propose import _find_pmg_path
from .depth_scope import scope_path, slice_l5_to_levels
from .rollout_slicer import run_rollout_slicer
from .user_story_feedback import sync_feedback_from_budget

_PLACEHOLDER_MARKERS = (
    "Flesh out what **complete** looks like",
    "(What the player experiences at full depth.)",
    "(Cross-system behavior at ship tier.)",
    "(Smallest honest vertical slice",
)


def _phase_num_from_row_id(row_id: str) -> str | None:
    m = re.match(r"phase_(\d+(?:_\d+)*)", row_id)
    return m.group(1).replace("_", ".") if m else None


def is_placeholder_l5(text: str) -> bool:
    """True when L5 is empty scaffold, not a factory substantive draft."""
    body = text.strip()
    if len(body) < 200:
        return True
    return any(marker in body for marker in _PLACEHOLDER_MARKERS)


def _is_placeholder_l5(text: str) -> bool:
    return is_placeholder_l5(text)


def extract_pmg_phase_section(pmg_text: str, phase_num: str) -> tuple[str, str, list[str]]:
    """Return (title, summary_paragraph, bullets) for Phase N from PMG body."""
    num_esc = re.escape(phase_num.split(".")[0])
    header_re = re.compile(
        rf"^#{{2,3}}\s+Phase\s+{num_esc}(?:\s*[-–—:\-]\s*(.+))?$",
        re.MULTILINE | re.IGNORECASE,
    )
    matches = list(header_re.finditer(pmg_text))
    if not matches:
        return f"Phase {phase_num}", "", []

    m = matches[0]
    title = m.group(1).strip() if m.group(1) else f"Phase {phase_num}"
    start = m.end()
    next_m = re.search(
        rf"^#{{2,3}}\s+Phase\s+\d",
        pmg_text[start:],
        re.MULTILINE | re.IGNORECASE,
    )
    end = start + next_m.start() if next_m else len(pmg_text)
    block = pmg_text[start:end]

    paragraph_parts: list[str] = []
    bullets: list[str] = []
    for line in block.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.startswith("- ") or stripped.startswith("* "):
            bullets.append(stripped[2:].strip())
            continue
        if stripped.startswith("|"):
            continue
        paragraph_parts.append(stripped)

    summary = " ".join(paragraph_parts).strip()
    return title, summary, bullets


def find_conceptual_context_for_phase(
    vault_root: Path,
    project_id: str,
    phase_num: str,
) -> list[tuple[Path, str]]:
    """Secondary+ conceptual notes under a phase — richest first for L5 drafting."""
    try:
        num = int(str(phase_num).split(".")[0])
    except ValueError:
        return []
    from .conceptual_track_ready import conceptual_notes_for_phase, _roadmap_level

    chunks: list[tuple[int, Path, str]] = []
    for path, fm, body in conceptual_notes_for_phase(vault_root, project_id, num):
        if not body.strip():
            continue
        level = _roadmap_level(fm, path)
        depth_rank = {"primary": 0, "secondary": 2, "tertiary": 3, "quaternary": 4}.get(level, 1)
        chunks.append((depth_rank, path, body[:2400]))
    chunks.sort(key=lambda x: (-x[0], str(x[1])))
    return [(p, b) for _, p, b in chunks]


def find_phase_roadmap_path(vault_root: Path, project_id: str, phase_num: str) -> Path | None:
    vault_root = vault_root.resolve()
    road = vault_root / "1-Projects" / project_id / "Roadmap"
    if not road.is_dir():
        return None
    prefix = f"Phase-{phase_num.split('.')[0]}-"
    for d in sorted(road.iterdir()):
        if not d.is_dir() or not d.name.startswith(prefix):
            continue
        candidates = sorted(d.glob("*Roadmap*.md"), key=lambda p: p.stat().st_mtime, reverse=True)
        if candidates:
            return candidates[0]
    return None


def _read_pin_excerpt(vault_root: Path, row: dict[str, Any], max_chars: int = 2400) -> str:
    chunks: list[str] = []
    for key in ("conceptual_pin", "execution_pins"):
        val = row.get(key)
        pins = val if isinstance(val, list) else ([val] if val else [])
        for pin in pins:
            if not pin:
                continue
            rel = normalize_pin(str(pin))
            path = vault_root / rel
            if not path.is_file() and not rel.endswith(".md"):
                path = vault_root / f"{rel}.md"
            if path.is_file():
                text = path.read_text(encoding="utf-8", errors="replace")
                chunks.append(text[:max_chars].strip())
    return "\n\n---\n\n".join(chunks)[:max_chars]


def _infer_core_loop(label: str, summary: str, bullets: list[str]) -> str:
    if bullets:
        lines = [f"- {b}" for b in bullets[:6]]
        return (
            f"When **{label}** is complete, the player-visible loop includes:\n\n"
            + "\n".join(lines)
        )
    return (
        f"When **{label}** is complete, the player can move through the core loop implied by the "
        f"phase goal: {summary[:400] or 'see complete vision'}."
    )


def _infer_scaffold_minimum(label: str, summary: str, bullets: list[str]) -> str:
    seed = bullets[0] if bullets else summary[:280]
    return (
        f"Smallest honest vertical slice for **{label}**: one end-to-end path that proves the "
        f"phase thesis without L4+ polish — {seed}"
    )


def _load_series_and_children(
    vault_root: Path,
    project_id: str,
    row_id: str,
) -> tuple[dict[str, Any] | None, list[dict[str, Any]], Path | None, Path | None]:
    """Return (series_item, child_items, series_path, digest_path)."""
    from .ux_mint_walk_files import parse_walk_card

    scopes = user_story_paths(vault_root, project_id)["scopes_dir"]
    series_path = scopes / row_id / "SERIES.md"
    digest_path = scopes / row_id / "BATCH-DIGEST.md"
    series: dict[str, Any] | None = None
    if series_path.is_file():
        series = parse_walk_card(
            series_path.read_text(encoding="utf-8", errors="replace"),
            fallback_id=row_id,
        )
    children: list[dict[str, Any]] = []
    for walk in sorted((scopes / row_id).glob("children-of-*/*/WALK.md")):
        children.append(
            parse_walk_card(
                walk.read_text(encoding="utf-8", errors="replace"),
                fallback_id=walk.parent.name,
            )
        )
    return (
        series,
        children,
        series_path if series_path.is_file() else None,
        digest_path if digest_path.is_file() else None,
    )


def _moment_bullets_from_feedstock(
    *,
    label: str,
    series: dict[str, Any] | None,
    children: list[dict[str, Any]],
    min_moments: int,
) -> list[str]:
    """Build seat/trigger/response/refusal/residue bullets from Pass B feedstock."""
    seats = []
    if series and isinstance(series.get("seat"), list):
        seats = [str(s) for s in series["seat"]]
    seat = ", ".join(seats) if seats else "shared_table"
    bullets: list[str] = []

    for ch in children:
        cid = str(ch.get("id") or "child")
        summary = str(ch.get("summary") or ch.get("label") or cid).strip()
        bullets.append(
            f"- **Seat:** {seat} · **Trigger:** enter `{cid}` · "
            f"**Observable response:** {summary[:220]} · "
            f"**Refusal/guard:** out of contract / wrong seat · "
            f"**Residue:** lasting readable state from this moment"
        )

    summary = str((series or {}).get("summary") or label)
    # Split summary into clause-sized moments when children are thin
    clauses = [c.strip() for c in re.split(r"[.;]", summary) if len(c.strip()) > 24]
    for i, clause in enumerate(clauses):
        if len(bullets) >= max(min_moments, 6):
            break
        bullets.append(
            f"- **Seat:** {seat} · **Trigger:** contract clause {i + 1} · "
            f"**Observable response:** {clause[:220]} · "
            f"**Refusal/guard:** anti-mandate / wrong altitude · "
            f"**Residue:** durable table-visible consequence when applicable"
        )

    # Thin expansion from alternatives (play-verb coverage, not chrome)
    alts = (series or {}).get("alternatives_not_banned") or []
    if isinstance(alts, list):
        for alt in alts:
            if len(bullets) >= min_moments:
                break
            bullets.append(
                f"- **Seat:** {seat} · **Trigger:** structure-menu choice · "
                f"**Observable response:** {str(alt)[:200]} remains first-class · "
                f"**Refusal/guard:** must not mandate the opposite as sole law · "
                f"**Residue:** chosen path leaves readable stakes/cost when relevant"
            )

    while len(bullets) < min_moments:
        n = len(bullets) + 1
        bullets.append(
            f"- **Seat:** {seat} · **Trigger:** open play-verb moment {n} for **{label}** · "
            f"**Observable response:** player/DM-visible contract step (expand from SERIES) · "
            f"**Refusal/guard:** out of scope / deferred exclusion · "
            f"**Residue:** lasting cost or handoff back to prior surface"
        )
    return bullets


def _format_list_block(values: Any, *, empty: str) -> str:
    if isinstance(values, list) and values:
        return "\n".join(f"- {v}" for v in values)
    if isinstance(values, str) and values.strip():
        return values.strip()
    return empty


def draft_l5_user_story(
    vault_root: Path,
    *,
    project_id: str,
    row_id: str,
    overwrite_placeholder: bool = True,
    force_overwrite: bool = False,
) -> dict[str, Any]:
    """
    Pass-B-aligned L5 draft (first-class Loop 2 MO).

    Primary feedstock: SERIES + BATCH-DIGEST + child WALK summaries.
    PMG only for hard-dep / integration seams — never primary vision prose.
    """
    from datetime import datetime, timezone

    from .l5_thin_config import thin_min_moments

    vault_root = vault_root.resolve()
    l5_path = scope_path(vault_root, project_id, row_id, 5)
    if l5_path.is_file() and not force_overwrite:
        existing = l5_path.read_text(encoding="utf-8", errors="replace")
        if not overwrite_placeholder or not _is_placeholder_l5(existing):
            # Allow refresh when still factory_draft under overwrite_placeholder
            if "l5_origin: pass_b_aligned" in existing or not overwrite_placeholder:
                return {
                    "ok": True,
                    "row_id": row_id,
                    "path": str(l5_path.relative_to(vault_root)),
                    "detail": "l5_exists",
                    "skipped": True,
                }
            if "l5_origin: factory_draft" not in existing and not _is_placeholder_l5(existing):
                return {
                    "ok": True,
                    "row_id": row_id,
                    "path": str(l5_path.relative_to(vault_root)),
                    "detail": "l5_exists",
                    "skipped": True,
                }

    paths = user_story_paths(vault_root, project_id)
    catalog = load_yaml(paths["catalog"])
    row = catalog_rows_by_id(catalog).get(row_id) or {}
    if not row:
        return {"ok": False, "row_id": row_id, "detail": "catalog_row_missing"}

    series, children, series_path, digest_path = _load_series_and_children(
        vault_root, project_id, row_id
    )
    label = str(
        (series or {}).get("label") or row.get("label") or row_id
    )
    summary = str((series or {}).get("summary") or row.get("label") or label)
    pin_raw = str(
        (series or {}).get("conceptual_pin")
        or row.get("conceptual_pin")
        or "needs pin"
    )
    needs_pin = "needs pin" in pin_raw.lower() or pin_raw.strip() in ("", "needs_pin")

    min_m = thin_min_moments(vault_root, project_id, row_id)
    # Non-thin still get at least 2 moments from feedstock
    moment_floor = max(min_m, 2 if (series or children) else 1)
    moments = _moment_bullets_from_feedstock(
        label=label,
        series=series,
        children=children,
        min_moments=moment_floor,
    )

    full_vision_lines = [summary]
    if children:
        full_vision_lines.append("")
        full_vision_lines.append("Child surfaces under this contract:")
        for ch in children[:12]:
            full_vision_lines.append(
                f"- `{ch.get('id')}` — {str(ch.get('summary') or ch.get('label') or '')[:160]}"
            )

    # PoC cut: omit later children / polish; keep first honest verbs
    child_ids = [str(c.get("id")) for c in children]
    if len(child_ids) > 2:
        poc = (
            f"First cut proves the parent contract with a small surface set "
            f"({', '.join(f'`{c}`' for c in child_ids[:2])}); defer "
            f"{', '.join(f'`{c}`' for c in child_ids[2:6])} and deeper chrome. "
            f"Keep anti-mandate and authored structure menus honest."
        )
    elif min_m:
        poc = (
            f"PoC names the play-verb moments in Moment inventory (intent / resolve / "
            f"residue) with thin chrome; defer pack-content depth, multi-wave tooling, "
            f"and non-essential polish. Full vision remains larger than this cut."
        )
    else:
        poc = (
            f"PoC delivers the series contract for **{label}** with one honest path and "
            f"explicit deferred exclusions; omit L4+ polish and optional thickeners."
        )

    deps = row.get("depends_on") if isinstance(row.get("depends_on"), list) else []
    dep_ids = []
    for d in deps:
        if isinstance(d, dict) and d.get("row_id"):
            dep_ids.append(str(d["row_id"]))
        elif isinstance(d, str):
            dep_ids.append(d)
    # Soft PMG seam only for hard-deps language
    pmg = _find_pmg_path(vault_root, project_id)
    hard_deps = (
        "\n".join(f"- `{d}`" for d in dep_ids)
        if dep_ids
        else (
            f"- Collaborative table / adjacent rails as named in SERIES hard seams "
            f"(see PMG only for integration names: "
            f"`{pmg.relative_to(vault_root) if pmg else 'PMG'}`)."
        )
    )

    dnm = _format_list_block(
        (series or {}).get("does_not_mandate"),
        empty="- _(none recorded on SERIES — add if product law risks appear)_",
    )
    alts = _format_list_block(
        (series or {}).get("alternatives_not_banned"),
        empty="- _(none recorded on SERIES)_",
    )

    anchors: list[str] = []
    if series_path:
        anchors.append(f"- SERIES: `scopes/{row_id}/SERIES.md`")
    if digest_path or children:
        anchors.append(f"- BATCH-DIGEST: `scopes/{row_id}/BATCH-DIGEST.md`")
    for ch in children[:8]:
        cid = ch.get("id")
        anchors.append(
            f"- WALK: `scopes/{row_id}/children-of-{row_id}/{cid}/WALK.md`"
        )
    if not needs_pin and pin_raw:
        anchors.append(f"- Conceptual pin: `{pin_raw}`")
    else:
        anchors.append("- Conceptual pin: `needs pin` (soft — resolve before catalog sign)")
    if pmg:
        anchors.append(f"- PMG seam only: `[[{pmg.relative_to(vault_root)}]]`")

    scaffold = (
        f"Smallest honest vertical slice for **{label}**: one end-to-end path that proves "
        f"the series contract without L4+ polish — "
        f"{(moments[0][2:80] if moments else summary[:120])}."
    )

    now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    body = (
        f"---\n"
        f"level: 5\n"
        f"row_id: {row_id}\n"
        f"label: {label}\n"
        f"l5_origin: pass_b_aligned\n"
        f"pass_b_aligned_at: {now}\n"
        f"affirm_status: drafted\n"
        f"conceptual_pin: {pin_raw}\n"
        f"operator_action: mutate_until_parity\n"
        f"---\n\n"
        f"# {label} — complete vision (L5)\n\n"
        f"> [!note] Pass-B-aligned Loop 2 MO\n"
        f"> Primary feedstock is locked SERIES / BATCH-DIGEST / WALK — not PMG mine. "
        f"Edit until parity; Grok validates via digest-first affirm.\n\n"
        f"## What it is\n\n{summary}\n\n"
        f"## Moment inventory\n\n" + "\n".join(moments) + "\n\n"
        f"## Full vision\n\n" + "\n".join(full_vision_lines) + "\n\n"
        f"## Early / PoC cut\n\n{poc}\n\n"
        f"## Hard dependencies\n\n{hard_deps}\n\n"
        f"## Out of scope\n\n"
        f"- Pack content dumps (class/spell/monster/merchant lists) — rules/content packs own those\n"
        f"- Mandating a single AP skin as product law\n"
        f"- Deferred exclusions for first slice: anything not named in Moment inventory / PoC cut\n\n"
        f"## Alternatives not banned\n\n{alts}\n\n"
        f"## does_not_mandate\n\n{dnm}\n\n"
        f"## Source anchors\n\n" + "\n".join(anchors) + "\n\n"
        f"## Scaffold minimum\n\n{scaffold}\n\n"
        f"<!-- pass-b-l5-draft: v1 -->\n"
    )

    l5_path.parent.mkdir(parents=True, exist_ok=True)
    l5_path.write_text(body, encoding="utf-8")
    return {
        "ok": True,
        "row_id": row_id,
        "path": str(l5_path.relative_to(vault_root)),
        "detail": "l5_pass_b_drafted",
        "chars": len(body),
        "needs_pin": needs_pin,
        "moment_count": len(moments),
    }


def _default_target_depth(vault_root: Path) -> int:
    try:
        from ...merged_config import load_merged_yaml_blocks

        blocks = load_merged_yaml_blocks(vault_root)
        rf = blocks.get("roadmap_factory")
        if isinstance(rf, dict):
            rollout = rf.get("default_rollout")
            if isinstance(rollout, list) and rollout:
                first = rollout[0]
                if isinstance(first, dict) and first.get("target_depth"):
                    return int(first["target_depth"])
            if rf.get("default_target_depth") is not None:
                return int(rf["default_target_depth"])
    except (ImportError, OSError, TypeError, ValueError):
        pass
    return 2


def bootstrap_default_budget(
    vault_root: Path,
    *,
    project_id: str,
    row_ids: list[str],
    target_depth: int | None = None,
) -> dict[str, Any]:
    paths = user_story_paths(vault_root, project_id)
    from .catalog_io import load_json

    existing = load_json(paths["budget"])
    if existing.get("rows"):
        return {
            "ok": True,
            "detail": "budget_exists",
            "path": str(paths["budget"].relative_to(vault_root)),
        }
    td = target_depth if target_depth is not None else _default_target_depth(vault_root)
    assignments = [{"row_id": rid, "target_depth": td} for rid in row_ids]
    out = run_rollout_slicer(
        vault_root,
        project_id=project_id,
        row_assignments=assignments,
        generate_beats=False,
    )
    return {**out.to_dict(), "detail": "budget_bootstrapped"}


def prepare_loop2_operator_surface(
    vault_root: Path,
    *,
    project_id: str,
    target_depth: int | None = None,
    slice_derived: bool = False,
) -> dict[str, Any]:
    """
    After catalog_mint: budget + substantive L5 drafts; L4..L1 only when slice_derived=True.

    Operator loop 2 then blocks for read/attest/sign — depth slicer runs after sign-off.
    """
    vault_root = vault_root.resolve()
    paths = user_story_paths(vault_root, project_id)
    catalog = load_yaml(paths["catalog"])
    by_id = catalog_rows_by_id(catalog)
    row_ids = [rid for rid, r in by_id.items() if r.get("planned") is not False]
    if not row_ids:
        row_ids = list(by_id.keys())

    budget = bootstrap_default_budget(
        vault_root, project_id=project_id, row_ids=row_ids, target_depth=target_depth
    )
    l5_results = [
        draft_l5_user_story(vault_root, project_id=project_id, row_id=rid)
        for rid in row_ids
    ]
    slice_out: dict[str, Any] = {"skipped": True}
    if slice_derived and row_ids:
        results = [
            slice_l5_to_levels(vault_root, project_id=project_id, row_id=rid, bootstrap=False)
            for rid in row_ids
        ]
        slice_out = {
            "ok": all(r.get("ok") for r in results),
            "row_count": len(results),
            "results": results,
        }

    feedback_rows = sync_feedback_from_budget(vault_root, project_id)

    return {
        "ok": bool(row_ids) and all(r.get("ok") for r in l5_results),
        "row_ids": row_ids,
        "budget": budget,
        "l5_drafts": l5_results,
        "depth_slice": slice_out,
        "feedback_rows_synced": len(feedback_rows),
        "detail": "loop2_operator_surface_prepared",
    }
