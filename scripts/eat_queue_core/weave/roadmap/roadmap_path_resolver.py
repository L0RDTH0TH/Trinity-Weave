"""Deterministic roadmap note paths from subphase-index (canonical § Complete hierarchy)."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Literal

import yaml

from .branch_depth import subphase_index_depth, subphase_index_parts

Track = Literal["conceptual", "execution"]
RoadmapLevel = Literal["primary", "secondary", "tertiary", "quaternary", "task"]

_ROADMAP_STAMP_RE = re.compile(
    r"-Roadmap(?:-\d{4}-\d{2}-\d{2}(?:-\d{4})?)?\.md$"
)
_SKIP_REL_PARTS = (
    "/User-Story/",
    "/Execution/",
    "/Conceptual-Amendments/",
    "/Conceptual-Decision-Records/",
    "/Versions/",
    "/.snapshots/",
)
_STATE_NAMES = frozenset(
    {
        "workflow_state.md",
        "roadmap-state.md",
        "distilled-core.md",
        "decisions-log.md",
    }
)


@dataclass(frozen=True)
class RoadmapPathRequest:
    vault_root: Path
    project_id: str
    subphase_index: str
    title_slug: str = ""
    roadmap_level: str = ""
    track: Track = "conceptual"
    phase_folder_name: str = ""
    secondary_folder_name: str = ""
    timestamp_slug: str = ""


@dataclass
class RoadmapPathResult:
    ok: bool
    rel_dir: str = ""
    rel_path: str = ""
    basename: str = ""
    ensure_dirs: list[str] = field(default_factory=list)
    frontmatter_hints: dict[str, Any] = field(default_factory=dict)
    violations: list[str] = field(default_factory=list)


def load_path_resolver_config(vault_root: Path) -> dict[str, Any]:
    from ...merged_config import load_merged_yaml_blocks

    out: dict[str, Any] = {"path_resolver_enforced": True}
    try:
        blocks = load_merged_yaml_blocks(vault_root)
        roadmap = blocks.get("roadmap")
        if isinstance(roadmap, dict):
            if roadmap.get("path_resolver_enforced") is not None:
                out["path_resolver_enforced"] = bool(roadmap["path_resolver_enforced"])
    except (ImportError, OSError, TypeError, ValueError):
        pass
    return out


def index_path_prefix(parts: list[int]) -> str:
    return "Phase-" + "-".join(str(p) for p in parts)


def slugify_title(title: str) -> str:
    raw = str(title or "").strip()
    raw = re.sub(r"^Phase\s+[\d.]+\s*[—–-]\s*", "", raw, flags=re.I)
    raw = re.sub(r"[^\w\s-]", "", raw)
    raw = re.sub(r"[\s_]+", "-", raw).strip("-")
    return raw or "Untitled"


def slug_from_basename(basename: str, parts: list[int]) -> str:
    name = basename
    if name.endswith(".md"):
        name = name[:-3]
    prefix = index_path_prefix(parts) + "-"
    if not name.startswith(prefix):
        return slugify_title(name)
    rest = name[len(prefix) :]
    if "-Roadmap-" in rest:
        rest = rest.split("-Roadmap-", 1)[0]
    else:
        rest = _ROADMAP_STAMP_RE.sub("", rest)
    return rest.strip("-") or "Roadmap-Slice"


def roadmap_level_for_index(index: str) -> str:
    depth = subphase_index_depth(index)
    return {1: "primary", 2: "secondary", 3: "tertiary", 4: "quaternary"}.get(depth, "deeper")


def _roadmap_root_rel(vault_root: Path, project_id: str, track: Track) -> str:
    base = f"1-Projects/{project_id}/Roadmap"
    if track == "execution":
        return f"{base}/Execution"
    return base


def phase_folder_for_num(vault_root: Path, project_id: str, phase_num: int, *, track: Track = "conceptual") -> Path | None:
    road = vault_root / "1-Projects" / project_id / "Roadmap"
    if track == "execution":
        road = road / "Execution"
    if not road.is_dir():
        return None
    for child in road.iterdir():
        if child.is_dir() and re.match(rf"Phase-{phase_num}-", child.name):
            return child
    return None


def find_secondary_folder(phase_dir: Path, secondary_index: str) -> Path | None:
    """Resolve Phase-N-M-* folder under a phase dir (nested or from flat secondary file)."""
    parts = subphase_index_parts(secondary_index)
    if not parts or len(parts) != 2:
        return None
    prefix = index_path_prefix(parts)
    for child in phase_dir.iterdir():
        if child.is_dir() and child.name.startswith(prefix + "-"):
            return child
    for child in phase_dir.glob(f"{prefix}-*-Roadmap-*.md"):
        slug = slug_from_basename(child.name, parts)
        folder = phase_dir / f"{prefix}-{slug}"
        return folder
    return None


def _default_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d-%H%M")


def roadmap_path_for(req: RoadmapPathRequest) -> RoadmapPathResult:
    """Compute canonical vault-relative path for a roadmap mint target."""
    parts = subphase_index_parts(req.subphase_index)
    if not parts:
        return RoadmapPathResult(False, violations=["subphase_index_invalid"])

    level = str(req.roadmap_level or "").lower() or roadmap_level_for_index(req.subphase_index)
    phase_dir = phase_folder_for_num(req.vault_root, req.project_id, parts[0], track=req.track)
    if phase_dir is None:
        return RoadmapPathResult(False, violations=[f"phase_folder_missing:{parts[0]}"])

    road_rel = str(phase_dir.relative_to(req.vault_root))
    stamp = str(req.timestamp_slug or "").strip() or _default_stamp()
    slug = str(req.title_slug or "").strip() or "Roadmap-Slice"
    slug = slugify_title(slug) if slug else "Roadmap-Slice"

    if len(parts) == 1:
        phase_name = req.phase_folder_name or phase_dir.name
        if phase_name.startswith(f"Phase-{parts[0]}-"):
            slug = phase_name[len(f"Phase-{parts[0]}-") :]
        basename = f"Phase-{parts[0]}-{slug}-Roadmap-{stamp}.md"
        rel_dir = road_rel
        rel_path = f"{rel_dir}/{basename}"
        return RoadmapPathResult(
            True,
            rel_dir=rel_dir,
            rel_path=rel_path,
            basename=basename,
            ensure_dirs=[rel_dir],
            frontmatter_hints={
                "roadmap-level": "primary",
                "phase-number": parts[0],
                "subphase-index": str(parts[0]),
            },
        )

    if len(parts) == 2:
        sec_prefix = index_path_prefix(parts)
        sec_folder_name = req.secondary_folder_name or f"{sec_prefix}-{slug}"
        if not sec_folder_name.startswith(sec_prefix):
            sec_folder_name = f"{sec_prefix}-{slug}"
        rel_dir = f"{road_rel}/{sec_folder_name}"
        basename = f"{sec_prefix}-{slug}-Roadmap-{stamp}.md"
        rel_path = f"{rel_dir}/{basename}"
        return RoadmapPathResult(
            True,
            rel_dir=rel_dir,
            rel_path=rel_path,
            basename=basename,
            ensure_dirs=[rel_dir],
            frontmatter_hints={
                "roadmap-level": "secondary",
                "phase-number": parts[0],
                "subphase-index": f"{parts[0]}.{parts[1]}",
            },
        )

    if len(parts) == 3:
        sec_index = f"{parts[0]}.{parts[1]}"
        sec_folder = find_secondary_folder(phase_dir, sec_index)
        if sec_folder is None:
            sec_prefix = index_path_prefix([parts[0], parts[1]])
            sec_folder_name = req.secondary_folder_name or f"{sec_prefix}-{slug}"
            rel_dir = f"{road_rel}/{sec_folder_name}"
        else:
            rel_dir = str(sec_folder.relative_to(req.vault_root))
        ter_prefix = index_path_prefix(parts)
        basename = f"{ter_prefix}-{slug}-Roadmap-{stamp}.md"
        rel_path = f"{rel_dir}/{basename}"
        return RoadmapPathResult(
            True,
            rel_dir=rel_dir,
            rel_path=rel_path,
            basename=basename,
            ensure_dirs=[rel_dir],
            frontmatter_hints={
                "roadmap-level": "tertiary",
                "phase-number": parts[0],
                "subphase-index": f"{parts[0]}.{parts[1]}.{parts[2]}",
            },
        )

    ter_prefix = index_path_prefix(parts)
    parent_parts = parts[:-1]
    parent_index = ".".join(str(p) for p in parent_parts)
    if len(parent_parts) == 2:
        sec_folder = find_secondary_folder(phase_dir, parent_index)
        rel_dir = (
            str(sec_folder.relative_to(req.vault_root))
            if sec_folder
            else f"{road_rel}/{index_path_prefix(parent_parts)}-{slug}"
        )
    else:
        rel_dir = road_rel
    basename = f"{ter_prefix}-{slug}-Roadmap-{stamp}.md"
    rel_path = f"{rel_dir}/{basename}"
    return RoadmapPathResult(
        True,
        rel_dir=rel_dir,
        rel_path=rel_path,
        basename=basename,
        ensure_dirs=[rel_dir],
        frontmatter_hints={
            "roadmap-level": level,
            "phase-number": parts[0],
            "subphase-index": ".".join(str(p) for p in parts),
        },
    )


def canonical_path_for_note(
    vault_root: Path,
    path: Path,
    fm: dict[str, Any],
    *,
    track: Track = "conceptual",
) -> RoadmapPathResult | None:
    """Given an existing note, compute where it should live."""
    idx = str(fm.get("subphase-index") or "").strip()
    parts = subphase_index_parts(idx)
    if not parts:
        return None
    try:
        rel = str(path.relative_to(vault_root))
    except ValueError:
        return None
    m = re.search(r"1-Projects/([^/]+)/Roadmap/", rel.replace("\\", "/"))
    project_id = m.group(1) if m else str(fm.get("project-id") or "")
    if not project_id:
        return None
    if "/Execution/" in rel:
        track = "execution"
    slug = slug_from_basename(path.name, parts)
    title = str(fm.get("title") or slug)
    return roadmap_path_for(
        RoadmapPathRequest(
            vault_root=vault_root,
            project_id=project_id,
            subphase_index=idx,
            title_slug=slug or slugify_title(title),
            roadmap_level=str(fm.get("roadmap-level") or ""),
            track=track,
            timestamp_slug=_extract_stamp(path.name),
        )
    )


def _extract_stamp(basename: str) -> str:
    m = re.search(r"-Roadmap-(\d{4}-\d{2}-\d{2}(?:-\d{4})?)\.md$", basename)
    return m.group(1) if m else ""


def path_placement_violations(vault_root: Path, path: Path, fm: dict[str, Any]) -> list[str]:
    """Return violations when note is not at canonical path for its subphase-index."""
    level = str(fm.get("roadmap-level") or "").lower()
    if level in ("master", "task", ""):
        return []
    idx = str(fm.get("subphase-index") or "").strip()
    parts = subphase_index_parts(idx)
    if not parts:
        return []

    try:
        rel = str(path.relative_to(vault_root)).replace("\\", "/")
    except ValueError:
        return ["path_outside_vault"]

    if any(part in rel for part in _SKIP_REL_PARTS):
        return []
    if Path(rel).name in _STATE_NAMES or "MOC" in rel:
        return []

    depth = len(parts)
    parent = path.parent
    parent_name = parent.name

    if depth == 1:
        if parent_name.startswith(f"Phase-{parts[0]}-"):
            return []
        return ["primary_not_in_phase_folder"]

    if depth == 2:
        sec_prefix = index_path_prefix(parts)
        if parent_name.startswith(sec_prefix + "-") and parent_name != f"Phase-{parts[0]}-":
            return []
        if path.name.startswith(sec_prefix + "-") and parent_name.startswith(f"Phase-{parts[0]}-"):
            return ["secondary_flat_in_phase_folder"]
        return ["secondary_not_in_secondary_folder"]

    if depth >= 3:
        sec_index = f"{parts[0]}.{parts[1]}"
        phase_dir = phase_folder_for_num(
            vault_root,
            _project_id_from_rel(rel) or str(fm.get("project-id") or ""),
            parts[0],
            track="execution" if "/Execution/" in rel else "conceptual",
        )
        if phase_dir is None:
            return ["phase_folder_missing"]
        sec_folder = find_secondary_folder(phase_dir, sec_index)
        if sec_folder is None:
            return ["secondary_folder_missing_for_tertiary"]
        try:
            if path.parent.resolve() == sec_folder.resolve():
                return []
        except OSError:
            pass
        if path.parent == phase_dir:
            return ["tertiary_flat_in_phase_folder"]
        return ["tertiary_not_in_secondary_folder"]

    return []


def _project_id_from_rel(rel: str) -> str | None:
    m = re.search(r"1-Projects/([^/]+)/Roadmap/", rel)
    return m.group(1) if m else None


def _read_note_fm(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8", errors="replace")
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 4)
    if end < 0:
        return {}
    fm = yaml.safe_load(text[4:end]) or {}
    return fm if isinstance(fm, dict) else {}


def scan_structural_path_violations(vault_root: Path, project_id: str) -> list[dict[str, Any]]:
    """Scan conceptual + execution roadmap trees for path placement violations."""
    vault_root = vault_root.resolve()
    out: list[dict[str, Any]] = []
    for track in ("conceptual", "execution"):
        road = vault_root / "1-Projects" / project_id / "Roadmap"
        if track == "execution":
            road = road / "Execution"
        if not road.is_dir():
            continue
        for path in road.rglob("*.md"):
            rel = str(path.relative_to(vault_root)).replace("\\", "/")
            if any(part in rel for part in _SKIP_REL_PARTS):
                continue
            if Path(rel).name in _STATE_NAMES or "MOC" in rel:
                continue
            if "/Phase-" not in rel:
                continue
            fm = _read_note_fm(path)
            if str(fm.get("roadmap_track") or "").lower() == "execution" and track == "conceptual":
                continue
            violations = path_placement_violations(vault_root, path, fm)
            if violations:
                canon = canonical_path_for_note(vault_root, path, fm, track=track)  # type: ignore[arg-type]
                out.append(
                    {
                        "rel_path": rel,
                        "subphase_index": fm.get("subphase-index"),
                        "roadmap_level": fm.get("roadmap-level"),
                        "violations": violations,
                        "canonical_rel_path": canon.rel_path if canon and canon.ok else "",
                    }
                )
    return out


def canonical_repath_target(
    vault_root: Path,
    path: Path,
    fm: dict[str, Any],
    *,
    track: Track = "conceptual",
) -> tuple[str, str] | None:
    """Return (rel_dir, rel_path) preserving basename; parent folder canonicalized."""
    canon = canonical_path_for_note(vault_root, path, fm, track=track)
    if not canon or not canon.ok:
        return None
    rel_path = f"{canon.rel_dir}/{path.name}"
    return canon.rel_dir, rel_path


def attach_deepen_path_hint(
    vault_root: Path,
    params: dict[str, Any],
) -> dict[str, Any]:
    """When deepen params include target index + title, attach canonical write path."""
    merged = dict(params)
    idx = str(params.get("next_subphase_index") or params.get("target_subphase_index") or "").strip()
    if not idx:
        return merged
    project_id = str(params.get("project_id") or "").strip()
    if not project_id:
        return merged
    title = str(params.get("target_title_slug") or params.get("target_title") or "")
    track: Track = "execution" if str(params.get("roadmap_track") or "").lower() == "execution" else "conceptual"
    result = roadmap_path_for(
        RoadmapPathRequest(
            vault_root=vault_root,
            project_id=project_id,
            subphase_index=idx,
            title_slug=title,
            track=track,
        )
    )
    if result.ok:
        merged["roadmap_write_path"] = result.rel_path
        merged["roadmap_write_dir"] = result.rel_dir
        merged["roadmap_path_resolver_enforced"] = load_path_resolver_config(vault_root).get(
            "path_resolver_enforced", True
        )
    return merged
