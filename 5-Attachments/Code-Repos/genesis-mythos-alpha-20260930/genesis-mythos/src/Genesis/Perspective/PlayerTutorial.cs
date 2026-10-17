// Tutorial-sanitized comparison clone; not production Prefer.
// Source pattern: Godot 4 CharacterBody3D FPS (Head Node3D pivot + Camera pitch),
// adapted from common tutorial structure (e.g. youtube.com/watch?v=A3HLeyaBCq4).
// No Genesis hosts, seat funnels, Decision-Matrix law, STOCK-AUTHORITY, or debug HUD.
// Look uses shared FpsLookInput in _Input (same commonality fix as Prefer).

using Godot;

namespace Genesis.Perspective;

public partial class PlayerTutorial : CharacterBody3D
{
	private const float WalkSpeed = 5f;
	private const float SprintSpeed = 8f;
	private const float JumpVelocity = 4.5f;
	private const float MouseSens = 0.003f;
	private const float BobFreq = 2.4f;
	private const float BobAmp = 0.08f;
	private const float BaseFov = 75f;
	private const float FovChange = 1.5f;

	private Node3D _head = null!;
	private Camera3D _cam = null!;
	private float _tBob;
	private float _gravity;

	public override void _Ready()
	{
		FpsLookInput.ConfigureOnce();
		_head = GetNode<Node3D>("Head");
		_cam = GetNode<Camera3D>("Head/Camera3D");
		_gravity = (float)ProjectSettings.GetSetting("physics/3d/default_gravity");
		EnsureMoveActions();
		Input.MouseMode = Input.MouseModeEnum.Captured;
	}

	public override void _Input(InputEvent @event)
	{
		if (FpsLookInput.TryHandleCaptureToggle(GetViewport(), @event))
			return;

		if (!FpsLookInput.TryGetLookDelta(@event, out var delta))
			return;

		// Head yaw (Y) from mouse X; camera pitch (X) from mouse Y — tutorial pivot split.
		_head.RotateY(-delta.X * MouseSens);
		_cam.RotateX(-delta.Y * MouseSens);
		var pitch = _cam.Rotation;
		pitch.X = Mathf.Clamp(pitch.X, Mathf.DegToRad(-90f), Mathf.DegToRad(90f));
		_cam.Rotation = pitch;
	}

	public override void _PhysicsProcess(double delta)
	{
		var dt = (float)delta;
		var v = Velocity;

		if (!IsOnFloor())
			v.Y -= _gravity * dt;

		if (Input.IsActionJustPressed("ui_accept") && IsOnFloor())
			v.Y = JumpVelocity;

		var speed = Input.IsKeyPressed(Key.Shift) ? SprintSpeed : WalkSpeed;
		var input = Input.GetVector("move_left", "move_right", "move_forward", "move_back");
		// Move relative to Head yaw (tutorial), not body basis.
		var dir = _head.GlobalTransform.Basis * new Vector3(input.X, 0f, input.Y);
		if (dir.LengthSquared() > 0.0001f)
			dir = dir.Normalized();
		else
			dir = Vector3.Zero;

		if (IsOnFloor())
		{
			if (dir != Vector3.Zero)
			{
				v.X = dir.X * speed;
				v.Z = dir.Z * speed;
			}
			else
			{
				v.X = Mathf.Lerp(v.X, 0f, dt * 7f);
				v.Z = Mathf.Lerp(v.Z, 0f, dt * 7f);
			}
		}
		else if (dir != Vector3.Zero)
		{
			v.X = Mathf.Lerp(v.X, dir.X * speed, dt * 3f);
			v.Z = Mathf.Lerp(v.Z, dir.Z * speed, dt * 3f);
		}

		Velocity = v;
		MoveAndSlide();

		// Head bob (sine / cosine) while grounded and moving.
		_tBob += dt * Velocity.Length() * (IsOnFloor() ? 1f : 0f);
		_cam.Position = HeadBob(_tBob);

		var velClamped = Mathf.Clamp(Velocity.Length(), 0.5f, SprintSpeed * 2f);
		var targetFov = BaseFov + FovChange * velClamped;
		_cam.Fov = Mathf.Lerp(_cam.Fov, targetFov, dt * 8f);
	}

	private Vector3 HeadBob(float time)
	{
		var pos = Vector3.Zero;
		pos.Y = Mathf.Sin(time * BobFreq) * BobAmp;
		pos.X = Mathf.Cos(time * BobFreq / 2f) * BobAmp;
		return pos;
	}

	/// <summary>Reuse project move_* actions; add at runtime if missing.</summary>
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

	/// <summary>Used by compare scene to leave overview camera as current.</summary>
	public void MakeCurrentCamera(bool current)
	{
		if (_cam != null)
			_cam.Current = current;
	}
}
