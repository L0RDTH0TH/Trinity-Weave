using System;
using System.Collections.Generic;
using Godot;

namespace Genesis.Core.WorldGen;

/// <summary>
/// Result of the Stålberg organic all-quad pipeline — vertices + quad faces (valence 4).
/// relax_r1: unique hashed topology + area-square relax; planar opaque board; depth-tested edges.
/// Refuse: non_unique_vertices / missing_square_area_force / naive_laplacian_only /
/// free_boundary_fold / extrusion_before_2d_stable / noodle_edge_clutter /
/// extruded_prism_as_quad_board. Hex19* types are NOT this Success surface.
/// </summary>
public sealed class OrganicQuadMesh
{
	public OrganicQuadMesh(List<Vector2> vertices, List<int[]> quads, int seedRingCount, ulong seed)
	{
		Vertices = vertices ?? throw new ArgumentNullException(nameof(vertices));
		Quads = quads ?? throw new ArgumentNullException(nameof(quads));
		SeedRingCount = seedRingCount;
		Seed = seed;
		FlattenToCraftPlane();
	}

	public List<Vector2> Vertices { get; }
	public List<int[]> Quads { get; }
	public int SeedRingCount { get; }
	public ulong Seed { get; }

	public int VertexCount => Vertices.Count;
	public int FaceCount => Quads.Count;
	public int EdgeEstimate
	{
		get
		{
			var seen = new HashSet<long>();
			foreach (var q in Quads)
			{
				if (q == null || q.Length != 4) continue;
				for (var i = 0; i < 4; i++)
					seen.Add(EdgeKey(q[i], q[(i + 1) % 4]));
			}

			return seen.Count;
		}
	}

	public bool AllFacesAreQuads
	{
		get
		{
			foreach (var q in Quads)
			{
				if (q == null || q.Length != 4)
					return false;
			}

			return Quads.Count > 0;
		}
	}

	/// <summary>
	/// Law step — keep the generative surface on the craft plane (XZ / Vector2).
	/// Finite sanitize only; refuses unbounded NaN/Inf as planar board input.
	/// </summary>
	public void FlattenToCraftPlane()
	{
		for (var i = 0; i < Vertices.Count; i++)
		{
			var v = Vertices[i];
			var x = float.IsFinite(v.X) ? v.X : 0f;
			var y = float.IsFinite(v.Y) ? v.Y : 0f;
			Vertices[i] = new Vector2(x, y);
		}
	}

	/// <summary>
	/// Opaque planar quad faces on craft plane Y=0 — depth write on.
	/// No Alpha (refuse extruded_prism_as_quad_board / noodle soup). Cull disabled for craft-cam angles.
	/// </summary>
	public ArrayMesh BuildFaceMesh(Color color)
	{
		var opaque = new Color(color.R, color.G, color.B, 1f);
		var st = new SurfaceTool();
		st.Begin(Mesh.PrimitiveType.Triangles);
		foreach (var q in Quads)
		{
			if (q.Length != 4) continue;
			var c0 = ToXz(Vertices[q[0]]);
			var c1 = ToXz(Vertices[q[1]]);
			var c2 = ToXz(Vertices[q[2]]);
			var c3 = ToXz(Vertices[q[3]]);
			// Two tris per quad, CCW about +Y.
			EmitTri(st, opaque, c0, c1, c2);
			EmitTri(st, opaque, c0, c2, c3);
		}

		var mesh = st.Commit();
		// Opaque + depth write. Cull disabled so craft-cam angles still see the board
		// (Back-cull + wrong winding = edges-only noodle silhouette). No Alpha = no prism soup.
		// Unshaded denim plate — Goal Final-grid-state reads as flat blueprint, not lit grey.
		mesh.SurfaceSetMaterial(0, new StandardMaterial3D
		{
			AlbedoColor = opaque,
			Transparency = BaseMaterial3D.TransparencyEnum.Disabled,
			CullMode = BaseMaterial3D.CullModeEnum.Disabled,
			ShadingMode = BaseMaterial3D.ShadingModeEnum.Unshaded,
			DepthDrawMode = BaseMaterial3D.DepthDrawModeEnum.OpaqueOnly,
		});
		return mesh;
	}

	/// <summary>
	/// Depth-tested opaque edge graph — unique edges only; no additive alpha spaghetti.
	/// </summary>
	public ArrayMesh BuildEdgeMesh(Color color)
	{
		var opaque = new Color(color.R, color.G, color.B, 1f);
		var st = new SurfaceTool();
		st.Begin(Mesh.PrimitiveType.Lines);
		var seen = new HashSet<long>();
		foreach (var q in Quads)
		{
			if (q.Length != 4) continue;
			for (var i = 0; i < 4; i++)
			{
				var a = q[i];
				var b = q[(i + 1) % 4];
				var key = EdgeKey(a, b);
				if (!seen.Add(key)) continue;
				// Tiny lift so edges sit on the opaque face without unbounded Z jitter.
				st.SetColor(opaque);
				st.AddVertex(ToXz(Vertices[a]) + Vector3.Up * 0.008f);
				st.SetColor(opaque);
				st.AddVertex(ToXz(Vertices[b]) + Vector3.Up * 0.008f);
			}
		}

		var mesh = st.Commit();
		mesh.SurfaceSetMaterial(0, new StandardMaterial3D
		{
			AlbedoColor = opaque,
			Transparency = BaseMaterial3D.TransparencyEnum.Disabled,
			ShadingMode = BaseMaterial3D.ShadingModeEnum.Unshaded,
			DepthDrawMode = BaseMaterial3D.DepthDrawModeEnum.OpaqueOnly,
			NoDepthTest = false,
		});
		return mesh;
	}


	/// <summary>
	/// Craft-plane pick — local XZ (craft plane) → containing organic quad face index.
	/// Occupancy authority key = Vector2I(faceIndex, 0). Refuse Hex19 as Success snap.
	/// </summary>
	public bool TryPickFace(Vector2 localXz, out int faceIndex)
	{
		faceIndex = -1;
		var bestDist = float.MaxValue;
		for (var i = 0; i < Quads.Count; i++)
		{
			var q = Quads[i];
			if (q == null || q.Length != 4) continue;
			var c0 = Vertices[q[0]];
			var c1 = Vertices[q[1]];
			var c2 = Vertices[q[2]];
			var c3 = Vertices[q[3]];
			if (!PointInQuad(localXz, c0, c1, c2, c3))
				continue;
			var centroid = (c0 + c1 + c2 + c3) * 0.25f;
			var d = localXz.DistanceSquaredTo(centroid);
			if (d >= bestDist) continue;
			bestDist = d;
			faceIndex = i;
		}

		return faceIndex >= 0;
	}

	/// <summary>Nearest face by centroid when hit is slightly outside (ghost soft snap).</summary>
	public bool TryNearestFace(Vector2 localXz, out int faceIndex, float maxDist = 1.25f)
	{
		faceIndex = -1;
		var best = maxDist * maxDist;
		for (var i = 0; i < Quads.Count; i++)
		{
			var q = Quads[i];
			if (q == null || q.Length != 4) continue;
			var c = FaceCentroid(i);
			var d = localXz.DistanceSquaredTo(c);
			if (d >= best) continue;
			best = d;
			faceIndex = i;
		}

		return faceIndex >= 0;
	}

	public bool ContainsFace(int faceIndex) =>
		faceIndex >= 0 && faceIndex < Quads.Count && Quads[faceIndex] is { Length: 4 };

	public Vector2 FaceCentroid(int faceIndex)
	{
		var q = Quads[faceIndex];
		return (Vertices[q[0]] + Vertices[q[1]] + Vertices[q[2]] + Vertices[q[3]]) * 0.25f;
	}

	public Vector3 FaceCentroidWorld(int faceIndex, Vector3 origin) =>
		ToXz(FaceCentroid(faceIndex)) + origin;

	public Vector3[] FaceCornersLocal(int faceIndex)
	{
		var q = Quads[faceIndex];
		return new[]
		{
			ToXz(Vertices[q[0]]),
			ToXz(Vertices[q[1]]),
			ToXz(Vertices[q[2]]),
			ToXz(Vertices[q[3]]),
		};
	}

	/// <summary>Encode organic face index as ICraftCellAuthority cell key.</summary>
	public static Vector2I FaceCell(int faceIndex) => new(faceIndex, 0);

	public static int FaceIndexFromCell(Vector2I cell) => cell.X;

	private static bool PointInQuad(Vector2 p, Vector2 a, Vector2 b, Vector2 c, Vector2 d) =>
		PointInTri(p, a, b, c) || PointInTri(p, a, c, d);

	private static bool PointInTri(Vector2 p, Vector2 a, Vector2 b, Vector2 c)
	{
		var v0 = c - a;
		var v1 = b - a;
		var v2 = p - a;
		var dot00 = v0.Dot(v0);
		var dot01 = v0.Dot(v1);
		var dot02 = v0.Dot(v2);
		var dot11 = v1.Dot(v1);
		var dot12 = v1.Dot(v2);
		var denom = dot00 * dot11 - dot01 * dot01;
		if (Mathf.Abs(denom) < 1e-8f) return false;
		var inv = 1f / denom;
		var u = (dot11 * dot02 - dot01 * dot12) * inv;
		var v = (dot00 * dot12 - dot01 * dot02) * inv;
		return u >= -1e-4f && v >= -1e-4f && (u + v) <= 1f + 1e-4f;
	}

	private static void EmitTri(SurfaceTool st, Color color, Vector3 a, Vector3 b, Vector3 c)
	{
		st.SetColor(color);
		st.SetNormal(Vector3.Up);
		st.AddVertex(a);
		st.SetColor(color);
		st.SetNormal(Vector3.Up);
		st.AddVertex(b);
		st.SetColor(color);
		st.SetNormal(Vector3.Up);
		st.AddVertex(c);
	}

	private static Vector3 ToXz(Vector2 v) => new(v.X, 0f, v.Y);

	private static long EdgeKey(int a, int b)
	{
		var lo = Math.Min(a, b);
		var hi = Math.Max(a, b);
		return ((long)lo << 32) | (uint)hi;
	}
}
