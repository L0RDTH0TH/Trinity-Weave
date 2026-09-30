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

/// <summary>ICameraRig — FP eye-height WASD+mouse; DM aerial over same place. Player≠DM rail.</summary>
public partial class CameraRigHost : Node3D, ICameraRig
{
	private Camera3D? _fpCam;
	private Camera3D? _dmCam;
	private PerspectiveMode? _active;
	private ReceiptLedger? _ledger;
	private Error _lastRefuse = Error.Ok;
	private bool _fpControl;
	private float _yaw;
	private float _pitch = -0.08f;
	private Vector3 _fpOrigin = new(0f, 1.65f, 7.5f);
	private Vector3 _dmOrigin = new(0f, 16f, 10f);
	private Vector3 _dmRotationDegrees = new(-58f, 0f, 0f);

	public const float MoveSpeed = 5.2f;
	public const float LookSensitivity = 0.0025f;

	public PerspectiveMode? ActiveMode => _active;
	public bool FpMounted { get; private set; }
	public bool DmMounted { get; private set; }
	public Error LastRefuse => _lastRefuse;

	public void BindLedger(ReceiptLedger ledger) => _ledger = ledger;

	public void SetSpawnOrigin(Vector3 eye) => _fpOrigin = eye;

	public void SetDmOrigin(Vector3 eye, Vector3? rotationDegrees = null)
	{
		_dmOrigin = eye;
		if (rotationDegrees.HasValue)
			_dmRotationDegrees = rotationDegrees.Value;
	}
	public override void _Ready() => EnsureCams();

	public override void _UnhandledInput(InputEvent @event)
	{
		if (!_fpControl || _active != PerspectiveMode.FirstPerson || _fpCam == null)
			return;
		if (@event is InputEventMouseMotion motion)
		{
			_yaw -= motion.Relative.X * LookSensitivity;
			_pitch -= motion.Relative.Y * LookSensitivity;
			_pitch = Mathf.Clamp(_pitch, -1.25f, 1.15f);
			_fpCam.Rotation = new Vector3(_pitch, _yaw, 0f);
			GetViewport().SetInputAsHandled();
		}
	}

	public override void _Process(double delta)
	{
		if (!_fpControl || _active != PerspectiveMode.FirstPerson || _fpCam == null)
			return;
		var input = Vector3.Zero;
		if (Input.IsKeyPressed(Key.W) || Input.IsKeyPressed(Key.Up)) input.Z -= 1f;
		if (Input.IsKeyPressed(Key.S) || Input.IsKeyPressed(Key.Down)) input.Z += 1f;
		if (Input.IsKeyPressed(Key.A) || Input.IsKeyPressed(Key.Left)) input.X -= 1f;
		if (Input.IsKeyPressed(Key.D) || Input.IsKeyPressed(Key.Right)) input.X += 1f;
		if (input == Vector3.Zero) return;
		input = input.Normalized();
		var basis = Basis.FromEuler(new Vector3(0f, _yaw, 0f));
		var move = (basis * input) * MoveSpeed * (float)delta;
		var next = _fpCam.Position + move;
		// Soft courtyard bounds
		next.X = Mathf.Clamp(next.X, -6.2f, 6.2f);
		next.Z = Mathf.Clamp(next.Z, -9.5f, 8.5f);
		next.Y = _fpOrigin.Y;
		_fpCam.Position = next;
	}

	private void EnsureCams()
	{
		if (_fpCam != null && _dmCam != null) return;
		_fpCam = new Camera3D { Name = "FpCamera", Current = false, Fov = 75f, Position = _fpOrigin };
		AddChild(_fpCam);
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

	public Error Activate(PerspectiveMode mode, SeatContext seat)
	{
		_lastRefuse = Error.Ok;
		EnsureCams();

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
			_fpControl = false;
			Input.MouseMode = Input.MouseModeEnum.Visible;
			_fpCam!.Current = false;
			_dmCam!.Current = true;
			_dmCam.Position = _dmOrigin;
			_dmCam.RotationDegrees = _dmRotationDegrees;
			_active = PerspectiveMode.DmWorldCam;			DmMounted = true;
			WriteCamReceipt();
			return Error.Ok;
		}

		var fpSeat = seat.GuardAny(SeatId.Player, SeatId.SessionCompose, SeatId.SharedTable, SeatId.DmAsPlayer);
		if (fpSeat != Error.Ok)
		{
			_lastRefuse = fpSeat;
			return fpSeat;
		}
		_dmCam!.Current = false;
		_fpCam!.Current = true;
		if (!FpMounted)
		{
			_fpCam.Position = _fpOrigin;
			_yaw = 0f;
			_pitch = -0.08f;
			_fpCam.Rotation = new Vector3(_pitch, _yaw, 0f);
		}
		_fpControl = true;
		Input.MouseMode = Input.MouseModeEnum.Captured;
		_active = PerspectiveMode.FirstPerson;
		FpMounted = true;
		WriteCamReceipt();
		return Error.Ok;
	}

	public Error ApplyFov(float fovDegrees)
	{
		if (_active == null) return Error.Unconfigured;
		var cam = _active == PerspectiveMode.FirstPerson ? _fpCam : _dmCam;
		if (cam == null) return Error.Unconfigured;
		cam.Fov = fovDegrees;
		return Error.Ok;
	}

	public void SetFpControl(bool enabled)
	{
		_fpControl = enabled && _active == PerspectiveMode.FirstPerson;
		if (_fpControl)
			Input.MouseMode = Input.MouseModeEnum.Captured;
	}

	private void WriteCamReceipt()
	{
		_ledger?.Record("R.cam.fp_dm_split", "placeholder_ok",
			$"fp_mount={(FpMounted ? "Ok" : "missing")};dm_mount={(DmMounted ? "Ok" : "missing")};player_to_dm=Unauthorized",
			"cam.fp_rig", "slot.cam.fp");
	}
}
