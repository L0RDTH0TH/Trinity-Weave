using Godot;

namespace Genesis.Perspective;

/// <summary>
/// Stock Godot 4 CharacterBody3D FPS controller.
/// Architecture (Decision-Matrix Prefer + Godot-Stock-Patterns + KidsCanCode / tutorial body-yaw):
///   CharacterBody3D — yaw via RotateY (mouse X)
///   child Camera3D @ eye height — pitch via Rotation.X clamp (mouse Y)
/// Look in _Input via <see cref="FpsLookInput"/> (shared; not _UnhandledInput).
/// Move in _PhysicsProcess (get_vector → basis → Velocity → MoveAndSlide).
/// </summary>
public partial class PlayerFp : CharacterBody3D
{
	public const float Speed = 5f;
	public const float Gravity = 24f;
	public const float Sens = 0.0025f;
	public const float PitchMin = -1.4f;
	public const float PitchMax = 1.4f;

	private const bool DebugHud = true;

	private Camera3D _cam = null!;
	private float _pitch;
	private bool _controlEnabled;
	private Label? _hud;
	private Vector3 _prevPos;
	private Vector2 _mouseRelFrame;
	private int _motionEvents;
	private float _hudAccum;

	public Camera3D EyeCamera => _cam;
	public bool ControlEnabled => _controlEnabled;

	public override void _Ready()
	{
		FpsLookInput.ConfigureOnce();
		EnsureMoveActions();
		_cam = GetNode<Camera3D>("Camera3D");
		_pitch = _cam.Rotation.X;
		_cam.Current = true;
		_prevPos = GlobalPosition;
		EnsureHud();
		SetControlEnabled(true);
		SetCaptured(true);
		GD.Print($"[PlayerFp] ready display={DisplayServer.GetName()} mouse_mode={Input.MouseMode} cam.Current={_cam.Current} pos={GlobalPosition}");
	}

	/// <summary>
	/// InputMap actions (project.godot + runtime backup):
	///   move_forward  → W / Up     (deadzone 0.2)
	///   move_back     → S / Down
	///   move_left     → A / Left
	///   move_right    → D / Right
	/// </summary>
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
			InputMap.AddAction(action, 0.2f);
		if (!ActionHasPhysicalKey(action, primary))
			InputMap.ActionAddEvent(action, new InputEventKey { PhysicalKeycode = primary });
		if (!ActionHasPhysicalKey(action, secondary))
			InputMap.ActionAddEvent(action, new InputEventKey { PhysicalKeycode = secondary });
	}

	private static bool ActionHasPhysicalKey(string action, Key key)
	{
		foreach (var ev in InputMap.ActionGetEvents(action))
		{
			if (ev is InputEventKey k && k.PhysicalKeycode == key)
				return true;
		}
		return false;
	}

	private void EnsureHud()
	{
		if (!DebugHud || _hud != null)
			return;
		var layer = new CanvasLayer { Name = "FpDebugLayer", Layer = 100 };
		_hud = new Label
		{
			Name = "FpDebugHud",
			Text = "posΔ=0 hvel=0 yaw=0 pitch=0 mouseRel=(0,0)",
			Position = new Vector2(12, 12),
			MouseFilter = Control.MouseFilterEnum.Ignore,
		};
		layer.AddChild(_hud);
		AddChild(layer);
	}

	public void SetCaptured(bool on)
	{
		Input.MouseMode = on ? Input.MouseModeEnum.Captured : Input.MouseModeEnum.Visible;
	}

	/// <summary>Thin host seat gate — enable/disable FPS processing; does not own locomotion math.</summary>
	public void SetControlEnabled(bool enabled)
	{
		_controlEnabled = enabled;
		SetPhysicsProcess(enabled);
		SetProcessInput(enabled);
		SetProcessUnhandledInput(false);
		if (!enabled)
			Velocity = Vector3.Zero;
	}

	public void ResetLook()
	{
		_pitch = -0.08f;
		Rotation = Vector3.Zero;
		if (_cam != null)
			_cam.Rotation = new Vector3(_pitch, 0f, 0f);
	}

	public void MakeCurrentCamera(bool current)
	{
		if (_cam != null)
			_cam.Current = current;
	}

	public override void _Input(InputEvent e)
	{
		if (!_controlEnabled)
			return;

		if (FpsLookInput.TryHandleCaptureToggle(GetViewport(), e))
			return;

		if (e is InputEventMouseMotion)
			_motionEvents++;

		if (!FpsLookInput.TryGetLookDelta(e, out var delta))
			return;

		// Immediate look in _Input — shared path with Tutorial (not _UnhandledInput).
		RotateY(-delta.X * Sens);
		_pitch = Mathf.Clamp(_pitch - delta.Y * Sens, PitchMin, PitchMax);
		_cam.Rotation = new Vector3(_pitch, 0f, 0f);
		_mouseRelFrame += delta;
	}

	public override void _PhysicsProcess(double delta)
	{
		if (!_controlEnabled)
			return;

		// Movement must NOT depend on mouse capture (prior bug: early-return when Visible
		// made WASD feel "dead" whenever pointer lock failed or Esc was pressed).
		var v = Velocity;
		if (!IsOnFloor())
			v.Y -= Gravity * (float)delta;

		var input = Input.GetVector("move_left", "move_right", "move_forward", "move_back");
		var dir = Transform.Basis * new Vector3(input.X, 0f, input.Y);
		if (dir.LengthSquared() > 0.0001f)
			dir = dir.Normalized();
		else
			dir = Vector3.Zero;

		v.X = dir.X * Speed;
		v.Z = dir.Z * Speed;
		Velocity = v;
		MoveAndSlide();

		var hVel = new Vector3(Velocity.X, 0f, Velocity.Z).Length();
		UpdateHud(input, hVel, (float)delta);
	}

	private void UpdateHud(Vector2 moveAxes, float hVel, float delta)
	{
		if (!DebugHud || _hud == null)
			return;

		var posDelta = (GlobalPosition - _prevPos).Length();
		_prevPos = GlobalPosition;
		var mouseRel = _mouseRelFrame;
		_mouseRelFrame = Vector2.Zero;
		var keys = moveAxes.LengthSquared() > 0.0001f;
		var captured = Input.MouseMode == Input.MouseModeEnum.Captured;

		_hud.Text =
			$"display={DisplayServer.GetName()} captured={captured} posΔ={posDelta:F3} hvel={hVel:F2} yaw={Rotation.Y:F3} pitch={_pitch:F3} mouseRel=({mouseRel.X:F1},{mouseRel.Y:F1}) axes=({moveAxes.X:F2},{moveAxes.Y:F2}) motionEvt={_motionEvents}";

		_hudAccum += delta;
		if (_hudAccum >= 0.5f)
		{
			_hudAccum = 0f;
			if (keys && _motionEvents == 0)
				_hud.Text += "\n★ motion starved while WASD — Linux/display, not FPS math";
			GD.Print($"[PlayerFp] {_hud.Text}");
			_motionEvents = 0;
		}
	}
}
