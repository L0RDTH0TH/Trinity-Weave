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
    {
        "id": "skip_dual_offset",
        "refuse": "skip_dual_offset",
        "summary": "s2 dual missing half-step offset quads / four-corner reads / update-four (markers-only dual)",
    },
    {
        "id": "hex_scaffold_as_final_mesh",
        "refuse": "hex_scaffold_as_final_mesh",
        "summary": "F5 primary surface is still the hex occupancy / hex scaffold lattice",
    },
    {
        "id": "dual_overlay_as_grid_kernel",
        "refuse": "dual_overlay_as_grid_kernel",
        "summary": "Quads only as dual overlay on hex fill; base mesh remains hex",
    },
    {
        "id": "skip_dissolve_relax",
        "refuse": "skip_dissolve_relax",
        "summary": "Quads without dissolve AND subdivide AND relax on the generative path",
    },
    {
        "id": "stretch_as_variant",
        "refuse": "stretch_as_variant",
        "summary": (
            "Dual Success claimed via non-uniform Scale / elongating organic-face "
            "footprint instead of discrete MeshLibrary silhouettes "
            "(empty/edge/corner/full)"
        ),
    },
    {
        "id": "over_neighbor_paint",
        "refuse": "over_neighbor_paint",
        "summary": (
            "Logic-point flip refreshes more than the ≤4 dual cells that share "
            "that corner (over-broad neighborhood / face-flood as dual Success)"
        ),
    },
    {
        "id": "unstable_dual_neighborhood",
        "refuse": "unstable_dual_neighborhood",
        "summary": (
            "Same logic point yields different dual-cell ownership sets across "
            "repeated clicks (neighborhood not geometric/stable)"
        ),
    },
    {
        "id": "stamp_as_dual",
        "refuse": "stamp_as_dual",
        "summary": (
            "Independent occupancy / centroid MeshLibrary stamps sold as dual "
            "cells owned by shared logic corners"
        ),
    },
    {
        "id": "primary_face_as_dual",
        "refuse": "primary_face_as_dual",
        "summary": (
            "Ownership/highlight keyed to OrganicQuadMesh face indices / primary "
            "face-neighborhood (cyan 2×2 on yellow wire) sold as dual Success "
            "without half-step OrganicDualOffsetLattice"
        ),
    },
    {
        "id": "proxy_substitution",
        "refuse": "proxy_substitution",
        "summary": (
            "Parent refuse class: countable / scanner / Prefer-symbol stand-in "
            "sold as Success for a different object class (intent-evidence mismatch)"
        ),
    },
    {
        "id": "intent_collapsed_to_mechanics",
        "refuse": "intent_collapsed_to_mechanics",
        "summary": (
            "Intent reduced to mechanical Prefer symbols / prove APIs / cardinality "
            "without surviving conceptual leg (success_object + invariant)"
        ),
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
    "stalberg",
    "organic_quad",
    "quad_kernel",
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
    "skip_dual_offset",
    "gray_ramp_only",
    "stretch_as_variant",
    "over_neighbor_paint",
    "unstable_dual_neighborhood",
    "stamp_as_dual",
    "primary_face_as_dual",
    "proxy_substitution",
    "intent_collapsed_to_mechanics",
    "inspiration_shape_miss",
    "hex_scaffold_as_final_mesh",
    "dual_overlay_as_grid_kernel",
    "skip_dissolve_relax",
    "noodle_edge_clutter",
    "wireframe_spaghetti",
    "extruded_prism_as_quad_board",
    "unbounded_z_jitter",
    "nonplanar_face_soup",
    "non_unique_vertices",
    "relax_before_quad_only",
    "naive_laplacian_only",
    "missing_square_area_force",
    "free_boundary_fold",
    "extrusion_before_2d_stable",
    "relax_step_too_hard",
)

# Intent-validates-gates Prefer — non-waivable parent + collapse class.
INTENT_VALIDATES_DO_NOT_WAIVE: tuple[str, ...] = (
    "proxy_substitution",
    "intent_collapsed_to_mechanics",
)

# Armed-named LIVE surfaces that a topology bind is always scanned against —
# a lane cannot dodge the seat by declaring an unrelated change set.
REQUIRED_LIVE_TOPOLOGY_FILES: tuple[str, ...] = (
    "Systems/DualGridCraftHost.cs",
    "Core/WorldGen/Hex19OccupancyLattice.cs",
)

# Stålberg organic all-quad kernel LIVE surfaces — required when armed.
REQUIRED_LIVE_ORGANIC_QUAD_FILES: tuple[str, ...] = (
    "Core/WorldGen/StalbergQuadKernel.cs",
    "Core/WorldGen/OrganicQuadMesh.cs",
    "Systems/DualGridCraftHost.cs",
)

_ORGANIC_PIPELINE_SIGNALS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("seed", re.compile(r"\bSeedHexLatticeRings\b")),
    ("triangulate", re.compile(r"\bTriangulateHexLattice\b")),
    ("dissolve", re.compile(r"\bDissolveTrianglePairs\b")),
    ("subdivide", re.compile(r"\bSubdivideFacesToQuads\b")),
    ("relax", re.compile(r"\bRelaxTowardSquares\b")),
    ("flatten", re.compile(r"\bFlattenToCraftPlane\b")),
    ("regenerate", re.compile(r"\bRegenerateOrganicQuadMesh\b")),
    ("prove", re.compile(r"\bProveOrganicQuadKernel\b")),
    ("unique_topo", re.compile(r"\bUniqueTopology2D\b")),
    ("get_or_add", re.compile(r"\bGetOrAddVertex\b")),
    ("position_hash", re.compile(r"\bPositionHash\b")),
    ("area_side", re.compile(r"\bEstimateIdealSideFromArea\b")),
    ("clamp_force", re.compile(r"\bClampForce\b")),
    ("boundary_pin", re.compile(r"\bMarkBoundaryPinned\b")),
    ("reweld", re.compile(r"\bWeldNearDuplicates\b")),
)

# Visual-r1 refuse: Alpha transparency on organic face/edge mesh = noodle/prism soup.
# CullMode.Disabled is OK when paired with opaque depth-tested faces (craft-cam readability).
_ORGANIC_NOODLE_RENDER_SIGNALS: tuple[tuple[str, re.Pattern[str]], ...] = (
    (
        "face_alpha_transparency",
        re.compile(
            r"BuildFaceMesh[\s\S]{0,1200}Transparency\s*=\s*BaseMaterial3D\.TransparencyEnum\.Alpha",
            re.M,
        ),
    ),
    (
        "edge_alpha_transparency",
        re.compile(
            r"BuildEdgeMesh[\s\S]{0,800}Transparency\s*=\s*BaseMaterial3D\.TransparencyEnum\.Alpha",
            re.M,
        ),
    ),
)

_HEX_SCAFFOLD_PRIMARY_SIGNALS: tuple[tuple[str, re.Pattern[str]], ...] = (
    (
        "hex19_lattice_graph_root",
        re.compile(r'Name\s*=\s*"Hex19LatticeGraph"'),
    ),
    (
        "build_lattice_visuals_as_primary",
        re.compile(r"BuildLatticeVisuals\s*\(\s*\)\s*;"),
    ),
)

_DUAL_OVERLAY_AS_KERNEL_SIGNALS: tuple[tuple[str, re.Pattern[str]], ...] = (
    (
        "dual_visual_success_true",
        re.compile(r'\["dual_visual_success"\]\s*=\s*true'),
    ),
    (
        "build_dual_offset_overlay_primary",
        re.compile(r"BuildDualOffsetOverlay\s*\(\s*\)\s*;"),
    ),
)

# s2 dual-offset LIVE surfaces — required when locks.step2_dual_offset is armed.
REQUIRED_LIVE_DUAL_FILES: tuple[str, ...] = (
    "Core/WorldGen/Hex19DualOffsetLattice.cs",
    "Systems/DualGridCraftHost.cs",
)

# Positive dual-offset evidence (corner-driven half-step quads + update-four).
_DUAL_OFFSET_SIGNALS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("dual_cells_touching", re.compile(r"\bDualCellsTouching\b")),
    ("update_four_api", re.compile(r"\bUpdateFourDualSlots\b")),
    ("corner_occupancy", re.compile(r"\bCornerOccupancySamples\b|\bCornerAxialOffsets\b|\bCornersPerDual\b")),
    ("half_step_offset", re.compile(r"\bIsHalfStepOffset\b|\bhalf[_-]?step\b|\bHalfStep\b", re.I)),
    ("tile_family", re.compile(r"\bTileFamilyIndex\b")),
    ("dual_overlay_toggle", re.compile(r"\bToggleDualOverlayVisible\b|\bSetDualOverlayVisible\b")),
)

# Markers-only / spray dual tells — Prefer must refuse as skip_dual_offset.
_DUAL_MARKERS_ONLY_SIGNALS: tuple[tuple[str, re.Pattern[str]], ...] = (
    (
        "per_occ_spray",
        re.compile(
            r"CellCount\s*\*\s*DualSlotsPerOccupancy|DualSlotsPerOccupancy\s*\*\s*CellCount"
        ),
    ),
    (
        "marker_mesh_as_dual",
        re.compile(r"\b(?:MakeDiskMarker|OccupancyMarker)\b.*[Dd]ual|[Dd]ual.*\b(?:MakeDiskMarker|SphereMesh)\b"),
    ),
)

# Dual-visual / MeshLibrary fidelity — shape-distinct families (refuse gray_ramp_only).
_DUAL_VISUAL_SIGNALS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("shape_distinct_builder", re.compile(r"\bMakeShapeDistinctDualVariant\b|\bCommitDualFamilyMesh\b")),
    ("dual_visual_family_enum", re.compile(r"\bDualVisualFamily\b")),
    ("prove_dual_visual", re.compile(r"\bProveDualVisualVariants\b")),
    ("shape_distinct_meshlibrary", re.compile(r"\bEnsureShapeDistinctDualMeshLibrary\b|approved_shape_distinct_graybox")),
    ("family_empty_edge_corner_full", re.compile(r"empty\s*\|\s*edge\s*\|\s*corner\s*\|\s*full|Empty\s*=\s*0,\s*\n\s*Edge\s*=\s*1")),
    # Discrete MeshLibrary item placement (not face-warped stretch).
    (
        "discrete_library_place",
        re.compile(
            r"\bPlaceDiscreteDual(?:Library)?(?:Item|Variant)\b|"
            r"GetItemMesh\s*\(\s*\(int\)\s*family|"
            r"GetItemMesh\s*\(\s*\(int\)\s*DualVisualFamily|"
            r"library_item_id\s*=\s*\(int\)\s*family|"
            r"discrete_meshlibrary_item",
            re.I,
        ),
    ),
    (
        "neighborhood_cardinality_gate",
        re.compile(
            r"\b(?:MaxDualCellsPerLogicFlip|ProveNeighborhoodCardinality|"
            r"DualCellsPerLogicFlip\s*=\s*4|update_four_cap\s*=\s*4)\b|"
            r"refuse\s*=\s*over_neighbor_paint|refuse=over_neighbor_paint",
            re.I,
        ),
    ),
)

_GRAY_RAMP_ONLY_TELLS: tuple[tuple[str, re.Pattern[str]], ...] = (
    (
        "organic_dual_uses_family_color_ramp",
        re.compile(
            r"EnsureOrganicDualCellMesh[\s\S]{0,1200}?DualFamilyColor\s*\(",
            re.M,
        ),
    ),
    (
        "library_null_same_plate",
        re.compile(r"MeshLibrary\?\s+Library\s*=>\s*null"),
    ),
    (
        "mesh_source_graybox_without_shape_distinct",
        re.compile(
            r'MeshLibrarySource\s*=>\s*"stalberg_organic_all_quad_graybox"'
        ),
    ),
)

# stretch_as_variant — axis elongation / face-warp sold as dual silhouette Success.
_STRETCH_AS_VARIANT_TELLS: tuple[tuple[str, re.Pattern[str]], ...] = (
    (
        "face_corners_commit_family_mesh",
        re.compile(
            r"MakeShapeDistinctDualVariant[\s\S]{0,800}?FaceCornersLocal[\s\S]{0,400}?CommitDualFamilyMesh",
            re.M,
        ),
    ),
    (
        "scale_xz_independent",
        re.compile(
            r"\.Scale\s*=\s*new\s+Vector3\s*\([^)]*"
            r"(?:edgeLen|faceWidth|faceHeight|aspect|elongat|stretch)",
            re.I,
        ),
    ),
)

# over_neighbor_paint — flip refreshes more than four dual cells / uncapped incident set.
_OVER_NEIGHBOR_PAINT_TELLS: tuple[tuple[str, re.Pattern[str]], ...] = (
    (
        "update_four_uncapped_foreach",
        re.compile(
            r"UpdateFourDualSlots[\s\S]{0,900}?foreach\s*\(\s*var\s+\w+\s+in\s+faces\s*\)"
            r"(?![\s\S]{0,400}?(?:Take\s*\(\s*4\s*\)|MaxDualCellsPerLogicFlip|faces\.Count\s*>\s*4))",
            re.M,
        ),
    ),
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


def _flatten_law_text(value: Any) -> str:
    if value in (None, "", [], {}):
        return ""
    if isinstance(value, str):
        return value
    try:
        return yaml.dump(value, default_flow_style=True)
    except (TypeError, ValueError):
        return str(value)


def armed_requires_organic_quad_kernel(armed: dict[str, Any] | None) -> bool:
    """True when the armed packet declares Stålberg organic all-quad kernel law."""
    armed = armed if isinstance(armed, dict) else {}
    blob = " ".join(
        [
            str(armed.get("slice_id") or ""),
            str(armed.get("ask_id") or ""),
            str(armed.get("mode") or ""),
            str(armed.get("done_when") or ""),
            _flatten_law_text(armed.get("hard_prefer_gaps")),
        ]
    ).lower()
    if any(
        m in blob
        for m in (
            "stalberg",
            "organic_all_quad",
            "quad_kernel",
            "skip_dissolve_relax",
            "hex_scaffold_as_final_mesh",
        )
    ):
        return True
    locks = armed.get("locks") if isinstance(armed.get("locks"), dict) else {}
    step1 = locks.get("step1_authorship") if isinstance(locks.get("step1_authorship"), dict) else {}
    success = str(step1.get("structural_success") or "").lower()
    if "organic_all_quad" in success or "dissolve" in success and "relax" in success:
        return True
    refuse = list(armed.get("refuse_codes") or [])
    if isinstance(step1.get("refuse"), list):
        refuse.extend(step1.get("refuse") or [])
    return any(
        str(c) in ("hex_scaffold_as_final_mesh", "dual_overlay_as_grid_kernel", "skip_dissolve_relax")
        for c in refuse
    )


def scan_organic_quad_kernel_evidence(game_repo: Path) -> dict[str, Any]:
    """LIVE evidence for seed→tri→dissolve→subdivide→relax organic all-quad kernel."""
    evidence: dict[str, Any] = {
        "repo_present": game_repo.is_dir(),
        "files_scanned": [],
        "required_organic_files_present": [],
        "required_organic_files_absent": [],
        "pipeline_signals": [],
        "hex_scaffold_signals": [],
        "dual_as_kernel_signals": [],
        "noodle_render_signals": [],
        "has_seed": False,
        "has_triangulate": False,
        "has_dissolve": False,
        "has_subdivide": False,
        "has_relax": False,
        "has_flatten": False,
        "has_regenerate": False,
        "has_unique_topo": False,
        "has_get_or_add": False,
        "has_position_hash": False,
        "has_area_side": False,
        "has_clamp_force": False,
        "has_boundary_pin": False,
        "has_reweld": False,
        "has_organic_root": False,
        "ensure_host_builds_organic": False,
        "ensure_host_builds_hex_scaffold": False,
        "ensure_host_builds_dual_overlay": False,
    }
    if not game_repo.is_dir():
        return evidence

    candidates: list[Path] = []
    for rel in REQUIRED_LIVE_ORGANIC_QUAD_FILES:
        fp = game_repo / rel
        if fp.is_file():
            candidates.append(fp)
            evidence["required_organic_files_present"].append(rel)
        else:
            evidence["required_organic_files_absent"].append(rel)
    host = game_repo / "Systems/WorldgenCraft.cs"
    if host.is_file():
        candidates.append(host)

    seen: set[Path] = set()
    ensure_host_body = ""
    for fp in candidates:
        if fp in seen or not fp.is_file():
            continue
        seen.add(fp)
        rel = str(fp.relative_to(game_repo)).replace("\\", "/")
        evidence["files_scanned"].append(rel)
        raw = fp.read_text(encoding="utf-8", errors="replace")
        code = _code_only(raw)
        for name, pat in _ORGANIC_PIPELINE_SIGNALS:
            if pat.search(code):
                evidence["pipeline_signals"].append(f"{name}:{rel}")
        if "StalbergOrganicQuadMesh" in code or "BuildOrganicQuadVisuals" in code:
            evidence["has_organic_root"] = True
        if rel.endswith("OrganicQuadMesh.cs"):
            for name, pat in _ORGANIC_NOODLE_RENDER_SIGNALS:
                if pat.search(raw):
                    evidence["noodle_render_signals"].append(f"{name}:{rel}")
        if rel.endswith("DualGridCraftHost.cs"):
            m = re.search(
                r"public\s+Error\s+EnsureHost\s*\([^)]*\)\s*\{(.*?)\n\t\}",
                raw,
                re.S,
            )
            if m:
                ensure_host_body = m.group(1)
                evidence["ensure_host_builds_organic"] = bool(
                    re.search(r"BuildOrganicQuadVisuals\s*\(", ensure_host_body)
                )
                evidence["ensure_host_builds_hex_scaffold"] = bool(
                    re.search(r"BuildLatticeVisuals\s*\(", ensure_host_body)
                )
                evidence["ensure_host_builds_dual_overlay"] = bool(
                    re.search(r"BuildDualOffsetOverlay\s*\(", ensure_host_body)
                )
            for name, pat in _HEX_SCAFFOLD_PRIMARY_SIGNALS:
                if pat.search(ensure_host_body or ""):
                    evidence["hex_scaffold_signals"].append(f"{name}:{rel}")
            for name, pat in _DUAL_OVERLAY_AS_KERNEL_SIGNALS:
                if pat.search(ensure_host_body or ""):
                    evidence["dual_as_kernel_signals"].append(f"{name}:{rel}")
        if rel.endswith("WorldgenCraft.cs"):
            for name, pat in _DUAL_OVERLAY_AS_KERNEL_SIGNALS:
                if pat.search(code):
                    evidence["dual_as_kernel_signals"].append(f"{name}:{rel}")

    for key in (
        "files_scanned",
        "pipeline_signals",
        "hex_scaffold_signals",
        "dual_as_kernel_signals",
        "noodle_render_signals",
    ):
        evidence[key] = sorted(set(evidence[key]))
    sigs = evidence["pipeline_signals"]
    evidence["has_seed"] = any(s.startswith("seed:") for s in sigs)
    evidence["has_triangulate"] = any(s.startswith("triangulate:") for s in sigs)
    evidence["has_dissolve"] = any(s.startswith("dissolve:") for s in sigs)
    evidence["has_subdivide"] = any(s.startswith("subdivide:") for s in sigs)
    evidence["has_relax"] = any(s.startswith("relax:") for s in sigs)
    evidence["has_flatten"] = any(s.startswith("flatten:") for s in sigs)
    evidence["has_regenerate"] = any(s.startswith("regenerate:") for s in sigs)
    evidence["has_unique_topo"] = any(s.startswith("unique_topo:") for s in sigs)
    evidence["has_get_or_add"] = any(s.startswith("get_or_add:") for s in sigs)
    evidence["has_position_hash"] = any(s.startswith("position_hash:") for s in sigs)
    evidence["has_area_side"] = any(s.startswith("area_side:") for s in sigs)
    evidence["has_clamp_force"] = any(s.startswith("clamp_force:") for s in sigs)
    evidence["has_boundary_pin"] = any(s.startswith("boundary_pin:") for s in sigs)
    evidence["has_reweld"] = any(s.startswith("reweld:") for s in sigs)

    # Craft-plane authority (armed when slice/mode names craft_plane_authority).
    host_fp = game_repo / "Systems/DualGridCraftHost.cs"
    if host_fp.is_file():
        host_raw = host_fp.read_text(encoding="utf-8", errors="replace")
        host_code = _code_only(host_raw)
        evidence["has_try_pick_organic_face"] = bool(
            re.search(r"\bTryPickOrganicFace\b", host_code)
        )
        evidence["has_organic_face_cell"] = bool(
            re.search(r"\bFaceCell\b|OrganicQuadMesh\.FaceCell", host_code)
        )
        pick_body = ""
        m_pick = re.search(
            r"public\s+bool\s+TryPickHexCell\s*\([^)]*\)\s*\{(.*?)\n\t\}",
            host_raw,
            re.S,
        )
        if m_pick:
            pick_body = m_pick.group(1)
        evidence["hex19_snap_in_try_pick_hex"] = bool(
            re.search(r"Hex19OccupancyLattice\s*\.\s*TrySnapWorldToCell", pick_body)
        )
        m_org = re.search(
            r"public\s+bool\s+TryPickOrganicFace\s*\([^)]*\)\s*\{(.*?)\n\t\}",
            host_raw,
            re.S,
        )
        org_body = m_org.group(1) if m_org else ""
        evidence["hex19_snap_in_try_pick_organic"] = bool(
            re.search(r"Hex19OccupancyLattice\s*\.\s*TrySnapWorldToCell", org_body)
        )
        evidence["set_cell_fill_uses_organic"] = bool(
            re.search(
                r"SetCellFill[\s\S]{0,800}ContainsFace|FaceIndexFromCell",
                host_raw,
            )
        )
    else:
        evidence["has_try_pick_organic_face"] = False
        evidence["has_organic_face_cell"] = False
        evidence["hex19_snap_in_try_pick_hex"] = False
        evidence["hex19_snap_in_try_pick_organic"] = False
        evidence["set_cell_fill_uses_organic"] = False
    return evidence


def organic_quad_violations_from_evidence(evidence: dict[str, Any]) -> list[str]:
    """Map organic-quad LIVE gaps onto durable refuse codes."""
    violations: list[str] = []
    absent = list(evidence.get("required_organic_files_absent") or [])
    if absent:
        violations.append("skip_dissolve_relax:missing_organic_live_files:" + ",".join(absent))
    missing_bits: list[str] = []
    for bit, key in (
        ("seed", "has_seed"),
        ("triangulate", "has_triangulate"),
        ("dissolve", "has_dissolve"),
        ("subdivide", "has_subdivide"),
        ("relax", "has_relax"),
    ):
        if not evidence.get(key):
            missing_bits.append(bit)
    if missing_bits:
        violations.append("skip_dissolve_relax:missing:" + "+".join(missing_bits))
    if not evidence.get("has_regenerate"):
        violations.append("skip_dissolve_relax:missing:regenerate")
    if not evidence.get("has_organic_root") or not evidence.get("ensure_host_builds_organic"):
        violations.append("hex_scaffold_as_final_mesh:organic_primary_missing")
    if evidence.get("ensure_host_builds_hex_scaffold"):
        violations.append("hex_scaffold_as_final_mesh:ensure_host_builds_hex19")
    if evidence.get("ensure_host_builds_dual_overlay") or evidence.get("dual_as_kernel_signals"):
        violations.append(
            "dual_overlay_as_grid_kernel:"
            + ",".join(str(s) for s in (evidence.get("dual_as_kernel_signals") or [])[:4])
        )
    noodle = list(evidence.get("noodle_render_signals") or [])
    if noodle:
        if any(s.startswith("face_alpha") for s in noodle):
            violations.append(
                "extruded_prism_as_quad_board:" + ",".join(noodle[:4])
            )
            violations.append("noodle_edge_clutter:" + ",".join(noodle[:4]))
        if any(s.startswith("edge_alpha") for s in noodle):
            violations.append(
                "wireframe_spaghetti:"
                + ",".join(s for s in noodle if s.startswith("edge_alpha"))[:4]
            )
    # visual_r1 armed packets require FlattenToCraftPlane in LIVE.
    if not evidence.get("has_flatten"):
        violations.append("unbounded_z_jitter:missing:FlattenToCraftPlane")
        violations.append("nonplanar_face_soup:missing:FlattenToCraftPlane")
    # relax_r1 algorithm fidelity seats (Grok / Lerg).
    if not evidence.get("has_unique_topo") and not evidence.get("has_get_or_add"):
        violations.append("non_unique_vertices:missing:UniqueTopology2D|GetOrAddVertex")
    if not evidence.get("has_area_side"):
        violations.append("missing_square_area_force:missing:EstimateIdealSideFromArea")
    if evidence.get("has_relax") and not evidence.get("has_area_side"):
        violations.append("naive_laplacian_only:relax_without_area_square_side")
    if not evidence.get("has_boundary_pin"):
        violations.append("free_boundary_fold:missing:MarkBoundaryPinned")
    if not evidence.get("has_clamp_force"):
        violations.append("relax_step_too_hard:missing:ClampForce")
    if evidence.get("has_flatten") and evidence.get("has_relax"):
        # 2D flatten present with relax = extrusion_before_2d_stable not triggered.
        pass
    elif evidence.get("has_relax") and not evidence.get("has_flatten"):
        violations.append("extrusion_before_2d_stable:relax_without_flatten")
    return violations


def armed_requires_craft_plane_authority(armed: dict[str, Any] | None) -> bool:
    """True when Prefer packet is the craft-plane authority rebind seat."""
    armed = armed if isinstance(armed, dict) else {}
    blob = " ".join(
        [
            str(armed.get("slice_id") or ""),
            str(armed.get("mode") or ""),
            str(armed.get("done_when") or ""),
            _flatten_law_text(armed.get("hard_prefer_gaps")),
        ]
    ).lower()
    if "craft_plane_authority" in blob or "hex19_pick_as_craft_authority" in blob:
        return True
    refuse = list(armed.get("refuse_codes") or [])
    locks = armed.get("locks") if isinstance(armed.get("locks"), dict) else {}
    step1 = locks.get("step1_authorship") if isinstance(locks.get("step1_authorship"), dict) else {}
    if isinstance(step1.get("refuse"), list):
        refuse.extend(step1.get("refuse") or [])
    return "hex19_pick_as_craft_authority" in {str(c) for c in refuse}


def armed_requires_dual_corner_on_organic(armed: dict[str, Any] | None) -> bool:
    """True when Prefer binds dual-corner authorship onto OrganicQuadMesh."""
    armed = armed if isinstance(armed, dict) else {}
    blob = " ".join(
        [
            str(armed.get("slice_id") or ""),
            str(armed.get("mode") or ""),
            str(armed.get("ask_id") or ""),
            str(armed.get("done_when") or ""),
        ]
    ).lower()
    if "dual_corner" in blob and ("organic" in blob or "stalberg" in blob):
        return True
    locks = armed.get("locks") if isinstance(armed.get("locks"), dict) else {}
    return isinstance(locks.get("dual_corner"), dict) and bool(locks.get("dual_corner"))


def armed_requires_dual_neighborhood(armed: dict[str, Any] | None) -> bool:
    """True when Prefer requires stable dual-graph ownership per logic point."""
    armed = armed if isinstance(armed, dict) else {}
    blob = " ".join(
        [
            str(armed.get("slice_id") or ""),
            str(armed.get("mode") or ""),
            str(armed.get("ask_id") or ""),
            str(armed.get("done_when") or ""),
        ]
    ).lower()
    if (
        "dual_neighborhood" in blob
        or "fix_dual_neighborhood" in blob
        or "stable_four_cell" in blob
        or "unstable_dual_neighborhood" in blob
        or "stamp_as_dual" in blob
    ):
        return True
    locks = armed.get("locks") if isinstance(armed.get("locks"), dict) else {}
    if isinstance(locks.get("dual_neighborhood"), dict) and bool(locks.get("dual_neighborhood")):
        return True
    refuse = list(armed.get("refuse_codes") or [])
    step1 = locks.get("step1_authorship") if isinstance(locks.get("step1_authorship"), dict) else {}
    if isinstance(step1.get("refuse"), list):
        refuse.extend(step1.get("refuse") or [])
    return bool(
        {"unstable_dual_neighborhood", "stamp_as_dual", "primary_face_as_dual"}
        & {str(c) for c in refuse}
    )


def armed_requires_dual_lattice(armed: dict[str, Any] | None) -> bool:
    """True when Prefer requires half-step OrganicDualOffsetLattice (not primary-face dual)."""
    armed = armed if isinstance(armed, dict) else {}
    blob = " ".join(
        [
            str(armed.get("slice_id") or ""),
            str(armed.get("mode") or ""),
            str(armed.get("ask_id") or ""),
            str(armed.get("done_when") or ""),
        ]
    ).lower()
    if (
        "dual_lattice" in blob
        or "primary_face_as_dual" in blob
        or "fix_dual_lattice" in blob
        or "organicdualoffsetlattice" in blob.replace("_", "")
    ):
        return True
    locks = armed.get("locks") if isinstance(armed.get("locks"), dict) else {}
    if isinstance(locks.get("dual_lattice"), dict) and bool(locks.get("dual_lattice")):
        return True
    refuse = list(armed.get("refuse_codes") or [])
    step1 = locks.get("step1_authorship") if isinstance(locks.get("step1_authorship"), dict) else {}
    if isinstance(step1.get("refuse"), list):
        refuse.extend(step1.get("refuse") or [])
    return "primary_face_as_dual" in {str(c) for c in refuse}


def armed_requires_dual_object_identity(armed: dict[str, Any] | None) -> bool:
    """Organic dual Prefer altitudes that must prove OrganicDualOffsetLattice object identity.

    Covers neighborhood / lattice / visual / dual-corner. Excludes Hex19 tutorial
    ``step2_dual_offset`` (markers dual — still uses ``skip_dual_offset`` seat).
    """
    return (
        armed_requires_dual_corner_on_organic(armed)
        or armed_requires_dual_visual(armed)
        or armed_requires_dual_neighborhood(armed)
        or armed_requires_dual_lattice(armed)
        or (
            isinstance(armed, dict)
            and isinstance(armed.get("locks"), dict)
            and isinstance(armed["locks"].get("dual_object_identity"), dict)
            and bool(armed["locks"].get("dual_object_identity"))
        )
    )


def armed_requires_any_dual_prefer(armed: dict[str, Any] | None) -> bool:
    """True when any dual Prefer altitude is armed (organic identity or Hex19 s2 offset)."""
    return armed_requires_dual_object_identity(armed) or armed_requires_dual_offset(armed)


def resolve_authorship_conceptual_fields(
    armed: dict[str, Any] | None,
    step1_lock: dict[str, Any] | None = None,
) -> dict[str, str]:
    """Resolve structural_success + success_object (+ optional conceptual leg) from armed law."""
    armed = armed if isinstance(armed, dict) else {}
    step1 = step1_lock if isinstance(step1_lock, dict) else {}
    locks = armed.get("locks") if isinstance(armed.get("locks"), dict) else {}
    dual_id = (
        locks.get("dual_object_identity")
        if isinstance(locks.get("dual_object_identity"), dict)
        else {}
    )
    intent_lock = (
        locks.get("intent_validates_gates")
        if isinstance(locks.get("intent_validates_gates"), dict)
        else {}
    )
    conceptual = (
        armed.get("conceptual_leg")
        if isinstance(armed.get("conceptual_leg"), dict)
        else {}
    )

    structural = str(
        step1.get("structural_success")
        or armed.get("structural_success")
        or intent_lock.get("structural_success")
        or conceptual.get("structural_success")
        or ""
    ).strip()
    success_object = str(
        step1.get("success_object")
        or armed.get("success_object")
        or dual_id.get("success_object_required")
        or dual_id.get("success_object")
        or intent_lock.get("success_object")
        or conceptual.get("success_object")
        or ""
    ).strip()
    end_state = str(
        conceptual.get("end_state")
        or conceptual.get("project_end_state")
        or armed.get("end_state")
        or armed.get("project_end_state")
        or step1.get("end_state")
        or ""
    ).strip()
    path_position = str(
        conceptual.get("path_position")
        or armed.get("path_position")
        or step1.get("path_position")
        or ""
    ).strip()
    intent_invariant = str(
        conceptual.get("intent_invariant")
        or armed.get("intent_invariant")
        or step1.get("intent_invariant")
        or dual_id.get("intent_invariant")
        or ""
    ).strip()
    return {
        "structural_success": structural,
        "success_object": success_object,
        "end_state": end_state,
        "path_position": path_position,
        "intent_invariant": intent_invariant,
    }


def authorship_armed_missing_required_fields(
    armed: dict[str, Any] | None,
    step1_lock: dict[str, Any] | None = None,
) -> list[str]:
    """Fail closed when authorship/dual Prefer packets omit intent + success_object."""
    armed = armed if isinstance(armed, dict) else {}
    if not armed:
        return []
    # Authorship / dual Prefer product packets must declare intent fields.
    needs = bool(step1_lock) or armed_requires_any_dual_prefer(armed) or bool(
        armed.get("prefer_authorship")
        or (isinstance(armed.get("locks"), dict) and armed["locks"].get("intent_validates_gates"))
        or (isinstance(armed.get("locks"), dict) and armed["locks"].get("dual_object_identity"))
    )
    if not needs:
        return []
    fields = resolve_authorship_conceptual_fields(armed, step1_lock)
    violations: list[str] = []
    if not fields["structural_success"]:
        violations.append("armed_packet_missing_structural_success")
    if not fields["success_object"]:
        violations.append("armed_packet_missing_success_object")
    return violations



def organic_mesh_graph_success_object(success_object: str) -> bool:
    """True when named success_object is primal MeshGraph class."""
    s = (success_object or "").lower().replace("-", "_")
    return bool(s) and (
        "organic_mesh_graph" in s
        or s in ("mesh_graph", "primal_mesh_graph")
    )


def armed_requires_organic_mesh_graph(armed: dict[str, Any] | None) -> bool:
    """True when Prefer requires OrganicMeshGraph Vertex/Edge/Face singletons + incidence."""
    armed = armed if isinstance(armed, dict) else {}
    blob = " ".join(
        [
            str(armed.get("slice_id") or ""),
            str(armed.get("ask_id") or ""),
            str(armed.get("mode") or ""),
            str(armed.get("done_when") or ""),
            str(armed.get("success_object") or ""),
            _flatten_law_text(armed.get("hard_prefer_gaps")),
        ]
    ).lower()
    if any(
        m in blob
        for m in (
            "organic_mesh_graph",
            "primal_graph",
            "indexed_lists_as_graph",
            "ephemeral_edge_key_as_topology",
            "mesograph",
            "mesh_graph",
        )
    ):
        return True
    locks = armed.get("locks") if isinstance(armed.get("locks"), dict) else {}
    if isinstance(locks.get("organic_mesh_graph"), dict):
        return True
    refuse = list(armed.get("refuse_codes") or [])
    step1 = locks.get("step1_authorship") if isinstance(locks.get("step1_authorship"), dict) else {}
    if isinstance(step1.get("refuse"), list):
        refuse.extend(step1.get("refuse") or [])
    return bool(
        {"indexed_lists_as_graph", "ephemeral_edge_key_as_topology"}
        & {str(c) for c in refuse}
    )


MESH_GRAPH_DO_NOT_WAIVE: tuple[str, ...] = (
    "indexed_lists_as_graph",
    "ephemeral_edge_key_as_topology",
    "non_unique_vertices",
    "proxy_substitution",
    "intent_collapsed_to_mechanics",
)

_MESH_GRAPH_FILE_SIGNALS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("organic_mesh_graph_type", re.compile(r"\bclass\s+OrganicMeshGraph\b")),
    ("vertex_singleton", re.compile(r"\bclass\s+Vertex\b")),
    ("edge_singleton", re.compile(r"\bclass\s+Edge\b")),
    ("face_singleton", re.compile(r"\bclass\s+Face\b")),
    ("get_or_add_vertex", re.compile(r"\bGetOrAddVertex\b")),
    ("get_or_add_edge", re.compile(r"\bGetOrAddEdge\b")),
    ("add_quad", re.compile(r"\bAddQuad\b")),
    ("faces_touching_vertex", re.compile(r"\bFacesTouchingVertex\b")),
)

_MESH_GRAPH_REQUIRED_FILES = (
    "Core/WorldGen/OrganicMeshGraph.cs",
    "Core/WorldGen/OrganicQuadMesh.cs",
    "Core/WorldGen/StalbergQuadKernel.cs",
    "Core/WorldGen/OrganicDualOffsetLattice.cs",
    "Systems/DualGridCraftHost.cs",
)


def scan_organic_mesh_graph_evidence(game_repo: Path) -> dict[str, Any]:
    """LIVE evidence for primal MeshGraph singletons + incidence."""
    evidence: dict[str, Any] = {
        "repo_present": game_repo.is_dir(),
        "files_scanned": [],
        "required_present": [],
        "required_absent": [],
        "signals": [],
        "has_organic_mesh_graph": False,
        "has_get_or_add_vertex": False,
        "has_get_or_add_edge": False,
        "has_add_quad": False,
        "has_faces_touching_vertex": False,
        "has_vertex_edge_face": False,
        "oqm_wraps_graph": False,
        "kernel_emits_graph": False,
        "dual_corners_vertex_refs": False,
        "support_face_success_tells": [],
        "indexed_lists_as_graph": False,
        "ephemeral_edge_key_as_topology": False,
    }
    if not game_repo.is_dir():
        return evidence
    for rel in _MESH_GRAPH_REQUIRED_FILES:
        fp = game_repo / rel
        if fp.is_file():
            evidence["required_present"].append(rel)
        else:
            evidence["required_absent"].append(rel)
    for rel in _MESH_GRAPH_REQUIRED_FILES:
        fp = game_repo / rel
        if not fp.is_file():
            continue
        raw = fp.read_text(encoding="utf-8", errors="replace")
        code = _code_only(raw)
        evidence["files_scanned"].append(rel.replace("\\", "/"))
        for name, pat in _MESH_GRAPH_FILE_SIGNALS:
            if pat.search(code):
                evidence["signals"].append(f"{name}:{rel}")
        if rel.endswith("OrganicMeshGraph.cs"):
            evidence["has_organic_mesh_graph"] = "class OrganicMeshGraph" in code
            evidence["has_get_or_add_vertex"] = "GetOrAddVertex" in code
            evidence["has_get_or_add_edge"] = "GetOrAddEdge" in code
            evidence["has_add_quad"] = "AddQuad" in code
            evidence["has_faces_touching_vertex"] = "FacesTouchingVertex" in code
            evidence["has_vertex_edge_face"] = all(
                x in code for x in ("class Vertex", "class Edge", "class Face")
            )
            # Ephemeral long edge keys as sole topology = refuse (HashSet<long> without Edge class is UniqueTopology2D)
            if "class Edge" not in code and ("HashSet<long>" in code or "<< 32" in code):
                evidence["ephemeral_edge_key_as_topology"] = True
        if rel.endswith("OrganicQuadMesh.cs"):
            evidence["oqm_wraps_graph"] = (
                "OrganicMeshGraph" in code and ("Graph" in code or "AttachGraph" in code)
            )
        if rel.endswith("StalbergQuadKernel.cs"):
            evidence["kernel_emits_graph"] = (
                "OrganicMeshGraph.FromIndexedMesh" in code
                or "new OrganicQuadMesh(graph" in code
                or "new OrganicQuadMesh(graph," in code
            )
        if rel.endswith("OrganicDualOffsetLattice.cs"):
            evidence["dual_corners_vertex_refs"] = (
                "OrganicMeshGraph.Vertex" in code and "CornerVertices" in code
            )
            if re.search(r"SupportFaceIndex\s*[=;]", code) and "Obsolete" not in code:
                evidence["support_face_success_tells"].append(f"support_face_assign:{rel}")
        if rel.endswith("DualGridCraftHost.cs"):
            if "ProveOrganicMeshGraph" in code:
                evidence["signals"].append(f"prove_organic_mesh_graph:{rel}")
            if re.search(r"\.Take\s*\(\s*4\s*\)", code):
                evidence["support_face_success_tells"].append(f"soft_take_4:{rel}")
            if "_vertexToFaces" in code and "DEAD for dual Success" not in code and "NOT dual Success" not in raw:
                evidence["support_face_success_tells"].append(f"live_vertex_to_faces:{rel}")

    # Indexed lists as graph when MeshGraph type missing or kernel does not emit graph.
    if not evidence["has_organic_mesh_graph"] or not evidence["kernel_emits_graph"]:
        evidence["indexed_lists_as_graph"] = True
    if evidence["has_organic_mesh_graph"] and not evidence["has_get_or_add_edge"]:
        evidence["ephemeral_edge_key_as_topology"] = True
    return evidence


def organic_mesh_graph_violations_from_evidence(evidence: dict[str, Any]) -> list[str]:
    """Prefer violations for primal MeshGraph seat."""
    violations: list[str] = []
    if not evidence.get("repo_present"):
        violations.append("indexed_lists_as_graph:missing_game_repo")
        return violations
    if evidence.get("required_absent"):
        violations.append(
            "indexed_lists_as_graph:missing_files:"
            + ",".join(evidence["required_absent"])
        )
    if not evidence.get("has_organic_mesh_graph"):
        violations.append("indexed_lists_as_graph:missing:OrganicMeshGraph")
    if not evidence.get("has_vertex_edge_face"):
        violations.append("indexed_lists_as_graph:missing:Vertex|Edge|Face")
    if not evidence.get("has_get_or_add_vertex"):
        violations.append("non_unique_vertices:missing:GetOrAddVertex")
    if not evidence.get("has_get_or_add_edge"):
        violations.append("ephemeral_edge_key_as_topology:missing:GetOrAddEdge")
    if not evidence.get("has_add_quad"):
        violations.append("indexed_lists_as_graph:missing:AddQuad")
    if not evidence.get("has_faces_touching_vertex"):
        violations.append("indexed_lists_as_graph:missing:FacesTouchingVertex")
    if not evidence.get("oqm_wraps_graph"):
        violations.append("indexed_lists_as_graph:OrganicQuadMesh_missing_Graph_wrap")
    if not evidence.get("kernel_emits_graph"):
        violations.append("indexed_lists_as_graph:kernel_not_emitting_OrganicMeshGraph")
    if not evidence.get("dual_corners_vertex_refs"):
        violations.append("proxy_substitution:dual_corners_not_vertex_refs")
    if evidence.get("indexed_lists_as_graph"):
        violations.append("indexed_lists_as_graph:live_indexed_lists_without_mesh_graph")
    if evidence.get("ephemeral_edge_key_as_topology"):
        violations.append("ephemeral_edge_key_as_topology:edge_keys_without_Edge_singleton")
    for tell in evidence.get("support_face_success_tells") or []:
        if "soft_take_4" in str(tell):
            violations.append(f"intent_collapsed_to_mechanics:{tell}")
        elif "support_face" in str(tell):
            violations.append(f"primary_face_as_dual:{tell}")
    return violations


def dual_success_object_is_lattice_cell(success_object: str) -> bool:
    """True when named success_object is dual-lattice cell class (not primary face)."""
    s = (success_object or "").lower().replace("-", "_")
    if not s:
        return False
    if any(
        bad in s
        for bad in (
            "primary_organic_face",
            "primary_face",
            "org_face",
            "centroid_stamp",
        )
    ):
        return False
    return any(
        good in s
        for good in (
            "organic_dual_offset_lattice_cell",
            "dual_offset_lattice",
            "dual_lattice_cell",
            "dual_offset_cells",
            "dual_offset_cell",
            "half_step_dual",
        )
    )


def armed_requires_dual_visual(armed: dict[str, Any] | None) -> bool:
    """True when Prefer requires shape-distinct dual mesh variants (not gray ramp)."""
    armed = armed if isinstance(armed, dict) else {}
    locks = armed.get("locks") if isinstance(armed.get("locks"), dict) else {}
    dv = locks.get("dual_visual")
    # Explicit defer: neighborhood Prefer may keep dual_visual lock as deferred:true.
    if isinstance(dv, dict) and dv.get("deferred"):
        return False
    blob = " ".join(
        [
            str(armed.get("slice_id") or ""),
            str(armed.get("mode") or ""),
            str(armed.get("ask_id") or ""),
            str(armed.get("done_when") or ""),
        ]
    ).lower()
    if (
        "dual_visual" in blob
        or "meshlibrary_fidelity" in blob
        or "gray_ramp_only" in blob
        or "stretch_as_variant" in blob
    ):
        return True
    if isinstance(dv, dict) and bool(dv):
        return True
    refuse = list(armed.get("refuse_codes") or [])
    step1 = locks.get("step1_authorship") if isinstance(locks.get("step1_authorship"), dict) else {}
    if isinstance(step1.get("refuse"), list):
        refuse.extend(step1.get("refuse") or [])
    # over_neighbor_paint alone does not arm dual_visual (shared with neighborhood Prefer).
    return bool({"gray_ramp_only", "stretch_as_variant"} & {str(c) for c in refuse})


# Dual-visual Prefer must list these refuse codes in do_not_waive (armed guidance).
DUAL_VISUAL_DO_NOT_WAIVE: tuple[str, ...] = (
    "gray_ramp_only",
    "stretch_as_variant",
    "over_neighbor_paint",
    "inspiration_shape_miss",
)

# Dual-neighborhood Prefer — stable four-cell ownership before dual_visual art.
DUAL_NEIGHBORHOOD_DO_NOT_WAIVE: tuple[str, ...] = (
    "unstable_dual_neighborhood",
    "over_neighbor_paint",
    "stamp_as_dual",
    "primary_face_as_dual",
)

# Dual-lattice Prefer — half-step OrganicDualOffsetLattice; refuse primary_face_as_dual.
DUAL_LATTICE_DO_NOT_WAIVE: tuple[str, ...] = (
    "primary_face_as_dual",
    "skip_dual_offset",
    "unstable_dual_neighborhood",
    "over_neighbor_paint",
    "stamp_as_dual",
)


# Soft truncate / missing stable-set proof → unstable_dual_neighborhood.
_UNSTABLE_NEIGHBORHOOD_TELLS: tuple[tuple[str, re.Pattern[str]], ...] = (
    (
        "soft_take_after_over_neighbor_warn",
        re.compile(
            r"over_neighbor_paint[\s\S]{0,900}?faces\.Take\s*\(\s*MaxDualCellsPerLogicFlip\s*\)",
            re.M,
        ),
    ),
)

# Centroid / face-occupancy stamps sold as dual cells.
_STAMP_AS_DUAL_TELLS: tuple[tuple[str, re.Pattern[str]], ...] = (
    (
        "centroid_discrete_place",
        re.compile(
            r"PlaceDiscreteDualLibraryItem[\s\S]{0,900}?"
            r"(?:FaceCentroid|corners\[0\]\s*\+\s*corners\[1\]\s*\+\s*corners\[2\]\s*\+\s*corners\[3\])",
            re.M,
        ),
    ),
    (
        "face_paint_filled_plate",
        re.compile(
            r"SetCellFill[\s\S]{0,1200}?EnsureFilledOrganicFaceMesh",
            re.M,
        ),
    ),
)

_DUAL_NEIGHBORHOOD_SIGNALS: tuple[tuple[str, re.Pattern[str]], ...] = (
    (
        "prove_stable_neighborhood",
        re.compile(
            r"\bProveStable(?:Dual)?Neighborhood\b|\bProveDualNeighborhoodStability\b",
            re.I,
        ),
    ),
    (
        "debug_owned_dual_highlight",
        re.compile(
            r"\bRefreshDebugDualCellIds\b|\bDebugDualCellIds\b|"
            r"debug_highlight.*dual|dual.*debug_highlight",
            re.I,
        ),
    ),
    (
        "hard_refuse_over_neighbor",
        re.compile(
            r"(?:faces|owned|cells)\.Count\s*>\s*MaxDualCellsPerLogicFlip[\s\S]{0,200}?return\s+0",
            re.M,
        ),
    ),
    (
        "corner_owned_dual_geometry",
        re.compile(
            r"OrganicDualOffsetLattice|DualCellsTouching|MakeHalfStepDual|Varignon|"
            r"half.?step.*dual|dual.*half.?step",
            re.I,
        ),
    ),
)

# Primary-face neighborhood sold as dual (cyan 2×2 on organic faces).
_PRIMARY_FACE_AS_DUAL_TELLS: tuple[tuple[str, re.Pattern[str]], ...] = (
    (
        "org_face_index_dual_key",
        re.compile(
            r'org_\{|"org_"\s*\+|Name\s*=\s*\$?"DualCell_org_',
            re.I,
        ),
    ),
    (
        "vertex_to_faces_as_dual_ownership",
        re.compile(
            r"_vertexToFaces[\s\S]{0,1200}?OwnedDualFaceIndices|"
            r"OwnedDualFaceIndices[\s\S]{0,400}?_vertexToFaces",
            re.M,
        ),
    ),
    (
        "ensure_organic_dual_by_face_index",
        re.compile(
            r"EnsureOrganicDualCellMesh\s*\(\s*(?:int\s+)?faceIndex|"
            r"EnsureOrganicDualCellMesh\s*\(\s*fi\s*\)",
            re.I,
        ),
    ),
)

_DUAL_LATTICE_SIGNALS: tuple[tuple[str, re.Pattern[str]], ...] = (
    (
        "organic_dual_offset_lattice_type",
        re.compile(r"\bOrganicDualOffsetLattice\b", re.I),
    ),
    (
        "dual_cells_touching_api",
        re.compile(r"OrganicDualOffsetLattice\.DualCellsTouching|\bDualCellsTouching\b", re.I),
    ),
    (
        "half_step_offset_proof",
        re.compile(r"\bIsHalfStepOffset\b|MakeHalfStepDual|VarignonMidpoints", re.I),
    ),
    (
        "owned_dual_cell_keys",
        re.compile(r"\bOwnedDualCell(?:Keys|Ids)\b|LastOwnedDualCellsCsv", re.I),
    ),
)


def scan_dual_neighborhood_evidence(game_repo: Path) -> dict[str, Any]:
    """LIVE evidence: stable ≤4 ownership; dual cells not independent stamps."""
    evidence: dict[str, Any] = {
        "repo_present": game_repo.is_dir(),
        "files_scanned": [],
        "neighborhood_signals": [],
        "lattice_signals": [],
        "unstable_tells": [],
        "stamp_tells": [],
        "primary_face_tells": [],
        "has_prove_stable_neighborhood": False,
        "has_debug_owned_dual_highlight": False,
        "has_hard_refuse_over_neighbor": False,
        "has_organic_dual_offset_lattice": False,
        "has_dual_cells_touching": False,
        "has_half_step_offset_proof": False,
        "unstable_dual_neighborhood": False,
        "stamp_as_dual": False,
        "over_neighbor_paint": False,
        "primary_face_as_dual": False,
    }
    host = game_repo / "Systems" / "DualGridCraftHost.cs"
    lattice = game_repo / "Core" / "WorldGen" / "OrganicDualOffsetLattice.cs"
    texts: list[tuple[str, str, str]] = []
    if host.is_file():
        rel = "Systems/DualGridCraftHost.cs"
        evidence["files_scanned"].append(rel)
        raw = host.read_text(encoding="utf-8", errors="replace")
        texts.append((rel, raw, _code_only(raw)))
    if lattice.is_file():
        rel = "Core/WorldGen/OrganicDualOffsetLattice.cs"
        evidence["files_scanned"].append(rel)
        raw = lattice.read_text(encoding="utf-8", errors="replace")
        texts.append((rel, raw, _code_only(raw)))
    if not texts:
        return evidence
    for rel, raw, code in texts:
        for name, pat in _DUAL_NEIGHBORHOOD_SIGNALS:
            if pat.search(code) or pat.search(raw):
                evidence["neighborhood_signals"].append(f"{name}:{rel}")
        for name, pat in _DUAL_LATTICE_SIGNALS:
            if pat.search(code) or pat.search(raw):
                evidence["lattice_signals"].append(f"{name}:{rel}")
        for name, pat in _UNSTABLE_NEIGHBORHOOD_TELLS:
            if pat.search(code) or pat.search(raw):
                evidence["unstable_tells"].append(f"{name}:{rel}")
        for name, pat in _STAMP_AS_DUAL_TELLS:
            if pat.search(code) or pat.search(raw):
                evidence["stamp_tells"].append(f"{name}:{rel}")
        for name, pat in _PRIMARY_FACE_AS_DUAL_TELLS:
            if pat.search(code) or pat.search(raw):
                evidence["primary_face_tells"].append(f"{name}:{rel}")
    evidence["neighborhood_signals"] = sorted(set(evidence["neighborhood_signals"]))
    evidence["lattice_signals"] = sorted(set(evidence["lattice_signals"]))
    evidence["unstable_tells"] = sorted(set(evidence["unstable_tells"]))
    evidence["stamp_tells"] = sorted(set(evidence["stamp_tells"]))
    evidence["primary_face_tells"] = sorted(set(evidence["primary_face_tells"]))
    sigs = evidence["neighborhood_signals"]
    lsigs = evidence["lattice_signals"]
    evidence["has_prove_stable_neighborhood"] = any(
        s.startswith("prove_stable_neighborhood:") for s in sigs
    )
    evidence["has_debug_owned_dual_highlight"] = any(
        s.startswith("debug_owned_dual_highlight:") for s in sigs
    )
    evidence["has_hard_refuse_over_neighbor"] = any(
        s.startswith("hard_refuse_over_neighbor:") for s in sigs
    )
    evidence["has_organic_dual_offset_lattice"] = any(
        s.startswith("organic_dual_offset_lattice_type:") for s in lsigs
    ) or (game_repo / "Core" / "WorldGen" / "OrganicDualOffsetLattice.cs").is_file()
    evidence["has_dual_cells_touching"] = any(
        s.startswith("dual_cells_touching_api:") for s in lsigs
    )
    evidence["has_half_step_offset_proof"] = any(
        s.startswith("half_step_offset_proof:") for s in lsigs
    )
    evidence["unstable_dual_neighborhood"] = bool(evidence["unstable_tells"]) or not evidence[
        "has_prove_stable_neighborhood"
    ]
    evidence["stamp_as_dual"] = bool(evidence["stamp_tells"])
    evidence["over_neighbor_paint"] = not evidence["has_hard_refuse_over_neighbor"]
    # Primary-face-as-dual: face-index dual ownership without organic dual-offset lattice.
    evidence["primary_face_as_dual"] = bool(evidence["primary_face_tells"]) and not (
        evidence["has_organic_dual_offset_lattice"]
        and evidence["has_dual_cells_touching"]
        and evidence["has_half_step_offset_proof"]
    )
    return evidence


def dual_neighborhood_violations_from_evidence(
    evidence: dict[str, Any], *, require_dual_lattice: bool = False
) -> list[str]:
    """Map dual-neighborhood LIVE gaps onto durable refuse codes (non-waivable)."""
    violations: list[str] = []
    if not evidence.get("has_prove_stable_neighborhood"):
        violations.append("unstable_dual_neighborhood:missing:ProveStableDualNeighborhood")
    if evidence.get("unstable_dual_neighborhood"):
        if evidence.get("unstable_tells"):
            violations.append(
                "unstable_dual_neighborhood:tells:"
                + ",".join(str(s) for s in (evidence.get("unstable_tells") or [])[:4])
            )
    if not evidence.get("has_debug_owned_dual_highlight"):
        violations.append("unstable_dual_neighborhood:missing:debug_owned_dual_highlight")
    if evidence.get("stamp_as_dual"):
        violations.append(
            "stamp_as_dual:tells:"
            + ",".join(str(s) for s in (evidence.get("stamp_tells") or [])[:4])
        )
    if evidence.get("over_neighbor_paint"):
        violations.append("over_neighbor_paint:missing:hard_return_0_on_incident_gt_4")
    if require_dual_lattice:
        if not evidence.get("has_organic_dual_offset_lattice"):
            violations.append("primary_face_as_dual:missing:OrganicDualOffsetLattice")
        if not evidence.get("has_dual_cells_touching"):
            violations.append("primary_face_as_dual:missing:DualCellsTouching")
        if not evidence.get("has_half_step_offset_proof"):
            violations.append("primary_face_as_dual:missing:IsHalfStepOffset_or_MakeHalfStepDual")
        if evidence.get("primary_face_as_dual"):
            violations.append(
                "primary_face_as_dual:tells:"
                + ",".join(str(s) for s in (evidence.get("primary_face_tells") or [])[:4])
            )
    return violations


def scan_dual_visual_evidence(game_repo: Path) -> dict[str, Any]:
    """LIVE evidence: discrete silhouettes + ≤4 neighborhood; not gray ramp / stretch."""
    evidence: dict[str, Any] = {
        "repo_present": game_repo.is_dir(),
        "files_scanned": [],
        "dual_visual_signals": [],
        "gray_ramp_tells": [],
        "stretch_tells": [],
        "over_neighbor_tells": [],
        "has_shape_distinct": False,
        "has_four_families": False,
        "has_prove_dual_visual": False,
        "has_discrete_library_place": False,
        "has_neighborhood_cardinality_gate": False,
        "gray_ramp_only": False,
        "stretch_as_variant": False,
        "over_neighbor_paint": False,
    }
    host = game_repo / "Systems" / "DualGridCraftHost.cs"
    if not host.is_file():
        return evidence
    rel = "Systems/DualGridCraftHost.cs"
    evidence["files_scanned"].append(rel)
    raw = host.read_text(encoding="utf-8", errors="replace")
    code = _code_only(raw)
    for name, pat in _DUAL_VISUAL_SIGNALS:
        if pat.search(code) or pat.search(raw):
            evidence["dual_visual_signals"].append(f"{name}:{rel}")
    for name, pat in _GRAY_RAMP_ONLY_TELLS:
        if pat.search(raw):
            evidence["gray_ramp_tells"].append(f"{name}:{rel}")
    for name, pat in _STRETCH_AS_VARIANT_TELLS:
        if pat.search(code) or pat.search(raw):
            evidence["stretch_tells"].append(f"{name}:{rel}")
    for name, pat in _OVER_NEIGHBOR_PAINT_TELLS:
        if pat.search(code) or pat.search(raw):
            evidence["over_neighbor_tells"].append(f"{name}:{rel}")
    evidence["dual_visual_signals"] = sorted(set(evidence["dual_visual_signals"]))
    evidence["gray_ramp_tells"] = sorted(set(evidence["gray_ramp_tells"]))
    evidence["stretch_tells"] = sorted(set(evidence["stretch_tells"]))
    evidence["over_neighbor_tells"] = sorted(set(evidence["over_neighbor_tells"]))
    sigs = evidence["dual_visual_signals"]
    evidence["has_shape_distinct"] = any(
        s.startswith("shape_distinct_builder:") or s.startswith("shape_distinct_meshlibrary:")
        for s in sigs
    )
    evidence["has_four_families"] = any(
        s.startswith("dual_visual_family_enum:") or s.startswith("family_empty_edge_corner_full:")
        for s in sigs
    )
    evidence["has_prove_dual_visual"] = any(s.startswith("prove_dual_visual:") for s in sigs)
    evidence["has_discrete_library_place"] = any(
        s.startswith("discrete_library_place:") for s in sigs
    )
    evidence["has_neighborhood_cardinality_gate"] = any(
        s.startswith("neighborhood_cardinality_gate:") for s in sigs
    )
    # Gray-ramp Success tell: Library null / old source / DualFamilyColor still drives organic dual.
    evidence["gray_ramp_only"] = bool(evidence["gray_ramp_tells"]) and not evidence["has_shape_distinct"]
    # Stretch Success tell: face-warped family mesh OR non-uniform Scale without discrete place.
    evidence["stretch_as_variant"] = bool(evidence["stretch_tells"]) and not evidence[
        "has_discrete_library_place"
    ]
    # Over-neighbor: uncapped foreach without cardinality gate signal.
    evidence["over_neighbor_paint"] = bool(evidence["over_neighbor_tells"]) and not evidence[
        "has_neighborhood_cardinality_gate"
    ]
    return evidence


def dual_visual_violations_from_evidence(evidence: dict[str, Any]) -> list[str]:
    """Map dual-visual LIVE gaps onto durable refuse codes (non-waivable)."""
    violations: list[str] = []
    if not evidence.get("has_shape_distinct"):
        violations.append("gray_ramp_only:missing:MakeShapeDistinctDualVariant")
    if not evidence.get("has_four_families"):
        violations.append("gray_ramp_only:missing:DualVisualFamily_empty_edge_corner_full")
    if not evidence.get("has_prove_dual_visual"):
        violations.append("gray_ramp_only:missing:ProveDualVisualVariants")
    if evidence.get("gray_ramp_only"):
        violations.append(
            "gray_ramp_only:tells:"
            + ",".join(str(s) for s in (evidence.get("gray_ramp_tells") or [])[:4])
        )
    if not evidence.get("has_discrete_library_place"):
        violations.append("stretch_as_variant:missing:PlaceDiscreteDualLibraryItem")
    if evidence.get("stretch_as_variant"):
        violations.append(
            "stretch_as_variant:tells:"
            + ",".join(str(s) for s in (evidence.get("stretch_tells") or [])[:4])
        )
    if not evidence.get("has_neighborhood_cardinality_gate"):
        violations.append("over_neighbor_paint:missing:MaxDualCellsPerLogicFlip")
    if evidence.get("over_neighbor_paint"):
        violations.append(
            "over_neighbor_paint:tells:"
            + ",".join(str(s) for s in (evidence.get("over_neighbor_tells") or [])[:4])
        )
    return violations


def craft_plane_authority_violations_from_evidence(evidence: dict[str, Any]) -> list[str]:
    """Refuse Hex19-owned pick/paint when craft-plane authority Prefer is armed."""
    violations: list[str] = []
    if not evidence.get("has_try_pick_organic_face"):
        violations.append("hex19_pick_as_craft_authority:missing:TryPickOrganicFace")
    if not evidence.get("has_organic_face_cell") and not evidence.get("set_cell_fill_uses_organic"):
        violations.append("hex19_pick_as_craft_authority:missing:FaceCell|ContainsFace")
    if evidence.get("hex19_snap_in_try_pick_hex") or evidence.get("hex19_snap_in_try_pick_organic"):
        violations.append("hex19_pick_as_craft_authority:TrySnapWorldToCell_still_in_pick")
    return violations


def armed_requires_dual_offset(armed: dict[str, Any] | None) -> bool:
    """True when the armed packet declares step-2 dual-offset law."""
    armed = armed if isinstance(armed, dict) else {}
    locks = armed.get("locks") if isinstance(armed.get("locks"), dict) else {}
    step2 = locks.get("step2_dual_offset") or armed.get("step2_dual_offset")
    if isinstance(step2, dict) and step2:
        return True
    blob = " ".join(
        [
            str(armed.get("slice_id") or ""),
            str(armed.get("mode") or ""),
            str(armed.get("tutorial_step") or ""),
        ]
    ).lower()
    return any(
        m in blob
        for m in ("dual_offset", "tutorial_s2", "half_offset", "update_four")
    )


def scan_dual_offset_evidence(game_repo: Path) -> dict[str, Any]:
    """LIVE evidence that s2 dual is corner-driven half-offset quads, not markers."""
    evidence: dict[str, Any] = {
        "repo_present": game_repo.is_dir(),
        "files_scanned": [],
        "required_dual_files_present": [],
        "required_dual_files_absent": [],
        "dual_signals": [],
        "markers_only_signals": [],
        "has_update_four": False,
        "has_corner_reads": False,
        "has_half_offset": False,
        "has_dual_toggle": False,
        "markers_only": False,
    }
    if not game_repo.is_dir():
        return evidence

    candidates: list[Path] = []
    for rel in REQUIRED_LIVE_DUAL_FILES:
        fp = game_repo / rel
        if fp.is_file():
            candidates.append(fp)
            evidence["required_dual_files_present"].append(rel)
        else:
            evidence["required_dual_files_absent"].append(rel)

    seen: set[Path] = set()
    for fp in candidates:
        if fp in seen or not fp.is_file():
            continue
        seen.add(fp)
        rel = str(fp.relative_to(game_repo)).replace("\\", "/")
        evidence["files_scanned"].append(rel)
        code = _code_only(fp.read_text(encoding="utf-8", errors="replace"))
        for name, pat in _DUAL_OFFSET_SIGNALS:
            if pat.search(code):
                evidence["dual_signals"].append(f"{name}:{rel}")
        for name, pat in _DUAL_MARKERS_ONLY_SIGNALS:
            if pat.search(code):
                evidence["markers_only_signals"].append(f"{name}:{rel}")

    for key in ("files_scanned", "dual_signals", "markers_only_signals"):
        evidence[key] = sorted(set(evidence[key]))
    sigs = evidence["dual_signals"]
    evidence["has_update_four"] = any(s.startswith("update_four_api:") or s.startswith("dual_cells_touching:") for s in sigs)
    evidence["has_corner_reads"] = any(s.startswith("corner_occupancy:") for s in sigs)
    evidence["has_half_offset"] = any(s.startswith("half_step_offset:") for s in sigs)
    evidence["has_dual_toggle"] = any(s.startswith("dual_overlay_toggle:") for s in sigs)
    # Spray formula in Prove* as a refuse check is OK; only flag when update-four API absent.
    evidence["markers_only"] = bool(evidence["markers_only_signals"]) and not evidence["has_update_four"]
    return evidence


def dual_offset_violations_from_evidence(evidence: dict[str, Any]) -> list[str]:
    """Map dual-offset LIVE gaps onto skip_dual_offset (non-waivable on s2)."""
    violations: list[str] = []
    absent = list(evidence.get("required_dual_files_absent") or [])
    if absent:
        violations.append("skip_dual_offset:missing_dual_live_files:" + ",".join(absent))
    missing_bits: list[str] = []
    if not evidence.get("has_update_four"):
        missing_bits.append("update_four")
    if not evidence.get("has_corner_reads"):
        missing_bits.append("four_corner_reads")
    if not evidence.get("has_half_offset"):
        missing_bits.append("half_step_offset")
    if not evidence.get("has_dual_toggle"):
        missing_bits.append("dual_overlay_toggle")
    if missing_bits:
        violations.append("skip_dual_offset:missing:" + "+".join(missing_bits))
    if evidence.get("markers_only"):
        violations.append(
            "skip_dual_offset:markers_only:"
            + ",".join(str(s) for s in (evidence.get("markers_only_signals") or [])[:4])
        )
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

    # Intent-validates-gates: authorship/dual armed packets require intent + object class.
    conceptual_fields = resolve_authorship_conceptual_fields(armed, step1_lock)
    violations.extend(authorship_armed_missing_required_fields(armed, step1_lock))

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

    # Stålberg organic all-quad LIVE heuristics — Prefer must not green hex-primary
    # or dual-overlay-on-hex when the armed packet declares organic kernel law.
    organic_evidence: dict[str, Any] | None = None
    if armed_requires_organic_quad_kernel(armed) and repo is not None:
        organic_evidence = scan_organic_quad_kernel_evidence(repo)
        organic_viols = organic_quad_violations_from_evidence(organic_evidence)
        if armed_requires_dual_corner_on_organic(armed):
            organic_viols = [
                v for v in organic_viols if not str(v).startswith("dual_overlay_as_grid_kernel")
            ]
        violations.extend(organic_viols)
        if armed_requires_craft_plane_authority(armed):
            violations.extend(craft_plane_authority_violations_from_evidence(organic_evidence))
        if topology_evidence is not None:
            topology_evidence = {**topology_evidence, "organic_quad_kernel": organic_evidence}
        else:
            topology_evidence = {"organic_quad_kernel": organic_evidence}

    # s2 dual-offset LIVE heuristics — Prefer must not green on s1 topology alone
    # when the armed packet declares step2_dual_offset / dual half-offset law.
    # Skip when organic-quad Prefer owns the seat (dual is next slice / refuse).
    dual_evidence: dict[str, Any] | None = None
    if (
        (
            armed_requires_dual_offset(armed)
            and not armed_requires_organic_quad_kernel(armed)
        )
        or armed_requires_dual_corner_on_organic(armed)
        or armed_requires_dual_visual(armed)
    ) and repo is not None:
        dual_evidence = scan_dual_offset_evidence(repo)
        violations.extend(dual_offset_violations_from_evidence(dual_evidence))
        if topology_evidence is not None:
            topology_evidence = {**topology_evidence, "dual_offset": dual_evidence}
        else:
            topology_evidence = {"dual_offset": dual_evidence}

    # Dual-visual fidelity — shape-distinct empty/edge/corner/full; refuse gray_ramp_only.
    dual_visual_evidence: dict[str, Any] | None = None
    if armed_requires_dual_visual(armed) and repo is not None:
        dual_visual_evidence = scan_dual_visual_evidence(repo)
        violations.extend(dual_visual_violations_from_evidence(dual_visual_evidence))
        if topology_evidence is not None:
            topology_evidence = {**topology_evidence, "dual_visual": dual_visual_evidence}
        else:
            topology_evidence = {"dual_visual": dual_visual_evidence}

    # Primal MeshGraph Prefer — Vertex/Edge/Face singletons + incidence.
    mesh_graph_evidence: dict[str, Any] | None = None
    if armed_requires_organic_mesh_graph(armed) and repo is not None:
        mesh_graph_evidence = scan_organic_mesh_graph_evidence(repo)
        mesh_viols = organic_mesh_graph_violations_from_evidence(mesh_graph_evidence)
        violations.extend(mesh_viols)
        so = conceptual_fields.get("success_object") or ""
        claimed_so = str(armed.get("success_object") or so)
        # SO identity only when this Prefer claims organic_mesh_graph as Success.
        # dual_rebind / dual_offset_cells may preserve MeshGraph without re-claiming it.
        if organic_mesh_graph_success_object(claimed_so) and so and not organic_mesh_graph_success_object(so):
            violations.append(f"proxy_substitution:success_object_not_organic_mesh_graph:{so}")
            violations.append(f"intent_collapsed_to_mechanics:success_object_proxy:{so}")
        if topology_evidence is not None:
            topology_evidence = {
                **topology_evidence,
                "organic_mesh_graph": mesh_graph_evidence,
                "conceptual_fields": conceptual_fields,
            }
        else:
            topology_evidence = {
                "organic_mesh_graph": mesh_graph_evidence,
                "conceptual_fields": conceptual_fields,
            }

    # Dual-neighborhood / organic dual Prefer — stable ≤4 ownership; refuse stamp_as_dual.
    # Organic dual altitudes always require dual-offset lattice proof (no detect-only neighborhood).
    dual_neighborhood_evidence: dict[str, Any] | None = None
    dual_object_identity = armed_requires_dual_object_identity(armed)
    if (
        armed_requires_dual_neighborhood(armed)
        or armed_requires_dual_lattice(armed)
        or dual_object_identity
    ) and repo is not None:
        dual_neighborhood_evidence = scan_dual_neighborhood_evidence(repo)
        # Intent-validates-gates: organic dual altitudes always require lattice proof.
        require_lattice = dual_object_identity or armed_requires_dual_lattice(armed)
        dual_viols = dual_neighborhood_violations_from_evidence(
            dual_neighborhood_evidence,
            require_dual_lattice=require_lattice,
        )
        violations.extend(dual_viols)
        # Parent class emit when wrong-object / proxy stand-in is detected.
        if any(
            str(v).startswith("primary_face_as_dual")
            or str(v).startswith("stamp_as_dual")
            or str(v).startswith("points_as_grid")
            or str(v).startswith("stretch_as_variant")
            for v in dual_viols
        ):
            violations.append("proxy_substitution:wrong_object_or_proxy_stand_in")
        if require_lattice and dual_neighborhood_evidence.get("primary_face_as_dual"):
            violations.append("intent_collapsed_to_mechanics:stable_metric_of_wrong_object")
        # success_object mismatch — dual Prefer naming primary face as Success.
        so = conceptual_fields.get("success_object") or ""
        if so and dual_object_identity and not dual_success_object_is_lattice_cell(so):
            if any(
                bad in so.lower()
                for bad in ("primary_face", "primary_organic", "org_face", "centroid")
            ):
                violations.append(
                    f"proxy_substitution:success_object_not_dual_lattice:{so}"
                )
                violations.append(
                    f"intent_collapsed_to_mechanics:success_object_proxy:{so}"
                )
        if topology_evidence is not None:
            topology_evidence = {
                **topology_evidence,
                "dual_neighborhood": dual_neighborhood_evidence,
                "conceptual_fields": conceptual_fields,
            }
        else:
            topology_evidence = {
                "dual_neighborhood": dual_neighborhood_evidence,
                "conceptual_fields": conceptual_fields,
            }

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
        if armed_requires_dual_offset(armed) and not armed_requires_organic_quad_kernel(
            armed
        ) and "skip_dual_offset" not in {str(x) for x in do_not_waive}:
            violations.append("prefer_overlay_missing_do_not_waive_dual_codes:skip_dual_offset")
        if armed_requires_dual_visual(armed):
            missing_dual_visual = [
                c
                for c in DUAL_VISUAL_DO_NOT_WAIVE
                if c not in {str(x) for x in do_not_waive}
            ]
            if missing_dual_visual:
                violations.append(
                    "prefer_overlay_missing_do_not_waive_dual_codes:"
                    + ",".join(missing_dual_visual)
                )
        if (
            armed_requires_dual_neighborhood(armed)
            or armed_requires_dual_lattice(armed)
            or dual_object_identity
        ):
            missing_neighborhood = [
                c
                for c in DUAL_NEIGHBORHOOD_DO_NOT_WAIVE
                if c not in {str(x) for x in do_not_waive}
            ]
            if missing_neighborhood:
                violations.append(
                    "prefer_overlay_missing_do_not_waive_dual_codes:"
                    + ",".join(missing_neighborhood)
                )
        if armed_requires_dual_lattice(armed) or dual_object_identity:
            missing_lattice = [
                c
                for c in DUAL_LATTICE_DO_NOT_WAIVE
                if c not in {str(x) for x in do_not_waive}
            ]
            if missing_lattice:
                violations.append(
                    "prefer_overlay_missing_do_not_waive_dual_codes:"
                    + ",".join(missing_lattice)
                )
        # Intent-validates-gates parent class always non-waivable on Prefer overlays.
        missing_intent = [
            c
            for c in INTENT_VALIDATES_DO_NOT_WAIVE
            if c not in {str(x) for x in do_not_waive}
        ]
        if missing_intent and (
            armed
            or job.get("prefer_authorship")
            or dual_object_identity
            or conceptual_fields.get("success_object")
        ):
            violations.append(
                "prefer_overlay_missing_do_not_waive_intent_codes:"
                + ",".join(missing_intent)
            )
        if armed_requires_organic_mesh_graph(armed):
            missing_mesh_graph = [
                c
                for c in MESH_GRAPH_DO_NOT_WAIVE
                if c not in {str(x) for x in do_not_waive}
            ]
            if missing_mesh_graph:
                violations.append(
                    "prefer_overlay_missing_do_not_waive_mesh_graph_codes:"
                    + ",".join(missing_mesh_graph)
                )
        if armed_requires_organic_quad_kernel(armed):
            missing_organic = [
                c
                for c in (
                    "hex_scaffold_as_final_mesh",
                    "dual_overlay_as_grid_kernel",
                    "skip_dissolve_relax",
                )
                if c not in {str(x) for x in do_not_waive}
            ]
            if missing_organic:
                violations.append(
                    "prefer_overlay_missing_do_not_waive_organic_codes:"
                    + ",".join(missing_organic)
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
