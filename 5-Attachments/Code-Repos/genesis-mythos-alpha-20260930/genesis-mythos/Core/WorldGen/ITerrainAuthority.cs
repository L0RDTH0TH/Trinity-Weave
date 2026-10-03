using System.Collections.Generic;
using Godot;

namespace Genesis.Core.WorldGen;

/// <summary>
/// World/height authority — Matrix Prefer: Terrain3D as sole height authority.
/// Dual-grid world craft: Terrain3D height + GridMap craft overlay; Never a second
/// parallel terrain/physics/voxel authority. Prefer r3: layers stay split under craft
/// (Hot Wheels toys) vs Sparky (fed real-car Terrain3D).
/// </summary>
public interface ITerrainAuthority
{
	string BackendId { get; }
	bool VendorPresent { get; }
	bool ClassDbReady { get; }
	bool IsDegraded { get; }
	/// <summary>True when a live Terrain3D node is mounted (ClassDB Prefer — not Multimesh stand-in).</summary>
	bool LiveMeshArmed { get; }
	/// <summary>True after at least one successful set_height → update_maps vendor push.</summary>
	bool HasVendorHeightFeed { get; }
	int VendorPushCount { get; }

	Error EnsureHost(Node3D parent);
	Error SetCellHeight(Vector2I cell, float height);
	float GetCellHeight(Vector2I cell);
	Error ImportHeightField(float[,] heights, Vector3 worldOrigin);
	/// <summary>
	/// Canonical Prefer stamp heights for <c>stamp_oasis_desert</c> — must push into Terrain3D.
	/// Multimesh/graybox-only = fail <c>graybox_only_world</c>.
	/// </summary>
	Error ApplyStampOasisDesertHeights(Vector2I center, int radius = 4);
	/// <summary>
	/// Deferred Prefer feed: push craft tile map → Terrain3D in one batch (Sparky enter /
	/// explicit feed). Not called on live craft place (refuse <c>craft_terrain_blend</c>).
	/// </summary>
	Error FeedFromCraftCells(IReadOnlyDictionary<Vector2I, CraftCellType> cells);
	/// <summary>
	/// Hide Terrain3D under craft (Hot Wheels toys only); show under Sparky after feed.
	/// Refuse <c>craft_terrain_blend</c>.
	/// </summary>
	void SetVisibleForCraftPhase(bool craftPhaseActive);
	Error FlushVendorMaps();
	Aabb GetTerrainBounds();
}
