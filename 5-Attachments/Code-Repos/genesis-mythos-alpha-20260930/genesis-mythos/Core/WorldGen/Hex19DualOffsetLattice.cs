using System;
using System.Collections.Generic;
using Godot;

namespace Genesis.Core.WorldGen;

/// <summary>
/// Tutorial s2 — dual lattice as HALF-STEP OFFSET quads over the hex-19 occupancy sites.
///
/// Algorithm structure (oskar-procedure docs/03, re-implemented for our hex-19 scaffold):
/// - Occupancy sites hold corner-state (player paint).
/// - Each dual cell is the skewed-square whose four corners are occupancy sites
///   (q,r), (q+1,r), (q,r+1), (q+1,r+1); centre sits half-step between them.
/// - One occupancy edit → UPDATE-FOUR: refresh the four dual cells that list that site
///   as a corner (not a global rebuild, not per-occupancy marker spray).
/// - 4 corner bits → 16 configs → 6 tile families under square symmetry (graybox height only).
///
/// Refuse skip_dual_offset when this lattice is absent or when duals are points-only markers.
/// Does NOT pull docs/02 tri→dissolve→subdivide→relax (later product only).
/// </summary>
public static class Hex19DualOffsetLattice
{
	public const int DualSlotsPerOccupancy = 4;
	public const int CornersPerDual = 4;

	/// <summary>
	/// Axial offsets of the four corners of a dual cell whose origin is the SW corner.
	/// Order: SW, SE, NW, NE — corner-state read order for family lookup.
	/// </summary>
	public static readonly Vector2I[] CornerAxialOffsets =
	{
		new(0, 0),
		new(1, 0),
		new(0, 1),
		new(1, 1),
	};

	/// <summary>
	/// Dual origins relative to an occupancy site so that site is one of the four corners.
	/// Exactly four — the update-four set.
	/// </summary>
	private static readonly Vector2I[] DualOriginsRelativeToOccupancy =
	{
		new(0, 0),   // site is SW corner
		new(-1, 0),  // site is SE corner
		new(0, -1),  // site is NW corner
		new(-1, -1), // site is NE corner
	};

	public readonly struct DualCell
	{
		public DualCell(Vector2I origin, Vector3 localCentre, Vector2I[] corners)
		{
			Origin = origin;
			LocalCentre = localCentre;
			Corners = corners;
		}

		/// <summary>SW corner axial key — unique dual identity.</summary>
		public Vector2I Origin { get; }

		/// <summary>Half-step centre between the four occupancy corners.</summary>
		public Vector3 LocalCentre { get; }

		/// <summary>Four occupancy sites sampled by this dual (length 4).</summary>
		public Vector2I[] Corners { get; }

		public string Key => $"{Origin.X}_{Origin.Y}";
	}

	/// <summary>
	/// Resolve a dual cell at the given SW origin. Corners outside hex-19 snap to the
	/// nearest in-lattice occupancy so every dual always has four corner values.
	/// </summary>
	public static DualCell DualAt(Vector2I origin, float hexSize = Hex19OccupancyLattice.DefaultSize)
	{
		var corners = new Vector2I[CornersPerDual];
		var sum = Vector3.Zero;
		for (var i = 0; i < CornersPerDual; i++)
		{
			var raw = origin + CornerAxialOffsets[i];
			var resolved = Hex19OccupancyLattice.Contains(raw)
				? raw
				: NearestInLattice(Hex19OccupancyLattice.AxialToLocal(raw, hexSize), hexSize);
			corners[i] = resolved;
			sum += Hex19OccupancyLattice.AxialToLocal(resolved, hexSize);
		}

		var centre = sum / CornersPerDual;
		return new DualCell(origin, centre, corners);
	}

	/// <summary>
	/// The four dual cells that touch one occupancy site (update-four set).
	/// Always length 4 — structural proof of corner-driven local rebuild.
	/// </summary>
	public static DualCell[] DualCellsTouching(
		Vector2I occupancy,
		float hexSize = Hex19OccupancyLattice.DefaultSize)
	{
		var cells = new DualCell[DualSlotsPerOccupancy];
		for (var i = 0; i < DualSlotsPerOccupancy; i++)
		{
			var origin = occupancy + DualOriginsRelativeToOccupancy[i];
			cells[i] = DualAt(origin, hexSize);
		}
		return cells;
	}

	/// <summary>Backward-compatible name — same as <see cref="DualCellsTouching"/>.</summary>
	public static DualCell[] DualSlotsAround(
		Vector2I occupancy,
		float hexSize = Hex19OccupancyLattice.DefaultSize) =>
		DualCellsTouching(occupancy, hexSize);

	/// <summary>Four occupancy corner samples for a dual cell (explicit, not nearest-guess).</summary>
	public static Vector2I[] CornerOccupancySamples(DualCell cell) => cell.Corners;

	public static Vector2I NearestInLattice(Vector3 local, float hexSize = Hex19OccupancyLattice.DefaultSize)
	{
		var fq = (Mathf.Sqrt(3f) / 3f * local.X - 1f / 3f * local.Z) / hexSize;
		var fr = (2f / 3f * local.Z) / hexSize;
		var q = Mathf.RoundToInt(fq);
		var r = Mathf.RoundToInt(fr);
		var s = Mathf.RoundToInt(-fq - fr);
		var dq = Mathf.Abs(q - fq);
		var dr = Mathf.Abs(r - fr);
		var ds = Mathf.Abs(s + fq + fr);
		if (dq > dr && dq > ds)
			q = -r - s;
		else if (dr > ds)
			r = -q - s;
		var axial = new Vector2I(q, r);
		if (Hex19OccupancyLattice.Contains(axial))
			return axial;

		var best = Hex19OccupancyLattice.Vertices[0];
		var bestDist = float.MaxValue;
		foreach (var v in Hex19OccupancyLattice.Vertices)
		{
			var d = Hex19OccupancyLattice.AxialToLocal(v, hexSize).DistanceSquaredTo(local);
			if (d < bestDist)
			{
				bestDist = d;
				best = v;
			}
		}
		return best;
	}

	/// <summary>
	/// Unique dual cells for the hex-19 scaffold — union of update-four sets over all
	/// occupancy sites (deduped by origin). Not 19×4 overlapping markers.
	/// </summary>
	public static List<DualCell> AllDualCells(float hexSize = Hex19OccupancyLattice.DefaultSize)
	{
		var map = new Dictionary<string, DualCell>();
		foreach (var cell in Hex19OccupancyLattice.Cells)
		{
			foreach (var dual in DualCellsTouching(cell.Axial, hexSize))
				map[dual.Key] = dual;
		}
		return new List<DualCell>(map.Values);
	}

	/// <summary>Backward-compatible name for overlay seed.</summary>
	public static List<DualCell> AllDualSlots(float hexSize = Hex19OccupancyLattice.DefaultSize) =>
		AllDualCells(hexSize);

	public static int CountFilledCorners(DualCell cell, Func<Vector2I, bool> isFilled)
	{
		var n = 0;
		foreach (var c in cell.Corners)
		{
			if (isFilled(c))
				n++;
		}
		return n;
	}

	/// <summary>
	/// Six tile families under square symmetry (docs/03) — graybox index only.
	/// 0 empty, 1 one-corner, 2 edge (adjacent), 3 saddle (diagonal), 4 three, 5 full.
	/// </summary>
	public static int TileFamilyIndex(DualCell cell, Func<Vector2I, bool> isFilled)
	{
		var bits = 0;
		for (var i = 0; i < CornersPerDual; i++)
		{
			if (isFilled(cell.Corners[i]))
				bits |= 1 << i;
		}
		return bits switch
		{
			0b0000 => 0,
			0b0001 or 0b0010 or 0b0100 or 0b1000 => 1,
			0b0011 or 0b0101 or 0b1010 or 0b1100 => 2, // adjacent pairs
			0b0110 or 0b1001 => 3, // diagonal saddle
			0b0111 or 0b1011 or 0b1101 or 0b1110 => 4,
			0b1111 => 5,
			_ => CountFilledCorners(cell, isFilled) >= 2 ? 2 : 1,
		};
	}

	/// <summary>
	/// True when dual centre is spatially offset from every occupancy site centre
	/// (half-step proof — refuse dual coincident with occupancy markers).
	/// </summary>
	public static bool IsHalfStepOffset(DualCell cell, float hexSize = Hex19OccupancyLattice.DefaultSize)
	{
		const float eps = 1e-4f;
		foreach (var v in Hex19OccupancyLattice.Vertices)
		{
			var occ = Hex19OccupancyLattice.AxialToLocal(v, hexSize);
			if (cell.LocalCentre.DistanceSquaredTo(occ) < eps)
				return false;
		}
		return true;
	}

	/// <summary>How many of the four corner axials are distinct (interior duals → 4).</summary>
	public static int DistinctCornerCount(DualCell cell)
	{
		var set = new HashSet<Vector2I>();
		foreach (var c in cell.Corners)
			set.Add(c);
		return set.Count;
	}
}
