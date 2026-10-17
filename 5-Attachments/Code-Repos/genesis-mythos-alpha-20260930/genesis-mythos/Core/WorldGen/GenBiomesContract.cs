using System.Collections.Generic;

namespace Genesis.Core.WorldGen;

/// <summary>
/// GEN-biomes law (<c>alpha0_gen_biomes_r1</c>).
/// After terrain gen (Create World Open), assign biomes to land cells from altitude /
/// climate / bias dials. Each biome has a mechanical tag that changes at least one
/// readout (movement cost or difficult terrain) AND a visible material/family tint.
/// String-on-a-cell alone = refuse. No creatures. Prior PACK-save-load + GEN-tone
/// feedstock retained. Create World Open auto-gen · Enter Craft empty · no Generate.
/// Nursery salts parked. Do not arm GEN-sites. No KEEP / ask_success without F5.
/// </summary>
public static class GenBiomesContract
{
	public const string SliceId = "alpha0_gen_biomes_r1";
	public const string AskId = "alpha0_gen_biomes";
	public const string TicketMap = "GEN-biomes";
	public const string SeriesId = "alpha0_world_builder_r1";
	public const string SeriesStep = "gen_biomes";
	public const string PriorProductSliceId = PackSaveLoadContract.SliceId;
	public const string PriorProductAskId = PackSaveLoadContract.AskId;
	public const string PriorProductTicket = PackSaveLoadContract.TicketMap;

	public const string SuccessObject = "biomes_mechanical_tags_visible_material";
	public const string ContractId = "C_gen_biomes_tags_and_look";

	public const string BiomesAssignedAfterTerrainLaw = "biomes_assigned_after_terrain_gen";
	public const string MechanicalTagChangesReadoutLaw = "biome_tag_changes_move_or_difficult_readout";
	public const string VisibleMaterialDifferenceLaw = "biome_visible_material_or_family_difference";
	public const string StringOnCellAloneBarred = "string_on_cell_alone_as_biome";
	public const string CreaturesBarred = "creatures_as_biome_success";
	public const string IdenticalLookBarred = "identical_look_all_land_biomes";

	public const string CreateWorldAutoGenLaw = GenTerrainContract.CreateWorldAutoGenLaw;
	public const string EmptyEnterKeepLaw = GenTerrainContract.EmptyEnterKeepLaw;
	public const string GenerateButtonAsProductUxBarred = GenTerrainContract.GenerateButtonAsProductUxBarred;
	public const string HotkeyAsProductUxBarred = GenTerrainContract.HotkeyAsProductUxBarred;
	public const string EmptyCreateWorldOpenBarred = GenTerrainContract.EmptyCreateWorldOpenBarred;
	public const string GenSitesBarred = "gen_sites_not_armed";
	public const string NurserySaltUnparkBarred = "nursery_salt_stubs_stay_parked";
	public const string PackSaveLoadKept = "pack_save_load_feedstock_retained";

	public const string SummaryLine =
		"GEN-biomes-r1 · land biomes + move/difficult tags + material tint · Create World Open auto-gen · Enter Craft empty · no Generate · GEN-sites unarmed";

	public static Dictionary<string, object> ToLogFields() => new()
	{
		["ask_id"] = AskId,
		["slice_id"] = SliceId,
		["ticket_map"] = TicketMap,
		["series_id"] = SeriesId,
		["series_step"] = SeriesStep,
		["prior_product_slice"] = PriorProductSliceId,
		["prior_product_ticket"] = PriorProductTicket,
		["success_object"] = SuccessObject,
		["contract"] = ContractId,
		["biomes_after_terrain"] = BiomesAssignedAfterTerrainLaw,
		["tag_changes_readout"] = MechanicalTagChangesReadoutLaw,
		["visible_material"] = VisibleMaterialDifferenceLaw,
		["string_on_cell_alone"] = StringOnCellAloneBarred,
		["creatures"] = CreaturesBarred,
		["identical_look"] = IdenticalLookBarred,
		["create_world_auto_gen"] = CreateWorldAutoGenLaw,
		["empty_enter_keep"] = EmptyEnterKeepLaw,
		["generate_button_as_product_ux"] = GenerateButtonAsProductUxBarred,
		["hotkey_as_product_ux"] = HotkeyAsProductUxBarred,
		["empty_create_world_open"] = EmptyCreateWorldOpenBarred,
		["gen_sites"] = GenSitesBarred,
		["nursery_salt_unpark"] = NurserySaltUnparkBarred,
		["pack_save_load"] = PackSaveLoadKept,
		["summary"] = SummaryLine,
	};
}
