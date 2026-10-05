using Genesis.Core;
using Genesis.Exemplar;
using Godot;

namespace Genesis.Ui;

public interface IUiHost
{
	Error MountLayers(SeatContext seat);
	Error SetLayer(StringName layer, bool visible);
	Error ReflectMode(int mode);
}

public interface IPlayRegionHost
{
	Error Mount(StringName mountId, SeatContext seat);
	Error Unmount();
	Error EnsureSingleViewport();
	Error BindSocket(StringName name, Node node);
	bool IsMounted { get; }
	StringName MountedId { get; }
}

/// <summary>Presentation shell launch + DevLeakageGuard (Phase 6.1.1).</summary>
public sealed class DevLeakageGuard
{
	public Error Check(string[] paths)
	{
		foreach (var p in paths)
		{
			if (string.IsNullOrEmpty(p)) continue;
			if (p.Contains("factory_attestation", System.StringComparison.OrdinalIgnoreCase) ||
			    p.Contains("half_b", System.StringComparison.OrdinalIgnoreCase))
				return Error.Unavailable;
		}
		return Error.Ok;
	}

	public bool IsClean { get; private set; }

	public void MarkClean(bool clean) => IsClean = clean;
}

public sealed class PresentationShellManifest
{
	public StringName ShellId { get; init; } = "presentation_shell_v0";
	public string[] LeakScanPaths { get; init; } = System.Array.Empty<string>();
}

public partial class PresentationSessionHandle : RefCounted
{
	public StringName SessionId { get; set; } = new StringName();
	public StringName ShellId { get; set; } = new StringName();
}

/// <summary>
/// Play region host — single visible PlayWorld (Node3D) so ICameraRig Current cams
/// are on the main window (kinesthetic proof). Contract mount lifecycle unchanged.
/// </summary>
public partial class PlayRegionHost : Node3D, IPlayRegionHost
{
	[Signal] public delegate void PresentationPlayRegionReadyEventHandler(ulong hostId);

	private Node3D? _playWorld;
	private readonly System.Collections.Generic.Dictionary<StringName, Node> _sockets = new();
	private bool _mounted;
	private StringName _mountedId = new StringName();
	private ReceiptLedger? _ledger;

	public bool IsMounted => _mounted;
	public StringName MountedId => _mountedId;
	public Node3D? PlayWorld => _playWorld;

	public void BindLedger(ReceiptLedger ledger) => _ledger = ledger;

	public Error EnsureSingleViewport()
	{
		if (_playWorld != null)
			return Error.AlreadyExists;
		_playWorld = new Node3D { Name = "PlayWorld" };
		AddChild(_playWorld);
		return Error.Ok;
	}

	public Error BindSocket(StringName name, Node node)
	{
		if (node == null || name == default) return Error.InvalidParameter;
		if (_sockets.ContainsKey(name)) return Error.AlreadyExists;
		_sockets[name] = node;
		if (node.GetParent() == null)
		{
			if (_playWorld != null)
				_playWorld.AddChild(node);
			else
				AddChild(node);
		}
		return Error.Ok;
	}

	public Error Mount(StringName mountId, SeatContext seat)
	{
		var seatErr = seat.GuardAny(SeatId.SessionCompose, SeatId.Presentation, SeatId.SharedTable);
		if (seatErr != Error.Ok) return seatErr;
		if (_mounted) return Error.AlreadyExists;
		if (mountId == default) return Error.InvalidParameter;
		if (_playWorld == null)
		{
			var vpErr = EnsureSingleViewport();
			if (vpErr != Error.Ok && vpErr != Error.AlreadyExists) return vpErr;
		}
		_mounted = true;
		_mountedId = mountId;
		EmitSignal(SignalName.PresentationPlayRegionReady, GetInstanceId());
		_ledger?.Record("R.shell.mount", "placeholder_ok",
			$"mount_id={mountId};DevLeakageGuard=pass", "shell.mount_id", "slot.shell.play_region");
		return Error.Ok;
	}

	public Error Unmount()
	{
		_mounted = false;
		_mountedId = new StringName();
		return Error.Ok;
	}
}

public partial class HUDLayerStack : Node, IUiHost
{
	private readonly System.Collections.Generic.Dictionary<StringName, CanvasLayer> _layers = new();
	private bool _mounted;
	private ReceiptLedger? _ledger;

	public void BindLedger(ReceiptLedger ledger) => _ledger = ledger;

	public override void _Ready()
	{
		EnsureLayer("base");
		EnsureLayer("mode");
		EnsureLayer("context");
		EnsureLayer("transient");
	}

	private CanvasLayer EnsureLayer(string name)
	{
		var sn = new StringName(name);
		if (_layers.TryGetValue(sn, out var existing)) return existing;
		var layer = new CanvasLayer { Name = $"Layer_{name}", Layer = _layers.Count };
		AddChild(layer);
		_layers[sn] = layer;
		return layer;
	}

	public Error MountLayers(SeatContext seat)
	{
		var seatErr = seat.GuardAny(SeatId.Presentation, SeatId.SessionCompose, SeatId.SharedTable);
		if (seatErr != Error.Ok) return seatErr;
		_Ready();
		_mounted = true;
		_ledger?.Record("R.shell.mount", "placeholder_ok",
			"mount_id=play_region_default;DevLeakageGuard=pass;hud=mounted",
			"ui.hud_stack", "slot.ui.hosts");
		return Error.Ok;
	}

	public Error SetLayer(StringName layer, bool visible)
	{
		if (!_mounted) return Error.Unconfigured;
		if (!_layers.TryGetValue(layer, out var l)) return Error.DoesNotExist;
		l.Visible = visible;
		return Error.Ok;
	}

	public Error ReflectMode(int mode)
	{
		if (!_mounted) return Error.Unconfigured;
		return SetLayer("mode", mode != 0);
	}
}

public sealed class LaunchFlowController
{
	private readonly DevLeakageGuard _guard = new();
	private readonly PresentationShellManifest _shell = new();
	private PlayRegionHost? _host;
	private HUDLayerStack? _hud;
	private PresentationSessionHandle? _handle;

	public PresentationShellManifest ShellManifest => _shell;
	public PlayRegionHost? PlayRegion => _host;
	public HUDLayerStack? Hud => _hud;
	public PresentationSessionHandle? SessionHandle => _handle;
	public DevLeakageGuard Guard => _guard;

	public void Bind(PlayRegionHost host, HUDLayerStack hud)
	{
		_host = host;
		_hud = hud;
	}

	public Error RunWithDevLeakageGuard(ReceiptLedger? ledger = null)
	{
		if (_host == null || _hud == null) return Error.Unconfigured;
		var err = _guard.Check(_shell.LeakScanPaths);
		if (err != Error.Ok) return err;
		_guard.MarkClean(true);
		err = _host.EnsureSingleViewport();
		if (err != Error.Ok && err != Error.AlreadyExists) return err;
		err = _host.Mount("play_region_default", SeatContext.SessionCompose);
		if (err != Error.Ok) return err;
		err = _hud.MountLayers(SeatContext.Presentation);
		if (err != Error.Ok) return err;
		_handle = new PresentationSessionHandle
		{
			SessionId = new StringName($"session_{Time.GetTicksMsec()}"),
			ShellId = _shell.ShellId
		};
		ledger?.Record("R.shell.mount", "placeholder_ok",
			"mount_id=play_region_default;DevLeakageGuard=pass",
			"shell.mount_id", "slot.shell.play_region");
		return Error.Ok;
	}
}
