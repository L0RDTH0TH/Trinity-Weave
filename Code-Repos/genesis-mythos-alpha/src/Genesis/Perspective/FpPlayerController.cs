using Godot;

namespace Genesis.Perspective;

/// <summary>
/// Stock Godot 4 FPS: CharacterBody3D body + Camera3D child at eye height.
/// Yaw on body (Y), pitch on camera (X). WASD from body facing. Esc/capture owned by host.
/// </summary>
public partial class FpPlayerController : CharacterBody3D
{
	public const float MoveSpeed = 5.2f;
	public const float LookSensitivity = 0.0025f;
	public const float EyeHeight = 1.65f;
	public const float PitchMinRad = -1.4f;
	public const float PitchMaxRad = 1.4f;
	public const float Gravity = 24f;

	private Camera3D? _camera;
	private float _pitch = -0.08f;
	private bool _controlEnabled;

	// Event-tracked keys so synthetic Input.parse_input_event (MCP) and real keys both move.
	private bool _heldW;
	private bool _heldS;
	private bool _heldA;
	private bool _heldD;
	private bool _heldUp;
	private bool _heldDown;
	private bool _heldLeft;
	private bool _heldRight;

	public Camera3D? EyeCamera => _camera;
	public bool ControlEnabled => _controlEnabled;

	public override void _Ready()
	{
		EnsureMoveActions();
		EnsureEyeCamera();
		// Start disabled — CameraRigHost enables on Player seat.
		SetControlEnabled(false);
	}

	private static void EnsureMoveActions()
	{
		EnsureKeyAction("move_forward", Key.W, Key.Up);
		EnsureKeyAction("move_back", Key.S, Key.Down);
		EnsureKeyAction("move_left", Key.A, Key.Left);
		EnsureKeyAction("move_right", Key.D, Key.Right);
	}

	private static void EnsureKeyAction(string action, Key primary, Key secondary)
	{
		if (!InputMap.HasAction(action))
			InputMap.AddAction(action);
		if (!ActionHasKey(action, primary))
		{
			var ev = new InputEventKey { Keycode = primary };
			InputMap.ActionAddEvent(action, ev);
		}
		if (!ActionHasKey(action, secondary))
		{
			var ev = new InputEventKey { Keycode = secondary };
			InputMap.ActionAddEvent(action, ev);
		}
	}

	private static bool ActionHasKey(string action, Key key)
	{
		foreach (var ev in InputMap.ActionGetEvents(action))
		{
			if (ev is InputEventKey k && k.Keycode == key)
				return true;
		}
		return false;
	}

	public void EnsureEyeCamera()
	{
		if (_camera != null && GodotObject.IsInstanceValid(_camera))
			return;

		_camera = GetNodeOrNull<Camera3D>("FpCamera");
		if (_camera != null)
			return;

		if (GetNodeOrNull<CollisionShape3D>("FpCapsule") == null)
		{
			var capsule = new CollisionShape3D
			{
				Name = "FpCapsule",
				Position = new Vector3(0f, 0.9f, 0f),
				Shape = new CapsuleShape3D { Radius = 0.35f, Height = 1.7f },
			};
			AddChild(capsule);
		}

		_camera = new Camera3D
		{
			Name = "FpCamera",
			Current = false,
			Fov = 75f,
			Position = new Vector3(0f, EyeHeight, 0f),
		};
		AddChild(_camera);
	}

	public void SetControlEnabled(bool enabled)
	{
		_controlEnabled = enabled;
		SetPhysicsProcess(enabled);
		SetProcessInput(enabled);
		SetProcessUnhandledInput(enabled);
		if (!enabled)
		{
			Velocity = Vector3.Zero;
			ClearHeldKeys();
		}
	}

	private void ClearHeldKeys()
	{
		_heldW = _heldS = _heldA = _heldD = false;
		_heldUp = _heldDown = _heldLeft = _heldRight = false;
	}

	public void ResetLook()
	{
		_pitch = -0.08f;
		Rotation = Vector3.Zero;
		if (_camera != null)
			_camera.Rotation = new Vector3(_pitch, 0f, 0f);
	}

	public void MakeCurrentCamera(bool current)
	{
		EnsureEyeCamera();
		if (_camera != null)
			_camera.Current = current;
	}

	public override void _Input(InputEvent @event)
	{
		if (!_controlEnabled)
			return;

		TrackHeldKeys(@event);

		// Click into viewport to recapture when mouse is free.
		if (@event is InputEventMouseButton { Pressed: true, ButtonIndex: MouseButton.Left }
		    && Input.MouseMode != Input.MouseModeEnum.Captured)
		{
			GetViewport()?.GuiReleaseFocus();
			Input.MouseMode = Input.MouseModeEnum.Captured;
			GetViewport().SetInputAsHandled();
			return;
		}

		if (Input.MouseMode != Input.MouseModeEnum.Captured)
			return;

		if (@event is InputEventMouseMotion motion)
		{
			RotateY(-motion.Relative.X * LookSensitivity);
			_pitch -= motion.Relative.Y * LookSensitivity;
			_pitch = Mathf.Clamp(_pitch, PitchMinRad, PitchMaxRad);
			if (_camera != null)
				_camera.Rotation = new Vector3(_pitch, 0f, 0f);
			GetViewport().SetInputAsHandled();
		}
	}

	public override void _UnhandledInput(InputEvent @event)
	{
		if (!_controlEnabled)
			return;
		TrackHeldKeys(@event);
	}

	private void TrackHeldKeys(InputEvent @event)
	{
		if (@event is not InputEventKey key || key.Echo)
			return;
		var pressed = key.Pressed;
		switch (key.Keycode)
		{
			case Key.W: _heldW = pressed; break;
			case Key.S: _heldS = pressed; break;
			case Key.A: _heldA = pressed; break;
			case Key.D: _heldD = pressed; break;
			case Key.Up: _heldUp = pressed; break;
			case Key.Down: _heldDown = pressed; break;
			case Key.Left: _heldLeft = pressed; break;
			case Key.Right: _heldRight = pressed; break;
		}
	}

	private Vector2 ReadMoveInput()
	{
		var x = 0f;
		var y = 0f;
		if (_heldW || _heldUp || Input.IsActionPressed("move_forward") || Input.IsKeyPressed(Key.W) || Input.IsKeyPressed(Key.Up))
			y -= 1f;
		if (_heldS || _heldDown || Input.IsActionPressed("move_back") || Input.IsKeyPressed(Key.S) || Input.IsKeyPressed(Key.Down))
			y += 1f;
		if (_heldA || _heldLeft || Input.IsActionPressed("move_left") || Input.IsKeyPressed(Key.A) || Input.IsKeyPressed(Key.Left))
			x -= 1f;
		if (_heldD || _heldRight || Input.IsActionPressed("move_right") || Input.IsKeyPressed(Key.D) || Input.IsKeyPressed(Key.Right))
			x += 1f;
		return new Vector2(x, y);
	}

	public override void _PhysicsProcess(double delta)
	{
		if (!_controlEnabled)
			return;

		var input = ReadMoveInput();

		var vel = Velocity;
		if (!IsOnFloor())
			vel.Y -= Gravity * (float)delta;
		else if (vel.Y < 0f)
			vel.Y = -0.1f;

		if (input != Vector2.Zero)
		{
			input = input.Normalized();
			// Body facing: -Z forward, +X right (stock Godot FPS).
			var direction = (Transform.Basis * new Vector3(input.X, 0f, input.Y)).Normalized();
			vel.X = direction.X * MoveSpeed;
			vel.Z = direction.Z * MoveSpeed;
		}
		else
		{
			vel.X = 0f;
			vel.Z = 0f;
		}

		Velocity = vel;
		MoveAndSlide();
	}
}
