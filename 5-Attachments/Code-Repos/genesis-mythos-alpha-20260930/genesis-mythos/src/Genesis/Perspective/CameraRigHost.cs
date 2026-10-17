using Genesis.Core;
using Genesis.Exemplar;
using Godot;

namespace Genesis.Perspective;

public enum PerspectiveMode
{
	FirstPerson,
	DmWorldCam,
}

public interface ICameraRig
{
	Error Activate(PerspectiveMode mode, SeatContext seat);
	Error ApplyFov(float fovDegrees);
	PerspectiveMode? ActiveMode { get; }
	bool FpMounted { get; }
	bool DmMounted { get; }
}

/// <summary>
/// Seat camera swap only. FP walk+look lives on <see cref="PlayerFp"/> (CharacterBody3D prefab).
/// DM = aerial Camera3D; FPS script disabled while DM is current.
/// Host Index ICameraRig = selector, not mover — no Move/Look/HandleInput on the body.
/// </summary>
public partial class CameraRigHost : Node3D, ICameraRig
{
	private const string PlayerScenePath = "res://player/Player.tscn";

	private PlayerFp? _fp;
	private Camera3D? _dmCam;
	private PerspectiveMode? _active;
	private ReceiptLedger? _ledger;
	private Error _lastRefuse = Error.Ok;
	private Vector3 _fpOrigin = new(0f, 1.65f, 7.5f);
	private Vector3 _dmOrigin = new(0f, 16f, 10f);
	private Vector3 _dmRotationDegrees = new(-58f, 0f, 0f);

	public PerspectiveMode? ActiveMode => _active;
	public bool FpMounted { get; private set; }
	public bool DmMounted { get; private set; }
	public Error LastRefuse => _lastRefuse;
	public bool MouseCaptured => Input.MouseMode == Input.MouseModeEnum.Captured;
	public PlayerFp? FpPlayer => _fp;

	public void BindLedger(ReceiptLedger ledger) => _ledger = ledger;

	public void SetSpawnOrigin(Vector3 eye) => _fpOrigin = eye;

	public void SetDmOrigin(Vector3 eye, Vector3? rotationDegrees = null)
	{
		_dmOrigin = eye;
		if (rotationDegrees.HasValue)
			_dmRotationDegrees = rotationDegrees.Value;
	}

	/// <summary>After site/stage travel — move mounted FP/DM cams to current origins.</summary>
	public void ApplySpawnOriginsToMountedRigs()
	{
		EnsureRigs();
		ResetFpToSpawn();
		if (_dmCam != null)
		{
			_dmCam.Position = _dmOrigin;
			_dmCam.RotationDegrees = _dmRotationDegrees;
		}
	}

	public override void _Ready() => EnsureRigs();

	private void EnsureRigs()
	{
		if (_fp != null && GodotObject.IsInstanceValid(_fp) && _dmCam != null && GodotObject.IsInstanceValid(_dmCam))
			return;

		_fp = GetNodeOrNull<PlayerFp>("Player") ?? GetNodeOrNull<PlayerFp>("FpPlayer");
		if (_fp == null)
		{
			var packed = GD.Load<PackedScene>(PlayerScenePath);
			if (packed == null)
			{
				GD.PushError($"[CameraRigHost] missing stock prefab {PlayerScenePath}");
				return;
			}
			_fp = packed.Instantiate<PlayerFp>();
			_fp.Name = "Player";
			AddChild(_fp);
		}

		_dmCam = GetNodeOrNull<Camera3D>("DmCamera");
		if (_dmCam == null)
		{
			_dmCam = new Camera3D
			{
				Name = "DmCamera",
				Current = false,
				Fov = 50f,
				Position = _dmOrigin,
				RotationDegrees = _dmRotationDegrees,
			};
			AddChild(_dmCam);
		}

		// Host owns seat enable — keep FPS off until Activate(FirstPerson).
		_fp.SetControlEnabled(false);
		_fp.MakeCurrentCamera(false);
		_fp.SetCaptured(false);
		Input.MouseMode = Input.MouseModeEnum.Visible;
	}

	private void ResetFpToSpawn()
	{
		if (_fp == null) return;
		// SpawnEye is eye height; body origin sits just above floor top (Y≈0).
		_fp.GlobalPosition = new Vector3(_fpOrigin.X, 0.05f, _fpOrigin.Z);
		_fp.Velocity = Vector3.Zero;
		_fp.ResetLook();
	}

	public Error Activate(PerspectiveMode mode, SeatContext seat)
	{
		_lastRefuse = Error.Ok;
		EnsureRigs();
		if (_fp == null || _dmCam == null)
			return Error.Unconfigured;

		if (mode == PerspectiveMode.DmWorldCam)
		{
			if (seat.Id == SeatId.Player)
			{
				_lastRefuse = Error.Unauthorized;
				WriteCamReceipt();
				return Error.Unauthorized;
			}
			var dmSeat = seat.GuardAny(SeatId.DmAsPlayer, SeatId.SessionCompose, SeatId.SharedTable);
			if (dmSeat != Error.Ok)
			{
				_lastRefuse = dmSeat;
				WriteCamReceipt();
				return dmSeat;
			}
			_fp.SetControlEnabled(false);
			ReleaseMouseCapture();
			_fp.MakeCurrentCamera(false);
			_dmCam.Current = true;
			_dmCam.Position = _dmOrigin;
			_dmCam.RotationDegrees = _dmRotationDegrees;
			_active = PerspectiveMode.DmWorldCam;
			DmMounted = true;
			WriteCamReceipt();
			return Error.Ok;
		}

		var fpSeat = seat.GuardAny(SeatId.Player, SeatId.SessionCompose, SeatId.SharedTable, SeatId.DmAsPlayer);
		if (fpSeat != Error.Ok)
		{
			_lastRefuse = fpSeat;
			return fpSeat;
		}
		_dmCam.Current = false;
		_fp.MakeCurrentCamera(true);
		if (!FpMounted)
			ResetFpToSpawn();
		_fp.SetControlEnabled(true);
		CaptureMouseForFp();
		_active = PerspectiveMode.FirstPerson;
		FpMounted = true;
		WriteCamReceipt();
		return Error.Ok;
	}

	public Error ApplyFov(float fovDegrees)
	{
		if (_active == null) return Error.Unconfigured;
		if (_active == PerspectiveMode.FirstPerson)
		{
			if (_fp?.EyeCamera == null) return Error.Unconfigured;
			_fp.EyeCamera.Fov = fovDegrees;
			return Error.Ok;
		}
		if (_dmCam == null) return Error.Unconfigured;
		_dmCam.Fov = fovDegrees;
		return Error.Ok;
	}

	public void SetFpControl(bool enabled)
	{
		EnsureRigs();
		if (_fp == null) return;
		var on = enabled && _active == PerspectiveMode.FirstPerson;
		_fp.SetControlEnabled(on);
		if (on)
			CaptureMouseForFp();
		else
			ReleaseMouseCapture();
	}

	/// <summary>Esc / UI: free the mouse without quitting. Look pauses until recapture.</summary>
	public void ReleaseMouseCapture()
	{
		Input.MouseMode = Input.MouseModeEnum.Visible;
		_fp?.SetCaptured(false);
	}

	/// <summary>Enter play / resume Player / click into viewport: capture for look.</summary>
	public void CaptureMouseForFp()
	{
		var vp = GetViewport();
		vp?.GuiReleaseFocus();
		_fp?.SetCaptured(true);
		Input.MouseMode = Input.MouseModeEnum.Captured;
	}

	private void WriteCamReceipt()
	{
		_ledger?.Record("R.cam.fp_dm_split", "placeholder_ok",
			$"fp_mount={(FpMounted ? "Ok" : "missing")};dm_mount={(DmMounted ? "Ok" : "missing")};player_to_dm=Unauthorized",
			"cam.fp_rig", "slot.cam.fp");
	}
}
