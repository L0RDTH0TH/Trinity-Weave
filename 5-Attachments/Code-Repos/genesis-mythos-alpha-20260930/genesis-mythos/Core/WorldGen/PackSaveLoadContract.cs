using System.Collections.Generic;

namespace Genesis.Core.WorldGen;

/// <summary>
/// PACK-save-load law (<c>alpha0_pack_save_load_r1</c>).
/// Quit and reload the same generated world (bias, dials, land/water/height/rivers,
/// optional hand edit) from a real <c>user://</c> pack file — not a fake toast.
/// Prior GEN-tone bias landform + GEN-terrain-product dials remain feedstock.
/// Create World Open auto-gen · Enter Craft empty · no Generate button.
/// Nursery salt stubs stay parked. 1e WORLD-import stays parked (real pack is this ticket).
/// Operator F5 pass retained as feedstock for GEN-biomes. No KEEP.
/// </summary>
public static class PackSaveLoadContract
{
	public const string SliceId = "alpha0_pack_save_load_r1";
	public const string AskId = "alpha0_pack_save_load";
	public const string TicketMap = "PACK-save-load";
	public const string SeriesId = "alpha0_world_builder_r1";
	public const string SeriesStep = "pack_save_load";
	public const string PriorProductSliceId = "alpha0_gen_tone_r1";
	public const string PriorProductAskId = "alpha0_gen_tone";
	public const string PriorProductTicket = "GEN-tone";
	public const string SuccessorBiomesSliceId = GenBiomesContract.SliceId;

	public const string SuccessObject = "quit_reload_same_generated_world_board";
	public const string ContractId = "C_pack_save_load_quit_reload_same_board";

	/// <summary>Canonical durable pack path under Godot user data (not a toast).</summary>
	public const string PersistPath = "user://worldgen/world_package_v1.json";

	public const string QuitReloadSameWorldLaw = "quit_and_reload_same_generated_world";
	public const string HandEditSurvivesLaw = "hand_edit_survives_reload";
	public const string RealFilePersistLaw = "real_user_data_pack_file_not_toast";
	public const string BlankAfterLoadBarred = "blank_amber_after_load";
	public const string LostWorldAfterLoadBarred = "lost_world_after_load";
	public const string FakeToastAsSaveBarred = "fake_toast_as_save";

	public const string CreateWorldAutoGenLaw = GenTerrainContract.CreateWorldAutoGenLaw;
	public const string EmptyEnterKeepLaw = GenTerrainContract.EmptyEnterKeepLaw;
	public const string GenerateButtonAsProductUxBarred = GenTerrainContract.GenerateButtonAsProductUxBarred;
	public const string HotkeyAsProductUxBarred = GenTerrainContract.HotkeyAsProductUxBarred;
	public const string EmptyCreateWorldOpenBarred = GenTerrainContract.EmptyCreateWorldOpenBarred;
	public const string GenBiomesSuccessor = "gen_biomes_armed_alpha0_gen_biomes_r1";
	public const string NurserySaltUnparkBarred = "nursery_salt_stubs_stay_parked";
	public const string WorldImportFullIngestBarred = "world_import_full_ingest_parked_until_pack";

	public const string SummaryLine =
		"PACK-save-load-r1 feedstock · quit/reload same board · organic_seed · successor=GEN-biomes-r1 · Create World Open auto-gen · Enter Craft empty · no Generate";

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
		["persist_path"] = PersistPath,
		["quit_reload_same_world"] = QuitReloadSameWorldLaw,
		["hand_edit_survives"] = HandEditSurvivesLaw,
		["real_file_persist"] = RealFilePersistLaw,
		["blank_after_load"] = BlankAfterLoadBarred,
		["lost_world_after_load"] = LostWorldAfterLoadBarred,
		["fake_toast_as_save"] = FakeToastAsSaveBarred,
		["create_world_auto_gen"] = CreateWorldAutoGenLaw,
		["empty_enter_keep"] = EmptyEnterKeepLaw,
		["generate_button_as_product_ux"] = GenerateButtonAsProductUxBarred,
		["hotkey_as_product_ux"] = HotkeyAsProductUxBarred,
		["empty_create_world_open"] = EmptyCreateWorldOpenBarred,
		["gen_biomes"] = GenBiomesSuccessor,
		["successor_biomes_slice"] = SuccessorBiomesSliceId,
		["nursery_salt_unpark"] = NurserySaltUnparkBarred,
		["world_import_parked"] = WorldImportFullIngestBarred,
		["summary"] = SummaryLine,
	};
}
