using System;
using System.Collections.Generic;
using System.Globalization;
using Godot;

namespace Genesis.Core.WorldGen;

/// <summary>
/// GEN-biomes assigner (<c>alpha0_gen_biomes_r1</c>).
/// Maps land vertices to biomes from altitude band + climate (+ wildness patch noise).
/// Each biome exposes move_cost / difficult_terrain tags AND a distinct albedo tint.
/// Water stays biome-none (amber empty / river ribbon). No creatures.
/// </summary>
public static class GenBiomeService
{
	public enum BiomeKind : byte
	{
		None = 0,
		Plains = 1,
		Forest = 2,
		Highland = 3,
		Marsh = 4,
		Desert = 5,
	}

	public readonly struct BiomeSpec
	{
		public BiomeKind Kind { get; init; }
		public string Name { get; init; }
		public string MechanicalTag { get; init; }
		public int MoveCost { get; init; }
		public bool DifficultTerrain { get; init; }
		public Color Albedo { get; init; }

		public string ProbeLine =>
			DifficultTerrain
				? $"{Name} · {MechanicalTag} · move={MoveCost} · difficult"
				: $"{Name} · {MechanicalTag} · move={MoveCost}";
	}

	public static readonly BiomeSpec SpecNone = new()
	{
		Kind = BiomeKind.None,
		Name = "Water",
		MechanicalTag = "none",
		MoveCost = 0,
		DifficultTerrain = false,
		Albedo = new Color(0.14f, 0.32f, 0.48f, 1f),
	};

	public static readonly BiomeSpec SpecPlains = new()
	{
		Kind = BiomeKind.Plains,
		Name = "Plains",
		MechanicalTag = "move:1",
		MoveCost = 1,
		DifficultTerrain = false,
		Albedo = new Color(0.52f, 0.72f, 0.34f, 1f), // bright grass
	};

	public static readonly BiomeSpec SpecForest = new()
	{
		Kind = BiomeKind.Forest,
		Name = "Forest",
		MechanicalTag = "difficult+move:2",
		MoveCost = 2,
		DifficultTerrain = true,
		Albedo = new Color(0.18f, 0.42f, 0.22f, 1f), // deep canopy green
	};

	public static readonly BiomeSpec SpecHighland = new()
	{
		Kind = BiomeKind.Highland,
		Name = "Highland",
		MechanicalTag = "difficult+move:3",
		MoveCost = 3,
		DifficultTerrain = true,
		Albedo = new Color(0.58f, 0.56f, 0.52f, 1f), // rock gray
	};

	public static readonly BiomeSpec SpecMarsh = new()
	{
		Kind = BiomeKind.Marsh,
		Name = "Marsh",
		MechanicalTag = "difficult+move:2",
		MoveCost = 2,
		DifficultTerrain = true,
		Albedo = new Color(0.38f, 0.48f, 0.28f, 1f), // olive wetland
	};

	public static readonly BiomeSpec SpecDesert = new()
	{
		Kind = BiomeKind.Desert,
		Name = "Desert",
		MechanicalTag = "move:2",
		MoveCost = 2,
		DifficultTerrain = false,
		Albedo = new Color(0.82f, 0.68f, 0.38f, 1f), // sand
	};

	public static BiomeSpec SpecFor(BiomeKind kind) => kind switch
	{
		BiomeKind.Plains => SpecPlains,
		BiomeKind.Forest => SpecForest,
		BiomeKind.Highland => SpecHighland,
		BiomeKind.Marsh => SpecMarsh,
		BiomeKind.Desert => SpecDesert,
		_ => SpecNone,
	};

	public static bool TryParseKind(string? raw, out BiomeKind kind)
	{
		kind = BiomeKind.None;
		if (string.IsNullOrWhiteSpace(raw))
			return false;
		if (Enum.TryParse(raw, ignoreCase: true, out BiomeKind parsed))
		{
			kind = parsed;
			return true;
		}
		if (byte.TryParse(raw, NumberStyles.Integer, CultureInfo.InvariantCulture, out var n)
			&& Enum.IsDefined(typeof(BiomeKind), n))
		{
			kind = (BiomeKind)n;
			return true;
		}
		return false;
	}

	/// <summary>
	/// Assign biome kinds to every editable vertex from a finished terrain pass.
	/// Climate dial biases Forest/Desert/Marsh; altitude bands force Highland.
	/// </summary>
	public static Dictionary<int, BiomeKind> Assign(
		GenTerrainService.PassResult pass,
		IReadOnlyList<Vector2>? vertexPositions = null)
	{
		var result = new Dictionary<int, BiomeKind>();
		if (pass == null)
			return result;

		var climate = pass.Dials.Climate;
		var wild = pass.Dials.Wildness;
		var seed = pass.Seed;

		foreach (var kv in pass.LandByVertex)
		{
			var v = kv.Key;
			if (!kv.Value)
			{
				result[v] = BiomeKind.None;
				continue;
			}

			pass.BandByVertex.TryGetValue(v, out var band);
			var pos = Vector2.Zero;
			if (vertexPositions != null && v >= 0 && v < vertexPositions.Count)
				pos = vertexPositions[v];

			var patch = Hash01(seed, v, pos);
			result[v] = ClassifyLand(band, climate, wild, patch);
		}

		return result;
	}

	public static BiomeKind ClassifyLand(
		GenTerrainService.AltitudeBand band,
		float climate,
		float wildness,
		float patch01)
	{
		if (band is GenTerrainService.AltitudeBand.Peak or GenTerrainService.AltitudeBand.Highland)
			return BiomeKind.Highland;

		if (band == GenTerrainService.AltitudeBand.Shelf)
		{
			// Wet shelf → Marsh when climate mid-high; else Plains fringe.
			if (climate >= 0.38f || patch01 < 0.35f + wildness * 0.2f)
				return BiomeKind.Marsh;
			return BiomeKind.Plains;
		}

		// Lowland (+ any residual land band): climate axis + wildness patches.
		if (climate <= 0.28f)
			return patch01 < 0.72f ? BiomeKind.Desert : BiomeKind.Plains;
		if (climate >= 0.62f)
			return patch01 < 0.78f + wildness * 0.1f ? BiomeKind.Forest : BiomeKind.Plains;

		// Mid climate — mix Plains with Forest/Marsh patches so ≥2 looks always appear.
		if (patch01 < 0.28f + wildness * 0.15f)
			return BiomeKind.Forest;
		if (patch01 > 0.82f - wildness * 0.08f)
			return BiomeKind.Marsh;
		return BiomeKind.Plains;
	}

	public static (int DistinctLand, Dictionary<BiomeKind, int> Counts) CountLand(
		IReadOnlyDictionary<int, BiomeKind> byVertex)
	{
		var counts = new Dictionary<BiomeKind, int>();
		foreach (var kv in byVertex)
		{
			if (kv.Value == BiomeKind.None)
				continue;
			counts.TryGetValue(kv.Value, out var n);
			counts[kv.Value] = n + 1;
		}
		return (counts.Count, counts);
	}

	public static string SummaryLine(
		IReadOnlyDictionary<int, BiomeKind> byVertex,
		WorldBoundsDials dials)
	{
		var (distinct, counts) = CountLand(byVertex);
		var parts = new List<string>();
		foreach (BiomeKind k in Enum.GetValues(typeof(BiomeKind)))
		{
			if (k == BiomeKind.None) continue;
			if (counts.TryGetValue(k, out var n) && n > 0)
				parts.Add($"{SpecFor(k).Name}={n}");
		}
		var list = parts.Count > 0 ? string.Join(",", parts) : "none";
		return $"GEN-biomes-r1 distinct={distinct} [{list}] climate={dials.Climate:0.##} wild={dials.Wildness:0.##}";
	}

	private static float Hash01(uint seed, int v, Vector2 pos)
	{
		unchecked
		{
			var h = seed ^ (uint)(v * 73856093) ^ (uint)((int)(pos.X * 12.9898f) * 19349663)
				^ (uint)((int)(pos.Y * 78.233f) * 83492791);
			h ^= h >> 13;
			h *= 1274126177u;
			h ^= h >> 16;
			return (h & 0xFFFFFFu) / 16777215f;
		}
	}
}
