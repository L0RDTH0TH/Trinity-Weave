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
/// ICameraRig — real FP CharacterBody3D (WASD + mouse look) + DM aerial over same place.
/// Player≠DM rail. Esc uncaptures mouse; click / resume Player seat recaptures.
/// </summary>
public partial class CameraRigHost : Node3D, ICameraRig
{
	private CharacterBody3D? _fpBody;
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
	public const float EyeHeight = 1.65f;
	public const float PitchMinRad = -1.4835f; // ~-85 deg
	public const float PitchMaxRad = 1.4835f;  // ~+85 deg
	public const float Gravity = 24f;

	public PerspectiveMode? ActiveMode => _active;
	public bool FpMounted { get; private set; }
	public bool DmMounted { get; private set; }
	public Error LastRefuse => _lastRefuse;
	public bool MouseCaptured => Input.MouseMode == Input.MouseModeEnum.Captured;

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
		if (_active != PerspectiveMode.FirstPerson || _fpBody == null || _fpCam == null)
			return;

		// Click into play viewport to recapture when mouse is free (Player FP seat).
		if (_fpControl && @event is InputEventMouseButton { Pressed: true, ButtonIndex: MouseButton.Left }
		    && Input.MouseMode != Input.MouseModeEnum.Captured)
		{
			CaptureMouseForFp();
			GetViewport().SetInputAsHandled();
			return;
		}

		if (!_fpControl || Input.MouseMode != Input.MouseModeEnum.Captured)
			return;

		if (@event is InputEventMouseMotion motion)
		{
			_yaw -= motion.Relative.X * LookSensitivity;
			_pitch -= motion.Relative.Y * LookSensitivity;
			_pitch = Mathf.Clamp(_pitch, PitchMinRad, PitchMaxRad);
			ApplyLookRotation();
			GetViewport().SetInputAsHandled();
		}
	}

	public override void _PhysicsProcess(double delta)
	{
		if (!_fpControl || _active != PerspectiveMode.FirstPerson || _fpBody == null)
			return;

		var input = Vector3.Zero;
		if (Input.IsKeyPressed(Key.W) || Input.IsKeyPressed(Key.Up)) input.Z -= 1f;
		if (Input.IsKeyPressed(Key.S) || Input.IsKeyPressed(Key.Down)) input.Z += 1f;
		if (Input.IsKeyPressed(Key.A) || Input.IsKeyPressed(Key.Left)) input.X -= 1f;
		if (Input.IsKeyPressed(Key.D) || Input.IsKeyPressed(Key.Right)) input.X += 1f;

		var vel = _fpBody.Velocity;
		if (!_fpBody.IsOnFloor())
			vel.Y -= Gravity * (float)delta;
		else if (vel.Y < 0f)
			vel.Y = -0.1f;

		if (input != Vector3.Zero)
		{
			input = input.Normalized();
			var basis = Basis.FromEuler(new Vector3(0f, _yaw, 0f));
			var wish = basis * input;
			wish.Y = 0f;
			wish = wish.Normalized() * MoveSpeed;
			vel.X = wish.X;
			vel.Z = wish.Z;
		}
		else
		{
			vel.X = 0f;
			vel.Z = 0f;
		}

		_fpBody.Velocity = vel;
		_fpBody.MoveAndSlide();
	}

	private void EnsureCams()
	{
		if (_fpBody != null && _fpCam != null && _dmCam != null) return;

		_fpBody = new CharacterBody3D
		{
			Name = "FpPlayer",
			FloorStopOnSlope = true,
			FloorMaxAngle = Mathf.DegToRad(46f),
		};
		var capsule = new CollisionShape3D
		{
			Name = "FpCapsule",
			Position = new Vector3(0f, 0.9f, 0f),
			Shape = new CapsuleShape3D { Radius = 0.35f, Height = 1.7f },
		};
		_fpBody.AddChild(capsule);

		_fpCam = new Camera3D
		{
			Name = "FpCamera",
			Current = false,
			Fov = 75f,
			Position = new Vector3(0f, EyeHeight, 0f),
		};
		_fpBody.AddChild(_fpCam);
		AddChild(_fpBody);

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

	private void ApplyLookRotation()
	{
		if (_fpBody == null || _fpCam == null) return;
		_fpBody.Rotation = new Vector3(0f, _yaw, 0f);
		_fpCam.Rotation = new Vector3(_pitch, 0f, 0f);
	}

	private void ResetFpToSpawn()
	{
		if (_fpBody == null || _fpCam == null) return;
		// SpawnEye is eye height; body feet sit slightly above floor top (Y≈0).
		_fpBody.GlobalPosition = new Vector3(_fpOrigin.X, 0.05f, _fpOrigin.Z);
		_fpBody.Velocity = Vector3.Zero;
		_yaw = 0f;
		_pitch = -0.08f;
		ApplyLookRotation();
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
			ReleaseMouseCapture();
			_fpCam!.Current = false;
			_dmCam!.Current = true;
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
		_dmCam!.Current = false;
		_fpCam!.Current = true;
		if (!FpMounted)
			ResetFpToSpawn();
		_fpControl = true;
		CaptureMouseForFp();
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
			CaptureMouseForFp();
		else
			ReleaseMouseCapture();
	}

	/// <summary>Esc / UI: free the mouse without quitting. Look pauses until recapture.</summary>
	public void ReleaseMouseCapture()
	{
		Input.MouseMode = Input.MouseModeEnum.Visible;
	}

	/// <summary>Enter play / resume Player / click into viewport: capture for look.</summary>
	public void CaptureMouseForFp()
	{
		var vp = GetViewport();
		vp?.GuiReleaseFocus();
		Input.MouseMode = Input.MouseModeEnum.Captured;
	}

	private void WriteCamReceipt()
	{
		_ledger?.Record("R.cam.fp_dm_split", "placeholder_ok",
			$"fp_mount={(FpMounted ? "Ok" : "missing")};dm_mount={(DmMounted ? "Ok" : "missing")};player_to_dm=Unauthorized",
			"cam.fp_rig", "slot.cam.fp");
	}
}
