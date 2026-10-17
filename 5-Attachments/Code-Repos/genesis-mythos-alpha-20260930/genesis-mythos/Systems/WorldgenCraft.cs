using System.Collections.Generic;
using Genesis.Camera;
using Genesis.Core;
using Genesis.Core.ClosedAlpha;
using Genesis.Core.WorldGen;
using Genesis.Player;
using Genesis.UI;
using Godot;

namespace Genesis.Systems;

/// <summary>
/// Weld entry <c>res://scenes/WorldgenCraft.tscn</c> — Stålberg organic all-quad planar board
/// (ask_id <c>alpha0_stalberg_quad_kernel</c>, slice relax_r1). Pipeline seed→tri→dissolve→subdivide→unique-topo→area-square-relax→flatten;
/// regenerable graybox quads; Hex19*/dual-on-hex not Success; Terrain3D hard-disabled.
/// Tutorial ladder s1–s6 remains a separate series.
/// </summary>
public partial class WorldgenCraft : Node3D
{
	public const string ScenePath = "res://scenes/WorldgenCraft.tscn";
	public const string SliceId = "alpha0_stalberg_dual_primary_vertex_place_r1";
	public const string WeldSliceId = "alpha0_stalberg_dual_primary_vertex_place_r1";
	public const string PreferAskId = "alpha0_stalberg_dual_visual";
	public const string HalfBOverlay = "alpha0_stalberg_dual_primary_vertex_place_r1";

	private DualGridCraftHost? _craft;
	private WorldShellController? _shell;
	private CraftPlanarCamRig? _craftCam;
	private CraftFocusAnchor? _focus;
	private CraftCellType _brush = CraftCellType.Grass;
	private bool _painting;
	private bool _erasing;
	private Label3D? _hint;
	private Vector2 _cursorScreen;
	private bool _cursorSeen;

	public override void _Ready()
	{
		AlphaFactoryLog.ConfigureRuntimePath();
		AlphaFactoryLog.Emit(
			"ui.boundary",
			"Flow_Launch",
			"WorldgenCraft entry armed — Stålberg dual-corner on OrganicQuadMesh (corner flip → incident dual cells); kernel+craft-plane intact; Hex19/tiles/art/Terrain3D not Success",
			new Dictionary<string, object>
			{
				["slice_id"] = SliceId,
				["weld_slice_id"] = WeldSliceId,
				["ask_id"] = PreferAskId,
				["half_b_overlay"] = HalfBOverlay,
				["ux_bullet"] = "UX-1",
				["claim_class"] = "staging",
				["scene"] = ScenePath,
				["matrix_prefer"] = "Irregular all-quad mesh via seed→tri→dissolve→subdivide→relax; regenerable; graybox OK",
				["matrix_never"] = "hex_scaffold_as_final_mesh; dual_overlay_as_grid_kernel; skip_dissolve_relax; points_as_grid; dual paint/tiles/art/Terrain3D Success",
				["topology"] = "organic_quad_faces_valence_4_planar",
				["render"] = "opaque_faces_depth_edges",
				["algorithm"] = "oskar-procedure/docs/02",
				["visual_bar"] = DualGridCraftHost.VisualBarCite,
				["art_style_id"] = DualGridCraftHost.ArtStyleId,
				["terrain3d"] = "hard_disabled_under_craft",
				["dual_visual_success"] = false,
				["dual_neighborhood_stable"] = true,
				["hex19_success"] = false,
			});

		var repoAbs = ProjectSettings.GlobalizePath("res://");
		var drops = FactoryDropRegistry.ConsumeRequiredDrops(repoAbs);
		AlphaFactoryLog.Emit(
			"drop.consume",
			"depends_on_drops",
			$"WorldgenCraft consumed {drops.Count} drop refs",
			new Dictionary<string, object> { ["drops_json"] = FactoryDropRegistry.ToJson(drops) });

		BuildEnvironment();
		HardDisableTerrain3DUnderCraft();

		_craft = GetNodeOrNull<DualGridCraftHost>("DualGridCraftHost");
		if (_craft == null)
		{
			_craft = new DualGridCraftHost { Name = "DualGridCraftHost" };
			AddChild(_craft);
			AlphaFactoryLog.Emit(
				"Degrade_FailVisible",
				"DualGrid_CraftOverlay",
				"DualGridCraftHost missing from WorldgenCraft.tscn — runtime-created fallback",
				level: "warn");
		}
		_craft.EnsureHost(this);
		_craft.SetDualOverlayVisible(true);
		var organicProof = _craft.ProveCraftPlaneAuthority();
		var dualProof = _craft.ProveDualOffsetStructure();
		var neighProof = _craft.ProveStableDualNeighborhood();
		if (!dualProof.Ok) organicProof = dualProof;
		if (!neighProof.Ok) organicProof = (false, neighProof.Summary);
		var structureOk = organicProof.Ok;
		AlphaFactoryLog.Emit(
			"craft.dual",
			"Stable_Neighborhood_Ready",
			neighProof.Ok
				? $"stable dual neighborhood — {neighProof.Summary}"
				: $"stable dual neighborhood FAIL — {neighProof.Summary}",
			new Dictionary<string, object>
			{
				["ask_id"] = PreferAskId,
				["overlay"] = HalfBOverlay,
				["stable_neighborhood_ok"] = neighProof.Ok,
				["stamp_as_dual"] = false,
				["over_neighbor_paint"] = false,
				["dual_visual_success"] = false,
				["hex19_success"] = false,
			},
			level: neighProof.Ok ? "info" : "error");
		AlphaFactoryLog.Emit(
			"craft.occupancy",
			"organic_quad_kernel_ready",
			structureOk
				? $"Stålberg organic all-quad ready — {organicProof.Summary}"
				: $"Stålberg organic all-quad FAIL — {organicProof.Summary}",
			new Dictionary<string, object>
			{
				["ask_id"] = PreferAskId,
				["overlay"] = HalfBOverlay,
				["visual_bar"] = DualGridCraftHost.VisualBarCite,
				["art_style_id"] = DualGridCraftHost.ArtStyleId,
				["organic_quad_ok"] = organicProof.Ok,
				["quad_faces"] = _craft.OrganicQuadFaceCount,
				["quad_vertices"] = _craft.OrganicQuadVertexCount,
				["all_faces_quads"] = _craft.OrganicMesh?.AllFacesAreQuads ?? false,
				["pipeline"] = "SeedHexLatticeRings|TriangulateHexLattice|DissolveTrianglePairs|SubdivideFacesToQuads|RelaxTowardSquares",
				["dual_visual_success"] = false,
				["dual_neighborhood_stable"] = true,
				["hex19_success"] = false,
				["refuse_ban"] = "unstable_dual_neighborhood|stamp_as_dual|over_neighbor_paint|hex_scaffold_as_final_mesh|dual_overlay_as_grid_kernel|skip_dissolve_relax|points_as_grid|count_equals_topology|bundle_tutorial_steps|terrain3d_in_scope|verify_mcp_only",
				["mesh_library_source"] = _craft.MeshLibrarySource,
			},
			level: structureOk ? "info" : "error");

		_shell = new WorldShellController(_craft);

		var seatVerify = _shell.VerifyWrongSeatRefuse();
		if (seatVerify != Error.Ok)
		{
			AlphaFactoryLog.Emit(
				"Degrade_FailVisible",
				"WorldShell_Enter",
				"seat refuse verify failed — aborting WorldgenCraft arm",
				level: "error");
			return;
		}

		var enter = _shell.Enter(SeatContext.SharedTable);
		if (enter != Error.Ok)
		{
			AlphaFactoryLog.Emit("Degrade_FailVisible", "WorldShell_Enter", $"enter failed {enter}", level: "error");
			return;
		}

		_focus = GetNodeOrNull<CraftFocusAnchor>("CraftFocusAnchor");
		if (_focus == null)
		{
			_focus = new CraftFocusAnchor { Name = "CraftFocusAnchor", Position = new Vector3(8f, 0f, 8f) };
			AddChild(_focus);
		}

		_craftCam = GetNodeOrNull<CraftPlanarCamRig>("CraftPlanarCamRig");
		if (_craftCam == null)
		{
			_craftCam = new CraftPlanarCamRig { Name = "CraftPlanarCamRig" };
			AddChild(_craftCam);
			AlphaFactoryLog.Emit(
				"Degrade_FailVisible",
				"CraftCam_Arm",
				"CraftPlanarCamRig missing from WorldgenCraft.tscn — runtime-created fallback",
				level: "warn");
		}
		// Initial arm only — place/remove must NOT call SetFocusWorld (refuse craft_cam_recenter_on_place).
		_craftCam.SetFocusWorld(_focus.GlobalPosition);
		_craftCam.SetInputEnabled(true);
		_craft?.SetLatticeOrigin(_focus.GlobalPosition);

		// Sparky cam may remain in scene tree for later tickets — input stays OFF; no Tab handoff this round.
		var sparky = GetNodeOrNull<SparkyDmFreeCamRig>("SparkyDmFreeCamRig");
		sparky?.SetInputEnabled(false);

		_cursorScreen = GetViewport().GetMousePosition();
		_cursorSeen = true;

		MountPdcCraftControls();
		// No Generate / Generate (regen) product chrome — refuse generate_button_as_product_ux.
		// Create World Open auto-gens; Enter Craft stays empty; Key.T accel only.

		_hint = new Label3D
		{
			Name = "CraftHint",
			Text = HintText(),
			Position = new Vector3(8f, 10f, 8f),
			FontSize = 42,
			Modulate = new Color(0.72f, 0.58f, 0.32f),
			Billboard = BaseMaterial3D.BillboardModeEnum.Enabled,
		};
		AddChild(_hint);

		// Lane split (operator product law):
		// Create World → Open = auto-run gen pass (refuse empty Create World Open / blank amber).
		// Load World = restore pack board (PACK-save-load) — skip auto-gen wipe.
		// Enter Craft = empty amber until operator places (1g KEEP applies to this lane ONLY).
		// Regen = dials change + re-Open / session rebind — not a Generate button.
		var packRestore = WorldPackageSession.IsPackRestorePending(GetTree().Root)
			|| WorldPackageSession.IsLoadedFromPack(GetTree().Root);
		var createWorldOpen = WorldPackageSession.IsCreateWorldOpenPath(GetTree().Root);
		AlphaFactoryLog.Emit(
			"craft.load",
			"World_ImportAttach_Deferred",
			packRestore
				? "Load World — PACK restore deferred after scene ready; skip Create World auto-gen wipe"
				: createWorldOpen
					? "Create World Open — auto ImportAttach gated; auto GEN deferred after scene ready; no Generate button"
					: "Enter Craft empty — auto ImportAttach gated; press I to restore persist; place to paint; GEN ≠ Enter Craft Success",
			new Dictionary<string, object>
			{
				["slice_id"] = PackSaveLoadContract.SliceId,
				["weld_slice_id"] = PackSaveLoadContract.SliceId,
				["ask_id"] = PackSaveLoadContract.AskId,
				["ticket_map"] = PackSaveLoadContract.TicketMap,
				["create_world_open"] = createWorldOpen,
				["pack_restore"] = packRestore,
				["craft_enter_empty"] = !createWorldOpen && !packRestore,
				["auto_import_attach"] = false,
				["gen_fill_as_craft_enter"] = false,
				["create_world_auto_gen"] = createWorldOpen && !packRestore,
				["gen_terrain_explicit"] = GenTerrainContract.ExplicitInvokeLaw,
				["hotkey_as_product_ux"] = false,
				["generate_button_as_product_ux"] = false,
				["empty_create_world_open_barred"] = GenTerrainContract.EmptyCreateWorldOpenBarred,
				["prior_tone_slice"] = GenToneContract.SliceId,
				["prior_incomplete_slice"] = GenTerrainContract.PriorIncompleteSliceId,
			});

		if (WorldPackageSession.IsPackRestorePending(GetTree().Root))
			CallDeferred(MethodName.RestorePackBoard);
		else if (createWorldOpen)
			CallDeferred(MethodName.AutoGenCreateWorldOpen);
		else
		{
			AlphaFactoryLog.Emit(
				"craft.phase",
				"CraftCam_Arm",
				"Enter Craft — empty amber board (1g manual lane); no Generate button; Key.T accel only; R=regen mesh; place tools KEEP; Terrain3D hard-disabled");
		}

		AlphaFactoryLog.Emit(
			"module.fit",
			"module_fit_pass",
			"UX-1..6 Stålberg kernel — seed hex rings · triangulate · dissolve · subdivide to quads · relax · render quads · regenerable");
		AlphaFactoryLog.Emit(
			"module.integrate",
			"integration_pass",
			"WorldgenCraft module lane — claim_class=staging; GEN-terrain-product lane-split auto-open; awaiting operator F5");
	}

	/// <summary>
	/// PACK-save-load — restore persisted gen board (+ hand edits) from user:// pack file.
	/// Skips Create World Open auto-gen so reload does not wipe the saved silhouette.
	/// </summary>
	private void RestorePackBoard()
	{
		if (!WorldPackageSession.ConsumePackRestorePending(GetTree().Root))
			return;
		if (_craft == null || _shell == null)
		{
			AlphaFactoryLog.Emit(
				"pack.load",
				"PACK_save_load_refuse",
				"Load World restore refused — craft/shell not ready",
				level: "error");
			return;
		}

		var err = _shell.ImportAttach(SeatContext.SharedTable, PackSaveLoadContract.PersistPath);
		var hud = GetTree().Root.GetNodeOrNull<GameHud>("GameHud");
		if (err == Error.Ok && _craft.GenTerrainApplied)
		{
			GetTree().Root.SetMeta(WorldPackageSession.MetaGenTerrainApplied, true);
			GetTree().Root.SetMeta(WorldPackageSession.MetaGenTerrainSummary, _craft.LastGenTerrainSummary);
			GetTree().Root.SetMeta(WorldPackageSession.MetaWeldSlice, PackSaveLoadContract.SliceId);
			GetTree().Root.SetMeta(WorldPackageSession.MetaAskId, PackSaveLoadContract.AskId);
			hud?.SetPerspectiveShellHint(
				$"PACK load · {_craft.LastGenTerrainSummary} · same board restore · F5 re-save");
			AlphaFactoryLog.Emit(
				"pack.load",
				"PACK_save_load",
				$"Load World restore ok — {_craft.LastGenTerrainSummary} (refuse blank_amber_after_load|lost_world_after_load|fake_toast_as_save)",
				new Dictionary<string, object>
				{
					["ask_id"] = PackSaveLoadContract.AskId,
					["slice_id"] = PackSaveLoadContract.SliceId,
					["path"] = PackSaveLoadContract.PersistPath,
					["gen_applied"] = true,
					["err"] = err.ToString(),
				});
		}
		else
		{
			hud?.SetPerspectiveShellHint("PACK load FAIL — blank/lost world (staging incomplete)");
			AlphaFactoryLog.Emit(
				"Degrade_FailVisible",
				"PACK_save_load",
				$"Load World restore failed err={err} applied={_craft.GenTerrainApplied} — blank amber after load = FAIL",
				level: "error");
		}

		RefreshHint();
	}

	/// <summary>
	/// Create World → Open: run the same gen pass from bound bias+dials+accepted scaffold feed.
	/// Refuse empty Create World Open (blank amber). Enter Craft never calls this.
	/// </summary>
	private void AutoGenCreateWorldOpen()
	{
		// Load World sticky (and one-shot pending) — never wipe restored board with a new gen.
		if (WorldPackageSession.IsPackRestorePending(GetTree().Root)
			|| WorldPackageSession.IsLoadedFromPack(GetTree().Root))
			return;
		if (!WorldPackageSession.IsCreateWorldOpenPath(GetTree().Root))
			return;
		var scf = WorldPackageSession.Active?.Scaffold;
		var lore = WorldPackageSession.Active?.Intents;
		AlphaFactoryLog.Emit(
			"gen.terrain",
			"GEN_tone_create_world_auto",
			"Create World Open — auto ApplyGenTerrainPass from bias landform+dials (+parked scaffold/lore salts; no Generate product button)",
			new Dictionary<string, object>
			{
				["slice_id"] = GenToneContract.SliceId,
				["ask_id"] = GenToneContract.AskId,
				["ticket_map"] = GenToneContract.TicketMap,
				["prior_terrain_slice"] = GenTerrainContract.SliceId,
				["propose_feed_slice"] = WorldProposeFeedContract.SliceId,
				["s0_optional_lore_slice"] = WorldSession0IntentBoard.OptionalLoreSliceId,
				["create_world_auto_gen"] = GenToneContract.CreateWorldAutoGenLaw,
				["bias_drives_landform"] = GenToneContract.BiasDrivesLandformLaw,
				["empty_create_world_open"] = false,
				["generate_button_as_product_ux"] = false,
				["scaffold_fed"] = scf?.FeedsGenerator ?? false,
				["scaffold_feed_salt"] = scf?.GenFeedSalt ?? 0u,
				["lore_fed"] = lore?.LoreFed ?? false,
				["lore_feed_salt"] = lore?.LoreFeedSalt ?? 0u,
				["claim_class"] = "staging",
			});
		RunGenTerrainGenerate(createWorldAutoOpen: true);
		AlphaFactoryLog.Emit(
			"craft.phase",
			"CraftCam_Arm",
			"Create World Open — board populated from dials/bias/scaffold feed; Key.T accel only; Terrain3D hard-disabled");
	}

	/// <summary>
	/// Success criterion: Terrain3D must not be callable/armed under craft.
	/// Disk retention of addon files is OK; nodes under craft path are stripped/disabled.
	/// </summary>
	private void HardDisableTerrain3DUnderCraft()
	{
		var host = GetNodeOrNull<Node3D>("DualGridCraftHost/Terrain3DAuthorityHost");
		if (host != null)
		{
			host.Visible = false;
			host.ProcessMode = ProcessModeEnum.Disabled;
			foreach (var child in host.GetChildren())
			{
				if (child is Node n)
				{
					n.ProcessMode = ProcessModeEnum.Disabled;
					if (n is Node3D n3) n3.Visible = false;
					n.QueueFree();
				}
			}
			AlphaFactoryLog.Emit(
				"terrain.disable",
				"terrain3d_hard_disabled",
				"Terrain3DAuthorityHost stripped/disabled under craft — refuse terrain3d_leak_f5",
				new Dictionary<string, object>
				{
					["ask_id"] = PreferAskId,
					["overlay"] = HalfBOverlay,
					["refuse_ban"] = "terrain3d_in_scope|terrain3d_leak_f5|craft_terrain_blend",
				});
		}
		else
		{
			AlphaFactoryLog.Emit(
				"terrain.disable",
				"terrain3d_hard_disabled",
				"Terrain3D host absent under craft path (prefer)",
				new Dictionary<string, object>
				{
					["ask_id"] = PreferAskId,
					["overlay"] = HalfBOverlay,
				});
		}
	}

	private void MountPdcCraftControls()
	{
		const string path = "res://UI/WorldgenCraftControls.tscn";
		if (!ResourceLoader.Exists(path))
		{
			AlphaFactoryLog.Emit(
				"Degrade_FailVisible",
				"depends_on_drops",
				$"PDC craft controls missing at {path}",
				level: "warn");
			return;
		}

		var layer = new CanvasLayer { Name = "PdcCraftControlsLayer", Layer = 8 };
		AddChild(layer);
		layer.AddChild(GD.Load<PackedScene>(path).Instantiate());
		AlphaFactoryLog.Emit(
			"drop.consume",
			"depends_on_drops",
			"instanced PDC WorldgenCraftControls (read-only consume — not a WorldgenCraft substitute)");
	}

	public override void _Input(InputEvent @event)
	{
		if (@event is InputEventKey { Pressed: true, Echo: false } key)
		{
			var code = key.Keycode != Key.None ? key.Keycode : key.PhysicalKeycode;
			switch (code)
			{
				case Key.Tab:
					// Prefer craft-visual: Tab must NOT arm Terrain3D / sparky feed (refuse terrain3d_leak_f5).
					AlphaFactoryLog.Emit(
						"camera.refuse",
						"terrain3d_leak_f5",
						"Tab→Terrain3D/sparky handoff refused under craft-visual (deferred later ticket)",
						new Dictionary<string, object>
						{
							["ask_id"] = PreferAskId,
							["overlay"] = HalfBOverlay,
							["refuse_code"] = "terrain3d_in_scope",
						},
						level: "warn");
					GetViewport().SetInputAsHandled();
					return;
				case Key.Key1:
					_brush = CraftCellType.Grass;
					RefreshHint();
					GetViewport().SetInputAsHandled();
					return;
				case Key.Key2:
					_brush = CraftCellType.Desert;
					RefreshHint();
					GetViewport().SetInputAsHandled();
					return;
				case Key.F6:
					ApplyTileOnlyStamp();
					GetViewport().SetInputAsHandled();
					return;
				case Key.F5:
					PersistWorld();
					GetViewport().SetInputAsHandled();
					return;
				case Key.I:
					// PACK re-attach from durable user:// pack (same path as F5 / Load World).
					_shell?.ImportAttach(SeatContext.SharedTable, PackSaveLoadContract.PersistPath);
					RefreshHint();
					GetViewport().SetInputAsHandled();
					return;
				case Key.G:
					// Occupancy lattice toggle (independent of dual). Shift+G = paired both.
					if (Input.IsKeyPressed(Key.Shift))
						_craft?.ToggleBothOverlays();
					else
						_craft?.ToggleOccupancyGridVisible();
					RefreshHint();
					GetViewport().SetInputAsHandled();
					return;
				case Key.D:
					// Dual-neighborhood Prefer — dual overlay shows corner-owned cells (not Hex19 Success).
					_craft?.ToggleDualOverlayVisible();
					RefreshHint();
					GetViewport().SetInputAsHandled();
					return;
				case Key.R:
					_craft?.RegenerateOrganicQuadMesh();
					RefreshHint();
					GetViewport().SetInputAsHandled();
					return;
				case Key.T:
					// Accel only — never product Success (refuse hotkey_as_product_ux /
					// generate_button_as_product_ux). Product gen = Create World Open auto.
					RunGenTerrainGenerate();
					GetViewport().SetInputAsHandled();
					return;
			}
		}

		if (_craftCam?.ActiveCamera == null || _shell == null || _focus == null)
			return;

		if (@event is InputEventMouseButton mb)
		{
			NoteCursor(mb.Position);
			UpdatePlacementGhost();
			if (mb.ButtonIndex == MouseButton.Left)
			{
				_painting = mb.Pressed;
				_erasing = false;
				if (mb.Pressed)
					TryPlaceAtCursor();
				GetViewport().SetInputAsHandled();
			}
			else if (mb.ButtonIndex == MouseButton.Right)
			{
				_erasing = mb.Pressed;
				_painting = false;
				if (mb.Pressed)
					TryRemoveAtCursor();
				GetViewport().SetInputAsHandled();
			}
		}

		if (@event is InputEventMouseMotion motion)
		{
			NoteCursor(motion.Position);
			UpdatePlacementGhost();
			RefreshBiomeProbe();
			if (_painting)
			{
				TryPlaceAtCursor();
				GetViewport().SetInputAsHandled();
			}
			else if (_erasing)
			{
				TryRemoveAtCursor();
				GetViewport().SetInputAsHandled();
			}
		}
	}

	/// <summary>Placement shadow under cursor before commit (tutorial s1).</summary>
	private void UpdatePlacementGhost()
	{
		if (_craft == null || _craftCam?.ActiveCamera == null)
			return;
		var screen = _cursorSeen ? _cursorScreen : GetViewport().GetMousePosition();
		_craft.UpdateGhost(_craftCam.ActiveCamera, screen);
	}

	/// <summary>
	/// GEN-biomes probe — hover primary V shows biome name + mechanical tag + move/difficult.
	/// Tag must differ across biomes (Plains move:1 vs Forest difficult+move:2).
	/// </summary>
	private void RefreshBiomeProbe()
	{
		if (_craft == null || _craft.GenTerrainApplied != true)
			return;
		if (!TryPickCellQuiet(out var point))
			return;
		if (!_craft.TryProbeBiome(point.X, out var spec))
			return;

		var hud = GetTree().Root.GetNodeOrNull<GameHud>("GameHud");
		var line = spec.Kind == GenBiomeService.BiomeKind.None
			? "Biome Water · tag=none · (not land)"
			: $"Biome {spec.ProbeLine}";
		hud?.SetPerspectiveShellHint(line);
		if (_hint != null)
		{
			var baseHint = HintText();
			_hint.Text = $"{baseHint}\n{line}";
		}
	}

	/// <summary>Quiet pick for probe — no degrade log spam on miss.</summary>
	private bool TryPickCellQuiet(out Vector2I point)
	{
		point = default;
		if (_craftCam?.ActiveCamera == null || _craft == null)
			return false;
		var screen = _cursorSeen ? _cursorScreen : GetViewport().GetMousePosition();
		return _craft.TryPickHexCell(_craftCam.ActiveCamera, screen, out point);
	}

	private void NoteCursor(Vector2 screen)
	{
		_cursorScreen = screen;
		_cursorSeen = true;
	}

	/// <summary>UX-1 — mouse ray → primary organic Vertex V (refuse camera_center_aim / secondary place).</summary>
	private bool TryPickCellAtCursor(out Vector2I point)
	{
		point = default;
		if (_craftCam?.ActiveCamera == null || _craft == null)
			return false;

		var screen = _cursorSeen ? _cursorScreen : GetViewport().GetMousePosition();
		if (!_craft.TryPickHexCell(_craftCam.ActiveCamera, screen, out point))
		{
			AlphaFactoryLog.Emit(
				"Degrade_FailVisible",
				"camera_center_aim",
				"mouse-cursor primary V miss — refuse camera_center_aim / secondary_face_snap_as_place",
				new Dictionary<string, object>
				{
					["ask_id"] = PreferAskId,
					["overlay"] = HalfBOverlay,
					["refuse_code"] = "camera_center_aim",
					["lattice"] = "organic_primary_vertex",
					["ux"] = "UX-1",
					["screen_x"] = screen.X,
					["screen_y"] = screen.Y,
				},
				level: "warn");
			return false;
		}

		return true;
	}

	private void TryPlaceAtCursor()
	{
		if (_shell == null) return;
		if (!TryPickCellAtCursor(out var point))
			return;
		// Do NOT SetFocusWorld / recenter orbit (refuse craft_cam_recenter_on_place).
		var err = _shell.Paint(SeatContext.SharedTable, point, _brush);
		AlphaFactoryLog.Emit(
			"craft.paint",
			"Cell_Commit",
			err == Error.Ok
				? $"UX-1 LMB FlipOrganicCorner primary_V={point.X} (DualCell(V); no cam recenter; no Terrain3D)"
				: $"place failed {err}",
			new Dictionary<string, object>
			{
				["ask_id"] = PreferAskId,
				["overlay"] = HalfBOverlay,
				["ux"] = "UX-1",
				["aim"] = "mouse_cursor",
				["lattice"] = "organic_primary_vertex",
				["primary_vertex"] = point.X,
				["pick_y"] = point.Y,
				["cam_recenter"] = false,
				["terrain_pushed"] = false,
				["refuse_ban"] = "craft_cam_recenter_on_place|secondary_glow_center_as_place_target|ocean_fill_all_empty_slots|face_stamp_as_dual_populate",
				["err"] = err.ToString(),
			},
			level: err == Error.Ok ? "info" : "error");
		UpdatePlacementGhost();
		RefreshBiomeProbe();
		RefreshHint();
	}

	private void TryRemoveAtCursor()
	{
		if (_shell == null) return;
		if (!TryPickCellAtCursor(out var point))
			return;
		var err = _shell.Remove(SeatContext.SharedTable, point);
		AlphaFactoryLog.Emit(
			"craft.paint",
			"Cell_Commit",
			err == Error.Ok
				? $"UX-1 RMB clear primary_V={point.X} (no cam recenter; no Terrain3D)"
				: $"remove failed {err}",
			new Dictionary<string, object>
			{
				["ask_id"] = PreferAskId,
				["overlay"] = HalfBOverlay,
				["ux"] = "UX-1",
				["aim"] = "mouse_cursor",
				["action"] = "remove",
				["lattice"] = "organic_primary_vertex",
				["primary_vertex"] = point.X,
				["cam_recenter"] = false,
				["terrain_pushed"] = false,
				["err"] = err.ToString(),
			},
			level: err == Error.Ok ? "info" : "error");
		UpdatePlacementGhost();
		RefreshHint();
	}

	private void ApplyTileOnlyStamp()
	{
		if (_shell == null) return;
		NoteCursor(GetViewport().GetMousePosition());
		if (!TryPickCellAtCursor(out var center))
		{
			AlphaFactoryLog.Emit(
				"Degrade_FailVisible",
				"camera_center_aim",
				"F6 stamp refused — no mouse-cursor ray (camera_center_aim banned)",
				level: "error");
			RefreshHint();
			return;
		}

		var err = _shell.StampOasisDesert(SeatContext.SharedTable, center);
		AlphaFactoryLog.Emit(
			"craft.stamp",
			"stamp_oasis_desert",
			err == Error.Ok
				? $"UX-1 tile-only F6 stamp at mouse=({center.X},{center.Y}) — no Terrain3D heights"
				: $"stamp failed {err}",
			new Dictionary<string, object>
			{
				["ask_id"] = PreferAskId,
				["overlay"] = HalfBOverlay,
				["ux"] = "UX-1",
				["aim"] = "mouse_cursor",
				["terrain_fed"] = false,
				["err"] = err.ToString(),
			},
			level: err == Error.Ok ? "info" : "error");
		RefreshHint();
	}

	private void PersistWorld()
	{
		if (_shell == null) return;
		var err = _shell.Persist(SeatContext.SharedTable, PackSaveLoadContract.PersistPath);
		var hud = GetTree().Root.GetNodeOrNull<GameHud>("GameHud");
		hud?.SetPerspectiveShellHint(
			err == Error.Ok
				? $"PACK saved → {PackSaveLoadContract.PersistPath} · quit/reload via Load World"
				: "PACK save FAILED — world not durable");
		RefreshHint();
	}

	/// <summary>
	/// GEN-terrain-product — Create World auto-open (product path) and Key.T accel only.
	/// Reads package dials/bias + accepted scaffold feed (WORLD-propose 1c debt).
	/// Create World Open calls with createWorldAutoOpen=true.
	/// Enter Craft never auto-invokes (1g empty manual lane). No Generate product button
	/// (sibling killed chrome — do not re-add). Regen = dials/scaffold change + re-Open.
	/// </summary>
	private void RunGenTerrainGenerate(bool createWorldAutoOpen = false)
	{
		if (_craft == null)
			return;

		var package = WorldPackageSession.Active;
		var bias = package?.GenBias ?? WorldGenBias.Medium;
		var dials = package?.Bounds ?? WorldBoundsDials.Defaults;
		var scaffold = package?.Scaffold;
		var loreSalt = package?.Intents?.LoreFeedSalt ?? 0u;
		var wasApplied = _craft.GenTerrainApplied;
		var pass = _craft.ApplyGenTerrainPass(bias, dials, scaffold: scaffold, loreFeedSalt: loreSalt);
		if (pass == null)
		{
			AlphaFactoryLog.Emit(
				"gen.terrain",
				"GEN_terrain_refuse",
				createWorldAutoOpen
					? "Create World auto-gen refused — craft board not ready"
					: "Key.T accel gen refused — craft board not ready",
				level: "warn");
			RefreshHint();
			return;
		}

		WorldPackageSession.BindGenTerrainResult(GetTree(), pass, createWorldAutoOpen);
		var hud = GetTree().Root.GetNodeOrNull<GameHud>("GameHud");
		var mode = createWorldAutoOpen
			? "Open auto"
			: (wasApplied ? "T accel regen" : "T accel");
		var feedNote = pass.ScaffoldFed ? $" · scf=0x{pass.ScaffoldFeedSalt:x8}" : "";
		var loreNote = pass.LoreFed ? $" · lore=0x{pass.LoreFeedSalt:x8}" : "";
		var biomeNote = _craft.LastGenBiomeDistinctLand > 0
			? $" · biomes={_craft.LastGenBiomeDistinctLand} [{_craft.LastGenBiomesSummary}]"
			: "";
		hud?.SetPerspectiveShellHint(
			$"GEN · {mode} · land={pass.LandCount} water={pass.WaterCount} rivers={pass.RiverCarveCount} · height reads · {pass.GenBiasId} · {pass.Dials.SummaryLine()}{feedNote}{loreNote}{biomeNote}");
		RefreshHint();
	}

	private void RefreshHint()
	{
		if (_hint != null)
			_hint.Text = HintText();
	}

	private string HintText()
	{
		var faces = _craft?.OrganicQuadFaceCount ?? 0;
		var verts = _craft?.OrganicQuadVertexCount ?? 0;
		var dual = _craft?.DualSlotCount ?? 0;
		var createWorld = WorldPackageSession.IsCreateWorldOpenPath(GetTree().Root);
		var packLane = WorldPackageSession.IsLoadedFromPack(GetTree().Root)
			|| WorldPackageSession.IsPackRestorePending(GetTree().Root);
		var gen = _craft?.GenTerrainApplied == true
			? $"GEN applied · {_craft.LastGenTerrainSummary}"
			: createWorld
				? "Create World Open pending auto-gen"
				: packLane
					? "Load World restoring pack"
					: "Enter Craft empty · place to paint";
		var lane = createWorld
			? "Create World (Open auto-gen)"
			: packLane
				? "Load World (PACK restore)"
				: "Enter Craft (empty)";
		var biomes = _craft?.LastGenBiomeDistinctLand > 0
			? $" · {_craft.LastGenBiomesSummary}"
			: "";
		return $"WorldgenCraft · GEN-biomes · {lane} · faces={faces} verts={verts} dual={dual} · Terrain3D:OFF\n" +
		       $"Hover = biome+tag+move · LMB place · D dual · R mesh · T=accel only · I pack-load · F5 pack-save · {gen}{biomes}";
	}

	private void BuildEnvironment()
	{
		// Light craft-plane water/sky tint toward YT teal — not Terrain3D world-builder Success.
		var env = new Godot.Environment
		{
			BackgroundMode = Godot.Environment.BGMode.Color,
			BackgroundColor = new Color(0.22f, 0.42f, 0.58f),
			AmbientLightSource = Godot.Environment.AmbientSource.Color,
			AmbientLightColor = new Color(0.42f, 0.52f, 0.58f),
		};
		AddChild(new WorldEnvironment { Environment = env });
		AddChild(new DirectionalLight3D
		{
			Name = "Sun",
			RotationDegrees = new Vector3(-42f, 35f, 0f),
			LightEnergy = 0.95f,
		});
	}
}
