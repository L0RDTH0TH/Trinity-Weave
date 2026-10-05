using Genesis.Core.ClosedAlpha;
using Godot;

namespace Genesis.Player;

/// <summary>
/// Craft focus / table cursor anchor — not an FPS mover.
/// Hosts select cameras; this node only marks craft orbit focus + ray pick plane.
/// Orbit focus + legacy rect snap helper. Tutorial s1 hex-19 pick lives on DualGridCraftHost.TryPickHexPoint.
/// </summary>
public partial class CraftFocusAnchor : Node3D
{
	[Export] public float PickPlaneY { get; set; } = 0f;

	public Vector2I WorldToLogicPoint(Vector3 world) =>
		new(Mathf.RoundToInt(world.X), Mathf.RoundToInt(world.Z));

	/// <summary>Legacy alias — logic point lattice (not floor-cell).</summary>
	public Vector2I WorldToCell(Vector3 world) => WorldToLogicPoint(world);

	public Vector3 LogicPointToWorld(Vector2I point) =>
		new(point.X, PickPlaneY, point.Y);

	public Vector3 CellToWorld(Vector2I cell) => LogicPointToWorld(cell);

	/// <summary>
	/// Mouse-cursor ray → nearest dual-grid logic point.
	/// Does <b>not</b> move GlobalPosition (refuse <c>craft_cam_recenter_on_place</c>).
	/// </summary>
	public bool TryPickCell(Camera3D camera, Vector2 screenPos, out Vector2I cell)
	{
		cell = default;
		var from = camera.ProjectRayOrigin(screenPos);
		var dir = camera.ProjectRayNormal(screenPos);
		if (Mathf.IsZeroApprox(dir.Y))
			return false;
		var t = (PickPlaneY - from.Y) / dir.Y;
		if (t < 0f) return false;
		var hit = from + dir * t;
		cell = WorldToLogicPoint(hit);
		return true;
	}
}
