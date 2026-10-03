using System.Collections.Generic;
using Genesis.Core.ClosedAlpha;
using Genesis.Systems;
using Godot;

namespace Genesis;

/// <summary>
/// Launch-path shim — LaunchShell → PlayRegion → <c>res://scenes/WorldgenCraft.tscn</c>.
/// Tutorial s1 hex-19 occupancy + ghost + grid toggle; Terrain3D deferred; dual Success stripped.
/// </summary>
public partial class PlayRegion : Node3D
{
	public override void _Ready()
	{
		AlphaFactoryLog.ConfigureRuntimePath();
		AlphaFactoryLog.Emit(
			"ui.boundary",
			"Flow_Launch",
			"PlayRegion handoff → WorldgenCraft.tscn (tutorial s1 occupancy entry)",
			new Dictionary<string, object>
			{
				["slice_id"] = WorldgenCraft.SliceId,
				["weld_slice_id"] = WorldgenCraft.WeldSliceId,
				["ask_id"] = WorldgenCraft.PreferAskId,
				["half_b_overlay"] = WorldgenCraft.HalfBOverlay,
				["ux_bullet"] = "UX-1",
				["ux7"] = "UX-7",
				["target"] = WorldgenCraft.ScenePath,
				["visual_bar"] = DualGridCraftHost.VisualBarCite,
				["terrain3d"] = "hard_disabled_under_craft",
			});

		var err = GetTree().ChangeSceneToFile(WorldgenCraft.ScenePath);
		if (err != Error.Ok)
		{
			AlphaFactoryLog.Emit(
				"Degrade_FailVisible",
				"Flow_Launch",
				$"ChangeSceneToFile({WorldgenCraft.ScenePath}) failed: {err}",
				level: "error");
		}
	}
}
