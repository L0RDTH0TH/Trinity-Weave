using System.Collections.Generic;
using Genesis.Core.ClosedAlpha;
using Genesis.UI;
using Godot;

namespace Genesis;

/// <summary>
/// Presentation launch shell — Create World (ux_worldgen_gui) → Play → PlayRegion.
/// No sim logic. Consumes CDC presence; degrades visibly when content drop is thin.
/// Fantasy UI chrome bar (framed panel + bronze actions) — not generic flat menu.
/// </summary>
public partial class LaunchShell : Control
{
	private const string PlayScenePath = "res://PlayRegion.tscn";
	private const string HudScenePath = "res://GameHud.tscn";
	private const string WorldgenGuiPath = "res://UI/WorldgenGui.tscn";
	private const string CdcManifestPath = "res://content/_factory/manifest.yaml";

	private Button? _playButton;
	private Button? _createWorldButton;
	private Button? _settingsButton;
	private PanelContainer? _settingsPanel;
	private PanelContainer? _menuFrame;
	private PanelContainer? _degradationBanner;
	private Label? _titleLabel;
	private Label? _subtitleLabel;
	private Label? _settingsBody;
	private Label? _degradationLabel;
	private Control? _worldgenHost;
	private WorldgenGui? _worldgenGui;
	private string? _acceptedScaffoldId;
	private string? _acceptedTone;

	public override void _Ready()
	{
		AlphaFactoryLog.ConfigureRuntimePath();

		_playButton = GetNode<Button>("%PlayButton");
		_createWorldButton = GetNodeOrNull<Button>("%CreateWorldButton");
		_settingsButton = GetNode<Button>("%SettingsButton");
		_settingsPanel = GetNode<PanelContainer>("%SettingsPanel");
		_menuFrame = GetNodeOrNull<PanelContainer>("%MenuFrame");
		_degradationBanner = GetNode<PanelContainer>("%DegradationBanner");
		_titleLabel = GetNodeOrNull<Label>("%TitleLabel") ?? GetNodeOrNull<Label>("Center/MenuFrame/Margin/VBox/Title");
		_subtitleLabel = GetNodeOrNull<Label>("%SubtitleLabel") ?? GetNodeOrNull<Label>("Center/MenuFrame/Margin/VBox/Subtitle");
		_settingsBody = GetNode<Label>("%SettingsBody");
		_degradationLabel = GetNode<Label>("%DegradationLabel");
		_worldgenHost = GetNodeOrNull<Control>("%WorldgenHost");

		if (_titleLabel != null)
			_titleLabel.Text = "Genesis Mythos";
		if (_subtitleLabel != null)
			_subtitleLabel.Text =
				"DM creates the first living world — table can shape; players do not author it.";
		_playButton!.Text = "Enter Craft";
		if (_createWorldButton != null)
			_createWorldButton.Text = "Create World";
		_settingsButton!.Text = "Controls";
		_settingsBody!.Text =
			"Worldgen dialogue (Create World):\n" +
			"  Propose / refine / preview scaffolds · Accept or Regenerate\n" +
			"  Players cannot author the first world\n\n" +
			"Craft cam (after Accept / Enter Craft):\n" +
			"  WASD — pan · LMB — paint · Shift+LMB — raise\n" +
			"  1/2 — grass / desert · F6 — stamp_oasis_desert · F5 — persist\n" +
			"  Tab — sparky inspect when a 3D world exists\n\n" +
			"Sparky (DM):\n" +
			"  WASD + mouse look simultaneously · Tab — return to craft\n" +
			"HUD stays on-screen after Play — no vault docs required.";
		_settingsPanel!.Visible = false;
		_degradationBanner!.Visible = false;
		if (_worldgenHost != null)
			_worldgenHost.Visible = false;

		ApplyFantasyChrome();

		_playButton.Pressed += OnPlayPressed;
		if (_createWorldButton != null)
			_createWorldButton.Pressed += OnCreateWorldPressed;
		_settingsButton.Pressed += OnSettingsPressed;

		EnsureCdcDependencyVisible();

		AlphaFactoryLog.Emit(
			"ui.boundary",
			"Flow_Launch",
			"LaunchShell loaded — Create World → ux_worldgen_gui; Play → PlayRegion",
			new Dictionary<string, object>
			{
				["slice_id"] = "row_ux_world_generation_r1_d1",
				["weld_slice_id"] = "alpha0_worldgen_dualgrid_sparky_r1",
				["ux_bullet"] = "UX-1",
				["lane_id"] = "presentation",
				["checklist"] = new[] { "Flow_Launch", "Flow_DM_Mode", "Anti_DevOnlyHUD", "Nav_LookWhileMove_DM" },
				["inspiration"] = "fantasy_ui_main_menu",
			});
	}

	private void ApplyFantasyChrome()
	{
		if (_menuFrame != null)
		{
			var frame = new StyleBoxFlat
			{
				BgColor = new Color(0.09f, 0.08f, 0.07f, 0.94f),
				BorderColor = new Color(0.72f, 0.58f, 0.32f, 1f),
				BorderWidthLeft = 3,
				BorderWidthTop = 3,
				BorderWidthRight = 3,
				BorderWidthBottom = 3,
				CornerRadiusTopLeft = 6,
				CornerRadiusTopRight = 6,
				CornerRadiusBottomRight = 6,
				CornerRadiusBottomLeft = 6,
				ContentMarginLeft = 8,
				ContentMarginRight = 8,
				ContentMarginTop = 8,
				ContentMarginBottom = 8,
			};
			_menuFrame.AddThemeStyleboxOverride("panel", frame);
		}

		StyleBronze(_createWorldButton, selected: true);
		StyleBronze(_playButton, selected: false);
		StyleBronze(_settingsButton, selected: false);
	}

	private static void StyleBronze(Button? btn, bool selected)
	{
		if (btn == null) return;
		var box = new StyleBoxFlat
		{
			BgColor = selected ? new Color(0.48f, 0.42f, 0.34f, 1f) : new Color(0.26f, 0.2f, 0.14f, 1f),
			BorderColor = new Color(0.78f, 0.62f, 0.34f, 1f),
			BorderWidthLeft = 2,
			BorderWidthTop = 2,
			BorderWidthRight = 2,
			BorderWidthBottom = 2,
			CornerRadiusTopLeft = 4,
			CornerRadiusTopRight = 4,
			CornerRadiusBottomRight = 4,
			CornerRadiusBottomLeft = 4,
			ContentMarginLeft = 14,
			ContentMarginRight = 14,
			ContentMarginTop = 10,
			ContentMarginBottom = 10,
		};
		btn.AddThemeStyleboxOverride("normal", box);
		btn.AddThemeStyleboxOverride("hover", box);
		btn.AddThemeStyleboxOverride("pressed", box);
		btn.AddThemeColorOverride("font_color", new Color(0.96f, 0.94f, 0.9f));
	}

	private void EnsureCdcDependencyVisible()
	{
		if (Godot.FileAccess.FileExists(CdcManifestPath))
		{
			AlphaFactoryLog.Emit(
				"drop.consume",
				"depends_on_cdc",
				"CDC manifest present — presentation may launch with safe chrome defaults",
				new Dictionary<string, object>
				{
					["depends_on_cdc"] = "cdc-alpha0_worldgen_dualgrid_sparky_r1-content-6a0017c7",
				});
			return;
		}

		_degradationBanner!.Visible = true;
		_degradationLabel!.Text =
			"Content drops unavailable — launch controls use safe defaults (CDC missing).";
		AlphaFactoryLog.Emit(
			"Degrade_FailVisible",
			"Anti_DevOnlyHUD",
			"CDC manifest missing at launch — degradation banner visible",
			level: "warn");
	}

	private void OnCreateWorldPressed()
	{
		if (_worldgenHost == null)
		{
			AlphaFactoryLog.Emit(
				"Degrade_FailVisible",
				"Anti_DevOnlyHUD",
				"WorldgenHost missing on LaunchShell",
				level: "warn");
			return;
		}

		if (!ResourceLoader.Exists(WorldgenGuiPath))
		{
			AlphaFactoryLog.Emit(
				"Degrade_FailVisible",
				"Anti_DevOnlyHUD",
				$"WorldgenGui missing at {WorldgenGuiPath}",
				level: "warn");
			_degradationBanner!.Visible = true;
			_degradationLabel!.Text = "Worldgen dialogue unavailable — Enter Craft still opens craft path.";
			return;
		}

		foreach (var child in _worldgenHost.GetChildren())
			child.QueueFree();

		var packed = GD.Load<PackedScene>(WorldgenGuiPath);
		_worldgenGui = packed.Instantiate<WorldgenGui>();
		_worldgenHost.AddChild(_worldgenGui);
		_worldgenHost.Visible = true;
		_worldgenGui.ScaffoldAccepted += OnScaffoldAccepted;
		_worldgenGui.DialogueCancelled += OnWorldgenCancelled;

		AlphaFactoryLog.Emit(
			"ui.boundary",
			"Flow_Launch",
			"Operator entered ux_worldgen_gui from LaunchShell");
	}

	private void OnScaffoldAccepted(string scaffoldId, string toneProfile)
	{
		_acceptedScaffoldId = scaffoldId;
		_acceptedTone = toneProfile;
		HideWorldgenGui();

		var root = GetTree().Root;
		root.SetMeta("worldgen_scaffold_id", scaffoldId);
		root.SetMeta("worldgen_tone_profile", toneProfile);

		AlphaFactoryLog.Emit(
			"ui.boundary",
			"Anti_DevOnlyHUD",
			$"Scaffold accepted — launching craft with tone={toneProfile}",
			new Dictionary<string, object>
			{
				["scaffold_id"] = scaffoldId,
				["tone"] = toneProfile,
				["ux_bullet"] = "UX-1",
			});

		LaunchPlayRegion();
	}

	private void OnWorldgenCancelled()
	{
		HideWorldgenGui();
	}

	private void HideWorldgenGui()
	{
		if (_worldgenGui != null)
		{
			_worldgenGui.ScaffoldAccepted -= OnScaffoldAccepted;
			_worldgenGui.DialogueCancelled -= OnWorldgenCancelled;
			_worldgenGui.QueueFree();
			_worldgenGui = null;
		}

		if (_worldgenHost != null)
			_worldgenHost.Visible = false;
	}

	private void OnPlayPressed()
	{
		AlphaFactoryLog.Emit(
			"ui.boundary",
			"Flow_Launch",
			"Operator selected Enter Craft — ChangeSceneToFile PlayRegion.tscn",
			new Dictionary<string, object>
			{
				["scaffold_id"] = _acceptedScaffoldId ?? "(none)",
				["tone"] = _acceptedTone ?? "(none)",
			});
		LaunchPlayRegion();
	}

	private void LaunchPlayRegion()
	{
		MountPersistentHud();
		var err = GetTree().ChangeSceneToFile(PlayScenePath);
		if (err != Error.Ok)
		{
			AlphaFactoryLog.Emit(
				"Degrade_FailVisible",
				"Flow_Launch",
				$"ChangeSceneToFile({PlayScenePath}) failed: {err}",
				level: "error");
		}
	}

	/// <summary>
	/// HUD is a root sibling so it survives ChangeSceneToFile (PlayRegion is module zone —
	/// presentation must not edit PlayRegion.tscn; module may later instance the same PDC drop).
	/// </summary>
	private void MountPersistentHud()
	{
		var root = GetTree().Root;
		if (root.GetNodeOrNull("GameHud") != null)
			return;

		if (!ResourceLoader.Exists(HudScenePath))
		{
			AlphaFactoryLog.Emit(
				"Degrade_FailVisible",
				"Anti_DevOnlyHUD",
				$"GameHud scene missing at {HudScenePath}",
				level: "warn");
			return;
		}

		var packed = GD.Load<PackedScene>(HudScenePath);
		var hud = packed.Instantiate<GameHud>();
		hud.Name = "GameHud";
		root.AddChild(hud);

		var tone = root.HasMeta("worldgen_tone_profile")
			? root.GetMeta("worldgen_tone_profile").AsString()
			: null;
		var hint = string.IsNullOrEmpty(tone)
			? "CRAFT cam — LMB paint cell · WASD pan · Tab → sparky when world exists"
			: $"CRAFT · {tone} — LMB paint · WASD pan · Tab → sparky when world exists";
		hud.SetPerspectiveShellHint(hint);
		AlphaFactoryLog.Emit(
			"ui.boundary",
			"Anti_DevOnlyHUD",
			"GameHud mounted on root — player-facing chrome (not dev-only)");
	}

	private void OnSettingsPressed()
	{
		_settingsPanel!.Visible = !_settingsPanel.Visible;
		AlphaFactoryLog.Emit(
			"ui.boundary",
			"Flow_Launch",
			_settingsPanel.Visible
				? "Controls panel opened — craft/sparky binds discoverable"
				: "Controls panel closed");
	}
}
