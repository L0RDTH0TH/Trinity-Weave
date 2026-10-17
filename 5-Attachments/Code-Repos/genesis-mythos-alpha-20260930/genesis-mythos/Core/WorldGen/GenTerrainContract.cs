using System.Collections.Generic;

namespace Genesis.Core.WorldGen;

/// <summary>
/// GEN-terrain-product feedstock law (<c>alpha0_gen_terrain_product_r2</c>).
/// Active Prefer pin is now <see cref="GenToneContract"/> (<c>GEN-tone</c> / <c>alpha0_gen_tone_r1</c>).
/// Prior r1 remains feedstock; W1–W5 dials/altitude/rivers stay required for terrain face.
/// Prior 2a <c>alpha0_gen_terrain_r1</c> stays callable (Key.T accel) but is INCOMPLETE /
/// superseded for product Success — do not KEEP 2a.
/// Create World → Open = world already generated (auto same pass from bias+dials).
/// Enter Craft = empty amber until operator places (1g empty-enter applies to this lane ONLY).
/// No Generate button. Regen = dials + re-Open. Key.T accel only. Not Azgaar JS port.
/// Not Townscaper Done. Not GEN-biomes / PACK. No ask_success without F5.
/// </summary>
public static class GenTerrainContract
{
	public const string SliceId = "alpha0_gen_terrain_product_r2";
	public const string AskId = "alpha0_gen_terrain_product";
	public const string TicketMap = "GEN-terrain-product";
	public const string SeriesId = "alpha0_world_builder_r1";
	public const string SeriesStep = "gen_terrain_product";
	public const string PriorProductSliceId = "alpha0_gen_terrain_product_r1";
	public const string PriorWorldSliceId = "alpha0_world_parity_r1";
	public const string PriorWorldAskId = "alpha0_world_parity";

	/// <summary>Prior Key.T starter — keep callable as accel; incomplete for product Success.</summary>
	public const string PriorIncompleteSliceId = "alpha0_gen_terrain_r1";
	public const string PriorIncompleteAskId = "alpha0_gen_terrain";
	public const string PriorIncompleteDisposition = "incomplete_superseded_for_product_success";

	public const string SuccessObject = "generated_land_water_height_rivers_from_ui";
	public const string ContractId = "C_gen_terrain_product_w1_w5";

	/// <summary>Product invoke = Create World Open auto-gen. Key.T is accel only — not Success.</summary>
	public const string ExplicitInvokeLaw = "create_world_open_auto_gen_key_t_accel_only";
	/// <summary>1g empty-enter KEEP applies to Enter Craft (manual peer) only — not Create World Open.</summary>
	public const string EmptyEnterKeepLaw = "enter_craft_empty_amber_manual_lane_only_1g";
	public const string CreateWorldAutoGenLaw = "create_world_open_auto_run_gen_pass_from_bias_dials";
	public const string RegenViaReopenLaw = "regen_via_dials_change_and_reopen_or_session_rebind";
	public const string HeightReadsInCraftLaw = "vis_height_high_vs_low_in_craft_view";
	public const string DialsChangePassLaw = "cell_rivers_climate_wildness_change_pass";
	public const string RiversWatercourseLaw = "rivers_dial_gt0_readable_watercourse_eq0_none";
	public const string AltitudeBandsLaw = "azgaar_style_altitude_bands_land_water_height";

	public const string GenFillAsCraftEnterBarred = "gen_fill_not_craft_enter_success";
	public const string EmptyCreateWorldOpenBarred = "empty_create_world_open";
	public const string HotkeyAsProductUxBarred = "hotkey_as_product_ux";
	public const string GenerateButtonAsProductUxBarred = "generate_button_as_product_ux";
	public const string ConfigMetaWithoutEffectBarred = "config_meta_without_effect";
	public const string StubAsHoursBarred = "stub_as_hours";
	public const string MapJobNameOnlyBarred = "map_job_name_only";
	public const string BiomesHistoryBarred = "gen_biomes_history_not_this_slice";
	public const string TownscaperDoneBarred = "townscaper_done_not_gen_terrain_success";
	public const string AzgaarJsPortBarred = "azgaar_js_webview_port_not_product";
	/// <summary>Feedstock note — active Prefer is GenToneContract; terrain F5 park bar lifted.</summary>
	public const string GenToneSuccessor = "gen_tone_armed_alpha0_gen_tone_r1";

	public const string SummaryLine =
		"GEN-terrain-product-r2 feedstock · altitude bands · dials→pass · height · rivers · successor=GEN-tone-r1";

	public static Dictionary<string, object> ToLogFields() => new()
	{
		["ask_id"] = AskId,
		["slice_id"] = SliceId,
		["ticket_map"] = TicketMap,
		["series_id"] = SeriesId,
		["series_step"] = SeriesStep,
		["prior_product_slice"] = PriorProductSliceId,
		["prior_world_slice"] = PriorWorldSliceId,
		["prior_incomplete_slice"] = PriorIncompleteSliceId,
		["prior_incomplete_disposition"] = PriorIncompleteDisposition,
		["success_object"] = SuccessObject,
		["contract"] = ContractId,
		["explicit_invoke"] = ExplicitInvokeLaw,
		["empty_enter_keep"] = EmptyEnterKeepLaw,
		["create_world_auto_gen"] = CreateWorldAutoGenLaw,
		["regen_via_reopen"] = RegenViaReopenLaw,
		["height_reads_in_craft"] = HeightReadsInCraftLaw,
		["dials_change_pass"] = DialsChangePassLaw,
		["rivers_watercourse"] = RiversWatercourseLaw,
		["altitude_bands"] = AltitudeBandsLaw,
		["gen_fill_as_craft_enter"] = GenFillAsCraftEnterBarred,
		["empty_create_world_open"] = EmptyCreateWorldOpenBarred,
		["hotkey_as_product_ux"] = HotkeyAsProductUxBarred,
		["generate_button_as_product_ux"] = GenerateButtonAsProductUxBarred,
		["config_meta_without_effect"] = ConfigMetaWithoutEffectBarred,
		["stub_as_hours"] = StubAsHoursBarred,
		["map_job_name_only"] = MapJobNameOnlyBarred,
		["biomes_history"] = BiomesHistoryBarred,
		["townscaper_done"] = TownscaperDoneBarred,
		["azgaar_js_port"] = AzgaarJsPortBarred,
		["gen_tone_successor"] = GenToneSuccessor,
		["summary"] = SummaryLine,
	};
}
