using System;
using System.Collections.Generic;
using System.Globalization;
using System.IO;
using System.Text.Json;
using Godot;

namespace Genesis.Core.ClosedAlpha;

/// <summary>
/// Factory runtime logging bus — state transitions, checklist boundaries, degradation.
/// Forbidden: seat-critical events via raw GD.Print only (Degrade_FailVisible anti-pattern).
/// </summary>
public static class AlphaFactoryLog
{
	private static readonly object FileLock = new();
	private static string _runtimePath = "";

	public static void ConfigureRuntimePath(string? path = null)
	{
		_runtimePath = string.IsNullOrWhiteSpace(path)
			? ProjectSettings.GlobalizePath("res://logs/factory-runtime.jsonl")
			: path;
	}

	public static void Emit(
		string category,
		string? checklistId,
		string detail,
		IReadOnlyDictionary<string, object>? observation = null,
		string level = "info")
	{
		if (string.IsNullOrEmpty(_runtimePath))
			ConfigureRuntimePath();

		var ts = DateTime.UtcNow.ToString("o", CultureInfo.InvariantCulture);
		var row = new Dictionary<string, object>
		{
			["ts"] = ts,
			["category"] = category,
			["detail"] = detail,
			["level"] = level,
			["slice_id"] = "row_ux_world_generation_r1_d6",
			["weld_slice_id"] = "alpha0_townscaper_craft_visual_r1",
			["ask_id"] = "alpha0_townscaper_craft_visual",
			["claim_class"] = "staging",
			["ux_bullet"] = "UX-1",
			["lane_id"] = "module",
			["half_b_overlay"] = "alpha0_townscaper_craft_visual_r1",
		};
		if (!string.IsNullOrWhiteSpace(checklistId))
			row["checklist_id"] = checklistId;

		var runId = OS.GetEnvironment("GMM_FACTORY_RUN_ID");
		if (!string.IsNullOrWhiteSpace(runId))
			row["run_id"] = runId;

		if (observation is { Count: > 0 })
			row["observation"] = observation;

		try
		{
			var dir = Path.GetDirectoryName(_runtimePath);
			if (!string.IsNullOrEmpty(dir))
				Directory.CreateDirectory(dir);
			lock (FileLock)
			{
				File.AppendAllText(_runtimePath, JsonSerializer.Serialize(row) + "\n");
			}
		}
		catch (Exception ex)
		{
			GD.PushWarning($"AlphaFactoryLog runtime file write failed: {ex.Message}");
		}

		PushMcpRuntimeLog(level, category, checklistId, detail);
	}

	private static void PushMcpRuntimeLog(string level, string category, string? checklistId, string detail)
	{
		try
		{
			var tree = Engine.GetMainLoop() as SceneTree;
			var mcp = tree?.Root?.GetNodeOrNull("/root/MCPRuntime");
			if (mcp == null)
				return;

			var cid = string.IsNullOrWhiteSpace(checklistId) ? "-" : checklistId;
			var line = $"factory|{level}|{category}|checklist_id={cid}|{detail}";
			mcp.Call("push_runtime_log", level, line);
		}
		catch (Exception ex)
		{
			GD.PushWarning($"AlphaFactoryLog MCP push failed: {ex.Message}");
		}
	}
}
