"""UX mint backlog — post-freeze ordered experience nouns for Grok to walk.

Deterministic harvest + axis coverage gate. Does not write slice-catalog rows.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .catalog_io import catalog_rows_by_id, load_yaml, project_root, save_yaml, user_story_paths
from .catalog_mint_propose import _find_pmg_path

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


def _utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


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


def _read_text(path: Path | None) -> str:
    if path is None or not path.is_file():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def _strip_fm(text: str) -> str:
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            return text[end + 4 :].lstrip("\n")
    return text


def _collect_feedstock(vault_root: Path, project_id: str, pmg_path: Path | None) -> list[tuple[str, str]]:
    """Return list of (derived_from_ref, text) chunks."""
    chunks: list[tuple[str, str]] = []
    pmg = pmg_path or _find_pmg_path(vault_root, project_id)
    if pmg and pmg.is_file():
        rel = str(pmg.relative_to(vault_root))
        chunks.append((f"pmg:{rel}", _strip_fm(_read_text(pmg))))

    paths = user_story_paths(vault_root, project_id)
    influence = paths["influence"]
    if influence.is_file():
        chunks.append((f"influence:{influence.relative_to(vault_root)}", _strip_fm(_read_text(influence))))

    roadmap = project_root(vault_root, project_id) / "Roadmap"
    if roadmap.is_dir():
        for p in sorted(roadmap.rglob("*.md")):
            # Prefer Phase 4–6 conceptual notes for UX intents
            name = p.name.lower()
            rel_s = str(p.relative_to(vault_root))
            if "user-story" in rel_s.lower() and p.name.lower() in {
                "influence-deck.md",
                "user-story-state.md",
            }:
                continue
            phase_hit = re.search(r"phase[-_]?([4-6])\b", name) or re.search(
                r"/phase[-_]?([4-6])", rel_s.lower()
            )
            if phase_hit or "conceptual" in name or "perspective" in name or "chrome" in name:
                chunks.append((f"pin:{rel_s}", _strip_fm(_read_text(p))[:8000]))
    return chunks


def _seed_from_text(derived_from: str, text: str) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    seen_axes: set[str] = set()
    for pat, axis, dim, id_stub, label, summary in _THEME_SEEDS:
        if axis in seen_axes and axis != "presentation_shells":
            # one primary seed per axis from a chunk unless shells
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
            "conceptual_pin": "",
            "derived_from": derived_from,
            "ux_family": "",
            "status": "pending",
        }
        if is_rejected_candidate(item["id"], item["label"], item["summary"]):
            continue
        out.append(item)
        seen_axes.add(axis)
    # Headings that look experiential (not Phase N)
    for m in _HEADING_RE.finditer(text):
        title = m.group(1).strip()
        if _PHASE_LABEL_RE.match(title):
            continue
        low = title.lower()
        if not any(h in low for h in EXPERIENTIAL_HINTS):
            continue
        axis = "agency"
        for pat, ax, *_rest in _THEME_SEEDS:
            if pat.search(title):
                axis = ax
                break
        dim = "ui_surface"
        item_id = f"ux_{_slug(title)}"
        if is_rejected_candidate(item_id, title):
            continue
        out.append(
            {
                "id": item_id,
                "label": title[:80],
                "dimension": dim,
                "ux_axis": axis,
                "summary": f"Experience noun from feedstock heading: {title[:120]}",
                "conceptual_pin": "",
                "derived_from": derived_from,
                "ux_family": "",
                "status": "pending",
            }
        )
    return out


def _rank_items(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    axis_rank = {a: i for i, a in enumerate(AXIS_ORDER)}

    def key(it: dict[str, Any]) -> tuple[int, str]:
        ax = str(it.get("ux_axis") or "")
        return (axis_rank.get(ax, 99), str(it.get("id") or ""))

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
            # Preserve operator status/order fields; refresh summary/derived if still pending
            if str(prev.get("status") or "") in {"done", "dropped", "in_dialogue"}:
                continue
            for k in ("label", "dimension", "ux_axis", "summary", "derived_from", "ux_family", "conceptual_pin"):
                if it.get(k) and not prev.get(k):
                    prev[k] = it[k]
            by_id[iid] = prev
        else:
            by_id[iid] = dict(it)
    return _rank_items(list(by_id.values()))


def load_mint_backlog(vault_root: Path, project_id: str) -> dict[str, Any]:
    path = backlog_path(vault_root, project_id)
    if not path.is_file():
        return {
            "schema_version": 1,
            "project_id": project_id,
            "backlog_status": "proposed",
            "waived_axes": [],
            "items": [],
        }
    data = load_yaml(path)
    if not isinstance(data, dict):
        return {"schema_version": 1, "project_id": project_id, "backlog_status": "proposed", "items": []}
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
    cov_ok, missing = assert_ux_axis_coverage(items, waived_axes=waived)
    if not cov_ok:
        return {
            "ok": False,
            "detail": "coverage_gap",
            "missing_axes": list(missing),
            "backlog_status": bl.get("backlog_status"),
        }
    bl["backlog_status"] = "frozen_for_mint"
    bl["frozen_at"] = _utc_now()
    path = backlog_path(vault_root, project_id)
    save_yaml(path, bl)
    return {
        "ok": True,
        "detail": "frozen_for_mint",
        "path": str(path.relative_to(vault_root)),
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
    Harvest UX experience nouns into MINT-BACKLOG.yaml.

    Idempotent merge preserves done/dropped/in_dialogue and frozen_for_mint status.
    Does not auto-write slice-catalog rows.
    """
    vault_root = vault_root.resolve()
    pid = str(project_id or "").strip()
    if not pid:
        return UxMintBacklogResult(False, "", "proposed", 0, 0, None, (), False, "project_id_required", ())

    path = backlog_path(vault_root, pid)
    existing: dict[str, Any] = {}
    prior_items: list[dict[str, Any]] = []
    prior_status = "proposed"
    if merge and path.is_file():
        existing = load_mint_backlog(vault_root, pid)
        prior_items = [i for i in (existing.get("items") or []) if isinstance(i, dict)]
        prior_status = str(existing.get("backlog_status") or "proposed")

    # Avoid duplicate ids already applied in catalog
    cat_path = user_story_paths(vault_root, pid)["catalog"]
    applied: set[str] = set()
    if cat_path.is_file():
        applied = set(catalog_rows_by_id(load_yaml(cat_path)).keys())

    harvested: list[dict[str, Any]] = []
    for derived, text in _collect_feedstock(vault_root, pid, pmg_path):
        for item in _seed_from_text(derived, text):
            if item["id"] in applied:
                item["status"] = "done"
            harvested.append(item)

    merged = _merge_items(prior_items, harvested)
    # Drop rejected after merge
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
    cov_ok, missing = assert_ux_axis_coverage(merged, waived_axes=waived)
    pending = [i for i in merged if str(i.get("status") or "") == "pending"]
    nxt = str(pending[0]["id"]) if pending else None

    # Keep frozen status unless regenerating with explicit unfreeze (not here)
    backlog_status = prior_status if prior_status == "frozen_for_mint" else "proposed"

    doc: dict[str, Any] = {
        "schema_version": 1,
        "project_id": pid,
        "backlog_status": backlog_status,
        "generated_at": _utc_now(),
        "waived_axes": waived,
        "rubric": "Docs/catalog-mint/_shared/UX-MINT-RUBRIC.md",
        "items": merged,
    }
    if existing.get("frozen_at") and backlog_status == "frozen_for_mint":
        doc["frozen_at"] = existing["frozen_at"]

    path.parent.mkdir(parents=True, exist_ok=True)
    save_yaml(path, doc)

    detail = "ux_mint_backlog_written"
    if not cov_ok:
        detail = "needs_operator_prune_coverage_gap"
    elif not merged:
        detail = "empty_harvest"

    ok = bool(merged)  # written; coverage may still fail
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
