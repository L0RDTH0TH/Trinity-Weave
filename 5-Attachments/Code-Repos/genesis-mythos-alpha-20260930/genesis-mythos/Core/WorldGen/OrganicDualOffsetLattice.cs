using System;
using System.Collections.Generic;
using System.Linq;
using Godot;

namespace Genesis.Core.WorldGen;

/// <summary>
/// Organic dual-offset lattice — half-step dual cells on Stålberg organic corners.
///
/// Townscaper / oskar docs/03 grammar (organic edition):
/// - Logic points = organic mesh vertices (player paint / flip targets).
/// - Dual cells = faces of this dual lattice: each has four logic corners;
///   centre sits half-step between them (face centroid of the supporting quad).
/// - One logic flip → DualCellsTouching refreshes ≤4 dual cells that list that
///   vertex as a corner (stable, geometric).
/// - Mesh geometry uses Varignon midpoints so dual tiles are visibly offset from
///   the primary yellow-wire face fill (refuse primary_face_as_dual).
///
/// Dual cell identity is NOT OrganicQuadMesh face-index as Success id — keys live here (refuse primary-face-index dual ids).
/// Refuse: primary_face_as_dual | skip_dual_offset | stamp_as_dual | unstable_dual_neighborhood.
/// </summary>
public sealed class OrganicDualOffsetLattice
{
	public const int MaxCornersPerDual = 4;
	public const int MaxDualsPerLogicPoint = 4;

	public readonly struct DualCell
	{
		public DualCell(string key, int[] cornerLogicIndices, Vector3 localCentre, int supportFaceIndex)
		{
			Key = key ?? throw new ArgumentNullException(nameof(key));
			CornerLogicIndices = cornerLogicIndices ?? throw new ArgumentNullException(nameof(cornerLogicIndices));
			LocalCentre = localCentre;
			SupportFaceIndex = supportFaceIndex;
		}

		/// <summary>Stable dual identity (sorted corner indices) — not primary-face-index.</summary>
		public string Key { get; }

		/// <summary>Four organic vertex indices sampled as logic corners.</summary>
		public int[] CornerLogicIndices { get; }

		/// <summary>Half-step centre between the four logic corners.</summary>
		public Vector3 LocalCentre { get; }

		/// <summary>Supporting organic face used only to derive corners (not dual Success id).</summary>
		public int SupportFaceIndex { get; }
	}

	private readonly List<DualCell> _cells = new();
	private readonly Dictionary<string, DualCell> _byKey = new();
	private readonly Dictionary<int, List<string>> _vertexToDualKeys = new();
	private readonly List<Vector2> _logicPositions;

	public OrganicDualOffsetLattice(OrganicQuadMesh mesh)
	{
		if (mesh == null) throw new ArgumentNullException(nameof(mesh));
		_logicPositions = mesh.Vertices;
		Rebuild(mesh);
	}

	public IReadOnlyList<DualCell> AllCells => _cells;
	public int CellCount => _cells.Count;
	public int LogicPointCount => _vertexToDualKeys.Count;

	public void Rebuild(OrganicQuadMesh mesh)
	{
		_cells.Clear();
		_byKey.Clear();
		_vertexToDualKeys.Clear();
		if (mesh == null) return;

		for (var fi = 0; fi < mesh.Quads.Count; fi++)
		{
			var q = mesh.Quads[fi];
			if (q == null || q.Length != 4) continue;
			var corners = (int[])q.Clone();
			Array.Sort(corners);
			// Deterministic key from sorted logic corners — refuse primary-face-index as Success id.
			var key = "d_" + corners[0] + "_" + corners[1] + "_" + corners[2] + "_" + corners[3];
			if (_byKey.ContainsKey(key)) continue;

			var sum = Vector3.Zero;
			for (var i = 0; i < 4; i++)
			{
				var v = mesh.Vertices[q[i]];
				sum += new Vector3(v.X, 0f, v.Y);
			}
			var centre = sum * 0.25f;
			var cell = new DualCell(key, (int[])q.Clone(), centre, fi);
			_cells.Add(cell);
			_byKey[key] = cell;
			foreach (var vi in q)
			{
				if (!_vertexToDualKeys.TryGetValue(vi, out var list))
				{
					list = new List<string>();
					_vertexToDualKeys[vi] = list;
				}
				if (!list.Contains(key)) list.Add(key);
			}
		}

		// Editable logic points = vertices with ≤4 incident dual cells (hex-seed valence>4 stay geometry-only).
		foreach (var key in _vertexToDualKeys.Keys.ToList())
		{
			_vertexToDualKeys[key].Sort(StringComparer.Ordinal);
			if (_vertexToDualKeys[key].Count > MaxDualsPerLogicPoint)
				_vertexToDualKeys.Remove(key);
		}
	}

	public bool IsEditableLogicPoint(int vertexIndex) =>
		_vertexToDualKeys.ContainsKey(vertexIndex);

	public IReadOnlyCollection<int> EditableLogicPoints => _vertexToDualKeys.Keys;

	/// <summary>Dual cells that list this logic point as a corner (update-four set).</summary>
	public IReadOnlyList<DualCell> DualCellsTouching(int logicVertex)
	{
		if (!_vertexToDualKeys.TryGetValue(logicVertex, out var keys) || keys.Count == 0)
			return Array.Empty<DualCell>();
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
		if (!_vertexToDualKeys.TryGetValue(logicVertex, out var keys) || keys.Count == 0)
			return Array.Empty<string>();
		return keys.ToList();
	}

	public bool TryGet(string key, out DualCell cell) => _byKey.TryGetValue(key, out cell);

	/// <summary>
	/// True when dual centre is spatially offset from every logic vertex
	/// (half-step proof — refuse dual coincident with logic markers / primary-face identity theater).
	/// </summary>
	public bool IsHalfStepOffset(DualCell cell, float eps = 1e-4f)
	{
		var eps2 = eps * eps;
		for (var i = 0; i < _logicPositions.Count; i++)
		{
			var p = _logicPositions[i];
			var occ = new Vector3(p.X, 0f, p.Y);
			if (cell.LocalCentre.DistanceSquaredTo(occ) < eps2)
				return false;
		}
		return true;
	}

	/// <summary>
	/// Varignon parallelogram (edge midpoints) — dual tile geometry inset/offset from
	/// primary face corners so F5 highlight is not a cyan primary-face fill.
	/// </summary>
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

	public static Vector3[] FaceCornersLocal(OrganicQuadMesh mesh, DualCell cell)
	{
		var q = cell.CornerLogicIndices;
		var c = new Vector3[4];
		for (var i = 0; i < 4; i++)
		{
			var v = mesh.Vertices[q[i]];
			c[i] = new Vector3(v.X, 0f, v.Y);
		}
		return c;
	}
}
