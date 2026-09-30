using Godot;
using Godot.Collections;

namespace Genesis.Exemplar;

/// <summary>Receipt row for fill-matrix hosts the proof loop touches.
/// Status values: ok | placeholder_ok | deferred — never stub_only for campaign claim.</summary>
public sealed class ReceiptRow
{
	public string Id { get; init; } = "";
	public string Status { get; init; } = "placeholder_ok";
	public string Verify { get; init; } = "";
	public string? PackKey { get; init; }
	public string? Slot { get; init; }
	public string? Owner { get; init; }

	public Dictionary ToDict()
	{
		var d = new Dictionary
		{
			["id"] = Id,
			["status"] = Status,
			["verify"] = Verify,
		};
		if (PackKey != null) d["pack_key"] = PackKey;
		if (Slot != null) d["slot"] = Slot;
		if (Owner != null) d["owner"] = Owner;
		return d;
	}
}

public sealed class ReceiptLedger
{
	private readonly System.Collections.Generic.Dictionary<string, ReceiptRow> _rows = new();
	public bool StubOnly { get; set; }

	public void Record(string id, string status, string verify, string? packKey = null, string? slot = null, string? owner = null)
	{
		_rows[id] = new ReceiptRow
		{
			Id = id,
			Status = status,
			Verify = verify,
			PackKey = packKey,
			Slot = slot,
			Owner = owner
		};
	}

	public bool Has(string id) => _rows.ContainsKey(id);
	public ReceiptRow? Get(string id) => _rows.TryGetValue(id, out var r) ? r : null;

	public Dictionary ToDict()
	{
		var root = new Dictionary();
		if (StubOnly) root["stub_only"] = true;
		foreach (var (k, v) in _rows)
			root[k] = v.ToDict();
		return root;
	}

	/// <summary>Loop-touched receipts only — does NOT alone pass CampaignCapableDoDGate.</summary>
	public static readonly string[] LoopTouchedIds =
	{
		"R.shell.mount",
		"R.cam.fp_dm_split",
		"R.sim.tick_once",
		"R.rules.pf1_bind",
		"R.agency.envelope",
		"R.seam.completeness",
	};
}

/// <summary>Campaign DoD gate — demo.loop_complete alone never satisfies.
/// Missing required receipts → Unconfigured; stub_only → InvalidParameter.</summary>
public sealed class CampaignCapableDoDGate
{
	private StringName _lastFail = default;
	private readonly System.Collections.Generic.List<string> _missing = new();

	public static readonly string[] RequiredReceiptIds =
	{
		"R.seam.completeness",
		"R.gen.worldmap_hash",
		"R.gen.terrain_admit",
		"R.sim.tick_once",
		"R.cam.fp_dm_split",
		"R.agency.envelope",
		"R.rules.pf1_bind",
		"R.shell.mount",
		"R.authority.packages",
		"R.art.astroneer_bar",
		"R.pmg.physics_econ",
		"R.pmg.pre_llm_dm",
	};

	public StringName LastFailCode => _lastFail;
	public string[] LastMissingReceipts => _missing.ToArray();

	public Error Validate(Dictionary receiptLedger)
	{
		_missing.Clear();
		_lastFail = default;
		if (receiptLedger == null) return Error.InvalidParameter;
		if (receiptLedger.ContainsKey("stub_only") && receiptLedger["stub_only"].AsBool())
		{
			_lastFail = "exemplar_stub_gen_rejected";
			return Error.InvalidParameter;
		}
		// demo.loop_complete alone is never enough
		if (receiptLedger.Count == 1 && receiptLedger.ContainsKey("demo.loop_complete"))
		{
			_lastFail = "exemplar_demo_alone_rejected";
			return Error.InvalidParameter;
		}
		foreach (var rid in RequiredReceiptIds)
		{
			if (!receiptLedger.ContainsKey(rid))
			{
				_missing.Add(rid);
				continue;
			}
			var row = receiptLedger[rid].AsGodotDictionary();
			if (row == null || row.Count == 0)
			{
				_missing.Add(rid);
				continue;
			}
			var status = row.ContainsKey("status") ? row["status"].AsString() : "";
			var verify = row.ContainsKey("verify") ? row["verify"].AsString() : "";
			if (status == "stub_only")
			{
				_lastFail = "exemplar_stub_gen_rejected";
				return Error.InvalidParameter;
			}
			if (string.IsNullOrEmpty(verify))
			{
				_missing.Add(rid);
				continue;
			}
			if (status is not ("ok" or "placeholder_ok" or "deferred"))
			{
				_missing.Add(rid);
			}
		}
		if (_missing.Count > 0)
		{
			_lastFail = "exemplar_receipt_missing";
			return Error.Unconfigured;
		}
		return Error.Ok;
	}
}

public sealed class ReferenceExemplarManifest
{
	public StringName ScopeId { get; init; } = "medium_fantasy_default";
	public StringName TrackId { get; init; } = "reference_exemplar";
	public StringName RulesetId { get; init; } = "pathfinder_pf1";
}

public sealed class AuthorityPackageContract
{
	public Error AssertPlayerCosmetics(Dictionary pkg, SeatContextLike seat)
	{
		if (pkg.ContainsKey("writes_world") && pkg["writes_world"].AsBool())
			return Error.Unauthorized;
		if (seat.IsPlayer && pkg.ContainsKey("world_mutate") && pkg["world_mutate"].AsBool())
			return Error.Unauthorized;
		return Error.Ok;
	}

	public Error AssertDmWorld(Dictionary pkg) => Error.Ok;
}

/// <summary>Minimal seat flag without circular Core dependency in package dict helpers.</summary>
public readonly struct SeatContextLike
{
	public bool IsPlayer { get; init; }
}
