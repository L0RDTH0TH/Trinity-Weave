"""Prefer authorship contract — durable product seats for worldgen / Terrain3D feed.

Constitution-grade Prefer law (not one-off brief text). Product Prefer seats dominate
proxy metrics (budgets, file existence, shell checklists, bootstrap stubs).

Locked step-1 law (operator 2026-10-01):
  Craft = Hot Wheels tile authorship; Terrain3D = fed car under Sparky;
  no craft-view blend; no cam recenter on place.
  Cite: https://www.youtube.com/watch?v=Y19Mw5YsgjI
  Vault: Ingest/Resources/Townscaper-Dual-Grid-Authorship-YT-Y19Mw5YsgjI-2026-10-01.md
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from .factory_little_val import FactoryLittleValResult

YT_CANONICAL = "https://www.youtube.com/watch?v=Y19Mw5YsgjI"
VAULT_CITE = (
    "Ingest/Resources/Townscaper-Dual-Grid-Authorship-YT-Y19Mw5YsgjI-2026-10-01.md"
)

# Durable negative examples — Prefer must not re-blend these failure modes.
NEGATIVE_EXAMPLES: tuple[dict[str, str], ...] = (
    {
        "id": "cam_yank_on_place",
        "refuse": "craft_cam_recenter_on_place",
        "summary": "Craft place/remove recenters camera / orbit focus onto the new tile",
    },
    {
        "id": "craft_view_terrain_blend",
        "refuse": "craft_terrain_blend",
        "summary": "Craft view deforms checker/grid into Terrain3D heights (Hot Wheels≠car)",
    },
    {
        "id": "craft_phase_terrain3d_deform",
        "refuse": "craft_phase_terrain3d_deform",
        "summary": "Craft phase authors via Terrain3D sculpt instead of tile map",
    },
    {
        "id": "missing_sparky_feed_separation",
        "refuse": "unfed_terrain_under_sparky",
        "summary": "Sparky sees graybox-only; Terrain3D not fed as separate consumer layer",
    },
    {
        "id": "layer_collapse_in_craft",
        "refuse": "inspiration_shape_miss",
        "summary": "Prefer collapses Hot Wheels craft into Terrain3D under craft cam",
    },
    {
        "id": "points_as_grid",
        "refuse": "points_as_grid",
        "summary": "Markers at coordinates with no edges/faces claimed as grid Success",
    },
    {
        "id": "count_equals_topology",
        "refuse": "count_equals_topology",
        "summary": "N points present ≠ lattice graph with cells/edges (proxy metric trap)",
    },
    {
        "id": "explicit_met_implicit_miss",
        "refuse": "explicit_met_implicit_miss",
        "summary": "Countable ask met while the bound structural Success (edges + faces/cells) is absent",
    },
)

WORLDGEN_SLICE_MARKERS: tuple[str, ...] = (
    "worldgen",
    "terrain3d_feed",
    "dualgrid",
    "dual_grid",
    "ux_world_generation",
    "townscaper",
    "tutorial_s",
    "occupancy",
)

# Patterns that indicate craft-cam recenter / focus yank on place (structural heuristics).
_CAM_RECENTER_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"SetFocusWorld\s*\(", re.I),
    re.compile(r"GlobalPosition\s*=\s*.*\b(?:picked?|cell|place)\b", re.I),
    re.compile(r"recenter.*(?:place|paint|cell)|(?:place|paint|cell).*recenter", re.I),
)

# Patterns that indicate craft-view Terrain3D deform (blend under craft).
_CRAFT_BLEND_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(
        r"craft.*(?:SetHeight|SetHeights|sculpt|deform).*Terrain3D|"
        r"Terrain3D.*(?:SetHeight|SetHeights|sculpt|deform).*craft",
        re.I,
    ),
    re.compile(r"ApplyTerrain(?:Under|In)Craft|BlendCraft(?:To|Into)Terrain", re.I),
)


# Product Prefer seats + topology refuses the lane may never waive.
PRODUCT_PREFER_DO_NOT_WAIVE: tuple[str, ...] = (
    "Terrain3D_prefer_proof",
    "prefer_authorship_pass",
    "craft_cam_recenter_on_place",
    "craft_terrain_blend",
    "points_as_grid",
    "count_equals_topology",
    "explicit_met_implicit_miss",
    "infinite_rect_as_hex19",
)

# Armed-named LIVE surfaces that a topology bind is always scanned against —
# a lane cannot dodge the seat by declaring an unrelated change set.
REQUIRED_LIVE_TOPOLOGY_FILES: tuple[str, ...] = (
    "Systems/DualGridCraftHost.cs",
    "Core/WorldGen/Hex19OccupancyLattice.cs",
)

# Positive edge evidence — neighbor/adjacency topology, not a coordinate list.
_EDGE_SIGNALS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("neighbor_api", re.compile(r"\bNeighbou?rs?(?:Of|Edges|Offsets|Axials)?\b", re.I)),
    ("adjacency", re.compile(r"\bAdjacen(?:t|cy)[A-Za-z]*\b", re.I)),
    ("edge_collection", re.compile(r"\bEdges?(?:List|Set|Pairs|Index|Keys|Of)?\b", re.I)),
    ("edge_builder", re.compile(r"\b(?:BuildEdges|EnumerateEdges|LatticeEdges|HexEdges)\b", re.I)),
    ("line_primitive", re.compile(r"PrimitiveType\.Lines\b|PRIMITIVE_LINES\b")),
)

# Positive face/cell evidence — a cell must be defined by its vertices/corners,
# not merely be the word "cell" next to a marker position.
_FACE_CELL_SIGNALS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("face_collection", re.compile(r"\bFaces?(?:List|Set|Index|Vertices|Corners)?\b", re.I)),
    ("cell_geometry", re.compile(r"\bCell(?:Vertices|Corners|Polygon|Face|Fan|Mesh|Outline)\b", re.I)),
    ("corner_api", re.compile(r"\b(?:HexCorners?|CornersOf|CellCornersOf|PolygonFan)\b", re.I)),
    ("cell_builder", re.compile(r"\b(?:BuildCells?|EnumerateCells?|CellsFromVertices|BuildFaces)\b", re.I)),
    ("cell_entity", re.compile(r"\bHexCells?\b", re.I)),
)

# Point-cloud tells — countable proxy without a graph.
_POINT_CLOUD_SIGNALS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("point_count", re.compile(r"\b(?:Lattice)?PointCount\b")),
    ("point_array", re.compile(r"\bPoint(?:s|Set|List)\b")),
    ("marker_per_point", re.compile(r"\b(?:MakeDiskMarker|OccupancyMarker|Slot_|MarkerMesh)\b")),
    ("logic_points", re.compile(r"\blogic_points\b|\bLogicPoint\w*\b")),
)

def _code_only(text: str) -> str:
    """Strip comments and literals — claims in prose/logs are not evidence.

    Single left-to-right scan, because `"res://x"` must not read as a comment and
    a literal containing a quote must not desynchronize the rest of the file.
    """
    out: list[str] = []
    i, n = 0, len(text)
    while i < n:
        ch = text[i]
        nxt = text[i + 1] if i + 1 < n else ""
        if ch == "/" and nxt == "/":
            end = text.find("\n", i)
            i = n if end < 0 else end
            continue
        if ch == "/" and nxt == "*":
            end = text.find("*/", i + 2)
            out.append(" ")
            i = n if end < 0 else end + 2
            continue
        if ch == "@" and nxt == '"':
            i += 2
            while i < n:
                if text[i] == '"':
                    if i + 1 < n and text[i + 1] == '"':
                        i += 2
                        continue
                    i += 1
                    break
                i += 1
            out.append(' "" ')
            continue
        if ch in "\"'":
            quote = ch
            i += 1
            while i < n and text[i] != "\n":
                if text[i] == "\\":
                    i += 2
                    continue
                if text[i] == quote:
                    i += 1
                    break
                i += 1
            out.append(' "" ' if quote == '"' else " '' ")
            continue
        out.append(ch)
        i += 1
    return "".join(out)


@dataclass(frozen=True)
class PreferAuthorshipResult:
    ok: bool
    little_val: FactoryLittleValResult
    detail: str
    applicable: bool = True
    negative_examples: tuple[str, ...] = ()
    warnings: tuple[str, ...] = ()
    topology_evidence: dict[str, Any] | None = None
    bind: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "detail": self.detail,
            "applicable": self.applicable,
            "violations": list(self.little_val.anti_pattern_violations),
            "negative_examples": list(self.negative_examples),
            "warnings": list(self.warnings),
            "topology_evidence": self.topology_evidence,
            "implicit_bind": self.bind,
        }


def slice_requires_prefer_authorship(slice_id: str, job: dict[str, Any] | None = None) -> bool:
    """True when slice / Prefer overlay is worldgen or Terrain3D-feed authorship."""
    blob = " ".join(
        [
            str(slice_id or ""),
            str((job or {}).get("ask_id") or ""),
            str((job or {}).get("half_b_overlay_slice_id") or ""),
            str((job or {}).get("catalog_row_id") or ""),
            str((job or {}).get("prefer_proof") or ""),
        ]
    ).lower()
    if any(m in blob for m in WORLDGEN_SLICE_MARKERS):
        return True
    armed = str((job or {}).get("armed_packet_path") or "")
    if armed and any(m in armed.lower() for m in WORLDGEN_SLICE_MARKERS):
        return True
    if (job or {}).get("step1_authorship") or (job or {}).get("prefer_authorship"):
        return True
    return False


def load_armed_packet(vault_root: Path, job: dict[str, Any] | None) -> dict[str, Any]:
    path_s = str((job or {}).get("armed_packet_path") or "").strip()
    if not path_s:
        return {}
    path = vault_root / path_s
    if not path.is_file():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return data if isinstance(data, dict) else {}


def resolve_step1_lock(armed: dict[str, Any] | None) -> tuple[dict[str, Any], list[str]]:
    """Prefer the dict lock shape; a bare ``step1_authorship: true`` only warns.

    Returns (lock_dict, warnings). Empty dict + empty warnings = no lock declared.
    """
    armed = armed if isinstance(armed, dict) else {}
    locks = armed.get("locks") if isinstance(armed.get("locks"), dict) else {}
    for candidate in (
        locks.get("step1_authorship"),
        locks.get("step1_occupancy"),
        armed.get("step1_authorship"),
    ):
        if isinstance(candidate, dict) and candidate:
            return candidate, []
    bare = (
        locks.get("step1_authorship")
        or locks.get("step1_occupancy")
        or armed.get("step1_authorship")
        or armed.get("prefer_authorship")
    )
    if bare:
        return {}, ["step1_authorship_bool_underspecified"]
    return {}, []


def scan_topology_evidence(
    game_repo: Path,
    *,
    changed_paths: tuple[str, ...] | None = None,
) -> dict[str, Any]:
    """Structured LIVE evidence for the lattice-graph axis (points ≠ grid).

    Edges **and** faces/cells are both required as positive, code-level evidence.
    The armed-named LIVE surfaces are always scanned, change set or not.
    """
    evidence: dict[str, Any] = {
        "repo_present": game_repo.is_dir(),
        "files_scanned": [],
        "required_live_files_present": [],
        "required_live_files_absent": [],
        "edge_signals": [],
        "face_cell_signals": [],
        "point_signals": [],
        "has_edges": False,
        "has_faces_or_cells": False,
        "points_only": False,
        "missing_axes": [],
    }
    if not game_repo.is_dir():
        evidence["missing_axes"] = ["edges", "faces_cells"]
        return evidence

    candidates: list[Path] = []
    for rel in REQUIRED_LIVE_TOPOLOGY_FILES:
        fp = game_repo / rel
        if fp.is_file():
            candidates.append(fp)
            evidence["required_live_files_present"].append(rel)
        else:
            evidence["required_live_files_absent"].append(rel)
    for rel in changed_paths or ():
        fp = game_repo / rel
        if fp.is_file() and fp.suffix.lower() == ".cs":
            candidates.append(fp)
    for sub in ("Systems", "Core/WorldGen"):
        base = game_repo / sub
        if base.is_dir():
            for pattern in ("*Craft*.cs", "*Lattice*.cs", "*Hex*.cs", "*Worldgen*.cs"):
                candidates.extend(base.rglob(pattern))

    seen: set[Path] = set()
    for fp in candidates:
        if fp in seen or not fp.is_file():
            continue
        seen.add(fp)
        rel = str(fp.relative_to(game_repo)).replace("\\", "/")
        evidence["files_scanned"].append(rel)
        raw = fp.read_text(encoding="utf-8", errors="replace")
        code = _code_only(raw)
        for name, pat in _EDGE_SIGNALS:
            if pat.search(code):
                evidence["edge_signals"].append(f"{name}:{rel}")
        for name, pat in _FACE_CELL_SIGNALS:
            if pat.search(code):
                evidence["face_cell_signals"].append(f"{name}:{rel}")
        for name, pat in _POINT_CLOUD_SIGNALS:
            if pat.search(code):
                evidence["point_signals"].append(f"{name}:{rel}")

    for key in ("files_scanned", "edge_signals", "face_cell_signals", "point_signals"):
        evidence[key] = sorted(set(evidence[key]))
    evidence["has_edges"] = bool(evidence["edge_signals"])
    evidence["has_faces_or_cells"] = bool(evidence["face_cell_signals"])
    missing = []
    if not evidence["has_edges"]:
        missing.append("edges")
    if not evidence["has_faces_or_cells"]:
        missing.append("faces_cells")
    evidence["missing_axes"] = missing
    evidence["points_only"] = bool(evidence["point_signals"]) and bool(missing)
    return evidence


def topology_violations_from_evidence(evidence: dict[str, Any]) -> list[str]:
    """Map structured evidence onto durable refuse codes (non-waivable)."""
    violations: list[str] = []
    missing = list(evidence.get("missing_axes") or [])
    if not missing:
        return violations
    violations.append("explicit_met_implicit_miss:topology_axes_missing:" + "+".join(missing))
    point_signals = [str(s) for s in (evidence.get("point_signals") or [])]
    if evidence.get("points_only"):
        violations.append("points_as_grid:" + ",".join(point_signals[:4]))
    if any(s.startswith("point_count:") for s in point_signals):
        violations.append(
            "count_equals_topology:" + ",".join(s for s in point_signals if s.startswith("point_count:"))
        )
    if not evidence.get("files_scanned"):
        violations.append("explicit_met_implicit_miss:no_live_topology_surface_scanned")
    return violations


def authorship_overlay_markdown(*, slice_id: str = "") -> str:
    """Step-1 authorship overlay injected into producer missions / Prefer handoffs."""
    neg = "\n".join(
        f"- `{ex['refuse']}` — {ex['summary']}" for ex in NEGATIVE_EXAMPLES
    )
    return (
        "## Prefer authorship contract (host law — durable; not one-off brief text)\n\n"
        f"- **Slice:** `{slice_id or '(matching worldgen/terrain3d_feed)'}`\n"
        f"- **YT lock:** {YT_CANONICAL}\n"
        f"- **Vault cite:** `{VAULT_CITE}`\n"
        "- **Craft** = Hot Wheels tile authorship only (Townscaper dual-grid)\n"
        "- **Terrain3D** = real car / fed consumer under Sparky (or explicit feed)\n"
        "- **No** craft-view Terrain3D blend / deform\n"
        "- **No** camera recenter on place\n"
        "- **No proxy override:** host_touch_budget / shell seats / bootstrap stubs "
        "cannot pass or waive these product Prefer seats\n\n"
        "### Durable negative examples (fail closed)\n"
        f"{neg}\n"
    )


def _scan_repo_for_refuse(
    game_repo: Path,
    *,
    changed_paths: tuple[str, ...] | None,
) -> list[str]:
    """Structural heuristics over changed (or key worldgen) C# sources."""
    violations: list[str] = []
    if not game_repo.is_dir():
        return ["prefer_authorship:game_repo_missing"]

    candidates: list[Path] = []
    if changed_paths:
        for rel in changed_paths:
            fp = game_repo / rel
            if fp.is_file() and fp.suffix.lower() == ".cs":
                candidates.append(fp)
    if not candidates:
        # Prefer-scoped default surfaces when no change set (fail soft on missing).
        for rel in (
            *REQUIRED_LIVE_TOPOLOGY_FILES,
            "Systems/Worldgen/DualGridCraftHost.cs",
            "Systems/Worldgen/WorldgenCraftController.cs",
            "Core/WorldGen/DualGridCraftHost.cs",
        ):
            fp = game_repo / rel
            if fp.is_file():
                candidates.append(fp)
        # Broader scan of Systems/** craft hosts when present.
        systems = game_repo / "Systems"
        if systems.is_dir():
            for fp in systems.rglob("*Craft*.cs"):
                candidates.append(fp)
            for fp in systems.rglob("*Worldgen*.cs"):
                candidates.append(fp)

    seen: set[Path] = set()
    for fp in candidates:
        if fp in seen or not fp.is_file():
            continue
        seen.add(fp)
        text = fp.read_text(encoding="utf-8", errors="replace")
        # Behaviour lives in code — a doc comment restating the ban is not a violation.
        code = _code_only(text)
        rel = str(fp.relative_to(game_repo)).replace("\\", "/")
        # Explicit refuse tags in source / receipts count as documented bans (ok).
        refuse_documented = "refuse craft_cam_recenter_on_place" in text.lower() or (
            "craft_cam_recenter_on_place" in text and "refuse" in text.lower()
        )
        for pat in _CAM_RECENTER_PATTERNS:
            if pat.search(code) and not refuse_documented:
                # SetFocusWorld alone is not enough — require place/paint context nearby.
                if "SetFocusWorld" in pat.pattern:
                    if re.search(
                        r"(TryPick|Paint|Place|OnPrimary|OnClick).{0,400}SetFocusWorld|"
                        r"SetFocusWorld.{0,200}(Pick|Paint|Place|cell)",
                        code,
                        re.I | re.S,
                    ):
                        violations.append(f"craft_cam_recenter_on_place:{rel}")
                else:
                    violations.append(f"craft_cam_recenter_on_place:{rel}")
                break
        for pat in _CRAFT_BLEND_PATTERNS:
            if pat.search(code):
                violations.append(f"craft_terrain_blend:{rel}")
                break

    # Manifest / receipt honesty: factory Systems manifest may declare open refuse codes.
    man = game_repo / "Systems/_factory/manifest.yaml"
    if man.is_file():
        try:
            data = yaml.safe_load(man.read_text(encoding="utf-8")) or {}
        except (OSError, yaml.YAMLError):
            data = {}
        if isinstance(data, dict):
            open_fails = data.get("open_prefer_fails") or data.get("prefer_fails_open") or []
            if isinstance(open_fails, list):
                for code in open_fails:
                    c = str(code).strip()
                    if c in {ex["refuse"] for ex in NEGATIVE_EXAMPLES}:
                        violations.append(f"open_prefer_fail:{c}")

    return sorted(set(violations))


def run_prefer_authorship_pass(
    vault_root: Path,
    *,
    lane_id: str | None = None,
    game_repo_rel: str = "",
    changed_paths: tuple[str, ...] | None = None,
    job: dict[str, Any] | None = None,
) -> PreferAuthorshipResult:
    """
    Product Prefer seat — fail closed on layer blend / cam yank / craft Terrain3D deform
    / missing sparky-feed separation signals. Waives cannot silence this seat.
    """
    vault_root = vault_root.resolve()
    job = job if isinstance(job, dict) else {}
    slice_id = str(job.get("slice_id") or "")
    applicable = slice_requires_prefer_authorship(slice_id, job)
    if not applicable:
        lv = FactoryLittleValResult(True, [], "prefer_authorship_pass_skipped")
        return PreferAuthorshipResult(
            True, lv, "prefer_authorship_not_applicable", applicable=False
        )

    # Product Prefer seats are never waiveable — even shell-era waive flags.
    waived = {str(x) for x in (job.get("waive_seats") or [])}
    forbidden_waives = sorted(waived & set(PRODUCT_PREFER_DO_NOT_WAIVE))
    if job.get("waive_shell_era_seats") and forbidden_waives:
        lv = FactoryLittleValResult(
            False,
            [f"waive_forbidden_on_product_prefer_seat:{c}" for c in forbidden_waives],
            "prefer_authorship_pass",
        )
        return PreferAuthorshipResult(
            False,
            lv,
            "waive_forbidden_on_product_prefer_seat",
            applicable=True,
            negative_examples=tuple(ex["refuse"] for ex in NEGATIVE_EXAMPLES),
        )

    violations: list[str] = []
    warnings: list[str] = []
    cite = vault_root / VAULT_CITE
    if not cite.is_file():
        violations.append(f"missing_authorship_vault_cite:{VAULT_CITE}")

    armed = load_armed_packet(vault_root, job)
    step1_lock, lock_warnings = resolve_step1_lock(armed)
    warnings.extend(lock_warnings)
    if armed and not step1_lock and not lock_warnings:
        # Prefer overlay armed without step1 lock → topology/authorship drift.
        if any(m in str(armed.get("slice_id") or "").lower() for m in WORLDGEN_SLICE_MARKERS):
            violations.append("armed_packet_missing_step1_authorship_lock")

    # Bind fidelity (post-lane): the entry-seat rewrite must still hold.
    from .implicit_intent_bind import check_implicit_intent_bind

    bind_check = check_implicit_intent_bind(
        vault_root,
        slice_id=slice_id,
        job=job,
        project_id=str(job.get("project_id") or "") or None,
    )
    if bind_check.applicable and not bind_check.ok:
        violations.extend(bind_check.violations)

    # Fail-closed: a Prefer-applicable slice may not carry a bind that disarms the
    # topology axis. Clean ask wording is not a licence for the seat to go quiet.
    if bind_check.applicable and bind_check.bind and not bind_check.topology_rewrite:
        violations.append(f"topology_rewrite_disarmed_on_prefer_slice:{slice_id}")

    repo: Path | None = None
    if not game_repo_rel:
        violations.append("missing_game_repo_rel")
    else:
        repo = vault_root / game_repo_rel.strip("/")
        violations.extend(
            _scan_repo_for_refuse(repo, changed_paths=changed_paths)
        )

    # LIVE topology heuristics — armed law arms this axis even when the bind claims
    # topology_rewrite: false, so a disarmed bind cannot skip the LIVE scan.
    topology_evidence: dict[str, Any] | None = None
    if bind_check.topology_axis_armed and repo is not None:
        topology_evidence = scan_topology_evidence(repo, changed_paths=changed_paths)
        violations.extend(topology_violations_from_evidence(topology_evidence))

    # do_not_waive product Prefer seats must remain listed when Prefer overlay present.
    do_not_waive = job.get("do_not_waive") or []
    if isinstance(do_not_waive, str):
        do_not_waive = [do_not_waive]
    product_codes = set(PRODUCT_PREFER_DO_NOT_WAIVE)
    # Soft: only require when Prefer fields present on job.
    if job.get("prefer_proof") or job.get("armed_packet_path") or job.get("half_b_brief_path"):
        if not any(str(x) in product_codes or "Terrain3D" in str(x) for x in do_not_waive):
            # Advisory → binding: Prefer overlays must declare do_not_waive product seats.
            violations.append("prefer_overlay_missing_do_not_waive_product_seats")
        if bind_check.topology_axis_armed:
            missing_topology = [
                c
                for c in ("points_as_grid", "count_equals_topology", "explicit_met_implicit_miss")
                if c not in {str(x) for x in do_not_waive}
            ]
            if missing_topology:
                violations.append(
                    "prefer_overlay_missing_do_not_waive_topology_codes:"
                    + ",".join(missing_topology)
                )

    ok = len(violations) == 0
    lv = FactoryLittleValResult(ok, violations, "prefer_authorship_pass")
    detail = "; ".join(violations) if violations else "prefer_authorship_pass_ok"
    if warnings:
        detail = f"{detail} | warnings: {'; '.join(warnings)}"
    return PreferAuthorshipResult(
        ok,
        lv,
        detail,
        applicable=True,
        negative_examples=tuple(ex["refuse"] for ex in NEGATIVE_EXAMPLES),
        warnings=tuple(warnings),
        topology_evidence=topology_evidence,
        bind=bind_check.to_dict() if bind_check.applicable else None,
    )


def product_prefer_seats_met(lane_seats: dict[str, Any] | None) -> bool:
    """True when Prefer product seats (authorship) are ok or not applicable."""
    if not lane_seats:
        return True
    passes = lane_seats.get("passes") or {}
    authorship = passes.get("prefer_authorship_pass")
    if authorship is None:
        return True
    return bool(getattr(authorship, "ok", True) if not isinstance(authorship, dict) else authorship.get("ok"))
