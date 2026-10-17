using System;
using System.Collections.Generic;
using System.Globalization;

namespace Genesis.Core.WorldGen;

/// <summary>
/// World-create dials (WORLD-bounds / GEN-terrain-product W2).
/// Cell size → landform frequency. Cell count → seed ring / board cell budget
/// (Create World Open remeshes before ApplyGenTerrainPass). Settlement distance
/// remains package feedstock for later sites.
/// </summary>
public sealed class WorldBoundsDials
{
	public const float CellSizeMin = 0.5f;
	public const float CellSizeMax = 3.0f;
	/// <summary>Seed-ring budget — low vs high must change board cell totals in craft (F5).</summary>
	public const float CellCountMin = 2f;
	public const float CellCountMax = 8f;
	public const float SettlementMin = 0.1f;
	public const float SettlementMax = 1.0f;
	public const float RiversMin = 0.0f;
	public const float RiversMax = 1.0f;
	public const float ClimateMin = 0.0f;
	public const float ClimateMax = 1.0f;
	public const float WildnessMin = 0.0f;
	public const float WildnessMax = 1.0f;

	public float CellSize { get; }
	/// <summary>Seed-ring count (2–8). Sister to <see cref="CellSize"/> — extent, not frequency.</summary>
	public float CellCount { get; }
	public float SettlementDistance { get; }
	public float Rivers { get; }
	public float Climate { get; }
	public float Wildness { get; }

	public WorldBoundsDials(
		float cellSize,
		float cellCount,
		float settlementDistance,
		float rivers,
		float climate,
		float wildness)
	{
		CellSize = Clamp(cellSize, CellSizeMin, CellSizeMax);
		CellCount = Clamp(cellCount, CellCountMin, CellCountMax);
		SettlementDistance = Clamp(settlementDistance, SettlementMin, SettlementMax);
		Rivers = Clamp(rivers, RiversMin, RiversMax);
		Climate = Clamp(climate, ClimateMin, ClimateMax);
		Wildness = Clamp(wildness, WildnessMin, WildnessMax);
	}

	public static WorldBoundsDials Defaults { get; } = new(
		cellSize: 1.0f,
		cellCount: StalbergQuadKernel.DefaultRingCount,
		settlementDistance: 0.45f,
		rivers: 0.4f,
		climate: 0.5f,
		wildness: 0.35f);

	/// <summary>Integer seed rings for Stålberg remesh — higher → more cells / larger footprint.</summary>
	public int ToSeedRingCount() =>
		(int)Math.Clamp(Math.Round(CellCount), CellCountMin, CellCountMax);

	public WorldBoundsDials With(
		float? cellSize = null,
		float? cellCount = null,
		float? settlementDistance = null,
		float? rivers = null,
		float? climate = null,
		float? wildness = null) =>
		new(
			cellSize ?? CellSize,
			cellCount ?? CellCount,
			settlementDistance ?? SettlementDistance,
			rivers ?? Rivers,
			climate ?? Climate,
			wildness ?? Wildness);

	public string SummaryLine() =>
		$"cell={Fmt(CellSize)} count={ToSeedRingCount()} settle={Fmt(SettlementDistance)} rivers={Fmt(Rivers)} climate={Fmt(Climate)} wild={Fmt(Wildness)}";

	public Dictionary<string, object> ToLogFields() => new()
	{
		["dial_cell_size"] = CellSize,
		["dial_cell_count"] = CellCount,
		["dial_seed_rings"] = ToSeedRingCount(),
		["dial_settlement_distance"] = SettlementDistance,
		["dial_rivers"] = Rivers,
		["dial_climate"] = Climate,
		["dial_wildness"] = Wildness,
		["dials_summary"] = SummaryLine(),
	};

	private static float Clamp(float v, float min, float max) =>
		Math.Clamp(v, min, max);

	private static string Fmt(float v) =>
		v.ToString("0.##", CultureInfo.InvariantCulture);
}
