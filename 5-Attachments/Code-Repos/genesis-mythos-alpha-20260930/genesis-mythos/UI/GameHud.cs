using System;
using System.Collections.Generic;
using Genesis.Camera;
using Genesis.Core.ClosedAlpha;
using Genesis.Systems;
using Godot;

namespace Genesis.UI;

/// <summary>
/// Player-facing play HUD for worldgen craft → sparky handoff.
/// No sim logic — reflective chrome + perspective shell hints only.
/// </summary>
public partial class GameHud : CanvasLayer
{
	private Label? _statusLabel;
	private Label? _feedbackLabel;
	private Label? _modeLabel;
	private Label? _helpLabel;
	private PanelContainer? _degradationBanner;
	private Label? _degradationLabel;
	private PanelContainer? _craftControls;
	private string? _lastPerspectiveHint;
	private bool _sparkyMode;

	public override void _Ready()
	{
		AlphaFactoryLog.ConfigureRuntimePath();

		_statusLabel = GetNodeOrNull<Label>("%StatusLabel");
		_feedbackLabel = GetNodeOrNull<Label>("%FeedbackLabel");
		_modeLabel = GetNodeOrNull<Label>("%ModeLabel");
		_helpLabel = GetNodeOrNull<Label>("%HelpLabel");
		_degradationBanner = GetNodeOrNull<PanelContainer>("%DegradationBanner");
		_degradationLabel = GetNodeOrNull<Label>("%DegradationLabel");
		_craftControls = GetNodeOrNull<PanelContainer>("%CraftControls");

		if (_degradationBanner != null)
			_degradationBanner.Visible = false;

		ApplyPlayerFacingChrome();
		AuditVisibleCopy();

		// Decorative chrome must not steal craft LMB (gui_input_steal).
		if (GetNodeOrNull<Control>("Root") is { } root)
			PropagateMouseIgnoreExceptInteractive(root);

		AlphaFactoryLog.Emit(
			"ui.boundary",
			"Flow_Launch",
			"GameHud ready — UX-1 worldgen chrome visible",
			new Dictionary<string, object>
			{
				["slice_id"] = "row_ux_world_generation_r1_d1",
				["weld_slice_id"] = DualGridCraftHost.WeldSliceId,
				["ux_bullet"] = "UX-1",
				["lane_id"] = "presentation",
				["checklist"] = new[] { "Flow_Launch", "Anti_DevOnlyHUD", "Flow_DM_Mode", "Nav_LookWhileMove_DM" },
			});
	}

	private static void PropagateMouseIgnoreExceptInteractive(Node node)
	{
		if (node is Control control and not BaseButton)
			control.MouseFilter = Control.MouseFilterEnum.Ignore;
		foreach (var child in node.GetChildren())
			PropagateMouseIgnoreExceptInteractive(child);
	}

	public override void _UnhandledInput(InputEvent @event)
	{
		// Reflect Tab for HUD only — do not consume (PlayRegion owns craft↔sparky).
		if (@event is InputEventKey { Pressed: true, Echo: false, Keycode: Key.Tab })
			CallDeferred(nameof(SyncPerspectiveFromWorld));
	}

	public void SetStatus(string text)
	{
		if (_statusLabel != null)
			_statusLabel.Text = text;
	}

	public void SetFeedback(string text)
	{
		if (_feedbackLabel != null)
			_feedbackLabel.Text = text;
	}

	public bool HasPerspectiveDiscoverabilityHint =>
		_statusLabel?.Text.Contains("Tab", StringComparison.OrdinalIgnoreCase) == true;

	/// <summary>Player-facing perspective shell hint API (Anti_DevOnlyHUD / Flow_DM_Mode).</summary>
	public void SetPerspectiveShellHint(string hintText)
	{
		SetStatus(hintText);
		_sparkyMode = hintText.Contains("SPARKY", StringComparison.OrdinalIgnoreCase);
		if (_modeLabel != null)
			_modeLabel.Text = _sparkyMode ? "MODE · SPARKY" : "MODE · CRAFT";

		if (_craftControls != null)
			_craftControls.Visible = !_sparkyMode;

		EmitPerspectiveBoundary(hintText);
	}

	/// <summary>
	/// Sync chrome from module sparky rig after Tab — avoids claiming SPARKY when
	/// PlayRegion refused handoff (world does not exist yet).
	/// </summary>
	private void SyncPerspectiveFromWorld()
	{
		var sparky = FindSparkyRig();
		if (sparky != null && sparky.InputEnabled)
		{
			SetPerspectiveShellHint(
				"SPARKY inspect/fly — WASD + mouse · Tab returns to craft");
			SetFeedback("Inspect the living world. Tab returns to craft authorship.");
			return;
		}

		SetPerspectiveShellHint("CRAFT cam — LMB place · RMB remove @ cursor · WASD pan");
		SetFeedback("Author dual-grid tiles under craft cam — stylized craft toys, not debug candy.");
	}

	private SparkyDmFreeCamRig? FindSparkyRig()
	{
		return GetTree()?.Root?.FindChild("SparkyDmFreeCamRig", recursive: true, owned: false)
			as SparkyDmFreeCamRig;
	}

	private void ApplyPlayerFacingChrome()
	{
		if (_helpLabel != null)
		{
			_helpLabel.Text =
				"Craft: LMB place · RMB remove @ cursor · WASD pan · 1/2 brush · F6 stamp_oasis_desert · F5 persist · G seed";
		}

		var tone = GetTree()?.Root?.HasMeta("worldgen_tone_profile") == true
			? GetTree()!.Root.GetMeta("worldgen_tone_profile").AsString()
			: null;
		SetPerspectiveShellHint(string.IsNullOrEmpty(tone)
			? "CRAFT cam — LMB place · RMB remove @ cursor · WASD pan"
			: $"CRAFT · {tone} — LMB place · RMB remove @ cursor · WASD pan");
		SetFeedback(string.IsNullOrEmpty(tone)
			? "Author dual-grid tiles under craft cam — stylized craft toys, not debug candy."
			: $"Living-world scaffold ({tone}) accepted — author dual-grid craft tiles.");
	}

	private void AuditVisibleCopy()
	{
		// CDC product copy is content-lane; bootstrap-only CDC → visible degradation, safe chrome.
		var cdcOk = Godot.FileAccess.FileExists("res://content/_factory/manifest.yaml");
		if (!cdcOk)
		{
			ShowDegradation("Content drops unavailable — HUD using safe presentation defaults.");
			return;
		}

		AlphaFactoryLog.Emit(
			"ui.boundary",
			"Anti_DevOnlyHUD",
			"Play HUD player-facing — depends_on_cdc satisfied; no dev-only success path",
			new Dictionary<string, object> { ["ux_bullet"] = "UX-1" });
	}

	private void ShowDegradation(string message)
	{
		if (_degradationBanner != null)
			_degradationBanner.Visible = true;
		if (_degradationLabel != null)
			_degradationLabel.Text = message;

		AlphaFactoryLog.Emit(
			"Degrade_FailVisible",
			"Anti_DevOnlyHUD",
			message,
			level: "warn");
	}

	private void EmitPerspectiveBoundary(string hint)
	{
		if (string.Equals(hint, _lastPerspectiveHint, StringComparison.Ordinal))
			return;

		_lastPerspectiveHint = hint;
		var detail = hint.Contains("SPARKY", StringComparison.OrdinalIgnoreCase)
			? "Perspective shell hint — sparky inspect/fly active"
			: "Perspective shell hint — craft authorship cam active";

		AlphaFactoryLog.Emit(
			"ui.boundary",
			"Flow_DM_Mode",
			detail,
			new Dictionary<string, object> { ["hint"] = hint, ["ux_bullet"] = "UX-1" });
	}
}
