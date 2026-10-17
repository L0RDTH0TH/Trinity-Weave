using System.Collections.Generic;
using Genesis.Core.ClosedAlpha;
using Genesis.Core.WorldGen;
using Genesis.Systems;
using Genesis.UI;
using Godot;

namespace Genesis;

/// <summary>
/// Presentation launch shell — Create World + Load World (PACK feedstock) + Import stub (1e parked)
/// + empty-campaigns (1f KEEP) + WORLD-parity peers (1g KEEP):
/// Create World → Open = world already generated (bias landform + dials + GEN-biomes).
/// Load World = quit/reload same generated world from user:// pack (incl. biomes).
/// Enter Craft = empty amber until place (1g empty-enter applies to this lane ONLY).
/// No Generate product button; regen = dials + re-Open. Key.T accel only (never Success).
/// Import stays parked. Zero campaigns lawful. Refuse empty Create World Open /
/// string_on_cell_alone biome / generate_button_as_product_ux. GEN-sites unarmed.
/// Fantasy UI chrome bar (framed panel + bronze actions) — not generic flat menu.
/// </summary>
public partial class LaunchShell : Control
{
	private const string PlayScenePath = "res://PlayRegion.tscn";
	private const string HudScenePath = "res://GameHud.tscn";
	private const string WorldgenGuiPath = "res://UI/WorldgenGui.tscn";
	private const string CdcManifestPath = "res://content/_factory/manifest.yaml";
	private const string WeldSliceId = WorldPackage.SliceId;

	private Button? _playButton;
	private Button? _createWorldButton;
	private Button? _loadWorldButton;
	private Button? _importWorldButton;
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
	private string? _acceptedWorldId;

	public override void _Ready()
	{
		AlphaFactoryLog.ConfigureRuntimePath();

		_playButton = GetNode<Button>("%PlayButton");
		_createWorldButton = GetNodeOrNull<Button>("%CreateWorldButton");
		_loadWorldButton = GetNodeOrNull<Button>("%LoadWorldButton");
		_importWorldButton = GetNodeOrNull<Button>("%ImportWorldButton");
		_settingsButton = GetNode<Button>("%SettingsButton");
		_settingsPanel = GetNode<PanelContainer>("%SettingsPanel");
		_menuFrame = GetNodeOrNull<PanelContainer>("%MenuFrame");
		_degradationBanner = GetNode<PanelContainer>("%DegradationBanner");
		_titleLabel = GetNodeOrNull<Label>("%TitleLabel")
			?? GetNodeOrNull<Label>("SafeArea/Scroll/ScrollBody/MenuFrame/Margin/VBox/TitleLabel");
		_subtitleLabel = GetNodeOrNull<Label>("%SubtitleLabel")
			?? GetNodeOrNull<Label>("SafeArea/Scroll/ScrollBody/MenuFrame/Margin/VBox/SubtitleLabel");
		_settingsBody = GetNode<Label>("%SettingsBody");
		_degradationLabel = GetNode<Label>("%DegradationLabel");
		_worldgenHost = GetNodeOrNull<Control>("%WorldgenHost");

		if (_titleLabel != null)
			_titleLabel.Text = "Genesis Mythos";
		if (_subtitleLabel != null)
			_subtitleLabel.Text =
				"GEN-biomes — Create World Open auto-gen · land biomes + move/difficult tags · Enter Craft empty · no Generate.";
		_playButton!.Text = "Enter Craft";
		if (_createWorldButton != null)
			_createWorldButton.Text = "Create World";
		if (_loadWorldButton != null)
			_loadWorldButton.Text = "Load World";
		if (_importWorldButton != null)
			_importWorldButton.Text = "Import World";
		_settingsButton!.Text = "Controls";
		_settingsBody!.Text =
			"GEN-biomes — mechanical tags + visible material difference:\n" +
			"  Create World → bias+dials → Open (terrain + biomes auto) → hover land for biome+tag\n" +
			"  At least two land looks (Plains/Forest/Highland/Marsh/Desert) · tag changes move/difficult\n" +
			"  " + GenBiomesContract.SummaryLine + "\n\n" +
			"Lane-split product law:\n" +
			"  Create World → Open = world already generated (bias landform + dials + biomes)\n" +
			"  Load World = restore saved pack incl. biomes (organic_seed)\n" +
			"  Enter Craft = empty amber board until place (1g KEEP — this lane ONLY)\n" +
			"  No Generate button — refuse generate_button_as_product_ux\n" +
			"  Key.T accel only (never Success)\n" +
			"  Prior PACK-save-load F5 · GEN-tone BiasLandform · terrain-product dials\n" +
			"  Refuse: string-only biome · identical land look · blank Open · creatures\n\n" +
			"WORLD-parity (1g KEEP) — authorship peers:\n" +
			"  Create World = procedural peer · Enter Craft = manual peer\n" +
			"  " + WorldParityContract.SummaryLine + "\n\n" +
			"Import World (1e KEEP-debt parked):\n" +
			"  Waits on real pack — use Load World for quit/reload; full canon ingest barred\n\n" +
			"Empty campaigns (1f KEEP):\n" +
			"  Zero campaigns lawful — attach later; world owns itself\n\n" +
			"Not DF-hours Done · not GEN-sites · not Townscaper Done\n\n" +
			"HUD stays on-screen after Play — no vault docs required.";
		_settingsPanel!.Visible = false;
		_degradationBanner!.Visible = false;
		if (_worldgenHost != null)
			_worldgenHost.Visible = false;

		ApplyFantasyChrome();

		_playButton.Pressed += OnPlayPressed;
		if (_createWorldButton != null)
			_createWorldButton.Pressed += OnCreateWorldPressed;
		if (_loadWorldButton != null)
			_loadWorldButton.Pressed += OnLoadWorldPressed;
		if (_importWorldButton != null)
			_importWorldButton.Pressed += OnImportWorldPressed;
		_settingsButton.Pressed += OnSettingsPressed;

		EnsureCdcDependencyVisible();

		AlphaFactoryLog.Emit(
			"ui.boundary",
			"Flow_Launch",
			"LaunchShell loaded — 1a–1g KEEP + GEN-terrain-product W1–W5 (Create World auto-gen · Enter Craft empty)",
			new Dictionary<string, object>
			{
				["slice_id"] = WeldSliceId,
				["ask_id"] = WorldPackage.AskId,
				["weld_slice_id"] = WeldSliceId,
				["ticket_map"] = WorldPackage.TicketMap,
				["prior_keep"] = WorldPackage.PriorKeepSliceId,
				["authorship_parity"] = WorldParityContract.PeerLaw,
				["gen_terrain"] = GenTerrainContract.SummaryLine,
				["create_world_auto_gen"] = GenTerrainContract.CreateWorldAutoGenLaw,
				["empty_enter_manual_only"] = GenTerrainContract.EmptyEnterKeepLaw,
				["campaign_ownership"] = WorldEmptyCampaignsContract.OwnershipLaw,
				["campaigns_empty_lawful"] = true,
				["ux_bullet"] = "UX-1",
				["lane_id"] = "presentation",
				["claim_class"] = "staging",
				["checklist"] = new[] { "Flow_Launch", "Flow_DM_Mode", "Anti_DevOnlyHUD" },
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

		// Create World / Load World / Enter Craft are peer authorship lanes — equal chrome weight.
		StyleBronze(_createWorldButton, selected: true);
		StyleBronze(_loadWorldButton, selected: true);
		StyleBronze(_playButton, selected: true);
		StyleBronze(_importWorldButton, selected: false);
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
			_degradationLabel!.Text = "Worldgen dialogue unavailable — Enter Craft still opens manual peer path.";
			return;
		}

		foreach (var child in _worldgenHost.GetChildren())
			child.QueueFree();

		var packed = GD.Load<PackedScene>(WorldgenGuiPath);
		_worldgenGui = packed.Instantiate<WorldgenGui>();
		_worldgenHost.AddChild(_worldgenGui);
		_worldgenHost.Visible = true;
		if (_menuFrame != null)
			_menuFrame.Visible = false;
		_worldgenGui.ScaffoldAccepted += OnScaffoldAccepted;
		_worldgenGui.DialogueCancelled += OnWorldgenCancelled;

		WorldPackageSession.BindParityPeers(GetTree(), WorldParityContract.ProceduralLaneCode);

		AlphaFactoryLog.Emit(
			"ui.boundary",
			"Flow_Launch",
			"Operator entered Create World dialogue — procedural peer lane (1a–1d KEEP path)",
			new Dictionary<string, object>
			{
				["slice_id"] = WeldSliceId,
				["ask_id"] = WorldPackage.AskId,
				["authorship_parity"] = WorldParityContract.PeerLaw,
				["active_lane"] = WorldParityContract.ProceduralLaneCode,
			});
	}

	private void OnLoadWorldPressed()
	{
		if (!DualGridCraftHost.TryReadPackWorld(PackSaveLoadContract.PersistPath, out var package, out var summary)
			|| package == null)
		{
			_degradationBanner!.Visible = true;
			_degradationLabel!.Text =
				"No saved world pack at " + PackSaveLoadContract.PersistPath +
				". Create World → Open → F5 save first. Import (1e) stays parked.";
			AlphaFactoryLog.Emit(
				"pack.load",
				"PACK_save_load_refuse",
				$"Load World refused — {summary}",
				level: "warn");
			return;
		}

		WorldPackageSession.BindFromPersisted(GetTree(), package);
		_acceptedWorldId = package.WorldId;
		_acceptedTone = package.GenBiasId;
		_degradationBanner!.Visible = false;

		AlphaFactoryLog.Emit(
			"ui.boundary",
			"PACK_save_load",
			$"Load World — restoring pack {summary}",
			new Dictionary<string, object>
			{
				["ask_id"] = PackSaveLoadContract.AskId,
				["slice_id"] = PackSaveLoadContract.SliceId,
				["ticket_map"] = PackSaveLoadContract.TicketMap,
				["world_id"] = package.WorldId,
				["gen_bias"] = package.GenBiasId,
				["path"] = PackSaveLoadContract.PersistPath,
				["summary"] = summary,
			});

		LaunchPlayRegion(WorldParityContract.ProceduralLaneCode);
	}

	private void OnImportWorldPressed()
	{
		var stub = WorldPackageSession.BindImportStub(GetTree());
		_degradationBanner!.Visible = true;
		_degradationLabel!.Text =
			"WORLD-import (1e) parked — use Load World for quit/reload of a saved pack. " +
			"Full canon ingest still barred. " + WorldEmptyCampaignsContract.SummaryLine +
			" · " + WorldParityContract.SummaryLine;
		AlphaFactoryLog.Emit(
			"ui.boundary",
			"Flow_Launch",
			"Operator pressed Import World — stub parked; PACK Load World owns quit/reload; full ingest barred",
			stub.ToLogFields());
	}

	private void OnScaffoldAccepted(string scaffoldId, string toneProfile)
	{
		_acceptedScaffoldId = scaffoldId;
		_acceptedTone = toneProfile;
		var dials = _worldgenGui?.SelectedDials ?? WorldBoundsDials.Defaults;
		var scaffold = _worldgenGui?.SelectedScaffold ?? WorldScaffoldProposal.Empty;
		var intents = _worldgenGui?.SelectedIntents ?? WorldSession0IntentBoard.Empty;
		HideWorldgenGui();

		var bias = WorldPackage.ParseBiasId(scaffold.GenBiasId);
		var package = WorldPackageSession.BindNew(GetTree(), bias, dials, scaffold, intents);
		_acceptedWorldId = package.WorldId;
		_acceptedScaffoldId = package.Scaffold.ScaffoldId;

		AlphaFactoryLog.Emit(
			"ui.boundary",
			"Anti_DevOnlyHUD",
			$"Create World open — world_id={package.WorldId} gen_bias={package.GenBiasId} scaffold={package.Scaffold.ScaffoldId} lore={package.Intents.SummaryLine} dials=[{package.Bounds.SummaryLine()}] {WorldEmptyCampaignsContract.SummaryLine} · {WorldParityContract.SummaryLine}",
			new Dictionary<string, object>
			{
				["scaffold_id"] = package.Scaffold.ScaffoldId,
				["scaffold_revision"] = package.Scaffold.Revision,
				["tone"] = toneProfile,
				["gen_bias"] = package.GenBiasId,
				["world_id"] = package.WorldId,
				["campaigns_empty"] = true,
				["campaigns_empty_lawful"] = true,
				["campaign_ownership"] = WorldEmptyCampaignsContract.OwnershipLaw,
				["campaign_attach"] = WorldEmptyCampaignsContract.AttachDeferredCode,
				["authorship_parity"] = WorldParityContract.PeerLaw,
				["dials_summary"] = package.Bounds.SummaryLine(),
				["intent_accepted_count"] = package.Intents.AcceptedCount,
				["intent_summary"] = package.Intents.SummaryLine,
				["lore_feed_salt"] = package.Intents.LoreFeedSalt,
				["lore_fed"] = package.Intents.LoreFed,
				["s0_packaging_slice"] = WorldSession0IntentBoard.PackagingSliceId,
				["s0_optional_lore_slice"] = WorldSession0IntentBoard.OptionalLoreSliceId,
				["s0_off_critical_path"] = true,
				["ask_id"] = WorldPackage.AskId,
				["slice_id"] = WeldSliceId,
				["ux_bullet"] = "UX-1",
			});

		LaunchPlayRegion(WorldParityContract.ProceduralLaneCode);
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
		if (_menuFrame != null)
			_menuFrame.Visible = true;
	}

	private void OnPlayPressed()
	{
		// Enter Craft = manual peer lane. WORLD package optional; parity peers always bind.
		if (WorldPackageSession.Active == null)
		{
			AlphaFactoryLog.Emit(
				"ui.boundary",
				"Flow_Launch",
				"Enter Craft without WORLD package — manual peer brush only (no scaffold bind)",
				level: "warn");
		}

		WorldPackageSession.BindParityPeers(GetTree(), WorldParityContract.ManualLaneCode);
		// Manual lane is not a pack restore — clear Load World sticky so craft stays empty.
		GetTree().Root.SetMeta(WorldPackageSession.MetaPackRestorePending, false);
		GetTree().Root.SetMeta(WorldPackageSession.MetaPackLoadedFromPersist, false);

		AlphaFactoryLog.Emit(
			"ui.boundary",
			"Flow_Launch",
			"Operator selected Enter Craft — manual peer lane → ChangeSceneToFile PlayRegion.tscn",
			new Dictionary<string, object>
			{
				["scaffold_id"] = _acceptedScaffoldId ?? "(none)",
				["tone"] = _acceptedTone ?? "(none)",
				["world_id"] = _acceptedWorldId ?? "(none)",
				["import_stub"] = WorldPackageSession.ImportStub?.SummaryLine ?? "(none)",
				["slice_id"] = WeldSliceId,
				["authorship_parity"] = WorldParityContract.PeerLaw,
				["active_lane"] = WorldParityContract.ManualLaneCode,
			});
		LaunchPlayRegion(WorldParityContract.ManualLaneCode);
	}

	private void LaunchPlayRegion(string activeLane)
	{
		MountPersistentHud(activeLane);
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
	private void MountPersistentHud(string activeLane)
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

		var tone = root.HasMeta(WorldPackageSession.MetaLegacyTone)
			? root.GetMeta(WorldPackageSession.MetaLegacyTone).AsString()
			: null;
		var worldId = root.HasMeta(WorldPackageSession.MetaWorldId)
			? root.GetMeta(WorldPackageSession.MetaWorldId).AsString()
			: null;
		var dials = root.HasMeta(WorldPackageSession.MetaDialsSummary)
			? root.GetMeta(WorldPackageSession.MetaDialsSummary).AsString()
			: null;
		var scaffold = root.HasMeta(WorldPackageSession.MetaScaffoldId)
			? root.GetMeta(WorldPackageSession.MetaScaffoldId).AsString()
			: null;
		var intentN = root.HasMeta(WorldPackageSession.MetaIntentAcceptedCount)
			? root.GetMeta(WorldPackageSession.MetaIntentAcceptedCount).AsInt32()
			: 0;
		var importCode = root.HasMeta(WorldPackageSession.MetaImportStatusCode)
			? root.GetMeta(WorldPackageSession.MetaImportStatusCode).AsString()
			: null;
		var campaignsEmpty = !root.HasMeta(WorldPackageSession.MetaCampaignsEmpty)
			|| root.GetMeta(WorldPackageSession.MetaCampaignsEmpty).AsBool();
		var parity = WorldParityContract.SummaryLine;
		var laneTag = activeLane == WorldParityContract.ManualLaneCode ? "manual" : "procedural";
		string hint;
		if (!string.IsNullOrEmpty(importCode) && string.IsNullOrEmpty(worldId))
		{
			hint = $"WORLD-import stub · {importCode} · campaigns=0 · parity peers ({laneTag})";
		}
		else if (string.IsNullOrEmpty(tone) && string.IsNullOrEmpty(worldId))
		{
			hint = $"CRAFT · Enter Craft empty until place · LMB place · {parity}";
		}
		else if (string.IsNullOrEmpty(worldId))
		{
			hint = $"CRAFT · gen_bias={tone} · empty until place · {parity}";
		}
		else if (string.IsNullOrEmpty(scaffold) || scaffold == "(none)")
		{
			hint = string.IsNullOrEmpty(dials)
				? $"WORLD · {tone} · {worldId} · campaigns=0 · Open auto-gen · no Generate btn · {laneTag}"
				: $"WORLD · {tone} · {worldId} · campaigns=0 · Open auto-gen · no Generate btn · {laneTag} · {dials}";
		}
		else
		{
			var camp = campaignsEmpty ? "campaigns=0" : "campaigns";
			hint = string.IsNullOrEmpty(dials)
				? $"WORLD · {tone} · scf={scaffold} · s0={intentN} · {camp} · Open auto-gen · no Generate btn · {laneTag}"
				: $"WORLD · {tone} · scf={scaffold} · s0={intentN} · {camp} · Open auto-gen · no Generate btn · {laneTag} · {dials}";
		}
		hud.SetPerspectiveShellHint(hint);
		AlphaFactoryLog.Emit(
			"ui.boundary",
			"Anti_DevOnlyHUD",
			"GameHud mounted on root — player-facing chrome (not dev-only); WORLD-parity peers on Play path");
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
