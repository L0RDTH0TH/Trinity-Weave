using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace Genesis.Core.WorldGen;

/// <summary>
/// World-seed board (WORLD-s0-intents) — optional lore/seeds that may bias what the world is.
/// Off Create World critical path: empty Open is lawful; filled lines salt gen (propose-feed peer).
/// Do not expand into campaign/table prep or full intent graph.
/// </summary>
public sealed class WorldSession0IntentBoard
{
	public const string PackagingSliceId = "alpha0_world_s0_intents_packaging_r1";
	public const string PackagingAskId = "alpha0_world_s0_intents_packaging";
	public const string OptionalLoreSliceId = "alpha0_world_s0_optional_lore_r1";
	public const string OptionalLoreAskId = "alpha0_world_s0_optional_lore";
	public const string DmLoreHonestySliceId = "alpha0_world_s0_dm_lore_honesty_r1";
	public const string DmLoreHonestyAskId = "alpha0_world_s0_dm_lore_honesty";
	public const string PriorSoftKeepSliceId = "alpha0_world_s0_intents_r1";

	private readonly List<WorldSession0Intent> _intents;
	private readonly List<(WorldSession0Intent.AuthorSeat Seat, string Text)> _seedBank;
	private int _nextSeedIndex;
	private int _nextOrdinal;

	public IReadOnlyList<WorldSession0Intent> Intents => _intents;
	public int AcceptedCount => _intents.Count(i => i.IsAccepted);
	public int ProposedCount => _intents.Count(i => i.Status == WorldSession0Intent.Disposition.Proposed);
	/// <summary>Packaging law: seeds optional — Open never blocked by accepted count.</summary>
	public bool CanOpenWorld => true;
	public bool HasMoreSeeds => _nextSeedIndex < _seedBank.Count;
	/// <summary>0 when empty; non-zero when optional lore fills salt Create World Open gen.</summary>
	public uint LoreFeedSalt { get; }
	public bool LoreFed => LoreFeedSalt != 0;
	public string SummaryLine =>
		LoreFed
			? $"lore optional · accepted={AcceptedCount} salt=0x{LoreFeedSalt:x8} (salts gen when present)"
			: $"lore optional · empty (Open skip-ok · unread salt=0)";

	private WorldSession0IntentBoard(
		List<WorldSession0Intent> intents,
		List<(WorldSession0Intent.AuthorSeat Seat, string Text)> seedBank,
		int nextSeedIndex,
		int nextOrdinal,
		uint loreFeedSalt = 0)
	{
		_intents = intents;
		_seedBank = seedBank;
		_nextSeedIndex = nextSeedIndex;
		_nextOrdinal = nextOrdinal;
		LoreFeedSalt = loreFeedSalt;
	}

	public static WorldSession0IntentBoard Empty { get; } = new(
		new List<WorldSession0Intent>(),
		new List<(WorldSession0Intent.AuthorSeat, string)>(),
		0,
		0,
		0);

	/// <summary>
	/// Optional freeform lore capture — DM world seed (+ Shared as table/world note).
	/// Player freeform removed (PCs attach later via friends/sheets — parked).
	/// Never gates Open; filled texts become accepted seeds + <see cref="LoreFeedSalt"/>.
	/// </summary>
	public static WorldSession0IntentBoard FromOptionalLore(
		string? dmLore,
		string? sharedLore = null,
		string? scaffoldId = null)
	{
		var intents = new List<WorldSession0Intent>();
		var ordinal = 1;
		void Add(WorldSession0Intent.AuthorSeat seat, string? raw)
		{
			var text = (raw ?? string.Empty).Trim();
			if (text.Length == 0)
				return;
			var id = $"lore_{seat.ToString().ToLowerInvariant()}_{ordinal}_{HashSalt(text, scaffoldId):x4}";
			intents.Add(WorldSession0Intent.CreateAccepted(id, text, seat, ordinal++));
		}

		Add(WorldSession0Intent.AuthorSeat.Dm, dmLore);
		Add(WorldSession0Intent.AuthorSeat.Shared, sharedLore);
		var salt = HashLoreSalt(intents.Select(i => i.Text), scaffoldId);
		return new WorldSession0IntentBoard(
			intents,
			new List<(WorldSession0Intent.AuthorSeat, string)>(),
			0,
			ordinal,
			salt);
	}

	/// <summary>Mint a board with initial proposed seeds (legacy collaborative bank — not Create World critical path).</summary>
	public static WorldSession0IntentBoard SeedFor(string genBiasId, string? scaffoldId = null)
	{
		var bias = string.IsNullOrWhiteSpace(genBiasId) ? "medium" : genBiasId.Trim().ToLowerInvariant();
		var bank = BuildSeedBank(bias);
		var board = new WorldSession0IntentBoard(
			new List<WorldSession0Intent>(),
			bank,
			0,
			1);
		board.ProposeNextSeed(scaffoldId);
		board.ProposeNextSeed(scaffoldId);
		board.ProposeNextSeed(scaffoldId);
		return board;
	}

	public WorldSession0Intent? ProposeNextSeed(string? scaffoldId = null)
	{
		if (!HasMoreSeeds)
			return null;
		var (seat, text) = _seedBank[_nextSeedIndex++];
		var id = $"int_{seat.ToString().ToLowerInvariant()}_{_nextOrdinal}_{HashSalt(text, scaffoldId):x4}";
		var intent = WorldSession0Intent.CreateProposed(id, text, seat, _nextOrdinal++);
		_intents.Add(intent);
		return intent;
	}

	public bool Accept(string intentId)
	{
		for (var i = 0; i < _intents.Count; i++)
		{
			if (_intents[i].IntentId != intentId || !_intents[i].CanAccept)
				continue;
			_intents[i] = _intents[i].AsAccepted();
			return true;
		}
		return false;
	}

	public bool Reject(string intentId)
	{
		for (var i = 0; i < _intents.Count; i++)
		{
			if (_intents[i].IntentId != intentId || !_intents[i].CanAccept)
				continue;
			_intents[i] = _intents[i].AsRejected();
			return true;
		}
		return false;
	}

	public WorldSession0Intent? Get(string intentId) =>
		_intents.FirstOrDefault(i => i.IntentId == intentId);

	public IReadOnlyList<WorldSession0Intent> AcceptedOnly() =>
		_intents.Where(i => i.IsAccepted).ToList();

	public string PreviewBody()
	{
		var sb = new StringBuilder();
		sb.AppendLine("Optional DM world lore / seeds — bias what the world is when present.");
		sb.AppendLine("Skip-ok: leave blank and Open still works. Filled DM/Shared salt Create World Open gen.");
		sb.AppendLine("Player chars attach later from friends/sheets (not typed here). No Accept≥1 gate.");
		sb.AppendLine();
		sb.AppendLine(SummaryLine);
		sb.AppendLine();
		if (_intents.Count == 0)
		{
			sb.AppendLine("Empty — Open world is lawful. Example: \"DM we start in Magic France\".");
			return sb.ToString();
		}

		foreach (var intent in _intents)
			sb.AppendLine($"· {intent.CardLine()}");

		sb.AppendLine();
		sb.Append(LoreFed
			? $"Open will salt gen (0x{LoreFeedSalt:x8}) like propose-feed."
			: "Open world allowed — seeds stay empty until you type.");
		return sb.ToString();
	}

	public Dictionary<string, object> ToLogFields()
	{
		var accepted = AcceptedOnly();
		return new Dictionary<string, object>
		{
			["intent_count"] = _intents.Count,
			["intent_accepted_count"] = AcceptedCount,
			["intent_proposed_count"] = ProposedCount,
			["intent_summary"] = SummaryLine,
			["intent_accepted_ids"] = string.Join(",", accepted.Select(i => i.IntentId)),
			["intent_accepted_texts"] = string.Join(" | ", accepted.Select(i => i.Text)),
			["lore_feed_salt"] = LoreFeedSalt,
			["lore_fed"] = LoreFed,
			["s0_optional_lore_slice"] = OptionalLoreSliceId,
			["s0_dm_lore_honesty_slice"] = DmLoreHonestySliceId,
			["s0_packaging_slice"] = PackagingSliceId,
		};
	}

	private static List<(WorldSession0Intent.AuthorSeat Seat, string Text)> BuildSeedBank(string bias)
	{
		var flavor = bias switch
		{
			"high" => "a brighter myth still unpaid",
			"low" => "a scarce wonder that costs dear",
			"grimdark" => "a scarred oath no one wants to name",
			_ => "an Exemplar-middle debt that waits",
		};
		return new List<(WorldSession0Intent.AuthorSeat, string)>
		{
			(WorldSession0Intent.AuthorSeat.Player,
				"A ruined lighthouse still guides smugglers at low tide."),
			(WorldSession0Intent.AuthorSeat.Dm,
				"A quiet war simmered before anyone named it."),
			(WorldSession0Intent.AuthorSeat.Shared,
				$"Something under the trade saddle remembers — {flavor}."),
			(WorldSession0Intent.AuthorSeat.Player,
				"Our table owes a debt to the river folk."),
			(WorldSession0Intent.AuthorSeat.Dm,
				"One settlement seal is forged; only the DM knows which."),
			(WorldSession0Intent.AuthorSeat.Shared,
				"A period of peace ends when the first road is painted."),
		};
	}

	private static int HashSalt(string text, string? scaffoldId)
	{
		unchecked
		{
			var h = 17;
			h = h * 31 + text.GetHashCode(StringComparison.Ordinal);
			h = h * 31 + (scaffoldId ?? "").GetHashCode(StringComparison.Ordinal);
			return h == int.MinValue ? 1 : Math.Abs(h);
		}
	}

	private static uint HashLoreSalt(IEnumerable<string> texts, string? scaffoldId)
	{
		unchecked
		{
			uint h = 2166136261u;
			var any = false;
			foreach (var t in texts)
			{
				if (string.IsNullOrWhiteSpace(t))
					continue;
				any = true;
				foreach (var c in t.Trim())
					h = (h ^ c) * 16777619u;
				h ^= 0x9E3779B9u;
			}

			if (!any)
				return 0;
			foreach (var c in scaffoldId ?? "")
				h = (h ^ c) * 16777619u;
			return h == 0 ? 1u : h;
		}
	}
}
