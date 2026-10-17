using System.Collections.Generic;

namespace Genesis.Core.WorldGen;

/// <summary>
/// WORLD-parity law (<c>alpha0_world_parity_r1</c> / series 1g).
/// Full procedural and full manual craft are first-class peers (feedstock).
/// Procedural lane = Create World propose/scaffold path (not GEN-fill Done).
/// Manual lane = Enter Craft dual-grid brush (not Townscaper product Done).
/// Enter Craft (manual) = empty amber (1g KEEP). Create World Open auto-gen is GEN-terrain-product
/// law (not 1g undo) — procedural peer still first-class.
/// Empty campaigns remain lawful (1f KEEP). No campaign attach on create.
/// </summary>
public static class WorldParityContract
{
	public const string SliceId = "alpha0_world_parity_r1";
	public const string AskId = "alpha0_world_parity";
	public const string TicketMap = "WORLD-parity";
	public const string PriorKeepSliceId = "alpha0_world_empty_campaigns_r1";
	public const string PriorKeepAskId = "alpha0_world_empty_campaigns";

	/// <summary>Procedural and manual authorship are peers — neither demoted.</summary>
	public const string PeerLaw = "procedural_manual_craft_peers";

	/// <summary>Create World / propose scaffold lane (GEN-terrain-product auto-gen on Open).</summary>
	public const string ProceduralLaneCode = "procedural_peer_create_world_propose";

	/// <summary>Enter Craft / dual-grid brush lane (empty amber 1g KEEP; not Townscaper Done).</summary>
	public const string ManualLaneCode = "manual_peer_enter_craft_brush";

	/// <summary>Enter Craft opens empty amber — 1g KEEP on manual lane only.</summary>
	public const string EmptyCraftEnterLaw = "enter_craft_empty_amber_manual_lane_only";

	/// <summary>Refuse selling GEN-fill or Townscaper Done as this ticket's Success.</summary>
	public const string GenFillBarredCode = "gen_fill_not_parity_success";
	public const string TownscaperDoneBarredCode = "townscaper_done_not_parity_success";
	public const string GenFillAsCraftEnterBarredCode = "gen_fill_not_craft_enter_success";

	public const string SummaryLine =
		"procedural ↔ manual craft peers · Enter Craft empty · Create World Open = GEN product · not Townscaper Done";

	public static Dictionary<string, object> ToLogFields() => new()
	{
		["ask_id"] = AskId,
		["slice_id"] = SliceId,
		["ticket_map"] = TicketMap,
		["prior_keep_slice"] = PriorKeepSliceId,
		["authorship_parity"] = PeerLaw,
		["procedural_lane"] = ProceduralLaneCode,
		["manual_lane"] = ManualLaneCode,
		["craft_enter_empty"] = EmptyCraftEnterLaw,
		["gen_fill_as_parity"] = GenFillBarredCode,
		["gen_fill_as_craft_enter"] = GenFillAsCraftEnterBarredCode,
		["townscaper_done_as_parity"] = TownscaperDoneBarredCode,
		["summary"] = SummaryLine,
	};
}
