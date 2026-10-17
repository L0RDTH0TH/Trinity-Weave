using System.Collections.Generic;
using System.Linq;
using Genesis.Core.ClosedAlpha;
using Godot;

namespace Genesis.Core.WorldGen;

/// <summary>
/// Root-meta session holder for the open world package (1a–1g KEEP + PACK-save-load).
/// Create World → Open auto-runs gen pass after craft ready; Enter Craft stays empty (1g manual only).
/// Load World restores a real <c>user://</c> pack (bias/dials/gen board) without blank amber.
/// Generate button stays struck. GEN-sites unarmed.
/// </summary>
public static class WorldPackageSession
{
	public const string MetaWorldId = "world_package_id";
	public const string MetaGenBias = "world_gen_bias";
	public const string MetaDisplayName = "world_display_name";
	public const string MetaCampaignsEmpty = "world_campaigns_empty";
	public const string MetaCampaignsEmptyLawful = "world_campaigns_empty_lawful";
	public const string MetaCampaignOwnership = "world_campaign_ownership";
	public const string MetaCampaignAttach = "world_campaign_attach";
	public const string MetaCampaignSummary = "world_campaign_summary";
	public const string MetaAuthorshipParity = "world_authorship_parity";
	public const string MetaParityProcedural = "world_parity_procedural_lane";
	public const string MetaParityManual = "world_parity_manual_lane";
	public const string MetaParityActiveLane = "world_parity_active_lane";
	public const string MetaParitySummary = "world_parity_summary";
	public const string MetaGenTerrainCreateWorldAuto = "world_gen_terrain_create_world_auto";
	public const string MetaWeldSlice = "world_weld_slice_id";
	public const string MetaAskId = "world_ask_id";
	/// <summary>Legacy HUD key — stores gen bias id (not campaign ToneProfile).</summary>
	public const string MetaLegacyTone = "worldgen_tone_profile";
	public const string MetaScaffoldId = "worldgen_scaffold_id";
	public const string MetaScaffoldRevision = "world_scaffold_revision";
	public const string MetaScaffoldStatus = "world_scaffold_status";
	public const string MetaScaffoldSummary = "world_scaffold_summary";
	public const string MetaScaffoldFeedSalt = "world_scaffold_feed_salt";
	public const string MetaScaffoldFeedsGenerator = "world_scaffold_feeds_generator";
	public const string MetaScaffoldCoastBias = "world_scaffold_coast_bias";
	public const string MetaScaffoldRidgeBias = "world_scaffold_ridge_bias";
	public const string MetaProposeFeedSlice = "world_propose_feed_slice_id";
	public const string MetaDialCellSize = "world_dial_cell_size";
	public const string MetaDialCellCount = "world_dial_cell_count";
	public const string MetaDialSeedRings = "world_dial_seed_rings";
	public const string MetaDialSettlement = "world_dial_settlement_distance";
	public const string MetaDialRivers = "world_dial_rivers";
	public const string MetaDialClimate = "world_dial_climate";
	public const string MetaDialWildness = "world_dial_wildness";
	public const string MetaDialsSummary = "world_dials_summary";
	public const string MetaIntentSummary = "world_s0_intent_summary";
	public const string MetaIntentAcceptedCount = "world_s0_intent_accepted_count";
	public const string MetaIntentAcceptedIds = "world_s0_intent_accepted_ids";
	public const string MetaIntentAcceptedTexts = "world_s0_intent_accepted_texts";
	public const string MetaLoreFeedSalt = "world_s0_lore_feed_salt";
	public const string MetaLoreFed = "world_s0_lore_fed";
	public const string MetaOptionalLoreSlice = "world_s0_optional_lore_slice_id";
	public const string MetaImportStatus = "world_import_status";
	public const string MetaImportStatusCode = "world_import_status_code";
	public const string MetaImportBundleLabel = "world_import_bundle_label";
	public const string MetaImportFullIngest = "world_import_full_ingest_claimed";
	public const string MetaGenTerrainApplied = "world_gen_terrain_applied";
	public const string MetaGenTerrainSummary = "world_gen_terrain_summary";
	public const string MetaGenTerrainSeed = "world_gen_terrain_seed";
	public const string MetaGenTerrainLandCount = "world_gen_terrain_land_count";
	public const string MetaGenTerrainWaterCount = "world_gen_terrain_water_count";
	public const string MetaGenTerrainRiverCount = "world_gen_terrain_river_count";
	public const string MetaGenTerrainHeightContract = "world_gen_terrain_height_contract";
	public const string MetaGenTerrainExplicit = "world_gen_terrain_explicit_invoke";
	public const string MetaPackRestorePending = "world_pack_restore_pending";
	public const string MetaPackPersistPath = "world_pack_persist_path";
	public const string MetaPackSlice = "world_pack_slice_id";
	/// <summary>
	/// Sticky for the Load World session — Create World Open auto-gen must not fire
	/// after the one-shot restore pending flag is consumed.
	/// </summary>
	public const string MetaPackLoadedFromPersist = "world_pack_loaded_from_persist";

	private static WorldPackage? _active;
	private static WorldCanonImportStub? _importStub;
	private static GenTerrainService.PassResult? _lastGenTerrain;

	public static WorldPackage? Active => _active;
	public static WorldCanonImportStub? ImportStub => _importStub;
	public static GenTerrainService.PassResult? LastGenTerrain => _lastGenTerrain;

	public static WorldPackage BindNew(
		SceneTree tree,
		WorldGenBias bias,
		WorldBoundsDials? bounds = null,
		WorldScaffoldProposal? scaffold = null,
		WorldSession0IntentBoard? intents = null,
		string? displayName = null)
	{
		var package = WorldPackage.OpenNew(bias, bounds, scaffold, intents, displayName);
		_active = package;
		ApplyMetas(tree.Root, package);
		// Create World Open path — clear any prior Load World sticky so auto-gen may run.
		tree.Root.SetMeta(MetaPackRestorePending, false);
		tree.Root.SetMeta(MetaPackLoadedFromPersist, false);
		AlphaFactoryLog.Emit(
			"world.open",
			"WORLD_parity",
			$"Create World open — id={package.WorldId} gen_bias={package.GenBiasId} scaffold={package.Scaffold.ScaffoldId} intents={package.Intents.AcceptedCount} dials=[{package.Bounds.SummaryLine()}] {WorldEmptyCampaignsContract.SummaryLine} · {WorldParityContract.SummaryLine}",
			package.ToLogFields());
		return package;
	}

	/// <summary>
	/// PACK-save-load — bind a persisted world package and mark craft to restore board from file
	/// instead of Create World Open auto-gen (refuse blank amber after load).
	/// </summary>
	public static WorldPackage BindFromPersisted(SceneTree tree, WorldPackage package)
	{
		_active = package;
		ApplyMetas(tree.Root, package);
		ApplyParityMetas(tree.Root, WorldParityContract.ProceduralLaneCode);
		tree.Root.SetMeta(MetaPackRestorePending, true);
		tree.Root.SetMeta(MetaPackLoadedFromPersist, true);
		tree.Root.SetMeta(MetaPackPersistPath, PackSaveLoadContract.PersistPath);
		tree.Root.SetMeta(MetaPackSlice, PackSaveLoadContract.SliceId);
		tree.Root.SetMeta(MetaWeldSlice, PackSaveLoadContract.SliceId);
		tree.Root.SetMeta(MetaAskId, PackSaveLoadContract.AskId);
		tree.Root.SetMeta(MetaGenTerrainCreateWorldAuto, false);
		AlphaFactoryLog.Emit(
			"pack.load",
			"PACK_save_load",
			$"Load World bound from pack — id={package.WorldId} gen_bias={package.GenBiasId} dials=[{package.Bounds.SummaryLine()}] path={PackSaveLoadContract.PersistPath}",
			package.ToLogFields());
		return package;
	}

	/// <summary>True when LaunchShell Load World requested craft restore from pack file.</summary>
	public static bool IsPackRestorePending(Node root) =>
		root != null
		&& root.HasMeta(MetaPackRestorePending)
		&& root.GetMeta(MetaPackRestorePending).AsBool();

	/// <summary>
	/// True for the whole Load World craft session (sticky until BindNew / Enter Craft).
	/// Survives ConsumePackRestorePending so AutoGen cannot re-fire after restore.
	/// </summary>
	public static bool IsLoadedFromPack(Node root) =>
		root != null
		&& root.HasMeta(MetaPackLoadedFromPersist)
		&& root.GetMeta(MetaPackLoadedFromPersist).AsBool();

	/// <summary>Consume pack-restore flag once craft begins restore (prevents double apply).</summary>
	public static bool ConsumePackRestorePending(Node root)
	{
		if (!IsPackRestorePending(root))
			return false;
		root.SetMeta(MetaPackRestorePending, false);
		return true;
	}

	/// <summary>
	/// Power-user WORLD-import entry on LaunchShell (1e KEEP-debt parked). Records stub metas only —
	/// does not load a real canon bundle. Real quit/reload is PACK-save-load Load World.
	/// </summary>
	public static WorldCanonImportStub BindImportStub(SceneTree tree, string? bundleLabel = null)
	{
		var stub = new WorldCanonImportStub();
		stub.ShowEntry();
		stub.AcknowledgeStub(bundleLabel);
		_importStub = stub;
		ApplyImportMetas(tree.Root, stub);
		AlphaFactoryLog.Emit(
			"world.import",
			"WORLD_import",
			$"WORLD-import stub acknowledged — {stub.SummaryLine} (full canon ingest barred; empty campaigns lawful; parity peers)",
			stub.ToLogFields());
		return stub;
	}

	/// <summary>
	/// Bind WORLD-parity peer law onto root even when Enter Craft opens without a Create World package.
	/// Manual lane remains a first-class peer — not a demoted toy path.
	/// </summary>
	public static void BindParityPeers(SceneTree tree, string activeLane)
	{
		ApplyParityMetas(tree.Root, activeLane);
		AlphaFactoryLog.Emit(
			"world.parity",
			"WORLD_parity",
			$"Authorship parity peers bound — active_lane={activeLane} · {WorldParityContract.SummaryLine}",
			new Dictionary<string, object>
			{
				["active_lane"] = activeLane,
				["slice_id"] = WorldParityContract.SliceId,
				["ask_id"] = WorldParityContract.AskId,
				["authorship_parity"] = WorldParityContract.PeerLaw,
			});
	}

	/// <summary>
	/// Record GEN-terrain pass metas after Create World auto-open or Generate regen.
	/// Enter Craft never binds via auto path.
	/// </summary>
	public static void BindGenTerrainResult(
		SceneTree tree,
		GenTerrainService.PassResult pass,
		bool createWorldAutoOpen = false)
	{
		_lastGenTerrain = pass;
		ApplyGenTerrainMetas(tree.Root, pass, createWorldAutoOpen);
		AlphaFactoryLog.Emit(
			"gen.terrain",
			"GEN_terrain",
			createWorldAutoOpen
				? $"GEN-terrain Create World auto-open bound — {pass.SummaryLine}"
				: $"GEN-terrain Generate/regen bound — {pass.SummaryLine}",
			pass.ToLogFields());
	}

	/// <summary>
	/// True when LaunchShell opened Create World (procedural package + active lane).
	/// Enter Craft (manual) returns false — empty amber KEEP applies there only.
	/// Load World returns false — pack restore owns the board (no AutoGen wipe).
	/// </summary>
	public static bool IsCreateWorldOpenPath(Node root)
	{
		if (root == null || _active == null)
			return false;
		if (IsLoadedFromPack(root) || IsPackRestorePending(root))
			return false;
		if (!root.HasMeta(MetaParityActiveLane))
			return false;
		return root.GetMeta(MetaParityActiveLane).AsString()
			== WorldParityContract.ProceduralLaneCode;
	}

	public static void ApplyMetas(Node root, WorldPackage package)
	{
		root.SetMeta(MetaWorldId, package.WorldId);
		root.SetMeta(MetaGenBias, package.GenBiasId);
		root.SetMeta(MetaDisplayName, package.DisplayName);
		root.SetMeta(MetaCampaignsEmpty, package.CampaignsEmpty);
		root.SetMeta(MetaCampaignsEmptyLawful, true);
		root.SetMeta(MetaCampaignOwnership, package.CampaignOwnership);
		root.SetMeta(MetaCampaignAttach, WorldEmptyCampaignsContract.AttachDeferredCode);
		root.SetMeta(MetaCampaignSummary, WorldEmptyCampaignsContract.SummaryLine);
		ApplyParityMetas(root, WorldParityContract.ProceduralLaneCode);
		root.SetMeta(MetaWeldSlice, package.WeldSliceId);
		root.SetMeta(MetaAskId, WorldPackage.AskId);
		// HUD / craft hint path still reads worldgen_tone_profile — bind gen bias there.
		root.SetMeta(MetaLegacyTone, package.GenBiasId);
		root.SetMeta(MetaScaffoldId, package.Scaffold.ScaffoldId);
		root.SetMeta(MetaScaffoldRevision, package.Scaffold.Revision);
		root.SetMeta(MetaScaffoldStatus, package.Scaffold.Status.ToString().ToLowerInvariant());
		root.SetMeta(MetaScaffoldSummary, package.Scaffold.SummaryLine);
		root.SetMeta(MetaScaffoldFeedSalt, (int)package.Scaffold.GenFeedSalt);
		root.SetMeta(MetaScaffoldFeedsGenerator, package.Scaffold.FeedsGenerator);
		root.SetMeta(MetaScaffoldCoastBias, package.Scaffold.CoastBias);
		root.SetMeta(MetaScaffoldRidgeBias, package.Scaffold.RidgeBias);
		root.SetMeta(MetaProposeFeedSlice, WorldProposeFeedContract.SliceId);
		root.SetMeta(MetaDialCellSize, package.Bounds.CellSize);
		root.SetMeta(MetaDialCellCount, package.Bounds.CellCount);
		root.SetMeta(MetaDialSeedRings, package.Bounds.ToSeedRingCount());
		root.SetMeta(MetaDialSettlement, package.Bounds.SettlementDistance);
		root.SetMeta(MetaDialRivers, package.Bounds.Rivers);
		root.SetMeta(MetaDialClimate, package.Bounds.Climate);
		root.SetMeta(MetaDialWildness, package.Bounds.Wildness);
		root.SetMeta(MetaDialsSummary, package.Bounds.SummaryLine());
		root.SetMeta(MetaIntentSummary, package.Intents.SummaryLine);
		root.SetMeta(MetaIntentAcceptedCount, package.Intents.AcceptedCount);
		var accepted = package.Intents.AcceptedOnly();
		root.SetMeta(MetaIntentAcceptedIds, string.Join(",", accepted.Select(i => i.IntentId)));
		root.SetMeta(MetaIntentAcceptedTexts, string.Join(" | ", accepted.Select(i => i.Text)));
		root.SetMeta(MetaLoreFeedSalt, (int)package.Intents.LoreFeedSalt);
		root.SetMeta(MetaLoreFed, package.Intents.LoreFed);
		root.SetMeta(MetaOptionalLoreSlice, WorldSession0IntentBoard.OptionalLoreSliceId);
	}

	public static void ApplyParityMetas(Node root, string activeLane)
	{
		root.SetMeta(MetaAuthorshipParity, WorldParityContract.PeerLaw);
		root.SetMeta(MetaParityProcedural, WorldParityContract.ProceduralLaneCode);
		root.SetMeta(MetaParityManual, WorldParityContract.ManualLaneCode);
		root.SetMeta(MetaParitySummary, WorldParityContract.SummaryLine);
		root.SetMeta(MetaWeldSlice, GenTerrainContract.SliceId);
		root.SetMeta(MetaAskId, GenTerrainContract.AskId);
		root.SetMeta(MetaParityActiveLane, activeLane);
		root.SetMeta(MetaGenTerrainExplicit, GenTerrainContract.ExplicitInvokeLaw);
		if (!root.HasMeta(MetaGenTerrainApplied))
			root.SetMeta(MetaGenTerrainApplied, false);
		if (!root.HasMeta(MetaGenTerrainCreateWorldAuto))
			root.SetMeta(MetaGenTerrainCreateWorldAuto, false);
	}

	public static void ApplyGenTerrainMetas(
		Node root,
		GenTerrainService.PassResult pass,
		bool createWorldAutoOpen = false)
	{
		root.SetMeta(MetaWeldSlice, GenTerrainContract.SliceId);
		root.SetMeta(MetaAskId, GenTerrainContract.AskId);
		root.SetMeta(MetaGenTerrainApplied, true);
		root.SetMeta(MetaGenTerrainCreateWorldAuto, createWorldAutoOpen);
		root.SetMeta(MetaGenTerrainSummary, pass.SummaryLine);
		root.SetMeta(MetaGenTerrainSeed, (int)pass.Seed);
		root.SetMeta(MetaGenTerrainLandCount, pass.LandCount);
		root.SetMeta(MetaGenTerrainWaterCount, pass.WaterCount);
		root.SetMeta(MetaGenTerrainRiverCount, pass.RiverCarveCount);
		root.SetMeta(MetaGenTerrainHeightContract, pass.HeightContract);
		root.SetMeta(MetaGenTerrainExplicit, GenTerrainContract.ExplicitInvokeLaw);
		root.SetMeta(MetaScaffoldFeedSalt, (int)pass.ScaffoldFeedSalt);
		root.SetMeta(MetaScaffoldFeedsGenerator, pass.ScaffoldFed);
		root.SetMeta(MetaProposeFeedSlice, WorldProposeFeedContract.SliceId);
		root.SetMeta(MetaLoreFeedSalt, (int)pass.LoreFeedSalt);
		root.SetMeta(MetaLoreFed, pass.LoreFed);
		root.SetMeta(MetaOptionalLoreSlice, WorldSession0IntentBoard.OptionalLoreSliceId);
	}

	public static void ApplyImportMetas(Node root, WorldCanonImportStub stub)
	{
		root.SetMeta(MetaWeldSlice, WorldPackage.SliceId);
		root.SetMeta(MetaAskId, WorldPackage.AskId);
		root.SetMeta(MetaCampaignsEmpty, stub.CampaignsEmpty);
		root.SetMeta(MetaCampaignsEmptyLawful, true);
		root.SetMeta(MetaCampaignOwnership, WorldEmptyCampaignsContract.OwnershipLaw);
		root.SetMeta(MetaCampaignAttach, WorldEmptyCampaignsContract.AttachDeferredCode);
		root.SetMeta(MetaCampaignSummary, WorldEmptyCampaignsContract.SummaryLine);
		ApplyParityMetas(root, WorldParityContract.ProceduralLaneCode);
		root.SetMeta(MetaImportStatus, stub.Status.ToString().ToLowerInvariant());
		root.SetMeta(MetaImportStatusCode, stub.StatusCode);
		root.SetMeta(MetaImportBundleLabel, stub.BundleLabel);
		root.SetMeta(MetaImportFullIngest, stub.FullIngestClaimed);
	}

	public static Dictionary<string, object> ActiveLogFields() =>
		_active?.ToLogFields() ?? new Dictionary<string, object>
		{
			["world_open"] = false,
			["slice_id"] = WorldPackage.SliceId,
			["authorship_parity"] = WorldParityContract.PeerLaw,
		};
}
