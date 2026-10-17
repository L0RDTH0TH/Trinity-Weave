using System;
using System.Collections.Generic;
using System.Globalization;
using System.Text;

namespace Genesis.Core.WorldGen;

/// <summary>
/// WORLD-propose scaffold card — readable proposal from bias + dials + revision.
/// Accept binds <see cref="GenFeedSalt"/> / axis biases into the Create World gen pass
/// (<c>alpha0_world_propose_feed_r1</c>). Menu-only Accept without gen effect = KEEP-debt.
/// Not GEN-* fill mesh by itself; feed salts the pass the board uses.
/// </summary>
public sealed class WorldScaffoldProposal
{
	public enum Disposition
	{
		Empty = 0,
		Proposed = 1,
		Rejected = 2,
		Accepted = 3,
	}

	public string ScaffoldId { get; }
	public int Revision { get; }
	public string GenBiasId { get; }
	public WorldBoundsDials Bounds { get; }
	public string RegionSketch { get; }
	public string SiteHint { get; }
	public string ClimateRead { get; }
	public string WildnessRead { get; }
	public string SummaryLine { get; }
	public Disposition Status { get; }
	public DateTimeOffset ProposedAtUtc { get; }

	/// <summary>Deterministic salt the gen pass must mix — changes on Propose again / Revise.</summary>
	public uint GenFeedSalt { get; }

	/// <summary>Coast vs inland axis (−1 coast-heavy … +1 inland) — shifts land threshold.</summary>
	public float CoastBias { get; }

	/// <summary>Ridge / highland axis (0 flat … 1 ridge) — shifts landform frequency.</summary>
	public float RidgeBias { get; }

	public string AxisPrimary { get; }
	public string AxisSecondary { get; }

	public bool CanAccept => Status == Disposition.Proposed;

	/// <summary>True when Accept (or accepted package bind) must feed Create World gen.</summary>
	public bool FeedsGenerator =>
		Status == Disposition.Accepted && GenFeedSalt != 0 && ScaffoldId != "(none)";

	private WorldScaffoldProposal(
		string scaffoldId,
		int revision,
		string genBiasId,
		WorldBoundsDials bounds,
		string regionSketch,
		string siteHint,
		string climateRead,
		string wildnessRead,
		string summaryLine,
		Disposition status,
		DateTimeOffset proposedAtUtc,
		uint genFeedSalt,
		float coastBias,
		float ridgeBias,
		string axisPrimary,
		string axisSecondary)
	{
		ScaffoldId = scaffoldId;
		Revision = revision;
		GenBiasId = genBiasId;
		Bounds = bounds;
		RegionSketch = regionSketch;
		SiteHint = siteHint;
		ClimateRead = climateRead;
		WildnessRead = wildnessRead;
		SummaryLine = summaryLine;
		Status = status;
		ProposedAtUtc = proposedAtUtc;
		GenFeedSalt = genFeedSalt;
		CoastBias = coastBias;
		RidgeBias = ridgeBias;
		AxisPrimary = axisPrimary;
		AxisSecondary = axisSecondary;
	}

	public static WorldScaffoldProposal Empty { get; } = new(
		scaffoldId: "(none)",
		revision: 0,
		genBiasId: "medium",
		bounds: WorldBoundsDials.Defaults,
		regionSketch: "No scaffold yet — Propose to mint a readable card.",
		siteHint: "—",
		climateRead: "—",
		wildnessRead: "—",
		summaryLine: "scaffold=none status=empty feed=0",
		status: Disposition.Empty,
		proposedAtUtc: DateTimeOffset.MinValue,
		genFeedSalt: 0,
		coastBias: 0f,
		ridgeBias: 0f,
		axisPrimary: "—",
		axisSecondary: "—");

	/// <summary>Tool proposes a new scaffold revision from bias + dials (deterministic salt).</summary>
	public static WorldScaffoldProposal Propose(
		string genBiasId,
		WorldBoundsDials dials,
		int revision,
		int reviseSalt = 0)
	{
		var rev = Math.Max(1, revision);
		var bias = string.IsNullOrWhiteSpace(genBiasId) ? "medium" : genBiasId.Trim().ToLowerInvariant();
		var seed = HashSeed(bias, dials, rev, reviseSalt);
		var rng = new Random(seed);

		var axes = new[]
		{
			"north coast shelf", "inland highland", "river fork basin",
			"windward ridge", "lee marsh belt", "trade saddle",
		};
		var ai = rng.Next(axes.Length);
		var bi = rng.Next(axes.Length);
		while (bi == ai)
			bi = rng.Next(axes.Length);
		var a = axes[ai];
		var b = axes[bi];

		// Structured feed biases so Accept/Revise change the gen pass (not meta-only).
		var coastBias = AxisCoastWeight(ai) * 0.55f + AxisCoastWeight(bi) * 0.45f;
		var ridgeBias = AxisRidgeWeight(ai) * 0.55f + AxisRidgeWeight(bi) * 0.45f;
		uint feed;
		unchecked
		{
			feed = (uint)seed;
			feed ^= (uint)(ai + 1) * 0x9E3779B9u;
			feed ^= (uint)(bi + 1) * 0x85EBCA6Bu;
			feed ^= (uint)rev << 7;
			feed ^= (uint)reviseSalt << 13;
			if (feed == 0) feed = 1u;
		}

		var settleBand = dials.SettlementDistance switch
		{
			< 0.3f => "tight cluster",
			< 0.6f => "spread holds",
			_ => "sparse outposts",
		};
		var siteCount = Math.Clamp(
			(int)Math.Round(3 + (1.0 - dials.SettlementDistance) * 6 + dials.Rivers * 2),
			2,
			12);
		var riverNote = dials.Rivers < 0.25f
			? "dry corridors"
			: dials.Rivers < 0.6f
				? "few named rivers"
				: "braided waterways";
		var climate = dials.Climate switch
		{
			< 0.33f => "cool / harsh seasons",
			< 0.66f => "temperate Exemplar middle",
			_ => "warm / generous seasons",
		};
		var wild = dials.Wildness switch
		{
			< 0.33f => "tamed edges",
			< 0.66f => "mixed wild belts",
			_ => "deep wild pressure",
		};
		var biasFlavor = bias switch
		{
			"high" => "brighter myth anchors",
			"low" => "scarce wonder nodes",
			"grimdark" => "scarred road pressure",
			_ => "Exemplar-shaped middle",
		};

		var stamp = DateTimeOffset.UtcNow;
		var scaffoldId = $"scf_{bias}_r{rev}_{seed:x8}";
		var region = $"{a} ↔ {b} · cell≈{Fmt(dials.CellSize)} · rings={dials.ToSeedRingCount()} · {riverNote}";
		var siteHint = $"{siteCount} site seats ({settleBand}) — records only, not placed";
		var summary =
			$"scaffold={scaffoldId} rev={rev} bias={bias} status=proposed feed=0x{feed:x8} · {settleBand} · {climate}";

		return new WorldScaffoldProposal(
			scaffoldId,
			rev,
			bias,
			dials,
			region,
			siteHint,
			climate + " · " + biasFlavor,
			wild,
			summary,
			Disposition.Proposed,
			stamp,
			feed,
			coastBias,
			ridgeBias,
			a,
			b);
	}

	public WorldScaffoldProposal AsRejected() =>
		new(
			ScaffoldId,
			Revision,
			GenBiasId,
			Bounds,
			RegionSketch,
			SiteHint,
			ClimateRead,
			WildnessRead,
			$"scaffold={ScaffoldId} rev={Revision} status=rejected feed=cleared",
			Disposition.Rejected,
			ProposedAtUtc,
			genFeedSalt: 0,
			coastBias: 0f,
			ridgeBias: 0f,
			AxisPrimary,
			AxisSecondary);

	public WorldScaffoldProposal AsAccepted() =>
		new(
			ScaffoldId,
			Revision,
			GenBiasId,
			Bounds,
			RegionSketch,
			SiteHint,
			ClimateRead,
			WildnessRead,
			$"scaffold={ScaffoldId} rev={Revision} status=accepted feed=0x{GenFeedSalt:x8}",
			Disposition.Accepted,
			ProposedAtUtc,
			GenFeedSalt == 0 ? 1u : GenFeedSalt,
			CoastBias,
			RidgeBias,
			AxisPrimary,
			AxisSecondary);

	public string PreviewBody()
	{
		var sb = new StringBuilder();
		sb.AppendLine($"Status: {Status.ToString().ToUpperInvariant()} · rev {Revision}");
		sb.AppendLine($"Id: {ScaffoldId}");
		sb.AppendLine($"Bias={GenBiasId} · Dials: {Bounds.SummaryLine()}");
		sb.AppendLine($"Gen feed salt: 0x{GenFeedSalt:x8} · coast={Fmt(CoastBias)} ridge={Fmt(RidgeBias)}");
		sb.AppendLine();
		sb.AppendLine($"Regions: {RegionSketch}");
		sb.AppendLine($"Sites: {SiteHint}");
		sb.AppendLine($"Climate: {ClimateRead}");
		sb.AppendLine($"Wildness: {WildnessRead}");
		sb.AppendLine();
		sb.Append(
			"Accept binds this scaffold into Create World Open gen (salt+axes change land/water). " +
			"Reject clears feed. Propose again / Revise mint a different salt — not one-shot menu chrome.");
		return sb.ToString();
	}

	public Dictionary<string, object> ToLogFields() => new()
	{
		["scaffold_id"] = ScaffoldId,
		["scaffold_revision"] = Revision,
		["scaffold_status"] = Status.ToString().ToLowerInvariant(),
		["scaffold_summary"] = SummaryLine,
		["scaffold_region"] = RegionSketch,
		["scaffold_sites"] = SiteHint,
		["scaffold_feed_salt"] = GenFeedSalt,
		["scaffold_coast_bias"] = CoastBias,
		["scaffold_ridge_bias"] = RidgeBias,
		["scaffold_feeds_generator"] = FeedsGenerator,
		["scaffold_axis_primary"] = AxisPrimary,
		["scaffold_axis_secondary"] = AxisSecondary,
		["gen_bias"] = GenBiasId,
	};

	private static float AxisCoastWeight(int axisIndex) => axisIndex switch
	{
		0 => -1f, // north coast shelf
		1 => 0.85f, // inland highland
		2 => -0.25f, // river fork basin
		3 => 0.55f, // windward ridge
		4 => -0.7f, // lee marsh belt
		5 => 0.2f, // trade saddle
		_ => 0f,
	};

	private static float AxisRidgeWeight(int axisIndex) => axisIndex switch
	{
		0 => 0.15f,
		1 => 0.95f,
		2 => 0.35f,
		3 => 1f,
		4 => 0.1f,
		5 => 0.45f,
		_ => 0.3f,
	};

	private static int HashSeed(string bias, WorldBoundsDials d, int rev, int salt)
	{
		unchecked
		{
			var h = 17;
			h = h * 31 + bias.GetHashCode(StringComparison.Ordinal);
			h = h * 31 + BitConverter.SingleToInt32Bits(d.CellSize);
			h = h * 31 + d.ToSeedRingCount();
			h = h * 31 + BitConverter.SingleToInt32Bits(d.SettlementDistance);
			h = h * 31 + BitConverter.SingleToInt32Bits(d.Rivers);
			h = h * 31 + BitConverter.SingleToInt32Bits(d.Climate);
			h = h * 31 + BitConverter.SingleToInt32Bits(d.Wildness);
			h = h * 31 + rev;
			h = h * 31 + salt;
			return h == int.MinValue ? 1 : Math.Abs(h);
		}
	}

	private static string Fmt(float v) =>
		v.ToString("0.##", CultureInfo.InvariantCulture);
}
