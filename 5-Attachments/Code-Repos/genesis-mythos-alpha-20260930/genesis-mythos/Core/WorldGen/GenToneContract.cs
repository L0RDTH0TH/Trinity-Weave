using System.Collections.Generic;

namespace Genesis.Core.WorldGen;

/// <summary>
/// GEN-tone law (<c>alpha0_gen_tone_r1</c>).
/// Same dials / same dials-derived seed, two Create World biases → visibly different world
/// (land share / land shape / river feel / relief). Stored bias with identical board = refuse.
/// Bias must drive altitude / land-water / rivers / relief — not meta-only, not salt-hash
/// with the same silhouette. Prior GEN-terrain-product r2 dials/altitude face remains feedstock.
/// Create World Open auto-gen · Enter Craft empty · no Generate button. Nursery salt stubs stay
/// parked. Feedstock for PACK-save-load. Do not arm GEN-biomes. Operator F5 pass retained.
/// </summary>
public static class GenToneContract
{
	public const string SliceId = "alpha0_gen_tone_r1";
	public const string AskId = "alpha0_gen_tone";
	public const string TicketMap = "GEN-tone";
	public const string SeriesId = "alpha0_world_builder_r1";
	public const string SeriesStep = "gen_tone";
	public const string PriorProductSliceId = "alpha0_gen_terrain_product_r2";
	public const string PriorProductAskId = "alpha0_gen_terrain_product";
	public const string PriorProductTicket = "GEN-terrain-product";
	public const string SuccessorPackSliceId = PackSaveLoadContract.SliceId;

	public const string SuccessObject = "bias_reshapes_land_water_rivers_relief";
	public const string ContractId = "C_gen_tone_same_seed_two_biases";

	public const string SameSeedTwoBiasesLaw = "same_dials_seed_two_biases_different_board";
	public const string BiasDrivesLandformLaw = "bias_drives_altitude_land_water_rivers_relief";
	public const string StoredBiasIdenticalBoardBarred = "stored_bias_identical_board";
	public const string BiasSaltOnlySilhouetteBarred = "bias_salt_hash_same_silhouette";
	public const string BiasMetaOnlyBarred = "config_meta_without_effect";

	public const string CreateWorldAutoGenLaw = GenTerrainContract.CreateWorldAutoGenLaw;
	public const string EmptyEnterKeepLaw = GenTerrainContract.EmptyEnterKeepLaw;
	public const string GenerateButtonAsProductUxBarred = GenTerrainContract.GenerateButtonAsProductUxBarred;
	public const string HotkeyAsProductUxBarred = GenTerrainContract.HotkeyAsProductUxBarred;
	public const string EmptyCreateWorldOpenBarred = GenTerrainContract.EmptyCreateWorldOpenBarred;
	public const string PackSaveLoadSuccessor = "pack_save_load_armed_alpha0_pack_save_load_r1";
	public const string GenBiomesBarred = "gen_biomes_not_armed";
	public const string NurserySaltUnparkBarred = "nursery_salt_stubs_stay_parked";

	public const string SummaryLine =
		"GEN-tone-r1 feedstock · BiasLandform · successor=PACK-save-load-r1 · Create World Open auto-gen · Enter Craft empty · no Generate · GEN-biomes unarmed";

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
		["same_seed_two_biases"] = SameSeedTwoBiasesLaw,
		["bias_drives_landform"] = BiasDrivesLandformLaw,
		["stored_bias_identical_board"] = StoredBiasIdenticalBoardBarred,
		["bias_salt_only_silhouette"] = BiasSaltOnlySilhouetteBarred,
		["bias_meta_only"] = BiasMetaOnlyBarred,
		["create_world_auto_gen"] = CreateWorldAutoGenLaw,
		["empty_enter_keep"] = EmptyEnterKeepLaw,
		["generate_button_as_product_ux"] = GenerateButtonAsProductUxBarred,
		["hotkey_as_product_ux"] = HotkeyAsProductUxBarred,
		["empty_create_world_open"] = EmptyCreateWorldOpenBarred,
		["pack_save_load"] = PackSaveLoadSuccessor,
		["gen_biomes"] = GenBiomesBarred,
		["nursery_salt_unpark"] = NurserySaltUnparkBarred,
		["summary"] = SummaryLine,
	};
}
