// Tutorial-sanitized comparison clone; not production Prefer.
// Disables both FPS controllers so OverviewCamera stays current (visual side-by-side only).

using Godot;

namespace Genesis.Perspective;

public partial class FpsSanityCompare : Node3D
{
	public override void _Ready()
	{
		if (GetNodeOrNull("PlayerOurs") is PlayerFp ours)
		{
			ours.SetControlEnabled(false);
			ours.MakeCurrentCamera(false);
			ours.SetCaptured(false);
		}

		if (GetNodeOrNull("PlayerTutorial") is PlayerTutorial tut)
		{
			tut.MakeCurrentCamera(false);
			tut.SetPhysicsProcess(false);
			tut.SetProcessUnhandledInput(false);
			tut.SetProcessInput(false);
		}

		Input.MouseMode = Input.MouseModeEnum.Visible;
	}
}
