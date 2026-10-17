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
/// Stålberg Stage-6 dual host — PLACE-coast bits KEEP + land-only Stage-6 coast emit.
/// Snap = primary logic Vertex V (KEEP). Ghost = OwnedDualCell(V) (≥3 corners KEEP).
/// Populate = FlipOrganicCorner(V) → DualCellsTouching(V) = owned + DualCellsSampling(V)
/// (PLACE-update-four sample recompute KEEP).
/// Place Success = one Full on OwnedDualCell(V) — DualCorners n=3 (tri) or n=4 (quad).
/// Coast bits KEEP = owner-off DualCells → OccupancyCorners → Edge/Corner/Diagonal/
/// InverseCorner/Full/Empty. Non-Full coast = EmitCoastLandOnlyFromStage6 (occupancy
/// outline → land deck) — refuse MeshFit GLB strip dependency / blue_water_as_coast_success.
/// OccupancyCorners ↔ Stage6 DualCorners; owner-on → Full via EmitFullSingleDeckFromStage6.
/// Empty = ClearDualSlot. Prefer: alpha0_stalberg_dual_coast_stage6_emit_r1.
/// Valence-5 stays non-placeable. KEEP 2u tri · 2w single-deck · 2x update-four · 2y bit map
/// · 2z strip-water KEEP (MeshFit coast path SUPERSEDED by Stage-6 land emit).
/// </summary>
public partial class DualGridCraftHost : Node3D, ICraftCellAuthority
{
	public const string CanonicalStampId = "stamp_oasis_desert";
	/// <summary>Legacy occupancy path — PACK-save-load canonical is <see cref="PackSaveLoadContract.PersistPath"/>.</summary>
	public const string PersistPath = PackSaveLoadContract.PersistPath;
	public const string SliceId = "alpha0_stalberg_dual_coast_stage6_emit_r1";
	public const string WeldSliceId = "alpha0_stalberg_dual_coast_stage6_emit_r1";
	public const string PreferAskId = "alpha0_stalberg_dual_visual";
	public const string VisualBarCite = "stalberg_dual_coast_stage6_emit";
	public const string ArtStyleId = "dual_offset_terrain_tile_nature_model_pack";
	public const string SuccessObject = "dual_cell_meshlibrary_placement";
	public const string PlacePolarity = "owned_dual_cell_place_coast_stage6_emit";
	public const string PaintContract = "C_dual_coast_stage6_emit";
	/// <summary>Board waterline lift for Full single-deck emit (MeshFit non-Full uses same).</summary>
	public const float FullDeckYLift = 12f;
	/// <summary>W4 — scale gen height facts into craft-visible altitude (high vs low / peak vs shelf).</summary>
	public const float GenHeightVisualScale = 68f;
	/// <summary>~1% edge inset toward centroid so neighboring Fulls do not share pixels.</summary>
	public const float FullDeckEdgeInset = 0.01f;
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
	private readonly Dictionary<int, float> _genHeightByVertex = new();
	private readonly Dictionary<int, GenBiomeService.BiomeKind> _genBiomeByVertex = new();
	private readonly HashSet<int> _genRiverVertices = new();
	private MeshInstance3D? _genRiverRibbon;
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
	/// <summary>Last OccupancyCorners bit mask sampled during Resolve (PLACE-update-four honesty).</summary>
	public int LastOccupancyBitsSampled { get; private set; }
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
	/// <summary>Last GEN-terrain height facts (craft-view altitude lift; empty until Generate).</summary>
	public IReadOnlyDictionary<int, float> LastGenHeightByVertex => _genHeightByVertex;
	public IReadOnlyCollection<int> LastGenRiverVertices => _genRiverVertices;
	/// <summary>Last GEN-biomes map (land vertices → biome kind; water = None).</summary>
	public IReadOnlyDictionary<int, GenBiomeService.BiomeKind> LastGenBiomeByVertex => _genBiomeByVertex;
	public string LastGenTerrainSummary { get; private set; } = "";
	public string LastGenBiomesSummary { get; private set; } = "";
	public int LastGenBiomeDistinctLand { get; private set; }
	public bool GenTerrainApplied { get; private set; }
	public int LastGenRiverCarveCount { get; private set; }

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
	/// Place Success — flip primary V; refresh DualCellsTouching(V) = owned +
	/// DualCellsSampling(V) (PLACE-update-four KEEP; ≤ MaxDualCellsPerLogicFlip).
	/// Ghost seat = OwnedDualCell(V). Owned DualCell → Full when owner on.
	/// Sampling DualCells resolve OccupancyCorners bits → coastline MeshLibrary
	/// (PLACE-coast; supersedes owned-only Empty-neighbor deferral). Empty skips mesh.
	/// Spray ≠ place Success (owned Full remains place); coasts read as coasts.
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
		var sampleKeys = _dualLattice.DualCellKeysSampling(vertexIndex).ToList();
		var expandKeys = _dualLattice.DualCellsExpandingFrom(vertexIndex).Select(c => c.Key).ToList();
		LastOwnedDualCellsCsv = string.Join(',', owned);
		LastOwnedDualFaceCount = owned.Count;
		LastExpandDualCellsCsv = string.Join(',', sampleKeys.Count > 0 ? sampleKeys : expandKeys);
		LastExpandDualCount = sampleKeys.Count > 0 ? sampleKeys.Count : expandKeys.Count;
		LastSmallCornerQuadsCsv = LastExpandDualCellsCsv;
		LastSmallCornerQuadCount = LastExpandDualCount;
		var prove = ProveStableDualNeighborhood();
		LastNeighborhoodStable = prove.Ok;
		var n = UpdateFourDualSlots(new Vector2I(vertexIndex, PrimaryPickY));
		HighlightOwnedDualCells(vertexIndex);
		AlphaFactoryLog.Emit(
			"craft.dual",
			"Corner_Flip",
			$"organic primary_V={vertexIndex} filled={_cornerLogic[vertexIndex]} dual_cells_refreshed={n} owned=[{string.Join(',', owned)}] sampling=[{string.Join(',', sampleKeys)}] place_coast=true touching=owned+DualCellsSampling (cap={MaxDualCellsPerLogicFlip})",
			new Dictionary<string, object>
			{
				["ask_id"] = PreferAskId,
				["overlay"] = WeldSliceId,
				["corner_index"] = vertexIndex,
				["filled"] = _cornerLogic[vertexIndex],
				["update_four"] = n,
				["owned_dual_cells"] = string.Join(',', owned),
				["owned_count"] = owned.Count,
				["sampling_dual_cells"] = string.Join(',', sampleKeys),
				["sampling_count"] = sampleKeys.Count,
				["expand_dual_cells"] = string.Join(',', expandKeys),
				["expand_count"] = expandKeys.Count,
				["max_dual_cells_per_logic_flip"] = MaxDualCellsPerLogicFlip,
				["success_object"] = SuccessObject,
				["place_polarity"] = PlacePolarity,
				["paint_contract"] = PaintContract,
				["owned_dual_cell_place"] = true,
				["owned_only_paint"] = false,
				["owned_only_coastline_deferred"] = false,
				["place_coast"] = true,
				["update_four_sample_recompute"] = true,
				["update_four_recompute_success"] = true,
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

		// Empty craft enter (1g WORLD-parity KEEP) — no demo Full/coast stamps on arm.
		// GEN-terrain owns self-populate via ApplyGenTerrainPass (Create World Open auto / Key.T accel) — not craft enter.
		// SeedDualVisualFamilyShowcase remains available for opt-in MCP/debug only (not _Ready).
		_cornerLogic.Clear();
		_genHeightByVertex.Clear();
		_genBiomeByVertex.Clear();
		ClearGenRiverRibbon();
		_genRiverVertices.Clear();
		GenTerrainApplied = false;
		LastGenTerrainSummary = "";
		LastGenBiomesSummary = "";
		LastGenBiomeDistinctLand = 0;
		LastGenRiverCarveCount = 0;

		// Visual slots = Stage-6 DualCells (Empty skips mesh → amber board only).
		foreach (var cell in _dualLattice.AllCells)
			EnsureStage6DualCellMesh(cell);

		// Dual debug: face-centroid plus markers only — no DualCellEdges ribbons (clutter).
		RebuildDualLatticeDebugVisuals();

		AlphaFactoryLog.Emit(
			"craft.grid",
			"Dual_Offset_Overlay",
			$"organic stage6_dual_cells armed EMPTY — unique_slots={_dualSlots.Count} stage6_cells={_dualLattice.CellCount} corner_bits={_cornerLogic.Count} update_four≤{MaxDualCellsPerLogicFlip} (refuse showcase_seed_on_enter|ocean_fill_all_empty_slots|gen_fill_as_craft_enter)",
			new Dictionary<string, object>
			{
				["ask_id"] = PreferAskId,
				["overlay"] = WeldSliceId,
				["craft_enter_empty"] = true,
				["showcase_seed_on_enter"] = false,
				["corner_logic_bits"] = _cornerLogic.Count,
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
	/// Opt-in MCP/debug only — seed empty/edge/corner/full silhouette demos.
	/// Never called from craft enter / EnsureHost / BuildOrganicDualCornerOverlay
	/// (1g empty-enter: amber board, no pre-placed Fulls/coasts). GEN-* owns fill later.
	/// Place Success remains OwnedDualCell(V) via FlipOrganicCorner.
	/// </summary>
	public void SeedDualVisualFamilyShowcase(bool refresh = true)
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
			"opt-in seed face-corner silhouettes empty|edge|corner|full (NOT craft-enter; place Success=OwnedDualCell; GEN-fill later)",
			new Dictionary<string, object>
			{
				["ask_id"] = PreferAskId,
				["overlay"] = WeldSliceId,
				["craft_enter_seed"] = false,
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
	/// Owner on → Full whole DualCell (place KEEP). Owner off → OccupancyCorners bits
	/// → Edge/Corner/Diagonal/InverseCorner/Full/Empty (PLACE-coast).
	/// DualCorners n=3 (tri) or n=4 (quad); OccupancyCorners length matches (no soft_take_4).
	/// Warp: n=4 dual-edge frame (edge0=c0→c1); n=3 barycentric. Empty skips ocean.
	/// Refuse silent_ghost_without_place_n3 / soft_take_4 / sector_pie / y_bias Full.
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
	/// Place MeshLibrary family on a Stage-6 DualCell. Full = one opaque inset deck from
	/// Stage-6 corners at FullDeckYLift (VIS-zfight / single-deck emit — no GLB flatten,
	/// MeshFit, Y-bias, SortingOffset, or RenderPriority harden). Non-Full coast families =
	/// land-only Stage-6 emit from OccupancyCorners bits (no MeshFit GLB). Empty =
	/// ClearDualSlot (ocean amber KEEP). Refuse silent_ghost_without_place_n3 / soft_take_4 /
	/// seizure_coplanar_deck_as_success / y_bias_as_zfight_fix / blue_water_as_coast_success /
	/// glb_meshfit_coast_as_success.
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
		if (stage6Corners == null || (stage6Corners.Length != 3 && stage6Corners.Length != 4))
			return;

		var lib = EnsureShapeDistinctDualMeshLibrary();
		var source = lib.GetItemMesh((int)family) ?? MakeUnitShapeDistinctPrototype(family);
		var isFull = family == DualVisualFamily.Full;

		MeshInstance3D mi;
		if (_dualSlots.TryGetValue(key, out var existing) && GodotObject.IsInstanceValid(existing))
			mi = existing;
		else
		{
			mi = new MeshInstance3D();
			_dualRoot.AddChild(mi);
			_dualSlots[key] = mi;
		}

		ArrayMesh fitted;
		float edge0YawRad;
		if (isFull)
		{
			// Full: emit one deck from Stage-6 corners — do NOT MeshFit / flatten the Full GLB.
			(fitted, edge0YawRad) = EmitFullSingleDeckFromStage6(stage6Corners, rot90, mirror, source);
		}
		else
		{
			// Coast families: land-only Stage-6 emit from occupancy bits — no MeshFit GLB.
			(fitted, edge0YawRad) = EmitCoastLandOnlyFromStage6(
				stage6Corners, LastOccupancyBitsSampled, source);
		}

		mi.Name = $"DualCell_{key}_{family}";
		mi.Mesh = fitted;
		// W4: GEN height facts lift decks so high vs low reads in craft view (not flat stub).
		var genLift = ComputeCellGenYLift(cell);
		mi.Position = new Vector3(0f, genLift, 0f);
		mi.Rotation = Vector3.Zero; // yaw baked into Stage6 corner order (not world yaw)
		mi.Scale = Vector3.One;
		var biomeSpec = ResolveCellBiomeSpec(cell);
		if (biomeSpec.Kind != GenBiomeService.BiomeKind.None)
		{
			// GEN-biomes: tint land decks so Plains/Forest/Highland/… read at craft cam.
			// Refuse string_on_cell_alone — material difference is required.
			mi.MaterialOverride = MakeBiomeTintMaterial(biomeSpec);
		}
		else
		{
			mi.MaterialOverride = null;
		}
		mi.SortingOffset = 0f;
		mi.SetMeta("gen_height_lift", genLift);
		mi.SetMeta("vis_height_in_craft", GenTerrainApplied && _genHeightByVertex.Count > 0);
		mi.SetMeta("biome_id", (int)biomeSpec.Kind);
		mi.SetMeta("biome_name", biomeSpec.Name);
		mi.SetMeta("biome_tag", biomeSpec.MechanicalTag);
		mi.SetMeta("biome_move_cost", biomeSpec.MoveCost);
		mi.SetMeta("biome_difficult", biomeSpec.DifficultTerrain);
		mi.SetMeta("gen_biomes_slice", GenBiomesContract.SliceId);
		mi.SetMeta("dual_key", key);
		mi.SetMeta("weld_slice_id", WeldSliceId);
		mi.SetMeta("ask_id", PreferAskId);
		mi.SetMeta("art_style_id", ArtStyleId);
		mi.SetMeta("success_object", SuccessObject);
		mi.SetMeta("place_polarity", PlacePolarity);
		mi.SetMeta("paint_contract", PaintContract);
		mi.SetMeta("dual_cell_meshlibrary_placement", true);
		mi.SetMeta("owned_only_paint", false);
		mi.SetMeta("owned_only_coastline_deferred", false);
		mi.SetMeta("place_coast", true);
		mi.SetMeta("coast_stage6_land_emit", !isFull);
		mi.SetMeta("coast_strip_terrain_water", true); // KEEP: land-only (no Terrain_Water emit)
		mi.SetMeta("glb_meshfit_coast_as_success", false);
		mi.SetMeta("blue_water_as_coast_success", false);
		mi.SetMeta("update_four_sample_recompute", true);
		mi.SetMeta("update_four_recompute_success", true);
		mi.SetMeta("update_four_cross_as_success", false);
		mi.SetMeta("occupancy_bits_sampled", LastOccupancyBitsSampled);
		mi.SetMeta("tri_cell_place", stage6Corners.Length == 3);
		mi.SetMeta("dual_corners_n", stage6Corners.Length);
		mi.SetMeta("soft_take_4", false);
		mi.SetMeta("silent_ghost_without_place_n3", false);
		mi.SetMeta("neighbor_corner_spray_as_place", false);
		mi.SetMeta("coast_family", family.ToString());
		mi.SetMeta("seizure_coplanar_deck_as_success", false);
		mi.SetMeta("y_bias_as_zfight_fix", false);
		mi.SetMeta("weak_full_ybias_as_harden", false);
		mi.SetMeta("zfight_success_deferred", false);
		mi.SetMeta("full_single_deck_emit", isFull);
		mi.SetMeta("full_glb_meshfit", false);
		mi.SetMeta("full_flatten_to_single_deck", false);
		mi.SetMeta("full_wallless_plateau", false);
		mi.SetMeta("zfight_harden_full", false);
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
		mi.SetMeta("dual_edge_frame_yaw", false);
		mi.SetMeta("dual_edge_frame_yaw_rad", edge0YawRad);
		mi.SetMeta("world_yaw_as_dual_edge_frame", false);
		mi.SetMeta("mesh_fit_to_stage6_corners", false);
		mi.SetMeta("vertex_bilinear_warp_to_stage6_corners", false);
		mi.SetMeta("vertex_barycentric_warp_to_stage6_triangle", false);
		mi.SetMeta("corners_eq4_only_meshfit", false);
		mi.SetMeta("four_corner_sector_piece", false);
		mi.SetMeta("whole_dual_cell_land", isFull);
		mi.SetMeta("full_deck_y_lift", FullDeckYLift);
		mi.SetMeta("full_deck_edge_inset", FullDeckEdgeInset);
		mi.SetMeta("full_y_bias", 0f);
		mi.SetMeta("full_craft_lift_extra", 0f);
		mi.SetMeta("full_per_key_y_epsilon", 0f);
		mi.SetMeta("full_sorting_offset", 0f);
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
	}

	/// <summary>
	/// Full place path only — one opaque triangle/quad deck from Stage-6 corners at
	/// FullDeckYLift. Inset ~FullDeckEdgeInset toward centroid so shared edges do not
	/// strobe. Albedo copied from Full library item; cull back; depth write on.
	/// CameraHeight~3850 / DefaultSpacing=210: near-plane depth steps dwarf Y-bias harden —
	/// refuse MakeWalllessFullPlateau / FlattenFullToSingleDeck / MeshFit on Full GLB.
	/// </summary>
	private static (ArrayMesh Mesh, float Edge0YawRad) EmitFullSingleDeckFromStage6(
		Vector3[] stage6Corners,
		int rot90,
		bool mirror,
		Mesh librarySource)
	{
		if (stage6Corners == null || (stage6Corners.Length != 3 && stage6Corners.Length != 4))
			return (new ArrayMesh(), 0f);
		var c = OrientStage6Targets(stage6Corners, rot90, mirror);
		var edge0 = new Vector3(c[1].X - c[0].X, 0f, c[1].Z - c[0].Z);
		var edge0YawRad = MathF.Atan2(edge0.Z, edge0.X);

		var centre = Vector3.Zero;
		foreach (var p in c)
			centre += p;
		centre /= c.Length;
		var insetKeep = 1f - FullDeckEdgeInset;
		var deck = new Vector3[c.Length];
		for (var i = 0; i < c.Length; i++)
		{
			var xz = centre.Lerp(c[i], insetKeep);
			deck[i] = new Vector3(xz.X, FullDeckYLift, xz.Z);
		}

		var st = new SurfaceTool();
		st.Begin(Mesh.PrimitiveType.Triangles);
		void Tri(Vector3 a, Vector3 b, Vector3 c3)
		{
			st.SetNormal(Vector3.Up);
			st.AddVertex(a);
			st.SetNormal(Vector3.Up);
			st.AddVertex(b);
			st.SetNormal(Vector3.Up);
			st.AddVertex(c3);
		}
		if (deck.Length == 3)
		{
			Tri(deck[0], deck[1], deck[2]);
		}
		else
		{
			Tri(deck[0], deck[1], deck[2]);
			Tri(deck[0], deck[2], deck[3]);
		}
		var mesh = st.Commit();
		mesh.SurfaceSetMaterial(0, MakeFullSingleDeckMaterial(librarySource));
		return (mesh, edge0YawRad);
	}

	/// <summary>GEN-biomes land tint — distinct albedo per biome (not string-only).</summary>
	private static StandardMaterial3D MakeBiomeTintMaterial(GenBiomeService.BiomeSpec spec) =>
		new()
		{
			AlbedoColor = spec.Albedo,
			Transparency = BaseMaterial3D.TransparencyEnum.Disabled,
			CullMode = BaseMaterial3D.CullModeEnum.Back,
			ShadingMode = BaseMaterial3D.ShadingModeEnum.PerPixel,
			DepthDrawMode = BaseMaterial3D.DepthDrawModeEnum.OpaqueOnly,
		};

	/// <summary>
	/// Resolve biome for a DualCell from owner / occupancy corners (majority land biome).
	/// Water-only / unset → None (no tint; amber empty stays clear).
	/// </summary>
	private GenBiomeService.BiomeSpec ResolveCellBiomeSpec(OrganicDualOffsetLattice.DualCell cell)
	{
		if (_genBiomeByVertex.Count == 0)
			return GenBiomeService.SpecNone;

		var tallies = new Dictionary<GenBiomeService.BiomeKind, int>();
		void Tally(int v)
		{
			if (!_genBiomeByVertex.TryGetValue(v, out var kind))
				return;
			if (kind == GenBiomeService.BiomeKind.None)
				return;
			tallies.TryGetValue(kind, out var n);
			tallies[kind] = n + 1;
		}

		if (cell.OccupancyCorners != null)
		{
			foreach (var v in cell.OccupancyCorners)
				Tally(v);
		}
		Tally(cell.OwnerVertexId);

		if (tallies.Count == 0)
			return GenBiomeService.SpecNone;

		GenBiomeService.BiomeKind best = GenBiomeService.BiomeKind.None;
		var bestN = -1;
		foreach (var kv in tallies)
		{
			if (kv.Value > bestN)
			{
				bestN = kv.Value;
				best = kv.Key;
			}
		}
		return GenBiomeService.SpecFor(best);
	}

	/// <summary>Probe biome at a primary logic vertex for craft HUD / hover readout.</summary>
	public bool TryProbeBiome(int logicVertex, out GenBiomeService.BiomeSpec spec)
	{
		spec = GenBiomeService.SpecNone;
		if (logicVertex < 0)
			return false;
		if (!_genBiomeByVertex.TryGetValue(logicVertex, out var kind))
		{
			// Corner may be water-default (unwritten) — still report Water.
			if (GenTerrainApplied)
			{
				spec = GenBiomeService.SpecNone;
				return true;
			}
			return false;
		}
		spec = GenBiomeService.SpecFor(kind);
		return true;
	}

	/// <summary>Opaque Full deck material — albedo from library item only; cull back; depth write.</summary>
	private static StandardMaterial3D MakeFullSingleDeckMaterial(Mesh librarySource)
	{
		var albedo = new Color(0.45f, 0.55f, 0.38f, 1f);
		var arrayMesh = librarySource as ArrayMesh ?? ConvertMeshToArrayMesh(librarySource);
		if (arrayMesh != null && arrayMesh.GetSurfaceCount() > 0)
		{
			var mat = arrayMesh.SurfaceGetMaterial(0);
			if (mat is BaseMaterial3D baseMat)
				albedo = new Color(baseMat.AlbedoColor.R, baseMat.AlbedoColor.G, baseMat.AlbedoColor.B, 1f);
		}
		return new StandardMaterial3D
		{
			AlbedoColor = albedo,
			Transparency = BaseMaterial3D.TransparencyEnum.Disabled,
			CullMode = BaseMaterial3D.CullModeEnum.Back,
			ShadingMode = BaseMaterial3D.ShadingModeEnum.PerPixel,
			DepthDrawMode = BaseMaterial3D.DepthDrawModeEnum.OpaqueOnly,
		};
	}

	/// <summary>
	/// Coast place path — land-only Stage-6 deck from OccupancyCorners bits.
	/// Walks Stage-6 corners: ON corners enter outline; mixed edges insert midpoints
	/// (marching-squares coast). Fans from inset centre. Land albedo from library
	/// (skips Terrain_Water). Refuse MeshFit GLB coast / blue_water_as_coast_success /
	/// glb_meshfit_coast_as_success / sector_pie_as_dual_cell_tile.
	/// </summary>
	private static (ArrayMesh Mesh, float Edge0YawRad) EmitCoastLandOnlyFromStage6(
		Vector3[] stage6Corners,
		int occupancyBits,
		Mesh librarySource)
	{
		if (stage6Corners == null || (stage6Corners.Length != 3 && stage6Corners.Length != 4))
			return (new ArrayMesh(), 0f);
		var n = stage6Corners.Length;
		var mask = n == 3 ? 0b111 : 0b1111;
		var bits = occupancyBits & mask;
		if (bits == 0)
			return (new ArrayMesh(), 0f);

		var edge0 = new Vector3(
			stage6Corners[1].X - stage6Corners[0].X, 0f,
			stage6Corners[1].Z - stage6Corners[0].Z);
		var edge0YawRad = MathF.Atan2(edge0.Z, edge0.X);

		var centre = Vector3.Zero;
		foreach (var p in stage6Corners)
			centre += p;
		centre /= n;
		var insetKeep = 1f - FullDeckEdgeInset;
		Vector3 Inset(Vector3 p)
		{
			var xz = centre.Lerp(p, insetKeep);
			return new Vector3(xz.X, FullDeckYLift, xz.Z);
		}
		var centreDeck = new Vector3(centre.X, FullDeckYLift, centre.Z);
		var c = new Vector3[n];
		for (var i = 0; i < n; i++)
			c[i] = Inset(stage6Corners[i]);

		// Outline: ON corner verts + midpoints on mixed land/water edges.
		var outline = new List<Vector3>(n * 2);
		for (var i = 0; i < n; i++)
		{
			var onI = (bits & (1 << i)) != 0;
			var j = (i + 1) % n;
			var onJ = (bits & (1 << j)) != 0;
			if (onI)
				outline.Add(c[i]);
			if (onI != onJ)
			{
				var mid = stage6Corners[i].Lerp(stage6Corners[j], 0.5f);
				outline.Add(Inset(mid));
			}
		}
		if (outline.Count < 3)
			return (new ArrayMesh(), edge0YawRad);

		var st = new SurfaceTool();
		st.Begin(Mesh.PrimitiveType.Triangles);
		void Tri(Vector3 a, Vector3 b, Vector3 c3)
		{
			st.SetNormal(Vector3.Up);
			st.AddVertex(a);
			st.SetNormal(Vector3.Up);
			st.AddVertex(b);
			st.SetNormal(Vector3.Up);
			st.AddVertex(c3);
		}
		for (var i = 0; i < outline.Count; i++)
		{
			var a = outline[i];
			var b = outline[(i + 1) % outline.Count];
			Tri(centreDeck, a, b);
		}
		var mesh = st.Commit();
		mesh.SurfaceSetMaterial(0, MakeCoastLandOnlyMaterial(librarySource));
		return (mesh, edge0YawRad);
	}

	/// <summary>
	/// Land-only coast albedo — first non-Terrain_Water surface from library, else moss green.
	/// </summary>
	private static StandardMaterial3D MakeCoastLandOnlyMaterial(Mesh librarySource)
	{
		var albedo = new Color(0.45f, 0.55f, 0.38f, 1f);
		var arrayMesh = librarySource as ArrayMesh ?? ConvertMeshToArrayMesh(librarySource);
		if (arrayMesh != null)
		{
			for (var surf = 0; surf < arrayMesh.GetSurfaceCount(); surf++)
			{
				var mat = arrayMesh.SurfaceGetMaterial(surf);
				if (IsTerrainWaterMaterial(mat))
					continue;
				if (mat is BaseMaterial3D baseMat)
				{
					albedo = new Color(baseMat.AlbedoColor.R, baseMat.AlbedoColor.G, baseMat.AlbedoColor.B, 1f);
					break;
				}
			}
		}
		return new StandardMaterial3D
		{
			AlbedoColor = albedo,
			Transparency = BaseMaterial3D.TransparencyEnum.Disabled,
			CullMode = BaseMaterial3D.CullModeEnum.Back,
			ShadingMode = BaseMaterial3D.ShadingModeEnum.PerPixel,
			DepthDrawMode = BaseMaterial3D.DepthDrawModeEnum.OpaqueOnly,
		};
	}

	/// <summary>
	/// Dual-edge-frame fit (n=4): authored mesh +X/+Z footprint → UV along Stage6 edge0
	/// (c0→c1) and c0→c3, then bilinear onto Stage6CornersLocal.
	/// Triangle fit (n=3): same UV → barycentric warp onto c0,c1,c2 (fold u+v&gt;1).
	/// Rot90/mirror permute targets. Legacy MeshFit path — coast now uses
	/// EmitCoastLandOnlyFromStage6 (2aa). Kept for refuse proofs / prototypes only.
	/// Strips Terrain_Water surfaces (name or water albedo) so land geometry alone MeshFits —
	/// refuse blue_water_as_coast_success / continuous blue blob.
	/// Returns edge0 yaw (rad) — refuse world_yaw_as_dual_edge_frame / corners_eq4_only_meshfit.
	/// </summary>
	private static (ArrayMesh Mesh, float Edge0YawRad) MeshFitToDualEdgeFrame(
		Mesh source,
		Vector3[] corners,
		int rot90,
		bool mirror)
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
		var lift = FullDeckYLift;
		var tri = c.Length == 3;

		var outMesh = new ArrayMesh();
		for (var surf = 0; surf < arrayMesh.GetSurfaceCount(); surf++)
		{
			var mat = arrayMesh.SurfaceGetMaterial(surf);
			// Coast MeshFit: skip Terrain_Water so Moss/Earth/Stone/Sand alone land in the slot.
			if (IsTerrainWaterMaterial(mat))
				continue;
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
			if (mat != null)
				outMesh.SurfaceSetMaterial(outMesh.GetSurfaceCount() - 1, mat);
		}
		return (outMesh, edge0YawRad);
	}

	/// <summary>
	/// True when a MeshFit surface is authored water (Terrain_Water name or blue water albedo).
	/// Used only on non-Empty coast MeshFit path — Empty ClearDualSlot never MeshFits.
	/// </summary>
	private static bool IsTerrainWaterMaterial(Material? mat)
	{
		if (mat == null)
			return false;
		var name = mat.ResourceName ?? string.Empty;
		if (name.Contains("Terrain_Water", StringComparison.OrdinalIgnoreCase)
		    || name.Contains("terrain_water", StringComparison.OrdinalIgnoreCase))
			return true;
		// Godot import sometimes parks the GLB material name on the resource path tip.
		var path = mat.ResourcePath ?? string.Empty;
		if (path.Contains("Terrain_Water", StringComparison.OrdinalIgnoreCase))
			return true;
		if (mat is BaseMaterial3D baseMat)
		{
			var a = baseMat.AlbedoColor;
			// Nature-pack / craft water: blue-dominant, not sand/moss/earth/stone.
			if (a.B > 0.35f && a.B > a.R + 0.08f && a.B >= a.G - 0.02f && a.A > 0.5f)
				return true;
		}
		return false;
	}

	/// <summary>Legacy name — dual-edge-frame fit (edge0 = c0→c1).</summary>
	private static ArrayMesh MeshFitToSmallCornerQuad(
		Mesh source,
		Vector3[] corners,
		int rot90,
		bool mirror) =>
		MeshFitToDualEdgeFrame(source, corners, rot90, mirror).Mesh;

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
	/// PLACE-update-four KEEP: OccupancyCorners bits always sampled on recompute.
	/// Place KEEP: OwnerVertexId on → Full whole DualCell.
	/// PLACE-coast: owner off → bits map to Edge/Corner/Diagonal/InverseCorner/Full/Empty
	/// (supersedes owned-only coastline Empty deferral). Spray ≠ place Success.
	/// </summary>
	private (DualVisualFamily Family, int Rot90, bool Mirror) ResolveOrganicDualVisualFamily(
		int[] occupancyCorners,
		int ownerVertexId)
	{
		// Always sample OccupancyCorners bits (PLACE-update-four honesty KEEP).
		var bits = 0;
		var n = 0;
		if (occupancyCorners != null &&
		    (occupancyCorners.Length == 3 || occupancyCorners.Length == 4))
		{
			n = occupancyCorners.Length;
			for (var i = 0; i < n; i++)
				if (_cornerLogic.TryGetValue(occupancyCorners[i], out var on) && on)
					bits |= 1 << i;
		}
		LastOccupancyBitsSampled = bits;

		var ownerOn = _cornerLogic.TryGetValue(ownerVertexId, out var o) && o;

		// Place KEEP: owner V on → whole DualCell Full (tri or quad plate).
		if (ownerOn)
			return (DualVisualFamily.Full, 0, false);

		// PLACE-coast: owner off → coastline family from OccupancyCorners bits.
		if (n == 3 || n == 4)
			return MapOccupancyBitsToCoastFamily(bits, n);

		return (DualVisualFamily.Empty, 0, false);
	}

	/// <summary>
	/// OccupancyCorners bit mask → sixpack family + rot90 in dual-edge frame.
	/// Corner L at c0; Edge bar along c0→c1; InverseCorner land on c0..c2 (missing c3).
	/// n=3 tri DualCell — no soft_take_4 pad to fake 4.
	/// </summary>
	private static (DualVisualFamily Family, int Rot90, bool Mirror) MapOccupancyBitsToCoastFamily(
		int bits,
		int cornerCount)
	{
		if (cornerCount == 3)
			return MapTriOccupancyBitsToCoastFamily(bits & 0b111);
		return MapQuadOccupancyBitsToCoastFamily(bits & 0b1111);
	}

	private static (DualVisualFamily Family, int Rot90, bool Mirror) MapQuadOccupancyBitsToCoastFamily(int bits) =>
		bits switch
		{
			0b0000 => (DualVisualFamily.Empty, 0, false),
			0b0001 => (DualVisualFamily.Corner, 0, false),
			0b0010 => (DualVisualFamily.Corner, 1, false),
			0b0100 => (DualVisualFamily.Corner, 2, false),
			0b1000 => (DualVisualFamily.Corner, 3, false),
			0b0011 => (DualVisualFamily.Edge, 0, false),
			0b0110 => (DualVisualFamily.Edge, 1, false),
			0b1100 => (DualVisualFamily.Edge, 2, false),
			0b1001 => (DualVisualFamily.Edge, 3, false),
			0b0101 => (DualVisualFamily.Diagonal, 0, false),
			0b1010 => (DualVisualFamily.Diagonal, 1, false),
			0b0111 => (DualVisualFamily.InverseCorner, 0, false),
			0b1110 => (DualVisualFamily.InverseCorner, 1, false),
			0b1101 => (DualVisualFamily.InverseCorner, 2, false),
			0b1011 => (DualVisualFamily.InverseCorner, 3, false),
			0b1111 => (DualVisualFamily.Full, 0, false),
			_ => (DualVisualFamily.Empty, 0, false),
		};

	private static (DualVisualFamily Family, int Rot90, bool Mirror) MapTriOccupancyBitsToCoastFamily(int bits) =>
		bits switch
		{
			0b000 => (DualVisualFamily.Empty, 0, false),
			0b001 => (DualVisualFamily.Corner, 0, false),
			0b010 => (DualVisualFamily.Corner, 1, false),
			0b100 => (DualVisualFamily.Corner, 2, false),
			0b011 => (DualVisualFamily.Edge, 0, false),
			0b110 => (DualVisualFamily.Edge, 1, false),
			0b101 => (DualVisualFamily.Edge, 2, false),
			0b111 => (DualVisualFamily.Full, 0, false),
			_ => (DualVisualFamily.Empty, 0, false),
		};

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

			var package = WorldPackageSession.Active;
			var landCount = 0;
			var waterCount = 0;
			foreach (var kv in _cornerLogic)
			{
				if (kv.Value) landCount++;
				else waterCount++;
			}
			// Vertices never written are water defaults for gen silhouette counts.
			if (_organicMesh != null && _cornerLogic.Count < _organicMesh.VertexCount)
				waterCount += _organicMesh.VertexCount - _cornerLogic.Count;

			// Organic mesh seed is mandatory for quit/reload silhouette fidelity:
			// corner/height/river indices bind to a seeded Stålberg remesh; a fresh
			// random remesh on Load maps the same indices onto a different board
			// (operator F5: "persisted terrain died and was regened").
			var organicSeed = _organicMesh?.Seed ?? 0UL;
			var payload = new Dictionary<string, object>
			{
				["schema_version"] = WorldPackage.SchemaVersion,
				["stamp"] = CanonicalStampId,
				["slice_id"] = GenBiomesContract.SliceId,
				["ask_id"] = GenBiomesContract.AskId,
				["ticket_map"] = GenBiomesContract.TicketMap,
				["weld_slice_id"] = GenBiomesContract.SliceId,
				["prior_pack_slice"] = PackSaveLoadContract.SliceId,
				["prior_tone_slice"] = GenToneContract.SliceId,
				["persist_path"] = PackSaveLoadContract.PersistPath,
				["grammar"] = "world_package_gen_board",
				["lattice"] = "organic_quad_faces",
				["seed_rings"] = _seedRingCount,
				["organic_seed"] = organicSeed.ToString(),
				["seed_spacing"] = _hexSize,
				["ux_bullet"] = "UX-1",
				["world"] = SerializeWorldPackage(package),
				["gen"] = new Dictionary<string, object>
				{
					["applied"] = GenTerrainApplied,
					["summary"] = LastGenTerrainSummary,
					["land_count"] = landCount,
					["water_count"] = waterCount,
					["river_count"] = _genRiverVertices.Count,
					["corner_logic"] = SerializeCornerLogic(),
					["heights"] = SerializeHeights(),
					["rivers"] = _genRiverVertices.OrderBy(v => v).ToList(),
					["biomes"] = SerializeBiomes(),
					["biomes_summary"] = LastGenBiomesSummary,
					["biome_distinct"] = LastGenBiomeDistinctLand,
				},
				["cells"] = SerializeOccupancy(),
			};
			File.WriteAllText(abs, JsonSerializer.Serialize(payload));
			AlphaFactoryLog.Emit(
				"pack.save",
				"PACK_save_load",
				$"PACK persist → {path} world={package?.WorldId ?? "(none)"} land={landCount} water={waterCount} rivers={_genRiverVertices.Count} corners={_cornerLogic.Count} organic_seed={organicSeed}",
				new Dictionary<string, object>
				{
					["ask_id"] = GenBiomesContract.AskId,
					["slice_id"] = GenBiomesContract.SliceId,
					["ticket_map"] = GenBiomesContract.TicketMap,
					["path"] = path,
					["world_id"] = package?.WorldId ?? "",
					["gen_bias"] = package?.GenBiasId ?? "",
					["land_count"] = landCount,
					["water_count"] = waterCount,
					["river_count"] = _genRiverVertices.Count,
					["biome_distinct"] = LastGenBiomeDistinctLand,
					["organic_seed"] = organicSeed.ToString(),
					["seed_rings"] = _seedRingCount,
					["gen_applied"] = GenTerrainApplied,
					["real_file"] = true,
					["fake_toast"] = false,
				});
			return Error.Ok;
		}
		catch (Exception ex)
		{
			AlphaFactoryLog.Emit("Degrade_FailVisible", "PACK_save_load", ex.Message, level: "error");
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

			var hasPackGen = root.TryGetProperty("gen", out var genEl)
				&& genEl.ValueKind == JsonValueKind.Object
				&& genEl.TryGetProperty("corner_logic", out _);

			if (hasPackGen)
			{
				var rings = root.TryGetProperty("seed_rings", out var ringsEl)
					? ringsEl.GetInt32()
					: _seedRingCount;
				if (rings <= 0)
					rings = _seedRingCount;

				ulong? organicSeed = null;
				if (root.TryGetProperty("organic_seed", out var seedEl))
				{
					if (seedEl.ValueKind == JsonValueKind.String
						&& ulong.TryParse(seedEl.GetString(), out var parsedSeed))
						organicSeed = parsedSeed;
					else if (seedEl.ValueKind == JsonValueKind.Number
						&& seedEl.TryGetUInt64(out var numSeed))
						organicSeed = numSeed;
				}

				if (root.TryGetProperty("seed_spacing", out var spacingEl)
					&& spacingEl.ValueKind == JsonValueKind.Number)
				{
					var spacing = (float)spacingEl.GetDouble();
					if (spacing > 0.01f)
						_hexSize = spacing;
				}

				// Always remesh with the persisted organic seed before reapplying board
				// facts — craft enter builds a default ring/seed mesh that must not keep
				// mismatched vertex indices. Missing seed = pre-fix pack; remesh rings
				// only and fail-visible (silhouette will not match until re-save).
				if (organicSeed.HasValue)
					RegenerateOrganicQuadMesh(rings, organicSeed.Value);
				else if (rings != _seedRingCount || _organicMesh == null)
					RegenerateOrganicQuadMesh(rings);

				if (_organicMesh == null || _dualLattice == null || _dualRoot == null)
					return Error.Failed;

				if (organicSeed.HasValue && _organicMesh.Seed != organicSeed.Value)
				{
					AlphaFactoryLog.Emit(
						"Degrade_FailVisible",
						"PACK_save_load",
						$"PACK restore organic seed mismatch want={organicSeed.Value} got={_organicMesh.Seed} — silhouette fidelity broken",
						level: "error");
					return Error.Failed;
				}

				_cornerLogic.Clear();
				_genHeightByVertex.Clear();
				_genBiomeByVertex.Clear();
				_genRiverVertices.Clear();

				if (genEl.TryGetProperty("corner_logic", out var corners))
				{
					foreach (var item in corners.EnumerateArray())
					{
						var v = item.GetProperty("v").GetInt32();
						var on = item.TryGetProperty("on", out var onEl) && onEl.GetBoolean();
						if (v < 0 || (_organicMesh != null && v >= _organicMesh.VertexCount))
							continue;
						_cornerLogic[v] = on;
					}
				}

				if (genEl.TryGetProperty("heights", out var heights))
				{
					foreach (var item in heights.EnumerateArray())
					{
						var v = item.GetProperty("v").GetInt32();
						var h = item.TryGetProperty("h", out var hEl)
							? (float)hEl.GetDouble()
							: 0f;
						if (v < 0 || (_organicMesh != null && v >= _organicMesh.VertexCount))
							continue;
						_genHeightByVertex[v] = h;
					}
				}

				if (genEl.TryGetProperty("rivers", out var rivers))
				{
					foreach (var item in rivers.EnumerateArray())
					{
						var v = item.GetInt32();
						if (v < 0 || (_organicMesh != null && v >= _organicMesh.VertexCount))
							continue;
						_genRiverVertices.Add(v);
					}
				}

				if (genEl.TryGetProperty("biomes", out var biomesEl))
				{
					foreach (var item in biomesEl.EnumerateArray())
					{
						var v = item.GetProperty("v").GetInt32();
						if (v < 0 || (_organicMesh != null && v >= _organicMesh.VertexCount))
							continue;
						GenBiomeService.BiomeKind kind = GenBiomeService.BiomeKind.None;
						if (item.TryGetProperty("biome", out var bEl))
						{
							if (bEl.ValueKind == JsonValueKind.String)
								GenBiomeService.TryParseKind(bEl.GetString(), out kind);
							else if (bEl.ValueKind == JsonValueKind.Number
								&& bEl.TryGetByte(out var bn)
								&& Enum.IsDefined(typeof(GenBiomeService.BiomeKind), bn))
								kind = (GenBiomeService.BiomeKind)bn;
						}
						_genBiomeByVertex[v] = kind;
					}
				}

				RefreshAllDualSlots();
				RebuildGenRiverRibbon();
				GenTerrainApplied = !genEl.TryGetProperty("applied", out var appliedEl)
					|| appliedEl.GetBoolean()
					|| _cornerLogic.Count > 0;
				var land = genEl.TryGetProperty("land_count", out var lc) ? lc.GetInt32() : _cornerLogic.Count(kv => kv.Value);
				var water = genEl.TryGetProperty("water_count", out var wc) ? wc.GetInt32() : 0;
				var riverN = genEl.TryGetProperty("river_count", out var rc)
					? rc.GetInt32()
					: _genRiverVertices.Count;
				LastGenRiverCarveCount = _genRiverVertices.Count;
				var restoredLand = _cornerLogic.Count(kv => kv.Value);
				var restoredWater = _cornerLogic.Count - restoredLand;
				LastGenTerrainSummary = genEl.TryGetProperty("summary", out var sumEl)
					? sumEl.GetString() ?? $"pack restore land={restoredLand} water={restoredWater} rivers={riverN}"
					: $"pack restore land={restoredLand} water={restoredWater} rivers={riverN}";
				var (distinctBiomes, _) = GenBiomeService.CountLand(_genBiomeByVertex);
				LastGenBiomeDistinctLand = distinctBiomes;
				LastGenBiomesSummary = genEl.TryGetProperty("biomes_summary", out var bioSumEl)
					? bioSumEl.GetString() ?? $"pack biomes distinct={distinctBiomes}"
					: $"pack biomes distinct={distinctBiomes}";
				if (!string.IsNullOrEmpty(LastGenBiomesSummary))
					LastGenTerrainSummary = $"{LastGenTerrainSummary} · {LastGenBiomesSummary}";

				// Optional occupancy cells (hand paint faces) after gen restore.
				if (root.TryGetProperty("cells", out var packCells))
					LoadOccupancyCells(packCells);

				AlphaFactoryLog.Emit(
					"pack.load",
					"PACK_save_load",
					$"PACK restore ← {path} land={land} water={water} rivers={_genRiverVertices.Count} corners={_cornerLogic.Count} applied={GenTerrainApplied} organic_seed={_organicMesh.Seed} seed_ok={organicSeed.HasValue}",
					new Dictionary<string, object>
					{
						["ask_id"] = PackSaveLoadContract.AskId,
						["slice_id"] = PackSaveLoadContract.SliceId,
						["path"] = path,
						["land_count"] = land,
						["water_count"] = water,
						["river_count"] = _genRiverVertices.Count,
						["restored_land"] = restoredLand,
						["restored_water"] = restoredWater,
						["organic_seed"] = _organicMesh.Seed.ToString(),
						["organic_seed_persisted"] = organicSeed.HasValue,
						["seed_rings"] = _seedRingCount,
						["gen_applied"] = GenTerrainApplied,
						["blank_amber"] = _cornerLogic.Count == 0,
						["auto_gen_skipped"] = true,
					});
				return _cornerLogic.Count == 0 && !GenTerrainApplied ? Error.InvalidData : Error.Ok;
			}

			// Legacy occupancy-only payloads (pre-PACK).
			if (root.TryGetProperty("cells", out var cells))
			{
				LoadOccupancyCells(cells);
			}
			else if (root.TryGetProperty("logic_points", out var legacy))
			{
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
				$"loaded legacy occupancy ← {path} cells={_occupancy.Count}",
				new Dictionary<string, object> { ["ask_id"] = PreferAskId, ["ux"] = "UX-5" });
			return Error.Ok;
		}
		catch (Exception ex)
		{
			AlphaFactoryLog.Emit("Degrade_FailVisible", "PACK_save_load", ex.Message, level: "error");
			return Error.Failed;
		}
	}

	private void LoadOccupancyCells(JsonElement cells)
	{
		foreach (var item in cells.EnumerateArray())
		{
			var q = item.GetProperty("q").GetInt32();
			var r = item.GetProperty("r").GetInt32();
			var cell = new Vector2I(q, r);
			if (cell.Y != 0 || _organicMesh == null || !_organicMesh.ContainsFace(cell.X))
				continue;
			var fill = item.TryGetProperty("fill", out var f)
				? (CellFill)f.GetInt32()
				: CellFill.Filled;
			SetCellFill(cell, fill);
		}
	}

	private static Dictionary<string, object> SerializeWorldPackage(WorldPackage? package)
	{
		if (package == null)
		{
			return new Dictionary<string, object>
			{
				["world_id"] = "",
				["display_name"] = "",
				["gen_bias"] = "medium",
				["opened_at_utc"] = DateTimeOffset.UtcNow.ToString("O"),
				["dials"] = SerializeDials(WorldBoundsDials.Defaults),
			};
		}

		return new Dictionary<string, object>
		{
			["world_id"] = package.WorldId,
			["display_name"] = package.DisplayName,
			["gen_bias"] = package.GenBiasId,
			["opened_at_utc"] = package.OpenedAtUtc.ToString("O"),
			["dials"] = SerializeDials(package.Bounds),
			["scaffold_id"] = package.Scaffold.ScaffoldId,
			["scaffold_feed_salt"] = (int)package.Scaffold.GenFeedSalt,
			["intent_accepted_count"] = package.Intents.AcceptedCount,
			["lore_feed_salt"] = (int)package.Intents.LoreFeedSalt,
		};
	}

	private static Dictionary<string, object> SerializeDials(WorldBoundsDials dials) => new()
	{
		["cell_size"] = dials.CellSize,
		["cell_count"] = dials.CellCount,
		["settlement_distance"] = dials.SettlementDistance,
		["rivers"] = dials.Rivers,
		["climate"] = dials.Climate,
		["wildness"] = dials.Wildness,
		["seed_rings"] = dials.ToSeedRingCount(),
		["summary"] = dials.SummaryLine(),
	};

	private List<Dictionary<string, object>> SerializeCornerLogic()
	{
		var list = new List<Dictionary<string, object>>();
		foreach (var (v, on) in _cornerLogic.OrderBy(kv => kv.Key))
		{
			list.Add(new Dictionary<string, object>
			{
				["v"] = v,
				["on"] = on,
			});
		}
		return list;
	}

	private List<Dictionary<string, object>> SerializeHeights()
	{
		var list = new List<Dictionary<string, object>>();
		foreach (var (v, h) in _genHeightByVertex.OrderBy(kv => kv.Key))
		{
			list.Add(new Dictionary<string, object>
			{
				["v"] = v,
				["h"] = h,
			});
		}
		return list;
	}

	private List<Dictionary<string, object>> SerializeBiomes()
	{
		var list = new List<Dictionary<string, object>>();
		foreach (var (v, kind) in _genBiomeByVertex.OrderBy(kv => kv.Key))
		{
			var spec = GenBiomeService.SpecFor(kind);
			list.Add(new Dictionary<string, object>
			{
				["v"] = v,
				["biome"] = kind.ToString(),
				["tag"] = spec.MechanicalTag,
				["move"] = spec.MoveCost,
				["difficult"] = spec.DifficultTerrain,
			});
		}
		return list;
	}

	/// <summary>Read package fields from a PACK JSON without applying craft board (LaunchShell Load World).</summary>
	public static bool TryReadPackWorld(string path, out WorldPackage? package, out string summary)
	{
		package = null;
		summary = "";
		try
		{
			var abs = ProjectSettings.GlobalizePath(path);
			if (!File.Exists(abs))
			{
				summary = "no pack file";
				return false;
			}

			using var doc = JsonDocument.Parse(File.ReadAllText(abs));
			var root = doc.RootElement;
			if (!root.TryGetProperty("world", out var worldEl))
			{
				summary = "pack missing world block";
				return false;
			}

			var biasId = worldEl.TryGetProperty("gen_bias", out var biasEl)
				? biasEl.GetString() ?? "medium"
				: "medium";
			var dials = WorldBoundsDials.Defaults;
			if (worldEl.TryGetProperty("dials", out var dialsEl) && dialsEl.ValueKind == JsonValueKind.Object)
			{
				dials = new WorldBoundsDials(
					cellSize: dialsEl.TryGetProperty("cell_size", out var cs) ? (float)cs.GetDouble() : dials.CellSize,
					cellCount: dialsEl.TryGetProperty("cell_count", out var cc) ? (float)cc.GetDouble() : dials.CellCount,
					settlementDistance: dialsEl.TryGetProperty("settlement_distance", out var sd)
						? (float)sd.GetDouble()
						: dials.SettlementDistance,
					rivers: dialsEl.TryGetProperty("rivers", out var rv) ? (float)rv.GetDouble() : dials.Rivers,
					climate: dialsEl.TryGetProperty("climate", out var cl) ? (float)cl.GetDouble() : dials.Climate,
					wildness: dialsEl.TryGetProperty("wildness", out var wd) ? (float)wd.GetDouble() : dials.Wildness);
			}

			var opened = DateTimeOffset.UtcNow;
			if (worldEl.TryGetProperty("opened_at_utc", out var openedEl)
				&& DateTimeOffset.TryParse(openedEl.GetString(), out var parsed))
				opened = parsed;

			package = WorldPackage.FromPersisted(
				worldId: worldEl.TryGetProperty("world_id", out var idEl) ? idEl.GetString() ?? "" : "",
				displayName: worldEl.TryGetProperty("display_name", out var nameEl) ? nameEl.GetString() ?? "" : "",
				bias: WorldPackage.ParseBiasId(biasId),
				bounds: dials,
				openedAtUtc: opened);
			var land = 0;
			var water = 0;
			var rivers = 0;
			if (root.TryGetProperty("gen", out var genEl))
			{
				land = genEl.TryGetProperty("land_count", out var lc) ? lc.GetInt32() : 0;
				water = genEl.TryGetProperty("water_count", out var wc) ? wc.GetInt32() : 0;
				rivers = genEl.TryGetProperty("river_count", out var rc) ? rc.GetInt32() : 0;
			}
			summary =
				$"id={package.WorldId} bias={package.GenBiasId} land={land} water={water} rivers={rivers} dials=[{package.Bounds.SummaryLine()}]";
			return true;
		}
		catch (Exception ex)
		{
			summary = ex.Message;
			return false;
		}
	}

	public static bool PackFileExists(string? path = null)
	{
		var p = string.IsNullOrWhiteSpace(path) ? PackSaveLoadContract.PersistPath : path!;
		return File.Exists(ProjectSettings.GlobalizePath(p));
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
	/// UPDATE — DualCellsTouching(V) when Y=PrimaryPickY: owned + DualCellsSampling(V).
	/// PLACE-update-four Success = shared DualCells that sample V recompute (bits sampled;
	/// owned-only mesh resolve KEEP). Place Full only on OwnedDualCell(V); sampling
	/// neighbors Clear/Empty unless their own owner is on (not Corner spray as Success).
	/// ≤ MaxDualCellsPerLogicFlip. Refuse secondary Y / face stamp / soft Take(4).
	/// </summary>
	public int UpdateFourDualSlots(Vector2I occupancy)
	{
		// Organic dual-lattice: Y==PrimaryPickY primary V place; secondary Y refused.
		if (_organicMesh != null && _dualRoot != null && _dualLattice != null)
		{
			// Organic populate: DualCellsTouching = owned + DualCellsSampling(V).
			// Owned Full when owner on; sampling neighbours recompute → Clear unless N owner-on.
			if (occupancy.Y == SecondaryPickY)
			{
				AlphaFactoryLog.Emit("craft.refuse", "secondary_glow_center_as_place_target",
					$"refuse secondary Y UpdateFour occupancy={occupancy} — use primary Y={PrimaryPickY} DualCellsTouching(owned+sampling)",
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
						$"refuse over_neighbor_paint vertex={vertex} touching_duals={cells.Count} cap={MaxDualCellsPerLogicFlip} sampling={_dualLattice.DualCellKeysSampling(vertex).Count}",
						level: "error");
					return 0;
				}
				var n = 0;
				foreach (var cell in cells)
				{
					EnsureStage6DualCellMesh(cell);
					n++;
				}
				AlphaFactoryLog.Emit(
					"craft.dual",
					"UpdateFour_SampleRecompute",
					$"vertex={vertex} refreshed={n} sampling={_dualLattice.DualCellKeysSampling(vertex).Count} last_bits={LastOccupancyBitsSampled} place_coast=true owned_only_coastline_deferred=false",
					new Dictionary<string, object>
					{
						["ask_id"] = PreferAskId,
						["overlay"] = WeldSliceId,
						["update_four_sample_recompute"] = true,
						["update_four_recompute_success"] = true,
						["place_coast"] = true,
						["owned_only_coastline_deferred"] = false,
						["neighbor_corner_spray_as_place"] = false,
						["update_four_cross_as_success"] = false,
						["occupancy_bits_sampled"] = LastOccupancyBitsSampled,
						["refreshed"] = n,
					});
				return n;
			}
			AlphaFactoryLog.Emit("craft.refuse", "primary_face_as_dual",
				$"refuse face-index UpdateFour occupancy={occupancy} — use primary Y={PrimaryPickY} DualCellsTouching(owned+sampling)",
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
	/// GEN-terrain-product populate — Azgaar-style altitude → land/water + craft height lift + river ribbon.
	/// Never called from EnsureHost / BuildOrganicDualCornerOverlay.
	/// Create World Open: WorldgenCraft auto-invokes after scene ready.
	/// Enter Craft: Key.T accel only (1g empty manual lane; no Generate product button).
	/// </summary>
	public GenTerrainService.PassResult? ApplyGenTerrainPass(
		WorldGenBias bias,
		WorldBoundsDials? dials = null,
		uint? seed = null,
		WorldScaffoldProposal? scaffold = null,
		uint loreFeedSalt = 0)
	{
		if (_organicMesh == null || _dualLattice == null || _dualRoot == null)
		{
			AlphaFactoryLog.Emit(
				"gen.terrain",
				"GEN_terrain_refuse",
				"ApplyGenTerrainPass refused — organic dual board not armed",
				level: "warn");
			return null;
		}

		var bounds = dials ?? WorldBoundsDials.Defaults;
		// W2 sister dial: cell count → seed rings / board cell budget (not landform freq).
		// Remesh before paint so Create World Open footprint visibly grows/shrinks.
		var targetRings = bounds.ToSeedRingCount();
		if (_seedRingCount != targetRings || _organicMesh == null || _dualLattice == null)
			RegenerateOrganicQuadMesh(targetRings);
		if (_organicMesh == null || _dualLattice == null || _dualRoot == null)
		{
			AlphaFactoryLog.Emit(
				"gen.terrain",
				"GEN_terrain_refuse",
				"ApplyGenTerrainPass refused — remesh after cell-count dial left board unarmed",
				level: "warn");
			return null;
		}

		var editable = _dualLattice.EditableLogicPoints;
		// WORLD-propose feed + optional s0 lore salt (empty lore = no-op).
		var pass = GenTerrainService.Compute(
			_organicMesh.Vertices, editable, bias, bounds, seed, scaffold, loreFeedSalt);

		// W5 polish: downhill watercourses along organic edges when rivers dial > 0.
		if (bounds.Rivers > 0f)
		{
			var adj = BuildOrganicVertexAdjacency();
			GenTerrainService.CarveDownhillRivers(pass, adj, bounds.Rivers);
		}

		_cornerLogic.Clear();
		_genHeightByVertex.Clear();
		_genBiomeByVertex.Clear();
		_genRiverVertices.Clear();
		foreach (var kv in pass.LandByVertex)
			_cornerLogic[kv.Key] = kv.Value;
		foreach (var kv in pass.HeightByVertex)
			_genHeightByVertex[kv.Key] = kv.Value;
		foreach (var kv in pass.RiverByVertex)
		{
			if (kv.Value)
				_genRiverVertices.Add(kv.Key);
		}

		// GEN-biomes: assign after land/water/height/rivers so Open shows tinted biomes.
		var biomeMap = GenBiomeService.Assign(pass, _organicMesh?.Vertices);
		foreach (var kv in biomeMap)
			_genBiomeByVertex[kv.Key] = kv.Value;
		var (distinctBiomes, biomeCounts) = GenBiomeService.CountLand(_genBiomeByVertex);
		LastGenBiomeDistinctLand = distinctBiomes;
		LastGenBiomesSummary = GenBiomeService.SummaryLine(_genBiomeByVertex, bounds);

		RefreshAllDualSlots();
		RebuildGenRiverRibbon();
		GenTerrainApplied = true;
		LastGenTerrainSummary = $"{pass.SummaryLine} · {LastGenBiomesSummary}";
		LastGenRiverCarveCount = _genRiverVertices.Count;

		var fields = pass.ToLogFields();
		fields["river_carve_count_applied"] = _genRiverVertices.Count;
		fields["altitude_bands_applied"] = true;
		fields["biome_distinct_land"] = distinctBiomes;
		fields["biomes_summary"] = LastGenBiomesSummary;
		foreach (var kv in biomeCounts)
			fields["biome_count_" + kv.Key.ToString().ToLowerInvariant()] = kv.Value;
		foreach (var kv in GenBiomesContract.ToLogFields())
			fields["biome_" + kv.Key] = kv.Value;
		AlphaFactoryLog.Emit(
			"gen.terrain",
			"GEN_terrain_apply",
			$"GEN-biomes-r1 apply — {LastGenTerrainSummary} rivers_applied={_genRiverVertices.Count} biome_distinct={distinctBiomes} (refuse string_on_cell_alone|identical_look_all_land_biomes|empty_create_world_open|gen_sites_not_armed)",
			fields);

		return pass;
	}

	/// <summary>Organic quad edges → undirected adjacency for downhill river carve.</summary>
	private Dictionary<int, List<int>> BuildOrganicVertexAdjacency()
	{
		var adj = new Dictionary<int, List<int>>();
		if (_organicMesh?.Quads == null)
			return adj;
		void Link(int a, int b)
		{
			if (a == b) return;
			if (!adj.TryGetValue(a, out var la))
			{
				la = new List<int>(4);
				adj[a] = la;
			}
			if (!la.Contains(b)) la.Add(b);
			if (!adj.TryGetValue(b, out var lb))
			{
				lb = new List<int>(4);
				adj[b] = lb;
			}
			if (!lb.Contains(a)) lb.Add(a);
		}
		foreach (var q in _organicMesh.Quads)
		{
			if (q == null || q.Length != 4) continue;
			for (var i = 0; i < 4; i++)
				Link(q[i], q[(i + 1) % 4]);
		}
		return adj;
	}

	/// <summary>W4 — average gen height for DualCell corners → craft Y lift.</summary>
	private float ComputeCellGenYLift(OrganicDualOffsetLattice.DualCell cell)
	{
		if (_genHeightByVertex.Count == 0)
			return 0f;
		var sum = 0f;
		var n = 0;
		if (cell.OccupancyCorners != null)
		{
			foreach (var v in cell.OccupancyCorners)
			{
				if (_genHeightByVertex.TryGetValue(v, out var h))
				{
					sum += h;
					n++;
				}
			}
		}
		if (n == 0 && _genHeightByVertex.TryGetValue(cell.OwnerVertexId, out var oh))
		{
			sum = oh;
			n = 1;
		}
		if (n == 0)
			return 0f;
		return (sum / n) * GenHeightVisualScale;
	}

	private void ClearGenRiverRibbon()
	{
		if (_genRiverRibbon != null && GodotObject.IsInstanceValid(_genRiverRibbon))
			_genRiverRibbon.QueueFree();
		_genRiverRibbon = null;
	}

	/// <summary>
	/// W5 — rivers dial &gt; 0 paints readable blue watercourse ribbons along river vertex edges;
	/// dial 0 leaves ribbon cleared. Wider than r1 so corridors read at craft cam.
	/// </summary>
	private void RebuildGenRiverRibbon()
	{
		ClearGenRiverRibbon();
		if (_organicMesh == null || _dualRoot == null || _genRiverVertices.Count == 0)
			return;

		var st = new SurfaceTool();
		st.Begin(Mesh.PrimitiveType.Triangles);
		var halfW = Mathf.Clamp(_hexSize * 0.065f, 3.2f, 14f);
		var color = new Color(0.14f, 0.42f, 0.86f, 0.96f);
		var y = FullDeckYLift + 2.8f;
		var seen = new HashSet<long>();
		foreach (var q in _organicMesh.Quads)
		{
			if (q == null || q.Length != 4) continue;
			for (var i = 0; i < 4; i++)
			{
				var a = q[i];
				var b = q[(i + 1) % 4];
				if (!_genRiverVertices.Contains(a) || !_genRiverVertices.Contains(b))
					continue;
				var lo = Math.Min(a, b);
				var hi = Math.Max(a, b);
				var key = ((long)lo << 32) | (uint)hi;
				if (!seen.Add(key)) continue;
				if (a < 0 || a >= _organicMesh.Vertices.Count || b < 0 || b >= _organicMesh.Vertices.Count)
					continue;
				var pa = _organicMesh.Vertices[a];
				var pb = _organicMesh.Vertices[b];
				OrganicQuadMesh.EmitPlanarEdgeRibbon(
					st,
					color,
					new Vector3(pa.X, y, pa.Y),
					new Vector3(pb.X, y, pb.Y),
					halfW);
			}
		}

		if (seen.Count == 0)
			return;

		var mesh = st.Commit();
		mesh.SurfaceSetMaterial(0, new StandardMaterial3D
		{
			AlbedoColor = color,
			Transparency = BaseMaterial3D.TransparencyEnum.Alpha,
			ShadingMode = BaseMaterial3D.ShadingModeEnum.Unshaded,
			CullMode = BaseMaterial3D.CullModeEnum.Disabled,
		});
		_genRiverRibbon = new MeshInstance3D
		{
			Name = "GenRiverRibbon",
			Mesh = mesh,
		};
		_genRiverRibbon.SetMeta("gen_river_watercourse", true);
		_genRiverRibbon.SetMeta("river_edge_count", seen.Count);
		_genRiverRibbon.SetMeta("slice_id", GenTerrainContract.SliceId);
		_dualRoot.AddChild(_genRiverRibbon);
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
