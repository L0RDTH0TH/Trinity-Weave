using Genesis.Ui;
using Godot;

namespace Genesis.Boundary;

public enum BuildProfile
{
	HorizonDemoInShell = 0,
	FactoryOnly = 1,
	DemoOnly = 2,
}

public sealed class DualTrackBoundaryManifest
{
	public StringName ProfileId { get; init; } = "horizon_demo_in_shell";
	public string[] FactoryAttestationKeys { get; init; } = { "factory.shell_ready", "factory.dev_leakage_clean" };
	public string[] DemoAttestationKeys { get; init; } = { "demo.loop_complete", "demo.stage" };
}

public sealed class TrackAuthorityRegistry
{
	private readonly System.Collections.Generic.Dictionary<StringName, StringName> _owners = new()
	{
		["presentation_shell"] = "factory",
		["play_region"] = "shared",
		["horizon_proof_loop"] = "demo",
		["receipt_ledger"] = "exemplar",
		["camera_rig"] = "shared",
		["sim_tick"] = "shared",
		["rules_plugin"] = "shared",
	};

	public StringName OwnerOf(StringName resource) =>
		_owners.TryGetValue(resource, out var o) ? o : "unknown";

	public Error AssertWrite(StringName track, StringName resource)
	{
		var owner = OwnerOf(resource);
		if (owner == "shared") return Error.Ok;
		if (owner == "unknown") return Error.DoesNotExist;
		if (owner != track) return Error.Unauthorized;
		return Error.Ok;
	}
}

public sealed class AttestationSeparationPolicy
{
	public bool KeysDisjoint(DualTrackBoundaryManifest m)
	{
		var factory = new System.Collections.Generic.HashSet<string>(m.FactoryAttestationKeys);
		foreach (var k in m.DemoAttestationKeys)
		{
			if (factory.Contains(k)) return false;
		}
		// Explicit: demo.loop_complete must never be a factory key.
		return !factory.Contains("demo.loop_complete");
	}
}

public sealed class CrossTrackEventFirewall
{
	private static readonly System.Collections.Generic.HashSet<string> AllowedShared =
		new(System.StringComparer.Ordinal)
		{
			"presentation_play_region_ready",
			"demo_stage_entered",
			"demo_loop_complete",
			"boundary_profile_selected",
		};

	public bool Allow(StringName eventId, StringName fromTrack, StringName toTrack)
	{
		if (fromTrack == toTrack) return true;
		if (fromTrack == "shared" || toTrack == "shared") return AllowedShared.Contains(eventId);
		// Demo must not write factory shell manifests / attestation.
		if (fromTrack == "demo" && toTrack == "factory")
			return false;
		if (fromTrack == "factory" && toTrack == "demo" && eventId == "factory.shell_ready")
			return true;
		return AllowedShared.Contains(eventId);
	}
}

public sealed class MountContractGlue
{
	public Error ValidateMount(IPlayRegionHost host, StringName demoId)
	{
		if (host == null) return Error.InvalidParameter;
		if (!host.IsMounted) return Error.Unconfigured;
		if (demoId == default) return Error.InvalidParameter;
		return Error.Ok;
	}
}

public sealed class BuildProfileSelector
{
	private BuildProfile _current = BuildProfile.HorizonDemoInShell;
	private readonly TrackAuthorityRegistry _authority = new();
	private readonly AttestationSeparationPolicy _attest = new();
	private readonly CrossTrackEventFirewall _firewall = new();

	public BuildProfile Current => _current;
	public TrackAuthorityRegistry Authority => _authority;
	public CrossTrackEventFirewall Firewall => _firewall;

	public Error Select(BuildProfile profile)
	{
		_current = profile;
		return Error.Ok;
	}

	public Error GateEvent(StringName eventId, StringName fromTrack, StringName toTrack)
	{
		if (!_firewall.Allow(eventId, fromTrack, toTrack))
			return Error.Unauthorized;
		return Error.Ok;
	}

	public Error ValidateBoundary(DualTrackBoundaryManifest m)
	{
		if (!_attest.KeysDisjoint(m))
			return Error.InvalidParameter;
		return Error.Ok;
	}

	/// <summary>Refuse path: demo track writing factory shell resource.</summary>
	public Error ProbeWrongTrackWrite() =>
		_authority.AssertWrite("demo", "presentation_shell");
}
