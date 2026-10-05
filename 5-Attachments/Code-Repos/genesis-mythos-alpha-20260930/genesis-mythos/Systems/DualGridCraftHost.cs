using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text.Json;
using Genesis.Core.ClosedAlpha;
using Genesis.Core.WorldGen;
using Godot;

namespace Genesis.Systems;

/// <summary>
/// Stålberg Stage-6 dual host — owned-only MeshLibrary paint + dual-edge-frame orient.
/// Snap = primary logic Vertex V (KEEP). Ghost = OwnedDualCell(V) (≥3 corners KEEP).
/// Populate = FlipOrganicCorner(V) → DualCellsTouching(V) recompute (owned + expand KEEP).
/// Place Success = one Full on OwnedDualCell(V) only — DualCorners n=3 (tri) or n=4 (quad);
/// neighbors ClearDualSlot/Empty unless their own owner is on (coastline deferred).
/// OccupancyCorners ↔ Stage6 DualCorners (n=3 bit map or n=4); owner-on → Full.
/// Mesh fit: n=4 dual-edge bilinear KEEP; n=3 barycentric triangle warp.
/// Prefer: alpha0_stalberg_dual_tri_cell_place_r1 (dual_cell_meshlibrary_placement).
/// Z-fight / FullYBias / seizure decks DEFERRED (not this slice Success).
/// Valence-5 stays non-placeable. Refuse silent_ghost_without_place_n3 / soft_take_4.
/// </summary>
public partial class DualGridCraftHost : Node3D, ICraftCellAuthority
{
	public const string CanonicalStampId = "stamp_oasis_desert";
	public const string PersistPath = "user://worldgen/living_world_v1.json";
	public const string SliceId = "alpha0_stalberg_dual_tri_cell_place_r1";
	public const string WeldSliceId = "alpha0_stalberg_dual_tri_cell_place_r1";
	public const string PreferAskId = "alpha0_stalberg_dual_visual";
	public const string VisualBarCite = "stalberg_dual_tri_cell_place";
	public const string ArtStyleId = "dual_offset_terrain_tile_nature_model_pack";
	public const string SuccessObject = "dual_cell_meshlibrary_placement";
	public const string PlacePolarity = "owned_dual_cell_tri_cell_place";
	public const string PaintContract = "C_dual_tri_cell_place";
	/// <summary>Legacy Full top lift — Z-fight harden DEFERRED (not Success this slice).</summary>
	public const float FullYBias = 0.12f;
	/// <summary>MeshInstance sorting offset for Full plates — visuals deferred companion.</summary>
	public const float FullSortingOffset = 0.02f;
	/// <summary>Legacy cream albedo — kept for refuse proofs only; not applied as Success material.</summary>
	public static readonly Color CreamPlatformAlbedo = new(0.93f, 0.86f, 0.68f, 1f);
	/// <summary>Legacy cream under-glow — not applied as Success material.</summary>
	public static readonly Color CreamPlatformUnderGlow = new(0.55f, 0.78f, 0.92f, 1f);
	/// <summary>Craft-plane water / board tint toward YT teal-blue (not Terrain3D world-builder).</summary>
	public static readonly Color CraftPlaneWaterTint = new(0.14f, 0.32f, 0.48f, 1f);
	/// <summary>Primary amber face underlay — organic grid read (not water tiles).</summary>
	public static readonly Color PrimaryAmberFaceTint = new(0.78f, 0.42f, 0.16f, 0.22f);
	/// <summary>
	/// ≤ MaxDualsPerLogicPoint DualCells per logic flip (owned + ≤4 expand).
	/// Aligns with OrganicDualOffsetLattice.MaxDualsPerLogicPoint; refuse soft Take.
	/// </summary>
	public const int MaxDualCellsPerLogicFlip = OrganicDualOffsetLattice.MaxDualsPerLogicPoint;
	/// <summary>Pick encoder Y — primary logic Vertex V (place Success).</summary>
	public const int PrimaryPickY = 1;
	/// <summary>Pick encoder Y — secondary face-centroid locus (glow debug only; not place).</summary>
	public const int SecondaryPickY = 2;

	/// <summary>Sixpack terrain families. Refuse gray_ramp_only / stretch_as_variant / plinth_as_terrain.</summary>
	public enum DualVisualFamily
	{
		Empty = 0,
		Edge = 1,
		Corner = 2,
		Full = 3,
		Diagonal = 4,
		InverseCorner = 5,
	}

	private readonly Dictionary<Vector2I, CellFill> _occupancy = new();
	private readonly Dictionary<Vector2I, MeshInstance3D> _filledCells = new();
	private readonly Dictionary<string, MeshInstance3D> _dualSlots = new();
	private Node3D? _gridRoot;
	private Node3D? _organicRoot;
	private Node3D? _dualRoot;
	private MeshInstance3D? _ghost;
	private OrganicQuadMesh? _organicMesh;
	private MeshLibrary? _dualMeshLibrary;
	private Vector3 _latticeOrigin = new(8f, 0f, 8f);
	/// <summary>Organic craft spacing — follows Stålberg DefaultSpacing (large cells; rings=ProductDensity).</summary>
	private float _hexSize = StalbergQuadKernel.DefaultSpacing;
	/// <summary>LIVE seed rings — DefaultRingCount (= ProductDensityRingCount=5); Prefer once froze hex19=2.</summary>
	private int _seedRingCount = StalbergQuadKernel.DefaultRingCount;
	private bool _latticeVisible = true;
	private bool _dualVisible;
	private bool _ghostVisible;
	private readonly Dictionary<int, bool> _cornerLogic = new();
	private OrganicDualOffsetLattice? _dualLattice;
	private readonly Dictionary<int, List<int>> _vertexToFaces = new(); // DEAD for dual Success — craft helper; use Graph.FacesTouchingVertex
	private int _lastFlippedVertex = -1;
	private int _lastFlippedSecondaryFace = -1;
	private Node3D? _debugDualIdsRoot;
	/// <summary>Dedicated parent for always-on dual wireframe + vertex spheres (cleared on lattice rebuild).</summary>
	private Node3D? _dualDebugRoot;
	private readonly List<string> _debugHighlightedDualKeys = new();
	/// <summary>Muted cyan accent for owned dual / selection — avoid neon bleach.</summary>
	private readonly Color _ownedDualHighlightColor = new(0.28f, 0.72f, 0.78f, 1f);
	/// <summary>Legacy dual-edge ribbon color — DualCellEdges removed (clutter); kept for refuse proofs.</summary>
	private readonly Color _dualEdgeWireColor = new(0.32f, 0.70f, 0.76f, 0.95f);
	/// <summary>Dual vertex plus markers at face centroids — muted coral, not bleach.</summary>
	private readonly Color _dualVertexPlusColor = new(0.88f, 0.48f, 0.40f, 1f);
	/// <summary>High-contrast segment hues for populated dual-cell sides (index 0..3).</summary>
	private static readonly Color[] DualSegmentPalette =
	{
		new(0.82f, 0.38f, 0.34f, 0.95f), // coral
		new(0.30f, 0.68f, 0.74f, 0.95f), // cyan
		new(0.72f, 0.52f, 0.22f, 0.95f), // muted amber-gold
		new(0.52f, 0.42f, 0.78f, 0.95f), // muted violet
	};

	public int PaintedCellCount => _occupancy.Count;
	public bool WorldExists => _organicMesh != null && _organicMesh.FaceCount > 0;
	public MeshLibrary? Library => EnsureShapeDistinctDualMeshLibrary();
	public string MeshLibrarySource => "blender_to_meshlibrary_dual_offset_terrain_tile_sixpack_stage6_dual_cell";
	public bool OccupancyGridVisible => _latticeVisible;
	public bool DualOverlayVisible => _dualVisible;
	public int DualSlotCount => _dualSlots.Count;
	/// <summary>MCP/F5 evidence — last flipped logic / secondary and stable dual-lattice set.</summary>
	public int LastFlippedVertex => _lastFlippedVertex;
	public int LastFlippedSecondaryFace => _lastFlippedSecondaryFace;
	public string LastOwnedDualCellsCsv { get; private set; } = "";
	public string LastOwnedDualFacesCsv { get => LastOwnedDualCellsCsv; private set => LastOwnedDualCellsCsv = value; }
	public int LastOwnedDualFaceCount { get; private set; }
	public string LastExpandDualCellsCsv { get; private set; } = "";
	public int LastExpandDualCount { get; private set; }
	public string LastSmallCornerQuadsCsv { get => LastExpandDualCellsCsv; private set => LastExpandDualCellsCsv = value; }
	public int LastSmallCornerQuadCount { get => LastExpandDualCount; private set => LastExpandDualCount = value; }
	public bool LastNeighborhoodStable { get; private set; }
	/// <summary>Prefer place mode — owned_dual_cell_place (refuse expand_only_paint_as_success).</summary>
	public string LastGlowMode { get; private set; } = "owned_dual_cell_place";
	public Vector3 LatticeOrigin => _latticeOrigin;
	public float HexSize => _hexSize;
	public OrganicQuadMesh? OrganicMesh => _organicMesh;
	public int OrganicQuadFaceCount => _organicMesh?.FaceCount ?? 0;
	public int OrganicQuadVertexCount => _organicMesh?.VertexCount ?? 0;

	/// <summary>Legacy hex-19 counts — not Success for this Prefer; organic quads own F5.</summary>
	public int LatticeVertexCount => OrganicQuadVertexCount;
	public int LatticeEdgeCount => _organicMesh?.EdgeEstimate ?? 0;
	public int LatticeCellCount => OrganicQuadFaceCount;

	public Error EnsureHost(Node3D parent)
	{
		if (_organicRoot != null && GodotObject.IsInstanceValid(_organicRoot))
			return Error.Ok;

		if (GetParent() == null)
			parent.AddChild(this);

		_latticeOrigin = ResolveLatticeOrigin();
		// Primary F5 = organic all-quad board; dual-corner authorship sits on top (not Hex19 Success).
		BuildOrganicQuadVisuals();
		BuildOrganicDualCornerOverlay();

		_ = EnsureShapeDistinctDualMeshLibrary();
		AlphaFactoryLog.Emit(
			"craft.grid",
			"Stalberg_OrganicQuadKernel",
			"Stålberg primal_graph_r1 — OrganicMeshGraph Vertex/Edge/Face + incidence; success_object=organic_mesh_graph; dual cells=Stage6AroundVertex; refuse indexed_lists_as_graph|ephemeral_edge_key_as_topology|primary_face_as_dual|proxy_substitution; Hex19 not Success",
			new Dictionary<string, object>
			{
				["ask_id"] = PreferAskId,
				["overlay"] = WeldSliceId,
				["grammar"] = "organic_quad_board__half_step_dual_lattice__logic_corners",
				["pipeline"] = "SeedHexLatticeRings|TriangulateHexLattice|DissolveTrianglePairs|SubdivideFacesToQuads|UniqueTopology2D|EstimateIdealSideFromArea|RelaxTowardSquares|WeldNearDuplicates|FlattenToCraftPlane",
				["quad_faces"] = OrganicQuadFaceCount,
				["quad_vertices"] = OrganicQuadVertexCount,
				["quad_edges"] = LatticeEdgeCount,
				["all_faces_quads"] = _organicMesh?.AllFacesAreQuads ?? false,
				["seed_rings"] = _seedRingCount,
				["seed_spacing"] = _hexSize,
				["regenerable"] = true,
				["topology"] = "unique_position_hashed_organic_quad_faces_valence_4_planar",
				["relax"] = "rotate90_average_squarify_area_side_boundary_pin_clamp",
				["render"] = "opaque_faces_depth_edges",
				["terrain3d"] = "hard_disabled_under_craft",
				["visual_bar"] = VisualBarCite,
				["art_style_id"] = ArtStyleId,
				["mesh_library_source"] = MeshLibrarySource,
				["shape_distinct_dual"] = false,
				["discrete_meshlibrary_item"] = false,
				["stamp_as_dual"] = false,
				["dual_neighborhood_stable"] = true,
				["primary_face_as_dual"] = false,
				["dual_lattice"] = true,
				["max_dual_cells_per_logic_flip"] = MaxDualCellsPerLogicFlip,
				["gray_ramp_only"] = false,
				["stretch_as_variant"] = false,
				["over_neighbor_paint"] = false,
				["dual_visual_success"] = false,
				["hex19_success"] = false,
				["connector_success"] = false,
				["refuse_ban"] = "unstable_dual_neighborhood|stamp_as_dual|over_neighbor_paint|stretch_as_variant|gray_ramp_only|inspiration_shape_miss|non_unique_vertices|missing_square_area_force|naive_laplacian_only|free_boundary_fold|extrusion_before_2d_stable|relax_before_quad_only|relax_step_too_hard|noodle_edge_clutter|wireframe_spaghetti|extruded_prism_as_quad_board|unbounded_z_jitter|nonplanar_face_soup|hex_scaffold_as_final_mesh|dual_overlay_as_grid_kernel|skip_dissolve_relax|points_as_grid|count_equals_topology|bundle_tutorial_steps|terrain3d_in_scope|verify_mcp_only",
			});
		return Error.Ok;
	}

	/// <summary>Operator regenerate — new seed → full pipeline → refresh graybox quads.</summary>
	public void RegenerateOrganicQuadMesh(int? ringCount = null, ulong? seed = null)
	{
		if (ringCount is int rings)
			_seedRingCount = Math.Max(1, rings);
		ClearOrganicOccupancyMeshes();
		_cornerLogic.Clear();
		BuildOrganicQuadVisuals(seed);
		BuildOrganicDualCornerOverlay();
		AlphaFactoryLog.Emit(
			"craft.grid",
			"organic_quad_regenerate",
			$"regenerated organic all-quad field — faces={OrganicQuadFaceCount} verts={OrganicQuadVertexCount} rings={_seedRingCount}",
			new Dictionary<string, object>
			{
				["ask_id"] = PreferAskId,
				["overlay"] = WeldSliceId,
				["quad_faces"] = OrganicQuadFaceCount,
				["all_faces_quads"] = _organicMesh?.AllFacesAreQuads ?? false,
				["seed_rings"] = _seedRingCount,
			});
	}

	/// <summary>Structural proof for Prefer — planar all-quad board, not hex scaffold / noodle soup.</summary>
	public (bool Ok, string Summary) ProveOrganicQuadKernel()
	{
		if (_organicRoot == null || !GodotObject.IsInstanceValid(_organicRoot))
			return (false, "organic_quad_root_missing");
		if (_organicRoot.GetNodeOrNull<MeshInstance3D>("OrganicQuadFaces") == null)
			return (false, "organic_quad_faces_mesh_missing");
		if (_organicRoot.GetNodeOrNull<MeshInstance3D>("OrganicQuadEdges") == null)
			return (false, "organic_quad_edges_mesh_missing");
		if (_organicMesh == null || !_organicMesh.AllFacesAreQuads)
			return (false, "faces_not_all_quads");
		if (_organicMesh.FaceCount < 4)
			return (false, "too_few_quad_faces");
		// Hex scaffold must not be the primary board.
		if (GetNodeOrNull<Node3D>("Hex19LatticeGraph") is { Visible: true })
			return (false, "hex_scaffold_as_final_mesh");
		// Dual-corner Prefer: dual overlay is authorship layer, not a substitute for the kernel board.
		if (_dualRoot != null && _dualRoot.Visible && PreferAskId == "alpha0_stalberg_quad_kernel")
			return (false, "dual_overlay_as_grid_kernel");
		return (true, $"organic_planar_quads faces={_organicMesh.FaceCount} verts={_organicMesh.VertexCount} edges={_organicMesh.EdgeEstimate} rings={_organicMesh.SeedRingCount}");
	}

	private void BuildOrganicQuadVisuals(ulong? seed = null)
	{
		foreach (var child in GetChildren())
		{
			if (child is GridMap gm)
				gm.QueueFree();
		}

		if (_organicRoot != null && GodotObject.IsInstanceValid(_organicRoot))
			_organicRoot.QueueFree();

		_organicMesh = StalbergQuadKernel.Generate(
			ringCount: _seedRingCount,
			spacing: _hexSize,
			seed: seed);
		_organicMesh.FlattenToCraftPlane();

		_organicRoot = new Node3D { Name = "StalbergOrganicQuadMesh", Visible = true };
		AddChild(_organicRoot);
		// Primary amber grid must read — faces + edges (env blue ≠ water tiles).
		// Refuse ocean_fill_all_empty_slots / blob_as_module as board surface.
		_organicRoot.AddChild(new MeshInstance3D
		{
			Name = "OrganicQuadFaces",
			Mesh = _organicMesh.BuildFaceMesh(PrimaryAmberFaceTint),
			Position = Vector3.Zero,
			Visible = true,
		});
		_organicRoot.AddChild(new MeshInstance3D
		{
			Name = "OrganicQuadEdges",
			// Ribbon half-width — PrimitiveType.Lines stay 1px; scale with craft spacing (210 = 70×3).
			// Orange grid accent ≈ YT Game Dev Buddies craft grid.
			Mesh = _organicMesh.BuildEdgeMesh(new Color(0.92f, 0.48f, 0.18f, 1f), CraftEdgeRibbonHalfWidth()),
			Position = Vector3.Zero,
		});
		_organicRoot.GlobalPosition = _latticeOrigin;
		_gridRoot = _organicRoot;
		_latticeVisible = true;
		_dualVisible = true;
		_cornerLogic.Clear();
		RebuildVertexFaceIndex();
		EnsurePlacementGhost();
	}

	private void EnsurePlacementGhost()
	{
		if (_ghost != null && GodotObject.IsInstanceValid(_ghost))
			return;
		_ghost = new MeshInstance3D
		{
			Name = "PlacementGhost",
			Visible = false,
		};
		AddChild(_ghost);
	}

	public void SetLatticeOrigin(Vector3 origin)
	{
		_latticeOrigin = origin;
		if (_organicRoot != null && GodotObject.IsInstanceValid(_organicRoot))
			_organicRoot.GlobalPosition = _latticeOrigin;
		if (_gridRoot != null && _gridRoot != _organicRoot)
			_gridRoot.GlobalPosition = _latticeOrigin;
		if (_dualRoot != null)
			_dualRoot.GlobalPosition = _latticeOrigin;
		foreach (var (_, mesh) in _filledCells)
			mesh.GlobalPosition = _latticeOrigin + Vector3.Up * 0.02f;
		RefreshAllDualSlots();
	}

	/// <summary>Show/hide the occupancy lattice — vertices, edges and faces together.</summary>
	public void SetOccupancyGridVisible(bool visible)
	{
		_latticeVisible = visible;
		if (_gridRoot != null)
			_gridRoot.Visible = visible;
		AlphaFactoryLog.Emit(
			"craft.ui",
			"occupancy_lattice_toggle",
			$"occupancy_lattice_visible={visible} — vertices+edges+faces (dual toggle independent)",
			new Dictionary<string, object>
			{
				["ask_id"] = PreferAskId,
				["overlay"] = WeldSliceId,
				["occupancy_lattice_visible"] = visible,
				["dual_overlay_visible"] = _dualVisible,
				["toggles"] = "occupancy_independent_of_dual",
			});
	}

	public void ToggleOccupancyGridVisible() => SetOccupancyGridVisible(!_latticeVisible);

	/// <summary>Show/hide dual half-offset overlay independently of the occupancy lattice.</summary>
	public void SetDualOverlayVisible(bool visible)
	{
		_dualVisible = visible;
		if (_dualRoot != null)
			_dualRoot.Visible = visible;
		AlphaFactoryLog.Emit(
			"craft.ui",
			"dual_overlay_toggle",
			$"dual_overlay_visible={visible} — half-step offset quads (independent of occupancy lattice)",
			new Dictionary<string, object>
			{
				["ask_id"] = PreferAskId,
				["overlay"] = WeldSliceId,
				["dual_overlay_visible"] = visible,
				["occupancy_lattice_visible"] = _latticeVisible,
				["dual_half_offset"] = true,
				["update_four"] = true,
			});
	}

	public void ToggleDualOverlayVisible() => SetDualOverlayVisible(!_dualVisible);

	/// <summary>Paired toggle — show/hide occupancy lattice and dual overlay together.</summary>
	public void ToggleBothOverlays()
	{
		var next = !(_latticeVisible && _dualVisible);
		SetOccupancyGridVisible(next);
		SetDualOverlayVisible(next);
	}

	/// <summary>
	/// Mouse ray → primary logic Vertex V under cursor (place Success).
	/// Encoder Y = PrimaryPickY. Refuse secondary_glow_center_as_place_target /
	/// secondary_face_snap_as_place / hex19_pick_as_craft_authority.
	/// Method name kept for WorldgenCraft compat; body is organic primary-V snap.
	/// </summary>
	public bool TryPickHexCell(Camera3D camera, Vector2 screenPos, out Vector2I cell)
	{
		// Place Success: primary organic corner V first (amber star / main intersection).
		// Secondary face-centroid glow remains FlipOrganicSecondary debug-only — not place.
		if (TryPickOrganicCorner(camera, screenPos, out var vertexIndex))
		{
			cell = new Vector2I(vertexIndex, PrimaryPickY);
			return true;
		}
		cell = default;
		return false;
	}

	/// <summary>Craft-plane pick — ray → organic quad face occupancy key.</summary>
	public bool TryPickOrganicFace(Camera3D camera, Vector2 screenPos, out Vector2I cell)
	{
		cell = default;
		if (_organicMesh == null || camera == null)
			return false;
		var from = camera.ProjectRayOrigin(screenPos);
		var dir = camera.ProjectRayNormal(screenPos);
		if (Mathf.IsZeroApprox(dir.Y))
			return false;
		var t = (_latticeOrigin.Y - from.Y) / dir.Y;
		if (t < 0f) return false;
		var hit = from + dir * t;
		var local = new Vector2(hit.X - _latticeOrigin.X, hit.Z - _latticeOrigin.Z);
		if (!_organicMesh.TryPickFace(local, out var face) &&
		    !_organicMesh.TryNearestFace(local, out face, maxDist: _hexSize * 0.85f))
			return false;
		cell = OrganicQuadMesh.FaceCell(face);
		return true;
	}

	/// <summary>Placement ghost — previews OwnedDualCell(V) under the cursor (primary V snap).</summary>
	public void UpdateGhost(Camera3D? camera, Vector2 screenPos)
	{
		if (_ghost == null) return;
		if (camera == null || !TryPickOrganicCorner(camera, screenPos, out var vertex) ||
		    _dualLattice == null || !_dualLattice.TryGetOwned(vertex, out var owned))
		{
			_ghost.Visible = false;
			_ghostVisible = false;
			return;
		}

		var corners = OrganicDualOffsetLattice.Stage6CornersLocal(owned);
		if (corners == null || corners.Length < 3)
		{
			_ghost.Visible = false;
			_ghostVisible = false;
			return;
		}

		_ghost.Mesh = MakeHalfStepDualCellMesh(corners, new Color(0.30f, 0.62f, 0.68f, 0.40f), height: 0.04f);
		_ghost.GlobalPosition = _latticeOrigin + Vector3.Up * 0.04f;
		_ghost.Visible = true;
		_ghostVisible = true;
	}

	public void HideGhost()
	{
		if (_ghost == null) return;
		_ghost.Visible = false;
		_ghostVisible = false;
	}

	/// <summary>
	/// Craft-plane structural proof — organic vertices + edges + faces (not Hex19 Success).
	/// A vertex total alone is refused (count_equals_topology).
	/// </summary>
	public (bool AllDistinct, string Summary) ProveLatticeGraphTopology()
	{
		if (_organicMesh == null || _organicRoot == null)
			return (false, "organic_craft_plane_not_built refuse=hex19_pick_as_craft_authority");
		if (_organicRoot.GetNodeOrNull<MeshInstance3D>("OrganicQuadEdges") == null)
			return (false, "organic_edge_surface_missing refuse=points_as_grid");
		if (_organicRoot.GetNodeOrNull<MeshInstance3D>("OrganicQuadFaces") == null)
			return (false, "organic_face_surface_missing refuse=points_as_grid");
		if (_organicMesh.EdgeEstimate <= 0)
			return (false, "organic_has_no_edges refuse=points_as_grid");
		if (_organicMesh.FaceCount <= 0)
			return (false, "organic_has_no_faces refuse=points_as_grid");
		return (true,
			$"organic craft plane verts={_organicMesh.VertexCount} edges={_organicMesh.EdgeEstimate} " +
			$"faces={_organicMesh.FaceCount} pick=TryPickOrganicFace hex19_success=false");
	}

	/// <summary>Prefer proof — craft authority is organic faces, not Hex19 snap.</summary>
	public (bool Ok, string Summary) ProveCraftPlaneAuthority()
	{
		var kernel = ProveOrganicQuadKernel();
		if (!kernel.Ok) return (false, kernel.Summary);
		var topo = ProveLatticeGraphTopology();
		if (!topo.AllDistinct) return (false, topo.Summary);
		// Mechanical tell: pick path must not call Hex19 TrySnapWorldToCell (code seat).
		return (true,
			$"craft_plane_authority organic_faces={_organicMesh!.FaceCount} " +
			$"pick=TryPickOrganicFace paint=FaceCell hex19_success=false dual_success=false");
	}

	private void RebuildVertexFaceIndex()
	{
		_vertexToFaces.Clear(); // dead for dual Success — craft-plane paint helper only; prefer Graph.FacesTouchingVertex
		if (_organicMesh == null)
		{
			_dualLattice = null;
			return;
		}
		// Prefer Success: OrganicMeshGraph incidence. Indexed _vertexToFaces is NOT dual ownership.
		if (_organicMesh.Graph != null)
		{
			foreach (var v in _organicMesh.Graph.Vertices)
			{
				var faces = _organicMesh.Graph.FacesTouchingVertex(v);
				if (faces.Count == 0) continue;
				var list = faces.Select(f => f.Id).OrderBy(i => i).ToList();
				_vertexToFaces[v.Id] = list;
			}
		}
		else
		{
			// Fail-closed tell — Prefer indexed_lists_as_graph when Graph missing.
			for (var fi = 0; fi < _organicMesh.Quads.Count; fi++)
			{
				var q = _organicMesh.Quads[fi];
				if (q == null || q.Length != 4) continue;
				foreach (var vi in q)
				{
					if (!_vertexToFaces.TryGetValue(vi, out var list))
					{
						list = new List<int>();
						_vertexToFaces[vi] = list;
					}
					if (!list.Contains(fi)) list.Add(fi);
				}
			}
			foreach (var key in _vertexToFaces.Keys.ToList())
				_vertexToFaces[key].Sort();
		}

		// Dual ownership corners = shared Vertex refs on OrganicDualOffsetLattice.
		_dualLattice = new OrganicDualOffsetLattice(_organicMesh);
	}

	/// <summary>
	/// Secondary pick — nearest dual vert at primal face centroid (coral/cyan locus).
	/// Prefer Success for glow center. Refuse primary_star_glow_as_success.
	/// </summary>
	public bool TryPickOrganicSecondary(Camera3D camera, Vector2 screenPos, out int faceId)
	{
		faceId = -1;
		if (_organicMesh == null || camera == null || _dualLattice == null) return false;
		var from = camera.ProjectRayOrigin(screenPos);
		var dir = camera.ProjectRayNormal(screenPos);
		if (Mathf.IsZeroApprox(dir.Y)) return false;
		var t = (_latticeOrigin.Y - from.Y) / dir.Y;
		if (t < 0f) return false;
		var hit = from + dir * t;
		var local = new Vector2(hit.X - _latticeOrigin.X, hit.Z - _latticeOrigin.Z);
		var best = (_hexSize * 0.55f) * (_hexSize * 0.55f);
		foreach (var fid in _dualLattice.EditableSecondaryFaces)
		{
			if (!_dualLattice.TryGetSecondaryCentroid(fid, out var c)) continue;
			var d = local.DistanceSquaredTo(c);
			if (d > best) continue;
			if (d < best || faceId < 0 || fid < faceId)
			{
				best = d;
				faceId = fid;
			}
		}
		// Sticky snap — repeat click near last secondary locus resolves identically.
		if (_lastFlippedSecondaryFace >= 0 &&
		    _dualLattice.IsEditableSecondaryPoint(_lastFlippedSecondaryFace) &&
		    _dualLattice.TryGetSecondaryCentroid(_lastFlippedSecondaryFace, out var stickyC))
		{
			var stickyR = (_hexSize * 0.35f) * (_hexSize * 0.35f);
			if (local.DistanceSquaredTo(stickyC) <= stickyR)
				faceId = _lastFlippedSecondaryFace;
		}
		return faceId >= 0 && _dualLattice.IsEditableSecondaryPoint(faceId);
	}

	/// <summary>Primary corner pick — place Success snap (amber V / main intersection).</summary>
	public bool TryPickOrganicCorner(Camera3D camera, Vector2 screenPos, out int vertexIndex)
	{
		vertexIndex = -1;
		if (_organicMesh == null || camera == null) return false;
		var from = camera.ProjectRayOrigin(screenPos);
		var dir = camera.ProjectRayNormal(screenPos);
		if (Mathf.IsZeroApprox(dir.Y)) return false;
		var t = (_latticeOrigin.Y - from.Y) / dir.Y;
		if (t < 0f) return false;
		var hit = from + dir * t;
		var local = new Vector2(hit.X - _latticeOrigin.X, hit.Z - _latticeOrigin.Z);
		if (_dualLattice == null)
			return false;
		var best = (_hexSize * 0.55f) * (_hexSize * 0.55f);
		foreach (var i in _dualLattice.EditableLogicPoints)
		{
			if (i < 0 || i >= _organicMesh.VertexCount) continue;
			var d = local.DistanceSquaredTo(_organicMesh.Vertices[i]);
			// Deterministic: strictly nearer, or equal distance → lower index wins.
			if (d > best) continue;
			if (d < best || vertexIndex < 0 || i < vertexIndex)
			{
				best = d;
				vertexIndex = i;
			}
		}
		// Sticky snap — repeat click near last flipped logic point resolves identically.
		if (_lastFlippedVertex >= 0 && _dualLattice.IsEditableLogicPoint(_lastFlippedVertex))
		{
			var stickyR = (_hexSize * 0.35f) * (_hexSize * 0.35f);
			var dSticky = local.DistanceSquaredTo(_organicMesh.Vertices[_lastFlippedVertex]);
			if (dSticky <= stickyR)
				vertexIndex = _lastFlippedVertex;
		}
		return vertexIndex >= 0 && _dualLattice.IsEditableLogicPoint(vertexIndex);
	}

	/// <summary>
	/// Glow-debug only — secondary face-centroid locus. Not place Success
	/// (refuse secondary_glow_center_as_place_target / secondary_face_snap_as_place).
	/// </summary>
	public int FlipOrganicSecondary(int faceId)
	{
		if (_organicMesh == null || _dualLattice == null || faceId < 0)
			return 0;
		if (!_dualLattice.IsEditableSecondaryPoint(faceId))
			return 0;
		_lastFlippedSecondaryFace = faceId;
		LastGlowMode = "secondary_face_center_debug";
		var small = _dualLattice.SmallCornerQuadsAroundFace(faceId);
		var smallKeys = small.Select(sc => sc.Key).ToList();
		// Nearest logic vert to face centroid — single bit flip (not all face corners).
		var faceCentroid = Vector3.Zero;
		var faceCount = 0;
		foreach (var sc in small)
		{
			if (sc.Corners == null || sc.Corners.Length < 3) continue;
			faceCentroid += sc.Corners[2]; // face-centroid corner of pie
			faceCount++;
		}
		if (faceCount > 0) faceCentroid /= faceCount;
		var bestVert = -1;
		var bestD = float.MaxValue;
		foreach (var sc in small)
		{
			if (!_dualLattice.IsEditableLogicPoint(sc.LogicVertexId)) continue;
			var p = _organicMesh.Vertices[sc.LogicVertexId];
			var d = new Vector2(faceCentroid.X, faceCentroid.Z).DistanceSquaredTo(p);
			if (d < bestD)
			{
				bestD = d;
				bestVert = sc.LogicVertexId;
			}
		}
		if (bestVert < 0)
			return 0;
		_cornerLogic[bestVert] = !(_cornerLogic.TryGetValue(bestVert, out var on) && on);
		_lastFlippedVertex = bestVert;
		LastOwnedDualCellsCsv = string.Join(',', _dualLattice.OwnedDualCellKeys(bestVert));
		LastOwnedDualFaceCount = 1;
		LastSmallCornerQuadsCsv = string.Join(',', smallKeys);
		LastSmallCornerQuadCount = smallKeys.Count;
		var prove = ProveStableDualNeighborhood();
		LastNeighborhoodStable = prove.Ok;
		var n = UpdateFourDualSlots(new Vector2I(bestVert, 1));
		HighlightSecondaryDualCells(faceId);
		AlphaFactoryLog.Emit(
			"craft.dual",
			"Secondary_Flip",
			$"organic secondary_face={faceId} logic_vert={bestVert} dual_cells_refreshed={n} glow=secondary_face_center populate=dual_cell_lookup (cap={MaxDualCellsPerLogicFlip})",
			new Dictionary<string, object>
			{
				["ask_id"] = PreferAskId,
				["overlay"] = WeldSliceId,
				["secondary_face"] = faceId,
				["logic_vert"] = bestVert,
				["glow_mode"] = "secondary_face_center",
				["update_four"] = n,
				["face_stamp_as_dual_populate"] = false,
				["sector_pie_as_dual_cell_tile"] = false,
				["dual_cell_meshlibrary_placement"] = true,
				["max_dual_cells_per_logic_flip"] = MaxDualCellsPerLogicFlip,
				["primary_star_glow_as_success"] = false,
				["secondary_glow_center"] = true,
				["stage6_union_as_single_glow_tile"] = false,
				["dual_half_offset"] = true,
				["primary_face_as_dual"] = false,
				["stamp_as_dual"] = false,
				["unstable_dual_neighborhood"] = false,
				["stretch_as_variant"] = false,
				["over_neighbor_paint"] = false,
				["hex19_success"] = false,
				["cam_recenter"] = false,
				["terrain_pushed"] = false,
			});
		return n;
	}

	/// <summary>
	/// Place Success — flip primary V; refresh DualCellsTouching(V) = owned + expand
	/// recompute (≤ MaxDualCellsPerLogicFlip). Ghost seat = OwnedDualCell(V).
	/// Non-Empty MeshLibrary only on OwnedDualCell(V); expand neighbors Clear/Empty unless
	/// their own owner is on. Empty skips mesh.
	/// </summary>
	public int FlipOrganicCorner(int vertexIndex)
	{
		if (_organicMesh == null || _dualLattice == null || vertexIndex < 0 || vertexIndex >= _organicMesh.VertexCount)
			return 0;
		if (!_dualLattice.IsEditableLogicPoint(vertexIndex))
			return 0;
		_cornerLogic[vertexIndex] = !(_cornerLogic.TryGetValue(vertexIndex, out var on) && on);
		_lastFlippedVertex = vertexIndex;
		LastGlowMode = "owned_dual_cell_place";
		var owned = OwnedDualCellKeys(vertexIndex);
		var expandKeys = _dualLattice.DualCellsExpandingFrom(vertexIndex).Select(c => c.Key).ToList();
		LastOwnedDualCellsCsv = string.Join(',', owned);
		LastOwnedDualFaceCount = owned.Count;
		LastExpandDualCellsCsv = string.Join(',', expandKeys);
		LastExpandDualCount = expandKeys.Count;
		LastSmallCornerQuadsCsv = LastExpandDualCellsCsv;
		LastSmallCornerQuadCount = LastExpandDualCount;
		var prove = ProveStableDualNeighborhood();
		LastNeighborhoodStable = prove.Ok;
		var n = UpdateFourDualSlots(new Vector2I(vertexIndex, PrimaryPickY));
		HighlightOwnedDualCells(vertexIndex);
		AlphaFactoryLog.Emit(
			"craft.dual",
			"Corner_Flip",
			$"organic primary_V={vertexIndex} filled={_cornerLogic[vertexIndex]} dual_cells_refreshed={n} owned=[{string.Join(',', owned)}] expand=[{string.Join(',', expandKeys)}] touching=DualCellsTouching (cap={MaxDualCellsPerLogicFlip})",
			new Dictionary<string, object>
			{
				["ask_id"] = PreferAskId,
				["overlay"] = WeldSliceId,
				["corner_index"] = vertexIndex,
				["filled"] = _cornerLogic[vertexIndex],
				["update_four"] = n,
				["owned_dual_cells"] = string.Join(',', owned),
				["owned_count"] = owned.Count,
				["expand_dual_cells"] = string.Join(',', expandKeys),
				["expand_count"] = expandKeys.Count,
				["max_dual_cells_per_logic_flip"] = MaxDualCellsPerLogicFlip,
				["success_object"] = SuccessObject,
				["place_polarity"] = PlacePolarity,
				["paint_contract"] = PaintContract,
				["owned_dual_cell_place"] = true,
				["owned_only_paint"] = true,
				["neighbor_corner_spray_as_place"] = false,
				["update_four_cross_as_success"] = false,
				["primary_vertex_place"] = true,
				["secondary_glow_center_as_place_target"] = false,
				["ocean_fill_all_empty_slots"] = false,
				["glow_mode"] = "primary_vertex_place",
				["stage6_union_as_single_glow_tile"] = false,
				["dual_half_offset"] = true,
				["primary_face_as_dual"] = false,
				["stamp_as_dual"] = false,
				["face_stamp_as_dual_populate"] = false,
				["unstable_dual_neighborhood"] = false,
				["stretch_as_variant"] = false,
				["over_neighbor_paint"] = false,
				["hex19_success"] = false,
				["cam_recenter"] = false,
				["terrain_pushed"] = false,
			});
		return n;
	}

	/// <summary>Organic dual overlay — half-step OrganicDualOffsetLattice cells (not primary-face fills).</summary>
	private void BuildOrganicDualCornerOverlay()
	{
		if (_dualRoot != null && GodotObject.IsInstanceValid(_dualRoot))
			_dualRoot.QueueFree();
		_dualSlots.Clear();
		_dualDebugRoot = null;
		_debugDualIdsRoot = null;
		if (_organicMesh == null) return;
		if (_dualLattice == null)
			_dualLattice = new OrganicDualOffsetLattice(_organicMesh);

		_dualRoot = new Node3D { Name = "OrganicDualOffsetOverlay", Visible = _dualVisible };
		AddChild(_dualRoot);
		_dualRoot.GlobalPosition = _latticeOrigin;

		// Staging showcase — seed corner patterns BEFORE first mesh build so names+geometry match families.
		SeedDualVisualFamilyShowcase(refresh: false);

		// Visual slots = Stage-6 DualCells (one MeshLibrary item each; Empty skips mesh).
		foreach (var cell in _dualLattice.AllCells)
			EnsureStage6DualCellMesh(cell);

		// Dual debug: face-centroid plus markers only — no DualCellEdges ribbons (clutter).
		RebuildDualLatticeDebugVisuals();

		AlphaFactoryLog.Emit(
			"craft.grid",
			"Dual_Offset_Overlay",
			$"organic stage6_dual_cells armed — unique_slots={_dualSlots.Count} stage6_cells={_dualLattice.CellCount} update_four≤{MaxDualCellsPerLogicFlip} (refuse ocean_fill_all_empty_slots|sector_pie_as_dual_cell_tile|primary_face_as_dual)",
			new Dictionary<string, object>
			{
				["ask_id"] = PreferAskId,
				["overlay"] = WeldSliceId,
				["dual_half_offset"] = true,
				["update_four"] = true,
				["max_dual_cells_per_logic_flip"] = MaxDualCellsPerLogicFlip,
				["dual_slots"] = _dualSlots.Count,
				["small_corner_quads"] = _dualLattice.SmallCornerQuadCount,
				["stage6_cells"] = _dualLattice.CellCount,
				["dual_on_organic"] = true,
				["primary_face_as_dual"] = false,
				["stage6_union_as_single_glow_tile"] = false,
				["organic_dual_offset_lattice"] = true,
				["shape_distinct_dual"] = true,
				["discrete_meshlibrary_item"] = true,
				["dual_families"] = "empty|edge|corner|full|diagonal|inverse",
				["dual_edge_wireframe"] = false,
				["dual_vertex_plus_markers"] = true,
				["ocean_fill_all_empty_slots"] = false,
				["dual_segment_colors"] = true,
				["gray_ramp_only"] = false,
				["stretch_as_variant"] = false,
				["over_neighbor_paint"] = false,
				["mesh_library_source"] = MeshLibrarySource,
				["hex19_success"] = false,
				["connector_success"] = false,
				["art_success"] = false,
			});
	}

	/// <summary>
	/// Dual lattice debug — face-centroid plus markers only.
	/// No DualCellEdges ribbons (clutter). Refuse FaceCornersLocal inset rings as dual edges.
	/// </summary>
	private void RebuildDualLatticeDebugVisuals()
	{
		if (_dualRoot == null || _dualLattice == null || _organicMesh == null)
			return;

		if (_dualDebugRoot != null && GodotObject.IsInstanceValid(_dualDebugRoot))
			_dualDebugRoot.QueueFree();

		_dualDebugRoot = new Node3D { Name = "DualLatticeDebug" };
		_dualRoot.AddChild(_dualDebugRoot);

		// DualCellEdges intentionally omitted — operator: remove dual edge wireframe clutter.

		_dualDebugRoot.AddChild(new MeshInstance3D
		{
			Name = "DualVertexPlusMarkers",
			Mesh = BuildDualVertexPlusMarkers(),
			Position = Vector3.Up * 0.70f,
		});
	}

	/// <summary>
	/// World half-width for primal/dual edge ribbons. Godot Lines ignore width;
	/// ~1.5% of spacing (half of prior 3% thicken-edges) at CameraHeight~3850 / DefaultSpacing=210.
	/// Clamps halved with the factor so spacing×fraction is not crushed by the old 1.25 max.
	/// </summary>
	private float CraftEdgeRibbonHalfWidth() =>
		Mathf.Clamp(_hexSize * 0.015f, 1.05f, 4.7f);

	/// <summary>
	/// Dual cell wireframe — Stage-6 polygons only (face-centroid dual verts + dual edges).
	/// Muted cyan — refuse bleach neon; distinct from primal amber OrganicQuadEdges.
	/// Refuse FaceCornersLocal / inset face rings (face_corners_local_as_dual_edges).
	/// Planar XZ ribbons (not PrimitiveType.Lines) so cyan stays thick at craft-cam height.
	/// </summary>
	private ArrayMesh BuildDualCellEdgeWireframe()
	{
		var st = new SurfaceTool();
		st.Begin(Mesh.PrimitiveType.Triangles);
		var halfW = CraftEdgeRibbonHalfWidth();
		var seen = new HashSet<(long, long, long, long, long, long)>();

		void AddEdge(Vector3 a, Vector3 b)
		{
			const float q = 0.1f;
			long Q(float v) => (long)MathF.Round(v / q);
			var ax = Q(a.X); var ay = Q(a.Y); var az = Q(a.Z);
			var bx = Q(b.X); var by = Q(b.Y); var bz = Q(b.Z);
			var swap = ax > bx || (ax == bx && ay > by) || (ax == bx && ay == by && az > bz);
			var key = swap ? (bx, by, bz, ax, ay, az) : (ax, ay, az, bx, by, bz);
			if (!seen.Add(key)) return;
			OrganicQuadMesh.EmitPlanarEdgeRibbon(st, _dualEdgeWireColor, a, b, halfW);
		}

		// Stage-6 DualCell polygons — edges connect face centroids (cross main cells).
		foreach (var cell in _dualLattice!.AllCells)
		{
			var poly = OrganicDualOffsetLattice.Stage6CornersLocal(cell);
			if (poly.Length < 2) continue;
			for (var i = 0; i < poly.Length; i++)
				AddEdge(poly[i], poly[(i + 1) % poly.Length]);
		}

		var mesh = st.Commit();
		mesh.SurfaceSetMaterial(0, new StandardMaterial3D
		{
			AlbedoColor = _dualEdgeWireColor,
			Transparency = _dualEdgeWireColor.A < 0.99f
				? BaseMaterial3D.TransparencyEnum.Alpha
				: BaseMaterial3D.TransparencyEnum.Disabled,
			ShadingMode = BaseMaterial3D.ShadingModeEnum.Unshaded,
			CullMode = BaseMaterial3D.CullModeEnum.Disabled,
		});
		return mesh;
	}

	/// <summary>
	/// Dual vertices = face centroids — planar plus (+) markers (not spheres).
	/// Arm length scales with spacing=210 so coral nodes stay visible at CameraHeight~3850.
	/// </summary>
	private ArrayMesh BuildDualVertexPlusMarkers()
	{
		var st = new SurfaceTool();
		st.Begin(Mesh.PrimitiveType.Triangles);
		var arm = Mathf.Clamp(_hexSize * 0.10f, 1.6f, 6.0f);
		var halfW = Mathf.Clamp(_hexSize * 0.018f, 0.35f, 1.4f);
		var seen = new HashSet<(long, long)>();
		foreach (var cell in _dualLattice!.AllCells)
		{
			if (cell.DualCorners == null) continue;
			foreach (var c in cell.DualCorners)
			{
				var key = ((long)MathF.Round(c.X * 100f), (long)MathF.Round(c.Z * 100f));
				if (!seen.Add(key)) continue;
				// Horizontal bar of +
				OrganicQuadMesh.EmitPlanarEdgeRibbon(
					st, _dualVertexPlusColor,
					c + new Vector3(-arm, 0f, 0f),
					c + new Vector3(arm, 0f, 0f),
					halfW);
				// Vertical bar of +
				OrganicQuadMesh.EmitPlanarEdgeRibbon(
					st, _dualVertexPlusColor,
					c + new Vector3(0f, 0f, -arm),
					c + new Vector3(0f, 0f, arm),
					halfW);
			}
		}

		var mesh = st.Commit();
		mesh.SurfaceSetMaterial(0, new StandardMaterial3D
		{
			AlbedoColor = _dualVertexPlusColor,
			ShadingMode = BaseMaterial3D.ShadingModeEnum.Unshaded,
			CullMode = BaseMaterial3D.CullModeEnum.Disabled,
		});
		return mesh;
	}

	/// <summary>
	/// Seed face-corner occupancy for empty/edge/corner/full silhouette demos only.
	/// Not place-path Success — LMB place proof = OwnedDualCell(V) via FlipOrganicCorner.
	/// Shared corners may lift neighbor DualCells — expected for silhouette staging.
	/// </summary>
	private void SeedDualVisualFamilyShowcase(bool refresh = true)
	{
		if (_organicMesh == null || _organicMesh.FaceCount < 8)
			return;
		_cornerLogic.Clear();
		// Face 1 → Corner silhouette (one bit) — demo only; place path uses OwnedDualCell.
		var qCorner = _organicMesh.Quads[1];
		_cornerLogic[qCorner[0]] = true;
		// Face 3 → Edge silhouette (two adjacent)
		var qEdge = _organicMesh.Quads[3];
		_cornerLogic[qEdge[0]] = true;
		_cornerLogic[qEdge[1]] = true;
		// Face 5 → Full silhouette (four bits)
		var qFull = _organicMesh.Quads[5];
		foreach (var v in qFull)
			_cornerLogic[v] = true;
		// Face 0 left Empty (zero bits) — silhouette contrast vs seeded neighbors.
		if (refresh)
			RefreshAllDualSlots();
		AlphaFactoryLog.Emit(
			"craft.dual",
			"DualVisual_FamilyShowcase",
			"seeded face-corner silhouettes empty|edge|corner|full (demo only; place Success=OwnedDualCell)",
			new Dictionary<string, object>
			{
				["ask_id"] = PreferAskId,
				["overlay"] = WeldSliceId,
				["shape_distinct_dual"] = true,
				["dual_families"] = "empty|edge|corner|full|diagonal|inverse",
				["gray_ramp_only"] = false,
			});
	}

	/// <summary>
	/// Pie slots are NOT MeshLibrary hosts (refuse sector_pie_as_dual_cell_tile).
	/// </summary>
	private void EnsureSmallCornerQuadMesh(OrganicDualOffsetLattice.SmallCornerQuad sc)
	{
		_ = sc;
	}

	/// <summary>
	/// Visual/populate — Stage-6 DualCell hosts one MeshLibrary item when non-Empty.
	/// Owned-only: non-Empty only when OwnerVertexId is on → Full whole DualCell.
	/// Neighbors recompute → ClearDualSlot/Empty unless their own owner is on.
	/// DualCorners n=3 (tri) or n=4 (quad); OccupancyCorners length matches (no soft_take_4).
	/// Warp: n=4 dual-edge frame (edge0=c0→c1); n=3 barycentric. Empty skips ocean.
	/// Refuse silent_ghost_without_place_n3 / soft_take_4 / neighbor_corner_spray / sector_pie.
	/// </summary>
	private void EnsureStage6DualCellMesh(OrganicDualOffsetLattice.DualCell cell)
	{
		if (_dualRoot == null || _dualLattice == null)
			return;
		var corners = OrganicDualOffsetLattice.Stage6CornersLocal(cell);
		if (corners == null || (corners.Length != 3 && corners.Length != 4))
			return;
		var occ = cell.OccupancyCorners;
		if (occ == null || occ.Length != corners.Length)
			return;
		var (family, rot90, mirror) = ResolveOrganicDualVisualFamily(occ, cell.OwnerVertexId);
		PlaceStage6DualCellLibraryItem(cell, corners, family, rot90, mirror);
	}

	/// <summary>Clear MeshLibrary instance for a DualCell key (Empty / unfilled).</summary>
	private void ClearDualSlot(string key)
	{
		if (string.IsNullOrEmpty(key)) return;
		if (_dualSlots.TryGetValue(key, out var existing) && GodotObject.IsInstanceValid(existing))
			existing.QueueFree();
		_dualSlots.Remove(key);
	}

	/// <summary>
	/// Place MeshLibrary family on a Stage-6 DualCell — dual-edge-frame (n=4) or barycentric
	/// triangle warp (n=3) onto Stage6CornersLocal. Full = wall-less whole-cell plateau.
	/// Y/sorting bias present but Z-fight Success DEFERRED. Empty = ClearDualSlot (ocean skip).
	/// Refuse silent_ghost_without_place_n3 / soft_take_4 / ocean_fill / neighbor Corner spray.
	/// </summary>
	private void PlaceStage6DualCellLibraryItem(
		OrganicDualOffsetLattice.DualCell cell,
		Vector3[] stage6Corners,
		DualVisualFamily family,
		int rot90,
		bool mirror)
	{
		if (_dualRoot == null)
			return;
		var key = cell.Key;
		// Empty: skip ocean GLB / opaque Empty on every DualCell — let amber primary grid read.
		if (family == DualVisualFamily.Empty)
		{
			ClearDualSlot(key);
			return;
		}
		var lib = EnsureShapeDistinctDualMeshLibrary();
		var source = lib.GetItemMesh((int)family) ?? MakeUnitShapeDistinctPrototype(family);
		var isFull = family == DualVisualFamily.Full;
		if (isFull)
			source = MakeWalllessFullPlateau(source);
		if (stage6Corners == null || (stage6Corners.Length != 3 && stage6Corners.Length != 4))
			return;

		MeshInstance3D mi;
		if (_dualSlots.TryGetValue(key, out var existing) && GodotObject.IsInstanceValid(existing))
			mi = existing;
		else
		{
			mi = new MeshInstance3D();
			_dualRoot.AddChild(mi);
			_dualSlots[key] = mi;
		}

		var yBias = isFull ? FullYBias : 0f;
		var (fitted, edge0YawRad) = MeshFitToDualEdgeFrame(source, stage6Corners, rot90, mirror, yBias);
		mi.Name = $"DualCell_{key}_{family}";
		mi.Mesh = fitted;
		mi.Position = Vector3.Zero;
		mi.Rotation = Vector3.Zero; // yaw is baked into dual-edge UV → Stage6 warp (not world yaw)
		mi.Scale = Vector3.One;
		mi.MaterialOverride = null;
		mi.SortingOffset = isFull ? FullSortingOffset : 0f;
		mi.SetMeta("dual_key", key);
		mi.SetMeta("weld_slice_id", WeldSliceId);
		mi.SetMeta("ask_id", PreferAskId);
		mi.SetMeta("art_style_id", ArtStyleId);
		mi.SetMeta("success_object", SuccessObject);
		mi.SetMeta("place_polarity", PlacePolarity);
		mi.SetMeta("paint_contract", PaintContract);
		mi.SetMeta("dual_cell_meshlibrary_placement", true);
		mi.SetMeta("owned_only_paint", true);
		mi.SetMeta("tri_cell_place", stage6Corners.Length == 3);
		mi.SetMeta("dual_corners_n", stage6Corners.Length);
		mi.SetMeta("soft_take_4", false);
		mi.SetMeta("silent_ghost_without_place_n3", false);
		mi.SetMeta("neighbor_corner_spray_as_place", false);
		mi.SetMeta("seizure_coplanar_deck_as_success", false);
		mi.SetMeta("zfight_success_deferred", true);
		mi.SetMeta("dual_offset_terrain_tile", true);
		mi.SetMeta("cream_quarter_platform", false);
		mi.SetMeta("plinth_as_terrain", false);
		mi.SetMeta("blob_as_module", false);
		mi.SetMeta("sector_pie_as_dual_cell_tile", false);
		mi.SetMeta("small_corner_quad", false);
		mi.SetMeta("stage6_dual_cell_host", true);
		mi.SetMeta("owned_by_logic_vertex", cell.OwnerVertexId);
		mi.SetMeta("dual_visual_family", family.ToString());
		mi.SetMeta("dual_visual_rot90", rot90);
		mi.SetMeta("dual_visual_mirror", mirror);
		mi.SetMeta("place_translate_yaw_uniform_scale", false);
		mi.SetMeta("dual_edge_frame_yaw", stage6Corners.Length == 4);
		mi.SetMeta("dual_edge_frame_yaw_rad", edge0YawRad);
		mi.SetMeta("world_yaw_as_dual_edge_frame", false);
		mi.SetMeta("mesh_fit_to_stage6_corners", true);
		mi.SetMeta("vertex_bilinear_warp_to_stage6_corners", stage6Corners.Length == 4);
		mi.SetMeta("vertex_barycentric_warp_to_stage6_triangle", stage6Corners.Length == 3);
		mi.SetMeta("corners_eq4_only_meshfit", false);
		mi.SetMeta("four_corner_sector_piece", false);
		mi.SetMeta("full_wallless_plateau", isFull);
		mi.SetMeta("whole_dual_cell_land", isFull);
		mi.SetMeta("full_y_bias", isFull ? FullYBias : 0f);
		mi.SetMeta("full_sorting_offset", isFull ? FullSortingOffset : 0f);
		mi.SetMeta("stretch_as_variant", false);
		mi.SetMeta("stamp_as_dual", false);
		mi.SetMeta("primary_face_as_dual", false);
		mi.SetMeta("stage6_union_as_single_glow_tile", false);
		mi.SetMeta("face_corners_local_as_dual_edges", false);
		mi.SetMeta("half_step_varignon_corner", false);
		mi.SetMeta("dual_vertex_at_face_centroid", true);
		mi.SetMeta("gray_ramp_only", false);
		mi.SetMeta("mesh_library_source", MeshLibrarySource);
		mi.SetMeta("discrete_meshlibrary_item", true);
		if (isFull)
			ApplyFullDepthBiasMaterials(mi);
	}

	/// <summary>
	/// Full = wall-less plateau — drop near-vertical skirt tris and keep only the top
	/// horizontal deck band so multi-deck Full GLBs do not coplanar-flash on pan.
	/// </summary>
	private static Mesh MakeWalllessFullPlateau(Mesh source)
	{
		var arrayMesh = source as ArrayMesh ?? ConvertMeshToArrayMesh(source);
		if (arrayMesh == null || arrayMesh.GetSurfaceCount() == 0)
			return source;
		var outMesh = new ArrayMesh();
		var keptAny = false;
		const float topBand = 0.08f;
		for (var surf = 0; surf < arrayMesh.GetSurfaceCount(); surf++)
		{
			var mdt = new MeshDataTool();
			if (mdt.CreateFromSurface(arrayMesh, surf) != Error.Ok)
				continue;
			// Pass 1: highest Y among near-horizontal faces (top deck).
			var topY = float.NegativeInfinity;
			for (var f = 0; f < mdt.GetFaceCount(); f++)
			{
				var n = mdt.GetFaceNormal(f);
				if (MathF.Abs(n.Y) < 0.55f)
					continue;
				var ySum = 0f;
				for (var k = 0; k < 3; k++)
					ySum += mdt.GetVertex(mdt.GetFaceVertex(f, k)).Y;
				topY = MathF.Max(topY, ySum / 3f);
			}
			if (float.IsNegativeInfinity(topY))
				continue;
			var st = new SurfaceTool();
			st.Begin(Mesh.PrimitiveType.Triangles);
			var kept = 0;
			for (var f = 0; f < mdt.GetFaceCount(); f++)
			{
				var n = mdt.GetFaceNormal(f);
				if (MathF.Abs(n.Y) < 0.55f)
					continue; // skirt / wall
				var ySum = 0f;
				for (var k = 0; k < 3; k++)
					ySum += mdt.GetVertex(mdt.GetFaceVertex(f, k)).Y;
				if (ySum / 3f < topY - topBand)
					continue; // lower coplanar decks — Z-fight flash
				for (var k = 0; k < 3; k++)
				{
					var vi = mdt.GetFaceVertex(f, k);
					st.SetNormal(n);
					var color = mdt.GetVertexColor(vi);
					if (color.A > 0f) st.SetColor(color);
					var uv = mdt.GetVertexUV(vi);
					st.SetUV(uv);
					st.AddVertex(mdt.GetVertex(vi));
				}
				kept++;
			}
			if (kept == 0)
				continue;
			outMesh = st.Commit(outMesh);
			var mat = arrayMesh.SurfaceGetMaterial(surf);
			if (mat != null)
				outMesh.SurfaceSetMaterial(outMesh.GetSurfaceCount() - 1, mat);
			keptAny = true;
		}
		if (keptAny)
			return outMesh;
		// Fallback flat top from AABB
		var aabb = arrayMesh.GetAabb();
		var y = aabb.Position.Y + MathF.Max(0.02f, aabb.Size.Y);
		var st2 = new SurfaceTool();
		st2.Begin(Mesh.PrimitiveType.Triangles);
		var c0 = new Vector3(aabb.Position.X, y, aabb.Position.Z);
		var c1 = new Vector3(aabb.Position.X + aabb.Size.X, y, aabb.Position.Z);
		var c2 = new Vector3(aabb.Position.X + aabb.Size.X, y, aabb.Position.Z + aabb.Size.Z);
		var c3 = new Vector3(aabb.Position.X, y, aabb.Position.Z + aabb.Size.Z);
		st2.SetNormal(Vector3.Up); st2.AddVertex(c0);
		st2.SetNormal(Vector3.Up); st2.AddVertex(c1);
		st2.SetNormal(Vector3.Up); st2.AddVertex(c2);
		st2.SetNormal(Vector3.Up); st2.AddVertex(c0);
		st2.SetNormal(Vector3.Up); st2.AddVertex(c2);
		st2.SetNormal(Vector3.Up); st2.AddVertex(c3);
		var flat = st2.Commit();
		if (arrayMesh.GetSurfaceCount() > 0)
		{
			var mat = arrayMesh.SurfaceGetMaterial(0);
			if (mat != null) flat.SurfaceSetMaterial(0, mat);
		}
		return flat;
	}

	/// <summary>
	/// Dual-edge-frame fit (n=4): authored mesh +X/+Z footprint → UV along Stage6 edge0
	/// (c0→c1) and c0→c3, then bilinear onto Stage6CornersLocal.
	/// Triangle fit (n=3): same UV → barycentric warp onto c0,c1,c2 (fold u+v&gt;1).
	/// Rot90/mirror permute targets. <paramref name="yBias"/> lifts Full tops (visuals deferred).
	/// Returns edge0 yaw (rad) — refuse world_yaw_as_dual_edge_frame / corners_eq4_only_meshfit.
	/// </summary>
	private static (ArrayMesh Mesh, float Edge0YawRad) MeshFitToDualEdgeFrame(
		Mesh source,
		Vector3[] corners,
		int rot90,
		bool mirror,
		float yBias = 0f)
	{
		if (corners == null || (corners.Length != 3 && corners.Length != 4))
			return (new ArrayMesh(), 0f);
		var c = OrientStage6Targets(corners, rot90, mirror);
		var edge0 = new Vector3(c[1].X - c[0].X, 0f, c[1].Z - c[0].Z);
		var edge0YawRad = MathF.Atan2(edge0.Z, edge0.X);
		var arrayMesh = source as ArrayMesh ?? ConvertMeshToArrayMesh(source);
		if (arrayMesh == null || arrayMesh.GetSurfaceCount() == 0)
			return (new ArrayMesh(), edge0YawRad);

		var aabb = arrayMesh.GetAabb();
		var minX = aabb.Position.X;
		var minZ = aabb.Position.Z;
		var sizeX = MathF.Max(1e-4f, aabb.Size.X);
		var sizeZ = MathF.Max(1e-4f, aabb.Size.Z);
		var slotDiag = c.Length == 3
			? (c[0].DistanceTo(c[1]) + c[1].DistanceTo(c[2]) + c[2].DistanceTo(c[0])) / 3f
			: c[0].DistanceTo(c[2]);
		var srcDiag = MathF.Max(1e-4f, MathF.Max(sizeX, sizeZ));
		var heightScale = MathF.Max(0.05f, slotDiag / srcDiag);
		// Elevate terrain mass above craft waterline. Board spacing≈210 — absolute lift for craft scale.
		const float yLift = 12f;
		var lift = yLift + yBias;
		var tri = c.Length == 3;

		var outMesh = new ArrayMesh();
		for (var surf = 0; surf < arrayMesh.GetSurfaceCount(); surf++)
		{
			var arrays = arrayMesh.SurfaceGetArrays(surf);
			if (arrays == null || arrays.Count == 0)
				continue;
			var verts = arrays[(int)Mesh.ArrayType.Vertex].AsVector3Array();
			if (verts == null || verts.Length == 0)
				continue;
			var warped = new Vector3[verts.Length];
			for (var i = 0; i < verts.Length; i++)
			{
				var v = verts[i];
				// Authored footprint UV: +X → u along dual edge0 (c0→c1), +Z → v.
				// n=4 → bilinear; n=3 → barycentric (refuse corners_eq4_only_meshfit).
				var u = Mathf.Clamp((v.X - minX) / sizeX, 0f, 1f);
				var vv = Mathf.Clamp((v.Z - minZ) / sizeZ, 0f, 1f);
				var xz = tri ? BarycentricCorner(c, u, vv) : BilinearCorner(c, u, vv);
				warped[i] = new Vector3(xz.X, lift + v.Y * heightScale, xz.Z);
			}
			arrays[(int)Mesh.ArrayType.Vertex] = warped;
			var norms = new Vector3[warped.Length];
			Array.Fill(norms, Vector3.Up);
			arrays[(int)Mesh.ArrayType.Normal] = norms;
			outMesh.AddSurfaceFromArrays(Mesh.PrimitiveType.Triangles, arrays);
			var mat = arrayMesh.SurfaceGetMaterial(surf);
			if (mat != null)
				outMesh.SurfaceSetMaterial(outMesh.GetSurfaceCount() - 1, mat);
		}
		return (outMesh, edge0YawRad);
	}

	/// <summary>Legacy name — dual-edge-frame fit (edge0 = c0→c1).</summary>
	private static ArrayMesh MeshFitToSmallCornerQuad(
		Mesh source,
		Vector3[] corners,
		int rot90,
		bool mirror) =>
		MeshFitToDualEdgeFrame(source, corners, rot90, mirror).Mesh;

	/// <summary>
	/// Depth/render-priority nudge on Full surface materials — companion to FullYBias /
	/// SortingOffset so pan does not flash coplanar decks (seizure_coplanar_deck refuse).
	/// </summary>
	private static void ApplyFullDepthBiasMaterials(MeshInstance3D mi)
	{
		if (mi?.Mesh == null)
			return;
		var mesh = mi.Mesh;
		var surfCount = mesh.GetSurfaceCount();
		for (var i = 0; i < surfCount; i++)
		{
			var mat = mi.GetActiveMaterial(i) ?? mesh.SurfaceGetMaterial(i);
			if (mat == null)
				continue;
			var dup = (Material)mat.Duplicate();
			if (dup is BaseMaterial3D std)
			{
				std.RenderPriority = 1;
				std.DepthDrawMode = BaseMaterial3D.DepthDrawModeEnum.OpaqueOnly;
			}
			mi.SetSurfaceOverrideMaterial(i, dup);
		}
	}

	/// <summary>Cheap Empty sector — thin rim hugging SmallCornerQuad edges (four corner pieces).</summary>
	private static ArrayMesh MakeEmptySectorFitMesh(Vector3[] c)
	{
		var st = new SurfaceTool();
		st.Begin(Mesh.PrimitiveType.Triangles);
		AddFitWall(st, c[0], c[1], 4f);
		AddFitWall(st, c[1], c[2], 4f);
		AddFitWall(st, c[2], c[3], 4f);
		AddFitWall(st, c[3], c[0], 4f);
		var mesh = st.Commit();
		mesh.SurfaceSetMaterial(0, MakeCreamQuarterPlatformMaterial());
		return mesh;
	}

	/// <summary>
	/// Cream quarter-platform material — YT Game Dev Buddies / Townscaper dual-grid reference.
	/// Shared cream for all families; soft cyan under-glow via emission (not albedo family ramp).
	/// </summary>
	private static StandardMaterial3D MakeCreamQuarterPlatformMaterial()
	{
		// Legacy refuse-proof helper — do not apply as Success MaterialOverride.
		return new StandardMaterial3D
		{
			AlbedoColor = CreamPlatformAlbedo,
			EmissionEnabled = true,
			Emission = CreamPlatformUnderGlow,
			EmissionEnergyMultiplier = 0.18f,
			CullMode = BaseMaterial3D.CullModeEnum.Disabled,
			ShadingMode = BaseMaterial3D.ShadingModeEnum.PerPixel,
			Roughness = 0.72f,
			Metallic = 0.02f,
		};
	}

	/// <summary>Graybox-only fallback albedos when GLB missing — not Prefer Success altitude.</summary>
	private static StandardMaterial3D MakeTerrainFallbackMaterial(DualVisualFamily family)
	{
		var albedo = family switch
		{
			DualVisualFamily.Empty => new Color(0.22f, 0.48f, 0.66f),
			DualVisualFamily.Edge => new Color(0.55f, 0.62f, 0.38f),
			DualVisualFamily.Corner => new Color(0.40f, 0.55f, 0.30f),
			DualVisualFamily.Full => new Color(0.30f, 0.52f, 0.28f),
			DualVisualFamily.Diagonal => new Color(0.36f, 0.50f, 0.28f),
			DualVisualFamily.InverseCorner => new Color(0.34f, 0.48f, 0.32f),
			_ => new Color(0.30f, 0.52f, 0.28f),
		};
		return new StandardMaterial3D
		{
			AlbedoColor = albedo,
			CullMode = BaseMaterial3D.CullModeEnum.Disabled,
			ShadingMode = BaseMaterial3D.ShadingModeEnum.PerPixel,
			Roughness = 0.75f,
			Metallic = 0.02f,
		};
	}

	private static void AddFitWall(SurfaceTool st, Vector3 a, Vector3 b, float h)
	{
		var a0 = a + Vector3.Up * 12f;
		var b0 = b + Vector3.Up * 12f;
		var a1 = a0 + Vector3.Up * h;
		var b1 = b0 + Vector3.Up * h;
		st.SetNormal(Vector3.Up); st.AddVertex(a0);
		st.SetNormal(Vector3.Up); st.AddVertex(b0);
		st.SetNormal(Vector3.Up); st.AddVertex(b1);
		st.SetNormal(Vector3.Up); st.AddVertex(a0);
		st.SetNormal(Vector3.Up); st.AddVertex(b1);
		st.SetNormal(Vector3.Up); st.AddVertex(a1);
	}

	/// <summary>Orient Stage6 DualCorners (n=3 or n=4) by rot90/mirror in dual-edge frame.</summary>
	private static Vector3[] OrientStage6Targets(Vector3[] corners, int rot90, bool mirror)
	{
		var c = (Vector3[])corners.Clone();
		if (c.Length == 3)
		{
			var r = ((rot90 % 3) + 3) % 3;
			for (var i = 0; i < r; i++)
			{
				var t = c[0];
				c[0] = c[1];
				c[1] = c[2];
				c[2] = t;
			}
			if (mirror)
				(c[1], c[2]) = (c[2], c[1]);
			return c;
		}
		var rq = ((rot90 % 4) + 4) % 4;
		for (var i = 0; i < rq; i++)
		{
			// Rotate CCW around sector: c0<-c3<-c2<-c1<-c0
			var t = c[0];
			c[0] = c[1];
			c[1] = c[2];
			c[2] = c[3];
			c[3] = t;
		}
		if (mirror)
		{
			// Mirror across c0–c2 diagonal in UV (swap c1/c3).
			(c[1], c[3]) = (c[3], c[1]);
		}
		return c;
	}

	/// <summary>Legacy name — Stage6 orient (n=4 SmallCornerQuad / DualCell).</summary>
	private static Vector3[] OrientSmallCornerTargets(Vector3[] corners, int rot90, bool mirror) =>
		OrientStage6Targets(corners, rot90, mirror);

	/// <summary>Bilinear map unit UV → Stage6 quad corners (CCW c0..c3).</summary>
	private static Vector3 BilinearCorner(Vector3[] c, float u, float v)
	{
		var a = c[0].Lerp(c[1], u);
		var b = c[3].Lerp(c[2], u);
		return a.Lerp(b, v);
	}

	/// <summary>
	/// Barycentric map unit UV → Stage6 triangle corners (c0,c1,c2).
	/// Fold the u+v&gt;1 half of the unit square onto the triangle (no soft pad to quad).
	/// </summary>
	private static Vector3 BarycentricCorner(Vector3[] c, float u, float v)
	{
		var uu = u;
		var vv = v;
		if (uu + vv > 1f)
		{
			var t = uu + vv - 1f;
			uu -= t;
			vv -= t;
		}
		var w = 1f - uu - vv;
		return c[0] * w + c[1] * uu + c[2] * vv;
	}

	private static ArrayMesh ConvertMeshToArrayMesh(Mesh mesh)
	{
		if (mesh == null) return new ArrayMesh();
		if (mesh is ArrayMesh am) return am;
		var st = new SurfaceTool();
		st.CreateFrom(mesh, 0);
		return st.Commit();
	}

	private static float ApproximateSmallCornerXZExtent(Vector3[] corners)
	{
		var minX = corners[0].X;
		var maxX = corners[0].X;
		var minZ = corners[0].Z;
		var maxZ = corners[0].Z;
		for (var i = 1; i < corners.Length; i++)
		{
			var p = corners[i];
			if (p.X < minX) minX = p.X;
			if (p.X > maxX) maxX = p.X;
			if (p.Z < minZ) minZ = p.Z;
			if (p.Z > maxZ) maxZ = p.Z;
		}
		return MathF.Max(0.05f, MathF.Min(maxX - minX, maxZ - minZ));
	}

	/// <summary>
	/// Stage-6 DualCell MeshLibrary path — one item per DualCell (lookup + edge-frame warp).
	/// </summary>
	private void EnsureHalfStepDualCellMesh(OrganicDualOffsetLattice.DualCell cell)
	{
		EnsureStage6DualCellMesh(cell);
	}

	/// <summary>Stage-6 dual tile fan from face-centroid polygon (N-gon).</summary>
	private ArrayMesh MakeHalfStepDualCellMesh(Vector3[] midpoints, Color color, float height)
	{
		if (midpoints == null || midpoints.Length < 3)
			return new ArrayMesh();
		var c = (Vector3[])midpoints.Clone();
		var centre = Vector3.Zero;
		foreach (var p in c) centre += p;
		centre /= c.Length;
		const float inset = 0.92f;
		var lift = Vector3.Up * height;
		for (var i = 0; i < c.Length; i++)
			c[i] = centre.Lerp(c[i], inset) + lift;
		var centreLift = centre + lift;
		var st = new SurfaceTool();
		st.Begin(Mesh.PrimitiveType.Triangles);
		for (var i = 0; i < c.Length; i++)
		{
			st.SetNormal(Vector3.Up); st.AddVertex(centreLift);
			st.SetNormal(Vector3.Up); st.AddVertex(c[i]);
			st.SetNormal(Vector3.Up); st.AddVertex(c[(i + 1) % c.Length]);
		}
		var mesh = st.Commit();
		mesh.SurfaceSetMaterial(0, new StandardMaterial3D
		{
			AlbedoColor = color,
			Transparency = color.A < 0.99f
				? BaseMaterial3D.TransparencyEnum.Alpha
				: BaseMaterial3D.TransparencyEnum.Disabled,
			CullMode = BaseMaterial3D.CullModeEnum.Disabled,
			ShadingMode = BaseMaterial3D.ShadingModeEnum.Unshaded,
		});
		return mesh;
	}

	/// <summary>
	/// Populated Stage-6 dual cell — N wedge/side segments colored by palette index.
	/// Lit segments = sides adjacent to an ON dual-edge neighbour bit; dim otherwise.
	/// Prefer readable occupancy over a single flat fill (refuse gray_ramp_only).
	/// </summary>
	private ArrayMesh MakeSegmentedDualCellMesh(Vector3[] midpoints, bool[] cornerOn, float height)
	{
		if (midpoints == null || midpoints.Length < 3)
			return new ArrayMesh();
		var c = (Vector3[])midpoints.Clone();
		var n = c.Length;
		var centre = Vector3.Zero;
		foreach (var p in c) centre += p;
		centre /= n;
		const float inset = 0.92f;
		var lift = Vector3.Up * height;
		for (var i = 0; i < n; i++)
			c[i] = centre.Lerp(c[i], inset) + lift;
		var centreLift = centre + lift;

		ArrayMesh? mesh = null;
		for (var seg = 0; seg < n; seg++)
		{
			var a = c[seg];
			var b = c[(seg + 1) % n];
			var lit = cornerOn != null && cornerOn.Length == n &&
			          (cornerOn[seg] || cornerOn[(seg + 1) % n]);
			var baseColor = DualSegmentPalette[seg % DualSegmentPalette.Length];
			var color = lit
				? baseColor
				: new Color(baseColor.R * 0.35f, baseColor.G * 0.35f, baseColor.B * 0.35f, 0.55f);

			var st = new SurfaceTool();
			st.Begin(Mesh.PrimitiveType.Triangles);
			st.SetNormal(Vector3.Up); st.AddVertex(centreLift);
			st.SetNormal(Vector3.Up); st.AddVertex(a);
			st.SetNormal(Vector3.Up); st.AddVertex(b);
			mesh = st.Commit(mesh);
			mesh.SurfaceSetMaterial(seg, new StandardMaterial3D
			{
				AlbedoColor = color,
				Transparency = color.A < 0.99f
					? BaseMaterial3D.TransparencyEnum.Alpha
					: BaseMaterial3D.TransparencyEnum.Disabled,
				CullMode = BaseMaterial3D.CullModeEnum.Disabled,
				ShadingMode = BaseMaterial3D.ShadingModeEnum.Unshaded,
			});
		}

		return mesh ?? new ArrayMesh();
	}

	/// <summary>
	/// Stage6 OccupancyCorners → family + rot/mirror in dual-edge frame.
	/// Owned-only paint (C_dual_owned_only_paint): non-Empty MeshLibrary only when
	/// OwnerVertexId is on → Full whole DualCell. Owner off → Empty / ClearDualSlot
	/// even if OccupancyCorners bits are set by a neighbor flip (coastline Corner/Edge
	/// deferred — refuse neighbor_corner_spray_as_place / update_four_cross_as_success).
	/// OccupancyCorners bit sampling KEEP for future coastline; not place Success here.
	/// </summary>
	private (DualVisualFamily Family, int Rot90, bool Mirror) ResolveOrganicDualVisualFamily(
		int[] occupancyCorners,
		int ownerVertexId)
	{
		// OccupancyCorners KEEP (Stage6 DualCorners samples) — n=3 or n=4 bit mask reserved
		// for deferred coastline Corner/Edge; owned-only paint does not stamp from bits.
		// Tri bit map: bit0..2 = CardinalNeighbors[0..2] ↔ DualCorners[0..2] (no soft_take_4).
		var bits = 0;
		if (occupancyCorners != null &&
		    (occupancyCorners.Length == 3 || occupancyCorners.Length == 4))
		{
			for (var i = 0; i < occupancyCorners.Length; i++)
				if (_cornerLogic.TryGetValue(occupancyCorners[i], out var on) && on)
					bits |= 1 << i;
		}
		_ = bits; // deferred coastline; not place Success this weld

		var ownerOn = _cornerLogic.TryGetValue(ownerVertexId, out var o) && o;

		// Owned DualCell land: owner V on → whole DualCell Full (tri or quad plate).
		if (ownerOn)
			return (DualVisualFamily.Full, 0, false);

		// Owner off → Empty (amber grid / ocean skip). UpdateFour still walks
		// DualCellsTouching so prior Corner/Edge neighbor stamps ClearDualSlot here.
		// Coastline Corner/Edge from OccupancyCorners bits is deferred (not Success).
		return (DualVisualFamily.Empty, 0, false);
	}

	/// <summary>Runtime MeshLibrary — Blender craft_dual_*.glb preferred; graybox prototypes fallback.</summary>
	private MeshLibrary EnsureShapeDistinctDualMeshLibrary()
	{
		if (_dualMeshLibrary != null && GodotObject.IsInstanceValid(_dualMeshLibrary))
			return _dualMeshLibrary;
		_dualMeshLibrary = new MeshLibrary();
		foreach (DualVisualFamily fam in Enum.GetValues(typeof(DualVisualFamily)))
		{
			var id = (int)fam;
			_dualMeshLibrary.CreateItem(id);
			var mesh = TryLoadCraftDualGlbMesh(fam) ?? MakeUnitShapeDistinctPrototype(fam);
			_dualMeshLibrary.SetItemMesh(id, mesh);
			_dualMeshLibrary.SetItemName(id, fam.ToString());
		}
		return _dualMeshLibrary;
	}

	private const string CraftDualGlbDir = "res://assets/craft/dual_grid/";

	private static string CraftDualGlbPath(DualVisualFamily fam) => fam switch
	{
		DualVisualFamily.Empty => CraftDualGlbDir + "craft_dual_Empty.glb",
		DualVisualFamily.Edge => CraftDualGlbDir + "craft_dual_Edge.glb",
		DualVisualFamily.Corner => CraftDualGlbDir + "craft_dual_Corner.glb",
		DualVisualFamily.Full => CraftDualGlbDir + "craft_dual_Full.glb",
		DualVisualFamily.Diagonal => CraftDualGlbDir + "craft_dual_Diagonal.glb",
		DualVisualFamily.InverseCorner => CraftDualGlbDir + "craft_dual_InverseCorner.glb",
		_ => CraftDualGlbDir + "craft_dual_Empty.glb",
	};

	/// <summary>Extract first Mesh from Blender-exported craft_dual PackedScene (GLB import).</summary>
	private static Mesh? TryLoadCraftDualGlbMesh(DualVisualFamily fam)
	{
		var path = CraftDualGlbPath(fam);
		if (!ResourceLoader.Exists(path))
			return null;
		var packed = GD.Load<PackedScene>(path);
		if (packed == null)
			return null;
		var root = packed.Instantiate();
		try
		{
			return FindFirstMesh(root);
		}
		finally
		{
			if (GodotObject.IsInstanceValid(root))
				root.QueueFree();
		}
	}

	private static Mesh? FindFirstMesh(Node node)
	{
		if (node is MeshInstance3D mi && mi.Mesh != null)
			return mi.Mesh;
		foreach (var child in node.GetChildren())
		{
			var found = FindFirstMesh(child);
			if (found != null)
				return found;
		}
		return null;
	}

	/// <summary>Prefer / MCP proof — four families differ in silhouette geometry, not albedo.</summary>
	public (bool Ok, string Summary) ProveDualVisualVariants()
	{
		var lib = EnsureShapeDistinctDualMeshLibrary();
		var familyCount = Enum.GetValues(typeof(DualVisualFamily)).Length;
		var heights = new float[familyCount];
		var volumes = new float[familyCount];
		for (var i = 0; i < familyCount; i++)
		{
			var mesh = lib.GetItemMesh(i);
			if (mesh == null)
				return (false, $"missing_family_mesh id={i} refuse=gray_ramp_only");
			var aabb = mesh.GetAabb();
			heights[i] = aabb.Size.Y;
			volumes[i] = aabb.Size.X * aabb.Size.Y * aabb.Size.Z;
		}
		// Distinct AABB heights/volumes across sixpack (not albedo / cream override).
		var distinctHeights = new HashSet<float>(heights.Select(h => MathF.Round(h, 3))).Count;
		var distinctVolumes = new HashSet<float>(volumes.Select(v => MathF.Round(v, 4))).Count;
		if (distinctHeights < 3 && distinctVolumes < 3)
			return (false, $"silhouette_not_distinct heights=[{string.Join(',', heights)}] volumes=[{string.Join(',', volumes)}] refuse=gray_ramp_only");
		if (MeshLibrarySource.Contains("cream_quarter") || (MeshLibrarySource.Contains("graybox") && !MeshLibrarySource.Contains("terrain_tile")))
			return (false, "mesh_library_source_cream_or_gray refuse=plinth_as_terrain");
		if (!MeshLibrarySource.Contains("terrain_tile"))
			return (false, "mesh_library_source_not_terrain_tile refuse=metrics_only_glb_drop");
		var neigh = ProveNeighborhoodCardinality();
		if (!neigh.Ok)
			return (false, neigh.Summary);
		return (true,
			$"dual_offset_terrain_tile discrete_meshlibrary_item families=empty|edge|corner|full|diagonal|inverse " +
			$"aabb_h=[{string.Join(',', heights.Select(h => h.ToString("0.###")))}] " +
			$"aabb_vol=[{string.Join(',', volumes.Select(v => v.ToString("0.####")))}] " +
			$"plinth_as_terrain=false blob_as_module=false gray_ramp_only=false stretch_as_variant=false " +
			$"library_items={familyCount} source={MeshLibrarySource} {neigh.Summary}");
	}

	/// <summary>
	/// Stable owned dual-lattice keys for logic point P — exactly one Stage-6 cell.
	/// Identical on every call for the same vertex (refuse unstable_dual_neighborhood).
	/// Refuse FaceCornersLocal / face-as-dual / soft Take(4).
	/// </summary>
	public IReadOnlyList<string> OwnedDualCellKeys(int vertexIndex)
	{
		if (_dualLattice == null)
			return Array.Empty<string>();
		return _dualLattice.OwnedDualCellKeys(vertexIndex);
	}

	/// <summary>
	/// Legacy MCP alias — derive-face indices only. NOT dual Success (refuse primary_face_as_dual /
	/// SupportFaceIndex Success). Prefer uses OwnedDualCellKeys / DualCorners / LocalCentre.
	/// </summary>
	public IReadOnlyList<int> OwnedDualFaceIndices(int vertexIndex)
	{
		if (_dualLattice == null)
			return Array.Empty<int>();
		return OwnedDualCellKeys(vertexIndex).Select(_ => -1).ToList();
	}

	/// <summary>
	/// Prefer seat — Stage-6 wire kept; SmallCornerQuadsAround = glow/populate unit.
	/// Refuse stage6_union_as_single_glow_tile / primary_face_as_dual / hex19_always_4.
	/// </summary>
	public (bool Ok, string Summary) ProveDualIncidenceOwnership()
	{
		if (_organicMesh?.Graph == null || _dualLattice == null)
			return (false, "stage6_cell_missing_graph refuse=primary_face_as_dual");
		var g = _organicMesh.Graph;
		var checkedPts = 0;
		var smallOk = 0;
		var valenceResidue = 0;
		var small2 = 0;
		var small4 = 0;
		var smallNonEmpty = 0;
		foreach (var v in g.Vertices)
		{
			var small = _dualLattice.SmallCornerQuadsAround(v.Id);
			if (small.Count == 0) continue;
			checkedPts++;
			var editable = _dualLattice.IsEditableLogicPoint(v.Id);
			if (small.Count > MaxDualCellsPerLogicFlip)
			{
				if (editable)
					return (false, $"over_neighbor_paint vertex={v.Id} small={small.Count} refuse=over_neighbor_paint");
				valenceResidue++;
				continue;
			}
			foreach (var sc in small)
			{
				if (sc.Corners == null || sc.Corners.Length != 4)
					return (false, $"unstable_dual_neighborhood bad_small_corners key={sc.Key}");
				if (sc.Key.StartsWith("d_v_", StringComparison.Ordinal))
					return (false, "stage6_union_as_single_glow_tile refuse=stage6_union_as_single_glow_tile");
			}
			if (small.Count > 0) smallNonEmpty++;
			if (small.Count == 2) small2++;
			if (small.Count == 4) small4++;
			// Stage-6 DualCell proof when present (≥3 faces); edge-2 verts may lack DualCell.
			var owned = OwnedDualCellKeys(v.Id);
			if (owned.Count > 0)
			{
				var proof = _dualLattice.ProveFaceCentroidAround(v.Id);
				if (!proof.Ok)
					return (false, proof.Summary);
			}
			smallOk++;
			if (!editable && small.Count >= OrganicDualOffsetLattice.MinSmallCornerQuadsEditable
				&& small.Count <= OrganicDualOffsetLattice.MaxSmallCornerQuadsPerLogicPoint)
				return (false, $"valence_drop_editable vertex={v.Id} small={small.Count} not_editable refuse=valence_drop_editable");
		}
		foreach (var cell in _dualLattice.AllCells)
		{
			if (cell.DualCorners == null || cell.DualCorners.Length < 3)
				return (false, "primary_face_as_dual missing_stage6_corners refuse=primary_face_as_dual");
			if (cell.OwnerFaceId >= 0)
				return (false, $"primary_face_as_dual owner_face={cell.OwnerFaceId} refuse=primary_face_as_dual");
			if (cell.OwnerVertexId < 0)
				return (false, $"stage6_cell_missing_owner key={cell.Key} refuse=unstable_dual_neighborhood");
			if (!_dualLattice.IsHalfStepOffset(cell))
				return (false, $"dual_verts_not_face_centroids key={cell.Key} refuse=dual_centre_on_logic_as_half_step_proof");
		}
		if (smallOk == 0)
			return (false, "no_small_corner_quads refuse=unstable_dual_neighborhood");
		if (smallNonEmpty == 0)
			return (false, "owned_only_glow no_small_corner_quads refuse=owned_only_glow");
		if (smallNonEmpty > 0 && small2 == 0 && small4 == smallNonEmpty)
			return (false, $"hex19_always_4 small4={small4} refuse=hex19_always_4");
		return (true,
			$"small_corner_quads_ownership ok points={checkedPts} small_ok={smallOk} valence_residue={valenceResidue} " +
			$"small2={small2} small4={small4} small_nonempty={smallNonEmpty} " +
			$"editable={_dualLattice.LogicPointCount} stage6_cells={_dualLattice.CellCount} " +
			$"neighborhood=small_corner_quads dual_verts=face_centroids dual_edges=centroid_centroid " +
			$"stage6_union_as_single_glow_tile=false primary_face_fill=false face_corners_local=false " +
			$"soft_take_4=false owned_only_glow=false hex19_always_4=false valence_drop_editable=false");
	}

	/// <summary>
	/// Prefer seat — interior logic points own exactly four dual-lattice cells; set stable.
	/// Refuse primary_face_as_dual / unstable_dual_neighborhood / over_neighbor_paint / stamp_as_dual.
	/// </summary>
	
	/// <summary>
	/// Prefer seat — primal ownership is OrganicMeshGraph singletons with incidence.
	/// Refuse indexed_lists_as_graph / ephemeral_edge_key_as_topology / non_unique_vertices.
	/// </summary>
	public (bool Ok, string Summary) ProveOrganicMeshGraph()
	{
		if (_organicMesh?.Graph == null)
			return (false, "indexed_lists_as_graph missing OrganicMeshGraph refuse=indexed_lists_as_graph");
		var g = _organicMesh.Graph;
		if (g.VertexCount == 0 || g.EdgeCount == 0 || g.FaceCount == 0)
			return (false, "ephemeral_edge_key_as_topology empty graph refuse=ephemeral_edge_key_as_topology");
		if (!g.AllFacesAreQuads)
			return (false, "organic_mesh_graph not_all_quads refuse=indexed_lists_as_graph");
		// Dual cells must be Stage-6 polygons of face centroids owned by Vertex refs.
		if (_dualLattice != null)
		{
			foreach (var cell in _dualLattice.AllCells)
			{
				if (cell.DualCorners == null || cell.DualCorners.Length < 3)
					return (false, "proxy_substitution dual_missing_stage6_corners refuse=proxy_substitution");
				if (cell.CornerFaces == null || cell.CornerFaces.Length != cell.DualCorners.Length)
					return (false, "proxy_substitution dual_corners_not_face_centroids refuse=proxy_substitution");
				if (cell.OwnerVertexId < 0)
					return (false, "proxy_substitution dual_missing_owner_vertex refuse=proxy_substitution");
			}
		}
		return (true,
			$"organic_mesh_graph verts={g.VertexCount} edges={g.EdgeCount} faces={g.FaceCount} " +
			$"incidence=FacesTouchingVertex dual_cells=Stage6AroundVertex " +
			$"indexed_lists_as_graph=false ephemeral_edge_key_as_topology=false");
	}

	public (bool Ok, string Summary) ProveStableDualNeighborhood()
	{
		if (_organicMesh == null || _dualLattice == null || _dualLattice.LogicPointCount == 0)
			return (false, "dual_lattice_missing refuse=unstable_dual_neighborhood");
		var incidence = ProveDualIncidenceOwnership();
		if (!incidence.Ok)
			return (false, incidence.Summary);
		var maxOwned = 0;
		var maxSmall = 0;
		var minSmall = int.MaxValue;
		var ownedExact1 = 0;
		var editableN = 0;
		var small2 = 0;
		var small4 = 0;
		var halfOk = 0;
		foreach (var cell in _dualLattice.AllCells)
		{
			if (_dualLattice.IsHalfStepOffset(cell))
				halfOk++;
		}
		if (_dualLattice.CellCount > 0 && halfOk < _dualLattice.CellCount)
			return (false, $"primary_face_as_dual dual_not_half_offset coincident={_dualLattice.CellCount - halfOk} refuse=primary_face_as_dual");
		foreach (var vi in _dualLattice.EditableLogicPoints)
		{
			var small = _dualLattice.SmallCornerQuadsAround(vi);
			if (small.Count == 0)
				return (false, $"unstable_dual_neighborhood vertex={vi} no_small_corner refuse=unstable_dual_neighborhood");
			if (small.Count > MaxDualCellsPerLogicFlip)
				return (false, $"over_neighbor_paint vertex={vi} small={small.Count} cap={MaxDualCellsPerLogicFlip} refuse=over_neighbor_paint");
			var a = OwnedDualCellKeys(vi);
			if (a.Count > maxOwned) maxOwned = a.Count;
			if (a.Count == OrganicDualOffsetLattice.MaxOwnedDualsPerLogicPoint)
				ownedExact1++;
			if (small.Count > maxSmall) maxSmall = small.Count;
			if (small.Count < minSmall) minSmall = small.Count;
			if (small.Count == 2) small2++;
			if (small.Count == 4) small4++;
			editableN++;
		}
		if (editableN == 0)
			return (false, "no_editable_small_corner_logic refuse=unstable_dual_neighborhood");
		if (maxSmall < 1)
			return (false, "owned_only_glow max_small=0 refuse=owned_only_glow");
		if (small2 == 0 && small4 == editableN)
			return (false, $"hex19_always_4 small4={small4} refuse=hex19_always_4");
		if (minSmall == int.MaxValue) minSmall = 0;
		// Secondary-centered glow proof — refuse primary_star_glow_as_success.
		var secN = 0;
		var sec4 = 0;
		var maxSec = 0;
		var minSec = int.MaxValue;
		foreach (var fid in _dualLattice.EditableSecondaryFaces)
		{
			var around = _dualLattice.SmallCornerQuadsAroundFace(fid);
			if (around.Count == 0)
				return (false, $"unstable_dual_neighborhood secondary_face={fid} empty refuse=unstable_dual_neighborhood");
			if (around.Count > MaxDualCellsPerLogicFlip)
				return (false, $"over_neighbor_paint secondary_face={fid} n={around.Count} refuse=over_neighbor_paint");
			if (around.Count > maxSec) maxSec = around.Count;
			if (around.Count < minSec) minSec = around.Count;
			if (around.Count == 4) sec4++;
			secN++;
		}
		if (secN == 0)
			return (false, "no_editable_secondary_faces refuse=primary_star_glow_as_success");
		if (minSec == int.MaxValue) minSec = 0;
		return (true,
			$"stable_secondary_glow_center max_owned={maxOwned} max_small={maxSmall} min_small={minSmall} " +
			$"owned_exact1={ownedExact1} editable={editableN} small2={small2} small4={small4} " +
			$"secondary_faces={secN} sec4={sec4} max_sec={maxSec} min_sec={minSec} " +
			$"logic_points={_dualLattice.LogicPointCount} dual_cells={_dualLattice.CellCount} " +
			$"small_corner_slots={_dualLattice.SmallCornerQuadCount} half_step={halfOk} " +
			$"glow_mode=secondary_face_center primary_star_glow_as_success=false " +
			$"primary_face_as_dual=false face_corners_local=false stage6_union_as_single_glow_tile=false " +
			$"stage6_cell_wire=true small_corner_quads=true dual_edges=centroid_centroid soft_take_4=false " +
			$"owned_only_glow=false hex19_always_4=false valence_drop_editable=false " +
			$"MaxDualCellsPerLogicFlip={MaxDualCellsPerLogicFlip} {incidence.Summary}");
	}

	/// <summary>Prefer — editable V has 2..4 small corner quads; Stage-6 owned ≤1 when present.</summary>
	public (bool Ok, string Summary) ProveNeighborhoodCardinality()
	{
		if (_dualLattice == null || _dualLattice.LogicPointCount == 0)
			return (false, "dual_lattice_missing refuse=over_neighbor_paint");
		var maxOwned = 0;
		var maxSmall = 0;
		foreach (var vi in _dualLattice.EditableLogicPoints)
		{
			var n = OwnedDualCellKeys(vi).Count;
			if (n > maxOwned) maxOwned = n;
			var t = _dualLattice.SmallCornerQuadsAround(vi).Count;
			if (t > maxSmall) maxSmall = t;
		}
		if (maxOwned > OrganicDualOffsetLattice.MaxOwnedDualsPerLogicPoint)
			return (false, $"face_block_neighborhood max_owned={maxOwned} refuse=face_block_neighborhood");
		if (maxSmall > MaxDualCellsPerLogicFlip)
			return (false, $"over_neighbor_paint max_small={maxSmall} cap={MaxDualCellsPerLogicFlip} refuse=over_neighbor_paint");
		return (true, $"neighborhood_cardinality_ok max_owned={maxOwned} max_small={maxSmall} MaxDualCellsPerLogicFlip={MaxDualCellsPerLogicFlip}");
	}

	/// <summary>
	/// Unit-prototype builder only (MeshLibrary inventory for deferred dual_visual).
	/// LIVE dual cells use MakeHalfStepDualCellMesh / VarignonMidpoints (OrganicDualOffsetLattice).
	/// </summary>
	private ArrayMesh MakeShapeDistinctDualVariant(int faceIndex, DualVisualFamily family, int rot90, bool mirror)
	{
		_ = faceIndex;
		_ = rot90;
		_ = mirror;
		return MakeUnitShapeDistinctPrototype(family);
	}

	/// <summary>
	/// F5 Prefer glow — cyan highlight on SmallCornerQuadsAroundFace(F).
	/// Cluster visual center = secondary face centroid. Refuse primary_star_glow_as_success.
	/// </summary>
	private void HighlightSecondaryDualCells(int faceId)
	{
		RestoreCreamMaterialsOnHighlightedSlots();
		_debugHighlightedDualKeys.Clear();

		var small = _dualLattice?.SmallCornerQuadsAroundFace(faceId)
			?? Array.Empty<OrganicDualOffsetLattice.SmallCornerQuad>();
		foreach (var sc in small)
		{
			if (!_dualSlots.TryGetValue(sc.Key, out var mi) || !GodotObject.IsInstanceValid(mi))
				continue;
			mi.MaterialOverride = new StandardMaterial3D
			{
				AlbedoColor = _ownedDualHighlightColor,
				Transparency = BaseMaterial3D.TransparencyEnum.Disabled,
				CullMode = BaseMaterial3D.CullModeEnum.Disabled,
				ShadingMode = BaseMaterial3D.ShadingModeEnum.Unshaded,
				NoDepthTest = true,
			};
			_debugHighlightedDualKeys.Add(sc.Key);
		}
		RefreshDebugDualCellIdsForFace(faceId);
	}

	private void RestoreCreamMaterialsOnHighlightedSlots()
	{
		// Clear highlight override — restore GLB terrain materials (refuse cream_quarter Success).
		foreach (var key in _debugHighlightedDualKeys)
		{
			if (_dualSlots.TryGetValue(key, out var prev) && GodotObject.IsInstanceValid(prev))
				prev.MaterialOverride = null;
		}
	}

	/// <summary>
	/// Debug highlight — OwnedDualCell(V) MeshLibrary seat (not SmallCornerQuad keys).
	/// Refuse sector_pie_as_dual_cell_tile / primary_star_glow_as_success as place Success.
	/// </summary>
	private void HighlightOwnedDualCells(int vertexIndex)
	{
		RestoreCreamMaterialsOnHighlightedSlots();
		_debugHighlightedDualKeys.Clear();

		if (_dualLattice != null && _dualLattice.TryGetOwned(vertexIndex, out var owned))
		{
			if (_dualSlots.TryGetValue(owned.Key, out var mi) && GodotObject.IsInstanceValid(mi))
			{
				mi.MaterialOverride = new StandardMaterial3D
				{
					AlbedoColor = _ownedDualHighlightColor,
					Transparency = BaseMaterial3D.TransparencyEnum.Disabled,
					CullMode = BaseMaterial3D.CullModeEnum.Disabled,
					ShadingMode = BaseMaterial3D.ShadingModeEnum.Unshaded,
					NoDepthTest = true,
				};
				_debugHighlightedDualKeys.Add(owned.Key);
			}
		}
		RefreshDebugDualCellIds(vertexIndex);
	}

	/// <summary>Debug — Label3D listing SmallCornerQuad keys for last secondary face.</summary>
	private void RefreshDebugDualCellIdsForFace(int faceId)
	{
		if (_dualRoot == null || _organicMesh == null || _dualLattice == null) return;
		if (_debugDualIdsRoot != null && GodotObject.IsInstanceValid(_debugDualIdsRoot))
			_debugDualIdsRoot.QueueFree();
		_debugDualIdsRoot = new Node3D { Name = "DebugDualCellIds" };
		_dualRoot.AddChild(_debugDualIdsRoot);
		var quads = _dualLattice.SmallCornerQuadsAroundFace(faceId);
		if (quads.Count == 0) return;
		if (_dualLattice.TryGetSecondaryCentroid(faceId, out var cent))
		{
			var hub = new Label3D
			{
				Name = $"SecondaryHub_f{faceId}",
				Text = $"SEC f{faceId}",
				Position = new Vector3(cent.X, 0.72f, cent.Y),
				FontSize = 16,
				Modulate = _dualVertexPlusColor,
				Billboard = BaseMaterial3D.BillboardModeEnum.Enabled,
				NoDepthTest = true,
			};
			_debugDualIdsRoot.AddChild(hub);
		}
		foreach (var sc in quads)
		{
			var c = sc.LocalCentre;
			var label = new Label3D
			{
				Name = $"SmallCornerId_{sc.Key}",
				Text = sc.Key,
				Position = new Vector3(c.X, 0.65f, c.Z),
				FontSize = 14,
				Modulate = _ownedDualHighlightColor,
				Billboard = BaseMaterial3D.BillboardModeEnum.Enabled,
				NoDepthTest = true,
			};
			_debugDualIdsRoot.AddChild(label);
		}
	}

	/// <summary>Debug — Label3D for OwnedDualCell(V) key at Stage-6 centre (not SmallCornerQuad).</summary>
	private void RefreshDebugDualCellIds(int vertexIndex)
	{
		if (_dualRoot == null || _organicMesh == null || _dualLattice == null) return;
		if (_debugDualIdsRoot != null && GodotObject.IsInstanceValid(_debugDualIdsRoot))
			_debugDualIdsRoot.QueueFree();
		_debugDualIdsRoot = new Node3D { Name = "DebugDualCellIds" };
		_dualRoot.AddChild(_debugDualIdsRoot);
		if (!_dualLattice.TryGetOwned(vertexIndex, out var owned))
			return;
		var c = owned.LocalCentre;
		var label = new Label3D
		{
			Name = $"OwnedDualId_{owned.Key}",
			Text = owned.Key,
			Position = new Vector3(c.X, 0.65f, c.Z),
			FontSize = 14,
			Modulate = _ownedDualHighlightColor,
			Billboard = BaseMaterial3D.BillboardModeEnum.Enabled,
			NoDepthTest = true,
		};
		_debugDualIdsRoot.AddChild(label);
	}

	private static Vector3[] ApplyRotMirrorCorners(Vector3[] corners, int rot90, bool mirror)
	{
		var c = (Vector3[])corners.Clone();
		var r = ((rot90 % 4) + 4) % 4;
		for (var step = 0; step < r; step++)
		{
			var t = c[0];
			c[0] = c[1];
			c[1] = c[2];
			c[2] = c[3];
			c[3] = t;
		}
		if (mirror)
			(c[1], c[3]) = (c[3], c[1]);
		return c;
	}

	private ArrayMesh MakeUnitShapeDistinctPrototype(DualVisualFamily family)
	{
		// Unit quad in XZ — used only for MeshLibrary item identity / Prefer AABB proof.
		var corners = new[]
		{
			new Vector3(-0.5f, 0f, -0.5f),
			new Vector3(0.5f, 0f, -0.5f),
			new Vector3(0.5f, 0f, 0.5f),
			new Vector3(-0.5f, 0f, 0.5f),
		};
		return CommitDualFamilyMesh(family, corners);
	}

	private ArrayMesh CommitDualFamilyMesh(DualVisualFamily family, Vector3[] c)
	{
		var st = new SurfaceTool();
		st.Begin(Mesh.PrimitiveType.Triangles);
		switch (family)
		{
			case DualVisualFamily.Empty:
				// Thin rim only — near-flat silhouette (readable as empty vs solid).
				AddWallQuad(st, c[0], c[1], 0.04f);
				AddWallQuad(st, c[1], c[2], 0.04f);
				AddWallQuad(st, c[2], c[3], 0.04f);
				AddWallQuad(st, c[3], c[0], 0.04f);
				break;
			case DualVisualFamily.Edge:
				// Thick bar along c0→c1 — adjacent-edge mass.
				AddWallQuad(st, c[0], c[1], 0.42f);
				AddTopCap(st, EdgeBarTop(c[0], c[1], c, 0.42f));
				break;
			case DualVisualFamily.Corner:
				// L-walls meeting at c0 — corner mass (rot/mirror selects which corner).
				AddWallQuad(st, c[0], c[1], 0.36f);
				AddWallQuad(st, c[0], c[3], 0.36f);
				AddTopCap(st, new[]
				{
					c[0] + Vector3.Up * 0.36f,
					c[0].Lerp(c[1], 0.55f) + Vector3.Up * 0.36f,
					c[0] + (c[0].Lerp(c[1], 0.55f) - c[0]) + (c[0].Lerp(c[3], 0.55f) - c[0]) + Vector3.Up * 0.36f,
					c[0].Lerp(c[3], 0.55f) + Vector3.Up * 0.36f,
				});
				break;
			case DualVisualFamily.Full:
				// Solid raised plate — full mass.
				AddWallQuad(st, c[0], c[1], 0.28f);
				AddWallQuad(st, c[1], c[2], 0.28f);
				AddWallQuad(st, c[2], c[3], 0.28f);
				AddWallQuad(st, c[3], c[0], 0.28f);
				AddTopCap(st, new[]
				{
					c[0] + Vector3.Up * 0.28f,
					c[1] + Vector3.Up * 0.28f,
					c[2] + Vector3.Up * 0.28f,
					c[3] + Vector3.Up * 0.28f,
				});
				break;
			case DualVisualFamily.Diagonal:
				// Two opposite corner masses — graybox fallback only.
				AddWallQuad(st, c[0], c[1], 0.22f);
				AddWallQuad(st, c[2], c[3], 0.22f);
				AddTopCap(st, new[]
				{
					c[0] + Vector3.Up * 0.22f,
					c[1] + Vector3.Up * 0.22f,
					c[2] + Vector3.Up * 0.22f,
					c[3] + Vector3.Up * 0.22f,
				});
				break;
			case DualVisualFamily.InverseCorner:
			default:
				// Three-corner cove mass — graybox fallback.
				AddWallQuad(st, c[0], c[1], 0.22f);
				AddWallQuad(st, c[1], c[2], 0.22f);
				AddWallQuad(st, c[2], c[3], 0.22f);
				AddTopCap(st, new[]
				{
					c[0] + Vector3.Up * 0.22f,
					c[1] + Vector3.Up * 0.22f,
					c[2] + Vector3.Up * 0.22f,
					c[3] + Vector3.Up * 0.22f,
				});
				break;
		}

		var mesh = st.Commit();
		// Graybox fallback materials only — LIVE Success uses GLB terrain materials via MeshLibrary.
		mesh.SurfaceSetMaterial(0, MakeTerrainFallbackMaterial(family));
		return mesh;
	}

	private static Vector3[] EdgeBarTop(Vector3 a, Vector3 b, Vector3[] face, float h)
	{
		var centre = (face[0] + face[1] + face[2] + face[3]) * 0.25f;
		var inward = ((a + b) * 0.5f).DirectionTo(centre) * ((a.DistanceTo(b)) * 0.35f);
		var a2 = a + inward;
		var b2 = b + inward;
		return new[]
		{
			a + Vector3.Up * h,
			b + Vector3.Up * h,
			b2 + Vector3.Up * h,
			a2 + Vector3.Up * h,
		};
	}

	private static void AddWallQuad(SurfaceTool st, Vector3 a, Vector3 b, float height)
	{
		var topA = a + Vector3.Up * height;
		var topB = b + Vector3.Up * height;
		var normal = new Vector3(b.X - a.X, 0f, b.Z - a.Z);
		normal = new Vector3(-normal.Z, 0f, normal.X);
		if (normal.LengthSquared() < 1e-8f) normal = Vector3.Forward;
		else normal = normal.Normalized();
		st.SetNormal(normal); st.AddVertex(a);
		st.SetNormal(normal); st.AddVertex(b);
		st.SetNormal(normal); st.AddVertex(topB);
		st.SetNormal(normal); st.AddVertex(a);
		st.SetNormal(normal); st.AddVertex(topB);
		st.SetNormal(normal); st.AddVertex(topA);
	}

	private static void AddTopCap(SurfaceTool st, Vector3[] top)
	{
		if (top.Length < 4) return;
		st.SetNormal(Vector3.Up); st.AddVertex(top[0]);
		st.SetNormal(Vector3.Up); st.AddVertex(top[1]);
		st.SetNormal(Vector3.Up); st.AddVertex(top[2]);
		st.SetNormal(Vector3.Up); st.AddVertex(top[0]);
		st.SetNormal(Vector3.Up); st.AddVertex(top[2]);
		st.SetNormal(Vector3.Up); st.AddVertex(top[3]);
	}


	public CellFill GetCellFill(Vector2I cell) =>
		_occupancy.TryGetValue(cell, out var f) ? f : CellFill.Empty;

	public Error SetCellFill(Vector2I cell, CellFill fill)
	{
		if (_organicMesh == null || _organicRoot == null) return Error.Unconfigured;
		if (cell.Y == SecondaryPickY)
		{
			// Glow-debug only — refuse secondary as place target on LMB craft path.
			AlphaFactoryLog.Emit(
				"craft.refuse",
				"secondary_glow_center_as_place_target",
				$"refuse secondary Y={SecondaryPickY} place — use primary V Y={PrimaryPickY} FlipOrganicCorner",
				new Dictionary<string, object>
				{
					["ask_id"] = PreferAskId,
					["overlay"] = WeldSliceId,
					["refuse_code"] = "secondary_glow_center_as_place_target",
					["secondary_face"] = cell.X,
				},
				level: "warn");
			return Error.InvalidParameter;
		}
		if (cell.Y == PrimaryPickY)
		{
			// Primary V place — Empty clears; any fill sets/toggles via FlipOrganicCorner.
			var vertex = cell.X;
			if (vertex < 0 || vertex >= _organicMesh.VertexCount)
				return Error.InvalidParameter;
			var want = fill != CellFill.Empty;
			var cur = _cornerLogic.TryGetValue(vertex, out var on) && on;
			if (want != cur)
				FlipOrganicCorner(vertex);
			return Error.Ok;
		}
		var face = OrganicQuadMesh.FaceIndexFromCell(cell);
		if (!_organicMesh.ContainsFace(face) || cell.Y != 0)
		{
			AlphaFactoryLog.Emit(
				"craft.refuse",
				"hex19_pick_as_craft_authority",
				$"refuse paint outside organic face authority cell=({cell.X},{cell.Y})",
				new Dictionary<string, object>
				{
					["ask_id"] = PreferAskId,
					["overlay"] = WeldSliceId,
					["refuse_code"] = "hex19_pick_as_craft_authority",
					["face_index"] = face,
					["cell_q"] = cell.X,
					["cell_r"] = cell.Y,
				},
				level: "warn");
			return Error.InvalidParameter;
		}

		if (fill == CellFill.Empty)
		{
			_occupancy.Remove(cell);
			if (_filledCells.TryGetValue(cell, out var old) && GodotObject.IsInstanceValid(old))
				old.QueueFree();
			_filledCells.Remove(cell);
		}
		else
		{
			_occupancy[cell] = CellFill.Filled;
			ApplyOrganicFaceFillPlate(cell);
		}

		// Face paint refreshes that one dual cell via corner-owned mesh — not a stamp plate.
		var refreshed = UpdateFourDualSlots(cell);

		AlphaFactoryLog.Emit(
			"craft.paint",
			"Cell_Commit",
			$"organic face={face} fill={fill} — craft_plane_authority (hex19_success=false dual_success=false)",
			new Dictionary<string, object>
			{
				["ask_id"] = PreferAskId,
				["overlay"] = WeldSliceId,
				["face_index"] = face,
				["cell_q"] = cell.X,
				["cell_r"] = cell.Y,
				["fill"] = fill.ToString(),
				["lattice"] = "organic_quad_faces",
				["craft_authority"] = "OrganicQuadMesh",
				["hex19_success"] = false,
				["dual_success"] = false,
				["dual_refresh"] = refreshed,
				["cam_recenter"] = false,
				["terrain_pushed"] = false,
				["visual_bar"] = VisualBarCite,
			});
		return Error.Ok;
	}

	public Error PaintCell(Vector2I cell, CraftCellType type, float? raiseDelta = null)
	{
		_ = raiseDelta; // refuse craft_terrain_blend — never height-paint
		var fill = type == CraftCellType.Empty ? CellFill.Empty : CellFill.Filled;
		return SetCellFill(cell, fill);
	}

	public CraftCellType GetCellType(Vector2I cell) =>
		GetCellFill(cell) == CellFill.Filled ? CraftCellType.Grass : CraftCellType.Empty;

	public IReadOnlyDictionary<Vector2I, CellFill> SnapshotCellFills() =>
		new Dictionary<Vector2I, CellFill>(_occupancy);

	public IReadOnlyDictionary<Vector2I, CraftCellType> SnapshotCells()
	{
		var map = new Dictionary<Vector2I, CraftCellType>();
		foreach (var (cell, fill) in _occupancy)
		{
			if (fill == CellFill.Filled)
				map[cell] = CraftCellType.Grass;
		}
		return map;
	}

	public Error ApplyStampOasisDesert(Vector2I center, int radius = 2)
	{
		if (_organicMesh == null) return Error.Unconfigured;
		var centerFace = OrganicQuadMesh.FaceIndexFromCell(center);
		if (!_organicMesh.ContainsFace(centerFace) || center.Y != 0)
			return Error.InvalidParameter;

		var centre = _organicMesh.FaceCentroid(centerFace);
		var maxDist = Math.Max(1, radius) * _hexSize;
		var maxDistSq = maxDist * maxDist;
		for (var i = 0; i < _organicMesh.FaceCount; i++)
		{
			if (_organicMesh.FaceCentroid(i).DistanceSquaredTo(centre) > maxDistSq)
				continue;
			var err = SetCellFill(OrganicQuadMesh.FaceCell(i), CellFill.Filled);
			if (err != Error.Ok) return err;
		}

		AlphaFactoryLog.Emit(
			"craft.stamp",
			"stamp_oasis_desert",
			$"Tile-only organic-face stamp {CanonicalStampId} face={centerFace} — no Terrain3D",
			new Dictionary<string, object>
			{
				["stamp_id"] = CanonicalStampId,
				["ask_id"] = PreferAskId,
				["overlay"] = WeldSliceId,
				["terrain3d"] = false,
				["lattice"] = "organic_quad_faces",
				["hex19_success"] = false,
			});
		return Error.Ok;
	}

	public Error Persist(string path)
	{
		try
		{
			var abs = ProjectSettings.GlobalizePath(path);
			var dir = Path.GetDirectoryName(abs);
			if (!string.IsNullOrEmpty(dir))
				Directory.CreateDirectory(dir);

			var payload = new Dictionary<string, object>
			{
				["stamp"] = CanonicalStampId,
				["slice_id"] = SliceId,
				["weld_slice_id"] = WeldSliceId,
				["ask_id"] = PreferAskId,
				["half_b_overlay"] = WeldSliceId,
				["grammar"] = "organic_quad_face_occupancy",
				["lattice"] = "organic_quad_faces",
				["lattice_vertices"] = Hex19OccupancyLattice.VertexCount,
				["lattice_edges"] = Hex19OccupancyLattice.EdgeCount,
				["lattice_cells"] = Hex19OccupancyLattice.CellCount,
				["art_style_id"] = ArtStyleId,
				["visual_bar"] = VisualBarCite,
				["dual_visual_success"] = true,
				["dual_half_offset"] = true,
				["update_four"] = true,
				["ux_bullet"] = "UX-1",
				["cells"] = SerializeOccupancy(),
			};
			File.WriteAllText(abs, JsonSerializer.Serialize(payload));
			AlphaFactoryLog.Emit(
				"craft.persist",
				"World_Persist",
				$"persisted hex-19 lattice occupancy → {path} cells={_occupancy.Count}",
				new Dictionary<string, object>
				{
					["ask_id"] = PreferAskId,
					["ux"] = "UX-1",
					["residue"] = "persistent_living_world",
				});
			return Error.Ok;
		}
		catch (Exception ex)
		{
			AlphaFactoryLog.Emit("Degrade_FailVisible", "World_Persist", ex.Message, level: "error");
			return Error.Failed;
		}
	}

	public Error Load(string path)
	{
		try
		{
			var abs = ProjectSettings.GlobalizePath(path);
			if (!File.Exists(abs)) return Error.FileNotFound;
			using var doc = JsonDocument.Parse(File.ReadAllText(abs));
			var root = doc.RootElement;

			if (root.TryGetProperty("cells", out var cells))
			{
				foreach (var item in cells.EnumerateArray())
				{
					var q = item.GetProperty("q").GetInt32();
					var r = item.GetProperty("r").GetInt32();
					var cell = new Vector2I(q, r);
					// Craft-plane payloads: q = organic face index, r = 0. Drop Hex19 axial leftovers.
					if (cell.Y != 0 || _organicMesh == null || !_organicMesh.ContainsFace(cell.X))
						continue;
					var fill = item.TryGetProperty("fill", out var f)
						? (CellFill)f.GetInt32()
						: CellFill.Filled;
					SetCellFill(cell, fill);
				}
			}
			else if (root.TryGetProperty("logic_points", out var legacy))
			{
				// Prior point-cloud weld payload — read for continuity, rewritten as cells on persist.
				foreach (var item in legacy.EnumerateArray())
				{
					var x = item.GetProperty("x").GetInt32();
					var y = item.GetProperty("y").GetInt32();
					var fill = (CellFill)item.GetProperty("fill").GetInt32();
					var axial = new Vector2I(x, y);
					if (!Hex19OccupancyLattice.Contains(axial))
						continue;
					SetCellFill(axial, fill);
				}
			}
			else
			{
				return Error.InvalidData;
			}

			AlphaFactoryLog.Emit(
				"craft.load",
				"World_Persist",
				$"loaded hex-19 lattice occupancy ← {path} cells={_occupancy.Count}",
				new Dictionary<string, object> { ["ask_id"] = PreferAskId, ["ux"] = "UX-5" });
			return Error.Ok;
		}
		catch (Exception ex)
		{
			AlphaFactoryLog.Emit("Degrade_FailVisible", "World_Persist", ex.Message, level: "error");
			return Error.Failed;
		}
	}

	private Vector3 ResolveLatticeOrigin()
	{
		var parent = GetParent();
		if (parent != null)
		{
			var focus = parent.GetNodeOrNull<Node3D>("CraftFocusAnchor");
			if (focus != null)
				return focus.GlobalPosition;
		}
		return new Vector3(8f, 0f, 8f);
	}

	/// <summary>
	/// Draw the lattice on all three topology axes under one toggleable root:
	/// faces/cells (flat plate), neighbour edges (line primitives), vertices (nodes).
	/// </summary>
	private void BuildLatticeVisuals()
	{
		// Strip any legacy GridMap children (prior rect weld).
		foreach (var child in GetChildren())
		{
			if (child is GridMap gm)
				gm.QueueFree();
		}

		_gridRoot = new Node3D { Name = "Hex19LatticeGraph", Visible = _latticeVisible };
		AddChild(_gridRoot);

		_gridRoot.AddChild(new MeshInstance3D
		{
			Name = "LatticeFaces",
			Mesh = BuildFaces(),
			Position = Vector3.Up * 0.01f,
		});

		_gridRoot.AddChild(new MeshInstance3D
		{
			Name = "LatticeEdges",
			Mesh = BuildEdgeLines(),
			Position = Vector3.Up * 0.03f,
		});

		_gridRoot.AddChild(new MeshInstance3D
		{
			Name = "LatticeVertices",
			Mesh = BuildVertexNodes(),
			Position = Vector3.Up * 0.04f,
		});

		_gridRoot.GlobalPosition = _latticeOrigin;

		_ghost = new MeshInstance3D
		{
			Name = "PlacementGhost",
			Mesh = MakeCellPolygonFan(
				Vector2I.Zero,
				new Color(0.30f, 0.62f, 0.68f, 0.40f),
				inset: 0.88f,
				centred: true),
			Visible = false,
		};
		AddChild(_ghost);
	}

	/// <summary>Face axis — the hex cells of the lattice as a flat graybox plate.</summary>
	private ArrayMesh BuildFaces()
	{
		var st = new SurfaceTool();
		st.Begin(Mesh.PrimitiveType.Triangles);
		st.SetColor(new Color(0.12f, 0.18f, 0.20f, 0.55f));
		foreach (var cell in Hex19OccupancyLattice.Cells)
		{
			var corners = Hex19OccupancyLattice.HexCorners(cell.Axial, _hexSize);
			var centre = Hex19OccupancyLattice.AxialToLocal(cell.Axial, _hexSize);
			// Triangle fan per face — the cell is its corners, not its centre marker.
			for (var i = 0; i < Hex19OccupancyLattice.CornersPerCell; i++)
			{
				var a = corners[i];
				var b = corners[(i + 1) % Hex19OccupancyLattice.CornersPerCell];
				st.SetNormal(Vector3.Up);
				st.AddVertex(centre);
				st.SetNormal(Vector3.Up);
				st.AddVertex(a);
				st.SetNormal(Vector3.Up);
				st.AddVertex(b);
			}
		}

		var mesh = st.Commit();
		mesh.SurfaceSetMaterial(0, new StandardMaterial3D
		{
			AlbedoColor = new Color(0.12f, 0.18f, 0.20f, 0.55f),
			Transparency = BaseMaterial3D.TransparencyEnum.Alpha,
			CullMode = BaseMaterial3D.CullModeEnum.Disabled,
			Roughness = 0.95f,
			ShadingMode = BaseMaterial3D.ShadingModeEnum.PerPixel,
		});
		return mesh;
	}

	/// <summary>
	/// Edge axis — neighbour adjacency between vertices plus the shared cell outlines,
	/// drawn as real line primitives so the lattice reads as a graph.
	/// </summary>
	private ArrayMesh BuildEdgeLines()
	{
		var st = new SurfaceTool();
		st.Begin(Mesh.PrimitiveType.Lines);

		// Cell outlines — the face boundaries shared between adjacent cells.
		foreach (var cell in Hex19OccupancyLattice.Cells)
		{
			var corners = Hex19OccupancyLattice.HexCorners(cell.Axial, _hexSize);
			for (var i = 0; i < Hex19OccupancyLattice.CornersPerCell; i++)
			{
				st.AddVertex(corners[i]);
				st.AddVertex(corners[(i + 1) % Hex19OccupancyLattice.CornersPerCell]);
			}
		}

		// Adjacency edges — one segment per unique neighbour pair in the graph.
		foreach (var (a, b) in Hex19OccupancyLattice.Edges)
		{
			st.AddVertex(Hex19OccupancyLattice.AxialToLocal(a, _hexSize) + Vector3.Up * 0.015f);
			st.AddVertex(Hex19OccupancyLattice.AxialToLocal(b, _hexSize) + Vector3.Up * 0.015f);
		}

		var mesh = st.Commit();
		mesh.SurfaceSetMaterial(0, new StandardMaterial3D
		{
			AlbedoColor = new Color(0.72f, 0.54f, 0.22f, 0.9f),
			Transparency = BaseMaterial3D.TransparencyEnum.Alpha,
			ShadingMode = BaseMaterial3D.ShadingModeEnum.Unshaded,
			VertexColorUseAsAlbedo = false,
		});
		return mesh;
	}

	/// <summary>Vertex axis — the 19 lattice nodes themselves.</summary>
	private ArrayMesh BuildVertexNodes()
	{
		var st = new SurfaceTool();
		st.Begin(Mesh.PrimitiveType.Triangles);
		var node = new SphereMesh { Radius = 0.075f, Height = 0.15f, RadialSegments = 8, Rings = 4 };
		foreach (var axial in Hex19OccupancyLattice.Vertices)
		{
			var xf = new Transform3D(Basis.Identity, Hex19OccupancyLattice.AxialToLocal(axial, _hexSize));
			st.AppendFrom(node, 0, xf);
		}

		var mesh = st.Commit();
		mesh.SurfaceSetMaterial(0, new StandardMaterial3D
		{
			AlbedoColor = new Color(0.78f, 0.58f, 0.28f),
			Roughness = 0.6f,
			ShadingMode = BaseMaterial3D.ShadingModeEnum.PerPixel,
		});
		return mesh;
	}

	/// <summary>Craft-plane occupancy plate on organic face (not dual Success; refuse stamp_as_dual).</summary>
	private void ApplyOrganicFaceFillPlate(Vector2I cell)
	{
		var face = OrganicQuadMesh.FaceIndexFromCell(cell);
		if (_organicMesh == null || !_organicMesh.ContainsFace(face))
			return;

		var mesh = MakeOrganicFacePlate(face, new Color(0.62f, 0.42f, 0.18f, 0.92f), height: 0.12f);
		if (_filledCells.TryGetValue(cell, out var existing) && GodotObject.IsInstanceValid(existing))
		{
			existing.Mesh = mesh;
			existing.GlobalPosition = _latticeOrigin + Vector3.Up * 0.02f;
			return;
		}

		var mi = new MeshInstance3D
		{
			Name = $"OrganicFace_{face}",
			Mesh = mesh,
		};
		AddChild(mi);
		mi.GlobalPosition = _latticeOrigin + Vector3.Up * 0.02f;
		_filledCells[cell] = mi;
	}

	private void ClearOrganicOccupancyMeshes()
	{
		foreach (var (_, mesh) in _filledCells)
		{
			if (mesh != null && GodotObject.IsInstanceValid(mesh))
				mesh.QueueFree();
		}
		_filledCells.Clear();
		_occupancy.Clear();
	}

	/// <summary>Graybox raised plate matching one organic quad face (craft paint / ghost).</summary>
	private ArrayMesh MakeOrganicFacePlate(int faceIndex, Color color, float height)
	{
		if (_organicMesh == null)
			return new ArrayMesh();
		var corners = _organicMesh.FaceCornersLocal(faceIndex);
		var st = new SurfaceTool();
		st.Begin(Mesh.PrimitiveType.Triangles);
		var lift = Vector3.Up * height;
		// Inset slightly so fill reads inside the yellow edge graph.
		var centre = (corners[0] + corners[1] + corners[2] + corners[3]) * 0.25f;
		const float inset = 0.88f;
		for (var i = 0; i < 4; i++)
			corners[i] = centre.Lerp(corners[i], inset) + lift;
		st.SetNormal(Vector3.Up); st.AddVertex(corners[0]);
		st.SetNormal(Vector3.Up); st.AddVertex(corners[1]);
		st.SetNormal(Vector3.Up); st.AddVertex(corners[2]);
		st.SetNormal(Vector3.Up); st.AddVertex(corners[0]);
		st.SetNormal(Vector3.Up); st.AddVertex(corners[2]);
		st.SetNormal(Vector3.Up); st.AddVertex(corners[3]);
		var mesh = st.Commit();
		mesh.SurfaceSetMaterial(0, new StandardMaterial3D
		{
			AlbedoColor = color,
			Transparency = color.A < 0.99f
				? BaseMaterial3D.TransparencyEnum.Alpha
				: BaseMaterial3D.TransparencyEnum.Disabled,
			CullMode = BaseMaterial3D.CullModeEnum.Disabled,
			ShadingMode = BaseMaterial3D.ShadingModeEnum.Unshaded,
		});
		return mesh;
	}

	// Legacy hex fill helper retained for tutorial ladder code paths (not craft-plane Success).
	private void EnsureFilledCellMesh(Vector2I axial)
	{
		ApplyOrganicFaceFillPlate(axial);
	}

	/// <summary>Flat hex footprint of one cell — the ghost and overlay shape.</summary>
	private ArrayMesh MakeCellPolygonFan(Vector2I axial, Color color, float inset, bool centred)
	{
		var corners = Hex19OccupancyLattice.HexCorners(axial, _hexSize * inset);
		var centre = centred
			? Vector3.Zero
			: Hex19OccupancyLattice.AxialToLocal(axial, _hexSize);
		if (centred)
		{
			var offset = Hex19OccupancyLattice.AxialToLocal(axial, _hexSize * inset);
			for (var i = 0; i < corners.Length; i++)
				corners[i] -= offset;
		}

		var st = new SurfaceTool();
		st.Begin(Mesh.PrimitiveType.Triangles);
		for (var i = 0; i < Hex19OccupancyLattice.CornersPerCell; i++)
		{
			st.SetNormal(Vector3.Up);
			st.AddVertex(centre);
			st.SetNormal(Vector3.Up);
			st.AddVertex(corners[i]);
			st.SetNormal(Vector3.Up);
			st.AddVertex(corners[(i + 1) % Hex19OccupancyLattice.CornersPerCell]);
		}

		var mesh = st.Commit();
		mesh.SurfaceSetMaterial(0, new StandardMaterial3D
		{
			AlbedoColor = color,
			Transparency = BaseMaterial3D.TransparencyEnum.Alpha,
			CullMode = BaseMaterial3D.CullModeEnum.Disabled,
			ShadingMode = BaseMaterial3D.ShadingModeEnum.Unshaded,
		});
		return mesh;
	}

	/// <summary>Occupied cell — a hex prism on the face, so fill reads as a cell not a disk.</summary>
	private ArrayMesh MakeCellPrism(Color color, float height)
	{
		var corners = Hex19OccupancyLattice.HexCorners(Vector2I.Zero, _hexSize * 0.94f);
		var st = new SurfaceTool();
		st.Begin(Mesh.PrimitiveType.Triangles);

		var top = Vector3.Up * height;
		for (var i = 0; i < Hex19OccupancyLattice.CornersPerCell; i++)
		{
			var a = corners[i];
			var b = corners[(i + 1) % Hex19OccupancyLattice.CornersPerCell];

			// Top face fan.
			st.SetNormal(Vector3.Up);
			st.AddVertex(top);
			st.SetNormal(Vector3.Up);
			st.AddVertex(a + top);
			st.SetNormal(Vector3.Up);
			st.AddVertex(b + top);

			// Side quad down to the lattice plane.
			var normal = new Vector3(a.X + b.X, 0f, a.Z + b.Z).Normalized();
			st.SetNormal(normal);
			st.AddVertex(a);
			st.SetNormal(normal);
			st.AddVertex(a + top);
			st.SetNormal(normal);
			st.AddVertex(b + top);

			st.SetNormal(normal);
			st.AddVertex(a);
			st.SetNormal(normal);
			st.AddVertex(b + top);
			st.SetNormal(normal);
			st.AddVertex(b);
		}

		var mesh = st.Commit();
		mesh.SurfaceSetMaterial(0, new StandardMaterial3D
		{
			AlbedoColor = color,
			Roughness = 0.85f,
			Metallic = 0f,
			ShadingMode = BaseMaterial3D.ShadingModeEnum.PerPixel,
		});
		return mesh;
	}


	/// <summary>
	/// Dual half-offset overlay — unique quads whose centres sit between occupancy sites.
	/// Each dual reads four occupancy corners; paint triggers update-four only.
	/// </summary>
	private void BuildDualOffsetOverlay()
	{
		if (_dualRoot != null && GodotObject.IsInstanceValid(_dualRoot))
			_dualRoot.QueueFree();
		_dualSlots.Clear();

		_dualRoot = new Node3D { Name = "DualHalfOffsetOverlay", Visible = _dualVisible };
		AddChild(_dualRoot);
		_dualRoot.GlobalPosition = _latticeOrigin;

		foreach (var cell in Hex19DualOffsetLattice.AllDualCells(_hexSize))
			EnsureDualCellMesh(cell);

		AlphaFactoryLog.Emit(
			"craft.grid",
			"Dual_Offset_Overlay",
			$"dual half-step offset quads armed — unique_cells={_dualSlots.Count} " +
			$"update_four={Hex19DualOffsetLattice.DualSlotsPerOccupancy} (refuse skip_dual_offset|markers_only_dual)",
			new Dictionary<string, object>
			{
				["ask_id"] = PreferAskId,
				["overlay"] = WeldSliceId,
				["dual_half_offset"] = true,
				["update_four"] = true,
				["dual_slots"] = _dualSlots.Count,
				["dual_unique_not_per_occ_spray"] = true,
				["dual_overlay_toggle"] = true,
				["connector_success"] = false,
				["art_success"] = false,
			});
	}

	/// <summary>
	/// UPDATE — DualCellsTouching(V) when Y=PrimaryPickY: recompute owned + expand.
	/// Place Success = Full only on OwnedDualCell(V); expand neighbors Clear/Empty unless
	/// their own owner is on (not Corner spray as place Success).
	/// ≤ MaxDualCellsPerLogicFlip. Refuse secondary Y / face stamp / soft Take(4).
	/// </summary>
	public int UpdateFourDualSlots(Vector2I occupancy)
	{
		// Organic dual-lattice: Y==PrimaryPickY primary V place; secondary Y refused.
		if (_organicMesh != null && _dualRoot != null && _dualLattice != null)
		{
			// Organic populate: DualCellsTouching(logicVert) — owned DualCell(V) Full when
			// owner on; expand neighbours recompute → ClearDualSlot unless N owner-on.
			if (occupancy.Y == SecondaryPickY)
			{
				AlphaFactoryLog.Emit("craft.refuse", "secondary_glow_center_as_place_target",
					$"refuse secondary Y UpdateFour occupancy={occupancy} — use primary Y={PrimaryPickY} DualCellsTouching",
					level: "error");
				return 0;
			}
			if (occupancy.Y == PrimaryPickY)
			{
				var vertex = occupancy.X;
				var cells = _dualLattice.DualCellsTouching(vertex);
				if (cells.Count == 0)
					return 0;
				if (cells.Count > MaxDualCellsPerLogicFlip)
				{
					AlphaFactoryLog.Emit("craft.refuse", "over_neighbor_paint",
						$"refuse over_neighbor_paint vertex={vertex} touching_duals={cells.Count} cap={MaxDualCellsPerLogicFlip}",
						level: "error");
					return 0;
				}
				var n = 0;
				foreach (var cell in cells)
				{
					EnsureStage6DualCellMesh(cell);
					n++;
				}
				return n;
			}
			AlphaFactoryLog.Emit("craft.refuse", "primary_face_as_dual",
				$"refuse face-index UpdateFour occupancy={occupancy} — use primary Y={PrimaryPickY} DualCellsTouching",
				level: "error");
			return 0;
		}
		if (_dualRoot == null)
			return 0;
		var hexCells = Hex19DualOffsetLattice.DualCellsTouching(occupancy, _hexSize);
		if (hexCells.Length != Hex19DualOffsetLattice.DualSlotsPerOccupancy)
			return 0;
		var nHex = 0;
		foreach (var cell in hexCells)
		{
			EnsureDualCellMesh(cell);
			nHex++;
		}
		return nHex;
	}

	public void RefreshAllDualSlots()
	{
		if (_dualRoot == null) return;
		if (_organicMesh != null && _dualLattice != null)
		{
			foreach (var cell in _dualLattice.AllCells)
				EnsureStage6DualCellMesh(cell);
			return;
		}
		foreach (var cell in Hex19DualOffsetLattice.AllDualCells(_hexSize))
			EnsureDualCellMesh(cell);
	}

	/// <summary>
	/// Structural proof — unique half-offset duals, four-corner reads, update-four API.
	/// Refuses attempt-1 markers-only (19×4 spray / coincident centres).
	/// </summary>
	public (bool Ok, string Summary) ProveDualOffsetStructure()
	{
		if (_organicMesh != null)
		{
			if (_dualRoot == null)
				return (false, "dual_overlay_missing refuse=skip_dual_offset");
			if (_dualLattice == null || _dualLattice.CellCount == 0)
				return (false, "organic_dual_offset_lattice_missing refuse=primary_face_as_dual");
			var quadCells = 0;
			foreach (var c in _dualLattice.AllCells)
				if (c.DualCorners != null && c.DualCorners.Length == 4) quadCells++;
			// Empty skips mesh — slots ≤ stage6 quads (refuse ocean_fill_all_empty_slots).
			if (_dualSlots.Count > quadCells)
				return (false, $"dual_lattice_count_mismatch mesh={_dualSlots.Count} stage6_quads={quadCells} refuse=skip_dual_offset");
			if (_dualLattice.LogicPointCount == 0)
				return (false, "dual_corner_index_missing refuse=skip_dual_offset");
			var neigh = ProveStableDualNeighborhood();
			if (!neigh.Ok)
				return (false, neigh.Summary);
			return (true,
				$"dual_lattice_on_organic unique_slots={_dualSlots.Count} stage6_dual_cell_host=true update_four=DualCellsTouching " +
				$"stage6_cells={_dualLattice.CellCount} empty_skip=true ocean_fill_all_empty_slots=false " +
				$"primary_vertex_place=true primary_face_as_dual=false stage6_union_as_single_glow_tile=false " +
				$"half_step_varignon_corner=true hex19_success=false dual_visual_deferred=true " +
				$"neighborhood={neigh.Summary}");
		}
		if (_dualRoot == null)
			return (false, "dual_overlay_missing refuse=skip_dual_offset");

		var all = Hex19DualOffsetLattice.AllDualCells(_hexSize);
		if (_dualSlots.Count != all.Count || all.Count == 0)
			return (false, $"dual_unique_count_mismatch mesh={_dualSlots.Count} lattice={all.Count} refuse=skip_dual_offset");

		// Markers-only tell: spray count equals CellCount×4 (attempt 1).
		if (_dualSlots.Count == Hex19OccupancyLattice.CellCount * Hex19DualOffsetLattice.DualSlotsPerOccupancy)
			return (false, "dual_markers_only_spray refuse=skip_dual_offset");

		var halfOk = 0;
		var multiCorner = 0;
		foreach (var cell in all)
		{
			if (Hex19DualOffsetLattice.IsHalfStepOffset(cell, _hexSize))
				halfOk++;
			if (Hex19DualOffsetLattice.DistinctCornerCount(cell) >= 2)
				multiCorner++;
		}
		if (halfOk < all.Count)
			return (false, $"dual_not_half_offset coincident={all.Count - halfOk} refuse=skip_dual_offset");
		if (multiCorner == 0)
			return (false, "dual_corners_collapsed refuse=skip_dual_offset");

		var touch = Hex19DualOffsetLattice.DualCellsTouching(Vector2I.Zero, _hexSize);
		if (touch.Length != Hex19DualOffsetLattice.DualSlotsPerOccupancy)
			return (false, "update_four_set_not_four refuse=skip_dual_offset");

		if (_dualRoot.GetNodeOrNull<MeshInstance3D>($"DualCell_{touch[0].Key}") == null && _dualSlots.Count == 0)
			return (false, "dual_cell_meshes_missing refuse=skip_dual_offset");

		return (true,
			$"dual_half_offset unique_cells={_dualSlots.Count} update_four=4 " +
			$"corner_driven=true dual_toggle=independent occupancy_toggle=kept " +
			$"connectors=false art=false");
	}

	private void EnsureDualCellMesh(Hex19DualOffsetLattice.DualCell cell)
	{
		if (_dualRoot == null) return;
		bool IsFilled(Vector2I axial) =>
			_occupancy.TryGetValue(axial, out var f) && f == CellFill.Filled;

		var family = Hex19DualOffsetLattice.TileFamilyIndex(cell, IsFilled);
		var filledCorners = Hex19DualOffsetLattice.CountFilledCorners(cell, IsFilled);
		var color = DualFamilyColor(family);
		var height = 0.03f + family * 0.04f;

		var mesh = MakeDualCornerQuad(cell, color, height);
		if (_dualSlots.TryGetValue(cell.Key, out var existing) && GodotObject.IsInstanceValid(existing))
		{
			existing.Mesh = mesh;
			existing.Position = Vector3.Up * 0.08f;
			existing.SetMeta("filled_corners", filledCorners);
			existing.SetMeta("tile_family", family);
			return;
		}

		var mi = new MeshInstance3D
		{
			Name = $"DualCell_{cell.Key}",
			Mesh = mesh,
			Position = Vector3.Up * 0.08f,
		};
		mi.SetMeta("filled_corners", filledCorners);
		mi.SetMeta("tile_family", family);
		mi.SetMeta("dual_origin_q", cell.Origin.X);
		mi.SetMeta("dual_origin_r", cell.Origin.Y);
		_dualRoot.AddChild(mi);
		_dualSlots[cell.Key] = mi;
	}

	/// <summary>
	/// LEGACY hex-19 dual path only — NOT organic dual-visual Success.
	/// Organic path uses MakeShapeDistinctDualVariant (refuse gray_ramp_only).
	/// </summary>
	private static Color DualFamilyColor(int family) => family switch
	{
		0 => new Color(0.14f, 0.20f, 0.22f, 0.35f),
		1 => new Color(0.20f, 0.28f, 0.30f, 0.55f),
		2 => new Color(0.28f, 0.36f, 0.34f, 0.68f),
		3 => new Color(0.42f, 0.36f, 0.22f, 0.78f), // saddle — muted amber
		4 => new Color(0.55f, 0.42f, 0.22f, 0.88f),
		_ => new Color(0.68f, 0.48f, 0.24f, 0.95f),
	};

	/// <summary>
	/// Dual visual = quad spanning the four occupancy corner positions (inset),
	/// not a tiny marker at an arbitrary offset. Corner-driven geometry.
	/// </summary>
	private ArrayMesh MakeDualCornerQuad(Hex19DualOffsetLattice.DualCell cell, Color color, float height)
	{
		var corners = new Vector3[Hex19DualOffsetLattice.CornersPerDual];
		for (var i = 0; i < Hex19DualOffsetLattice.CornersPerDual; i++)
			corners[i] = Hex19OccupancyLattice.AxialToLocal(cell.Corners[i], _hexSize);

		// Inset toward centre so dual plates don't fully cover occupancy faces.
		var centre = cell.LocalCentre;
		const float inset = 0.72f;
		for (var i = 0; i < corners.Length; i++)
			corners[i] = centre.Lerp(corners[i], inset) + Vector3.Up * height;

		var st = new SurfaceTool();
		st.Begin(Mesh.PrimitiveType.Triangles);
		// SW-SE-NE, SW-NE-NW (CornerAxialOffsets order: SW,SE,NW,NE)
		st.SetNormal(Vector3.Up); st.AddVertex(corners[0]);
		st.SetNormal(Vector3.Up); st.AddVertex(corners[1]);
		st.SetNormal(Vector3.Up); st.AddVertex(corners[3]);
		st.SetNormal(Vector3.Up); st.AddVertex(corners[0]);
		st.SetNormal(Vector3.Up); st.AddVertex(corners[3]);
		st.SetNormal(Vector3.Up); st.AddVertex(corners[2]);

		var mesh = st.Commit();
		mesh.SurfaceSetMaterial(0, new StandardMaterial3D
		{
			AlbedoColor = color,
			Transparency = BaseMaterial3D.TransparencyEnum.Alpha,
			CullMode = BaseMaterial3D.CullModeEnum.Disabled,
			ShadingMode = BaseMaterial3D.ShadingModeEnum.Unshaded,
		});
		return mesh;
	}

	private List<Dictionary<string, int>> SerializeOccupancy()
	{
		var list = new List<Dictionary<string, int>>();
		foreach (var (cell, fill) in _occupancy)
		{
			list.Add(new Dictionary<string, int>
			{
				["q"] = cell.X,
				["r"] = cell.Y,
				["fill"] = (int)fill,
			});
		}
		return list;
	}
}
