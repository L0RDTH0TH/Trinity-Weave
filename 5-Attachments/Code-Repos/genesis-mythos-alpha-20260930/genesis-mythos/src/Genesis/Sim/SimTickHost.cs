using Genesis.Core;
using Genesis.Exemplar;
using Godot;
using Godot.Collections;

namespace Genesis.Sim;

public sealed class SimSnapshot
{
	public double SimTime { get; init; }
	public Dictionary Payload { get; init; } = new();
}

public sealed class WorldEventLog
{
	private readonly System.Collections.Generic.List<string> _rows = new();
	public IReadOnlyList<string> Rows => _rows;
	public void Append(string row) => _rows.Add(row);
	public bool Contains(string fragment) => _rows.Exists(r => r.Contains(fragment, System.StringComparison.Ordinal));
}

public interface ISimTickHost
{
	Error Tick(double simTime, SimSnapshot snapshot);
	int TickCount { get; }
}

/// <summary>Proof-loop sim host — hard cap ≤1 tick per arm; second tick → Bug.</summary>
public sealed class SimTickHost : ISimTickHost
{
	private readonly WorldEventLog _log;
	private ReceiptLedger? _ledger;
	private int _ticks;
	private bool _armed;
	private bool _paused;

	public SimTickHost(WorldEventLog log) => _log = log;
	public int TickCount => _ticks;
	public WorldEventLog Log => _log;

	public void BindLedger(ReceiptLedger ledger) => _ledger = ledger;

	public void Arm() => _armed = true;
	public void SetPaused(bool paused) => _paused = paused;

	public Error Tick(double simTime, SimSnapshot snapshot)
	{
		if (snapshot == null) return Error.InvalidParameter;
		if (_paused) return Error.Busy;
		if (!_armed) return Error.Unconfigured;
		if (_ticks >= 1) return Error.Bug; // one-shot violated
		_ticks++;
		_log.Append($"tick_once;simTime={simTime:F3}");
		_ledger?.Record("R.sim.tick_once", "placeholder_ok",
			"ticks<=1;WorldEventLog.contains=tick_once",
			"sim.tick_host", "slot.sim.tick");
		return Error.Ok;
	}
}
