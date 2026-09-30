using Genesis.Core;
using Genesis.Module;
using Genesis.Table;
using Godot;

namespace Genesis;

/// <summary>
/// Genesis Mythos table — Alpha 0 front door → example module cartridge → offline play.
/// Placeholder art. NOT campaign ship. No LAN. Factory not greenlit.
/// </summary>
public partial class GameSessionRoot : Node3D
{
	private FrontDoorUi? _frontDoor;
	private SessionRoleBoard? _roles;
	private TablePlaySession? _play;
	private ModulePack? _loadedPack;

	public override void _Ready()
	{
		Input.MouseMode = Input.MouseModeEnum.Visible;
		_frontDoor = new FrontDoorUi();
		_frontDoor.EnterPlayRequested += OnEnterPlay;
		_frontDoor.ExitRequested += () => GetTree().Quit();
		AddChild(_frontDoor);

		_roles = new SessionRoleBoard();
		_roles.ContinueRequested += OnRolesContinue;
		_roles.BackRequested += OnRolesBack;
		AddChild(_roles);

		_play = new TablePlaySession { Name = "TablePlaySession" };
		_play.ReturnToFrontDoor += OnReturnToFrontDoor;
		AddChild(_play);
		_play.Visible = false;

		_frontDoor.ShowDoor();
		GD.Print("[Alpha0] Front door ready — pick example_goblin_oneshot → Enter play");
	}

	private void OnEnterPlay(string packId)
	{
		var err = ModulePackLoader.Load(packId, out var pack, out var error);
		if (err != Error.Ok || pack == null)
		{
			GD.PushError($"[Alpha0] pack load failed: {error}");
			return;
		}
		_loadedPack = pack;
		GD.Print($"[Alpha0] Loaded pack_id={pack.PackId} pregens={pack.Pregens.Count} sites={pack.Sites.Count}");
		_frontDoor?.HideDoor();
		CallDeferred(nameof(OpenRolesDeferred));
	}

	private void OpenRolesDeferred()
	{
		if (_loadedPack == null) return;
		_roles?.Open(_loadedPack);
	}

	private void OnRolesBack()
	{
		_roles?.Close();
		_frontDoor?.ShowDoor();
		Input.MouseMode = Input.MouseModeEnum.Visible;
	}

	private void OnRolesContinue(SeatId seat, string pregenId)
	{
		if (_loadedPack == null || _play == null) return;
		_roles?.Close();
		_play.Visible = true;
		var err = _play.Start(_loadedPack, seat, pregenId);
		if (err != Error.Ok)
		{
			GD.PushError($"[Alpha0] table start failed: {err}");
			_play.Visible = false;
			_frontDoor?.ShowDoor();
			Input.MouseMode = Input.MouseModeEnum.Visible;
			return;
		}
		GD.Print($"[Alpha0] Table session started seat={seat} pregen={pregenId}");
	}

	private void OnReturnToFrontDoor()
	{
		if (_play != null)
		{
			foreach (var c in _play.GetChildren())
				c.QueueFree();
			_play.Visible = false;
		}
		_loadedPack = null;
		_roles?.Close();
		_frontDoor?.ShowDoor();
		Input.MouseMode = Input.MouseModeEnum.Visible;
	}

	/// <summary>Playtest/MCP helper — enter currently selected pack from front door.</summary>
	public void DebugEnterSelectedPack() => _frontDoor?.RequestEnterSelected();

	/// <summary>Playtest/MCP helper — continue from role board into site.</summary>
	public void DebugContinueFromRoles() => _roles?.RequestContinue();

	public override void _UnhandledInput(InputEvent @event)
	{
		// Esc on front door / roles quits; play session handles its own Esc.
		if (_play != null && _play.Visible) return;
		if (@event is InputEventKey { Pressed: true, Keycode: Key.Escape })
		{
			GetTree().Quit();
			GetViewport().SetInputAsHandled();
		}
	}
}
