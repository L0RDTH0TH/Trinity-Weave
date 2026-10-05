using System;
using System.Collections.Generic;
using Godot;

namespace Genesis.Core.WorldGen;

/// <summary>
/// One face of the hex-19 lattice — the cell a ghost snaps to and occupancy fills.
/// A cell is defined by its six corners, not by the marker sitting at its centre.
/// </summary>
public readonly struct HexCell
{
	public HexCell(Vector2I axial, int index)
	{
		Axial = axial;
		Index = index;
	}

	/// <summary>Axial coordinate of the lattice vertex this face is built around.</summary>
	public Vector2I Axial { get; }

	/// <summary>Stable index into <see cref="Hex19OccupancyLattice.Cells"/>.</summary>
	public int Index { get; }
}

/// <summary>
/// Fixed hex-19 occupancy LATTICE GRAPH — centre + 2 rings (1+6+12 = 19 vertices),
/// the neighbour EDGES between them, and the hex FACES/CELLS those vertices define.
///
/// Tutorial s1 law (Grid-Topology-Host-Law): points are not a grid. A bare vertex
/// list is refused as points_as_grid / count_equals_topology — Success needs all
/// three axes (vertices + neighbour edges + faces/cells) to exist as topology.
/// Pointy-top axial (q,r) -> world XZ relative to the lattice origin.
/// </summary>
public static class Hex19OccupancyLattice
{
	public const int VertexCount = 19;
	public const int CornersPerCell = 6;
	public const float DefaultSize = 1.15f;

	/// <summary>Axial neighbour directions — the edge set generator for the graph.</summary>
	public static readonly Vector2I[] NeighborOffsets =
	{
		new(1, 0), new(1, -1), new(0, -1), new(-1, 0), new(-1, 1), new(0, 1),
	};

	/// <summary>The 19 lattice vertices (axial), rings 0..2 inclusive.</summary>
	public static readonly Vector2I[] Vertices = BuildRingVertices(rings: 2);

	private static readonly HashSet<Vector2I> VertexSet = new(Vertices);

	/// <summary>Unique neighbour edges between in-lattice vertices (graph axis 2).</summary>
	public static readonly (Vector2I A, Vector2I B)[] Edges = BuildEdges();

	/// <summary>The hex faces/cells the lattice resolves to (graph axis 3).</summary>
	public static readonly HexCell[] Cells = BuildCells();

	public static int EdgeCount => Edges.Length;
	public static int CellCount => Cells.Length;

	public static bool Contains(Vector2I axial) => VertexSet.Contains(axial);

	public static int HexDistance(Vector2I a, Vector2I b)
	{
		var dq = a.X - b.X;
		var dr = a.Y - b.Y;
		return (Math.Abs(dq) + Math.Abs(dr) + Math.Abs(dq + dr)) / 2;
	}

	/// <summary>True when two lattice vertices share an edge.</summary>
	public static bool AreAdjacent(Vector2I a, Vector2I b) =>
		a != b && Contains(a) && Contains(b) && HexDistance(a, b) == 1;

	/// <summary>In-lattice neighbours of a vertex (adjacency list for the graph).</summary>
	public static List<Vector2I> NeighborsOf(Vector2I axial)
	{
		var list = new List<Vector2I>(CornersPerCell);
		foreach (var d in NeighborOffsets)
		{
			var n = new Vector2I(axial.X + d.X, axial.Y + d.Y);
			if (Contains(n))
				list.Add(n);
		}
		return list;
	}

	/// <summary>Edges incident to one vertex — used for edge highlight / lattice draw.</summary>
	public static List<(Vector2I A, Vector2I B)> EdgesOf(Vector2I axial)
	{
		var list = new List<(Vector2I, Vector2I)>(CornersPerCell);
		foreach (var n in NeighborsOf(axial))
			list.Add(axial.X < n.X || (axial.X == n.X && axial.Y < n.Y) ? (axial, n) : (n, axial));
		return list;
	}

	/// <summary>Pointy-top axial -> local XZ (Y unused).</summary>
	public static Vector3 AxialToLocal(Vector2I axial, float size = DefaultSize)
	{
		var x = size * (Mathf.Sqrt(3f) * axial.X + Mathf.Sqrt(3f) / 2f * axial.Y);
		var z = size * (1.5f * axial.Y);
		return new Vector3(x, 0f, z);
	}

	public static Vector3 AxialToWorld(Vector2I axial, Vector3 origin, float size = DefaultSize) =>
		origin + AxialToLocal(axial, size);

	/// <summary>
	/// The six corners of a pointy-top hex face, CCW. Shared corners between adjacent
	/// cells are what makes the lattice a tiling of faces rather than loose markers.
	/// </summary>
	public static Vector3[] HexCorners(Vector2I axial, float size = DefaultSize)
	{
		var centre = AxialToLocal(axial, size);
		var corners = new Vector3[CornersPerCell];
		for (var i = 0; i < CornersPerCell; i++)
		{
			var angle = Mathf.Pi / 180f * (60f * i + 30f);
			corners[i] = new Vector3(
				centre.X + size * Mathf.Cos(angle),
				centre.Y,
				centre.Z + size * Mathf.Sin(angle));
		}
		return corners;
	}

	/// <summary>Face corners in world space for the cell at <paramref name="axial"/>.</summary>
	public static Vector3[] CellCornersOf(Vector2I axial, Vector3 origin, float size = DefaultSize)
	{
		var corners = HexCorners(axial, size);
		for (var i = 0; i < corners.Length; i++)
			corners[i] += origin;
		return corners;
	}

	/// <summary>
	/// World hit -> the CELL containing it (axial cube rounding over the whole face),
	/// not the nearest marker within a radius. Ghost snaps to a cell, never to a disk.
	/// </summary>
	public static bool TrySnapWorldToCell(
		Vector3 worldHit,
		Vector3 origin,
		out Vector2I axial,
		float size = DefaultSize)
	{
		axial = default;
		var local = worldHit - origin;
		var fq = (Mathf.Sqrt(3f) / 3f * local.X - 1f / 3f * local.Z) / size;
		var fr = (2f / 3f * local.Z) / size;
		var rounded = CubeRound(fq, fr);
		if (!Contains(rounded))
			return false;
		axial = rounded;
		return true;
	}

	/// <summary>Cube rounding — fractional axial to the containing hex face.</summary>
	private static Vector2I CubeRound(float fq, float fr)
	{
		var fs = -fq - fr;
		var q = Mathf.RoundToInt(fq);
		var r = Mathf.RoundToInt(fr);
		var s = Mathf.RoundToInt(fs);

		var dq = Mathf.Abs(q - fq);
		var dr = Mathf.Abs(r - fr);
		var ds = Mathf.Abs(s - fs);

		if (dq > dr && dq > ds)
			q = -r - s;
		else if (dr > ds)
			r = -q - s;
		return new Vector2I(q, r);
	}

	private static Vector2I[] BuildRingVertices(int rings)
	{
		var list = new List<Vector2I> { Vector2I.Zero };
		for (var ring = 1; ring <= rings; ring++)
		{
			// Start at (+ring, 0) and walk the six edges counterclockwise.
			var q = ring;
			var r = 0;
			var dirs = new (int dq, int dr)[]
			{
				(0, -1), (-1, 0), (-1, 1), (0, 1), (1, 0), (1, -1),
			};
			foreach (var (dq, dr) in dirs)
			{
				for (var step = 0; step < ring; step++)
				{
					list.Add(new Vector2I(q, r));
					q += dq;
					r += dr;
				}
			}
		}

		if (list.Count != VertexCount)
			throw new InvalidOperationException($"Hex19 expected {VertexCount} vertices, got {list.Count}");
		return list.ToArray();
	}

	/// <summary>Enumerate each neighbour pair once — the lattice edge set.</summary>
	private static (Vector2I A, Vector2I B)[] BuildEdges()
	{
		var seen = new HashSet<(Vector2I, Vector2I)>();
		var edges = new List<(Vector2I, Vector2I)>();
		foreach (var v in Vertices)
		{
			foreach (var d in NeighborOffsets)
			{
				var n = new Vector2I(v.X + d.X, v.Y + d.Y);
				if (!VertexSet.Contains(n))
					continue;
				var key = v.X < n.X || (v.X == n.X && v.Y < n.Y) ? (v, n) : (n, v);
				if (seen.Add(key))
					edges.Add(key);
			}
		}

		if (edges.Count == 0)
			throw new InvalidOperationException("Hex19 lattice has no edges — points_as_grid");
		return edges.ToArray();
	}

	/// <summary>Build the face set — one hex cell per lattice vertex.</summary>
	private static HexCell[] BuildCells()
	{
		var cells = new HexCell[Vertices.Length];
		for (var i = 0; i < Vertices.Length; i++)
			cells[i] = new HexCell(Vertices[i], i);
		return cells;
	}
}
