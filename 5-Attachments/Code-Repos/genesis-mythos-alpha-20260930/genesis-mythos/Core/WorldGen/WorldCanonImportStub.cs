using System;
using System.Collections.Generic;

namespace Genesis.Core.WorldGen;

/// <summary>
/// WORLD-import power-user entry (<c>alpha0_world_import_r1</c> / series 1e KEEP).
/// Play-path stub only — does <b>not</b> perform full world/offline-history canon ingest.
/// Honest status stays scaffolding until a later PACK/canon ticket lands Done.
/// Empty campaigns remain lawful (1f KEEP). Active weld = WORLD-parity (1g).
/// </summary>
public sealed class WorldCanonImportStub
{
	public const string SliceId = "alpha0_world_import_r1";
	public const string AskId = "alpha0_world_import";
	public const string TicketMap = "WORLD-import";
	public const string PriorKeepSliceId = "alpha0_world_s0_intents_r1";
	public const string StatusScaffolding = "scaffolding_not_full_ingest";
	public const string StatusBarred = "full_canon_ingest_barred";
	public const string DemoFixtureLabel = "offline_history_canon_bundle (fixture not loaded)";

	public enum Disposition
	{
		Idle,
		EntryShown,
		StubAcknowledged,
	}

	public Disposition Status { get; private set; } = Disposition.Idle;
	public string StatusCode { get; private set; } = StatusScaffolding;
	public string BundleLabel { get; private set; } = DemoFixtureLabel;
	public DateTimeOffset? EnteredAtUtc { get; private set; }
	public bool FullIngestClaimed => false;
	public bool CampaignsEmpty => true;

	public string SummaryLine =>
		$"WORLD-import stub · {StatusCode} · {WorldEmptyCampaignsContract.SummaryLine} · {WorldParityContract.SummaryLine} · full_ingest=false";

	public void ShowEntry()
	{
		Status = Disposition.EntryShown;
		StatusCode = StatusScaffolding;
		EnteredAtUtc = DateTimeOffset.UtcNow;
	}

	/// <summary>
	/// Acknowledge the power-user path without loading a real canon bundle.
	/// Refuses to claim full ingest Done.
	/// </summary>
	public void AcknowledgeStub(string? bundleLabel = null)
	{
		if (!string.IsNullOrWhiteSpace(bundleLabel))
			BundleLabel = bundleLabel.Trim();
		Status = Disposition.StubAcknowledged;
		StatusCode = StatusBarred;
		EnteredAtUtc ??= DateTimeOffset.UtcNow;
	}

	public Dictionary<string, object> ToLogFields()
	{
		var fields = new Dictionary<string, object>
		{
			["ask_id"] = AskId,
			["slice_id"] = SliceId,
			["ticket_map"] = TicketMap,
			["prior_keep_slice"] = PriorKeepSliceId,
			["import_status"] = Status.ToString().ToLowerInvariant(),
			["import_status_code"] = StatusCode,
			["bundle_label"] = BundleLabel,
			["full_ingest_claimed"] = FullIngestClaimed,
			["entered_at_utc"] = EnteredAtUtc?.ToString("O") ?? "",
			["active_weld_slice"] = WorldParityContract.SliceId,
		};
		foreach (var kv in WorldEmptyCampaignsContract.ToLogFields())
			fields[kv.Key] = kv.Value;
		foreach (var kv in WorldParityContract.ToLogFields())
			fields[kv.Key] = kv.Value;
		return fields;
	}
}
