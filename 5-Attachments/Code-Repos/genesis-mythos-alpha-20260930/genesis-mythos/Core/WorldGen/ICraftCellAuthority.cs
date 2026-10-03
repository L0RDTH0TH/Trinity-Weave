using System.Collections.Generic;
using Godot;

namespace Genesis.Core.WorldGen;

/// <summary>
/// Craft-plane occupancy authority — cells are FACES of the craft lattice graph
/// (OrganicQuadMesh quads for Stålberg Prefer; Hex19 scaffold is tutorial-only / not Success).
/// Not a height/terrain authority. Terrain3D Prefer is out of scope for craft-core.
/// Prefer hard law: refuse craft_cam_recenter_on_place — interface does not move cameras.
/// Prefer hard law: refuse craft_terrain_blend — no Terrain3D height authority here.
/// Prefer hard law: refuse points_as_grid — a cell is its corners, not a marker.
/// Prefer hard law: refuse hex19_pick_as_craft_authority when organic board is Success.
/// </summary>
public enum CraftCellType : int
{
	Empty = 0,
	Grass = 1,
	Desert = 2,
	Oasis = 3,
}

/// <summary>Binary occupancy fill for a hex lattice cell (depth widens in later steps).</summary>
public enum CellFill : int
{
	Empty = 0,
	Filled = 1,
}

public interface ICraftCellAuthority
{
	Error EnsureHost(Node3D parent);

	/// <summary>
	/// Set occupancy on one lattice cell (face of the craft graph).
	/// Stålberg craft-plane: cell.X = OrganicQuadMesh face index; cell.Y = 0.
	/// </summary>
	Error SetCellFill(Vector2I cell, CellFill fill);

	CellFill GetCellFill(Vector2I cell);

	/// <summary>Compat: maps typed brush onto cell occupancy (Empty clears; any non-Empty fills).</summary>
	Error PaintCell(Vector2I cell, CraftCellType type, float? raiseDelta = null);

	CraftCellType GetCellType(Vector2I cell);

	/// <summary>Tile-only scaffold stamp — no Terrain3D height path (craft-core).</summary>
	Error ApplyStampOasisDesert(Vector2I center, int radius = 2);

	IReadOnlyDictionary<Vector2I, CellFill> SnapshotCellFills();

	/// <summary>Legacy typed snapshot — filled cells map to Grass for deferred consumers (not armed under craft).</summary>
	IReadOnlyDictionary<Vector2I, CraftCellType> SnapshotCells();

	int PaintedCellCount { get; }
	bool WorldExists { get; }
	Error Persist(string path);
	Error Load(string path);
}
