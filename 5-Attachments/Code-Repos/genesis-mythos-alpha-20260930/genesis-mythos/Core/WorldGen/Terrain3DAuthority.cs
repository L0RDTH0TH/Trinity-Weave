using System.Collections.Generic;
using Genesis.Core.ClosedAlpha;
using Godot;

namespace Genesis.Core.WorldGen;

/// <summary>
/// Terrain3D Prefer-path wrapper (Matrix Dual-grid Prefer).
/// Host under WorldgenCraft / DualGridCraftHost. ClassDB Prefer required for Success;
/// Multimesh/graybox-only height preview = fail visible <c>graybox_only_world</c>.
/// Prefer r3 layer-split: craft hides this host (toys only); Sparky enter / explicit feed
/// pushes tile map → set_height/update_maps (Hot Wheels ≠ car).
/// </summary>
public sealed class Terrain3DAuthority : ITerrainAuthority
{
	public const string PreferBackend = "terrain3d";
	public const string PluginCfg = "res://addons/terrain_3d/plugin.cfg";
	public const string GdExtension = "res://addons/terrain_3d/terrain.gdextension";
	public const string LinuxDebugSo = "res://addons/terrain_3d/bin/libterrain.linux.debug.x86_64.so";
	/// <summary>Terrain3DRegion.TYPE_MAX — HEIGHT/CONTROL/COLOR.</summary>
	public const int MapTypeMax = 3;

	private readonly Dictionary<Vector2I, float> _heights = new();
	private Node3D? _host;
	private Node3D? _terrainNode;
	private GodotObject? _dataObj;
	private MultiMeshInstance3D? _preview;
	private bool _degradedLogged;
	private bool _vendorArmedLogged;
	private int _pendingVendorPushes;
	private int _vendorPushCount;
	private bool _lastFlushOk;

	public string BackendId => PreferBackend;
	public bool AddonOnDisk =>
		Godot.FileAccess.FileExists(PluginCfg)
		|| Godot.FileAccess.FileExists(GdExtension)
		|| Godot.FileAccess.FileExists(LinuxDebugSo);
	public bool ClassDbReady => ClassDB.ClassExists("Terrain3D");
	public bool VendorPresent => AddonOnDisk || ClassDbReady;
	public bool LiveMeshArmed => ClassDbReady && _terrainNode != null && GodotObject.IsInstanceValid(_terrainNode);
	public bool IsDegraded => !LiveMeshArmed;
	public bool HasVendorHeightFeed => _vendorPushCount > 0 && _lastFlushOk && LiveMeshArmed;
	public int VendorPushCount => _vendorPushCount;

	public Error EnsureHost(Node3D parent)
	{
		if (parent == null) return Error.InvalidParameter;
		if (_host != null && GodotObject.IsInstanceValid(_host))
		{
			if (_host.GetParent() != parent)
			{
				_host.GetParent()?.RemoveChild(_host);
				parent.AddChild(_host);
			}
			return Error.Ok;
		}

		// Prefer: live Terrain3D under DualGridCraftHost (or WorldgenCraft).
		_host = parent.GetNodeOrNull<Node3D>("Terrain3DAuthorityHost");
		if (_host == null)
		{
			_host = new Node3D { Name = "Terrain3DAuthorityHost" };
			parent.AddChild(_host);
		}

		if (ClassDbReady)
			TryMountLiveTerrain3D();

		if (_terrainNode == null)
			ArmDegradedPreview();
		else
			HideDegradedPreview();

		AlphaFactoryLog.Emit(
			"terrain.host",
			"Terrain3D_Vendor",
			LiveMeshArmed
				? $"Terrain3D Prefer host armed under {parent.Name}/Terrain3DAuthorityHost"
				: $"Terrain3D Prefer host DEGRADED under {parent.Name} — graybox_only_world until ClassDB Prefer",
			new Dictionary<string, object>
			{
				["parent"] = parent.Name,
				["live_mesh"] = LiveMeshArmed,
				["classdb"] = ClassDbReady,
				["addon_on_disk"] = AddonOnDisk,
				["matrix_row"] = "Dual-grid world craft",
				["prefer"] = "Terrain3D height authority + GridMap craft overlay",
				["never"] = "parallel terrain engine; GridMap as second height authority",
			},
			level: LiveMeshArmed ? "info" : "warn");

		return Error.Ok;
	}

	private void TryMountLiveTerrain3D()
	{
		try
		{
			var existing = _host!.GetNodeOrNull<Node3D>("Terrain3D_Prefer");
			if (existing != null && GodotObject.IsInstanceValid(existing))
			{
				_terrainNode = existing;
				CacheDataObject();
				LogVendorArmed();
				SetVisibleForCraftPhase(craftPhaseActive: true);
				return;
			}

			var inst = ClassDB.Instantiate("Terrain3D");
			if (inst.AsGodotObject() is not Node3D terrain)
			{
				AlphaFactoryLog.Emit(
					"Degrade_FailVisible",
					"Terrain3D_Vendor",
					"ClassDB.Instantiate(Terrain3D) did not yield Node3D",
					level: "warn");
				return;
			}

			terrain.Name = "Terrain3D_Prefer";
			_host!.AddChild(terrain);
			_terrainNode = terrain;

			var dataDir = ProjectSettings.GlobalizePath("user://worldgen/terrain3d_prefer_r3");
			DirAccess.MakeDirRecursiveAbsolute(dataDir);
			terrain.Call("set_data_directory", dataDir);
			terrain.Call("set_show_checkered", true);
			terrain.Call("set_show_heightmap", false);
			terrain.Call("set_collision_mode", 1); // Dynamic — Sparky can inspect mesh with collision

			CacheDataObject();
			LogVendorArmed();
			// Prefer r3: start hidden under craft — Hot Wheels toys only until Sparky/explicit feed.
			SetVisibleForCraftPhase(craftPhaseActive: true);
		}
		catch (System.Exception ex)
		{
			AlphaFactoryLog.Emit(
				"Degrade_FailVisible",
				"Terrain3D_Vendor",
				$"Terrain3D instantiate failed: {ex.Message}",
				level: "warn");
		}
	}

	private void LogVendorArmed()
	{
		if (_vendorArmedLogged) return;
		_vendorArmedLogged = true;
		AlphaFactoryLog.Emit(
			"terrain.authority",
			"Terrain3D_Vendor",
			"Terrain3D ClassDB Prefer height authority path armed",
			new Dictionary<string, object>
			{
				["backend"] = BackendId,
				["vendor_present"] = true,
				["classdb"] = true,
				["ask_id"] = "alpha0_worldgen_terrain3d_feed",
				["matrix_row"] = "Dual-grid world craft",
			});
	}

	private void CacheDataObject()
	{
		_dataObj = null;
		if (_terrainNode == null) return;
		var dataVar = _terrainNode.Call("get_data");
		if (dataVar.VariantType == Variant.Type.Nil) return;
		_dataObj = dataVar.AsGodotObject();
	}

	private void ArmDegradedPreview()
	{
		if (!_degradedLogged)
		{
			_degradedLogged = true;
			var reason = AddonOnDisk
				? "terrain_3d addon on disk but ClassDB Terrain3D not loaded — Multimesh stand-in only; fail graybox_only_world (not Prefer Success)"
				: "terrain_3d addon missing — Multimesh stand-in only; fail graybox_only_world. Install addons/terrain_3d (Matrix Prefer).";
			AlphaFactoryLog.Emit(
				"Degrade_FailVisible",
				"graybox_only_world",
				reason,
				new Dictionary<string, object>
				{
					["backend"] = BackendId,
					["addon_on_disk"] = AddonOnDisk,
					["classdb"] = ClassDbReady,
					["refuse_code"] = "graybox_only_world",
					["matrix_row"] = "Dual-grid world craft",
				},
				level: "warn");
		}

		if (_preview != null && GodotObject.IsInstanceValid(_preview))
			return;

		_preview = new MultiMeshInstance3D { Name = "HeightPreview_Degraded_NOT_Prefer" };
		var mm = new MultiMesh
		{
			TransformFormat = MultiMesh.TransformFormatEnum.Transform3D,
			Mesh = new BoxMesh { Size = new Vector3(0.95f, 0.2f, 0.95f) },
		};
		_preview.Multimesh = mm;
		_preview.MaterialOverride = new StandardMaterial3D
		{
			AlbedoColor = new Color(0.75f, 0.25f, 0.2f),
			Roughness = 0.9f,
		};
		_host!.AddChild(_preview);
	}

	private void HideDegradedPreview()
	{
		if (_preview == null) return;
		_preview.QueueFree();
		_preview = null;
	}

	public Error SetCellHeight(Vector2I cell, float height)
	{
		_heights[cell] = Mathf.Max(0f, height);
		if (!TryPushHeightToVendor(cell, _heights[cell]))
		{
			RebuildPreview();
			return LiveMeshArmed ? Error.Failed : Error.Ok;
		}

		_pendingVendorPushes++;
		RebuildPreview();
		return Error.Ok;
	}

	public float GetCellHeight(Vector2I cell) =>
		_heights.TryGetValue(cell, out var h) ? h : 0f;

	public Error ImportHeightField(float[,] heights, Vector3 worldOrigin)
	{
		if (heights == null) return Error.InvalidParameter;
		if (IsDegraded)
			return FailGrayboxOnly("ImportHeightField refused — Terrain3D ClassDB Prefer not armed");

		var w = heights.GetLength(0);
		var h = heights.GetLength(1);
		var originCell = new Vector2I(Mathf.FloorToInt(worldOrigin.X), Mathf.FloorToInt(worldOrigin.Z));
		for (var z = 0; z < h; z++)
		for (var x = 0; x < w; x++)
		{
			var cell = new Vector2I(originCell.X + x, originCell.Y + z);
			_heights[cell] = heights[x, z];
			TryPushHeightToVendor(cell, heights[x, z]);
			_pendingVendorPushes++;
		}

		var flush = FlushVendorMaps();
		AlphaFactoryLog.Emit(
			"terrain.import",
			"Terrain3D_Admit",
			$"ImportHeightField {w}x{h} origin={worldOrigin} flush={flush}");
		return flush;
	}

	/// <summary>
	/// Prefer r3 UX-2/UX-3: hide Terrain3D under craft (refuse craft_terrain_blend);
	/// reveal after Sparky enter / explicit feed.
	/// </summary>
	public void SetVisibleForCraftPhase(bool craftPhaseActive)
	{
		if (_host != null && GodotObject.IsInstanceValid(_host))
			_host.Visible = !craftPhaseActive;
		if (_preview != null && GodotObject.IsInstanceValid(_preview))
			_preview.Visible = !craftPhaseActive;

		AlphaFactoryLog.Emit(
			"terrain.layer",
			craftPhaseActive ? "craft_terrain_blend" : "Terrain3D_Vendor",
			craftPhaseActive
				? "UX-2 — Terrain3D host HIDDEN under craft (Hot Wheels toys only; refuse craft_terrain_blend)"
				: "UX-3 — Terrain3D host VISIBLE under Sparky (fed real-car layer)",
			new Dictionary<string, object>
			{
				["ask_id"] = "alpha0_worldgen_terrain3d_feed",
				["overlay"] = "alpha0_worldgen_terrain3d_feed_r3",
				["craft_phase"] = craftPhaseActive,
				["visible"] = !craftPhaseActive,
				["refuse_ban"] = "craft_terrain_blend",
				["ux"] = craftPhaseActive ? "UX-2" : "UX-3",
			});
	}

	/// <summary>
	/// Prefer r3 UX-3: batch feed craft tile map → Terrain3D (Sparky enter / explicit feed).
	/// Not invoked on live craft place — that would re-blend layers under craft cam.
	/// </summary>
	public Error FeedFromCraftCells(IReadOnlyDictionary<Vector2I, CraftCellType> cells)
	{
		if (cells == null || cells.Count == 0)
			return FailGrayboxOnly(
				"FeedFromCraftCells refused — empty tile map (unfed_terrain_under_sparky / graybox_only_world)");

		if (IsDegraded)
			return FailGrayboxOnly(
				"tile map→Terrain3D feed refused — Multimesh/graybox alone (ClassDB Prefer not armed). refuse_code=graybox_only_world|unfed_terrain_under_sparky");

		_pendingVendorPushes = 0;
		Vector2I? proofCell = null;
		float proofMin = 0.2f;
		var pushed = 0;
		foreach (var (cell, type) in cells)
		{
			if (type == CraftCellType.Empty) continue;
			var typeH = HeightForCraftType(type);
			// Preserve richer explicit-stamp heights; raise floor from craft tile type.
			var height = Mathf.Max(GetCellHeight(cell), typeH);
			_heights[cell] = height;
			if (!TryPushHeightToVendor(cell, height))
				return FailGrayboxOnly($"feed set_height failed at ({cell.X},{cell.Y}) — refuse unfed_terrain_under_sparky");
			_pendingVendorPushes++;
			pushed++;
			proofCell ??= cell;
			proofMin = Mathf.Max(0.2f, height * 0.4f);
		}

		if (pushed == 0)
			return FailGrayboxOnly("FeedFromCraftCells — no non-empty craft cells to feed");

		var flush = FlushVendorMaps();
		if (flush != Error.Ok)
			return FailGrayboxOnly("feed update_maps flush failed — Terrain3D not fed from tile map");

		if (proofCell is { } pc && !VerifyVendorHeightReadback(pc, minExpected: proofMin))
			return FailGrayboxOnly($"feed Terrain3D get_height readback failed at ({pc.X},{pc.Y})");

		AlphaFactoryLog.Emit(
			"terrain.feed",
			"Terrain3D_Admit",
			$"UX-3 Prefer — tile map → Terrain3D fed layer (fed_cells={pushed} vendor_pushes={_vendorPushCount})",
			new Dictionary<string, object>
			{
				["ask_id"] = "alpha0_worldgen_terrain3d_feed",
				["overlay"] = "alpha0_worldgen_terrain3d_feed_r3",
				["ux"] = "UX-3",
				["cell_count"] = cells.Count,
				["fed_cells"] = pushed,
				["live_mesh"] = true,
				["vendor_pushes"] = _vendorPushCount,
				["refuse_ban"] = "unfed_terrain_under_sparky",
				["feed_when"] = "sparky_enter_or_explicit",
				["claim_class"] = "staging",
			});
		return Error.Ok;
	}

	public Error ApplyStampOasisDesertHeights(Vector2I center, int radius = 4)
	{
		if (IsDegraded)
			return FailGrayboxOnly(
				$"stamp_oasis_desert height push refused — Multimesh/graybox alone (ClassDB Prefer not armed). refuse_code=graybox_only_world");

		_pendingVendorPushes = 0;
		for (var z = -radius; z <= radius; z++)
		for (var x = -radius; x <= radius; x++)
		{
			var c = new Vector2I(center.X + x, center.Y + z);
			var dist = Mathf.Sqrt(x * x + z * z);
			float height;
			if (dist < 0.5f)
				height = 0.35f; // oasis dip (still above void)
			else if (dist <= radius * 0.45f)
				height = 1.2f + (radius * 0.45f - dist) * 0.4f;
			else
			{
				// Desert dune ring — visible Terrain3D mesh residue for Sparky
				var t = 1f - Mathf.Abs(dist - radius * 0.75f) / (radius * 0.35f + 0.01f);
				height = 2.5f + Mathf.Clamp(t, 0f, 1f) * 5.5f;
			}

			_heights[c] = height;
			if (!TryPushHeightToVendor(c, height))
				return FailGrayboxOnly($"stamp_oasis_desert set_height failed at ({c.X},{c.Y})");
			_pendingVendorPushes++;
		}

		var flush = FlushVendorMaps();
		if (flush != Error.Ok)
			return FailGrayboxOnly("stamp_oasis_desert update_maps flush failed — Terrain3D mesh not updated");

		// Read-back Prefer proof: get_height at dune sample must be finite / non-zero.
		var proofOk = VerifyVendorHeightReadback(center + new Vector2I(radius, 0), minExpected: 2f);
		if (!proofOk)
			return FailGrayboxOnly("stamp_oasis_desert Terrain3D get_height readback failed — mesh feed not proven");

		AlphaFactoryLog.Emit(
			"terrain.stamp",
			"stamp_oasis_desert",
			$"Prefer feed OK — stamp_oasis_desert → Terrain3D height/region + update_maps (pushes={_vendorPushCount})",
			new Dictionary<string, object>
			{
				["stamp_id"] = "stamp_oasis_desert",
				["ask_id"] = "alpha0_worldgen_terrain3d_feed",
				["overlay"] = "alpha0_worldgen_terrain3d_feed_r3",
				["feed_when"] = "explicit_stamp",
				["center_x"] = center.X,
				["center_y"] = center.Y,
				["radius"] = radius,
				["live_mesh"] = true,
				["vendor_pushes"] = _vendorPushCount,
				["claim_class"] = "staging",
			});
		return Error.Ok;
	}

	private static float HeightForCraftType(CraftCellType type) => type switch
	{
		CraftCellType.Grass => 1.15f,
		CraftCellType.Desert => 1.65f,
		CraftCellType.Oasis => 0.45f,
		_ => 0f,
	};

	public Error FlushVendorMaps()
	{
		if (!LiveMeshArmed || _dataObj == null)
			return FailGrayboxOnly("FlushVendorMaps — no live Terrain3D data");

		try
		{
			// Terrain3DRegion.TYPE_MAX, regenerate all maps, no mipmaps required for Prefer proof.
			_dataObj.Call("update_maps", MapTypeMax, true, false);
			_dataObj.Call("calc_height_range", true);
			_vendorPushCount += _pendingVendorPushes;
			_pendingVendorPushes = 0;
			_lastFlushOk = true;
			AlphaFactoryLog.Emit(
				"terrain.flush",
				"Terrain3D_Vendor",
				$"update_maps(TYPE_MAX) ok — vendor_pushes_total={_vendorPushCount}");
			return Error.Ok;
		}
		catch (System.Exception ex)
		{
			_lastFlushOk = false;
			return FailGrayboxOnly($"update_maps failed: {ex.Message}");
		}
	}

	public Aabb GetTerrainBounds()
	{
		if (_heights.Count == 0)
			return new Aabb(Vector3.Zero, new Vector3(1, 1, 1));
		var min = new Vector3(float.MaxValue, 0, float.MaxValue);
		var max = new Vector3(float.MinValue, 1, float.MinValue);
		foreach (var (cell, height) in _heights)
		{
			min.X = Mathf.Min(min.X, cell.X);
			min.Z = Mathf.Min(min.Z, cell.Y);
			max.X = Mathf.Max(max.X, cell.X + 1);
			max.Z = Mathf.Max(max.Z, cell.Y + 1);
			max.Y = Mathf.Max(max.Y, height + 0.5f);
		}
		return new Aabb(min, max - min);
	}

	private bool TryPushHeightToVendor(Vector2I cell, float height)
	{
		if (!LiveMeshArmed)
			return false;

		try
		{
			if (_dataObj == null || !GodotObject.IsInstanceValid(_dataObj))
				CacheDataObject();
			if (_dataObj == null)
				return false;

			var world = new Vector3(cell.X + 0.5f, 0f, cell.Y + 0.5f);
			var hasRegion = _dataObj.Call("has_regionp", world).AsBool();
			if (!hasRegion)
				_dataObj.Call("add_region_blankp", world, true);

			_dataObj.Call("set_height", world, height);
			return true;
		}
		catch (System.Exception ex)
		{
			AlphaFactoryLog.Emit(
				"Degrade_FailVisible",
				"Terrain3D_Vendor",
				$"set_height push failed cell=({cell.X},{cell.Y}): {ex.Message}",
				level: "warn");
			return false;
		}
	}

	private bool VerifyVendorHeightReadback(Vector2I cell, float minExpected)
	{
		if (_dataObj == null) return false;
		try
		{
			var world = new Vector3(cell.X + 0.5f, 0f, cell.Y + 0.5f);
			var h = _dataObj.Call("get_height", world).AsSingle();
			var ok = !float.IsNaN(h) && h >= minExpected * 0.5f;
			AlphaFactoryLog.Emit(
				"terrain.verify",
				"stamp_oasis_desert",
				ok
					? $"Terrain3D get_height readback ok h={h:F2} at ({cell.X},{cell.Y})"
					: $"Terrain3D get_height readback weak h={h:F2} expected≥{minExpected}",
				level: ok ? "info" : "warn");
			return ok;
		}
		catch (System.Exception ex)
		{
			AlphaFactoryLog.Emit(
				"Degrade_FailVisible",
				"graybox_only_world",
				$"get_height readback threw: {ex.Message}",
				level: "warn");
			return false;
		}
	}

	private Error FailGrayboxOnly(string message)
	{
		_lastFlushOk = false;
		AlphaFactoryLog.Emit(
			"Degrade_FailVisible",
			"graybox_only_world",
			message,
			new Dictionary<string, object>
			{
				["refuse_code"] = "graybox_only_world",
				["live_mesh"] = LiveMeshArmed,
				["classdb"] = ClassDbReady,
				["ask_id"] = "alpha0_worldgen_terrain3d_feed",
			},
			level: "error");
		RebuildPreview();
		return Error.Failed;
	}

	private void RebuildPreview()
	{
		// Multimesh is FailVisible stand-in only — never Prefer Success.
		if (_preview?.Multimesh == null) return;
		var mm = _preview.Multimesh;
		mm.InstanceCount = _heights.Count;
		var i = 0;
		foreach (var (cell, height) in _heights)
		{
			var y = Mathf.Max(0.05f, height);
			var xf = new Transform3D(
				Basis.Identity.Scaled(new Vector3(1f, Mathf.Max(0.2f, y * 0.35f), 1f)),
				new Vector3(cell.X + 0.5f, y * 0.5f, cell.Y + 0.5f));
			mm.SetInstanceTransform(i++, xf);
		}
	}
}
