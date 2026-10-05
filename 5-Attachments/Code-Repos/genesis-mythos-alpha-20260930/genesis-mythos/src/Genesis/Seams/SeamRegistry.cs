using Genesis.Core;
using Godot;
using Godot.Collections;

namespace Genesis.Seams;

public enum SeamLifecycle { Draft, Published, Deprecated }
public enum SeamFamily { Generation, Rules, Bus, Input }

public sealed class SeamEntry
{
	public required StringName SeamId { get; init; }
	public required SeamFamily Family { get; init; }
	public required StringName PortOwner { get; init; }
	public required SeamLifecycle Lifecycle { get; set; }
	public StringName LayerOwner { get; init; } = new("WorldState");
	public Dictionary SwapContract { get; init; } = new();
}

public interface ISeamRegistry
{
	Error Publish(SeamEntry entry);
	Error AssertPublished(StringName seamId);
	SeamEntry? Get(StringName seamId);
	Error Deprecate(StringName seamId);
}

public interface IPortBinder
{
	Error Bind(StringName seamId, GodotObject port, SeatContext seat);
	GodotObject? Resolve(StringName seamId);
}

public sealed class SeamRegistry : ISeamRegistry
{
	private readonly System.Collections.Generic.Dictionary<StringName, SeamEntry> _entries = new();

	public Error Publish(SeamEntry entry)
	{
		if (entry.SeamId == default || string.IsNullOrEmpty(entry.SeamId))
			return Error.InvalidParameter;
		if (_entries.TryGetValue(entry.SeamId, out var existing) &&
		    existing.Lifecycle == SeamLifecycle.Published &&
		    existing.PortOwner != entry.PortOwner)
			return Error.AlreadyExists;
		_entries[entry.SeamId] = entry;
		return Error.Ok;
	}

	public Error AssertPublished(StringName seamId)
	{
		if (!_entries.TryGetValue(seamId, out var e))
			return Error.DoesNotExist;
		return e.Lifecycle == SeamLifecycle.Published ? Error.Ok : Error.Unavailable;
	}

	public SeamEntry? Get(StringName seamId) =>
		_entries.TryGetValue(seamId, out var e) ? e : null;

	public Error Deprecate(StringName seamId)
	{
		if (!_entries.TryGetValue(seamId, out var e))
			return Error.DoesNotExist;
		e.Lifecycle = SeamLifecycle.Deprecated;
		return Error.Ok;
	}
}

public sealed class PortBinder : IPortBinder
{
	private readonly System.Collections.Generic.Dictionary<StringName, GodotObject> _ports = new();

	public Error Bind(StringName seamId, GodotObject port, SeatContext seat)
	{
		if (port == null) return Error.InvalidParameter;
		if (!seat.AllowsSessionCompose()) return Error.Unauthorized;
		_ports[seamId] = port;
		return Error.Ok;
	}

	public GodotObject? Resolve(StringName seamId) =>
		_ports.TryGetValue(seamId, out var p) ? p : null;
}

public sealed class CompletenessGate
{
	public static readonly StringName[] Required =
	{
		"gen.stage.terrain", "gen.stage.biomes", "gen.stage.pois", "gen.stage.entities",
		"gen.stage.sim_bootstrap", "rules.plugin.core", "bus.sub.sim_default",
		"bus.sub.canon_default", "input.parser.player_lite"
	};

	public Error Check(ISeamRegistry registry)
	{
		foreach (var id in Required)
		{
			var err = registry.AssertPublished(id);
			if (err != Error.Ok) return err;
		}
		return Error.Ok;
	}
}
