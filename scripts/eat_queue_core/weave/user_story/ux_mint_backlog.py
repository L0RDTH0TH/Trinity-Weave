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
_ITEM_FIELD_RE = re.compile(r"^- (\w+):\s*(.*)$", re.MULTILINE)


def _utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _yaml_list_fm(values: list[str]) -> str:
    if not values:
        return "[]"
    return "[" + ", ".join(str(v) for v in values) + "]"


def render_mint_backlog_markdown(doc: dict[str, Any]) -> str:
    """Render Obsidian-facing MINT-BACKLOG.md from a backlog document."""
    pid = str(doc.get("project_id") or "").strip() or "project"
    status = str(doc.get("backlog_status") or "proposed")
    waived = [str(a) for a in (doc.get("waived_axes") or [])]
    generated = str(doc.get("generated_at") or "")
    frozen = str(doc.get("frozen_at") or "")
    rubric = str(doc.get("rubric") or "Docs/catalog-mint/_shared/UX-MINT-RUBRIC.md")
    items = [i for i in (doc.get("items") or []) if isinstance(i, dict)]

    lines: list[str] = [
        "---",
        f"title: MINT-BACKLOG — {pid}",
        f"project-id: {pid}",
        "para-type: Project",
        f"backlog_status: {status}",
        f"waived_axes: {_yaml_list_fm(waived)}",
        "schema_version: 1",
    ]
    if generated:
        lines.append(f"generated_at: {generated}")
    if frozen:
        lines.append(f"frozen_at: {frozen}")
    lines.extend(
        [
            f"rubric: {rubric}",
            "machine_mirror: MINT-BACKLOG.yaml",
            "---",
            "",
            f"# MINT-BACKLOG — `{pid}`",
            "",
            "Obsidian **operator prune / critique** surface. Edit item fields below "
            "(especially `status`), then harvest/freeze/sync will refresh "
            "`MINT-BACKLOG.yaml` (machine walk queue + Grok pack).",
            "",
            "## Operator gate",
            "",
            "1. Prune: set `status` to `dropped`, or rewrite `label` / `summary` toward experience nouns.",
            "2. Cover or waive required taxonomy slots (see rubric) — missing faces/facets block freeze.",
            "3. When ready: set frontmatter `backlog_status: frozen_for_mint` **or** run "
            "`UX_MINT_BACKLOG` `action: freeze`.",
            "4. Mint walk: Grok takes next `pending` only when frozen (or you name an id).",
            "",
            f"**Current status:** `{status}`  ",
            f"**Waived axes/slots:** `{', '.join(waived) if waived else '(none)'}`  ",
            f"**Rubric:** [[{rubric.replace('.md', '')}|UX mint rubric]]",
            "",
            "## Quick status",
            "",
        ]
    )
    for it in items:
        iid = str(it.get("id") or "").strip()
        if not iid:
            continue
        st = str(it.get("status") or "pending").strip()
        label = str(it.get("label") or iid).strip()
        face = str(it.get("catalog_face") or "")
        mark = "x" if st == "done" else "-" if st == "dropped" else " "
        if st == "in_dialogue":
            mark = " "
        suffix = f" [{face}]" if face else ""
        if it.get("supplement"):
            suffix += " [supplement]"
        lines.append(f"- [{mark}] `{iid}` — {label} (`{st}`){suffix}")
    lines.extend(["", "## Items", ""])

    for it in items:
        iid = str(it.get("id") or "").strip()
        if not iid:
            continue
        label = str(it.get("label") or iid).strip()
        lines.append(f"### `{iid}` — {label}")
        lines.append("")
        for key in (
            "status",
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
            "maps_to",
            "notes",
        ):
            val = it.get(key)
            if val is None:
                val = ""
            text = str(val).replace("\n", " ").strip()
            lines.append(f"- {key}: {text}")
        lines.append("")

    lines.append("## Coverage reminder")
    lines.append("")
    lines.append(
        "Required taxonomy: core + domain pack(s) per `UX-MINT-TAXONOMY/manifest.yaml` "
        "and project `UX-MINT-TAXONOMY.project.yaml`. LLM-feed-first; prune before freeze."
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

    items: list[dict[str, Any]] = []
    headers = list(_ITEM_HEADER_RE.finditer(body))
    for i, match in enumerate(headers):
        iid = match.group(1).strip()
        label_from_h = (match.group(2) or "").strip()
        start = match.end()
        end_pos = headers[i + 1].start() if i + 1 < len(headers) else len(body)
        block = body[start:end_pos]
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
        ):
            if fields.get(extra):
                item[extra] = fields[extra]
        items.append(item)

    doc: dict[str, Any] = {
        "schema_version": int(fm.get("schema_version") or 1),
        "project_id": pid,
        "backlog_status": status,
        "waived_axes": waived,
        "rubric": str(fm.get("rubric") or "Docs/catalog-mint/_shared/UX-MINT-RUBRIC.md"),
        "items": items,
    }
    if fm.get("generated_at"):
        doc["generated_at"] = str(fm["generated_at"])
    if fm.get("frozen_at"):
        doc["frozen_at"] = str(fm["frozen_at"])
    return doc


def write_mint_backlog(vault_root: Path, project_id: str, doc: dict[str, Any]) -> tuple[Path, Path]:
    """Write YAML machine mirror + Obsidian markdown surface."""
    vault_root = vault_root.resolve()
    ypath = backlog_path(vault_root, project_id)
    mpath = backlog_md_path(vault_root, project_id)
    ypath.parent.mkdir(parents=True, exist_ok=True)
    # YAML keeps machine fields only (notes optional)
    yaml_doc = dict(doc)
    save_yaml(ypath, yaml_doc)
    mpath.write_text(render_mint_backlog_markdown(doc), encoding="utf-8")
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
            "mode_tier": "supplement",
            "dnd_pillar": "shared",
            "feedstock_hit": True,
            "pillar_notes": "",
            "supplement": True,
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
                "mode_tier": "supplement",
                "dnd_pillar": "shared",
                "feedstock_hit": True,
                "pillar_notes": "",
                "supplement": True,
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


def collect_supplement_items(chunks: list[tuple[str, str]], *, max_items: int = 80) -> list[dict[str, Any]]:
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
    for ref, text in ordered:
        if len(by_id) >= max_items * 2:
            break
        if ref.startswith("pin:"):
            low = ref.lower()
            if re.search(r"phase[-_]?[1-3]\b", low) and not any(
                k in low for k in ("perspective", "agency", "chrome", "presentation", "hud")
            ):
                continue
        # Headings from phenomenology cards + PMG + pins — not raw research URL noise
        allow_headings = (
            ref.startswith("actual_play:") or ref.startswith("pmg:") or ref.startswith("pin:")
        )
        for item in _seed_from_text(ref, text, allow_headings=allow_headings):
            iid = str(item.get("id") or "")
            if not iid or iid in by_id:
                continue
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

    def key(it: dict[str, Any]) -> tuple[int, int, str, int, str]:
        return (
            1 if it.get("supplement") else 0,
            face_rank.get(str(it.get("catalog_face") or ""), 9),
            str(it.get("experience_mode") or ""),
            pillar_rank.get(str(it.get("dnd_pillar") or ""), 9),
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

    if use_md:
        try:
            data = parse_mint_backlog_markdown(mpath.read_text(encoding="utf-8"))
            if isinstance(data, dict) and data.get("items") is not None:
                if not data.get("project_id"):
                    data["project_id"] = project_id
                return data
        except Exception:
            pass
    if not y_exists:
        return empty
    data = load_yaml(path)
    if not isinstance(data, dict):
        return empty
    return data


def next_pending_item(backlog: dict[str, Any]) -> dict[str, Any] | None:
    for it in backlog.get("items") or []:
        if isinstance(it, dict) and str(it.get("status") or "") == "pending":
            return it
    return None


def backlog_summary(vault_root: Path, project_id: str) -> dict[str, Any]:
    """Surface for loop2 / next-tick — pending count + next id."""
    bl = load_mint_backlog(vault_root, project_id)
    items = [i for i in (bl.get("items") or []) if isinstance(i, dict)]
    pending = [i for i in items if str(i.get("status") or "") == "pending"]
    nxt = pending[0] if pending else None
    return {
        "backlog_status": str(bl.get("backlog_status") or "proposed"),
        "item_count": len(items),
        "pending_count": len(pending),
        "next_pending_id": str(nxt.get("id")) if nxt else None,
        "next_pending_label": str(nxt.get("label")) if nxt else None,
        "path": str(backlog_path(vault_root, project_id).relative_to(vault_root.resolve())),
    }


def freeze_mint_backlog(vault_root: Path, project_id: str) -> dict[str, Any]:
    vault_root = vault_root.resolve()
    bl = load_mint_backlog(vault_root, project_id)
    items = [i for i in (bl.get("items") or []) if isinstance(i, dict)]
    waived = [str(a) for a in (bl.get("waived_axes") or [])]
    cov_ok, missing = assert_backlog_coverage(vault_root, project_id, items, waived=waived)
    if not cov_ok:
        return {
            "ok": False,
            "detail": "coverage_gap",
            "missing_axes": list(missing),
            "backlog_status": bl.get("backlog_status"),
        }
    bl["backlog_status"] = "frozen_for_mint"
    bl["frozen_at"] = _utc_now()
    if not bl.get("project_id"):
        bl["project_id"] = project_id
    path, md_path = write_mint_backlog(vault_root, project_id, bl)
    return {
        "ok": True,
        "detail": "frozen_for_mint",
        "path": str(path.relative_to(vault_root)),
        "md_path": str(md_path.relative_to(vault_root)),
        "backlog_status": "frozen_for_mint",
        **backlog_summary(vault_root, project_id),
    }


def generate_ux_mint_backlog(
    vault_root: Path,
    *,
    project_id: str,
    pmg_path: Path | None = None,
    merge: bool = True,
) -> UxMintBacklogResult:
    """
    Draft thick UX backlog from cross-project taxonomy × feedstock.

    Idempotent merge preserves done/dropped/in_dialogue and frozen_for_mint status.
    Does not auto-write slice-catalog rows. Obsidian edits live in the .md surface.
    """
    from .ux_mint_taxonomy import (
        collect_ux_mint_feedstock,
        expand_taxonomy_to_items,
        load_ux_mint_taxonomy,
    )

    vault_root = vault_root.resolve()
    pid = str(project_id or "").strip()
    if not pid:
        return UxMintBacklogResult(False, "", "proposed", 0, 0, None, (), False, "project_id_required", ())

    path = backlog_path(vault_root, pid)
    md_path = backlog_md_path(vault_root, pid)
    existing: dict[str, Any] = {}
    prior_items: list[dict[str, Any]] = []
    prior_status = "proposed"
    if merge and (path.is_file() or md_path.is_file()):
        existing = load_mint_backlog(vault_root, pid)
        prior_items = [i for i in (existing.get("items") or []) if isinstance(i, dict)]
        prior_status = str(existing.get("backlog_status") or "proposed")

    cat_path = user_story_paths(vault_root, pid)["catalog"]
    applied: set[str] = set()
    if cat_path.is_file():
        applied = set(catalog_rows_by_id(load_yaml(cat_path)).keys())

    taxonomy = load_ux_mint_taxonomy(vault_root, pid)
    chunks = collect_ux_mint_feedstock(vault_root, pid, pmg_path=pmg_path)
    harvested = expand_taxonomy_to_items(taxonomy, chunks)
    # B: union project-specific pin nouns (supplements) — coverage still taxonomy-only
    supplements = collect_supplement_items(chunks)
    tax_ids = {str(i.get("id") or "") for i in harvested}
    for item in supplements:
        iid = str(item.get("id") or "")
        if iid and iid not in tax_ids:
            harvested.append(item)
    for item in harvested:
        if item.get("id") in applied:
            item["status"] = "done"

    merged = _merge_items(prior_items, harvested)
    merged = [
        i
        for i in merged
        if not is_rejected_candidate(
            str(i.get("id") or ""),
            str(i.get("label") or ""),
            str(i.get("summary") or ""),
        )
    ]
    merged = _rank_items(merged)

    waived = [str(a) for a in (existing.get("waived_axes") or [])]
    cov_ok, missing = assert_backlog_coverage(vault_root, pid, merged, waived=waived)
    pending = [i for i in merged if str(i.get("status") or "") == "pending"]
    nxt = str(pending[0]["id"]) if pending else None

    backlog_status = prior_status if prior_status == "frozen_for_mint" else "proposed"

    doc: dict[str, Any] = {
        "schema_version": 1,
        "project_id": pid,
        "backlog_status": backlog_status,
        "generated_at": _utc_now(),
        "waived_axes": waived,
        "rubric": "Docs/catalog-mint/_shared/UX-MINT-RUBRIC.md",
        "taxonomy": "Templates/Roadmap/User-Story/UX-MINT-TAXONOMY/manifest.yaml",
        "items": merged,
    }
    if existing.get("frozen_at") and backlog_status == "frozen_for_mint":
        doc["frozen_at"] = existing["frozen_at"]

    path, _md = write_mint_backlog(vault_root, pid, doc)

    detail = "ux_mint_backlog_written"
    if not cov_ok:
        detail = "needs_operator_prune_coverage_gap"
    elif not merged:
        detail = "empty_harvest"

    ok = bool(merged)
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
    )
