using System;
using System.Collections.Generic;
using System.Globalization;
using Godot;

namespace Genesis.Core.WorldGen;

/// <summary>
/// GEN-tone pass (<c>alpha0_gen_tone_r1</c>) over GEN-terrain-product r2 altitude feedstock.
/// Create World bias drives landform (sea / continent shape / relief / rivers) — not meta-only,
/// not salt-hash with the same silhouette. Same dials → same dials-derived seed; two biases →
/// visibly different board. Host applies via Create World auto-open or Key.T accel.
/// Cell size / cell count / rivers / climate / wildness still reshape (W2). Rivers dial 0 = no carve.
/// Nursery salt stubs stay parked. PACK / GEN-biomes unarmed.
/// </summary>
public static class GenTerrainService
{
	/// <summary>Readable altitude bands (Azgaar-style shelf → peak) for W3/W4 stranger test.</summary>
	public enum AltitudeBand : byte
	{
		DeepOcean = 0,
		Shelf = 1,
		Lowland = 2,
		Highland = 3,
		Peak = 4,
	}

	/// <summary>
	/// Bias landform profile — characteristic silhouette per Create World tone.
	/// Applied on top of dials; must change board even when dials-derived seed is held fixed.
	/// </summary>
	public readonly struct BiasLandform
	{
		public float SeaBase { get; init; }
		public float FreqScale { get; init; }
		public float AnisoX { get; init; }
		public float AnisoY { get; init; }
		public float DetailAmp { get; init; }
		public float ReliefAmp { get; init; }
		public float RiverWidthScale { get; init; }
		public float RunoffLo { get; init; }
		public float RunoffHi { get; init; }
		public float RimSoftness { get; init; }
		public float PeakBoost { get; init; }
		public float WarpAmp { get; init; }
		public float FragmentAmp { get; init; }
		public string Label { get; init; }

		public static BiasLandform For(WorldGenBias bias) => bias switch
		{
			// High Fantasy — brighter myth: more land, larger continents, gentler relief, clearer rivers.
			WorldGenBias.High => new BiasLandform
			{
				SeaBase = 0.30f,
				FreqScale = 0.78f,
				AnisoX = 1.05f,
				AnisoY = 0.92f,
				DetailAmp = 0.14f,
				ReliefAmp = 0.82f,
				RiverWidthScale = 1.28f,
				RunoffLo = -0.01f,
				RunoffHi = 0.48f,
				RimSoftness = 1.18f,
				PeakBoost = 0.06f,
				WarpAmp = 0.04f,
				FragmentAmp = 0.02f,
				Label = "high",
			},
			// Medium Fantasy — Exemplar middle road.
			WorldGenBias.Medium => new BiasLandform
			{
				SeaBase = 0.44f,
				FreqScale = 1.0f,
				AnisoX = 1.0f,
				AnisoY = 1.0f,
				DetailAmp = 0.22f,
				ReliefAmp = 1.0f,
				RiverWidthScale = 1.0f,
				RunoffLo = -0.02f,
				RunoffHi = 0.42f,
				RimSoftness = 1.0f,
				PeakBoost = 0f,
				WarpAmp = 0.08f,
				FragmentAmp = 0.06f,
				Label = "medium",
			},
			// Low Fantasy — scarce wonder / harder logistics: less land, flatter, thinner watercourses.
			WorldGenBias.Low => new BiasLandform
			{
				SeaBase = 0.58f,
				FreqScale = 1.12f,
				AnisoX = 0.88f,
				AnisoY = 1.14f,
				DetailAmp = 0.18f,
				ReliefAmp = 0.62f,
				RiverWidthScale = 0.72f,
				RunoffLo = 0.02f,
				RunoffHi = 0.32f,
				RimSoftness = 0.88f,
				PeakBoost = -0.04f,
				WarpAmp = 0.05f,
				FragmentAmp = 0.04f,
				Label = "low",
			},
			// Grimdark — costly hope / scarred coasts: more water shelf, broken land, harsh relief, scour rivers.
			WorldGenBias.Grimdark => new BiasLandform
			{
				SeaBase = 0.56f,
				FreqScale = 1.42f,
				AnisoX = 0.72f,
				AnisoY = 1.28f,
				DetailAmp = 0.38f,
				ReliefAmp = 1.45f,
				RiverWidthScale = 0.58f,
				RunoffLo = -0.04f,
				RunoffHi = 0.55f,
				RimSoftness = 0.72f,
				PeakBoost = 0.10f,
				WarpAmp = 0.16f,
				FragmentAmp = 0.18f,
				Label = "grimdark",
			},
			_ => For(WorldGenBias.Medium),
		};
	}

	public sealed class PassResult
	{
		public required uint Seed { get; init; }
		public required string GenBiasId { get; init; }
		public required WorldBoundsDials Dials { get; init; }
		public required uint ScaffoldFeedSalt { get; init; }
		public required bool ScaffoldFed { get; init; }
		public required uint LoreFeedSalt { get; init; }
		public required bool LoreFed { get; init; }
		public required float SeaLevel { get; init; }
		public required string BiasLandformLabel { get; init; }
		/// <summary>Logic vertex → land (true) or water/empty (false).</summary>
		public required Dictionary<int, bool> LandByVertex { get; init; }
		/// <summary>Logic vertex → relative height above sea (feeds craft-view altitude lift).</summary>
		public required Dictionary<int, float> HeightByVertex { get; init; }
		/// <summary>Logic vertex → absolute elevation field (pre–sea-level; downhill river source).</summary>
		public required Dictionary<int, float> ElevationByVertex { get; init; }
		/// <summary>Logic vertex → altitude band (DeepOcean…Peak).</summary>
		public required Dictionary<int, AltitudeBand> BandByVertex { get; init; }
		/// <summary>Logic vertex → river corridor (readable watercourse when dial &gt; 0).</summary>
		public required Dictionary<int, bool> RiverByVertex { get; init; }
		public required int LandCount { get; init; }
		public required int WaterCount { get; init; }
		public required int RiverCarveCount { get; init; }
		public required int EditableCount { get; init; }
		public required int PeakCount { get; init; }
		public required int HighlandCount { get; init; }
		public required string HeightContract { get; init; }
		public required string SummaryLine { get; init; }

		public Dictionary<string, object> ToLogFields()
		{
			var fields = new Dictionary<string, object>
			{
				["gen_seed"] = Seed,
				["gen_bias"] = GenBiasId,
				["bias_landform"] = BiasLandformLabel,
				["land_count"] = LandCount,
				["water_count"] = WaterCount,
				["river_carve_count"] = RiverCarveCount,
				["editable_count"] = EditableCount,
				["peak_count"] = PeakCount,
				["highland_count"] = HighlandCount,
				["sea_level"] = SeaLevel,
				["land_share"] = EditableCount > 0 ? (float)LandCount / EditableCount : 0f,
				["height_contract"] = HeightContract,
				["gen_summary"] = SummaryLine,
				["dial_cell_affects_pass"] = true,
				["dial_cell_count_affects_rings"] = true,
				["altitude_bands"] = true,
				["bias_drives_landform"] = true,
				["same_dials_seed_bias_independent"] = true,
				["seed_rings"] = Dials.ToSeedRingCount(),
				["rivers_dial"] = Dials.Rivers,
				["scaffold_feed_salt"] = ScaffoldFeedSalt,
				["scaffold_fed"] = ScaffoldFed,
				["lore_feed_salt"] = LoreFeedSalt,
				["lore_fed"] = LoreFed,
			};
			foreach (var kv in GenToneContract.ToLogFields())
				fields["tone_" + kv.Key] = kv.Value;
			foreach (var kv in GenTerrainContract.ToLogFields())
				fields["terrain_" + kv.Key] = kv.Value;
			foreach (var kv in WorldProposeFeedContract.ToLogFields())
				fields["propose_feed_" + kv.Key] = kv.Value;
			foreach (var kv in Dials.ToLogFields())
				fields[kv.Key] = kv.Value;
			return fields;
		}
	}

	/// <summary>
	/// Compute terrain facts for editable dual-grid logic vertices. Does not mutate craft.
	/// Bias landform reshapes elevation / sea / rivers even when dials-derived seed is identical.
	/// When <paramref name="scaffold"/> FeedsGenerator, salt+axes change the pass (1c debt, parked).
	/// When <paramref name="loreFeedSalt"/> ≠ 0, optional s0 lore salts the seed (1d, parked).
	/// </summary>
	public static PassResult Compute(
		IReadOnlyList<Vector2> vertexPositions,
		IEnumerable<int> editableLogicPoints,
		WorldGenBias bias,
		WorldBoundsDials dials,
		uint? seed = null,
		WorldScaffoldProposal? scaffold = null,
		uint loreFeedSalt = 0)
	{
		var biasId = WorldPackage.ToBiasId(bias);
		var landform = BiasLandform.For(bias);
		var feed = scaffold != null && scaffold.FeedsGenerator ? scaffold : null;
		var feedSalt = feed?.GenFeedSalt ?? 0u;
		// GEN-tone: dials (+ parked scaffold/lore salts) derive seed — bias is NOT mixed in.
		// Same dials ⇒ same seed; BiasLandform alone must change the silhouette.
		var s = seed ?? DeriveSeed(dials, feedSalt, loreFeedSalt);
		var coastBias = feed?.CoastBias ?? 0f;
		var ridgeBias = feed?.RidgeBias ?? 0f;

		// W2: cell size → landform frequency (larger cell → coarser continents), then bias scale.
		var cell = Math.Max(0.45f, dials.CellSize);
		var baseFreq = (0.042f + dials.Wildness * 0.11f + Math.Abs(ridgeBias) * 0.04f)
			/ cell * landform.FreqScale;
		// Climate + bias landform → sea level (higher climate → lower sea → more land share).
		var seaLevel = SeaLevelForLandform(landform, dials.Climate, coastBias);
		var riversOn = dials.Rivers > 0f;
		// Corridor half-width on the river-ridge field; dial 0 → none (W5). Bias scales feel.
		var riverWidth = riversOn
			? (0.018f + dials.Rivers * 0.095f) * landform.RiverWidthScale
			: 0f;
		var riverFreq = (0.028f + dials.Wildness * 0.05f + Math.Abs(coastBias) * 0.018f)
			/ cell * (0.85f + landform.FreqScale * 0.15f);

		var land = new Dictionary<int, bool>();
		var height = new Dictionary<int, float>();
		var elevMap = new Dictionary<int, float>();
		var bands = new Dictionary<int, AltitudeBand>();
		var river = new Dictionary<int, bool>();
		var landN = 0;
		var waterN = 0;
		var riverN = 0;
		var editableN = 0;
		var peakN = 0;
		var highlandN = 0;

		foreach (var v in editableLogicPoints)
		{
			editableN++;
			var pos = v >= 0 && v < vertexPositions.Count ? vertexPositions[v] : Vector2.Zero;

			// Multi-octave continental heightfield — bias anisotropy / warp / fragment reshape mass.
			var elev = SampleElevation(pos, baseFreq, dials.Wildness, ridgeBias, s, landform);
			elevMap[v] = elev;

			var band = ClassifyBand(elev, seaLevel);
			bands[v] = band;
			if (band == AltitudeBand.Peak) peakN++;
			else if (band == AltitudeBand.Highland) highlandN++;

			// River ridge field — continuous corridors; only carve when dial > 0.
			var riverField = Fbm2D(pos.X * riverFreq + 41.7f, pos.Y * riverFreq - 13.2f, s ^ 0xBEEFu, octaves: 3);
			var onRiverRidge = riversOn && Math.Abs(riverField - 0.5f) < riverWidth;
			// Prefer downhill / coastal runoff; bias runoff band changes river feel.
			var runoffOk = elev >= seaLevel + landform.RunoffLo
				&& elev < seaLevel + landform.RunoffHi + dials.Wildness * 0.12f;
			var isRiver = onRiverRidge && runoffOk;

			var isLand = !isRiver && elev >= seaLevel;
			river[v] = isRiver;
			if (isRiver) riverN++;
			land[v] = isLand;
			if (isLand) landN++;
			else waterN++;

			// Relative height for craft Y lift (W4) — bias relief amp + peak boost.
			var rel = elev - seaLevel;
			var relief = landform.ReliefAmp;
			var h = isLand
				? rel * (1.55f + dials.Wildness * 1.25f) * relief + BandLift(band) + landform.PeakBoost
				: rel * 0.35f * relief - 0.22f;
			if (isRiver) h = Math.Min(h, -0.28f);
			height[v] = h;
		}

		var feedNote = feed != null
			? $" scaffold_feed=0x{feedSalt:x8} coast={coastBias:0.##} ridge={ridgeBias:0.##}"
			: " scaffold_feed=none";
		var loreNote = loreFeedSalt != 0
			? $" lore_feed=0x{loreFeedSalt:x8}"
			: " lore_feed=none";
		var landShare = editableN > 0 ? (float)landN / editableN : 0f;
		var summary =
			$"GEN-tone-r1 seed={s} bias={biasId} landform={landform.Label} sea={seaLevel:0.##} " +
			$"land={landN}({landShare:0%}) water={waterN} rivers={riverN} peak={peakN} high={highlandN} " +
			$"editable={editableN} · bias_landform · altitude_bands · height_reads · {dials.SummaryLine()}{feedNote}{loreNote}";

		return new PassResult
		{
			Seed = s,
			GenBiasId = biasId,
			Dials = dials,
			ScaffoldFeedSalt = feedSalt,
			ScaffoldFed = feed != null,
			LoreFeedSalt = loreFeedSalt,
			LoreFed = loreFeedSalt != 0,
			SeaLevel = seaLevel,
			BiasLandformLabel = landform.Label,
			LandByVertex = land,
			HeightByVertex = height,
			ElevationByVertex = elevMap,
			BandByVertex = bands,
			RiverByVertex = river,
			LandCount = landN,
			WaterCount = waterN,
			RiverCarveCount = riverN,
			EditableCount = editableN,
			PeakCount = peakN,
			HighlandCount = highlandN,
			HeightContract = GenTerrainContract.HeightReadsInCraftLaw,
			SummaryLine = summary,
		};
	}

	/// <summary>
	/// Downhill river polish along mesh edges — sources at highlands/peaks flow to shelf/ocean.
	/// Call from host after <see cref="Compute"/> when rivers dial &gt; 0; dial 0 leaves pass unchanged.
	/// </summary>
	public static void CarveDownhillRivers(
		PassResult pass,
		IReadOnlyDictionary<int, List<int>> adjacency,
		float riversDial)
	{
		if (pass == null || adjacency == null || riversDial <= 0f)
			return;

		var elev = pass.ElevationByVertex;
		var land = pass.LandByVertex;
		var river = pass.RiverByVertex;
		var height = pass.HeightByVertex;
		var bands = pass.BandByVertex;
		var sea = pass.SeaLevel;

		// Rank land vertices by elevation; source count scales with rivers dial.
		var candidates = new List<(int V, float E)>();
		foreach (var kv in elev)
		{
			if (!land.TryGetValue(kv.Key, out var isLand) || !isLand) continue;
			if (!bands.TryGetValue(kv.Key, out var band)) continue;
			if (band is not (AltitudeBand.Highland or AltitudeBand.Peak or AltitudeBand.Lowland))
				continue;
			if (kv.Value < sea + 0.08f) continue;
			candidates.Add((kv.Key, kv.Value));
		}
		candidates.Sort((a, b) => b.E.CompareTo(a.E));
		var sourceBudget = Math.Clamp(
			(int)Math.Round(2 + riversDial * 10f + pass.EditableCount * 0.012f * riversDial),
			0,
			Math.Min(28, candidates.Count));
		if (sourceBudget <= 0) return;

		var carved = 0;
		var used = new HashSet<int>();
		for (var i = 0; i < candidates.Count && carved < sourceBudget; i++)
		{
			var src = candidates[i].V;
			if (!used.Add(src)) continue;
			var path = new List<int> { src };
			var cur = src;
			var steps = 0;
			var maxSteps = 18 + (int)(riversDial * 22f);
			while (steps++ < maxSteps)
			{
				if (!adjacency.TryGetValue(cur, out var nbrs) || nbrs.Count == 0)
					break;
				var best = -1;
				var bestE = elev.TryGetValue(cur, out var ce) ? ce : 0f;
				foreach (var n in nbrs)
				{
					if (!elev.TryGetValue(n, out var ne)) continue;
					if (ne < bestE - 0.0005f)
					{
						bestE = ne;
						best = n;
					}
				}
				if (best < 0) break;
				path.Add(best);
				cur = best;
				// Stop once we hit shelf/ocean or an existing river corridor.
				if (elev.TryGetValue(cur, out var eCur) && eCur < sea + 0.02f)
					break;
				if (river.TryGetValue(cur, out var already) && already)
					break;
			}

			if (path.Count < 3) continue;
			foreach (var v in path)
			{
				river[v] = true;
				land[v] = false;
				height[v] = Math.Min(height.TryGetValue(v, out var hv) ? hv : -0.28f, -0.28f);
				if (bands.ContainsKey(v))
					bands[v] = elev.TryGetValue(v, out var ev) && ev >= sea
						? AltitudeBand.Shelf
						: AltitudeBand.DeepOcean;
				used.Add(v);
			}
			carved++;
		}
		// Dictionaries mutated in place; host recounts river vertices after polish.
	}

	private static float SampleElevation(
		Vector2 pos,
		float baseFreq,
		float wildness,
		float ridgeBias,
		uint seed,
		BiasLandform landform)
	{
		// Bias anisotropy stretches the continent mass so High vs Grimdark silhouettes differ.
		var px = pos.X * landform.AnisoX;
		var py = pos.Y * landform.AnisoY;
		var n1 = Fbm2D(px * baseFreq, py * baseFreq, seed, octaves: 4);
		var n2 = Fbm2D(px * baseFreq * 2.3f + 17.3f, py * baseFreq * 2.3f - 9.1f, seed ^ 0xA5A5u, octaves: 3);
		var warp = Fbm2D(px * baseFreq * 0.55f - 3.1f, py * baseFreq * 0.55f + 8.7f, seed ^ 0xC0DEu, octaves: 2);
		// Broad continent mass + detail relief; bias DetailAmp / FragmentAmp control breakup.
		var detail = landform.DetailAmp + wildness * 0.28f;
		detail = Math.Clamp(detail, 0.08f, 0.62f);
		var continent = n1 * (1f - detail) + n2 * detail;
		continent += (warp - 0.5f) * landform.WarpAmp;
		// Fragment noise carves extra water bites into landmass (Grimdark high, High low).
		if (landform.FragmentAmp > 0.001f)
		{
			var frag = Fbm2D(px * baseFreq * 3.7f + 5.5f, py * baseFreq * 3.7f - 2.2f, seed ^ 0xF00Du, octaves: 2);
			continent -= (frag - 0.35f) * landform.FragmentAmp;
		}
		// Soft radial falloff keeps coasts readable on finite boards (Azgaar map-edge feel, crude).
		var radial = MathF.Sqrt(pos.X * pos.X + pos.Y * pos.Y);
		var boardR = 420f;
		var rim = Math.Clamp(
			1f - radial / (boardR * (0.85f + wildness * 0.25f) * landform.RimSoftness),
			0f,
			1f);
		rim = rim * rim * (3f - 2f * rim);
		var elev = continent * 0.78f + rim * 0.22f;
		elev += ridgeBias * 0.06f * (n2 - 0.5f);
		elev += landform.PeakBoost * 0.15f * (n1 - 0.5f);
		return Math.Clamp(elev, 0f, 1f);
	}

	private static float SeaLevelForLandform(BiasLandform landform, float climate, float coastBias)
	{
		var baseSea = landform.SeaBase;
		// Climate dial: higher → lower sea → more land share (readable land %).
		var sea = baseSea - (climate - 0.5f) * 0.20f;
		// Coast-heavy scaffold → slightly higher sea (more water shelf).
		sea += coastBias * 0.07f;
		return Math.Clamp(sea, 0.18f, 0.72f);
	}

	private static AltitudeBand ClassifyBand(float elev, float seaLevel)
	{
		if (elev < seaLevel - 0.14f) return AltitudeBand.DeepOcean;
		if (elev < seaLevel) return AltitudeBand.Shelf;
		if (elev < seaLevel + 0.16f) return AltitudeBand.Lowland;
		if (elev < seaLevel + 0.34f) return AltitudeBand.Highland;
		return AltitudeBand.Peak;
	}

	private static float BandLift(AltitudeBand band) => band switch
	{
		AltitudeBand.Lowland => 0.12f,
		AltitudeBand.Highland => 0.28f,
		AltitudeBand.Peak => 0.48f,
		_ => 0f,
	};

	/// <summary>
	/// Dials + parked scaffold/lore salts only. Bias is NOT hashed — GEN-tone same-seed law.
	/// </summary>
	private static uint DeriveSeed(
		WorldBoundsDials dials,
		uint scaffoldFeedSalt = 0,
		uint loreFeedSalt = 0)
	{
		unchecked
		{
			uint h = 2166136261u;
			h ^= (uint)(dials.CellSize * 5000f);
			h ^= (uint)(dials.ToSeedRingCount() * 7919);
			h ^= (uint)(dials.Rivers * 1000f) << 2;
			h ^= (uint)(dials.Climate * 2000f) << 5;
			h ^= (uint)(dials.Wildness * 3000f) << 8;
			h ^= (uint)(dials.SettlementDistance * 4000f) << 11;
			// WORLD-propose feed: Accept / Revise must change seed (menu-only barred) — parked nursery.
			if (scaffoldFeedSalt != 0)
				h ^= scaffoldFeedSalt * 0x27D4EB2Du;
			// WORLD-s0 optional lore: filled lines salt seed; empty = no-op (skip-ok) — parked nursery.
			if (loreFeedSalt != 0)
				h ^= loreFeedSalt * 0x85EBCA6Bu;
			// GEN-tone r1 deepen salt so prior r2 boards are not bit-identical after bias landform.
			h ^= 0x71A0E3C5u;
			return h == 0 ? 1u : h;
		}
	}

	private static float Fbm2D(float x, float y, uint seed, int octaves)
	{
		var sum = 0f;
		var amp = 0.5f;
		var freq = 1f;
		var norm = 0f;
		for (var i = 0; i < octaves; i++)
		{
			sum += ValueNoise2D(x * freq, y * freq, seed + (uint)(i * 97)) * amp;
			norm += amp;
			amp *= 0.5f;
			freq *= 2.03f;
		}
		return norm > 0f ? sum / norm : 0f;
	}

	/// <summary>Cheap value noise — natural-gen starter; not full erosion stack.</summary>
	private static float ValueNoise2D(float x, float y, uint seed)
	{
		var x0 = (int)Math.Floor(x);
		var y0 = (int)Math.Floor(y);
		var fx = x - x0;
		var fy = y - y0;
		fx = fx * fx * (3f - 2f * fx);
		fy = fy * fy * (3f - 2f * fy);
		var a = Hash01(x0, y0, seed);
		var b = Hash01(x0 + 1, y0, seed);
		var c = Hash01(x0, y0 + 1, seed);
		var d = Hash01(x0 + 1, y0 + 1, seed);
		var u = Lerp(a, b, fx);
		var v = Lerp(c, d, fx);
		return Lerp(u, v, fy);
	}

	private static float Hash01(int x, int y, uint seed)
	{
		unchecked
		{
			uint n = seed;
			n ^= (uint)(x * 374761393);
			n ^= (uint)(y * 668265263);
			n = (n ^ (n >> 13)) * 1274126177u;
			n ^= n >> 16;
			return (n & 0xFFFFu) / 65535f;
		}
	}

	private static float Lerp(float a, float b, float t) => a + (b - a) * t;

	public static string FormatHeightSample(IReadOnlyDictionary<int, float> heights, int maxSamples = 3)
	{
		if (heights == null || heights.Count == 0) return "(none)";
		var parts = new List<string>(maxSamples);
		var n = 0;
		foreach (var kv in heights)
		{
			parts.Add($"v{kv.Key}={kv.Value.ToString("0.##", CultureInfo.InvariantCulture)}");
			if (++n >= maxSamples) break;
		}
		return string.Join(",", parts);
	}
}
