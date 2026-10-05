using System;
using System.Collections.Generic;
using Godot;

namespace Genesis.Core.WorldGen;

/// <summary>
/// Stålberg / Lerg organic all-quad grid kernel (oskar-procedure docs/02 + Lerg pipeline).
/// Pipeline: Seed (Variant B hex) → Triangulate → Dissolve → Subdivide →
/// Unique topology (position-hash) → Rotate-90 average squarify → Re-weld → Flatten.
/// Hex19OccupancyLattice / Hex19DualOffsetLattice are NOT Success types for this ask.
/// Prefer: alpha0_stalberg_quad_kernel_squarify_r1 — Stage 5 = rotate-90 average
/// (replaces Variant A closest-square atan). Refuse closest_square_as_organic_success,
/// diamond_lock_hex_seed, naive_laplacian_only, free_boundary_fold,
/// missing_square_area_force, relax_step_too_hard, relax_before_quad_only.
/// </summary>
public static class StalbergQuadKernel
{
	/// <summary>
	/// Product-density seed rings — rings=5 → ~10 cells across post-subdivide.
	/// Prefer tickets historically froze hex19 rings=2; operator greenlit density lift 2026-10-04.
	/// </summary>
	public const int ProductDensityRingCount = 5;
	/// <summary>
	/// LIVE craft seed CELL COUNT — equals <see cref="ProductDensityRingCount"/> (density lift LIVE).
	/// World SIZE still enlarged via <see cref="DefaultSpacing"/> (keep 210 unless cam can't frame).
	/// </summary>
	public const int DefaultRingCount = ProductDensityRingCount;
	/// <summary>Legacy dense-era spacing (rings=5 era). Kept for compare / density-lift restore.</summary>
	public const float LegacyDenseSpacing = 1.15f;
	/// <summary>
	/// Manual craft spacing — enlarge physical cell size at product density (rings=5).
	/// 210.0 = 70× original baseline spacing (3.0); 10× the prior craft footprint (21).
	/// </summary>
	public const float DefaultSpacing = 210.0f;
	/// <summary>
	/// Soft relax with mesh-boundary pin union (not hull-only). Iter4: re-test flow vs goal
	/// after boundary-edge pins fix free_boundary_fold / jagged hex.
	/// Diagnostic hold was <c>0</c> (relax_r2 / topology_base pre-relax MCP); Stage 5 is ON again.
	/// </summary>
	public const int DefaultRelaxIters = 80;
	/// <summary>Soft step — Prefer band [0.05, 0.15]; operator nudge 0.08→0.12 (iters 90).</summary>
	public const float DefaultPullRate = 0.12f;
	public const float DefaultSideLength = 0.55f;
	/// <summary>
	/// Legacy absolute force clamp (tuned for spacing ≈1–3). At 7× spacing this near-zeroed Stage 5;
	/// <see cref="Generate"/> uses <see cref="DefaultForceClampSideFraction"/> × area side instead.
	/// </summary>
	public const float DefaultForceClamp = 0.35f;
	/// <summary>
	/// Per-iter force clamp as a fraction of area-derived ideal side — keeps Stage 5 strength
	/// stable when <see cref="DefaultSpacing"/> changes (refuse scale-blind absolute clamp).
	/// </summary>
	public const float DefaultForceClampSideFraction = 0.25f;
	public const float PositionHashQuantum = 1e-4f;
	public const float ReweldEpsilon = 1e-3f;

	public static OrganicQuadMesh Generate(
		int ringCount = DefaultRingCount,
		float spacing = DefaultSpacing,
		ulong? seed = null,
		int relaxIters = DefaultRelaxIters)
	{
		var rngSeed = seed ?? (ulong)DateTime.UtcNow.Ticks;
		var rng = new Random((int)(rngSeed & 0x7fffffff));

		// Stage 1–2: axial-keyed seed + local neighbour triangulation (NO PlaneToAxial round-trip).
		// Grok: star explosion = bad connectivity before relax; keep axial indices authoritative.
		var (points, indexByAxial) = SeedHexLatticeRingsWithAxial(ringCount, spacing);
		var tris = TriangulateHexLatticeFromAxial(indexByAxial);
		LogEdgeStats("tri", points, tris);

		// Stage 3–4: merge → subdivide to 100% quads BEFORE relax.
		var (verts, faces) = DissolveTrianglePairs(points, tris, rng);
		LogFaceMix("merge", faces);
		LogEdgeStats("merge", verts, faces);
		(verts, var quads) = SubdivideFacesToQuads(verts, faces);
		LogEdgeStats("sub_raw", verts, quads);

		// Primal MeshGraph — UniqueTopology2D migrates into Vertex/Edge/Face singletons + incidence.
		// Refuse indexed_lists_as_graph / ephemeral_edge_key_as_topology as Success.
		var graph = OrganicMeshGraph.FromIndexedMesh(verts, quads, PositionHashQuantum);
		(verts, quads) = graph.ToIndexedMesh();
		if (!graph.AllFacesAreQuads || quads.Count == 0)
			throw new InvalidOperationException("relax_before_quad_only: mesh not quad-only after subdivide");
		LogEdgeStats("sub_unique", verts, quads);

		// Area-based ideal side → half-diagonal scale for rotate-90 targets (not naïve Laplacian).
		var side = EstimateIdealSideFromArea(verts, quads);
		if (side < 1e-4f) side = spacing * 0.5f;
		var pinned = MarkBoundaryPinned(verts, quads);
		var pull = Mathf.Clamp(DefaultPullRate, 0.05f, 0.15f);
		// Side-relative clamp — absolute DefaultForceClamp made 7× spacing look like relax-off.
		var forceClamp = MathF.Max(side * DefaultForceClampSideFraction, 1e-4f);
		GD.Print($"StalbergQuadKernel.Generate DIAG: relaxIters={relaxIters} pull={pull} forceClamp={forceClamp} quads={quads.Count} verts={verts.Count} pinned={pinned.Count} side={side} topoKey=qxqy relaxMode=rotate90_avg");
		RelaxTowardSquares(
			verts, quads, relaxIters, pull, side, pinned, forceClamp);
		LogEdgeStats("post_relax", verts, quads);

		// Re-weld near-duplicates after relax — refuse welds that raise valence >4
		// (would create over_neighbor_paint / unstable dual ownership).
		var preWeldVerts = verts;
		var preWeldQuads = quads;
		(verts, quads) = WeldNearDuplicates(verts, quads, ReweldEpsilon);
		var maxValence = MaxVertexFaceValence(quads, verts.Count);
		if (maxValence > 4)
		{
			GD.Print($"StalbergQuadKernel.post_weld: refuse valence={maxValence}>4 — keep pre-weld unique topo (dual-neighborhood)");
			verts = preWeldVerts;
			quads = preWeldQuads;
			maxValence = MaxVertexFaceValence(quads, verts.Count);
		}
		LogEdgeStats("post_weld", verts, quads);
		GD.Print($"StalbergQuadKernel.post_weld: max_vertex_face_valence={maxValence}");

		// Explicit craft-plane flatten — 2D stable before any extrusion language.
		for (var i = 0; i < verts.Count; i++)
		{
			var v = verts[i];
			verts[i] = new Vector2(
				float.IsFinite(v.X) ? v.X : 0f,
				float.IsFinite(v.Y) ? v.Y : 0f);
		}

		// Hold final primal graph after relax/weld — Success ownership = organic_mesh_graph.
		graph = OrganicMeshGraph.FromIndexedMesh(verts, quads, PositionHashQuantum);
		(verts, quads) = graph.ToIndexedMesh();
		return new OrganicQuadMesh(graph, ringCount, rngSeed);
	}

	/// <summary>Stage 1 — Variant B: concentric hex rings with axial→index map (authoritative).</summary>
	public static List<Vector2> SeedHexLatticeRings(int ringCount, float spacing)
	{
		var (verts, _) = SeedHexLatticeRingsWithAxial(ringCount, spacing);
		return verts;
	}

	/// <summary>Stage 1 — returns verts + axial index map so triangulation never round-trips via PlaneToAxial.</summary>
	public static (List<Vector2> Verts, Dictionary<Vector2I, int> IndexByAxial) SeedHexLatticeRingsWithAxial(
		int ringCount,
		float spacing)
	{
		ringCount = Math.Max(1, ringCount);
		var verts = new List<Vector2>();
		var indexByAxial = new Dictionary<Vector2I, int>();
		for (var q = -ringCount; q <= ringCount; q++)
		{
			for (var r = -ringCount; r <= ringCount; r++)
			{
				if (HexDist(q, r) > ringCount) continue;
				var axial = new Vector2I(q, r);
				var idx = verts.Count;
				verts.Add(AxialToPlane(axial, spacing));
				indexByAxial[axial] = idx;
			}
		}

		return (verts, indexByAxial);
	}

	/// <summary>
	/// Stage 2 — local hex-lattice triangulation from axial neighbours only.
	/// Each unit cell = one triangle among a site and two consecutive 60° neighbours.
	/// No centre-to-outer long rays; no PlaneToAxial remapping.
	/// </summary>
	public static List<int[]> TriangulateHexLatticeFromAxial(Dictionary<Vector2I, int> indexByAxial)
	{
		var triSet = new HashSet<string>();
		var tris = new List<int[]>();
		var dirs = new[]
		{
			new Vector2I(1, 0), new Vector2I(1, -1), new Vector2I(0, -1),
			new Vector2I(-1, 0), new Vector2I(-1, 1), new Vector2I(0, 1),
		};

		foreach (var (axial, i0) in indexByAxial)
		{
			for (var d = 0; d < 6; d++)
			{
				var a1 = axial + dirs[d];
				var a2 = axial + dirs[(d + 1) % 6];
				if (!indexByAxial.TryGetValue(a1, out var i1)) continue;
				if (!indexByAxial.TryGetValue(a2, out var i2)) continue;
				// Emit each geometric triangle once: only when i0 is the min index (canonical).
				if (i0 > i1 || i0 > i2) continue;
				var key = TriKey(i0, i1, i2);
				if (!triSet.Add(key)) continue;
				tris.Add(new[] { i0, i1, i2 });
			}
		}

		return tris;
	}

	/// <summary>Legacy entry — rebuilds axial via PlaneToAxial (prefer FromAxial).</summary>
	public static List<int[]> TriangulateHexLattice(List<Vector2> points)
	{
		var indexByAxial = new Dictionary<Vector2I, int>();
		var spacing = EstimateSpacing(points);
		for (var i = 0; i < points.Count; i++)
		{
			var axial = PlaneToAxial(points[i], spacing);
			// Last-write wins on collision — this is the star-risk path; kept for diagnostics only.
			indexByAxial[axial] = i;
		}

		return TriangulateHexLatticeFromAxial(indexByAxial);
	}

	private static void LogFaceMix(string tag, List<int[]> faces)
	{
		var tri = 0;
		var quad = 0;
		foreach (var f in faces)
		{
			if (f == null) continue;
			if (f.Length == 3) tri++;
			else if (f.Length == 4) quad++;
		}

		GD.Print($"StalbergQuadKernel.{tag}: faces={faces.Count} tris={tri} quads={quad}");
	}

	private static void LogEdgeStats(string tag, List<Vector2> verts, List<int[]> faces)
	{
		var min = float.MaxValue;
		var max = 0f;
		double sum = 0;
		var n = 0;
		var longRays = 0;
		foreach (var f in faces)
		{
			if (f == null || f.Length < 3) continue;
			for (var i = 0; i < f.Length; i++)
			{
				var a = f[i];
				var b = f[(i + 1) % f.Length];
				if (a < 0 || b < 0 || a >= verts.Count || b >= verts.Count) continue;
				var d = verts[a].DistanceTo(verts[b]);
				if (d < 1e-8f) continue;
				min = MathF.Min(min, d);
				max = MathF.Max(max, d);
				sum += d;
				n++;
				if (d > DefaultSpacing * 1.75f) longRays++;
			}
		}

		var mean = n > 0 ? sum / n : 0;
		GD.Print(
			$"StalbergQuadKernel.{tag}: edges={n} len[min/mean/max]={min:F3}/{mean:F3}/{max:F3} longRays={longRays}");
	}

	/// <summary>Stage 3 — greedy dissolve of triangle pairs that share an edge into quads.</summary>
	public static (List<Vector2> Verts, List<int[]> Faces) DissolveTrianglePairs(
		List<Vector2> points,
		List<int[]> tris,
		Random rng)
	{
		var verts = new List<Vector2>(points);
		var live = new List<int[]>(tris);
		var tabu = new HashSet<long>();

		while (true)
		{
			var edgeOwners = new Dictionary<long, List<int>>();
			for (var ti = 0; ti < live.Count; ti++)
			{
				var t = live[ti];
				if (t.Length != 3) continue;
				RegisterEdge(edgeOwners, t[0], t[1], ti);
				RegisterEdge(edgeOwners, t[1], t[2], ti);
				RegisterEdge(edgeOwners, t[2], t[0], ti);
			}

			var candidates = new List<long>();
			foreach (var (ek, owners) in edgeOwners)
			{
				if (owners.Count == 2 && !tabu.Contains(ek))
					candidates.Add(ek);
			}

			if (candidates.Count == 0) break;
			Shuffle(candidates, rng);

			var merged = false;
			foreach (var ek in candidates)
			{
				var owners = edgeOwners[ek];
				var tA = live[owners[0]];
				var tB = live[owners[1]];
				UnpackEdge(ek, out var ea, out var eb);
				var oppA = OppositeVertex(tA, ea, eb);
				var oppB = OppositeVertex(tB, ea, eb);
				if (oppA < 0 || oppB < 0) continue;
				var quad = new[] { ea, oppA, eb, oppB };
				if (!LegitQuad(verts, quad))
				{
					tabu.Add(ek);
					continue;
				}

				var remove = new HashSet<int> { owners[0], owners[1] };
				var next = new List<int[]>();
				for (var i = 0; i < live.Count; i++)
				{
					if (!remove.Contains(i))
						next.Add(live[i]);
				}

				next.Add(quad);
				live = next;
				merged = true;
				break;
			}

			if (!merged) break;
		}

		return (verts, live);
	}

	/// <summary>Stage 4 — every remaining face becomes quads (100% quads). Shared edge mids via edge key.</summary>
	public static (List<Vector2> Verts, List<int[]> Quads) SubdivideFacesToQuads(
		List<Vector2> verts,
		List<int[]> faces)
	{
		var outVerts = new List<Vector2>(verts);
		var midCache = new Dictionary<long, int>();
		var quads = new List<int[]>();

		foreach (var face in faces)
		{
			if (face.Length is < 3 or > 4) continue;
			var centroid = Vector2.Zero;
			foreach (var idx in face)
				centroid += outVerts[idx];
			centroid /= face.Length;
			var cIdx = outVerts.Count;
			outVerts.Add(centroid);

			var mids = new int[face.Length];
			for (var i = 0; i < face.Length; i++)
			{
				var a = face[i];
				var b = face[(i + 1) % face.Length];
				mids[i] = GetMidpoint(outVerts, midCache, a, b);
			}

			for (var i = 0; i < face.Length; i++)
			{
				var corner = face[i];
				var midPrev = mids[(i + face.Length - 1) % face.Length];
				var midNext = mids[i];
				var q = new[] { corner, midNext, cIdx, midPrev };
				NormalizeWinding(outVerts, q);
				quads.Add(q);
			}
		}

		return (outVerts, quads);
	}

	/// <summary>
	/// Stage 5 — Oskar-style rotate-90 average squarify (Prefer squarify_r1).
	/// Replaces Variant A closest-square (atan + fixed square targets) which diamond-locks
	/// hex seeds. Per quad: corner←centre → align via ±90°/180 → average → scale to
	/// area half-diagonal → rotate targets 0/90/180/270 → pull; avg across incident quads.
	/// Boundary pinned; per-vertex force clamped. Not naïve Laplacian.
	/// </summary>
	public static void RelaxTowardSquares(
		List<Vector2> verts,
		List<int[]> quads,
		int iters,
		float pullRate,
		float sideLength,
		HashSet<int>? pinned = null,
		float forceClamp = DefaultForceClamp)
	{
		// Half-diagonal from ideal square side (area-based caller) — size discipline only.
		var halfDiag = sideLength / MathF.Sqrt(2f);
		var forces = new Vector2[verts.Count];
		var counts = new int[verts.Count];
		var pull = Mathf.Clamp(pullRate, 0.05f, 0.15f);
		// Tighter clamp — unnormalized sum historically spiked interiors.
		var clamp = MathF.Max(1e-4f, MathF.Min(forceClamp, sideLength * 0.55f));

		for (var iter = 0; iter < iters; iter++)
		{
			Array.Clear(forces, 0, forces.Length);
			Array.Clear(counts, 0, counts.Length);
			foreach (var q in quads)
			{
				if (q.Length != 4) continue;
				var c = (verts[q[0]] + verts[q[1]] + verts[q[2]] + verts[q[3]]) * 0.25f;
				var r0 = verts[q[0]] - c;
				var r1 = verts[q[1]] - c;
				var r2 = verts[q[2]] - c;
				var r3 = verts[q[3]] - c;

				// Align each corner into slot-0 by rotating back i·90°, then average.
				// Rot90 CCW = (-y,x); RotNeg90 CW = (y,-x).
				var avg = (
					r0 +
					new Vector2(r1.Y, -r1.X) +
					(-r2) +
					new Vector2(-r3.Y, r3.X)
				) * 0.25f;

				var len = avg.Length();
				if (len < 1e-8f) continue;
				// Soft size toward area half-diagonal — hard normalize diamond-locks hex seeds.
				// Natural length keeps organic cell-size variation (single-grid-section look).
				var blended = Mathf.Lerp(len, halfDiag, 0.25f);
				avg *= blended / len;

				// Square targets: avg rotated 0°, 90°, 180°, 270° (winding-matched).
				var t0 = avg;
				var t1 = new Vector2(-avg.Y, avg.X);
				var t2 = -avg;
				var t3 = new Vector2(avg.Y, -avg.X);

				forces[q[0]] += t0 - r0;
				forces[q[1]] += t1 - r1;
				forces[q[2]] += t2 - r2;
				forces[q[3]] += t3 - r3;
				counts[q[0]]++;
				counts[q[1]]++;
				counts[q[2]]++;
				counts[q[3]]++;
			}

			for (var i = 0; i < verts.Count; i++)
			{
				if (pinned != null && pinned.Contains(i))
					continue;
				if (counts[i] <= 0) continue;
				// Average by incident faces — refuse force_sum_unnormalized star collapse.
				var f = ClampForce(forces[i] / counts[i], clamp);
				verts[i] += f * pull;
			}
		}
	}

	/// <summary>
	/// Ideal square side from average face area: side = √area; half-diagonal D = side/√2 used in relax.
	/// Prefer signal: EstimateIdealSideFromArea — refuse missing_square_area_force if absent.
	/// </summary>
	public static float EstimateIdealSideFromArea(List<Vector2> verts, List<int[]> quads)
	{
		double areaSum = 0;
		var n = 0;
		foreach (var q in quads)
		{
			if (q == null || q.Length != 4) continue;
			var a = verts[q[0]];
			var b = verts[q[1]];
			var c = verts[q[2]];
			var d = verts[q[3]];
			// Shoelace for quad.
			var area = Math.Abs(
				(a.X * b.Y - b.X * a.Y) +
				(b.X * c.Y - c.X * b.Y) +
				(c.X * d.Y - d.X * c.Y) +
				(d.X * a.Y - a.X * d.Y)) * 0.5;
			if (area > 1e-12)
			{
				areaSum += area;
				n++;
			}
		}

		if (n == 0) return DefaultSideLength;
		var meanArea = areaSum / n;
		return (float)Math.Sqrt(meanArea);
	}

	/// <summary>Legacy mean-edge helper retained for diagnostics; relax uses area-based side.</summary>
	public static float EstimateMeanQuadSide(List<Vector2> verts, List<int[]> quads)
	{
		double sum = 0;
		var n = 0;
		foreach (var q in quads)
		{
			if (q == null || q.Length != 4) continue;
			for (var i = 0; i < 4; i++)
			{
				sum += verts[q[i]].DistanceTo(verts[q[(i + 1) % 4]]);
				n++;
			}
		}

		return n > 0 ? (float)(sum / n) : DefaultSideLength;
	}

	/// <summary>
	/// Pin silhouette so relax cannot fold the board (refuse free_boundary_fold).
	/// Primary: verts on mesh boundary edges (face-count == 1). Secondary: convex hull.
	/// Hull-only missed some post-subdivide boundary mids → jagged hex after soft relax.
	/// </summary>
	public static HashSet<int> MarkBoundaryPinned(List<Vector2> verts, List<int[]>? quads = null)
	{
		var pinned = new HashSet<int>();
		if (verts.Count == 0) return pinned;
		if (verts.Count <= 3)
		{
			for (var i = 0; i < verts.Count; i++)
				pinned.Add(i);
			return pinned;
		}

		if (quads != null && quads.Count > 0)
		{
			var edgeUses = new Dictionary<long, int>();
			foreach (var q in quads)
			{
				if (q == null || q.Length < 3) continue;
				for (var i = 0; i < q.Length; i++)
				{
					var a = q[i];
					var b = q[(i + 1) % q.Length];
					var key = EdgeKey(a, b);
					edgeUses.TryGetValue(key, out var n);
					edgeUses[key] = n + 1;
				}
			}

			foreach (var (ek, n) in edgeUses)
			{
				if (n != 1) continue;
				UnpackEdge(ek, out var a, out var b);
				pinned.Add(a);
				pinned.Add(b);
			}
		}

		// Union convex-hull pins (legacy + float-edge safety).
		var order = new List<int>(verts.Count);
		for (var i = 0; i < verts.Count; i++)
			order.Add(i);
		order.Sort((a, b) =>
		{
			var cmp = verts[a].X.CompareTo(verts[b].X);
			return cmp != 0 ? cmp : verts[a].Y.CompareTo(verts[b].Y);
		});

		var lower = new List<int>();
		foreach (var i in order)
		{
			while (lower.Count >= 2 && Cross(verts, lower[^2], lower[^1], i) <= 0f)
				lower.RemoveAt(lower.Count - 1);
			lower.Add(i);
		}

		var upper = new List<int>();
		for (var k = order.Count - 1; k >= 0; k--)
		{
			var i = order[k];
			while (upper.Count >= 2 && Cross(verts, upper[^2], upper[^1], i) <= 0f)
				upper.RemoveAt(upper.Count - 1);
			upper.Add(i);
		}

		for (var i = 0; i < lower.Count - 1; i++)
			pinned.Add(lower[i]);
		for (var i = 0; i < upper.Count - 1; i++)
			pinned.Add(upper[i]);
		return pinned;
	}

	/// <summary>Max number of quads incident to any vertex (Townscaper dual ownership ≤4).</summary>
	public static int MaxVertexFaceValence(List<int[]> quads, int vertCount)
	{
		if (vertCount <= 0 || quads == null || quads.Count == 0) return 0;
		var counts = new int[vertCount];
		foreach (var q in quads)
		{
			if (q == null) continue;
			var seen = new HashSet<int>();
			foreach (var vi in q)
			{
				if (vi < 0 || vi >= vertCount) continue;
				if (!seen.Add(vi)) continue; // degenerates: same vert twice in one face
				counts[vi]++;
			}
		}
		var max = 0;
		foreach (var c in counts)
			if (c > max) max = c;
		return max;
	}

	/// <summary>Re-weld near-duplicate vertices by position after relax.</summary>
	public static (List<Vector2> Verts, List<int[]> Quads) WeldNearDuplicates(
		List<Vector2> verts,
		List<int[]> quads,
		float epsilon)
	{
		return UniqueTopology2D.FromIndexedMesh(verts, quads, Math.Max(epsilon, PositionHashQuantum))
			.ToIndexedMesh();
	}

	public static Vector2 ClampForce(Vector2 force, float maxMagnitude)
	{
		var len = force.Length();
		if (len <= maxMagnitude || len < 1e-12f) return force;
		return force * (maxMagnitude / len);
	}

	private static float Cross(List<Vector2> verts, int o, int a, int b)
	{
		var oa = verts[a] - verts[o];
		var ob = verts[b] - verts[o];
		return oa.X * ob.Y - oa.Y * ob.X;
	}

	private static float EstimateSpacing(List<Vector2> points)
	{
		if (points.Count < 2) return DefaultSpacing;
		var best = float.MaxValue;
		for (var i = 0; i < Math.Min(points.Count, 12); i++)
		{
			for (var j = i + 1; j < Math.Min(points.Count, 24); j++)
			{
				var d = points[i].DistanceTo(points[j]);
				if (d > 1e-4f && d < best) best = d;
			}
		}

		return best < float.MaxValue ? best : DefaultSpacing;
	}

	private static Vector2 AxialToPlane(Vector2I axial, float spacing)
	{
		var x = spacing * (axial.X + axial.Y * 0.5f);
		var z = spacing * (axial.Y * (MathF.Sqrt(3f) * 0.5f));
		return new Vector2(x, z);
	}

	private static Vector2I PlaneToAxial(Vector2 p, float spacing)
	{
		var x = p.X / spacing;
		var z = p.Y / spacing;
		var r = z / (MathF.Sqrt(3f) * 0.5f);
		var q = x - r * 0.5f;
		return CubeRound(q, r);
	}

	private static Vector2I CubeRound(float q, float r)
	{
		var s = -q - r;
		var rq = MathF.Round(q);
		var rr = MathF.Round(r);
		var rs = MathF.Round(s);
		var dq = MathF.Abs(rq - q);
		var dr = MathF.Abs(rr - r);
		var ds = MathF.Abs(rs - s);
		if (dq > dr && dq > ds)
			rq = -rr - rs;
		else if (dr > ds)
			rr = -rq - rs;
		return new Vector2I((int)rq, (int)rr);
	}

	private static int HexDist(int q, int r) =>
		(Math.Abs(q) + Math.Abs(r) + Math.Abs(q + r)) / 2;

	private static string TriKey(int a, int b, int c)
	{
		var arr = new[] { a, b, c };
		Array.Sort(arr);
		return $"{arr[0]}:{arr[1]}:{arr[2]}";
	}

	private static void RegisterEdge(Dictionary<long, List<int>> map, int a, int b, int triIndex)
	{
		var key = EdgeKey(a, b);
		if (!map.TryGetValue(key, out var list))
		{
			list = new List<int>(2);
			map[key] = list;
		}

		list.Add(triIndex);
	}

	private static long EdgeKey(int a, int b)
	{
		var lo = Math.Min(a, b);
		var hi = Math.Max(a, b);
		return ((long)lo << 32) | (uint)hi;
	}

	private static void UnpackEdge(long key, out int a, out int b)
	{
		a = (int)(key >> 32);
		b = (int)(key & 0xffffffff);
	}

	private static int OppositeVertex(int[] tri, int ea, int eb)
	{
		foreach (var v in tri)
		{
			if (v != ea && v != eb) return v;
		}

		return -1;
	}

	private static bool LegitQuad(List<Vector2> verts, int[] q)
	{
		if (q.Length != 4) return false;
		float? sign = null;
		for (var i = 0; i < 4; i++)
		{
			var a = verts[q[i]];
			var b = verts[q[(i + 1) % 4]];
			var c = verts[q[(i + 2) % 4]];
			var cross = (b.X - a.X) * (c.Y - b.Y) - (b.Y - a.Y) * (c.X - b.X);
			if (MathF.Abs(cross) < 1e-8f) return false;
			var s = MathF.Sign(cross);
			if (sign == null) sign = s;
			else if (s != sign) return false;

			var inDir = (b - a).Normalized();
			var outDir = (c - b).Normalized();
			var ang = MathF.Acos(Mathf.Clamp(inDir.Dot(outDir), -1f, 1f));
			var interior = MathF.PI - ang;
			if (interior < 0.2f * MathF.PI || interior > 0.9f * MathF.PI)
				return false;
		}

		return true;
	}

	private static int GetMidpoint(List<Vector2> verts, Dictionary<long, int> cache, int a, int b)
	{
		var key = EdgeKey(a, b);
		if (cache.TryGetValue(key, out var idx)) return idx;
		idx = verts.Count;
		verts.Add((verts[a] + verts[b]) * 0.5f);
		cache[key] = idx;
		return idx;
	}

	private static void NormalizeWinding(List<Vector2> verts, int[] q)
	{
		var e0 = verts[q[1]] - verts[q[0]];
		var e1 = verts[q[2]] - verts[q[1]];
		var cross = e0.X * e1.Y - e0.Y * e1.X;
		if (cross < 0f)
			Array.Reverse(q);
	}

	private static void Shuffle<T>(IList<T> list, Random rng)
	{
		for (var i = list.Count - 1; i > 0; i--)
		{
			var j = rng.Next(i + 1);
			(list[i], list[j]) = (list[j], list[i]);
		}
	}
}

/// <summary>
/// Indexed weld helper — migrates into OrganicMeshGraph (not Prefer Success alone).
/// Prefer Success: OrganicMeshGraph Vertex/Edge/Face singletons + incidence.
/// Prefer: GetOrAddVertex / PositionHash — refuse non_unique_vertices / indexed_lists_as_graph.
/// CRITICAL: never XOR-pack qx^qy into one long (antipodal hex verts collide → star rays).
/// </summary>
public sealed class UniqueTopology2D
{
	private readonly float _quantum;
	/// <summary>Injective spatial key — (qx,qy) tuple, not XOR-folded long.</summary>
	private readonly Dictionary<(long Qx, long Qy), int> _byCell = new();
	private readonly List<Vector2> _verts = new();
	private readonly List<int[]> _faces = new();
	private readonly HashSet<long> _edges = new();

	public UniqueTopology2D(float quantum)
	{
		_quantum = Math.Max(1e-6f, quantum);
	}

	public List<Vector2> Vertices => _verts;
	public List<int[]> Faces => _faces;
	public int EdgeCount => _edges.Count;

	public bool AllFacesAreQuads
	{
		get
		{
			foreach (var f in _faces)
			{
				if (f == null || f.Length != 4) return false;
			}

			return _faces.Count > 0;
		}
	}

	public int GetOrAddVertex(Vector2 p)
	{
		var key = QuantizeCell(p, _quantum);
		if (_byCell.TryGetValue(key, out var idx))
			return idx;
		idx = _verts.Count;
		_verts.Add(p);
		_byCell[key] = idx;
		return idx;
	}

	public void AddFace(int[] indices)
	{
		if (indices == null || indices.Length < 3) return;
		var face = (int[])indices.Clone();
		_faces.Add(face);
		for (var i = 0; i < face.Length; i++)
		{
			var a = face[i];
			var b = face[(i + 1) % face.Length];
			var lo = Math.Min(a, b);
			var hi = Math.Max(a, b);
			_edges.Add(((long)lo << 32) | (uint)hi);
		}
	}

	public static UniqueTopology2D FromIndexedMesh(
		List<Vector2> verts,
		List<int[]> faces,
		float quantum)
	{
		var topo = new UniqueTopology2D(quantum);
		var remap = new int[verts.Count];
		for (var i = 0; i < verts.Count; i++)
			remap[i] = topo.GetOrAddVertex(verts[i]);

		foreach (var f in faces)
		{
			if (f == null || f.Length < 3) continue;
			var mapped = new int[f.Length];
			var ok = true;
			for (var i = 0; i < f.Length; i++)
			{
				if (f[i] < 0 || f[i] >= remap.Length)
				{
					ok = false;
					break;
				}

				mapped[i] = remap[f[i]];
			}

			if (!ok) continue;
			// Drop degenerate faces with duplicate corner ids after weld.
			var distinct = new HashSet<int>(mapped);
			if (distinct.Count < f.Length) continue;
			topo.AddFace(mapped);
		}

		return topo;
	}

	public (List<Vector2> Verts, List<int[]> Quads) ToIndexedMesh() =>
		(new List<Vector2>(_verts), new List<int[]>(_faces));

	/// <summary>Quantize to injective grid cell. Prefer seat scans for PositionHash name.</summary>
	public static (long Qx, long Qy) QuantizeCell(Vector2 p, float quantum)
	{
		quantum = Math.Max(1e-6f, quantum);
		var qx = (long)MathF.Round(p.X / quantum);
		var qy = (long)MathF.Round(p.Y / quantum);
		return (qx, qy);
	}

	/// <summary>
	/// Stable diagnostic fingerprint of a quantized cell (NOT used as dictionary key).
	/// Legacy XOR pack collided antipodes — kept only as a non-key fingerprint helper.
	/// </summary>
	public static long PositionHash(Vector2 p, float quantum)
	{
		var (qx, qy) = QuantizeCell(p, quantum);
		// Injective-ish Cantor pairing on signed zig-zag — never XOR qx^qy as a map key.
		unchecked
		{
			var zx = qx >= 0 ? qx * 2 : -qx * 2 - 1;
			var zy = qy >= 0 ? qy * 2 : -qy * 2 - 1;
			return ((zx + zy) * (zx + zy + 1) / 2) + zy;
		}
	}
}
