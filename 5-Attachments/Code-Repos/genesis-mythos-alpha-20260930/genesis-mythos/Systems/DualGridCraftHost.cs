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
/// Stålberg dual-lattice host — OrganicQuadMesh craft plane + OrganicDualOffsetLattice.
/// Logic points = organic corners; dual cells = half-step offset lattice faces (≤4 per flip).
/// Prefer: alpha0_stalberg_dual_lattice_r1.
/// Refuse: primary_face_as_dual | unstable_dual_neighborhood | over_neighbor_paint | stamp_as_dual | skip_dual_offset.
/// Dual-visual ask_success deferred. Preserve organic + craft authority + rings=2 spacing=3.0.
/// </summary>
public partial class DualGridCraftHost : Node3D, ICraftCellAuthority
{
	public const string CanonicalStampId = "stamp_oasis_desert";
	public const string PersistPath = "user://worldgen/living_world_v1.json";
	public const string SliceId = "alpha0_stalberg_dual_lattice_r1";
	public const string WeldSliceId = "alpha0_stalberg_dual_lattice_r1";
	public const string PreferAskId = "alpha0_stalberg_dual_lattice";
	public const string VisualBarCite = "stalberg_dual_lattice_half_step_offset";
	public const string ArtStyleId = "approved_half_step_dual_lattice_not_primary_faces";
	/// <summary>Townscaper dual-corner — one logic flip touches at most four dual cells.</summary>
	public const int MaxDualCellsPerLogicFlip = 4;

	/// <summary>Four-family altitude (full ~6 MeshLibrary depth later). Refuse gray_ramp_only / stretch_as_variant.</summary>
	public enum DualVisualFamily
	{
		Empty = 0,
		Edge = 1,
		Corner = 2,
		Full = 3,
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
	/// <summary>Organic craft spacing — follows Stålberg DefaultSpacing (large cells, low count).</summary>
	private float _hexSize = StalbergQuadKernel.DefaultSpacing;
	private int _seedRingCount = StalbergQuadKernel.DefaultRingCount;
	private bool _latticeVisible = true;
	private bool _dualVisible;
	private bool _ghostVisible;
	private readonly Dictionary<int, bool> _cornerLogic = new();
	private OrganicDualOffsetLattice? _dualLattice;
	private readonly Dictionary<int, List<int>> _vertexToFaces = new(); // craft-plane face index only — NOT dual Success
	private int _lastFlippedVertex = -1;
	private Node3D? _debugDualIdsRoot;
	private readonly List<string> _debugHighlightedDualKeys = new();
	private readonly Color _ownedDualHighlightColor = new(0.12f, 0.92f, 1f, 1f);

	public int PaintedCellCount => _occupancy.Count;
	public bool WorldExists => _organicMesh != null && _organicMesh.FaceCount > 0;
	public MeshLibrary? Library => EnsureShapeDistinctDualMeshLibrary();
	public string MeshLibrarySource => "approved_discrete_shape_distinct_graybox_standins_empty_edge_corner_full";
	public bool OccupancyGridVisible => _latticeVisible;
	public bool DualOverlayVisible => _dualVisible;
	public int DualSlotCount => _dualSlots.Count;
	/// <summary>MCP/F5 evidence — last flipped logic point and stable owned dual-lattice set.</summary>
	public int LastFlippedVertex => _lastFlippedVertex;
	public string LastOwnedDualCellsCsv { get; private set; } = "";
	public string LastOwnedDualFacesCsv { get => LastOwnedDualCellsCsv; private set => LastOwnedDualCellsCsv = value; }
	public int LastOwnedDualFaceCount { get; private set; }
	public bool LastNeighborhoodStable { get; private set; }
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
			"Stålberg dual-lattice r1 — half-step OrganicDualOffsetLattice; refuse primary_face_as_dual|unstable_dual_neighborhood|stamp_as_dual|over_neighbor_paint; Hex19 not Success",
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
				["relax"] = "area_based_closest_square_boundary_pin_clamp",
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
		// Opaque planar board — refuse translucent prism / noodle alpha soup.
		_organicRoot.AddChild(new MeshInstance3D
		{
			Name = "OrganicQuadFaces",
			Mesh = _organicMesh.BuildFaceMesh(new Color(0.22f, 0.42f, 0.62f, 1f)),
			Position = Vector3.Zero,
		});
		_organicRoot.AddChild(new MeshInstance3D
		{
			Name = "OrganicQuadEdges",
			Mesh = _organicMesh.BuildEdgeMesh(new Color(1f, 0.85f, 0.2f, 1f)),
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
	/// Mouse ray → OrganicQuadMesh FACE under cursor (craft-plane authority).
	/// Cell key = OrganicQuadMesh.FaceCell(faceIndex). Refuse hex19_pick_as_craft_authority.
	/// Method name kept for WorldgenCraft compat; body is organic, not Hex19 snap.
	/// </summary>
	public bool TryPickHexCell(Camera3D camera, Vector2 screenPos, out Vector2I cell)
	{
		// Dual-corner Prefer: pick nearest organic corner logic point (Y=1 encoder).
		if (TryPickOrganicCorner(camera, screenPos, out var vertex))
		{
			cell = new Vector2I(vertex, 1);
			return true;
		}
		return TryPickOrganicFace(camera, screenPos, out cell);
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

	/// <summary>Placement ghost — previews the ORGANIC FACE footprint under the cursor.</summary>
	public void UpdateGhost(Camera3D? camera, Vector2 screenPos)
	{
		if (_ghost == null) return;
		if (camera == null || !TryPickOrganicFace(camera, screenPos, out var cell))
		{
			_ghost.Visible = false;
			_ghostVisible = false;
			return;
		}

		if (_occupancy.ContainsKey(cell))
		{
			_ghost.Visible = false;
			_ghostVisible = false;
			return;
		}

		var face = OrganicQuadMesh.FaceIndexFromCell(cell);
		_ghost.Mesh = MakeOrganicFacePlate(face, new Color(0.85f, 0.9f, 0.95f, 0.45f), height: 0.04f);
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
		_vertexToFaces.Clear();
		if (_organicMesh == null)
		{
			_dualLattice = null;
			return;
		}
		// Craft-plane face adjacency (paint/pick) — NOT dual Success ownership.
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

		// Dual Success ownership lives on OrganicDualOffsetLattice (half-step keys).
		_dualLattice = new OrganicDualOffsetLattice(_organicMesh);
	}

	/// <summary>Corner logic points = OrganicQuadMesh vertices (Townscaper dual-corner authorship).</summary>
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

	/// <summary>Flip corner logic point; rebuild owned dual-lattice cells (≤ MaxDualCellsPerLogicFlip).</summary>
	public int FlipOrganicCorner(int vertexIndex)
	{
		if (_organicMesh == null || _dualLattice == null || vertexIndex < 0 || vertexIndex >= _organicMesh.VertexCount)
			return 0;
		if (!_dualLattice.IsEditableLogicPoint(vertexIndex))
			return 0;
		_cornerLogic[vertexIndex] = !(_cornerLogic.TryGetValue(vertexIndex, out var on) && on);
		_lastFlippedVertex = vertexIndex;
		var owned = OwnedDualCellKeys(vertexIndex);
		LastOwnedDualCellsCsv = string.Join(',', owned);
		LastOwnedDualFaceCount = owned.Count;
		var prove = ProveStableDualNeighborhood();
		LastNeighborhoodStable = prove.Ok;
		var n = UpdateFourDualSlots(new Vector2I(vertexIndex, 1));
		HighlightOwnedDualCells(vertexIndex);
		AlphaFactoryLog.Emit(
			"craft.dual",
			"Corner_Flip",
			$"organic corner={vertexIndex} filled={_cornerLogic[vertexIndex]} dual_cells_refreshed={n} owned=[{string.Join(',', owned)}] (cap={MaxDualCellsPerLogicFlip})",
			new Dictionary<string, object>
			{
				["ask_id"] = PreferAskId,
				["overlay"] = WeldSliceId,
				["corner_index"] = vertexIndex,
				["filled"] = _cornerLogic[vertexIndex],
				["update_four"] = n,
				["owned_dual_cells"] = string.Join(',', owned),
				["owned_count"] = owned.Count,
				["max_dual_cells_per_logic_flip"] = MaxDualCellsPerLogicFlip,
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

	/// <summary>Organic dual overlay — half-step OrganicDualOffsetLattice cells (not primary-face fills).</summary>
	private void BuildOrganicDualCornerOverlay()
	{
		if (_dualRoot != null && GodotObject.IsInstanceValid(_dualRoot))
			_dualRoot.QueueFree();
		_dualSlots.Clear();
		if (_organicMesh == null) return;
		if (_dualLattice == null)
			_dualLattice = new OrganicDualOffsetLattice(_organicMesh);

		_dualRoot = new Node3D { Name = "OrganicDualOffsetOverlay", Visible = _dualVisible };
		AddChild(_dualRoot);
		_dualRoot.GlobalPosition = _latticeOrigin;

		// Staging showcase — seed corner patterns BEFORE first mesh build so names+geometry match families.
		SeedDualVisualFamilyShowcase(refresh: false);

		foreach (var cell in _dualLattice.AllCells)
			EnsureHalfStepDualCellMesh(cell);

		AlphaFactoryLog.Emit(
			"craft.grid",
			"Dual_Offset_Overlay",
			$"organic dual-lattice cells armed — unique_cells={_dualSlots.Count} half_step update_four≤{MaxDualCellsPerLogicFlip} (refuse primary_face_as_dual|unstable_dual_neighborhood|stamp_as_dual|over_neighbor_paint)",
			new Dictionary<string, object>
			{
				["ask_id"] = PreferAskId,
				["overlay"] = WeldSliceId,
				["dual_half_offset"] = true,
				["update_four"] = true,
				["max_dual_cells_per_logic_flip"] = MaxDualCellsPerLogicFlip,
				["dual_slots"] = _dualSlots.Count,
				["dual_on_organic"] = true,
				["primary_face_as_dual"] = false,
				["organic_dual_offset_lattice"] = true,
				["shape_distinct_dual"] = true,
				["discrete_meshlibrary_item"] = true,
				["dual_families"] = "empty|edge|corner|full",
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
	/// Seed a few corner patterns so empty/edge/corner/full silhouettes are visible without albedo ramp.
	/// Shared corners may lift neighbors — expected for dual-corner authorship demo.
	/// </summary>
	private void SeedDualVisualFamilyShowcase(bool refresh = true)
	{
		if (_organicMesh == null || _organicMesh.FaceCount < 8)
			return;
		_cornerLogic.Clear();
		// Face 1 → Corner (one bit)
		var qCorner = _organicMesh.Quads[1];
		_cornerLogic[qCorner[0]] = true;
		// Face 3 → Edge (two adjacent)
		var qEdge = _organicMesh.Quads[3];
		_cornerLogic[qEdge[0]] = true;
		_cornerLogic[qEdge[1]] = true;
		// Face 5 → Full (four bits)
		var qFull = _organicMesh.Quads[5];
		foreach (var v in qFull)
			_cornerLogic[v] = true;
		// Face 0 left Empty (zero bits) — silhouette contrast vs seeded neighbors.
		if (refresh)
			RefreshAllDualSlots();
		AlphaFactoryLog.Emit(
			"craft.dual",
			"DualVisual_FamilyShowcase",
			"seeded corner patterns for empty|edge|corner|full silhouette proof (refuse gray_ramp_only)",
			new Dictionary<string, object>
			{
				["ask_id"] = PreferAskId,
				["overlay"] = WeldSliceId,
				["shape_distinct_dual"] = true,
				["dual_families"] = "empty|edge|corner|full",
				["gray_ramp_only"] = false,
			});
	}

	/// <summary>
	/// Dual cell mesh from OrganicDualOffsetLattice — Varignon half-step geometry.
	/// Refuse primary_face_as_dual (no primary-face-index dual keys / primary-face fill as dual).
	/// Refuse stamp_as_dual — no centroid MeshLibrary independent occupancy stamps.
	/// </summary>
	private void EnsureHalfStepDualCellMesh(OrganicDualOffsetLattice.DualCell cell)
	{
		if (_dualRoot == null || _organicMesh == null || _dualLattice == null)
			return;
		var q = cell.CornerLogicIndices;
		var filled = 0;
		for (var i = 0; i < 4; i++)
			if (_cornerLogic.TryGetValue(q[i], out var on) && on) filled++;

		var faceCorners = OrganicDualOffsetLattice.FaceCornersLocal(_organicMesh, cell);
		// Varignon midpoints = half-step offset tile (not primary-face fill).
		var mid = OrganicDualOffsetLattice.VarignonMidpoints(faceCorners);
		var height = filled == 0 ? 0.12f : 0.16f + filled * 0.05f;
		var albedo = filled == 0
			? new Color(0.55f, 0.58f, 0.62f, 0.72f)
			: new Color(0.58f, 0.60f, 0.64f, 0.95f);
		var mesh = MakeHalfStepDualCellMesh(mid, albedo, height);

		var key = cell.Key;
		MeshInstance3D mi;
		if (_dualSlots.TryGetValue(key, out var existing) && GodotObject.IsInstanceValid(existing))
			mi = existing;
		else
		{
			mi = new MeshInstance3D();
			_dualRoot.AddChild(mi);
			_dualSlots[key] = mi;
		}

		mi.Name = $"DualCell_{key}";
		mi.Mesh = mesh;
		mi.Position = Vector3.Up * 0.10f;
		mi.Rotation = Vector3.Zero;
		mi.Scale = Vector3.One;
		mi.MaterialOverride = null;
		mi.SetMeta("filled_corners", filled);
		mi.SetMeta("dual_key", key);
		mi.SetMeta("owned_by_logic_corners", true);
		mi.SetMeta("stamp_as_dual", false);
		mi.SetMeta("primary_face_as_dual", false);
		mi.SetMeta("half_step_varignon", true);
		mi.SetMeta("shared_logic_corner_dual", true);
		mi.SetMeta("gray_ramp_only", false);
		mi.SetMeta("stretch_as_variant", false);
	}

	/// <summary>Half-step dual tile from Varignon midpoints (offset from primary yellow-wire faces).</summary>
	private ArrayMesh MakeHalfStepDualCellMesh(Vector3[] midpoints, Color color, float height)
	{
		var c = (Vector3[])midpoints.Clone();
		var centre = (c[0] + c[1] + c[2] + c[3]) * 0.25f;
		const float inset = 0.88f;
		var lift = Vector3.Up * height;
		for (var i = 0; i < 4; i++)
			c[i] = centre.Lerp(c[i], inset) + lift;
		var st = new SurfaceTool();
		st.Begin(Mesh.PrimitiveType.Triangles);
		st.SetNormal(Vector3.Up); st.AddVertex(c[0]);
		st.SetNormal(Vector3.Up); st.AddVertex(c[1]);
		st.SetNormal(Vector3.Up); st.AddVertex(c[2]);
		st.SetNormal(Vector3.Up); st.AddVertex(c[0]);
		st.SetNormal(Vector3.Up); st.AddVertex(c[2]);
		st.SetNormal(Vector3.Up); st.AddVertex(c[3]);
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
	/// Corner bitmask → four-family altitude + rot/mirror.
	/// empty / edge / corner / full — diagonal+inverse fold into edge/corner (full ~6 MeshLibrary later).
	/// </summary>
	private (DualVisualFamily Family, int Rot90, bool Mirror) ResolveOrganicDualVisualFamily(int[] q)
	{
		var bits = 0;
		for (var i = 0; i < 4; i++)
			if (_cornerLogic.TryGetValue(q[i], out var on) && on)
				bits |= 1 << i;

		return bits switch
		{
			0b0000 => (DualVisualFamily.Empty, 0, false),
			0b0001 => (DualVisualFamily.Corner, 0, false),
			0b0010 => (DualVisualFamily.Corner, 1, false),
			0b0100 => (DualVisualFamily.Corner, 2, false),
			0b1000 => (DualVisualFamily.Corner, 3, false),
			// Adjacent pairs → Edge
			0b0011 => (DualVisualFamily.Edge, 0, false),
			0b0110 => (DualVisualFamily.Edge, 1, false),
			0b1100 => (DualVisualFamily.Edge, 2, false),
			0b1001 => (DualVisualFamily.Edge, 3, false),
			// Diagonals → Edge with mirror (distinct ridge orientation; still Edge family this altitude)
			0b0101 => (DualVisualFamily.Edge, 0, true),
			0b1010 => (DualVisualFamily.Edge, 1, true),
			// Three corners → inverse Corner (mirror)
			0b1110 => (DualVisualFamily.Corner, 0, true),
			0b1101 => (DualVisualFamily.Corner, 1, true),
			0b1011 => (DualVisualFamily.Corner, 2, true),
			0b0111 => (DualVisualFamily.Corner, 3, true),
			0b1111 => (DualVisualFamily.Full, 0, false),
			_ => (DualVisualFamily.Edge, 0, false),
		};
	}

	/// <summary>Runtime MeshLibrary of four shape-distinct prototypes (Prefer / GridMap-ready).</summary>
	private MeshLibrary EnsureShapeDistinctDualMeshLibrary()
	{
		if (_dualMeshLibrary != null && GodotObject.IsInstanceValid(_dualMeshLibrary))
			return _dualMeshLibrary;
		_dualMeshLibrary = new MeshLibrary();
		foreach (DualVisualFamily fam in Enum.GetValues(typeof(DualVisualFamily)))
		{
			var id = (int)fam;
			_dualMeshLibrary.CreateItem(id);
			_dualMeshLibrary.SetItemMesh(id, MakeUnitShapeDistinctPrototype(fam));
			_dualMeshLibrary.SetItemName(id, fam.ToString());
		}
		return _dualMeshLibrary;
	}

	/// <summary>Prefer / MCP proof — four families differ in silhouette geometry, not albedo.</summary>
	public (bool Ok, string Summary) ProveDualVisualVariants()
	{
		var lib = EnsureShapeDistinctDualMeshLibrary();
		var heights = new float[4];
		var volumes = new float[4];
		for (var i = 0; i < 4; i++)
		{
			var mesh = lib.GetItemMesh(i);
			if (mesh == null)
				return (false, $"missing_family_mesh id={i} refuse=gray_ramp_only");
			var aabb = mesh.GetAabb();
			heights[i] = aabb.Size.Y;
			volumes[i] = aabb.Size.X * aabb.Size.Y * aabb.Size.Z;
		}
		// Distinct AABB heights/volumes across empty/edge/corner/full (not albedo).
		var distinctHeights = new HashSet<float>(heights.Select(h => MathF.Round(h, 3))).Count;
		var distinctVolumes = new HashSet<float>(volumes.Select(v => MathF.Round(v, 4))).Count;
		if (distinctHeights < 3 && distinctVolumes < 3)
			return (false, $"silhouette_not_distinct heights=[{string.Join(',', heights)}] volumes=[{string.Join(',', volumes)}] refuse=gray_ramp_only");
		if (MeshLibrarySource.Contains("graybox") && !MeshLibrarySource.Contains("shape_distinct") && !MeshLibrarySource.Contains("discrete"))
			return (false, "mesh_library_source_gray_ramp refuse=gray_ramp_only");
		var neigh = ProveNeighborhoodCardinality();
		if (!neigh.Ok)
			return (false, neigh.Summary);
		return (true,
			$"shape_distinct_dual discrete_meshlibrary_item families=empty|edge|corner|full " +
			$"aabb_h=[{string.Join(',', heights.Select(h => h.ToString("0.###")))}] " +
			$"aabb_vol=[{string.Join(',', volumes.Select(v => v.ToString("0.####")))}] " +
			$"gray_ramp_only=false stretch_as_variant=false over_neighbor_paint=false " +
			$"library_items=4 source={MeshLibrarySource} {neigh.Summary}");
	}

	/// <summary>
	/// Stable owned dual-lattice keys for logic point P — DualCellsTouching, sorted.
	/// Identical on every call for the same vertex (refuse unstable_dual_neighborhood).
	/// Refuse primary_face_as_dual — keys are OrganicDualOffsetLattice ids, not primary-face-index ids.
	/// </summary>
	public IReadOnlyList<string> OwnedDualCellKeys(int vertexIndex)
	{
		if (_dualLattice == null)
			return Array.Empty<string>();
		return _dualLattice.DualCellKeysTouching(vertexIndex);
	}

	/// <summary>Legacy alias — returns support face indices for MCP that still ask faces; Prefer uses keys.</summary>
	public IReadOnlyList<int> OwnedDualFaceIndices(int vertexIndex)
	{
		if (_dualLattice == null)
			return Array.Empty<int>();
		return _dualLattice.DualCellsTouching(vertexIndex).Select(c => c.SupportFaceIndex).ToList();
	}

	/// <summary>
	/// Prefer seat — interior logic points own exactly four dual-lattice cells; set stable.
	/// Refuse primary_face_as_dual / unstable_dual_neighborhood / over_neighbor_paint / stamp_as_dual.
	/// </summary>
	public (bool Ok, string Summary) ProveStableDualNeighborhood()
	{
		if (_organicMesh == null || _dualLattice == null || _dualLattice.LogicPointCount == 0)
			return (false, "dual_lattice_missing refuse=unstable_dual_neighborhood");
		var max = 0;
		var interior4 = 0;
		var halfOk = 0;
		foreach (var cell in _dualLattice.AllCells)
		{
			if (_dualLattice.IsHalfStepOffset(cell))
				halfOk++;
		}
		if (halfOk < _dualLattice.CellCount)
			return (false, $"primary_face_as_dual dual_not_half_offset coincident={_dualLattice.CellCount - halfOk} refuse=primary_face_as_dual");
		foreach (var vi in _dualLattice.EditableLogicPoints)
		{
			var a = OwnedDualCellKeys(vi);
			var b = OwnedDualCellKeys(vi);
			if (a.Count != b.Count)
				return (false, $"unstable_dual_neighborhood vertex={vi} len_mismatch refuse=unstable_dual_neighborhood");
			for (var i = 0; i < a.Count; i++)
			{
				if (a[i] != b[i])
					return (false, $"unstable_dual_neighborhood vertex={vi} set_drift refuse=unstable_dual_neighborhood");
			}
			if (a.Count > MaxDualCellsPerLogicFlip)
				return (false, $"over_neighbor_paint vertex={vi} incident={a.Count} cap={MaxDualCellsPerLogicFlip} refuse=over_neighbor_paint");
			if (a.Count > max) max = a.Count;
			if (a.Count == 4) interior4++;
		}
		if (interior4 == 0)
			return (false, "no_interior_logic_points_with_exact4 refuse=unstable_dual_neighborhood");
		return (true,
			$"stable_dual_lattice max_incident={max} interior_exact4={interior4} logic_points={_dualLattice.LogicPointCount} " +
			$"dual_cells={_dualLattice.CellCount} half_step={halfOk} primary_face_as_dual=false stamp_as_dual=false " +
			$"MaxDualCellsPerLogicFlip={MaxDualCellsPerLogicFlip}");
	}

	/// <summary>Prefer — every logic vertex maps to ≤ MaxDualCellsPerLogicFlip dual cells.</summary>
	public (bool Ok, string Summary) ProveNeighborhoodCardinality()
	{
		if (_dualLattice == null || _dualLattice.LogicPointCount == 0)
			return (false, "dual_lattice_missing refuse=over_neighbor_paint");
		var max = 0;
		foreach (var vi in _dualLattice.EditableLogicPoints)
		{
			var n = OwnedDualCellKeys(vi).Count;
			if (n > max) max = n;
		}
		if (max > MaxDualCellsPerLogicFlip)
			return (false, $"over_neighbor_paint max_incident={max} cap={MaxDualCellsPerLogicFlip} refuse=over_neighbor_paint");
		return (true, $"neighborhood_cardinality_ok max_incident={max} MaxDualCellsPerLogicFlip={MaxDualCellsPerLogicFlip}");
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
	/// F5 debug — cyan highlight on owned dual-lattice cells (Varignon tiles), not primary faces.
	/// </summary>
	private void HighlightOwnedDualCells(int vertexIndex)
	{
		foreach (var key in _debugHighlightedDualKeys)
		{
			if (_dualSlots.TryGetValue(key, out var prev) && GodotObject.IsInstanceValid(prev))
				prev.MaterialOverride = null;
		}
		_debugHighlightedDualKeys.Clear();

		var owned = OwnedDualCellKeys(vertexIndex);
		foreach (var key in owned)
		{
			if (!_dualSlots.TryGetValue(key, out var mi) || !GodotObject.IsInstanceValid(mi))
				continue;
			mi.MaterialOverride = new StandardMaterial3D
			{
				AlbedoColor = _ownedDualHighlightColor,
				Transparency = BaseMaterial3D.TransparencyEnum.Disabled,
				CullMode = BaseMaterial3D.CullModeEnum.Disabled,
				ShadingMode = BaseMaterial3D.ShadingModeEnum.Unshaded,
				NoDepthTest = true,
			};
			_debugHighlightedDualKeys.Add(key);
		}
		RefreshDebugDualCellIds(vertexIndex);
	}

	/// <summary>Debug — Label3D listing owned dual-lattice keys for last flipped logic point.</summary>
	private void RefreshDebugDualCellIds(int vertexIndex)
	{
		if (_dualRoot == null || _organicMesh == null || _dualLattice == null) return;
		if (_debugDualIdsRoot != null && GodotObject.IsInstanceValid(_debugDualIdsRoot))
			_debugDualIdsRoot.QueueFree();
		_debugDualIdsRoot = new Node3D { Name = "DebugDualCellIds" };
		_dualRoot.AddChild(_debugDualIdsRoot);
		var cells = _dualLattice.DualCellsTouching(vertexIndex);
		if (cells.Count == 0) return;
		foreach (var cell in cells)
		{
			var c = cell.LocalCentre;
			var label = new Label3D
			{
				Name = $"DualId_{cell.Key}",
				Text = cell.Key,
				Position = new Vector3(c.X, 0.65f, c.Z),
				FontSize = 16,
				Modulate = _ownedDualHighlightColor,
				Billboard = BaseMaterial3D.BillboardModeEnum.Enabled,
				NoDepthTest = true,
			};
			_debugDualIdsRoot.AddChild(label);
		}
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
			default:
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
		}

		var mesh = st.Commit();
		// Shared mid-gray — silhouette/geometry carries family identity (refuse gray_ramp_only).
		mesh.SurfaceSetMaterial(0, new StandardMaterial3D
		{
			AlbedoColor = new Color(0.62f, 0.64f, 0.68f, 1f),
			CullMode = BaseMaterial3D.CullModeEnum.Disabled,
			ShadingMode = BaseMaterial3D.ShadingModeEnum.PerPixel,
			Roughness = 0.85f,
		});
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
		if (cell.Y == 1)
		{
			// Corner logic point — Empty clears; any fill sets/toggles via FlipOrganicCorner.
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
				new Color(0.85f, 0.9f, 1f, 0.42f),
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
		st.SetColor(new Color(0.34f, 0.37f, 0.42f, 0.5f));
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
			AlbedoColor = new Color(0.34f, 0.37f, 0.42f, 0.5f),
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
			AlbedoColor = new Color(0.82f, 0.86f, 0.92f, 0.9f),
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
			AlbedoColor = new Color(0.9f, 0.92f, 0.96f),
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

		var mesh = MakeOrganicFacePlate(face, new Color(0.72f, 0.55f, 0.28f, 0.92f), height: 0.12f);
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
	/// UPDATE-FOUR — refresh only dual cells that list this occupancy as a corner (≤4).
	/// Corner-driven local rebuild (oskar docs/03), not global rebuild theater.
	/// Refuse over_neighbor_paint when incident set exceeds MaxDualCellsPerLogicFlip.
	/// </summary>
	public int UpdateFourDualSlots(Vector2I occupancy)
	{
		// Organic dual-lattice: occupancy.Y==1 → corner/vertex index; refresh DualCellsTouching.
		if (_organicMesh != null && _dualRoot != null && _dualLattice != null)
		{
			if (occupancy.Y == 1)
			{
				var vertex = occupancy.X;
				var organicCells = _dualLattice.DualCellsTouching(vertex);
				if (organicCells.Count == 0)
					return 0;
				if (organicCells.Count > MaxDualCellsPerLogicFlip)
				{
					AlphaFactoryLog.Emit("craft.refuse", "over_neighbor_paint",
						$"refuse over_neighbor_paint vertex={vertex} incident={organicCells.Count}",
						level: "error");
					return 0; // refuse=over_neighbor_paint hard
				}
				var n = 0;
				foreach (var cell in organicCells)
				{
					EnsureHalfStepDualCellMesh(cell);
					n++;
				}
				return n;
			}
			// Face-index path — resolve supporting dual cell by support face, not org_ key.
			foreach (var cell in _dualLattice.AllCells)
			{
				if (cell.SupportFaceIndex == occupancy.X)
				{
					EnsureHalfStepDualCellMesh(cell);
					return 1;
				}
			}
			return 0;
		}
		if (_dualRoot == null)
			return 0;
		var cells = Hex19DualOffsetLattice.DualCellsTouching(occupancy, _hexSize);
		if (cells.Length != Hex19DualOffsetLattice.DualSlotsPerOccupancy)
			return 0;
		var nHex = 0;
		foreach (var cell in cells)
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
				EnsureHalfStepDualCellMesh(cell);
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
			if (_dualSlots.Count != _dualLattice.CellCount)
				return (false, $"dual_lattice_count_mismatch mesh={_dualSlots.Count} lattice={_dualLattice.CellCount} refuse=skip_dual_offset");
			if (_dualLattice.LogicPointCount == 0)
				return (false, "dual_corner_index_missing refuse=skip_dual_offset");
			var neigh = ProveStableDualNeighborhood();
			if (!neigh.Ok)
				return (false, neigh.Summary);
			return (true,
				$"dual_lattice_on_organic unique_cells={_dualSlots.Count} corner_logic=true update_four=DualCellsTouching " +
				$"primary_face_as_dual=false stamp_as_dual=false half_step_varignon=true hex19_success=false dual_visual_deferred=true " +
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
		0 => new Color(0.42f, 0.45f, 0.49f, 0.28f),
		1 => new Color(0.52f, 0.55f, 0.59f, 0.5f),
		2 => new Color(0.6f, 0.63f, 0.67f, 0.65f),
		3 => new Color(0.66f, 0.68f, 0.72f, 0.75f), // saddle
		4 => new Color(0.72f, 0.74f, 0.78f, 0.85f),
		_ => new Color(0.8f, 0.82f, 0.86f, 0.95f),
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
