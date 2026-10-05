using System.Collections.Generic;
using System.IO;
using System.Text.Json;
using Genesis.Core.ClosedAlpha;
using Godot;

namespace Genesis.Core.WorldGen;

/// <summary>Consumes ADC/TAC/CDC/PDC drop manifests (read-only) before module integrate.</summary>
public static class FactoryDropRegistry
{
	public sealed record DropRef(string Contract, string DropId, string Path);

	public static IReadOnlyList<DropRef> ConsumeRequiredDrops(string gameRepoAbs)
	{
		var found = new List<DropRef>();
		var required = new (string Contract, string Rel)[]
		{
			("adc", "assets/_factory/manifest.yaml"),
			("tac", "assets/_techart/_factory/manifest.yaml"),
			("cdc", "content/_factory/manifest.yaml"),
			("pdc", "UI/_factory/manifest.yaml"),
			("audc", "audio/_factory/manifest.yaml"),
		};

		foreach (var (contract, rel) in required)
		{
			var full = Path.Combine(gameRepoAbs, rel);
			if (!File.Exists(full))
			{
				AlphaFactoryLog.Emit(
					"Degrade_FailVisible",
					"depends_on_drops",
					$"missing drop manifest {contract}:{rel}",
					level: "error");
				continue;
			}

			foreach (var id in ReadDropIds(File.ReadAllText(full)))
			{
				found.Add(new DropRef(contract, id, rel));
				AlphaFactoryLog.Emit(
					"drop.consume",
					"depends_on_drops",
					$"consumed {contract} drop_id={id}",
					new Dictionary<string, object> { ["contract"] = contract, ["drop_id"] = id });
			}
		}

		return found;
	}

	private static IEnumerable<string> ReadDropIds(string text)
	{
		foreach (var line in text.Split('\n'))
		{
			var t = line.Trim();
			// YAML list item: "- drop_id: foo" or plain "drop_id: foo"
			if (t.StartsWith("- ", System.StringComparison.Ordinal))
				t = t[2..].Trim();
			if (!t.StartsWith("drop_id:", System.StringComparison.Ordinal))
				continue;
			var id = t["drop_id:".Length..].Trim().Trim('\'', '"');
			if (!string.IsNullOrWhiteSpace(id))
				yield return id;
		}
	}

	public static string ToJson(IReadOnlyList<DropRef> drops) =>
		JsonSerializer.Serialize(drops);
}
