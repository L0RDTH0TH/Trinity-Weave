"""UX mint backlog — post-freeze ordered experience nouns for Grok to walk.

Deterministic harvest + axis coverage gate. Does not write slice-catalog rows.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

from .catalog_io import catalog_rows_by_id, load_yaml, save_yaml, user_story_paths
from .ux_mint_walk_files import (
    children_of_dirname,
    load_items_from_walk_files,
    split_backlog_doc_to_walk_dirs,
    sync_all_walk_files,
    sync_batch_digests,
    walk_tree_present,
)

REQUIRED_UX_AXES = (
    "perspective_overrides",
    "agency",
    "dm_player_rails",
    "class_chrome",
    "combat_cast_feedback",
    "session0_identity_art",
)

# Shells are allowed as one supporting axis — never the whole backlog alone.
SUPPORTING_AXES = ("presentation_shells",)

AXIS_ORDER = REQUIRED_UX_AXES + SUPPORTING_AXES

EXPERIENTIAL_HINTS = (
    "feel",
    "flow",
    "presentation",
    "chrome",
    "feedback",
    "player",
    "dm",
    "agency",
    "perspective",
    "scry",
    "clairvoyance",
    "art",
    "identity",
    "session",
    "cast",
    "rail",
)

# Patterns that look like phase/backend scaffolding — reject as backlog ids/labels.
_PHASE_ID_RE = re.compile(r"^phase_[\d_]+$", re.IGNORECASE)
_PHASE_LABEL_RE = re.compile(r"^phase\s+[\d.]+", re.IGNORECASE)
_BACKENDISH = re.compile(
    r"\b(damage\s+formula|rules?\s+resolution|stack\s+domain|factory\s+chore|"
    r"data\s+structur|sim(?:ulation)?\s+only|backend\s+only)\b",
    re.IGNORECASE,
)

# Keyword → (ux_axis, dimension, id_stub, label, summary)
_THEME_SEEDS: tuple[tuple[re.Pattern[str], str, str, str, str, str], ...] = (
    (
        re.compile(r"\b(scry|clairvoyance|perspective\s+override|fp\b|first[\s-]?person)\b", re.I),
        "perspective_overrides",
        "ui_surface",
        "ux_scry_presentation",
        "Scry / Clairvoyance presentation",
        "How perspective overrides feel and present to the player (not the sim alone).",
    ),
    (
        re.compile(r"\b(agency|player\s+choice|intent\s+loop|decision\s+loop)\b", re.I),
        "agency",
        "player_rail",
        "ux_player_agency_loop",
        "Player agency loop",
        "Frictionless moments where the player feels authorship over outcomes.",
    ),
    (
        re.compile(r"\b(dm\s+rail|player\s+rail|collaboration|session\s+flow)\b", re.I),
        "dm_player_rails",
        "dm_rail",
        "ux_dm_player_rails",
        "DM / player rails",
        "How DM and player flows share chrome without fighting each other.",
    ),
    (
        re.compile(r"\b(class|subclass|archetype)\b.{0,40}\b(chrome|ui|presentation|identity)\b|"
                   r"\b(chrome|class\s+identity)\b", re.I),
        "class_chrome",
        "ui_surface",
        "ux_class_chrome",
        "Class / subclass chrome",
        "Visible class identity polish — not class feature math.",
    ),
    (
        re.compile(r"\b(class|subclass|fighter|wizard|rogue|cleric|bard)\b", re.I),
        "class_chrome",
        "ui_surface",
        "ux_class_chrome",
        "Class / subclass chrome",
        "Visible class identity polish — not class feature math.",
    ),
    (
        re.compile(
            r"\b(booming\s*blade|cast\s+feedback|combat\s+feedback|vfx|hit\s+feel|"
            r"spell\s+feedback|attack\s+feedback)\b",
            re.I,
        ),
        "combat_cast_feedback",
        "ui_surface",
        "ux_combat_cast_feedback",
        "Combat / cast feedback",
        "Sensory cast and hit feedback the player/DM notice in the moment.",
    ),
    (
        re.compile(r"\b(session\s*0|art\s+direction|palette|identity\s+art|character\s+creation)\b", re.I),
        "session0_identity_art",
        "session_bootstrap",
        "ux_session0_identity_art",
        "Session 0 / identity art",
        "Bootstrap rituals and art direction that set identity tone.",
    ),
    (
        re.compile(r"\b(presentation\s+shell|ui_presentation_shell|factory\s+phase\s+0)\b", re.I),
        "presentation_shells",
        "ui_surface",
        "ux_presentation_shell",
        "Presentation shell",
        "Baseline shell that hosts experience surfaces (supporting axis only).",
    ),
)

_HEADING_RE = re.compile(r"^#{2,4}\s+(.+)$", re.MULTILINE)
# Moment-card experience nouns: "- label: …\n  summary: …"
_NOUN_CANDIDATE_RE = re.compile(
    r"(?m)^-\s*label:\s*(.+?)\s*$\n[ \t]*summary:\s*(.+?)\s*$",
)


MINT_PHASES = (
    "series_draft",
    "series_walk",
    "series_locked",
    "hub_children",
    "children_greenlit",
    "children_batch",
    "post_mint",
)

HARVEST_PASSES = frozenset({"series", "children", "full"})

DOC_PHASE_KEYS = (
    "mint_phase",
    "series_draft_accepted",
    "waive_series_draft",
    "series_published_trinity_ref",
    "children_published_trinity_ref",
    "children_greenlit",
    "children_rewritten",
    "archive_ref",
    "harvest_pass",
)

ITEM_LANE_KEYS = (
    "mint_lane",
    "parent_id",
    "depth_band",
    "fanout",
    "depends_on",
    "historical_id",
)


@dataclass(frozen=True)
class UxMintBacklogResult:
    ok: bool
    path: str
    backlog_status: str
    item_count: int
    pending_count: int
    next_pending_id: str | None
    missing_axes: tuple[str, ...]
    coverage_ok: bool
    detail: str
    proposed_ids: tuple[str, ...]
    mint_phase: str = "series_draft"
    harvest_pass: str = "series"

    def to_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "path": self.path,
            "backlog_status": self.backlog_status,
            "item_count": self.item_count,
            "pending_count": self.pending_count,
            "next_pending_id": self.next_pending_id,
            "missing_axes": list(self.missing_axes),
            "coverage_ok": self.coverage_ok,
            "detail": self.detail,
            "proposed_ids": list(self.proposed_ids),
            "mint_phase": self.mint_phase,
            "harvest_pass": self.harvest_pass,
        }


def backlog_path(vault_root: Path, project_id: str) -> Path:
    return user_story_paths(vault_root, project_id)["catalog"].parent / "MINT-BACKLOG.yaml"


def backlog_md_path(vault_root: Path, project_id: str) -> Path:
    """Obsidian prune / critique surface — operator edits this; YAML is machine mirror."""
    return user_story_paths(vault_root, project_id)["catalog"].parent / "MINT-BACKLOG.md"


_ITEM_HEADER_RE = re.compile(
    r"^###\s+`([^`]+)`\s*(?:—|--|-)?\s*(.*)$",
    re.MULTILINE,
)
# Do not use \s* after the colon — it eats newlines and merges the next `- key:` line
# into an empty value (e.g. `- series_id: \n- series_order:` → series_id="- series_order:").
_ITEM_FIELD_RE = re.compile(r"^- (\w+):[ \t]*(.*)$", re.MULTILINE)


def _utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _yaml_list_fm(values: list[str]) -> str:
    if not values:
        return "[]"
    return "[" + ", ".join(str(v) for v in values) + "]"


# Doc-level machine gates — never drop when MD is newer but FM incomplete.
_DOC_GATE_KEYS = (
    "series_published_trinity_ref",
    "children_published_trinity_ref",
    "locked_child_batches",
    "active_child_batch",
    "next_child_batch",
    "children_greenlit",
    "children_rewritten",
    "mint_phase",
    "harvest_pass",
    "series_draft_accepted",
    "waive_series_draft",
    "archive_ref",
    "quality_validation",
    "quality_validation_status",
    "frozen_at",
    "backlog_status",
)


def _gate_empty(val: Any) -> bool:
    if val is None:
        return True
    if isinstance(val, bool):
        return False
    if isinstance(val, (list, dict)):
        return len(val) == 0
    return str(val).strip() == ""


def _merge_yaml_doc_gates(md_doc: dict[str, Any], y_doc: dict[str, Any]) -> dict[str, Any]:
    """Keep operator item edits from MD; fill missing doc gates from YAML."""
    out = dict(md_doc)
    for key in _DOC_GATE_KEYS:
        if key not in y_doc:
            continue
        # Explicit empty locked list on MD is intentional (unlock) — do not revive from YAML
        if key == "locked_child_batches" and "locked_child_batches" in md_doc:
            continue
        if _gate_empty(out.get(key)) and not _gate_empty(y_doc.get(key)):
            out[key] = y_doc[key]
    return out


def _items_by_series_parent(
    items: list[dict[str, Any]],
) -> list[tuple[dict[str, Any] | None, list[dict[str, Any]]]]:
    """Group non-series children under their series parent (paternity order)."""
    series: list[dict[str, Any]] = []
    children: list[dict[str, Any]] = []
    for it in items:
        if str(it.get("walk_tier") or "") == "series":
            series.append(it)
        else:
            children.append(it)

    def _series_key(it: dict[str, Any]) -> tuple[int, str]:
        try:
            rank = int(it.get("series_walk_rank") or 999)
        except (TypeError, ValueError):
            rank = 999
        return (rank, str(it.get("id") or ""))

    series_sorted = sorted(series, key=_series_key)
    series_ids = {str(s.get("id") or "") for s in series_sorted}
    by_parent: dict[str, list[dict[str, Any]]] = {sid: [] for sid in series_ids}
    orphans: list[dict[str, Any]] = []
    for ch in children:
        pid = str(ch.get("parent_id") or "").strip()
        if pid and pid in by_parent:
            by_parent[pid].append(ch)
        else:
            orphans.append(ch)

    def _child_key(it: dict[str, Any]) -> str:
        return str(it.get("id") or "")

    out: list[tuple[dict[str, Any] | None, list[dict[str, Any]]]] = []
    for parent in series_sorted:
        pid = str(parent.get("id") or "")
        kids = sorted(by_parent.get(pid, []), key=_child_key)
        out.append((parent, kids))
    if orphans:
        out.append((None, sorted(orphans, key=_child_key)))
    return out


def _quick_status_line(it: dict[str, Any], indent: str = "") -> str:
    iid = str(it.get("id") or "").strip()
    st = str(it.get("status") or "pending").strip()
    label = str(it.get("label") or iid).strip()
    face = str(it.get("catalog_face") or "")
    mark = "x" if st == "done" else "-" if st == "dropped" else " "
    if st == "in_dialogue":
        mark = " "
    suffix = f" [{face}]" if face else ""
    walk = str(it.get("walk_tier") or "")
    if walk:
        suffix += f" [{walk}]"
    elif it.get("supplement"):
        suffix += " [supplement]"
    return f"{indent}- [{mark}] `{iid}` — {label} (`{st}`){suffix}"


def _render_item_block(it: dict[str, Any]) -> list[str]:
    import json

    iid = str(it.get("id") or "").strip()
    if not iid:
        return []
    label = str(it.get("label") or iid).strip()
    lines = [f"### `{iid}` — {label}", ""]
    for key in (
        "status",
        "walk_tier",
        "mint_lane",
        "parent_id",
        "depth_band",
        "fanout",
        "depends_on",
        "historical_id",
        "series_id",
        "series_order",
        "series_walk_rank",
        "altitude",
        "seat",
        "time_scale",
        "does_not_mandate",
        "alternatives_not_banned",
        "inherits_parent_anti_mandate",
        "catalog_face",
        "experience_mode",
        "mode_tier",
        "dnd_pillar",
        "ux_axis",
        "dimension",
        "summary",
        "pillar_notes",
        "conceptual_pin",
        "derived_from",
        "ux_family",
        "supplement",
        "coverage_slot",
        "maps_to",
        "notes",
    ):
        val = it.get(key)
        if val is None:
            val = ""
        if isinstance(val, (list, dict)):
            text = json.dumps(val, ensure_ascii=False)
        else:
            text = str(val).replace("\n", " ").strip()
        if text == "" and not isinstance(val, (list, dict)):
            continue
        lines.append(f"- {key}: {text}")
    lines.append("")
    return lines


def render_mint_backlog_markdown(doc: dict[str, Any]) -> str:
    """Render Obsidian-facing MINT-BACKLOG.md from a backlog document."""
    pid = str(doc.get("project_id") or "").strip() or "project"
    status = str(doc.get("backlog_status") or "proposed")
    waived = [str(a) for a in (doc.get("waived_axes") or [])]
    generated = str(doc.get("generated_at") or "")
    frozen = str(doc.get("frozen_at") or "")
    rubric = str(doc.get("rubric") or "Docs/catalog-mint/_shared/UX-MINT-RUBRIC.md")
    mint_phase = str(doc.get("mint_phase") or "series_draft")
    harvest_pass = str(doc.get("harvest_pass") or "series")
    items = [i for i in (doc.get("items") or []) if isinstance(i, dict)]
    walk_split = bool(doc.get("walk_defs_split"))

    lines: list[str] = [
        "---",
        f"title: MINT-BACKLOG — {pid}",
        f"project-id: {pid}",
        "para-type: Project",
        f"backlog_status: {status}",
        f"mint_phase: {mint_phase}",
        f"harvest_pass: {harvest_pass}",
        f"series_draft_accepted: {str(bool(doc.get('series_draft_accepted'))).lower()}",
        f"waive_series_draft: {str(bool(doc.get('waive_series_draft'))).lower()}",
        f"children_greenlit: {str(bool(doc.get('children_greenlit'))).lower()}",
        f"children_rewritten: {str(bool(doc.get('children_rewritten'))).lower()}",
        f"walk_defs_split: {str(walk_split).lower()}",
        f"waived_axes: {_yaml_list_fm(waived)}",
        "schema_version: 1",
    ]
    locked_batches = [str(x) for x in (doc.get("locked_child_batches") or [])]
    # Always emit (including []) so unlock cannot be undone by YAML gate-merge
    lines.append(f"locked_child_batches: {_yaml_list_fm(locked_batches)}")
    for key in ("active_child_batch", "next_child_batch"):
        if doc.get(key):
            lines.append(f"{key}: {doc.get(key)}")
    if generated:
        lines.append(f"generated_at: {generated}")
    if frozen:
        lines.append(f"frozen_at: {frozen}")
    for key in (
        "series_published_trinity_ref",
        "children_published_trinity_ref",
        "archive_ref",
        "quality_validation_status",
        "quality_validation",
        "walk_defs_layout",
    ):
        val = doc.get(key)
        if val:
            text = str(val).replace("\n", " ").strip()
            lines.append(f"{key}: {text}")
    lines.extend(
        [
            f"rubric: {rubric}",
            "machine_mirror: MINT-BACKLOG.yaml",
            "---",
            "",
            f"# MINT-BACKLOG — `{pid}`",
            "",
        ]
    )
    if walk_split:
        lines.extend(
            [
                "Obsidian **list / prune** surface. Full Meaning defs live under "
                "`scopes/<parent>/SERIES.md` and "
                "`scopes/<parent>/children-of-<parent>/<child>/WALK.md` "
                "(list **dirs** under `children-of-*` to see the batch). "
                "Edit walk cards or status here; harvest/freeze/sync refreshes "
                "`MINT-BACKLOG.yaml`.",
                "",
            ]
        )
    else:
        lines.extend(
            [
                "Obsidian **operator prune / critique** surface. Edit item fields below "
                "(especially `status`), then harvest/freeze/sync will refresh "
                "`MINT-BACKLOG.yaml` (machine walk queue + Grok pack).",
                "",
            ]
        )
    lines.extend(
        [
            "## Operator gate (two-pass mint)",
            "",
            "1. **Series draft** (Cursor) → accept → series-only harvest.",
            "2. Prune series; freeze (series anti-mandate gate). Taxonomy coverage waits for children pass.",
            "3. Grok+user **series walk** until all series `done`.",
            "4. Diff/fit vs `archive_ref` if remine. Then **Trinity/GitHub publish** "
            "(`series_published_trinity_ref`) — Grok-facing gate, not Curator.",
            "5. Only then children harvest (series lens) → greenlight → Cursor batches → "
            "Trinity-publish children.",
            "6. Actions: `UX_MINT_BACKLOG` `series_draft` | `generate` | `freeze` | "
            "`publish_series` | `greenlight_children` | `lock_child_batch` | `publish_children`.",
            "",
            f"**Current status:** `{status}`  ",
            f"**Mint phase:** `{mint_phase}`  ",
            f"**Harvest pass:** `{harvest_pass}`  ",
            f"**Series Trinity ref:** `{doc.get('series_published_trinity_ref') or '(none)'}`  ",
            f"**Children Trinity ref:** `{doc.get('children_published_trinity_ref') or '(none)'}`  ",
            f"**Quality validation:** `{doc.get('quality_validation_status') or '(unset)'}`  ",
            f"**Locked child batches:** `{', '.join(str(x) for x in (doc.get('locked_child_batches') or [])) or '(none)'}`  ",
            f"**Active / next child batch:** `{doc.get('active_child_batch') or doc.get('next_child_batch') or '(auto: largest pending)'}`  ",
            f"**Waived axes/slots:** `{', '.join(waived) if waived else '(none)'}`  ",
            f"**Walk defs split:** `{walk_split}`  ",
            f"**Rubric:** [[{rubric.replace('.md', '')}|UX mint rubric]]",
            "",
        ]
    )
    qv = str(doc.get("quality_validation") or "").strip()
    if qv:
        lines.extend(
            [
                f"> [!warning] Quality caveat — structure first  ",
                f"> {qv}",
                "",
            ]
        )
    lines.extend(
        [
            "## Quick status (by series parent)",
            "",
            "Grouped by paternity — series parent, then its children. "
            "Not a flat coverage list.",
            "",
        ]
    )
    locked = {str(x) for x in (doc.get("locked_child_batches") or [])}
    active = str(doc.get("active_child_batch") or doc.get("next_child_batch") or "").strip()
    for parent, children in _items_by_series_parent(items):
        if parent is None:
            lines.append("#### Unparented children")
            lines.append("")
            for ch in children:
                lines.append(_quick_status_line(ch, indent=""))
            lines.append("")
            continue
        batch_id = str(parent.get("id") or "")
        badge = ""
        if batch_id in locked:
            badge = " — **LOCKED batch**"
        elif batch_id == active:
            badge = " — **ACTIVE batch**"
        lines.append(
            f"#### Series `{batch_id}` — "
            f"{str(parent.get('label') or batch_id).strip()}{badge}"
        )
        lines.append("")
        lines.append(_quick_status_line(parent, indent=""))
        if walk_split:
            lines.append(
                f"  - *Walk dirs:* `scopes/{batch_id}/SERIES.md` · "
                f"`scopes/{batch_id}/{children_of_dirname(batch_id)}/<child>/WALK.md`"
            )
        if children:
            pend = sum(1 for c in children if str(c.get("status") or "") == "pending")
            done = sum(1 for c in children if str(c.get("status") or "") == "done")
            lines.append(
                f"  - *Children: {done} done / {pend} pending / {len(children)} total*"
            )
            for ch in children:
                lines.append(_quick_status_line(ch, indent="  "))
        else:
            lines.append("  - *No children lensed under this series*")
        lines.append("")

    if walk_split:
        lines.extend(
            [
                "## Items",
                "",
                "Full Meaning cards are **not** inlined here. Open:",
                "",
                "- Series: `scopes/<series_id>/SERIES.md`",
                "- Children: list dirs under `scopes/<parent>/children-of-<parent>/` "
                "then open `<child>/WALK.md`",
                "",
                "Factory L5 remains `scopes/<row_id>/L5.md` (separate from walk cards).",
                "",
            ]
        )
    else:
        lines.extend(["## Items", ""])
        for parent, children in _items_by_series_parent(items):
            if parent is None:
                lines.append("#### Unparented children")
                lines.append("")
                for ch in children:
                    lines.extend(_render_item_block(ch))
                continue
            batch_id = str(parent.get("id") or "")
            lines.append(f"#### Series parent `{batch_id}`")
            lines.append("")
            lines.extend(_render_item_block(parent))
            if children:
                lines.append(f"**Children of `{batch_id}`**")
                lines.append("")
                for ch in children:
                    lines.extend(_render_item_block(ch))

    lines.append("## Coverage reminder")
    lines.append("")
    lines.append(
        "Two-pass: series cards first (`walk_tier: series`), locked + Trinity-published, "
        "then children mined through those lenses. Display groups children under their "
        "`parent_id` series. Taxonomy slots are children-pass coverage; "
        "Actual-Play nouns are thickeners/skins. See rubric + `SERIES-ALTITUDE-EXEMPLARS.md`."
    )
    lines.append("")
    return "\n".join(lines)


def parse_mint_backlog_markdown(text: str) -> dict[str, Any]:
    """Parse Obsidian MINT-BACKLOG.md into the machine backlog document shape."""
    fm: dict[str, Any] = {}
    body = text
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            raw_fm = text[3:end].strip()
            try:
                parsed = yaml.safe_load(raw_fm) or {}
                if isinstance(parsed, dict):
                    fm = parsed
            except Exception:
                fm = {}
            body = text[end + 4 :].lstrip("\n")

    waived_raw = fm.get("waived_axes") or []
    if isinstance(waived_raw, str):
        waived = [a.strip() for a in waived_raw.strip("[]").split(",") if a.strip()]
    elif isinstance(waived_raw, list):
        waived = [str(a) for a in waived_raw]
    else:
        waived = []

    pid = str(fm.get("project-id") or fm.get("project_id") or "").strip()
    status = str(fm.get("backlog_status") or fm.get("status") or "proposed").strip()

    # Only parse item cards under ## Items — Quick status #### batch headers are display-only.
    items_body = body
    items_match = re.search(r"^##\s+Items\b[^\n]*\n", body, re.MULTILINE)
    if items_match:
        start = items_match.end()
        next_h2 = re.search(r"^##\s+\S", body[start:], re.MULTILINE)
        end = start + next_h2.start() if next_h2 else len(body)
        items_body = body[start:end]

    items: list[dict[str, Any]] = []
    headers = list(_ITEM_HEADER_RE.finditer(items_body))
    for i, match in enumerate(headers):
        iid = match.group(1).strip()
        label_from_h = (match.group(2) or "").strip()
        start = match.end()
        end_pos = headers[i + 1].start() if i + 1 < len(headers) else len(items_body)
        block = items_body[start:end_pos]
        fields: dict[str, str] = {}
        for fm_match in _ITEM_FIELD_RE.finditer(block):
            fields[fm_match.group(1)] = fm_match.group(2).strip()
        item = {
            "id": iid,
            "label": fields.get("label") or label_from_h or iid,
            "dimension": fields.get("dimension") or "",
            "ux_axis": fields.get("ux_axis") or "",
            "summary": fields.get("summary") or "",
            "conceptual_pin": fields.get("conceptual_pin") or "",
            "derived_from": fields.get("derived_from") or "",
            "ux_family": fields.get("ux_family") or "",
            "status": fields.get("status") or "pending",
        }
        for extra in (
            "catalog_face",
            "experience_mode",
            "mode_tier",
            "dnd_pillar",
            "pillar_notes",
            "notes",
            "walk_tier",
            "maps_to",
            "series_id",
            "altitude",
            "time_scale",
            "seat",
            "does_not_mandate",
            "alternatives_not_banned",
            "series_order",
            "series_walk_rank",
            "mint_lane",
            "parent_id",
            "fanout",
            "historical_id",
            "depends_on",
            "depth_band",
        ):
            if fields.get(extra):
                raw = fields[extra]
                if extra in (
                    "seat",
                    "does_not_mandate",
                    "alternatives_not_banned",
                    "depends_on",
                ) and raw.strip().startswith("["):
                    try:
                        import json

                        parsed = json.loads(raw)
                        item[extra] = parsed if isinstance(parsed, list) else raw
                        continue
                    except Exception:
                        pass
                    try:
                        parsed = yaml.safe_load(raw)
                        item[extra] = parsed if isinstance(parsed, list) else raw
                        continue
                    except Exception:
                        pass
                if extra in ("series_order", "depth_band", "series_walk_rank"):
                    try:
                        item[extra] = int(raw)
                        continue
                    except (TypeError, ValueError):
                        pass
                item[extra] = raw
        for flag in ("supplement", "coverage_slot", "feedstock_hit"):
            raw = fields.get(flag)
            if raw is None or raw == "":
                continue
            item[flag] = str(raw).strip().lower() in {"true", "1", "yes"}
        items.append(item)

    def _fm_bool(key: str, default: bool = False) -> bool:
        raw = fm.get(key)
        if raw is None:
            return default
        if isinstance(raw, bool):
            return raw
        return str(raw).strip().lower() in {"true", "1", "yes"}

    doc: dict[str, Any] = {
        "schema_version": int(fm.get("schema_version") or 1),
        "project_id": pid,
        "backlog_status": status,
        "waived_axes": waived,
        "rubric": str(fm.get("rubric") or "Docs/catalog-mint/_shared/UX-MINT-RUBRIC.md"),
        "mint_phase": str(fm.get("mint_phase") or "series_draft"),
        "harvest_pass": str(fm.get("harvest_pass") or "series"),
        "series_draft_accepted": _fm_bool("series_draft_accepted"),
        "waive_series_draft": _fm_bool("waive_series_draft"),
        "children_greenlit": _fm_bool("children_greenlit"),
        "children_rewritten": _fm_bool("children_rewritten"),
        "walk_defs_split": _fm_bool("walk_defs_split"),
        "items": items,
    }
    locked_raw = fm.get("locked_child_batches") or []
    if isinstance(locked_raw, str):
        doc["locked_child_batches"] = [
            a.strip() for a in locked_raw.strip("[]").split(",") if a.strip()
        ]
    elif isinstance(locked_raw, list):
        doc["locked_child_batches"] = [str(a) for a in locked_raw]
    for key in (
        "generated_at",
        "frozen_at",
        "series_published_trinity_ref",
        "children_published_trinity_ref",
        "archive_ref",
        "quality_validation",
        "quality_validation_status",
        "active_child_batch",
        "next_child_batch",
        "walk_defs_layout",
    ):
        if fm.get(key):
            doc[key] = str(fm[key])
    return doc


def _maybe_overlay_walk_items(vault_root: Path, project_id: str, data: dict[str, Any]) -> dict[str, Any]:
    """When walk dirs exist, Meaning items come from SERIES.md / children-of-*/WALK.md."""
    scopes = user_story_paths(vault_root, project_id)["scopes_dir"]
    if not walk_tree_present(scopes):
        return data
    out = dict(data)
    walk_items = load_items_from_walk_files(scopes)
    if walk_items:
        out["items"] = walk_items
        out["walk_defs_split"] = True
        out.setdefault(
            "walk_defs_layout",
            "scopes/<parent>/children-of-<parent>/<child>/WALK.md",
        )
    return out


def migrate_mint_backlog_to_walk_dirs(vault_root: Path, project_id: str) -> dict[str, Any]:
    """One-shot: split monolithic backlog Meaning into walk dirs; rewrite thin list."""
    ypath = backlog_path(vault_root, project_id)
    if not ypath.is_file():
        raise FileNotFoundError(ypath)
    doc = load_yaml(ypath)
    if not isinstance(doc, dict):
        raise ValueError("MINT-BACKLOG.yaml is not a mapping")
    doc.setdefault("project_id", project_id)
    doc = split_backlog_doc_to_walk_dirs(vault_root, project_id, doc)
    write_mint_backlog(vault_root, project_id, doc)
    return doc


def write_mint_backlog(vault_root: Path, project_id: str, doc: dict[str, Any]) -> tuple[Path, Path]:
    """Write YAML machine mirror + Obsidian markdown surface (+ walk dirs when split)."""
    vault_root = vault_root.resolve()
    ypath = backlog_path(vault_root, project_id)
    mpath = backlog_md_path(vault_root, project_id)
    ypath.parent.mkdir(parents=True, exist_ok=True)
    yaml_doc = dict(doc)
    if bool(yaml_doc.get("walk_defs_split")):
        sync_all_walk_files(vault_root, project_id, yaml_doc)
    save_yaml(ypath, yaml_doc)
    mpath.write_text(render_mint_backlog_markdown(yaml_doc), encoding="utf-8")
    return ypath, mpath


def _slug(text: str) -> str:
    s = re.sub(r"[^a-zA-Z0-9]+", "_", text.lower()).strip("_")
    return s[:48] or "ux_item"


def is_rejected_candidate(item_id: str, label: str, summary: str = "") -> bool:
    """Anti-phase / anti-backend filter."""
    if _PHASE_ID_RE.match(item_id.strip()):
        return True
    if _PHASE_LABEL_RE.match(label.strip()):
        return True
    blob = f"{label} {summary}"
    if _BACKENDISH.search(blob):
        return True
    # Pure phase-title harvest residues
    if re.match(r"^phase_\d", item_id, re.I):
        return True
    return False


def experiential_skew_ok(items: list[dict[str, Any]], *, min_ratio: float = 0.5) -> bool:
    """Heuristic: enough labels/summaries carry experiential vocabulary."""
    if not items:
        return False
    hits = 0
    for it in items:
        blob = f"{it.get('label', '')} {it.get('summary', '')}".lower()
        if any(h in blob for h in EXPERIENTIAL_HINTS):
            hits += 1
    return (hits / len(items)) >= min_ratio


def assert_ux_axis_coverage(
    items: list[dict[str, Any]],
    *,
    waived_axes: list[str] | None = None,
) -> tuple[bool, tuple[str, ...]]:
    """Legacy axis check retained for older fixtures; prefer assert_taxonomy_coverage."""
    waived = {str(a) for a in (waived_axes or [])}
    present: set[str] = set()
    for it in items:
        if str(it.get("status") or "") == "dropped":
            continue
        ax = str(it.get("ux_axis") or "").strip()
        if ax:
            present.add(ax)
    missing = tuple(a for a in REQUIRED_UX_AXES if a not in present and a not in waived)
    return (len(missing) == 0, missing)


def assert_backlog_coverage(
    vault_root: Path,
    project_id: str,
    items: list[dict[str, Any]],
    *,
    waived: list[str] | None = None,
) -> tuple[bool, tuple[str, ...]]:
    """Primary gate: taxonomy slot completeness."""
    from .ux_mint_taxonomy import assert_taxonomy_coverage, load_ux_mint_taxonomy

    tax = load_ux_mint_taxonomy(vault_root, project_id)
    if tax.get("slots"):
        return assert_taxonomy_coverage(items, tax, waived_slots=waived)
    return assert_ux_axis_coverage(items, waived_axes=waived)


# Theme seed axis → nearest taxonomy experience_mode (for maps_to on supplements).
_AXIS_TO_MODE = {
    "perspective_overrides": "divination_override",
    "agency": "baseline_fp",
    "dm_player_rails": "dm_pilot",
    "class_chrome": "class_chrome_discovery",
    "combat_cast_feedback": "combat_cast_feedback",
    "session0_identity_art": "session0_bootstrap",
    "presentation_shells": "application_shell",
}


def _pin_from_derived(derived_from: str) -> str:
    if not derived_from or ":" not in derived_from:
        return ""
    prefix, _, rest = derived_from.partition(":")
    if prefix in {"pin", "pmg", "research", "rules", "resource", "actual_play"} and rest:
        return rest
    return ""


def _seed_experience_noun_candidates(
    derived_from: str,
    text: str,
) -> list[dict[str, Any]]:
    """Lift `label` / `summary` pairs from Actual-Play moment cards into supplements."""
    if not derived_from.startswith("actual_play:"):
        return []
    pin = _pin_from_derived(derived_from)
    out: list[dict[str, Any]] = []
    for m in _NOUN_CANDIDATE_RE.finditer(text or ""):
        label = m.group(1).strip().strip("`\"'")
        summary = m.group(2).strip().strip("`\"'")
        if not label or len(label) < 3:
            continue
        if _is_junk_heading(label):
            continue
        item_id = f"ux_{_slug(label)}"
        if is_rejected_candidate(item_id, label, summary):
            continue
        axis = "agency"
        for pat, ax, *_rest in _THEME_SEEDS:
            if pat.search(f"{label} {summary}"):
                axis = ax
                break
        face = "table"
        low = f"{label} {summary}".lower()
        if any(k in low for k in ("chrome", "screen", "verb", "feedback", "diegetic", "hud")):
            face = "surfaces"
        elif any(k in low for k in ("world", "faction", "npc", "lore", "earned", "conspiracy")):
            face = "living_world"
        elif any(k in low for k in ("camp", "quiet", "pillar", "companion", "trust", "social")):
            face = "table"
        elif any(k in low for k in ("flee", "agency", "stolen", "control", "authorship")):
            face = "inhabit"
        out.append(
            {
                "id": item_id,
                "label": label[:80],
                "dimension": "ui_surface",
                "ux_axis": axis,
                "summary": summary[:400] or f"Experience noun from actual-play card: {label}",
                "conceptual_pin": pin,
                "derived_from": derived_from,
                "ux_family": "",
                "status": "pending",
                "catalog_face": face,
                "experience_mode": "",
                "mode_tier": "thickener",
                "dnd_pillar": "shared",
                "feedstock_hit": True,
                "pillar_notes": "",
                # AP nouns are exemplar skins only — never series/primary walk.
                "supplement": True,
                "coverage_slot": False,
                "walk_tier": "thickener",
                "altitude": "scene_exemplar",
                "maps_to": _AXIS_TO_MODE.get(axis, ""),
            }
        )
    return out


def _seed_from_text(
    derived_from: str,
    text: str,
    *,
    allow_headings: bool = True,
) -> list[dict[str, Any]]:
    """Project-specific supplement nouns from theme seeds + experiential headings."""
    from .ux_mint_taxonomy import is_api_heading

    out: list[dict[str, Any]] = []
    seen_axes: set[str] = set()
    pin = _pin_from_derived(derived_from)
    # Prefer explicit moment-card candidates before heading/theme heuristics
    out.extend(_seed_experience_noun_candidates(derived_from, text))
    for pat, axis, dim, id_stub, label, summary in _THEME_SEEDS:
        if axis in seen_axes and axis != "presentation_shells":
            if any(x["ux_axis"] == axis for x in out):
                continue
        if not pat.search(text):
            continue
        item = {
            "id": id_stub,
            "label": label,
            "dimension": dim,
            "ux_axis": axis,
            "summary": summary,
            "conceptual_pin": pin,
            "derived_from": derived_from,
            "ux_family": "",
            "status": "pending",
            "catalog_face": "supplement",
            "experience_mode": "",
            "mode_tier": "thickener",
            "dnd_pillar": "shared",
            "feedstock_hit": True,
            "pillar_notes": "",
            "supplement": True,
            "coverage_slot": False,
            "walk_tier": "thickener",
            "maps_to": _AXIS_TO_MODE.get(axis, ""),
        }
        if is_rejected_candidate(item["id"], item["label"], item["summary"]):
            continue
        out.append(item)
        seen_axes.add(axis)
    if not allow_headings:
        return out
    for m in _HEADING_RE.finditer(text):
        title = m.group(1).strip()
        if _PHASE_LABEL_RE.match(title):
            continue
        if is_api_heading(title):
            continue
        if _is_junk_heading(title):
            continue
        low = title.lower()
        if not any(h in low for h in EXPERIENTIAL_HINTS):
            continue
        axis = "agency"
        for pat, ax, *_rest in _THEME_SEEDS:
            if pat.search(title):
                axis = ax
                break
        item_id = f"ux_{_slug(title)}"
        if is_rejected_candidate(item_id, title):
            continue
        out.append(
            {
                "id": item_id,
                "label": title[:80],
                "dimension": "ui_surface",
                "ux_axis": axis,
                "summary": (
                    f"Project-specific experience noun from feedstock heading "
                    f"`{title[:120]}`. Grounds taxonomy coverage in local pin language."
                ),
                "conceptual_pin": pin,
                "derived_from": derived_from,
                "ux_family": "",
                "status": "pending",
                "catalog_face": "supplement",
                "experience_mode": "",
                "mode_tier": "thickener",
                "dnd_pillar": "shared",
                "feedstock_hit": True,
                "pillar_notes": "",
                "supplement": True,
                "coverage_slot": False,
                "walk_tier": "thickener",
                "maps_to": _AXIS_TO_MODE.get(axis, ""),
            }
        )
    return out


def _is_junk_heading(title: str) -> bool:
    """Drop URL / meta / process / bare API-token headings from research noise."""
    low = title.lower().strip()
    if low.startswith("source:") or "http://" in low or "https://" in low:
        return True
    if low.startswith("www.") or ".com/" in low or ".io/" in low:
        return True
    if any(
        k in low
        for k in (
            "workflow_state",
            "slice catalog handoff",
            "factory line restart",
            "supersession",
            "binding decision",
            "gap closed",
            "batch mode",
        )
    ):
        return True
    if low.startswith("filled ") or low.startswith("with "):
        return True
    # CamelCase *Slot / *Handle / *Gate tokens (even when regex camel split fails on DMCam…)
    if re.search(
        r"(Slot|Handle|Gate|Policy|Manifest|Controller|Rig|Envelope)\s*$",
        title.strip(),
    ) and " " not in title.strip():
        return True
    return False


def collect_supplement_items(chunks: list[tuple[str, str]], *, max_items: int = 120) -> list[dict[str, Any]]:
    """Union pin-noun supplements; prefer UX-rich tiers (actual_play/pmg/research/pin Phase 4–6)."""
    by_id: dict[str, dict[str, Any]] = {}
    ordered = sorted(
        chunks,
        key=lambda ct: (
            0
            if ct[0].startswith("actual_play:")
            else 1
            if ct[0].startswith("pmg:")
            else 2
            if ct[0].startswith("research:")
            else 3
            if ct[0].startswith("pin:")
            else 4
            if ct[0].startswith("rules:")
            else 5
        ),
    )
    # Pass 1: moment-card experience noun candidates (thickeners / scene skins only)
    for ref, text in ordered:
        if not ref.startswith("actual_play:"):
            continue
        for item in _seed_experience_noun_candidates(ref, text):
            iid = str(item.get("id") or "")
            if not iid or iid in by_id:
                continue
            by_id[iid] = item
            if len(by_id) >= max_items:
                return list(by_id.values())
    # Pass 2: theme seeds + headings (fill remaining budget)
    for ref, text in ordered:
        if len(by_id) >= max_items:
            break
        if ref.startswith("pin:"):
            low = ref.lower()
            if re.search(r"phase[-_]?[1-3]\b", low) and not any(
                k in low for k in ("perspective", "agency", "chrome", "presentation", "hud")
            ):
                continue
        allow_headings = (
            ref.startswith("actual_play:") or ref.startswith("pmg:") or ref.startswith("pin:")
        )
        for item in _seed_from_text(ref, text, allow_headings=allow_headings):
            iid = str(item.get("id") or "")
            if not iid or iid in by_id:
                continue
            # Skip re-adding candidates already harvested in pass 1
            by_id[iid] = item
            if len(by_id) >= max_items:
                return list(by_id.values())
    return list(by_id.values())


def _rank_items(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    face_rank = {
        "inhabit": 0,
        "table": 1,
        "living_world": 2,
        "surfaces": 3,
        "flows": 4,
        "content": 5,
        "system": 6,
        "supplement": 8,
    }
    pillar_rank = {"shared": 0, "exploration": 1, "combat": 2, "roleplay": 3}
    # Walk order: series packs → taxonomy coverage → AP/theme thickeners
    # Legacy "phenomenology" ranks with thickener (demoted).
    tier_rank = {"series": 0, "coverage": 1, "thickener": 2, "phenomenology": 2}

    def key(it: dict[str, Any]) -> tuple[int, int, int, int, int, str, int, str]:
        derived = str(it.get("derived_from") or "")
        walk = str(it.get("walk_tier") or "").strip()
        if not walk:
            if derived.startswith("series:"):
                walk = "series"
            elif it.get("coverage_slot"):
                walk = "coverage"
            elif it.get("supplement") or derived.startswith("actual_play:"):
                walk = "thickener"
            else:
                walk = "coverage"
        # Enforce invariant: AP source never ranks as series
        if derived.startswith("actual_play:") and walk == "series":
            walk = "thickener"
        try:
            s_rank = int(it.get("series_walk_rank") or 0)
        except (TypeError, ValueError):
            s_rank = 0
        try:
            s_order = int(it.get("series_order") or 0)
        except (TypeError, ValueError):
            s_order = 0
        return (
            tier_rank.get(walk, 9),
            s_rank if walk == "series" else 0,
            s_order if walk == "series" else 0,
            face_rank.get(str(it.get("catalog_face") or ""), 9),
            pillar_rank.get(str(it.get("dnd_pillar") or ""), 9),
            str(it.get("series_id") or ""),
            0,
            str(it.get("id") or ""),
        )

    return sorted(items, key=key)


def _merge_items(
    existing: list[dict[str, Any]],
    harvested: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    by_id: dict[str, dict[str, Any]] = {}
    for it in existing:
        iid = str(it.get("id") or "").strip()
        if iid:
            by_id[iid] = dict(it)
    for it in harvested:
        iid = str(it.get("id") or "").strip()
        if not iid:
            continue
        if iid in by_id:
            prev = by_id[iid]
            st = str(prev.get("status") or "pending")
            if st in {"done", "dropped", "in_dialogue"}:
                # Keep operator terminal/in-flight row; still attach taxonomy keys if missing
                for k in ("catalog_face", "experience_mode", "mode_tier", "dnd_pillar"):
                    if it.get(k) and not prev.get(k):
                        prev[k] = it[k]
                by_id[iid] = prev
                continue
            merged = dict(it)
            merged["status"] = st
            if prev.get("notes"):
                merged["notes"] = prev["notes"]
            if prev.get("conceptual_pin") and str(prev.get("conceptual_pin")) not in ("", "needs pin"):
                merged["conceptual_pin"] = prev["conceptual_pin"]
            by_id[iid] = merged
        else:
            by_id[iid] = dict(it)
    return _rank_items(list(by_id.values()))


def load_mint_backlog(vault_root: Path, project_id: str) -> dict[str, Any]:
    """
    Load backlog. Prefer newer of Obsidian `MINT-BACKLOG.md` vs YAML mirror
    (Obsidian edits bump MD mtime; harness-only YAML edits still load).

    When MD wins on mtime, still fill empty doc-level gates from YAML so
    Trinity refs / locked batches cannot vanish from an incomplete frontmatter.
    """
    empty = {
        "schema_version": 1,
        "project_id": project_id,
        "backlog_status": "proposed",
        "waived_axes": [],
        "items": [],
    }
    mpath = backlog_md_path(vault_root, project_id)
    path = backlog_path(vault_root, project_id)
    md_exists = mpath.is_file()
    y_exists = path.is_file()
    use_md = False
    if md_exists and y_exists:
        use_md = mpath.stat().st_mtime >= path.stat().st_mtime
    elif md_exists:
        use_md = True

    y_doc: dict[str, Any] | None = None
    if y_exists:
        loaded = load_yaml(path)
        if isinstance(loaded, dict):
            y_doc = loaded

    if use_md:
        try:
            data = parse_mint_backlog_markdown(mpath.read_text(encoding="utf-8"))
            if isinstance(data, dict) and data.get("items") is not None:
                if not data.get("project_id"):
                    data["project_id"] = project_id
                if y_doc is not None:
                    data = _merge_yaml_doc_gates(data, y_doc)
                data = _maybe_overlay_walk_items(vault_root, project_id, data)
                return data
        except Exception:
            pass
    if y_doc is not None:
        return _maybe_overlay_walk_items(vault_root, project_id, y_doc)
    empty2 = dict(empty)
    return _maybe_overlay_walk_items(vault_root, project_id, empty2)


def pending_child_batches(backlog: dict[str, Any]) -> list[tuple[str, list[dict[str, Any]]]]:
    """Pending non-series items grouped by parent_id, largest batch first."""
    groups: dict[str, list[dict[str, Any]]] = {}
    for it in backlog.get("items") or []:
        if not isinstance(it, dict):
            continue
        if str(it.get("walk_tier") or "") == "series":
            continue
        if str(it.get("status") or "") != "pending":
            continue
        pid = str(it.get("parent_id") or "").strip() or "_unparented"
        groups.setdefault(pid, []).append(it)
    ordered = sorted(groups.items(), key=lambda kv: (-len(kv[1]), kv[0]))
    return ordered


def next_pending_item(backlog: dict[str, Any]) -> dict[str, Any] | None:
    """Next pending item respecting mint_phase / Trinity gates / same-width child batches."""
    phase = str(backlog.get("mint_phase") or "series_walk")
    greenlit = bool(backlog.get("children_greenlit"))
    series_pub = str(backlog.get("series_published_trinity_ref") or "").strip()
    ranked = _rank_items([i for i in (backlog.get("items") or []) if isinstance(i, dict)])
    for it in ranked:
        if str(it.get("status") or "") != "pending":
            continue
        walk = str(it.get("walk_tier") or "")
        if phase in {"series_draft", "series_walk", "series_locked"} or not series_pub:
            if walk == "series":
                return it
            continue
        if phase == "hub_children":
            if walk == "series":
                continue
            if str(it.get("fanout") or "") == "high" or str(it.get("mint_lane") or "") == "human_grok":
                return it
            continue
        if not greenlit:
            continue
        if walk == "series":
            continue
        # Children: stay inside active/same-width batch (not global rank across parents)
        active = str(backlog.get("active_child_batch") or backlog.get("next_child_batch") or "").strip()
        batches = pending_child_batches(backlog)
        if not batches:
            return None
        if active:
            for pid, items in batches:
                if pid == active:
                    # rank within batch only
                    ids = {str(i.get("id")) for i in items}
                    for cand in ranked:
                        if str(cand.get("id") or "") in ids and str(cand.get("status") or "") == "pending":
                            return cand
                    return items[0]
        # Default: largest pending parent batch
        pid, items = batches[0]
        ids = {str(i.get("id")) for i in items}
        for cand in ranked:
            if str(cand.get("id") or "") in ids and str(cand.get("status") or "") == "pending":
                return cand
        return items[0]
    return None


def backlog_summary(vault_root: Path, project_id: str) -> dict[str, Any]:
    """Surface for loop2 / next-tick — pending count + next id."""
    bl = load_mint_backlog(vault_root, project_id)
    items = [i for i in (bl.get("items") or []) if isinstance(i, dict)]
    pending = [i for i in items if str(i.get("status") or "") == "pending"]
    nxt = next_pending_item(bl)
    return {
        "backlog_status": str(bl.get("backlog_status") or "proposed"),
        "mint_phase": str(bl.get("mint_phase") or "series_draft"),
        "harvest_pass": str(bl.get("harvest_pass") or "series"),
        "series_published_trinity_ref": str(bl.get("series_published_trinity_ref") or ""),
        "children_published_trinity_ref": str(bl.get("children_published_trinity_ref") or ""),
        "children_greenlit": bool(bl.get("children_greenlit")),
        "item_count": len(items),
        "pending_count": len(pending),
        "next_pending_id": str(nxt.get("id")) if nxt else None,
        "next_pending_label": str(nxt.get("label")) if nxt else None,
        "path": str(backlog_path(vault_root, project_id).relative_to(vault_root.resolve())),
    }


def _list_field_count(raw: Any) -> int:
    """Count entries in list-ish backlog fields (list, JSON/YAML string, or truncated)."""
    if isinstance(raw, list):
        return len([x for x in raw if str(x).strip()])
    if not isinstance(raw, str) or not raw.strip():
        return 0
    s = raw.strip()
    if s.startswith("["):
        try:
            import json

            parsed = json.loads(s)
            if isinstance(parsed, list):
                return len([x for x in parsed if str(x).strip()])
        except Exception:
            pass
        try:
            parsed = yaml.safe_load(s)
            if isinstance(parsed, list):
                return len([x for x in parsed if str(x).strip()])
        except Exception:
            pass
        inner = s.strip("[]")
        parts = [p.strip().strip("'\"") for p in inner.split(",") if p.strip().strip("'\"")]
        return len(parts)
    return len([p for p in re.split(r"[|;]", s) if p.strip()])


def _alternatives_count(item: dict[str, Any]) -> int:
    return _list_field_count(item.get("alternatives_not_banned"))


def assert_series_freeze_gates(items: list[dict[str, Any]]) -> tuple[bool, list[str]]:
    """
    Fail-closed freeze gate for series parents: each pending/in_dialogue/done series
    item needs ≥2 alternatives_not_banned (or ≥2 does_not_mandate) as bootstrap.
    """
    gaps: list[str] = []
    for it in items:
        if str(it.get("walk_tier") or "") != "series":
            continue
        st = str(it.get("status") or "pending")
        if st == "dropped":
            continue
        if _alternatives_count(it) < 2 and _list_field_count(it.get("does_not_mandate")) < 2:
            gaps.append(str(it.get("id") or "?"))
    return (len(gaps) == 0, gaps)


def series_items_non_dropped(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for it in items:
        if str(it.get("walk_tier") or "") != "series":
            continue
        if str(it.get("status") or "pending") == "dropped":
            continue
        out.append(it)
    return out


def assert_all_series_done(items: list[dict[str, Any]]) -> tuple[bool, list[str]]:
    pending: list[str] = []
    for it in series_items_non_dropped(items):
        if str(it.get("status") or "") != "done":
            pending.append(str(it.get("id") or "?"))
    return (len(pending) == 0, pending)


def assert_series_draft_for_freeze(bl: dict[str, Any]) -> tuple[bool, str]:
    if bool(bl.get("series_draft_accepted")) or bool(bl.get("waive_series_draft")):
        return True, ""
    return False, "series_draft_not_accepted"


def assert_series_published_for_children(bl: dict[str, Any]) -> tuple[bool, str]:
    items = [i for i in (bl.get("items") or []) if isinstance(i, dict)]
    done_ok, pending = assert_all_series_done(items)
    if not done_ok:
        return False, f"series_incomplete:{','.join(pending[:12])}"
    ref = str(bl.get("series_published_trinity_ref") or "").strip()
    if not ref:
        return False, "series_published_trinity_ref_missing"
    return True, ""


# Prefer series parents that own dual-rail / domain claims over axis/face coincidence.
# Keys = child experience_mode (taxonomy slot id) or child id without ux_ prefix.
CHILD_SERIES_AFFINITY: dict[str, str] = {
    # Dual-rail camera / control envelopes (player FP + DM WorldCam and departures)
    "baseline_fp": "ux_camera_control_envelopes",
    "baseline_fp_controls": "ux_camera_control_envelopes",
    "divination_override": "ux_camera_control_envelopes",
    "planar_travel_override": "ux_camera_control_envelopes",
    "liminal_unconscious": "ux_camera_control_envelopes",
    "dominate_pilot": "ux_camera_control_envelopes",
    "dominate_victim": "ux_camera_control_envelopes",
    "absent_proxy": "ux_camera_control_envelopes",
    "agency_handoff_enter_exit": "ux_camera_control_envelopes",
    "dm_worldcam": "ux_camera_control_envelopes",
    "dm_mapcam": "ux_camera_control_envelopes",
    "dm_sensorium": "ux_camera_control_envelopes",
    "dm_pilot": "ux_camera_control_envelopes",
    # Living-world continuity (not mid-game power-band dump)
    "canon_pipeline_feel": "ux_living_world_continuity",
    "economy_resources": "ux_living_world_continuity",
    "economy_trade": "ux_living_world_continuity",
    "quest_pressure_surface": "ux_living_world_continuity",
    "sim_weather_pulse": "ux_living_world_continuity",
    "wa_faction_goals": "ux_living_world_continuity",
    "wa_faction_hierarchy": "ux_living_world_continuity",
    "wa_faction_offscreen": "ux_living_world_continuity",
    "wa_faction_reputation": "ux_living_world_continuity",
    "wa_faction_territory": "ux_living_world_continuity",
    "wa_lore_articles": "ux_living_world_continuity",
    "wa_npc_agenda": "ux_living_world_continuity",
    "wa_npc_relations": "ux_living_world_continuity",
    "wa_npc_secrets": "ux_living_world_continuity",
    "wa_npc_sheet": "ux_living_world_continuity",
    "wa_npc_dialogue_hooks": "ux_living_world_continuity",
    "wa_timelines": "ux_living_world_continuity",
    "wa_locations": "ux_living_world_continuity",
    "wa_maps_vs_embodied": "ux_living_world_continuity",
    # Authorship / world change
    "worldgen_gui": "ux_world_generation",
    "content_authoring_surface": "ux_world_authorship_modability",
    # Table / chronicle / prep (non-camera)
    "chronicle_buckets": "ux_backstory_legacy_integration",
    "player_lite_lore_gui": "ux_backstory_legacy_integration",
    "dm_workbench_lore_gui": "ux_dm_session_prep",
    "session0_bootstrap": "ux_dm_campaign_creation",
    "tone_profile_surface": "ux_dm_campaign_creation",
    "session_onboarding": "ux_dm_campaign_creation",
    "class_chrome_discovery": "ux_backstory_legacy_integration",
    "combat_cast_feedback": "ux_combat_play_surface",
    "application_shell": "ux_collaborative_table_agency",
    "primary_navigation": "ux_collaborative_table_agency",
}

_VACUUM_PARENTS = frozenset(
    {
        "ux_mid_game",
        "ux_early_game",
        "ux_late_game",
    }
)


def _child_affinity_key(child: dict[str, Any]) -> str:
    mode = str(child.get("experience_mode") or "").strip()
    if mode:
        return mode
    iid = str(child.get("id") or "").strip()
    if iid.startswith("ux_"):
        return iid[3:]
    return iid


def _lens_parent_for_child(
    child: dict[str, Any],
    series_parents: list[dict[str, Any]],
) -> dict[str, Any] | None:
    """
    Pick a locked series parent to lens a coverage/thickener child.

    Affinity map wins for dual-rail / domain ownership (e.g. DM WorldCam under
    camera envelopes, not session-prep). Axis/face scores are secondary.
    """
    by_id = {str(sp.get("id") or ""): sp for sp in series_parents if sp.get("id")}
    aff_key = _child_affinity_key(child)
    preferred = CHILD_SERIES_AFFINITY.get(aff_key)
    if preferred and preferred in by_id:
        return by_id[preferred]

    c_axis = str(child.get("ux_axis") or "")
    c_face = str(child.get("catalog_face") or "")
    c_dim = str(child.get("dimension") or "")
    c_blob = " ".join(
        [
            str(child.get("id") or ""),
            str(child.get("label") or ""),
            str(child.get("experience_mode") or ""),
            c_axis,
        ]
    ).lower()
    best: dict[str, Any] | None = None
    best_score = -1
    for sp in series_parents:
        sid = str(sp.get("id") or "")
        score = 0
        if c_axis and c_axis == str(sp.get("ux_axis") or ""):
            score += 3
        if c_face and c_face == str(sp.get("catalog_face") or ""):
            score += 2
        if c_dim and c_dim == str(sp.get("dimension") or ""):
            score += 2
        # Keyword overlap with parent summary (catches dual-rail claims)
        p_blob = f"{sp.get('label') or ''} {sp.get('summary') or ''}".lower()
        for token in (
            "worldcam",
            "mapcam",
            "sensorium",
            "pilot",
            "scry",
            "dominate",
            "absent",
            "quiet",
            "combat",
            "legacy",
            "off-screen",
            "offscreen",
            "faction",
            "mod",
            "worldgen",
        ):
            if token in c_blob and token in p_blob:
                score += 4
        if sid in _VACUUM_PARENTS:
            score -= 2  # prefer specific parents over power-band dumps
        if score > best_score:
            best_score = score
            best = sp
    return best if best_score > 0 else (series_parents[0] if series_parents else None)


def relens_mint_children(
    vault_root: Path,
    project_id: str,
    *,
    rewrite_summaries: bool = True,
) -> dict[str, Any]:
    """Re-apply series lens (affinity-aware) to non-series backlog items."""
    vault_root = vault_root.resolve()
    bl = load_mint_backlog(vault_root, project_id)
    items = [i for i in (bl.get("items") or []) if isinstance(i, dict)]
    parents = [
        i for i in items if str(i.get("walk_tier") or "") == "series" and str(i.get("status") or "") != "dropped"
    ]
    moved: list[dict[str, str]] = []
    for it in items:
        if str(it.get("walk_tier") or "") == "series":
            continue
        old = str(it.get("parent_id") or "")
        parent = _lens_parent_for_child(it, parents)
        if not parent:
            continue
        new = str(parent.get("id") or "")
        if new and new != old:
            moved.append({"id": str(it.get("id")), "from": old, "to": new})
            it["parent_id"] = new
            # Dual-rail inherit flag — do NOT clone parent does_not_mandate onto the child
            _normalize_child_anti_mandate_surface(it, parent)
            notes = str(it.get("notes") or "")
            notes = re.sub(r";?\s*lensed_by:[^\s;]+", "", notes).strip("; ").strip()
            it["notes"] = f"{notes}; lensed_by:{new}; relens:affinity".strip("; ")
            if rewrite_summaries:
                it["summary"] = _contract_child_summary(it, parent)
                it["mint_lane"] = "validate_batch"
                it["content_rewrite"] = "contract_v1_relens"
    bl["items"] = _rank_items(items)
    bl["children_relensed"] = True
    write_mint_backlog(vault_root, project_id, bl)
    return {
        "ok": True,
        "detail": "children_relensed",
        "moved_count": len(moved),
        "moved": moved,
        **backlog_summary(vault_root, project_id),
    }


def _list_field_as_strs(raw: Any) -> list[str]:
    if isinstance(raw, list):
        return [str(x).strip() for x in raw if str(x).strip()]
    if isinstance(raw, str) and raw.strip():
        try:
            parsed = yaml.safe_load(raw)
            if isinstance(parsed, list):
                return [str(x).strip() for x in parsed if str(x).strip()]
        except Exception:
            pass
        return [raw.strip()]
    return []


def _draft_child_local_alternatives(
    item: dict[str, Any],
    parent: dict[str, Any] | None = None,
) -> list[str]:
    """
    First-pass local alternatives_not_banned from child identity.
    Prefer structure menus; do not invent local bans.
    """
    iid = str(item.get("id") or "").strip()
    mode = str(item.get("experience_mode") or item.get("ux_family") or "").strip().lower()
    label = str(item.get("label") or iid).strip().lower()
    summary = str(item.get("summary") or "").lower()
    blob = f"{iid} {mode} {label} {summary}"

    # Known camera / agency envelopes
    keyed: dict[str, list[str]] = {
        "ux_absent_proxy": [
            "Volunteer delegate vs DM-proposed vote for who holds the stick",
            "Soft revoke on owner return vs hard cutover with table ack",
        ],
        "ux_agency_handoff_enter_exit": [
            "Sparse vs rich transfer chrome at enter/exit",
            "Quiet stick-pass vs announced table beat",
        ],
        "ux_baseline_fp": [
            "Minimal HUD vs richer diegetic embodiment chrome",
            "Strict FP-only default vs rare comfort assists that still restore to FP",
        ],
        "ux_baseline_fp_controls": [
            "Gesture-light vs denser intent surfaces in FP",
            "Look-then-act vs simultaneous look/move issuance",
        ],
        "ux_divination_override": [
            "Sparse vs frequent rules-bound remote-sense use",
            "Thin scry pane vs fuller remote presentation that still hard-restores",
        ],
        "ux_dm_mapcam": [
            "Measurement-first MapCam vs token/fog-first layout",
            "Rare MapCam dips vs frequent grid adjudication",
        ],
        "ux_dm_pilot": [
            "Session-policy DM pilot vs rules-triggered only",
            "Brief pilot envelopes vs longer possession-like duration (still restore)",
        ],
        "ux_dm_sensorium": [
            "Strict read-only bind vs annotated LOS helpers that never transfer intent",
            "Short Sensorium peeks vs sustained watch",
        ],
        "ux_dm_worldcam": [
            "DM who rarely leaves WorldCam vs frequent MapCam/Sensorium/pilot use",
            "Comfort-smooth WorldCam motion vs snappy cuts (final state still explicit)",
        ],
        "ux_dominate_pilot": [
            "Thin vs fuller dominate-pilot embodiment in early builds",
            "Strict rules-duration vs session-extended pilot that still hard-restores",
        ],
        "ux_dominate_victim": [
            "Sparse vs rich passenger / liminal chrome for the victim",
            "Locked-input only vs light passenger cues without restoring control early",
        ],
        "ux_liminal_unconscious": [
            "Sparse vs rich liminal/unconscious presentation",
            "Hard blackout vs soft liminal that still returns to baseline",
        ],
        "ux_planar_travel_override": [
            "Brief gate flash vs longer planar transition presentation",
            "Rules-only planar departures vs session-flavored transitions (still restore)",
        ],
        "ux_chronicle_buckets": [
            "Strict three-bucket separation vs soft merged chronicle views",
            "Thin personal archive vs richer searchable chronicle",
        ],
        "ux_class_chrome_discovery": [
            "Optional vs always-on identity chrome in the embodied moment",
            "Sparse diegetic notice vs explicit class/identity recognition surface",
        ],
        "ux_player_lite_lore_gui": [
            "Minimal inbox+Legacies vs fuller recap/chronicle chrome",
            "Read-mostly vs light intent-propose without DM-write power",
        ],
        "ux_session0_bootstrap": [
            "Thin collaborative seed vs DM-solo then reveal",
            "Minimal bounds-only vs deep intent+canon pass",
        ],
        "ux_session_onboarding": [
            "First-run product onboarding vs returning-session warm start",
            "Preference-light vs identity-tone-heavy ritual",
        ],
        "ux_tone_profile_surface": [
            "Four core profiles only vs profiles + optional modifiers",
            "Tone as soft bias vs stronger subsystem weighting (still not siloed presets)",
        ],
        "ux_application_shell": [
            "Sparse region map vs denser chrome stacking",
            "Shared shell for both seats vs seat-aware region packs (still one product)",
        ],
        "ux_primary_navigation": [
            "Menu/route-primary vs spatial/world wayfinding-primary",
            "Flat top-level destinations vs deep hierarchical breadcrumbs",
        ],
    }
    if iid in keyed:
        return keyed[iid][:4]

    # Generic coverage draft from keywords
    alts: list[str] = []
    if "faction" in blob:
        alts = [
            "Off-screen faction tick sparse vs dense",
            "Player-visible residue only vs DM machinery exposed",
        ]
    elif "npc" in blob:
        alts = [
            "Thin NPC sheet vs richer agenda/secret surfaces",
            "Dialogue-hook light vs dense relationship graph",
        ]
    elif "economy" in blob or "trade" in blob:
        alts = [
            "Abstract resource pressure vs detailed trade routes",
            "Background economy vs player-facing market surfaces",
        ]
    elif "worldgen" in blob or "author" in blob:
        alts = [
            "Guided wizard vs power-user authoring surface",
            "Procedural-first vs hand-authored seed bias",
        ]
    elif "application_shell" in blob or (
        "shell" in blob and "navigation" not in blob and "nav" not in blob
    ):
        alts = [
            "Sparse region map vs denser chrome stacking",
            "Shared shell for both seats vs seat-aware region packs (still one product)",
        ]
    elif "primary_navigation" in blob or "navigation" in blob or "wayfinding" in blob:
        alts = [
            "Menu/route-primary vs spatial/world wayfinding-primary",
            "Flat top-level destinations vs deep hierarchical breadcrumbs",
        ]
    elif "combat" in blob or "cast" in blob:
        alts = [
            "Sparse cast feedback vs richer combat telegraph chrome",
            "Rules-tight feedback vs cinematic optional skins",
        ]
    elif "session0" in blob or "session_0" in blob or "bootstrap" in blob:
        alts = [
            "Thin collaborative seed vs DM-solo then reveal",
            "Minimal bounds-only vs deep intent+canon pass",
        ]
    elif "onboard" in blob:
        alts = [
            "First-run product onboarding vs returning-session warm start",
            "Preference-light vs identity-tone-heavy ritual",
        ]
    elif "tone" in blob:
        alts = [
            "Four core profiles only vs profiles + optional modifiers",
            "Tone as soft bias vs stronger subsystem weighting (still not siloed presets)",
        ]
    elif "session" in blob:
        alts = [
            "First-run product onboarding vs returning-session warm start",
            "Thin collaborative seed vs DM-solo then reveal",
        ]
    elif "canon" in blob or "quest" in blob or "weather" in blob or "sim" in blob:
        alts = [
            "Quiet background sim vs more visible pressure ticks",
            "DM-only machinery vs player-readable residue on return",
        ]
    elif "chronicle" in blob or "legacy" in blob or "lore_gui" in blob or "chrome" in blob:
        alts = [
            "Minimal player-lite inbox vs fuller recap/chronicle chrome",
            "Thin personal archive vs richer searchable chronicle buckets",
        ]
    else:
        plabel = str((parent or {}).get("label") or "parent").strip()
        alts = [
            f"Sparse vs rich presentation under {plabel}",
            f"Minimal vs fuller control surface under {plabel} (still not a single AP default)",
        ]
    return alts[:4]


def _normalize_child_anti_mandate_surface(
    item: dict[str, Any],
    parent: dict[str, Any] | None,
    *,
    draft_alternatives_if_missing: bool = True,
) -> dict[str, Any]:
    """
    Child card: inherits_parent_anti_mandate + local alternatives_not_banned.
    Strip cloned parent does_not_mandate; keep only true local ban deltas.
    """
    parent_anti = _list_field_as_strs((parent or {}).get("does_not_mandate"))
    child_anti = _list_field_as_strs(item.get("does_not_mandate"))
    # Cloned parent list → clear and inherit
    if parent_anti and child_anti == parent_anti:
        item["does_not_mandate"] = []
        item["inherits_parent_anti_mandate"] = True
    elif parent_anti and child_anti:
        # Keep only deltas not on parent
        deltas = [x for x in child_anti if x not in parent_anti]
        item["does_not_mandate"] = deltas
        item["inherits_parent_anti_mandate"] = True
    elif parent and str(item.get("parent_id") or "").strip():
        item["inherits_parent_anti_mandate"] = True
        if not child_anti:
            item["does_not_mandate"] = []
    else:
        item.setdefault("inherits_parent_anti_mandate", False)

    alts = _list_field_as_strs(item.get("alternatives_not_banned"))
    if draft_alternatives_if_missing and len(alts) < 2:
        item["alternatives_not_banned"] = _draft_child_local_alternatives(item, parent)
    elif alts:
        item["alternatives_not_banned"] = alts
    return item


def _apply_series_lens(child: dict[str, Any], parent: dict[str, Any]) -> dict[str, Any]:
    out = dict(child)
    out["parent_id"] = str(parent.get("id") or "")
    out["mint_lane"] = out.get("mint_lane") or "cursor_draft"
    out["depth_band"] = out.get("depth_band") if out.get("depth_band") is not None else 1
    _normalize_child_anti_mandate_surface(out, parent, draft_alternatives_if_missing=True)
    notes = str(out.get("notes") or "").strip()
    lens = f"lensed_by:{parent.get('id')}"
    out["notes"] = f"{notes}; {lens}".strip("; ") if notes else lens
    return out


def series_draft_paths(vault_root: Path, project_id: str) -> tuple[Path, Path]:
    us = user_story_paths(vault_root, project_id)["catalog"].parent
    return us / "SERIES-DRAFT.yaml", us / "SERIES-DRAFT.md"


def write_series_draft_stub(
    vault_root: Path,
    project_id: str,
    *,
    archive_ref: str = "",
) -> dict[str, Any]:
    """
    Phase 0 stub: dump current series packs into SERIES-DRAFT for operator prune.
    Cursor indexer may rewrite before accept.
    """
    from .ux_mint_series import load_ux_mint_series

    vault_root = vault_root.resolve()
    series_doc = load_ux_mint_series(vault_root, project_id)
    ypath, mpath = series_draft_paths(vault_root, project_id)
    ypath.parent.mkdir(parents=True, exist_ok=True)
    draft = {
        "schema_version": 1,
        "project_id": project_id,
        "status": "proposed",
        "archive_ref": archive_ref or "",
        "generated_at": _utc_now(),
        "note": "Cursor proposes; operator accepts → UX-MINT-SERIES.project.yaml + series_draft_accepted",
        "packs": series_doc.get("packs") or [],
        "enabled_pack_ids": series_doc.get("enabled_pack_ids") or [],
    }
    save_yaml(ypath, draft)
    lines = [
        f"# SERIES-DRAFT — `{project_id}`",
        "",
        "Phase 0 series proposal. Accept → promote overlay / set `series_draft_accepted` on backlog.",
        "",
        f"- archive_ref: `{archive_ref or '(none)'}`",
        f"- packs: `{len(draft['packs'])}`",
        f"- machine: `SERIES-DRAFT.yaml`",
        "",
    ]
    mpath.write_text("\n".join(lines), encoding="utf-8")
    return {
        "ok": True,
        "detail": "series_draft_written",
        "path": str(ypath.relative_to(vault_root)),
        "md_path": str(mpath.relative_to(vault_root)),
        "pack_count": len(draft["packs"]),
    }


def accept_series_draft(
    vault_root: Path,
    project_id: str,
    *,
    waive: bool = False,
) -> dict[str, Any]:
    """Mark series draft accepted on backlog (creates empty proposed backlog if missing)."""
    vault_root = vault_root.resolve()
    bl = load_mint_backlog(vault_root, project_id)
    if not bl.get("project_id"):
        bl["project_id"] = project_id
    bl["series_draft_accepted"] = True
    if waive:
        bl["waive_series_draft"] = True
    bl["mint_phase"] = str(bl.get("mint_phase") or "series_draft")
    if bl["mint_phase"] == "series_draft":
        bl["mint_phase"] = "series_walk"
    write_mint_backlog(vault_root, project_id, bl)
    return {"ok": True, "detail": "series_draft_accepted", **backlog_summary(vault_root, project_id)}


def publish_series_trinity(
    vault_root: Path,
    project_id: str,
    *,
    trinity_ref: str,
    emit_pack: bool = True,
) -> dict[str, Any]:
    """
    Gate: all series done + record Grok-facing Trinity/GitHub ref.
    Caller runs weave_public_sync; pass resulting commit/ref as trinity_ref.
    """
    vault_root = vault_root.resolve()
    bl = load_mint_backlog(vault_root, project_id)
    items = [i for i in (bl.get("items") or []) if isinstance(i, dict)]
    done_ok, pending = assert_all_series_done(items)
    if not done_ok:
        return {
            "ok": False,
            "detail": "series_incomplete",
            "pending_series_ids": pending,
        }
    ref = str(trinity_ref or "").strip()
    if not ref:
        return {"ok": False, "detail": "trinity_ref_required"}
    pack_out: dict[str, Any] = {}
    if emit_pack:
        from .catalog_mint_pack import emit_catalog_mint_pack

        pack = emit_catalog_mint_pack(vault_root, project_id=project_id)
        pack_out = pack.to_dict()
        if not pack.ok:
            return {"ok": False, "detail": "pack_emit_failed", "pack": pack_out}
    bl["series_published_trinity_ref"] = ref
    bl["mint_phase"] = "series_locked"
    write_mint_backlog(vault_root, project_id, bl)
    return {
        "ok": True,
        "detail": "series_published_trinity",
        "series_published_trinity_ref": ref,
        "pack": pack_out,
        **backlog_summary(vault_root, project_id),
    }


_SUMMARY_RESIDUE_MARKERS = (
    "Feedstock:",
    "Nearest context:",
    "## maps_to",
    "maps_to_taxonomy",
    "Pillars:",
    "exploration: (infer",
    "combat: mentioned in feedstock",
    "roleplay: (infer",
)


def _summary_has_residue(text: str) -> bool:
    s = str(text or "")
    if any(m in s for m in _SUMMARY_RESIDUE_MARKERS):
        return True
    if "- label:" in s and "summary:" in s.lower():
        return True
    return False


def _strip_summary_residue(text: str) -> str:
    """Keep product-contract prose; drop harvest evidence glued onto summary."""
    s = str(text or "").replace("\n", " ").strip()
    if not s:
        return ""
    cut_at = len(s)
    for marker in (
        " Feedstock:",
        "Feedstock:",
        " Nearest context:",
        "Nearest context:",
        " ## maps_to",
        "## maps_to",
        " maps_to_taxonomy",
        " Pillars:",
        "Pillars:",
    ):
        idx = s.find(marker)
        if idx != -1:
            cut_at = min(cut_at, idx)
    s = s[:cut_at].strip()
    # Drop leading [gap] machine prefix from walk-facing text
    s = re.sub(r"^\[gap\]\s*", "", s).strip()
    s = re.sub(r"\s+", " ", s)
    return s


def _contract_child_summary(
    item: dict[str, Any],
    parent: dict[str, Any] | None,
) -> str:
    """Rewrite child summary into clean capability-contract language under parent."""
    label = str(item.get("label") or item.get("id") or "Capability").strip()
    raw = str(item.get("summary") or "")
    clean = _strip_summary_residue(raw)
    # Drop stacked "(under …)" clauses from prior relens/rewrite before adding one
    clean = re.sub(r"\s*\(under [^)]*\)\s*", " ", clean)
    clean = re.sub(r"\s+", " ", clean).strip().rstrip(" .")
    if clean:
        clean = clean + "."
    parent_label = str((parent or {}).get("label") or (parent or {}).get("id") or "").strip()
    # If still empty/short/dirty, synthesize a contract from label + parent lens
    if len(clean) < 48 or _summary_has_residue(clean):
        if parent_label:
            clean = (
                f"{label.rstrip('.')} — table-facing capability under "
                f"{parent_label}; structure menu, not a single AP scene default."
            )
        else:
            clean = (
                f"{label.rstrip('.')} — table-facing capability contract; "
                "structure menu, not a single AP scene default."
            )
    # Single parent clause only
    elif parent_label and f"(under {parent_label})" not in clean and len(clean) < 280:
        clean = f"{clean.rstrip('.')} (under {parent_label})."
    return clean[:520].strip()


def rewrite_mint_children(
    vault_root: Path,
    project_id: str,
    *,
    only_pending: bool = True,
) -> dict[str, Any]:
    """
    Stage between children harvest and Grok validate: strip feedstock residue from
    walk-facing summaries; move evidence into notes; mint_lane → validate_batch.
    """
    vault_root = vault_root.resolve()
    bl = load_mint_backlog(vault_root, project_id)
    ok, reason = assert_series_published_for_children(bl)
    if not ok:
        return {"ok": False, "detail": reason}
    items = [i for i in (bl.get("items") or []) if isinstance(i, dict)]
    parents = {
        str(i.get("id") or ""): i
        for i in items
        if str(i.get("walk_tier") or "") == "series"
    }
    rewritten = 0
    skipped = 0
    for it in items:
        if str(it.get("walk_tier") or "") == "series":
            continue
        st = str(it.get("status") or "pending")
        if only_pending and st not in {"pending", "in_dialogue", "validate_batch"}:
            skipped += 1
            continue
        parent = parents.get(str(it.get("parent_id") or ""))
        old_summary = str(it.get("summary") or "")
        new_summary = _contract_child_summary(it, parent)
        # Preserve residue into notes once
        if _summary_has_residue(old_summary) or old_summary != new_summary:
            notes = str(it.get("notes") or "").strip()
            if _summary_has_residue(old_summary) and "feedstock_excerpt:" not in notes:
                excerpt = old_summary
                for marker in ("Feedstock:", "Nearest context:"):
                    if marker in excerpt:
                        excerpt = excerpt.split(marker, 1)[-1].strip()
                        break
                excerpt = excerpt[:400]
                bit = f"pre_rewrite_summary_residue: {excerpt}"
                it["notes"] = f"{notes}; {bit}".strip("; ") if notes else bit
            it["summary"] = new_summary
            rewritten += 1
        else:
            it["summary"] = new_summary
            rewritten += 1
        it["mint_lane"] = "validate_batch"
        it["content_rewrite"] = "contract_v1"
        _normalize_child_anti_mandate_surface(it, parent, draft_alternatives_if_missing=True)
    bl["items"] = _rank_items(items)
    bl["children_rewritten"] = True
    bl["mint_phase"] = "children_batch"
    bl["harvest_pass"] = "children"
    qv = str(bl.get("quality_validation") or "")
    note = (
        "children_rewrite_applied — walk-facing child summaries distilled to "
        "product-contract language; feedstock kept in notes. Grok+user still validate batches."
    )
    if "children_rewrite_applied" not in qv:
        bl["quality_validation"] = f"{qv} | {note}".strip(" |")
    bl["quality_validation_status"] = "children_rewritten_awaiting_grok_validate"
    write_mint_backlog(vault_root, project_id, bl)
    return {
        "ok": True,
        "detail": "children_rewritten",
        "rewritten_count": rewritten,
        "skipped_count": skipped,
        **backlog_summary(vault_root, project_id),
    }


def greenlight_children(vault_root: Path, project_id: str) -> dict[str, Any]:
    vault_root = vault_root.resolve()
    bl = load_mint_backlog(vault_root, project_id)
    ok, reason = assert_series_published_for_children(bl)
    if not ok:
        return {"ok": False, "detail": reason}
    # Prefer rewrite before greenlight walk; auto-run if missing
    if not bool(bl.get("children_rewritten")):
        rw = rewrite_mint_children(vault_root, project_id)
        if not rw.get("ok"):
            return rw
        bl = load_mint_backlog(vault_root, project_id)
    bl["children_greenlit"] = True
    bl["mint_phase"] = "children_batch"
    write_mint_backlog(vault_root, project_id, bl)
    return {"ok": True, "detail": "children_greenlit", **backlog_summary(vault_root, project_id)}


def publish_children_trinity(
    vault_root: Path,
    project_id: str,
    *,
    trinity_ref: str,
    emit_pack: bool = True,
) -> dict[str, Any]:
    vault_root = vault_root.resolve()
    bl = load_mint_backlog(vault_root, project_id)
    if not bool(bl.get("children_greenlit")):
        return {"ok": False, "detail": "children_not_greenlit"}
    ref = str(trinity_ref or "").strip()
    if not ref:
        return {"ok": False, "detail": "trinity_ref_required"}
    pack_out: dict[str, Any] = {}
    if emit_pack:
        from .catalog_mint_pack import emit_catalog_mint_pack

        pack = emit_catalog_mint_pack(vault_root, project_id=project_id)
        pack_out = pack.to_dict()
        if not pack.ok:
            return {"ok": False, "detail": "pack_emit_failed", "pack": pack_out}
    bl["children_published_trinity_ref"] = ref
    write_mint_backlog(vault_root, project_id, bl)
    return {
        "ok": True,
        "detail": "children_published_trinity",
        "children_published_trinity_ref": ref,
        "pack": pack_out,
        **backlog_summary(vault_root, project_id),
    }


def child_batch_status_path(vault_root: Path, project_id: str) -> Path:
    return user_story_paths(vault_root, project_id)["catalog"].parent / "CHILD-BATCH-STATUS.md"


def _parent_child_counts(doc: dict[str, Any], parent_id: str) -> tuple[int, int, int]:
    """Return (done, pendingish, total) for coverage children under parent."""
    done = pendingish = total = 0
    for it in doc.get("items") or []:
        if not isinstance(it, dict):
            continue
        if str(it.get("walk_tier") or "") == "series":
            continue
        if str(it.get("parent_id") or "").strip() != parent_id:
            continue
        total += 1
        st = str(it.get("status") or "")
        if st == "done":
            done += 1
        elif st in {"pending", "in_dialogue"}:
            pendingish += 1
    return done, pendingish, total


def render_child_batch_status_markdown(doc: dict[str, Any]) -> str:
    """Harness-owned board for locked vs active same-width batches."""
    pid = str(doc.get("project_id") or "").strip() or "project"
    locked = [str(x) for x in (doc.get("locked_child_batches") or [])]
    active = str(doc.get("active_child_batch") or doc.get("next_child_batch") or "").strip()
    lines = [
        "---",
        f"title: Child batch status — {pid}",
        f"project-id: {pid}",
        "---",
        "",
        "# Child batch status",
        "",
        "**Source of truth for Grok:** this note + `MINT-BACKLOG` frontmatter "
        "(`locked_child_batches`, `active_child_batch`). Ignore chat tables that still say a locked batch is in flight.",
        "",
        "**Walk layout:** Meaning cards under `scopes/`: `SERIES.md` + "
        "`children-of-<parent>/<child>/WALK.md`. Pass B opens **`BATCH-DIGEST.md`** under the active parent first "
        "(full `WALK.md` only for yellow/red/thin). Law: `Docs/catalog-mint/_shared/CHILD-BATCH-VALIDATION.md`.",
        "",
        "## Locked",
        "",
    ]
    if locked:
        for parent in locked:
            done, _pend, total = _parent_child_counts(doc, parent)
            lines.append(
                f"- `{parent}` — **{done}/{total} done**  "
                f"Dirs: `scopes/{parent}/children-of-{parent}/` · digest: `scopes/{parent}/BATCH-DIGEST.md`"
            )
    else:
        lines.append("- _(none)_")
    lines.extend(["", "## Open (same-width) — suggested order", ""])
    lines.append("| # | Parent | Pending | Status |")
    lines.append("|---|--------|---------|--------|")
    # Ordered open parents: pending batches by size, then any active with zero pending
    batches = pending_child_batches(doc)
    seen: set[str] = set()
    rows: list[tuple[str, int, str]] = []
    for parent, kids in batches:
        if parent in locked:
            continue
        status = "**ACTIVE**" if parent == active else "queued"
        rows.append((parent, len(kids), status))
        seen.add(parent)
    if active and active not in seen and active not in locked:
        _d, pend, _t = _parent_child_counts(doc, active)
        rows.insert(0, (active, pend, "**ACTIVE**"))
        seen.add(active)
    if not rows:
        lines.append("| — | _(none open)_ | 0 | — |")
    else:
        for i, (parent, pend, status) in enumerate(rows, start=1):
            hint = f" — `scopes/{parent}/BATCH-DIGEST.md`" if "ACTIVE" in status else ""
            lines.append(f"| {i} | `{parent}` | {pend} | {status}{hint} |")
    nxt = None
    active = str(doc.get("active_child_batch") or doc.get("next_child_batch") or "").strip()
    if active:
        for it in _rank_items([i for i in (doc.get("items") or []) if isinstance(i, dict)]):
            if str(it.get("walk_tier") or "") == "series":
                continue
            if str(it.get("parent_id") or "").strip() != active:
                continue
            if str(it.get("status") or "") in {"pending", "in_dialogue"}:
                nxt = it
                break
    if nxt is None and not active:
        nxt = next_pending_item(doc)
    if nxt:
        lines.extend(
            [
                "",
                f"**Next pending noun (within active batch):** `{nxt.get('id')}` "
                f"(parent `{nxt.get('parent_id') or ''}`)",
            ]
        )
    elif active:
        _d, pend, total = _parent_child_counts(doc, active)
        lines.extend(
            [
                "",
                f"**Active batch `{active}`:** {total - pend}/{total} done — "
                f"re-validate via `scopes/{active}/BATCH-DIGEST.md` "
                f"(no pending nouns; open digest for Pass B receipt).",
            ]
        )
    lines.extend(
        [
            "",
            "Early/mid-game are **not** separate child batches (DM pilot → camera; WA dump → living-world).",
            "",
        ]
    )
    return "\n".join(lines)


def write_child_batch_status(vault_root: Path, project_id: str, doc: dict[str, Any]) -> Path:
    path = child_batch_status_path(vault_root, project_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_child_batch_status_markdown(doc), encoding="utf-8")
    return path


def emit_child_batch_digest(vault_root: Path, project_id: str) -> dict[str, Any]:
    """Refresh BATCH-DIGEST.md files + child batch board without locking."""
    vault_root = vault_root.resolve()
    bl = load_mint_backlog(vault_root, project_id)
    if not bool(bl.get("walk_defs_split")):
        bl = split_backlog_doc_to_walk_dirs(vault_root, project_id, bl)
    paths = sync_batch_digests(vault_root, project_id, bl)
    board = write_child_batch_status(vault_root, project_id, bl)
    write_mint_backlog(vault_root, project_id, bl)
    return {
        "ok": True,
        "detail": "child_batch_digest_emitted",
        "digest_count": len(paths),
        "digest_paths": [str(p.relative_to(vault_root)) for p in paths],
        "board": str(board.relative_to(vault_root)),
        **backlog_summary(vault_root, project_id),
    }


def lock_child_batch(
    vault_root: Path,
    project_id: str,
    *,
    parent_id: str | None = None,
    emit_pack: bool = True,
) -> dict[str, Any]:
    """Lock a same-width child batch after all children are done; advance active."""
    vault_root = vault_root.resolve()
    bl = load_mint_backlog(vault_root, project_id)
    parent = str(parent_id or bl.get("active_child_batch") or bl.get("next_child_batch") or "").strip()
    if not parent:
        return {"ok": False, "detail": "parent_id_required"}
    locked = [str(x) for x in (bl.get("locked_child_batches") or [])]
    if parent in locked:
        return {"ok": False, "detail": "batch_already_locked", "parent_id": parent}
    children = [
        it
        for it in (bl.get("items") or [])
        if isinstance(it, dict)
        and str(it.get("walk_tier") or "") != "series"
        and str(it.get("parent_id") or "").strip() == parent
    ]
    if not children:
        return {"ok": False, "detail": "no_children_under_parent", "parent_id": parent}
    not_done = [
        str(it.get("id") or "")
        for it in children
        if str(it.get("status") or "") != "done"
    ]
    if not_done:
        return {
            "ok": False,
            "detail": "children_not_all_done",
            "parent_id": parent,
            "not_done": not_done,
            "hint": "Mark greens done after batch receipt; re-scope yellow/red first.",
        }
    locked.append(parent)
    bl["locked_child_batches"] = locked
    # Advance to next largest pending parent not locked
    batches = pending_child_batches(bl)
    next_parent = ""
    for pid, _kids in batches:
        if pid not in locked and pid != parent:
            next_parent = pid
            break
    bl["active_child_batch"] = next_parent
    bl["next_child_batch"] = next_parent
    write_mint_backlog(vault_root, project_id, bl)
    write_child_batch_status(vault_root, project_id, bl)
    pack_out: dict[str, Any] = {}
    if emit_pack:
        from .catalog_mint_pack import emit_catalog_mint_pack

        pack = emit_catalog_mint_pack(vault_root, project_id=project_id)
        pack_out = pack.to_dict()
        if not pack.ok:
            return {
                "ok": False,
                "detail": "pack_emit_failed",
                "parent_id": parent,
                "pack": pack_out,
            }
    return {
        "ok": True,
        "detail": "child_batch_locked",
        "parent_id": parent,
        "locked_child_batches": locked,
        "active_child_batch": next_parent,
        "pack": pack_out,
        **backlog_summary(vault_root, project_id),
    }


def freeze_mint_backlog(vault_root: Path, project_id: str) -> dict[str, Any]:
    vault_root = vault_root.resolve()
    bl = load_mint_backlog(vault_root, project_id)
    items = [i for i in (bl.get("items") or []) if isinstance(i, dict)]
    draft_ok, draft_reason = assert_series_draft_for_freeze(bl)
    if not draft_ok:
        return {
            "ok": False,
            "detail": draft_reason,
            "hint": "Run UX_MINT_BACKLOG action: accept_series_draft (or set waive_series_draft).",
            "backlog_status": bl.get("backlog_status"),
        }
    harvest_pass = str(bl.get("harvest_pass") or "series")
    mint_phase = str(bl.get("mint_phase") or "series_walk")
    # Series-first freeze: anti-mandate only. Full taxonomy coverage waits for children pass.
    require_coverage = harvest_pass in {"children", "full"} or mint_phase in {
        "children_greenlit",
        "children_batch",
        "post_mint",
    }
    waived = [str(a) for a in (bl.get("waived_axes") or [])]
    if require_coverage:
        cov_ok, missing = assert_backlog_coverage(vault_root, project_id, items, waived=waived)
        if not cov_ok:
            return {
                "ok": False,
                "detail": "coverage_gap",
                "missing_axes": list(missing),
                "backlog_status": bl.get("backlog_status"),
            }
    alt_ok, alt_gaps = assert_series_freeze_gates(items)
    if not alt_ok:
        return {
            "ok": False,
            "detail": "alternatives_not_banned_gap",
            "missing_alternatives_ids": alt_gaps,
            "backlog_status": bl.get("backlog_status"),
            "hint": "Each series parent needs ≥2 alternatives_not_banned (or ≥2 does_not_mandate) before freeze.",
        }
    bl["backlog_status"] = "frozen_for_mint"
    bl["frozen_at"] = _utc_now()
    if not bl.get("project_id"):
        bl["project_id"] = project_id
    if not bl.get("mint_phase") or bl.get("mint_phase") == "series_draft":
        bl["mint_phase"] = "series_walk"
    path, md_path = write_mint_backlog(vault_root, project_id, bl)
    return {
        "ok": True,
        "detail": "frozen_for_mint",
        "path": str(path.relative_to(vault_root)),
        "md_path": str(md_path.relative_to(vault_root)),
        "backlog_status": "frozen_for_mint",
        "coverage_required": require_coverage,
        **backlog_summary(vault_root, project_id),
    }


def generate_ux_mint_backlog(
    vault_root: Path,
    *,
    project_id: str,
    pmg_path: Path | None = None,
    merge: bool = True,
    harvest_pass: str = "series",
    series_draft_accepted: bool | None = None,
    archive_ref: str | None = None,
) -> UxMintBacklogResult:
    """
    Draft UX backlog — two-pass by default.

    harvest_pass:
      - series: series parents only (Phase A)
      - children: taxonomy/coverage lensed by locked series (requires Trinity series gate)
      - full: legacy series ∪ coverage ∪ thickeners (tests / escape)
    """
    from .ux_mint_taxonomy import (
        collect_ux_mint_feedstock,
        expand_taxonomy_to_items,
        load_ux_mint_taxonomy,
    )
    from .ux_mint_series import (
        expand_series_to_items,
        load_ux_mint_series,
        write_lens_audit,
    )

    vault_root = vault_root.resolve()
    pid = str(project_id or "").strip()
    if not pid:
        return UxMintBacklogResult(
            False, "", "proposed", 0, 0, None, (), False, "project_id_required", (),
            mint_phase="series_draft", harvest_pass="series",
        )

    hp = str(harvest_pass or "series").strip().lower()
    if hp not in HARVEST_PASSES:
        hp = "series"

    path = backlog_path(vault_root, pid)
    md_path = backlog_md_path(vault_root, pid)
    existing: dict[str, Any] = {}
    prior_items: list[dict[str, Any]] = []
    prior_status = "proposed"
    if merge and (path.is_file() or md_path.is_file()):
        existing = load_mint_backlog(vault_root, pid)
        prior_items = [i for i in (existing.get("items") or []) if isinstance(i, dict)]
        prior_status = str(existing.get("backlog_status") or "proposed")

    if hp == "children":
        gate_bl = existing if existing else load_mint_backlog(vault_root, pid)
        ok_gate, reason = assert_series_published_for_children(gate_bl)
        if not ok_gate:
            return UxMintBacklogResult(
                False,
                str(path.relative_to(vault_root)) if path.is_file() else "",
                prior_status,
                len(prior_items),
                0,
                None,
                (),
                False,
                reason,
                (),
                mint_phase=str(gate_bl.get("mint_phase") or "series_walk"),
                harvest_pass=hp,
            )

    cat_path = user_story_paths(vault_root, pid)["catalog"]
    applied: set[str] = set()
    if cat_path.is_file():
        applied = set(catalog_rows_by_id(load_yaml(cat_path)).keys())

    taxonomy = load_ux_mint_taxonomy(vault_root, pid)
    chunks = collect_ux_mint_feedstock(vault_root, pid, pmg_path=pmg_path)
    series_doc = load_ux_mint_series(vault_root, pid)
    series_items = expand_series_to_items(series_doc)
    for it in series_items:
        it["mint_lane"] = "human_grok"
        it.setdefault("fanout", "low")

    harvested: list[dict[str, Any]] = []
    if hp in {"series", "full"}:
        harvested.extend(series_items)

    if hp in {"children", "full"}:
        tax_items = expand_taxonomy_to_items(taxonomy, chunks)
        parents = [
            i
            for i in (series_items if hp == "full" else prior_items + series_items)
            if str(i.get("walk_tier") or "") == "series"
            and str(i.get("status") or "") != "dropped"
        ]
        # Prefer done parents from prior when children pass
        if hp == "children":
            parents = [
                i
                for i in prior_items
                if str(i.get("walk_tier") or "") == "series"
                and str(i.get("status") or "") == "done"
            ] or parents
        for item in tax_items:
            parent = _lens_parent_for_child(item, parents)
            if parent:
                item = _apply_series_lens(item, parent)
            else:
                item["mint_lane"] = "human_grok"
            harvested.append(item)
        if hp == "full":
            supplements = collect_supplement_items(chunks)
            existing_ids = {str(i.get("id") or "") for i in harvested}
            for item in supplements:
                iid = str(item.get("id") or "")
                if str(item.get("derived_from") or "").startswith("actual_play:"):
                    item["walk_tier"] = "thickener"
                    item["supplement"] = True
                    item["altitude"] = item.get("altitude") or "scene_exemplar"
                    item["mint_lane"] = "cursor_draft"
                if iid and iid not in existing_ids:
                    parent = _lens_parent_for_child(item, parents)
                    if parent:
                        item = _apply_series_lens(item, parent)
                    harvested.append(item)
                    existing_ids.add(iid)
        elif hp == "children":
            # Keep prior series rows when merging children
            pass

    for item in harvested:
        if item.get("id") in applied:
            item["status"] = "done"
        if str(item.get("walk_tier") or "") == "series":
            if str(item.get("altitude") or "") != "product_contract":
                item["walk_tier"] = "thickener"
                item["supplement"] = True
            if not str(item.get("derived_from") or "").startswith("series:"):
                item["walk_tier"] = "thickener"
                item["supplement"] = True

    if hp == "children" and merge:
        # Preserve series + prior; merge new children
        series_prior = [
            i for i in prior_items if str(i.get("walk_tier") or "") == "series"
        ]
        merged = _merge_items(series_prior + [
            i for i in prior_items if str(i.get("walk_tier") or "") != "series"
        ], harvested)
    elif merge:
        merged = _merge_items(prior_items, harvested)
    else:
        merged = list(harvested)
    merged = [
        i
        for i in merged
        if not is_rejected_candidate(
            str(i.get("id") or ""),
            str(i.get("label") or ""),
            str(i.get("summary") or ""),
        )
    ]
    if hp == "series" and not merge:
        merged = [i for i in merged if str(i.get("walk_tier") or "") == "series"]
    merged = _rank_items(merged)

    waived = [str(a) for a in (existing.get("waived_axes") or [])]
    if hp == "series":
        cov_ok, missing = True, ()
    else:
        cov_ok, missing = assert_backlog_coverage(vault_root, pid, merged, waived=waived)
    pending = [i for i in merged if str(i.get("status") or "") == "pending"]
    # Phase-aware next — full harvest still walks series first
    if hp == "series":
        tmp_phase, tmp_green, tmp_ref = "series_walk", False, ""
    elif hp == "children":
        tmp_phase, tmp_green, tmp_ref = (
            "children_batch",
            True,
            str(existing.get("series_published_trinity_ref") or "x"),
        )
    else:
        tmp_phase, tmp_green, tmp_ref = "series_walk", False, ""
    tmp_doc = {
        "items": merged,
        "mint_phase": tmp_phase,
        "children_greenlit": tmp_green,
        "series_published_trinity_ref": tmp_ref,
    }
    nxt_item = next_pending_item(tmp_doc)
    nxt = str(nxt_item["id"]) if nxt_item else (str(pending[0]["id"]) if pending else None)

    backlog_status = prior_status if (merge and prior_status == "frozen_for_mint") else "proposed"
    now = _utc_now()

    accepted = existing.get("series_draft_accepted")
    if series_draft_accepted is not None:
        accepted = bool(series_draft_accepted)
    elif accepted is None:
        accepted = False

    mint_phase = str(existing.get("mint_phase") or "series_draft")
    if hp == "series":
        mint_phase = "series_walk" if accepted or existing.get("waive_series_draft") else "series_draft"
    elif hp == "children":
        mint_phase = "children_batch" if existing.get("children_greenlit") else "series_locked"

    doc: dict[str, Any] = {
        "schema_version": 1,
        "project_id": pid,
        "backlog_status": backlog_status,
        "generated_at": now,
        "waived_axes": waived,
        "rubric": "Docs/catalog-mint/_shared/UX-MINT-RUBRIC.md",
        "taxonomy": "Templates/Roadmap/User-Story/UX-MINT-TAXONOMY/manifest.yaml",
        "series": "Templates/Roadmap/User-Story/UX-MINT-SERIES/manifest.yaml",
        "mint_phase": mint_phase,
        "harvest_pass": hp,
        "series_draft_accepted": bool(accepted),
        "waive_series_draft": bool(existing.get("waive_series_draft")),
        "children_greenlit": bool(existing.get("children_greenlit")),
        "items": merged,
    }
    for key in (
        "series_published_trinity_ref",
        "children_published_trinity_ref",
        "archive_ref",
        "quality_validation",
        "quality_validation_status",
    ):
        if archive_ref and key == "archive_ref":
            doc[key] = archive_ref
        elif existing.get(key):
            doc[key] = existing[key]
    if existing.get("frozen_at") and backlog_status == "frozen_for_mint":
        doc["frozen_at"] = existing["frozen_at"]

    path, _md = write_mint_backlog(vault_root, pid, doc)
    write_lens_audit(
        vault_root,
        pid,
        [i for i in merged if str(i.get("walk_tier") or "") == "series"],
        generated_at=now,
    )

    detail = "ux_mint_backlog_written"
    if hp == "series":
        detail = "ux_mint_backlog_series_pass"
    elif hp == "children":
        detail = "ux_mint_backlog_children_pass"
    if hp != "series" and not cov_ok:
        detail = "needs_operator_prune_coverage_gap"
    elif not merged:
        detail = "empty_harvest"

    ok = bool(merged)
    # Children harvest is incomplete without rewrite — distill walk-facing summaries.
    if ok and hp == "children" and str(doc.get("series_published_trinity_ref") or "").strip():
        rw = rewrite_mint_children(vault_root, pid)
        if rw.get("ok"):
            detail = "ux_mint_backlog_children_pass_rewritten"
            bl2 = load_mint_backlog(vault_root, pid)
            pending = [i for i in (bl2.get("items") or []) if str(i.get("status") or "") == "pending"]
            nxt_item = next_pending_item(bl2)
            nxt = str(nxt_item["id"]) if nxt_item else None
            mint_phase = str(bl2.get("mint_phase") or mint_phase)
            item_count = len([i for i in (bl2.get("items") or []) if isinstance(i, dict)])
            return UxMintBacklogResult(
                ok=True,
                path=str(path.relative_to(vault_root)),
                backlog_status=str(bl2.get("backlog_status") or backlog_status),
                item_count=item_count,
                pending_count=len(pending),
                next_pending_id=nxt,
                missing_axes=missing,
                coverage_ok=cov_ok,
                detail=detail,
                proposed_ids=tuple(
                    str(i.get("id")) for i in (bl2.get("items") or []) if isinstance(i, dict) and i.get("id")
                ),
                mint_phase=mint_phase,
                harvest_pass=hp,
            )

    return UxMintBacklogResult(
        ok=ok,
        path=str(path.relative_to(vault_root)),
        backlog_status=backlog_status,
        item_count=len(merged),
        pending_count=len(pending),
        next_pending_id=nxt,
        missing_axes=missing,
        coverage_ok=cov_ok,
        detail=detail,
        proposed_ids=tuple(str(i.get("id")) for i in merged if i.get("id")),
        mint_phase=mint_phase,
        harvest_pass=hp,
    )
