using Genesis.Core.ClosedAlpha;
using Godot;

namespace Genesis.Camera;

/// <summary>
/// Craft envelope / vtt_planar_ortho — planar lock, orbit ≤180° about focus,
/// WASD plane pan. Sparky bindings stay off while this rig is active.
/// </summary>
public partial class CraftPlanarCamRig : Node3D
{
	[Export] public float PanSpeed { get; set; } = 12f;
	[Export] public float OrbitSpeed { get; set; } = 1.2f;
	/// <summary>Horizontal orbit radius. Prefer board-readable top-down: smaller distance + taller height.</summary>
	[Export] public float CameraDistance { get; set; } = 5f;
	/// <summary>Height for manual-scale board (rings=2, spacing≈3 — large cells, low count).</summary>
	[Export] public float CameraHeight { get; set; } = 22f;
	/// <summary>Unused for pose math — kept for scene compat. Pose uses LookAt from height/distance offset.</summary>
	[Export] public float PitchDegrees { get; set; } = -72f;

	private Camera3D? _camera;
	private Node3D? _focus;
	private float _orbitYaw;
	private const float OrbitHalfRange = Mathf.Pi * 0.5f; // ±90° → 180° total
	private bool _inputEnabled;

	public bool InputEnabled => _inputEnabled;
	public Camera3D? ActiveCamera => _camera;

	public override void _Ready()
	{
		_focus = GetNodeOrNull<Node3D>("Focus") ?? new Node3D { Name = "Focus" };
		if (_focus.GetParent() == null)
			AddChild(_focus);

		_camera = GetNodeOrNull<Camera3D>("Camera3D");
		if (_camera == null)
		{
			_camera = new Camera3D
			{
				Name = "Camera3D",
				Projection = Camera3D.ProjectionType.Perspective,
				Fov = 50f,
			};
			AddChild(_camera);
		}

		ApplyPose();
		AlphaFactoryLog.Emit(
			"camera.craft",
			"CraftCam_Arm",
			"vtt_planar_ortho craft envelope armed — planar lock, orbit≤180, WASD pan, sparky off");
	}

	public void SetInputEnabled(bool enabled)
	{
		_inputEnabled = enabled;
		if (_camera != null)
			_camera.Current = enabled;
	}

	public void SetFocusWorld(Vector3 worldPos)
	{
		if (_focus != null)
			_focus.GlobalPosition = worldPos;
		ApplyPose();
	}

	public override void _Process(double delta)
	{
		if (!_inputEnabled || _focus == null || _camera == null)
			return;

		var pan = Input.GetVector("move_left", "move_right", "move_forward", "move_back");
		if (pan != Vector2.Zero)
		{
			var right = new Vector3(Mathf.Cos(_orbitYaw), 0f, -Mathf.Sin(_orbitYaw));
			var forward = new Vector3(Mathf.Sin(_orbitYaw), 0f, Mathf.Cos(_orbitYaw));
			_focus.GlobalPosition += (right * pan.X + forward * -pan.Y) * PanSpeed * (float)delta;
		}

		if (Input.IsMouseButtonPressed(MouseButton.Middle) || Input.IsKeyPressed(Key.Q) || Input.IsKeyPressed(Key.E))
		{
			var orbit = 0f;
			if (Input.IsKeyPressed(Key.Q)) orbit -= 1f;
			if (Input.IsKeyPressed(Key.E)) orbit += 1f;
			_orbitYaw = Mathf.Clamp(_orbitYaw + orbit * OrbitSpeed * (float)delta, -OrbitHalfRange, OrbitHalfRange);
		}

		ApplyPose();
	}

	private void ApplyPose()
	{
		if (_focus == null || _camera == null) return;
		// Offset then LookAt — do NOT clobber pitch after LookAt (that skewed the craft view
		// into near-edge-on silhouettes that read as "spike stars" on a flat hex board).
		var offset = new Vector3(
			Mathf.Sin(_orbitYaw) * CameraDistance,
			CameraHeight,
			Mathf.Cos(_orbitYaw) * CameraDistance);
		_camera.GlobalPosition = _focus.GlobalPosition + offset;
		if (offset.LengthSquared() > 1e-6f)
			_camera.LookAt(_focus.GlobalPosition, Vector3.Up);
	}
}
