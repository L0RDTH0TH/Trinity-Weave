using System.Collections.Generic;
using Genesis.Core;
using Genesis.Core.ClosedAlpha;
using Godot;

namespace Genesis.Core.WorldGen;

/// <summary>
/// Primary world-shell entry — refuses wrong seat with Unauthorized (never silent OK).
/// Craft-visual Prefer (<c>alpha0_townscaper_craft_visual</c>): Hot Wheels dual-grid authorship only.
/// Terrain3D feed / height stamp / Tab-sparky handoff are hard-disabled (deferred later ticket).
/// </summary>
public sealed class WorldShellController
{
	public const string TypeName = "Genesis.World.WorldShellController";
	public const string PreferAskId = "alpha0_townscaper_craft_visual";
	public const string PreferOverlay = "alpha0_townscaper_craft_visual_r1";
	public const string SliceId = "row_ux_world_generation_r1_d6";

	private readonly ICraftCellAuthority _craft;
	private bool _armed;

	public WorldShellController(ICraftCellAuthority craft)
	{
		_craft = craft;
	}

	/// <summary>Legacy ctor retained for compile safety — terrain arg is ignored / refused under craft-visual.</summary>
	public WorldShellController(ICraftCellAuthority craft, ITerrainAuthority? terrain)
	{
		_craft = craft;
		if (terrain != null)
		{
			AlphaFactoryLog.Emit(
				"shell.refuse",
				"terrain3d_in_scope",
				"WorldShell craft-visual ignores ITerrainAuthority — Terrain3D hard-disabled under craft (deferred later)",
				new Dictionary<string, object>
				{
					["ask_id"] = PreferAskId,
					["overlay"] = PreferOverlay,
					["refuse_code"] = "terrain3d_in_scope",
					["terrain_ignored"] = true,
				},
				level: "warn");
		}
	}

	public bool IsArmed => _armed;
	public bool WorldExists => _craft.WorldExists;
	public bool TerrainPreferReady => false;

	public Error Enter(SeatContext seat)
	{
		var guard = seat.GuardAny(SeatId.SharedTable, SeatId.DmAsPlayer, SeatId.SessionCompose);
		if (guard != Error.Ok)
		{
			AlphaFactoryLog.Emit(
				"shell.refuse",
				"WorldShell_Enter",
				$"Enter refused seat={seat.Id} → Unauthorized (UX-1/UX-3 wrong seat)",
				new Dictionary<string, object>
				{
					["seat"] = seat.Id.ToString(),
					["type"] = TypeName,
					["result"] = "Unauthorized",
					["ux"] = "UX-1",
					["ux3"] = "UX-3",
				},
				level: "warn");
			return Error.Unauthorized;
		}

		_armed = true;
		AlphaFactoryLog.Emit(
			"shell.enter",
			"WorldShell_Enter",
			$"Enter ok seat={seat.Id} — collaborative worldgen shell armed (UX-1/UX-7)",
			new Dictionary<string, object>
			{
				["seat"] = seat.Id.ToString(),
				["type"] = TypeName,
				["ux"] = "UX-1",
				["ux7"] = "UX-7",
				["ask_id"] = PreferAskId,
				["overlay"] = PreferOverlay,
				["surface"] = "ux_worldgen_gui",
			});
		return Error.Ok;
	}

	/// <summary>Junior verify: Player seat must return Unauthorized (UX-3 — players do not author first world).</summary>
	public Error VerifyWrongSeatRefuse()
	{
		var wasArmed = _armed;
		var probe = Enter(SeatContext.Player);
		_armed = wasArmed;

		if (probe == Error.Unauthorized)
		{
			AlphaFactoryLog.Emit(
				"shell.verify",
				"WorldShell_Enter",
				"VerifyWrongSeatRefuse PASS — Player → Unauthorized (UX-3 players cannot author first world)",
				new Dictionary<string, object> { ["type"] = TypeName, ["ux"] = "UX-3" });
			return Error.Ok;
		}

		AlphaFactoryLog.Emit(
			"Degrade_FailVisible",
			"WorldShell_Enter",
			$"VerifyWrongSeatRefuse FAIL — Player Enter returned {probe} (expected Unauthorized)",
			level: "error");
		return Error.Failed;
	}

	/// <summary>
	/// LMB place / typed paint — dual-grid logic point commit only.
	/// Never pushes Terrain3D (refuse <c>craft_terrain_blend</c>).
	/// </summary>
	public Error Paint(SeatContext seat, Vector2I cell, CraftCellType type, float raiseDelta = 0f)
	{
		if (!_armed) return Error.Unconfigured;
		var guard = seat.GuardAny(SeatId.SharedTable, SeatId.DmAsPlayer, SeatId.SessionCompose);
		if (guard != Error.Ok)
		{
			AlphaFactoryLog.Emit(
				"shell.refuse",
				"Cell_Commit",
				$"Paint refused seat={seat.Id} → Unauthorized (UX-3)",
				level: "warn");
			return Error.Unauthorized;
		}

		_ = raiseDelta; // height raise banned under craft-visual
		var painted = _craft.PaintCell(cell, type, raiseDelta: null);
		if (painted != Error.Ok) return painted;

		AlphaFactoryLog.Emit(
			"shell.place",
			"Cell_Commit",
			"UX-1 craft-visual — dual-grid logic place (no Terrain3D; refuse craft_terrain_blend / craft_cam_recenter_on_place)",
			new Dictionary<string, object>
			{
				["ask_id"] = PreferAskId,
				["overlay"] = PreferOverlay,
				["ux"] = "UX-1",
				["cell_x"] = cell.X,
				["cell_y"] = cell.Y,
				["type"] = type.ToString(),
				["terrain_pushed"] = false,
				["cam_recenter"] = false,
				["refuse_ban"] = "craft_terrain_blend|craft_cam_recenter_on_place|camera_center_aim",
				["claim_class"] = "staging",
			});
		return Error.Ok;
	}

	/// <summary>RMB remove — clear logic point under mouse (dual-grid).</summary>
	public Error Remove(SeatContext seat, Vector2I cell)
	{
		return Paint(seat, cell, CraftCellType.Empty);
	}

	/// <summary>
	/// UX-5 — import/attach a persistent living world as a first-class shell op (not a paste hack).
	/// </summary>
	public Error ImportAttach(SeatContext seat, string path)
	{
		if (!_armed) return Error.Unconfigured;
		var guard = seat.GuardAny(SeatId.SharedTable, SeatId.DmAsPlayer, SeatId.SessionCompose);
		if (guard != Error.Ok)
		{
			AlphaFactoryLog.Emit(
				"shell.refuse",
				"World_ImportAttach",
				$"ImportAttach refused seat={seat.Id} → Unauthorized (UX-5/UX-3)",
				new Dictionary<string, object> { ["ux"] = "UX-5", ["seat"] = seat.Id.ToString() },
				level: "warn");
			return Error.Unauthorized;
		}

		var loaded = _craft.Load(path);
		AlphaFactoryLog.Emit(
			loaded == Error.Ok ? "shell.import" : "Degrade_FailVisible",
			"World_ImportAttach",
			loaded == Error.Ok
				? $"UX-5 import/attach first-class ← {path} (durable table-visible residue)"
				: $"ImportAttach failed {loaded} path={path}",
			new Dictionary<string, object>
			{
				["ask_id"] = PreferAskId,
				["overlay"] = PreferOverlay,
				["ux"] = "UX-5",
				["path"] = path,
				["world_exists"] = _craft.WorldExists,
				["err"] = loaded.ToString(),
			},
			level: loaded == Error.Ok ? "info" : "error");
		return loaded;
	}

	/// <summary>Hard refuse — Terrain3D feed not callable from craft-visual (deferred later).</summary>
	public Error FeedTerrainFromCraftMap(SeatContext seat)
	{
		_ = seat;
		AlphaFactoryLog.Emit(
			"shell.refuse",
			"terrain3d_leak_f5",
			"FeedTerrainFromCraftMap refused — Terrain3D hard-disabled under craft-visual (deferred later ticket)",
			new Dictionary<string, object>
			{
				["ask_id"] = PreferAskId,
				["overlay"] = PreferOverlay,
				["refuse_code"] = "terrain3d_in_scope",
				["ban"] = "terrain3d_leak_f5|craft_terrain_blend",
			},
			level: "warn");
		return Error.Unavailable;
	}

	/// <summary>Tile-only stamp — no Terrain3D height feed (craft-visual).</summary>
	public Error StampOasisDesert(SeatContext seat, Vector2I center)
	{
		if (!_armed) return Error.Unconfigured;
		var guard = seat.GuardAny(SeatId.SharedTable, SeatId.DmAsPlayer, SeatId.SessionCompose);
		if (guard != Error.Ok)
		{
			AlphaFactoryLog.Emit(
				"shell.refuse",
				"stamp_oasis_desert",
				$"Stamp refused seat={seat.Id} → Unauthorized (UX-3)",
				level: "warn");
			return Error.Unauthorized;
		}

		var stamp = _craft.ApplyStampOasisDesert(center, radius: 4);
		if (stamp != Error.Ok) return stamp;

		AlphaFactoryLog.Emit(
			"shell.stamp",
			"stamp_oasis_desert",
			"UX-1 craft-visual — tile-only stamp_oasis_desert (no Terrain3D heights; refuse terrain3d_in_scope)",
			new Dictionary<string, object>
			{
				["ask_id"] = PreferAskId,
				["overlay"] = PreferOverlay,
				["ux"] = "UX-1",
				["terrain_fed"] = false,
				["claim_class"] = "staging",
			});
		return Error.Ok;
	}

	public Error Persist(SeatContext seat, string path)
	{
		if (!_armed) return Error.Unconfigured;
		var guard = seat.GuardAny(SeatId.SharedTable, SeatId.DmAsPlayer, SeatId.SessionCompose);
		if (guard != Error.Ok)
		{
			AlphaFactoryLog.Emit(
				"shell.refuse",
				"World_Persist",
				$"Persist refused seat={seat.Id} → Unauthorized (UX-3)",
				level: "warn");
			return Error.Unauthorized;
		}
		return _craft.Persist(path);
	}
}
