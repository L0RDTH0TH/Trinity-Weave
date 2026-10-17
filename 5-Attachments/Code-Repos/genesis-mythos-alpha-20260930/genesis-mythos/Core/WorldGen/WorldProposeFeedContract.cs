using System.Collections.Generic;

namespace Genesis.Core.WorldGen;

/// <summary>
/// WORLD-propose debt residual (<c>alpha0_world_propose_feed_r1</c>).
/// Prior <c>alpha0_world_propose_r1</c> KEEP was menu-only (KEEP-debt) — Accept must feed
/// the generator or the board. Menu chrome ≠ Success. Not GEN-tone / GEN-biomes / PACK.
/// Staging until operator F5. Do not KEEP. Do not arm forward MAP.
/// </summary>
public static class WorldProposeFeedContract
{
	public const string SliceId = "alpha0_world_propose_feed_r1";
	public const string AskId = "alpha0_world_propose_feed";
	public const string TicketMap = "WORLD-propose";
	public const string SeriesId = "alpha0_world_builder_r1";
	public const string SeriesStep = "1c_propose_feed";
	public const string PriorMenuOnlySliceId = "alpha0_world_propose_r1";
	public const string PriorMenuOnlyDisposition = "KEEP-debt_menu_only_superseded_by_propose_feed";

	public const string SuccessObject = "scaffold_accept_feeds_gen_pass";
	public const string ContractId = "C_world_propose_feed_w1_w3";

	public const string AcceptFeedsGenLaw = "accept_binds_scaffold_feed_salt_into_gen_pass";
	public const string ReviseChangesGenLaw = "propose_again_or_revise_changes_gen_feed_salt";
	public const string RejectClearsFeedLaw = "reject_clears_scaffold_feed_until_new_propose";

	public const string MenuOnlyBarred = "menu_only_propose_as_success";
	public const string MetaWithoutGenBarred = "scaffold_meta_without_gen_effect";
	public const string HotkeyAsProductUxBarred = "hotkey_as_product_ux";
	public const string ConfigMetaWithoutEffectBarred = "config_meta_without_effect";
	public const string StubAsHoursBarred = "stub_as_hours";
	public const string MapJobNameOnlyBarred = "map_job_name_only";
	public const string ForwardMapBarred = "gen_tone_biomes_pack_not_this_debt";

	public const string SummaryLine =
		"WORLD-propose feed · Accept→gen salt · Revise≠same land · Reject clears · menu-only barred · staging";

	public static Dictionary<string, object> ToLogFields() => new()
	{
		["ask_id"] = AskId,
		["slice_id"] = SliceId,
		["ticket_map"] = TicketMap,
		["series_id"] = SeriesId,
		["series_step"] = SeriesStep,
		["prior_menu_only_slice"] = PriorMenuOnlySliceId,
		["prior_menu_only_disposition"] = PriorMenuOnlyDisposition,
		["success_object"] = SuccessObject,
		["contract"] = ContractId,
		["accept_feeds_gen"] = AcceptFeedsGenLaw,
		["revise_changes_gen"] = ReviseChangesGenLaw,
		["reject_clears_feed"] = RejectClearsFeedLaw,
		["menu_only"] = MenuOnlyBarred,
		["meta_without_gen"] = MetaWithoutGenBarred,
		["hotkey_as_product_ux"] = HotkeyAsProductUxBarred,
		["config_meta_without_effect"] = ConfigMetaWithoutEffectBarred,
		["stub_as_hours"] = StubAsHoursBarred,
		["map_job_name_only"] = MapJobNameOnlyBarred,
		["forward_map"] = ForwardMapBarred,
		["summary"] = SummaryLine,
	};
}
