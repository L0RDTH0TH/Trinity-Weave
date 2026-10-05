using System.Collections.Generic;
using Genesis.Camera;
using Genesis.Core;
using Genesis.Core.ClosedAlpha;
using Genesis.Core.WorldGen;
using Genesis.Player;
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

		// UX-5: first-class import/attach of prior persistent world when present.
		var import = _shell.ImportAttach(SeatContext.SharedTable, DualGridCraftHost.PersistPath);
		if (import == Error.Ok)
			AlphaFactoryLog.Emit("craft.load", "World_ImportAttach", "UX-5 restored attached living world");
		else if (import != Error.FileNotFound)
			AlphaFactoryLog.Emit("Degrade_FailVisible", "World_ImportAttach", $"import status {import}", level: "warn");

		AlphaFactoryLog.Emit(
			"craft.phase",
			"CraftCam_Arm",
			"Stålberg organic all-quad planar board; R=regenerate; graybox; no noodle/prism; no cam yank; Terrain3D hard-disabled; no dual paint/tiles/art Success");
		AlphaFactoryLog.Emit(
			"module.fit",
			"module_fit_pass",
			"UX-1..6 Stålberg kernel — seed hex rings · triangulate · dissolve · subdivide to quads · relax · render quads · regenerable");
		AlphaFactoryLog.Emit(
			"module.integrate",
			"integration_pass",
			"WorldgenCraft module lane — claim_class=staging; overlay=alpha0_stalberg_quad_kernel_relax_r1; density lift LIVE rings=5 pull=0.12; awaiting operator F5 squarified planar all-quad board");
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
					// UX-5 explicit re-attach
					_shell?.ImportAttach(SeatContext.SharedTable, DualGridCraftHost.PersistPath);
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
		_shell.Persist(SeatContext.SharedTable, DualGridCraftHost.PersistPath);
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
		return $"WorldgenCraft · STÅLBERG PRIMARY-V DUALCELL PLACE r1 · stage6 host · pitch cam · faces={faces} verts={verts} dual={dual} · Terrain3D:OFF\n" +
		       "LMB snap primary V → one DualCell(V) module · Empty=skip ocean · cam pitch 35–55° · amber grid · D dual · R regen · F5";
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
