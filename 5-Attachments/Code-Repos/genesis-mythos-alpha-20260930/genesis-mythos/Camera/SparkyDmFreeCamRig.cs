using Genesis.Core.ClosedAlpha;
using Godot;

namespace Genesis.Camera;

/// <summary>
/// god_mode_sparky — free/sparky mastery DM cam for post-world inspect/fly.
/// Not the craft-authorship cam; bindings off until PlayRegion handoff.
/// </summary>
public partial class SparkyDmFreeCamRig : Node3D
{
	[Export] public float MoveSpeed { get; set; } = 14f;
	[Export] public float VerticalSpeed { get; set; } = 10f;
	[Export] public float MouseSensitivity { get; set; } = 0.003f;

	private Camera3D? _camera;
	private float _pitch = Mathf.DegToRad(-25f);
	private float _yaw;
	private bool _inputEnabled;

	public bool InputEnabled => _inputEnabled;
	public bool FreeCamEngaged { get; private set; }
	public bool IsTabletopTopDown => false;
	public float TabletopPitchRadians => -Mathf.Pi / 2f;

	public override void _Ready()
	{
		_camera = GetNodeOrNull<Camera3D>("Camera3D");
		if (_camera == null)
		{
			_camera = new Camera3D { Name = "Camera3D", Fov = 70f };
			AddChild(_camera);
		}
		ApplyRotation();
		AlphaFactoryLog.Emit("camera.sparky", "Sparky_Arm", "god_mode_sparky rig ready (bindings gated until handoff)");
	}

	public void SetInputEnabled(bool enabled)
	{
		_inputEnabled = enabled;
		if (_camera != null)
			_camera.Current = enabled;
		if (enabled)
			AlphaFactoryLog.Emit("camera.sparky", "Sparky_Handoff", "sparky bindings ON — post-world inspect/fly");
	}

	public void SnapAbove(Vector3 focus, float height = 16f)
	{
		GlobalPosition = focus + Vector3.Up * height;
		_yaw = 0f;
		_pitch = Mathf.DegToRad(-40f);
		ApplyRotation();
		FreeCamEngaged = true;
	}

	public override void _UnhandledInput(InputEvent @event)
	{
		if (!_inputEnabled) return;
		if (@event is InputEventMouseMotion motion && Input.MouseMode == Input.MouseModeEnum.Captured)
		{
			_yaw -= motion.Relative.X * MouseSensitivity;
			_pitch = Mathf.Clamp(_pitch - motion.Relative.Y * MouseSensitivity, -1.4f, 1.2f);
			ApplyRotation();
			FreeCamEngaged = true;
			GetViewport().SetInputAsHandled();
		}
	}

	public override void _Process(double delta)
	{
		if (!_inputEnabled) return;

		var move = Input.GetVector("move_left", "move_right", "move_forward", "move_back");
		var up = 0f;
		if (Input.IsKeyPressed(Key.Space)) up += 1f;
		if (Input.IsKeyPressed(Key.Shift)) up -= 1f;

		if (move != Vector2.Zero || up != 0f)
		{
			var basis = GlobalTransform.Basis;
			var forward = -basis.Z;
			var right = basis.X;
			GlobalPosition += (right * move.X + forward * -move.Y) * MoveSpeed * (float)delta;
			GlobalPosition += Vector3.Up * up * VerticalSpeed * (float)delta;
			FreeCamEngaged = true;
		}
	}

	private void ApplyRotation()
	{
		Rotation = new Vector3(_pitch, _yaw, 0f);
	}
}
