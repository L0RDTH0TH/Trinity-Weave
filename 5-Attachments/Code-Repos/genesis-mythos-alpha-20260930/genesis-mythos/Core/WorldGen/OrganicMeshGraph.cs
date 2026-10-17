using System;
using System.Collections.Generic;
using System.Linq;
using Godot;

namespace Genesis.Core.WorldGen;

/// <summary>
/// Primal organic MeshGraph — Vertex / Edge / Face singletons with incidence.
///
/// success_object: organic_mesh_graph
/// Intent invariant: Primal ownership is Vertex/Edge/Face singletons with incidence;
/// dual cells are half-offset quads whose corners are those shared Vertex refs.
///
/// Refuse: indexed_lists_as_graph | ephemeral_edge_key_as_topology | non_unique_vertices
/// | proxy_substitution | intent_collapsed_to_mechanics.
/// </summary>
public sealed class OrganicMeshGraph
{
	public sealed class Vertex
	{
		internal Vertex(int id, Vector2 position)
		{
			Id = id;
			Position = position;
		}

		public int Id { get; }
		public Vector2 Position { get; set; }
		internal readonly List<Edge> Edges = new();
		internal readonly List<Face> Faces = new();

		public IReadOnlyList<Edge> IncidentEdges => Edges;
		public IReadOnlyList<Face> IncidentFaces => Faces;
	}

	public sealed class Edge
	{
		internal Edge(int id, Vertex a, Vertex b)
		{
			Id = id;
			A = a ?? throw new ArgumentNullException(nameof(a));
			B = b ?? throw new ArgumentNullException(nameof(b));
		}

		public int Id { get; }
		public Vertex A { get; }
		public Vertex B { get; }

		public Vertex Other(Vertex v)
		{
			if (ReferenceEquals(v, A)) return B;
			if (ReferenceEquals(v, B)) return A;
			throw new ArgumentException("vertex not on edge", nameof(v));
		}
	}

	public sealed class Face
	{
		internal Face(int id, Vertex[] corners, Edge[] edges)
		{
			Id = id;
			Corners = corners ?? throw new ArgumentNullException(nameof(corners));
			Edges = edges ?? throw new ArgumentNullException(nameof(edges));
		}

		public int Id { get; }
		/// <summary>Shared Vertex singletons — dual corners must reference these.</summary>
		public Vertex[] Corners { get; }
		public Edge[] Edges { get; }
	}

	private readonly float _quantum;
	private readonly Dictionary<(long Qx, long Qy), Vertex> _byCell = new();
	private readonly Dictionary<(int Lo, int Hi), Edge> _edgeByEnds = new();
	private readonly List<Vertex> _vertices = new();
	private readonly List<Edge> _edges = new();
	private readonly List<Face> _faces = new();

	public OrganicMeshGraph(float quantum = 1e-4f)
	{
		_quantum = Math.Max(1e-6f, quantum);
	}

	public IReadOnlyList<Vertex> Vertices => _vertices;
	public IReadOnlyList<Edge> Edges => _edges;
	public IReadOnlyList<Face> Faces => _faces;
	public int VertexCount => _vertices.Count;
	public int EdgeCount => _edges.Count;
	public int FaceCount => _faces.Count;

	public bool AllFacesAreQuads
	{
		get
		{
			foreach (var f in _faces)
			{
				if (f.Corners == null || f.Corners.Length != 4) return false;
			}
			return _faces.Count > 0;
		}
	}

	public Vertex GetOrAddVertex(Vector2 p)
	{
		var key = UniqueTopology2D.QuantizeCell(p, _quantum);
		if (_byCell.TryGetValue(key, out var existing))
			return existing;
		var v = new Vertex(_vertices.Count, p);
		_vertices.Add(v);
		_byCell[key] = v;
		return v;
	}

	public Edge GetOrAddEdge(Vertex a, Vertex b)
	{
		if (a == null) throw new ArgumentNullException(nameof(a));
		if (b == null) throw new ArgumentNullException(nameof(b));
		if (ReferenceEquals(a, b))
			throw new ArgumentException("degenerate edge", nameof(b));
		var lo = Math.Min(a.Id, b.Id);
		var hi = Math.Max(a.Id, b.Id);
		var ek = (lo, hi);
		if (_edgeByEnds.TryGetValue(ek, out var existing))
			return existing;
		var e = new Edge(_edges.Count, a, b);
		_edges.Add(e);
		_edgeByEnds[ek] = e;
		if (!a.Edges.Contains(e)) a.Edges.Add(e);
		if (!b.Edges.Contains(e)) b.Edges.Add(e);
		return e;
	}

	public Face AddQuad(Vertex a, Vertex b, Vertex c, Vertex d)
	{
		if (a == null || b == null || c == null || d == null)
			throw new ArgumentNullException("quad corners");
		var corners = new[] { a, b, c, d };
		var distinct = new HashSet<Vertex>(corners);
		if (distinct.Count != 4)
			throw new ArgumentException("degenerate quad — non-unique Vertex corners");
		var edges = new[]
		{
			GetOrAddEdge(a, b),
			GetOrAddEdge(b, c),
			GetOrAddEdge(c, d),
			GetOrAddEdge(d, a),
		};
		var face = new Face(_faces.Count, corners, edges);
		_faces.Add(face);
		foreach (var v in corners)
		{
			if (!v.Faces.Contains(face))
				v.Faces.Add(face);
		}
		return face;
	}

	public Face AddQuad(int a, int b, int c, int d) =>
		AddQuad(GetVertex(a), GetVertex(b), GetVertex(c), GetVertex(d));

	public Vertex GetVertex(int id)
	{
		if (id < 0 || id >= _vertices.Count)
			throw new ArgumentOutOfRangeException(nameof(id));
		return _vertices[id];
	}

	/// <summary>Incident faces via Vertex singleton incidence — not ephemeral index maps.</summary>
	public IReadOnlyList<Face> FacesTouchingVertex(Vertex v)
	{
		if (v == null) return Array.Empty<Face>();
		return v.Faces;
	}

	public IReadOnlyList<Face> FacesTouchingVertex(int vertexId)
	{
		if (vertexId < 0 || vertexId >= _vertices.Count)
			return Array.Empty<Face>();
		return _vertices[vertexId].Faces;
	}

	/// <summary>
	/// Build graph from indexed mesh — migrates UniqueTopology2D weld into MeshGraph singletons.
	/// Indexed lists are input only; Success ownership lives on returned Vertex/Edge/Face refs.
	/// </summary>
	public static OrganicMeshGraph FromIndexedMesh(
		List<Vector2> verts,
		List<int[]> faces,
		float quantum)
	{
		var topo = UniqueTopology2D.FromIndexedMesh(verts, faces, quantum);
		var graph = new OrganicMeshGraph(quantum);
		foreach (var p in topo.Vertices)
			graph.GetOrAddVertex(p);
		foreach (var f in topo.Faces)
		{
			if (f == null || f.Length != 4) continue;
			var distinct = new HashSet<int>(f);
			if (distinct.Count != 4) continue;
			graph.AddQuad(f[0], f[1], f[2], f[3]);
		}
		return graph;
	}

	/// <summary>Transitional export for callers still consuming indexed buffers.</summary>
	public (List<Vector2> Verts, List<int[]> Quads) ToIndexedMesh()
	{
		var verts = _vertices.Select(v => v.Position).ToList();
		var quads = new List<int[]>(_faces.Count);
		foreach (var f in _faces)
		{
			if (f.Corners.Length != 4) continue;
			quads.Add(new[]
			{
				f.Corners[0].Id,
				f.Corners[1].Id,
				f.Corners[2].Id,
				f.Corners[3].Id,
			});
		}
		return (verts, quads);
	}

	public void SyncPositionsFrom(List<Vector2> positions)
	{
		if (positions == null) return;
		var n = Math.Min(positions.Count, _vertices.Count);
		for (var i = 0; i < n; i++)
			_vertices[i].Position = positions[i];
	}
}
