using System.Collections.Generic;
using Genesis.Core.ClosedAlpha;
using Genesis.Systems;
using Godot;

namespace Genesis.UI;

/// <summary>
/// PDC craft chrome drop for module consume (PlayRegion instances this scene).
/// Reflective hints only — no sim / paint / camera ownership.
/// </summary>
public partial class WorldgenCraftControls : Control
{
	private Label? _hint;

	public override void _Ready()
	{
		AlphaFactoryLog.ConfigureRuntimePath();

		// Ignore all pointer hit-tests — craft LMB must reach the 3D viewport (gui_input_steal).
		MouseFilter = Control.MouseFilterEnum.Ignore;
		PropagateMouseIgnore(this);

		_hint = GetNodeOrNull<Label>("Banner/Margin/Hint");
		if (_hint != null)
		{
			_hint.Text =
				"Craft authorship — LMB place · RMB remove @ cursor · WASD pan · 1/2 brush · " +
				"F6 stamp_oasis_desert · F5 persist · I import/attach";
		}

		AlphaFactoryLog.Emit(
			"ui.boundary",
			"Flow_Launch",
			"PDC WorldgenCraftControls mounted — player-facing craft chrome (no sim)",
			new Dictionary<string, object>
			{
				["slice_id"] = "row_ux_world_generation_r1_d6",
				["weld_slice_id"] = DualGridCraftHost.WeldSliceId,
				["ux_bullet"] = "UX-1",
				["lane_id"] = "presentation",
				["checklist"] = new[] { "Flow_Launch", "Anti_DevOnlyHUD", "Flow_DM_Mode" },
			});
		AlphaFactoryLog.Emit(
			"ui.boundary",
			"Anti_DevOnlyHUD",
			"WorldgenCraftControls mouse_filter=Ignore — craft pointer not stolen by chrome");
	}

	private static void PropagateMouseIgnore(Node node)
	{
		if (node is Control control)
			control.MouseFilter = Control.MouseFilterEnum.Ignore;
		foreach (var child in node.GetChildren())
			PropagateMouseIgnore(child);
	}
}
