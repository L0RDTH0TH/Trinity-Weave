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


def draft_l5_user_story(
    vault_root: Path,
    *,
    project_id: str,
    row_id: str,
    overwrite_placeholder: bool = True,
) -> dict[str, Any]:
    """
    Factory L5 draft — substantive mutatable user story from PMG + roadmap context.

    Not empty form fields: a first-pass experiential definition the operator edits until
    parity with their actual goal.
    """
    vault_root = vault_root.resolve()
    l5_path = scope_path(vault_root, project_id, row_id, 5)
    if l5_path.is_file():
        existing = l5_path.read_text(encoding="utf-8", errors="replace")
        if not overwrite_placeholder or not _is_placeholder_l5(existing):
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

    label = str(row.get("label") or row_id)
    pmg = _find_pmg_path(vault_root, project_id)
    pmg_text = pmg.read_text(encoding="utf-8", errors="replace") if pmg and pmg.is_file() else ""

    phase_num = _phase_num_from_row_id(row_id)
    pmg_title, pmg_summary, pmg_bullets = ("", "", [])
    phase_roadmap_excerpt = ""
    conceptual_excerpts: list[str] = []
    if phase_num:
        pmg_title, pmg_summary, pmg_bullets = extract_pmg_phase_section(pmg_text, phase_num)
        phase_path = find_phase_roadmap_path(vault_root, project_id, phase_num)
        if phase_path and phase_path.is_file():
            phase_roadmap_excerpt = phase_path.read_text(encoding="utf-8", errors="replace")[:2000].strip()
        for cpath, cbody in find_conceptual_context_for_phase(vault_root, project_id, phase_num):
            rel = cpath.relative_to(vault_root)
            conceptual_excerpts.append(f"### [[{rel}]]\n\n{cbody[:1600]}")

    pin_excerpt = _read_pin_excerpt(vault_root, row)
    vision_parts = [
        p
        for p in [
            pmg_summary,
            "\n\n".join(conceptual_excerpts[:3]) if conceptual_excerpts else "",
            pin_excerpt[:800] if pin_excerpt and pin_excerpt not in pmg_summary else "",
        ]
        if p
    ]
    complete_vision = vision_parts[0] if vision_parts else (
        f"At ship tier, **{label}** delivers the experiential bar described in the project master goal "
        f"for catalog row `{row_id}`."
    )

    core_loop = _infer_core_loop(label, pmg_summary, pmg_bullets)
    integration = (
        f"At ship tier, **{label}** integrates with adjacent phases through explicit modularity seams, "
        f"canon/intent hooks where applicable, and factory-verifiable contracts — not one-off UI glue. "
    )
    if pmg_bullets:
        integration += f"Key integration anchors: {'; '.join(pmg_bullets[:3])}."
    scaffold = _infer_scaffold_minimum(label, pmg_summary, pmg_bullets)

    anchors: list[str] = []
    if pmg:
        anchors.append(f"- PMG: `[[{pmg.relative_to(vault_root)}]]`")
    if phase_num and (phase_roadmap_excerpt or conceptual_excerpts):
        pr = find_phase_roadmap_path(vault_root, project_id, phase_num)
        if pr:
            anchors.append(f"- Phase roadmap: `[[{pr.relative_to(vault_root)}]]`")
        for cpath, _ in find_conceptual_context_for_phase(vault_root, project_id, phase_num)[:4]:
            anchors.append(f"- Conceptual: `[[{cpath.relative_to(vault_root)}]]`")

    body = (
        f"---\n"
        f"level: 5\n"
        f"row_id: {row_id}\n"
        f"label: {label}\n"
        f"l5_origin: factory_draft\n"
        f"operator_action: mutate_until_parity\n"
        f"---\n\n"
        f"# {label} — complete vision (L5)\n\n"
        f"> [!note] Factory draft — mutate until parity\n"
        f"> This is the factory's read of your goal from PMG + roadmap context. "
        f"Edit until it matches what you actually want at ship tier.\n\n"
        f"## Complete vision\n\n{complete_vision}\n\n"
        f"## Core loop\n\n{core_loop}\n\n"
        f"## Integration & polish\n\n{integration}\n\n"
        f"## Scaffold minimum\n\n{scaffold}\n\n"
    )
    if anchors:
        body += "## Source anchors\n\n" + "\n".join(anchors) + "\n\n"
    body += "<!-- factory-l5-draft: v1 -->\n<!-- operator-mutate-until-parity -->\n"

    l5_path.parent.mkdir(parents=True, exist_ok=True)
    l5_path.write_text(body, encoding="utf-8")
    return {
        "ok": True,
        "row_id": row_id,
        "path": str(l5_path.relative_to(vault_root)),
        "detail": "l5_factory_drafted",
        "chars": len(body),
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
