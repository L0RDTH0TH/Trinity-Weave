using Godot;

namespace Genesis.Perspective;

/// <summary>
/// Shared FPS pointer helpers used by Prefer (<see cref="PlayerFp"/>) and Tutorial
/// (<see cref="PlayerTutorial"/>).
///
/// Commonality fix: mouse look must run in <see cref="Node._Input"/> — not
/// <see cref="Node._UnhandledInput"/> — so GUI / focus / key-hold paths cannot
/// starve <see cref="InputEventMouseMotion"/> while WASD is held.
/// Prefer <see cref="InputEventMouseMotion.ScreenRelative"/> under Captured
/// (engine docs). Call <see cref="ConfigureOnce"/> from each controller Ready.
/// </summary>
public static class FpsLookInput
{
	private static bool s_configured;

	/// <summary>
	/// Once per process: disable accumulated input so motion is delivered as
	/// often as the platform emits it (docs / jitter guidance).
	/// </summary>
	public static void ConfigureOnce()
	{
		if (s_configured)
			return;
		s_configured = true;
		// Leave UseAccumulatedInput at engine default (true). Forcing false did not
		// fix Linux key-hold mouse starvation and can make motion delivery spikier.
	}

	/// <summary>
	/// When mouse is Captured, extract look delta from a motion event.
	/// Prefers ScreenRelative (unscaled); falls back to Relative.
	/// </summary>
	public static bool TryGetLookDelta(InputEvent e, out Vector2 delta)
	{
		delta = Vector2.Zero;
		if (Input.MouseMode != Input.MouseModeEnum.Captured)
			return false;
		if (e is not InputEventMouseMotion motion)
			return false;

		delta = motion.ScreenRelative;
		if (delta.IsZeroApprox())
			delta = motion.Relative;
		return !delta.IsZeroApprox();
	}

	/// <summary>
	/// Esc → Visible; LMB while Visible → Captured (+ optional GuiReleaseFocus).
	/// Returns true when the event was consumed for capture toggling.
	/// </summary>
	public static bool TryHandleCaptureToggle(Viewport? viewport, InputEvent e, bool releaseGuiFocusOnCapture = true)
	{
		if (e is InputEventKey { Pressed: true, Keycode: Key.Escape })
		{
			Input.MouseMode = Input.MouseModeEnum.Visible;
			viewport?.SetInputAsHandled();
			return true;
		}

		if (e is InputEventMouseButton { Pressed: true, ButtonIndex: MouseButton.Left }
		    && Input.MouseMode != Input.MouseModeEnum.Captured)
		{
			if (releaseGuiFocusOnCapture)
				viewport?.GuiReleaseFocus();
			Input.MouseMode = Input.MouseModeEnum.Captured;
			viewport?.SetInputAsHandled();
			return true;
		}

		return false;
	}
}
