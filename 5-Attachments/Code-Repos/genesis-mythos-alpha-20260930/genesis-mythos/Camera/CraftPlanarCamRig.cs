using Genesis.Core.ClosedAlpha;
using Godot;

namespace Genesis.Camera;

/// <summary>
/// Craft envelope / vtt_planar_ortho — planar lock, continuous 360° yaw orbit about focus,
/// pitched look-down (reads as 3D, not parallel-plane top-down), WASD plane pan, mouse-wheel zoom.
/// Sparky bindings stay off while this rig is active.
/// </summary>
public partial class CraftPlanarCamRig : Node3D
{
	/// <summary>WASD pan — 70× baseline (12 → 840); 10× prior craft (84).</summary>
	[Export] public float PanSpeed { get; set; } = 840f;
	[Export] public float OrbitSpeed { get; set; } = 1.2f;
	/// <summary>Horizontal orbit radius — density-lift frame (rings=5 @ spacing 210).</summary>
	/// <summary>Horizontal orbit radius — slightly closer so 35–40° pitch foreshortens the board.</summary>
	[Export] public float CameraDistance { get; set; } = 2200f;
	/// <summary>
	/// Derived from pitch + CameraDistance when ApplyPose runs; export kept for scene compat / inspect.
	/// Before tilt weld: ~3850 with distance 875 (≈77° look-down = parallel-plane feel).
	/// </summary>
	[Export] public float CameraHeight { get; set; } = 1845f;
	/// <summary>
	/// Look-down pitch from horizontal in degrees (Godot-negative). Default −40° (within 35–55° band)
	/// so WorldgenCraft reads as 3D; was −72 unused / effectively ~−77° from height/distance ratio.
	/// </summary>
	[Export] public float PitchDegrees { get; set; } = -40f;
	/// <summary>Shallowest look-down (closest to horizon) — operator band ~35°.</summary>
	[Export] public float MinPitchDegrees { get; set; } = -55f;
	/// <summary>Steepest look-down (closest to top-down) — operator band ~55° abs → −55 clamp floor.</summary>
	[Export] public float MaxPitchDegrees { get; set; } = -35f;
	/// <summary>Wheel zoom multiplicative step per notch.</summary>
	[Export] public float ZoomSpeed { get; set; } = 1.12f;
	/// <summary>Zoom clamps — headroom for rings=5 @ spacing 210.</summary>
	[Export] public float MinCameraHeight { get; set; } = 420f;
	[Export] public float MaxCameraHeight { get; set; } = 10500f;
	[Export] public float MinCameraDistance { get; set; } = 90f;
	[Export] public float MaxCameraDistance { get; set; } = 4200f;
	/// <summary>Radians per pixel for middle-mouse drag orbit (X=yaw, Y=pitch).</summary>
	[Export] public float OrbitDragSensitivity { get; set; } = 0.005f;

	private Camera3D? _camera;
	private Node3D? _focus;
	private float _orbitYaw;
	private bool _inputEnabled;

	public bool InputEnabled => _inputEnabled;
	public Camera3D? ActiveCamera => _camera;
	/// <summary>Effective look-down magnitude in degrees (35–55 band when defaults hold).</summary>
	public float EffectiveLookDownDegrees => Mathf.Abs(Mathf.Clamp(PitchDegrees, MinPitchDegrees, MaxPitchDegrees));

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

		ClampPitch();
		SyncHeightFromPitch();
		ApplyPose();
		AlphaFactoryLog.Emit(
			"camera.craft",
			"CraftCam_Arm",
			$"vtt_planar_ortho craft envelope armed — planar lock, pitch={PitchDegrees:0.#}° look-down={EffectiveLookDownDegrees:0.#}°, orbit 360 yaw, WASD pan, wheel zoom, sparky off");
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

	public override void _UnhandledInput(InputEvent @event)
	{
		if (!_inputEnabled || _focus == null || _camera == null)
			return;

		if (@event is InputEventMouseButton mb && mb.Pressed)
		{
			if (mb.ButtonIndex == MouseButton.WheelUp)
			{
				ApplyZoom(1f / ZoomSpeed);
				GetViewport().SetInputAsHandled();
				return;
			}
			if (mb.ButtonIndex == MouseButton.WheelDown)
			{
				ApplyZoom(ZoomSpeed);
				GetViewport().SetInputAsHandled();
				return;
			}
		}

		if (@event is InputEventMouseMotion motion
		    && Input.IsMouseButtonPressed(MouseButton.Middle))
		{
			_orbitYaw += motion.Relative.X * OrbitDragSensitivity;
			// Drag up → shallower pitch (more 3D); drag down → steeper (more top-down).
			PitchDegrees -= Mathf.RadToDeg(motion.Relative.Y * OrbitDragSensitivity);
			ClampPitch();
			SyncHeightFromPitch();
			ApplyPose();
			GetViewport().SetInputAsHandled();
		}
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

		if (Input.IsKeyPressed(Key.Q) || Input.IsKeyPressed(Key.E))
		{
			var orbit = 0f;
			if (Input.IsKeyPressed(Key.Q)) orbit -= 1f;
			if (Input.IsKeyPressed(Key.E)) orbit += 1f;
			// Continuous 360° — no ±90° clamp; sin/cos wrap naturally.
			_orbitYaw += orbit * OrbitSpeed * (float)delta;
		}

		ApplyPose();
	}

	private void ApplyZoom(float factor)
	{
		CameraDistance = Mathf.Clamp(CameraDistance * factor, MinCameraDistance, MaxCameraDistance);
		SyncHeightFromPitch();
		CameraHeight = Mathf.Clamp(CameraHeight, MinCameraHeight, MaxCameraHeight);
		// If height hit a clamp, back-solve distance so pitch stays in band.
		if (CameraHeight <= MinCameraHeight || CameraHeight >= MaxCameraHeight)
			CameraDistance = Mathf.Clamp(
				CameraHeight / Mathf.Max(1e-4f, Mathf.Tan(Mathf.DegToRad(EffectiveLookDownDegrees))),
				MinCameraDistance,
				MaxCameraDistance);
		ApplyPose();
	}

	private void ClampPitch()
	{
		// Note: MinPitchDegrees is more negative (steeper); MaxPitchDegrees is less negative (shallower).
		PitchDegrees = Mathf.Clamp(PitchDegrees, MinPitchDegrees, MaxPitchDegrees);
	}

	private void SyncHeightFromPitch()
	{
		var lookDown = EffectiveLookDownDegrees;
		CameraHeight = CameraDistance * Mathf.Tan(Mathf.DegToRad(lookDown));
	}

	private void ApplyPose()
	{
		if (_focus == null || _camera == null) return;
		ClampPitch();
		SyncHeightFromPitch();
		// Offset from pitch+distance then LookAt — pitch is owned by height/distance ratio
		// (do NOT overwrite Rotation after LookAt; that previously skewed silhouettes).
		var offset = new Vector3(
			Mathf.Sin(_orbitYaw) * CameraDistance,
			CameraHeight,
			Mathf.Cos(_orbitYaw) * CameraDistance);
		_camera.GlobalPosition = _focus.GlobalPosition + offset;
		if (offset.LengthSquared() > 1e-6f)
			_camera.LookAt(_focus.GlobalPosition, Vector3.Up);
	}
}
