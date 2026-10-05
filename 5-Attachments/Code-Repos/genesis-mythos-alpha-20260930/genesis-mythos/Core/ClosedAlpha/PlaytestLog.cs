using System;
using System.Collections.Generic;
using System.Globalization;
using System.IO;
using System.Text.Json;
using Godot;

namespace Genesis.Core.ClosedAlpha;

/// <summary>Playtest session facade on AlphaFactoryLog — Layer D session JSONL.</summary>
public static class PlaytestLog
{
	private static readonly object SessionLock = new();
	private static string _sessionPath = "";
	private static string _sliceId = "alpha0_worldgen_dualgrid_sparky_r1";

	public static bool Active => !string.IsNullOrEmpty(_sessionPath);

	public static void BeginSession(string? sessionPath = null, string? sliceId = null)
	{
		lock (SessionLock)
		{
			_sessionPath = string.IsNullOrWhiteSpace(sessionPath)
				? ProjectSettings.GlobalizePath($"user://playtest/session-{DateTime.UtcNow:yyyyMMddTHHmmss}.jsonl")
				: ProjectSettings.GlobalizePath(sessionPath);
			_sliceId = string.IsNullOrWhiteSpace(sliceId)
				? (OS.GetEnvironment("GMM_PLAYTEST_SLICE") ?? "alpha0_worldgen_dualgrid_sparky_r1")
				: sliceId;

			var dir = Path.GetDirectoryName(_sessionPath);
			if (!string.IsNullOrEmpty(dir))
				Directory.CreateDirectory(dir);

			AlphaFactoryLog.Emit("playtest", "Flow_Launch", $"session_begin slice={_sliceId} path={_sessionPath}");
		}
	}

	public static void EndSession()
	{
		if (!Active) return;
		AlphaFactoryLog.Emit("playtest", "Flow_Launch", "session_end");
		lock (SessionLock)
			_sessionPath = "";
	}

	public static void EmitOperatorMark(string checklistId, string verdict, string note = "")
	{
		if (!Active) return;
		var row = new Dictionary<string, object>
		{
			["type"] = "operator_mark",
			["checklist_id"] = checklistId,
			["verdict"] = verdict,
			["note"] = note,
			["slice_id"] = _sliceId,
			["ts"] = DateTime.UtcNow.ToString("o", CultureInfo.InvariantCulture),
		};
		try
		{
			lock (SessionLock)
				File.AppendAllText(_sessionPath, JsonSerializer.Serialize(row) + "\n");
		}
		catch (Exception ex)
		{
			GD.PushWarning($"PlaytestLog write failed: {ex.Message}");
		}

		AlphaFactoryLog.Emit("playtest_mark", checklistId, $"{verdict}: {note}");
	}
}
