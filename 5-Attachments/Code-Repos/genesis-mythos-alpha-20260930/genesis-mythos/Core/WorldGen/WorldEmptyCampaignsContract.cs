using System.Collections.Generic;

namespace Genesis.Core.WorldGen;

/// <summary>
/// WORLD-empty-campaigns law (<c>alpha0_world_empty_campaigns_r1</c> / series 1f KEEP).
/// A saved world may lawfully contain zero campaigns. Campaigns attach later as guests;
/// they do not own the world. Not campaign-attach Done; not ToneProfile campaign bind.
/// Active Prefer after KEEP close advances to WORLD-parity (1g); this contract stays binding.
/// </summary>
public static class WorldEmptyCampaignsContract
{
	public const string SliceId = "alpha0_world_empty_campaigns_r1";
	public const string AskId = "alpha0_world_empty_campaigns";
	public const string TicketMap = "WORLD-empty-campaigns";
	public const string PriorKeepSliceId = "alpha0_world_import_r1";
	public const string PriorKeepAskId = "alpha0_world_import";

	/// <summary>World package owns itself; campaigns are later guests.</summary>
	public const string OwnershipLaw = "world_owns_self_campaigns_guest";

	/// <summary>Zero campaigns is a lawful success state, not a missing feature.</summary>
	public const string EmptyLawfulCode = "campaigns_empty_lawful";

	/// <summary>Attach is deferred — not part of world-create Success.</summary>
	public const string AttachDeferredCode = "campaign_attach_deferred";

	public const string SummaryLine =
		"campaigns=0 · attach later · world owns itself (campaigns are guests)";

	public static Dictionary<string, object> ToLogFields(int campaignCount = 0) => new()
	{
		["ask_id"] = AskId,
		["slice_id"] = SliceId,
		["ticket_map"] = TicketMap,
		["prior_keep_slice"] = PriorKeepSliceId,
		["campaign_count"] = campaignCount,
		["campaigns_empty"] = campaignCount == 0,
		["campaigns_empty_lawful"] = true,
		["campaign_ownership"] = OwnershipLaw,
		["campaign_attach"] = AttachDeferredCode,
		["empty_lawful_code"] = EmptyLawfulCode,
		["summary"] = SummaryLine,
	};
}
