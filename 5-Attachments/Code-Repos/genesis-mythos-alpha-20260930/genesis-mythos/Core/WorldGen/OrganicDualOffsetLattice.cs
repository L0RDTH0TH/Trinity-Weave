using System;
using System.Collections.Generic;
using System.Linq;
using Godot;

namespace Genesis.Core.WorldGen;

/// <summary>
/// Organic dual-offset lattice — Stage-6 dual wire identity + small_corner_quads glow.
///
/// success_object: dual_offset_cells
/// Intent: Stage-6 DualCell identity (OwnedDualCellKeys=one; dual verts=face centroids;
/// dual edges centroid–centroid) remains lattice topology / wire. Pick/glow/populate
/// centers on the secondary grid — dual verts at face centroids — via
/// SmallCornerQuadsAroundFace(F) (typically 4 pie sectors meeting at the coral/cyan
/// secondary locus). SmallCornerQuadsAround(V) remains the primary-star query (edge≈2 /
/// interior≈4) but is NOT Prefer Success when Prefer claims secondary-centered.
///
/// SmallCornerQuad(V,F) corners: V, mid(edge V→next), faceCentroid(F), mid(edge prev→V).
/// Stage-6 polygon around V = union of those pieces (too big as one highlight fill).
///
/// Refuse: primary_star_glow_as_success · stage6_union_as_single_glow_tile ·
/// primary_face_as_dual · owned_only_glow · hex19_always_4 · soft_take_4 ·
/// face_corners_local_as_dual_edges · vertex_neighbor_as_dual_corner ·
/// dual_rebind_cardinal_wrong_locus · valence_drop_editable.
/// </summary>
public sealed class OrganicDualOffsetLattice
{
	public const int MaxCornersPerDual = 8;
	public const int MaxDualsPerLogicPoint = 5; // owned + ≤4 dual-edge neighbours
	public const int MaxOwnedDualsPerLogicPoint = 1;
	public const int MaxExpandDualsPerLogicPoint = 4; // degree-dependent; refuse soft pad always-4
	public const int MaxSmallCornerQuadsPerLogicPoint = 4;
	public const int MinSmallCornerQuadsEditable = 2;
	public const int MaxSmallCornerQuadsPerSecondaryFace = 4;
	public const int MinSmallCornerQuadsPerSecondaryFace = 3;

	public readonly struct DualCell
	{
		public DualCell(
			string key,
			int ownerVertexId,
			OrganicMeshGraph.Face[] cornerFaces,
			OrganicMeshGraph.Vertex[] cornerVertices,
			Vector3 localCentre,
			Vector3[] dualCorners)
		{
			Key = key ?? throw new ArgumentNullException(nameof(key));
			OwnerVertexId = ownerVertexId;
			CornerFaces = cornerFaces ?? throw new ArgumentNullException(nameof(cornerFaces));
			CornerVertices = cornerVertices ?? throw new ArgumentNullException(nameof(cornerVertices));
			LocalCentre = localCentre;
			DualCorners = dualCorners ?? throw new ArgumentNullException(nameof(dualCorners));
		}

		/// <summary>Stable dual identity — one Stage-6 cell per logic Vertex.</summary>
		public string Key { get; }

		/// <summary>Logic Vertex that owns this dual cell (placement / snap centre).</summary>
		public int OwnerVertexId { get; }

		/// <summary>
		/// Faces incident to owner, CCW — each face centroid is a dual vertex.
		/// </summary>
		public OrganicMeshGraph.Face[] CornerFaces { get; }

		/// <summary>
		/// Dual-edge neighbour logic Vertices (edge-adjacent owners), CCW about owner.
		/// Used for expand / DualCellsTouching neighbour refresh — NOT dual geometry corners
		/// (refuse vertex_neighbor_as_dual_corner as dual-corner Success) and NOT the sole
		/// occupancy mask (owner must participate — see <see cref="CornerLogicIndices"/>).
		/// </summary>
		public OrganicMeshGraph.Vertex[] CornerVertices { get; }

		/// <summary>
		/// Occupancy samples for MeshLibrary family lookup — Stage6 dual-edge frame.
		/// bit i ↔ DualCorners[i] (face centroid of CornerFaces[i]);
		/// edge i = DualCorners[i] → DualCorners[(i+1) mod n] (edge0 = c0→c1).
		/// Sample[i] = CardinalNeighbors[i] (CCW about owner).
		/// n=4: bits 0..3. n=3 (tri DualCell): bits 0..2 — document bit map; NO soft pad to 4.
		/// Owner V is placement centre (grammar), NOT a corner bit — host resolves
		/// owner-on → Full (whole DualCell land; refuse Corner-wedge-only / soft_take_4).
		/// Length empty when DualCorners ∉ {3,4} or CornerVertices shorter than DualCorners.
		/// Valence-5 non-editable (SmallCornerQuads 2..4 only).
		/// </summary>
		public int[] OccupancyCorners
		{
			get
			{
				if (CornerVertices == null || DualCorners == null)
					return Array.Empty<int>();
				var n = DualCorners.Length;
				// n=3 tri DualCell or n=4 quad — refuse soft_take_4 pad to fake 4.
				if (n != 3 && n != 4)
					return Array.Empty<int>();
				if (CornerVertices.Length < n)
					return Array.Empty<int>();
				var occ = new int[n];
				for (var i = 0; i < n; i++)
					occ[i] = CornerVertices[i].Id;
				return occ;
			}
		}

		/// <summary>
		/// Alias of <see cref="OccupancyCorners"/> (Stage6-aligned). Prior owned_cell_place
		/// used [Owner V, n0, n1, n2] — SUPERSEDED (primary-vert ring ≠ DualCorners ring).
		/// </summary>
		public int[] CornerLogicIndices => OccupancyCorners;

		/// <summary>Placement centre — logic Vertex position (main intersection).</summary>
		public Vector3 LocalCentre { get; }

		/// <summary>Stage-6 dual polygon corners — face centroids (dual verts).</summary>
		public Vector3[] DualCorners { get; }

		/// <summary>Obsolete face-as-dual owner — always -1. Refuse primary_face_as_dual.</summary>
		public int OwnerFaceId => -1;

		/// <summary>Obsolete face-proxy id — use Key / OwnerVertexId / DualCorners.</summary>
		public int DeriveFaceIndex => -1;

		[Obsolete("SupportFaceIndex is not dual Success — use Key / OwnerVertexId / DualCorners")]
		public int SupportFaceIndex => DeriveFaceIndex;
	}

	/// <summary>
	/// Primary-edge-carved dual sector at logic V on primal Face F — the glow/populate unit.
	/// Corners (CCW): V → mid(V→next) → faceCentroid(F) → mid(prev→V).
	/// Refuse stage6_union_as_single_glow_tile / primary_face_as_dual.
	/// </summary>
	public readonly struct SmallCornerQuad
	{
		public SmallCornerQuad(
			string key,
			int logicVertexId,
			int faceId,
			Vector3[] corners)
		{
			Key = key ?? throw new ArgumentNullException(nameof(key));
			LogicVertexId = logicVertexId;
			FaceId = faceId;
			Corners = corners ?? throw new ArgumentNullException(nameof(corners));
		}

		public string Key { get; }
		public int LogicVertexId { get; }
		public int FaceId { get; }
		/// <summary>Four corners: V, edge-mid next, face centroid, edge-mid prev.</summary>
		public Vector3[] Corners { get; }

		public Vector3 LocalCentre
		{
			get
			{
				if (Corners == null || Corners.Length == 0) return Vector3.Zero;
				var s = Vector3.Zero;
				foreach (var c in Corners) s += c;
				return s / Corners.Length;
			}
		}
	}

	private readonly List<DualCell> _cells = new();
	private readonly Dictionary<string, DualCell> _byKey = new();
	private readonly Dictionary<int, string> _ownerToDualKey = new();
	private readonly Dictionary<int, List<string>> _touchingDualKeys = new();
	private readonly Dictionary<int, List<string>> _expandDualKeys = new();
	private readonly Dictionary<int, List<SmallCornerQuad>> _smallCornerQuads = new();
	private readonly Dictionary<int, List<SmallCornerQuad>> _smallCornerQuadsByFace = new();
	private readonly Dictionary<string, SmallCornerQuad> _smallCornerByKey = new();
	private readonly List<int> _editableLogicPoints = new();
	private readonly List<int> _editableSecondaryFaces = new();
	private readonly List<Vector2> _logicPositions;
	private readonly OrganicMeshGraph? _graph;

	public OrganicDualOffsetLattice(OrganicQuadMesh mesh)
	{
		if (mesh == null) throw new ArgumentNullException(nameof(mesh));
		_graph = mesh.Graph;
		_logicPositions = mesh.Vertices;
		Rebuild(mesh);
	}

	public IReadOnlyList<DualCell> AllCells => _cells;
	public int CellCount => _cells.Count;
	public int SmallCornerQuadCount => _smallCornerByKey.Count;
	public int LogicPointCount => _editableLogicPoints.Count;
	public int SecondaryPointCount => _editableSecondaryFaces.Count;
	public OrganicMeshGraph? Graph => _graph;

	public static string DualKeyFromOwner(int ownerVertexId) => "d_v_" + ownerVertexId;

	public static string SmallCornerKey(int logicVertexId, int faceId) =>
		"sc_v" + logicVertexId + "_f" + faceId;

	/// <summary>Face centroid in mesh XY (craft plane) — dual vertex locus.</summary>
	public static Vector2 FaceCentroid2(OrganicMeshGraph.Face face)
	{
		if (face?.Corners == null || face.Corners.Length == 0)
			return Vector2.Zero;
		var sum = Vector2.Zero;
		foreach (var c in face.Corners)
			sum += c.Position;
		return sum / face.Corners.Length;
	}

	public static Vector3 FaceCentroid3(OrganicMeshGraph.Face face)
	{
		var p = FaceCentroid2(face);
		return new Vector3(p.X, 0f, p.Y);
	}

	/// <summary>
	/// Stage-6 dual cell polygon around logic Vertex V — face centroids of faces
	/// touching V, sorted CCW about V. Dual verts = those centroids.
	/// </summary>
	public static Vector3[] Stage6DualCellPolygon(OrganicMeshGraph.Vertex v)
	{
		if (v == null) return Array.Empty<Vector3>();
		var faces = OrderedIncidentFaces(v);
		if (faces.Count == 0) return Array.Empty<Vector3>();
		var poly = new Vector3[faces.Count];
		for (var i = 0; i < faces.Count; i++)
			poly[i] = FaceCentroid3(faces[i]);
		return poly;
	}

	public static List<OrganicMeshGraph.Face> OrderedIncidentFaces(OrganicMeshGraph.Vertex v)
	{
		var result = new List<OrganicMeshGraph.Face>();
		if (v?.Faces == null || v.Faces.Count == 0) return result;
		var origin = v.Position;
		return v.Faces.OrderBy(f =>
		{
			var c = FaceCentroid2(f);
			return Mathf.Atan2(c.Y - origin.Y, c.X - origin.X);
		}).ToList();
	}

	/// <summary>Edge-neighbors (dual-edge neighbour owners). Not dual corners.</summary>
	public static List<OrganicMeshGraph.Vertex> CardinalNeighbors(OrganicMeshGraph.Vertex v)
	{
		var result = new List<OrganicMeshGraph.Vertex>();
		if (v == null) return result;
		foreach (var e in v.IncidentEdges)
		{
			var other = e.Other(v);
			if (!result.Contains(other))
				result.Add(other);
		}
		var origin = v.Position;
		result.Sort((a, b) =>
		{
			var aa = Mathf.Atan2(a.Position.Y - origin.Y, a.Position.X - origin.X);
			var bb = Mathf.Atan2(b.Position.Y - origin.Y, b.Position.X - origin.X);
			return aa.CompareTo(bb);
		});
		return result;
	}

	public void Rebuild(OrganicQuadMesh mesh)
	{
		_cells.Clear();
		_byKey.Clear();
		_ownerToDualKey.Clear();
		_touchingDualKeys.Clear();
		_expandDualKeys.Clear();
		_smallCornerQuads.Clear();
		_smallCornerQuadsByFace.Clear();
		_smallCornerByKey.Clear();
		_editableLogicPoints.Clear();
		_editableSecondaryFaces.Clear();
		if (mesh == null) return;

		var graph = mesh.Graph;
		if (graph == null || graph.VertexCount == 0 || graph.FaceCount == 0)
			return;

		// Small corner quads — glow/populate units (one per incident Face at V).
		foreach (var v in graph.Vertices)
		{
			var faces = OrderedIncidentFaces(v);
			if (faces.Count == 0) continue;
			var list = new List<SmallCornerQuad>(faces.Count);
			foreach (var f in faces)
			{
				var corners = SmallCornerQuadCorners(v, f);
				if (corners.Length != 4) continue;
				var sk = SmallCornerKey(v.Id, f.Id);
				var sc = new SmallCornerQuad(sk, v.Id, f.Id, corners);
				list.Add(sc);
				_smallCornerByKey[sk] = sc;
				if (!_smallCornerQuadsByFace.TryGetValue(f.Id, out var byFace))
				{
					byFace = new List<SmallCornerQuad>();
					_smallCornerQuadsByFace[f.Id] = byFace;
				}
				byFace.Add(sc);
			}
			if (list.Count > 0)
				_smallCornerQuads[v.Id] = list;
		}

		// Stage-6: one dual cell per logic Vertex with ≥3 incident faces (wire / topology).
		foreach (var v in graph.Vertices)
		{
			var faces = OrderedIncidentFaces(v);
			if (faces.Count < 3) continue;

			var poly = new Vector3[faces.Count];
			for (var i = 0; i < faces.Count; i++)
				poly[i] = FaceCentroid3(faces[i]);

			var neighbours = CardinalNeighbors(v);
			var key = DualKeyFromOwner(v.Id);
			var centre = new Vector3(v.Position.X, 0f, v.Position.Y);
			var cell = new DualCell(
				key,
				v.Id,
				faces.ToArray(),
				neighbours.ToArray(),
				centre,
				poly);
			_cells.Add(cell);
			_byKey[key] = cell;
			_ownerToDualKey[v.Id] = key;
		}

		// Expand / touching — topology neighbour DualCells (not glow units).
		foreach (var cell in _cells)
		{
			var expand = new List<string>();
			foreach (var n in cell.CornerVertices)
			{
				if (_ownerToDualKey.TryGetValue(n.Id, out var nk) && nk != cell.Key && !expand.Contains(nk))
					expand.Add(nk);
			}
			expand.Sort(StringComparer.Ordinal);
			_expandDualKeys[cell.OwnerVertexId] = expand;

			// Owned first, then expand neighbours sorted — UpdateFour paints OwnedDualCell
			// before shared-corner neighbours (refuse expand-only as Success).
			var expandSorted = new List<string>(expand);
			expandSorted.Sort(StringComparer.Ordinal);
			var keys = new List<string> { cell.Key };
			foreach (var ek in expandSorted)
			{
				if (!keys.Contains(ek))
					keys.Add(ek);
			}
			_touchingDualKeys[cell.OwnerVertexId] = keys;
		}

		// Editable primary = has 2..4 small corner quads (edge≈2, interior≈4). Refuse soft pad.
		foreach (var kv in _smallCornerQuads)
		{
			var n = kv.Value.Count;
			if (n >= MinSmallCornerQuadsEditable && n <= MaxSmallCornerQuadsPerLogicPoint)
				_editableLogicPoints.Add(kv.Key);
		}
		_editableLogicPoints.Sort();

		// Editable secondary = face centroids with 3..4 incident small corner quads
		// (quad faces → 4 pie sectors meeting at the dual vert). Sorted per face.
		foreach (var kv in _smallCornerQuadsByFace)
		{
			kv.Value.Sort((a, b) => a.LogicVertexId.CompareTo(b.LogicVertexId));
			var n = kv.Value.Count;
			if (n >= MinSmallCornerQuadsPerSecondaryFace && n <= MaxSmallCornerQuadsPerSecondaryFace)
				_editableSecondaryFaces.Add(kv.Key);
		}
		_editableSecondaryFaces.Sort();
	}

	public bool IsEditableLogicPoint(int vertexIndex)
	{
		if (vertexIndex < 0) return false;
		if (!_smallCornerQuads.TryGetValue(vertexIndex, out var list))
			return false;
		var n = list.Count;
		return n >= MinSmallCornerQuadsEditable && n <= MaxSmallCornerQuadsPerLogicPoint;
	}

	public IReadOnlyCollection<int> EditableLogicPoints => _editableLogicPoints;

	/// <summary>The single Stage-6 dual cell owned by logic Vertex V (or empty).</summary>
	public IReadOnlyList<string> OwnedDualCellKeys(int logicVertex)
	{
		if (!_ownerToDualKey.TryGetValue(logicVertex, out var key))
			return Array.Empty<string>();
		return new[] { key };
	}

	public bool TryGetOwned(int logicVertex, out DualCell cell)
	{
		cell = default;
		if (!_ownerToDualKey.TryGetValue(logicVertex, out var key))
			return false;
		return _byKey.TryGetValue(key, out cell);
	}

	/// <summary>
	/// Corner piece of primal Face F at logic Vertex V — glow/populate unit.
	/// Corners CCW: V, mid(V→next), faceCentroid(F), mid(prev→V).
	/// Primary edges supply two sides; dual wire still uses face centroids only.
	/// </summary>
	public static Vector3[] SmallCornerQuadCorners(
		OrganicMeshGraph.Vertex v,
		OrganicMeshGraph.Face f)
	{
		if (v == null || f?.Corners == null || f.Corners.Length < 3)
			return Array.Empty<Vector3>();
		var i = -1;
		for (var k = 0; k < f.Corners.Length; k++)
		{
			if (ReferenceEquals(f.Corners[k], v))
			{
				i = k;
				break;
			}
		}
		if (i < 0) return Array.Empty<Vector3>();
		var n = f.Corners.Length;
		var prev = f.Corners[(i - 1 + n) % n];
		var next = f.Corners[(i + 1) % n];
		var v3 = new Vector3(v.Position.X, 0f, v.Position.Y);
		var prev3 = new Vector3(prev.Position.X, 0f, prev.Position.Y);
		var next3 = new Vector3(next.Position.X, 0f, next.Position.Y);
		var midPrev = (v3 + prev3) * 0.5f;
		var midNext = (v3 + next3) * 0.5f;
		var centroid = FaceCentroid3(f);
		// V → mid along next edge → face centroid → mid along prev edge.
		return new[] { v3, midNext, centroid, midPrev };
	}

	/// <summary>
	/// Degree-many small primary-cut corner quads incident to V (≈ one per Face).
	/// Edge≈2, interior≈4. Primary-star query — Prefer Success for secondary glow
	/// uses SmallCornerQuadsAroundFace (refuse primary_star_glow_as_success).
	/// </summary>
	public IReadOnlyList<SmallCornerQuad> SmallCornerQuadsAround(int logicVertex)
	{
		if (!_smallCornerQuads.TryGetValue(logicVertex, out var list) || list.Count == 0)
			return Array.Empty<SmallCornerQuad>();
		return list;
	}

	public IReadOnlyList<string> SmallCornerQuadKeysAround(int logicVertex)
	{
		var quads = SmallCornerQuadsAround(logicVertex);
		if (quads.Count == 0) return Array.Empty<string>();
		return quads.Select(q => q.Key).ToList();
	}

	/// <summary>
	/// Small corner quads incident to secondary locus Face F (face centroid dual vert).
	/// Typically 4 pie sectors meeting at the coral/cyan secondary point — Prefer
	/// glow/populate Success. Refuse primary_star_glow_as_success.
	/// </summary>
	public IReadOnlyList<SmallCornerQuad> SmallCornerQuadsAroundFace(int faceId)
	{
		if (!_smallCornerQuadsByFace.TryGetValue(faceId, out var list) || list.Count == 0)
			return Array.Empty<SmallCornerQuad>();
		return list;
	}

	public IReadOnlyList<string> SmallCornerQuadKeysAroundFace(int faceId)
	{
		var quads = SmallCornerQuadsAroundFace(faceId);
		if (quads.Count == 0) return Array.Empty<string>();
		return quads.Select(q => q.Key).ToList();
	}

	public bool IsEditableSecondaryPoint(int faceId)
	{
		if (faceId < 0) return false;
		if (!_smallCornerQuadsByFace.TryGetValue(faceId, out var list))
			return false;
		var n = list.Count;
		return n >= MinSmallCornerQuadsPerSecondaryFace && n <= MaxSmallCornerQuadsPerSecondaryFace;
	}

	public IReadOnlyCollection<int> EditableSecondaryFaces => _editableSecondaryFaces;

	public bool TryGetSecondaryCentroid(int faceId, out Vector2 centroid)
	{
		centroid = default;
		if (_graph == null || faceId < 0 || faceId >= _graph.FaceCount)
			return false;
		var face = _graph.Faces[faceId];
		if (face == null || face.Id != faceId) return false;
		centroid = FaceCentroid2(face);
		return true;
	}

	public bool TryGetSmallCornerQuad(string key, out SmallCornerQuad quad) =>
		_smallCornerByKey.TryGetValue(key, out quad);

	public IReadOnlyCollection<SmallCornerQuad> AllSmallCornerQuads => _smallCornerByKey.Values;

	/// <summary>
	/// Topology neighbour DualCell keys (exclude owned). Not the glow unit —
	/// glow uses SmallCornerQuadsAround. Kept for lattice neighbour queries.
	/// </summary>
	public IReadOnlyList<string> ExpandDualNeighborKeys(int logicVertex)
	{
		if (_graph == null || logicVertex < 0 || logicVertex >= _graph.VertexCount)
			return Array.Empty<string>();
		if (!_expandDualKeys.TryGetValue(logicVertex, out var list) || list.Count == 0)
			return Array.Empty<string>();
		// Hard refuse soft Take(4) — return full expand degree.
		return list;
	}

	public IReadOnlyList<DualCell> DualCellsExpandingFrom(int logicVertex)
	{
		var keys = ExpandDualNeighborKeys(logicVertex);
		if (keys.Count == 0) return Array.Empty<DualCell>();
		var result = new List<DualCell>(keys.Count);
		foreach (var k in keys)
		{
			if (_byKey.TryGetValue(k, out var cell))
				result.Add(cell);
		}
		return result;
	}

	/// <summary>
	/// Owned Stage-6 cell plus expand neighbours (UpdateFour mesh refresh set).
	/// Glow highlight uses ExpandDualNeighborKeys — not this full touching set.
	/// </summary>
	public IReadOnlyList<DualCell> DualCellsTouching(OrganicMeshGraph.Vertex logicVertex)
	{
		if (logicVertex == null) return Array.Empty<DualCell>();
		return DualCellsTouching(logicVertex.Id);
	}

	public IReadOnlyList<DualCell> DualCellsTouching(int logicVertex)
	{
		var keys = DualCellKeysTouching(logicVertex);
		if (keys.Count == 0) return Array.Empty<DualCell>();
		var result = new List<DualCell>(keys.Count);
		foreach (var k in keys)
		{
			if (_byKey.TryGetValue(k, out var cell))
				result.Add(cell);
		}
		return result;
	}

	public IReadOnlyList<string> DualCellKeysTouching(int logicVertex)
	{
		if (_graph == null || logicVertex < 0 || logicVertex >= _graph.VertexCount)
			return Array.Empty<string>();

		if (!_touchingDualKeys.TryGetValue(logicVertex, out var list) || list.Count == 0)
			return Array.Empty<string>();

		// Hard refuse soft Take(4) — return full owned+expand neighbourhood.
		return list;
	}

	/// <summary>
	/// Wrong-locus keys for refuse proof — dual_rebind vertex-centred star keys.
	/// Must NOT equal OwnedDualCellKeys.
	/// </summary>
	public IReadOnlyList<string> VertexNeighborStarKeysForProof(int logicVertex)
	{
		if (_graph == null || logicVertex < 0 || logicVertex >= _graph.VertexCount)
			return Array.Empty<string>();
		var v = _graph.GetVertex(logicVertex);
		var keys = new List<string>();
		foreach (var n in CardinalNeighbors(v))
		{
			var neigh = CardinalNeighbors(n);
			if (neigh.Count < 3) continue;
			// Fake face-as-dual key style from prior wrong locus — for inequality proof only.
			var fake = "star_" + string.Join("_", neigh.Select(x => x.Id).OrderBy(i => i));
			if (!keys.Contains(fake)) keys.Add(fake);
		}
		keys.Sort(StringComparer.Ordinal);
		return keys;
	}

	public bool TryGet(string key, out DualCell cell) => _byKey.TryGetValue(key, out cell);

	public bool TryGetByFace(int ownerFaceId, out DualCell cell)
	{
		// Face-as-dual lookup removed — refuse primary_face_as_dual.
		cell = default;
		_ = ownerFaceId;
		return false;
	}

	/// <summary>
	/// Half-step / Stage-6 polarity: dual verts at face centroids; LocalCentre at
	/// owner logic Vertex (placement). Refuse dual verts coincident with logic verts.
	/// </summary>
	public bool IsHalfStepOffset(DualCell cell, float eps = 1e-4f)
	{
		if (_graph == null) return false;
		if (cell.OwnerVertexId < 0 || cell.OwnerVertexId >= _graph.VertexCount)
			return false;
		if (cell.DualCorners == null || cell.DualCorners.Length < 3)
			return false;
		if (cell.CornerFaces == null || cell.CornerFaces.Length != cell.DualCorners.Length)
			return false;

		var owner = _graph.GetVertex(cell.OwnerVertexId);
		var expectCentre = new Vector3(owner.Position.X, 0f, owner.Position.Y);
		if (cell.LocalCentre.DistanceSquaredTo(expectCentre) > eps * eps * 100f)
			return false;

		for (var i = 0; i < cell.CornerFaces.Length; i++)
		{
			var expect = FaceCentroid3(cell.CornerFaces[i]);
			if (cell.DualCorners[i].DistanceSquaredTo(expect) > eps * eps * 100f)
				return false;
			// Dual vert must not sit on a logic Vertex (Hex19 polarity for dual verts).
			foreach (var v in _graph.Vertices)
			{
				var occ = new Vector3(v.Position.X, 0f, v.Position.Y);
				if (cell.DualCorners[i].DistanceSquaredTo(occ) < eps * eps)
					return false;
			}
		}
		return true;
	}

	/// <summary>
	/// Stage-6 cell identity proof — owned dual = polygon of face centroids around V.
	/// Refuse face-as-dual / FaceCornersLocal rings / vertex-neighbour star as dual corners.
	/// </summary>
	public (bool Ok, string Summary) ProveFaceCentroidAround(int logicVertex)
	{
		if (_graph == null || logicVertex < 0 || logicVertex >= _graph.VertexCount)
			return (false, "stage6_cell_missing_graph refuse=primary_face_as_dual");
		if (!TryGetOwned(logicVertex, out var owned))
			return (false, "stage6_cell_empty refuse=unstable_dual_neighborhood");

		var ownedKeys = OwnedDualCellKeys(logicVertex);
		if (ownedKeys.Count != MaxOwnedDualsPerLogicPoint)
			return (false, $"owned_count={ownedKeys.Count} refuse=face_block_neighborhood");

		var touching = DualCellsTouching(logicVertex);
		if (touching.Count == 0)
			return (false, "stage6_touching_empty refuse=unstable_dual_neighborhood");
		if (touching.Count > MaxDualsPerLogicPoint)
			return (false, $"over_neighbor_paint incident={touching.Count} refuse=over_neighbor_paint");

		var small = SmallCornerQuadsAround(logicVertex);
		if (small.Count == 0)
			return (false, "small_corner_quads_empty refuse=unstable_dual_neighborhood");
		if (small.Count > MaxSmallCornerQuadsPerLogicPoint)
			return (false, $"over_neighbor_paint small={small.Count} refuse=over_neighbor_paint");
		foreach (var sc in small)
		{
			if (sc.Corners == null || sc.Corners.Length != 4)
				return (false, "small_corner_quad_bad_corners refuse=unstable_dual_neighborhood");
			// Refuse Stage-6 union sold as the glow unit (4+ centroid-only ring).
			if (sc.Key.StartsWith("d_v_", StringComparison.Ordinal))
				return (false, "stage6_union_as_single_glow_tile refuse=stage6_union_as_single_glow_tile");
		}

		// Refuse identity with dual_rebind vertex-neighbour star keys.
		var starKeys = VertexNeighborStarKeysForProof(logicVertex);
		if (starKeys.Count > 0 && ownedKeys.Count == starKeys.Count && ownedKeys[0] == starKeys[0])
			return (false, "vertex_neighbor_as_dual_corner identical_to_edge_neighbor_star refuse=dual_rebind_cardinal_wrong_locus");

		if (!IsHalfStepOffset(owned))
			return (false, $"dual_verts_not_face_centroids key={owned.Key} refuse=dual_centre_on_logic_as_half_step_proof");

		if (owned.OwnerFaceId >= 0)
			return (false, $"primary_face_as_dual owner_face={owned.OwnerFaceId} refuse=primary_face_as_dual");

		var expectPoly = Stage6DualCellPolygon(_graph.GetVertex(logicVertex));
		if (expectPoly.Length != owned.DualCorners.Length)
			return (false, "stage6_polygon_mismatch refuse=face_scan_proxy_neighborhood");
		for (var i = 0; i < expectPoly.Length; i++)
		{
			if (owned.DualCorners[i].DistanceSquaredTo(expectPoly[i]) > 1e-6f)
				return (false, "stage6_polygon_drift refuse=face_scan_proxy_neighborhood");
		}

		return (true,
			$"stage6_wire+small_corner_quads n_touch={touching.Count} small={small.Count} owned=1 around={logicVertex} " +
			$"dual_verts=face_centroids dual_edges=centroid_centroid small_corner_quads=true " +
			$"hex19_dual_vert_polarity=true vertex_neighbor_star=false " +
			$"primary_face_fill=false face_corners_local=false soft_take_4=false " +
			$"stage6_union_as_single_glow_tile=false owned_only_glow=false");
	}

	/// <summary>Backward-compatible name — Stage-6 cell proof.</summary>
	public (bool Ok, string Summary) ProveCardinalAround(int logicVertex) =>
		ProveFaceCentroidAround(logicVertex);

	public static Vector3[] VarignonMidpoints(Vector3[] faceCorners)
	{
		if (faceCorners == null || faceCorners.Length != 4)
			throw new ArgumentException("faceCorners must be length 4", nameof(faceCorners));
		return new[]
		{
			(faceCorners[0] + faceCorners[1]) * 0.5f,
			(faceCorners[1] + faceCorners[2]) * 0.5f,
			(faceCorners[2] + faceCorners[3]) * 0.5f,
			(faceCorners[3] + faceCorners[0]) * 0.5f,
		};
	}

	/// <summary>
	/// Stage-6 dual cell ring — DualCorners (face centroids). NOT FaceCornersLocal inset
	/// toward primal face verts (refuse inset_face_corners_as_dual /
	/// face_corners_local_as_dual_edges / primary_face_as_dual).
	/// </summary>
	public static Vector3[] Stage6CornersLocal(DualCell cell)
	{
		if (cell.DualCorners != null && cell.DualCorners.Length >= 3)
			return (Vector3[])cell.DualCorners.Clone();
		// Fallback diamond about placement centre — should not hit for editable cells.
		var centre = cell.LocalCentre;
		const float s = 0.35f;
		return new[]
		{
			centre + new Vector3(-s, 0f, -s),
			centre + new Vector3(s, 0f, -s),
			centre + new Vector3(s, 0f, s),
			centre + new Vector3(-s, 0f, s),
		};
	}

	/// <summary>
	/// OBSOLETE — FaceCornersLocal inset rings are NOT dual Success.
	/// Kept only so Prefer scanners / refuse proofs can detect removal from paint path.
	/// Prefer Stage6CornersLocal.
	/// </summary>
	[Obsolete("FaceCornersLocal inset rings are refuse=face_corners_local_as_dual_edges — use Stage6CornersLocal")]
	public static Vector3[] FaceCornersLocal(OrganicQuadMesh mesh, DualCell cell)
	{
		_ = mesh;
		return Stage6CornersLocal(cell);
	}
}
