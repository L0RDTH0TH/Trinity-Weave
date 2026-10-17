using System;
using System.Collections.Generic;

namespace Genesis.Core.WorldGen;

/// <summary>
/// Session-0 world package (1a–1g KEEP + active GEN-biomes / <c>alpha0_gen_biomes_r1</c>).
/// Durable identity + gen bias + dials + scaffold + accepted Session 0 intents + lawful empty campaigns.
/// Procedural (Create World) and manual (Enter Craft) remain peer authorship lanes (1g KEEP).
/// Craft enter stays empty; Create World Open auto-gens from bias landform + dials + biomes (no Generate button).
/// PACK persists bias/dials/gen board/biomes so quit→reload restores the same world (not blank amber).
/// Prior PACK-save-load + GEN-tone BiasLandform + terrain-product r2 feedstock. Campaigns attach later.
/// Nursery salt stubs stay parked. 1e import stays parked. GEN-sites unarmed.
/// </summary>
public sealed class WorldPackage
{
	public const string SliceId = GenBiomesContract.SliceId;
	public const string AskId = GenBiomesContract.AskId;
	public const string TicketMap = GenBiomesContract.TicketMap;
	public const string PriorKeepSliceId = GenTerrainContract.PriorWorldSliceId;
	public const string PriorKeepAskId = GenTerrainContract.PriorWorldAskId;
	public const int SchemaVersion = 11;

	public string WorldId { get; }
	public string DisplayName { get; }
	public WorldGenBias GenBias { get; }
	public string GenBiasId { get; }
	public WorldBoundsDials Bounds { get; }
	public WorldScaffoldProposal Scaffold { get; }
	public WorldSession0IntentBoard Intents { get; }
	public IReadOnlyList<string> CampaignIds { get; }
	public DateTimeOffset OpenedAtUtc { get; }
	public string WeldSliceId => SliceId;

	public bool CampaignsEmpty => CampaignIds.Count == 0;
	public string CampaignOwnership => WorldEmptyCampaignsContract.OwnershipLaw;
	public string AuthorshipParity => WorldParityContract.PeerLaw;

	private WorldPackage(
		string worldId,
		string displayName,
		WorldGenBias genBias,
		string genBiasId,
		WorldBoundsDials bounds,
		WorldScaffoldProposal scaffold,
		WorldSession0IntentBoard intents,
		DateTimeOffset openedAtUtc)
	{
		WorldId = worldId;
		DisplayName = displayName;
		GenBias = genBias;
		GenBiasId = genBiasId;
		Bounds = bounds;
		Scaffold = scaffold;
		Intents = intents;
		CampaignIds = Array.Empty<string>();
		OpenedAtUtc = openedAtUtc;
	}

	/// <summary>DM opens a new world after accepting scaffold + ≥1 Session 0 intent; campaigns empty (lawful).</summary>
	public static WorldPackage OpenNew(
		WorldGenBias bias,
		WorldBoundsDials? bounds = null,
		WorldScaffoldProposal? scaffold = null,
		WorldSession0IntentBoard? intents = null,
		string? displayName = null)
	{
		var biasId = ToBiasId(bias);
		var dials = bounds ?? WorldBoundsDials.Defaults;
		var scf = scaffold?.Status == WorldScaffoldProposal.Disposition.Accepted
			? scaffold
			: (scaffold?.CanAccept == true ? scaffold.AsAccepted() : WorldScaffoldProposal.Empty);
		var board = intents ?? WorldSession0IntentBoard.Empty;
		var stamp = DateTimeOffset.UtcNow;
		var worldId = $"world_{biasId}_{stamp:yyyyMMddHHmmss}";
		var name = string.IsNullOrWhiteSpace(displayName)
			? $"New world · {biasId}"
			: displayName.Trim();
		return new WorldPackage(worldId, name, bias, biasId, dials, scf, board, stamp);
	}

	/// <summary>Rehydrate a previously persisted pack (PACK-save-load) without minting a new world id.</summary>
	public static WorldPackage FromPersisted(
		string worldId,
		string displayName,
		WorldGenBias bias,
		WorldBoundsDials bounds,
		DateTimeOffset openedAtUtc,
		WorldScaffoldProposal? scaffold = null,
		WorldSession0IntentBoard? intents = null)
	{
		var biasId = ToBiasId(bias);
		var id = string.IsNullOrWhiteSpace(worldId)
			? $"world_{biasId}_reloaded"
			: worldId.Trim();
		var name = string.IsNullOrWhiteSpace(displayName)
			? $"Reloaded · {biasId}"
			: displayName.Trim();
		return new WorldPackage(
			id,
			name,
			bias,
			biasId,
			bounds,
			scaffold ?? WorldScaffoldProposal.Empty,
			intents ?? WorldSession0IntentBoard.Empty,
			openedAtUtc == default ? DateTimeOffset.UtcNow : openedAtUtc);
	}

	public static WorldGenBias ParseBiasId(string? id)
	{
		if (string.IsNullOrWhiteSpace(id))
			return WorldGenBias.Medium;
		return id.Trim().ToLowerInvariant() switch
		{
			"high" or "high_fantasy" => WorldGenBias.High,
			"medium" or "medium_fantasy" => WorldGenBias.Medium,
			"low" or "low_fantasy" => WorldGenBias.Low,
			"grimdark" => WorldGenBias.Grimdark,
			_ => WorldGenBias.Medium,
		};
	}

	public static string ToBiasId(WorldGenBias bias) => bias switch
	{
		WorldGenBias.High => "high",
		WorldGenBias.Medium => "medium",
		WorldGenBias.Low => "low",
		WorldGenBias.Grimdark => "grimdark",
		_ => "medium",
	};

	public Dictionary<string, object> ToLogFields()
	{
		var fields = new Dictionary<string, object>
		{
			["ask_id"] = AskId,
			["slice_id"] = SliceId,
			["ticket_map"] = TicketMap,
			["prior_keep_slice"] = PriorKeepSliceId,
			["world_id"] = WorldId,
			["display_name"] = DisplayName,
			["gen_bias"] = GenBiasId,
			["schema_version"] = SchemaVersion,
			["opened_at_utc"] = OpenedAtUtc.ToString("O"),
			["tone_profile_bind"] = "deferred_campaign_may_override",
			["authorship_parity"] = AuthorshipParity,
			["gen_terrain_explicit"] = GenTerrainContract.ExplicitInvokeLaw,
		};
		foreach (var kv in GenTerrainContract.ToLogFields())
			fields[kv.Key] = kv.Value;
		foreach (var kv in WorldParityContract.ToLogFields())
			fields["parity_" + kv.Key] = kv.Value;
		foreach (var kv in WorldEmptyCampaignsContract.ToLogFields(CampaignIds.Count))
			fields[kv.Key] = kv.Value;
		foreach (var kv in Bounds.ToLogFields())
			fields[kv.Key] = kv.Value;
		foreach (var kv in Scaffold.ToLogFields())
			fields[kv.Key] = kv.Value;
		foreach (var kv in Intents.ToLogFields())
			fields[kv.Key] = kv.Value;
		return fields;
	}
}
