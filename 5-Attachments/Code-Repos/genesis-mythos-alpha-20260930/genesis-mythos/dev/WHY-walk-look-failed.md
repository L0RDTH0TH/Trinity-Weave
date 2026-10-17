# Why walk+look kept failing (honest)

This is **not** because FPS controllers are hard. Prefer and Tutorial both failed the same way because they share the same **input delivery** path on this machine.

## What we know

1. Your session is **Wayland** (`XDG_SESSION_TYPE=wayland`).
2. Both C# controllers used the same mouse-look approach (motion events while Captured).
3. Linux reports of **WASD held → mouse motion ignored** are common (Godot issues / forums). That is compositor/display-server behavior, not CharacterBody3D math.
4. Prefer had an extra foot-gun: `_PhysicsProcess` **returned early when mouse was not Captured**, so a failed pointer-lock looked like “no WASD at all.”

## What to run (A/B)

| Scene | What it is |
|-------|------------|
| `dev/FpsSanityStockGdscript.tscn` | **main_scene now** — boring GDScript stock FPS + HUD that counts `motion_evt` while keys held |
| `dev/FpsSanity.tscn` | Prefer C# (movement no longer gated on capture) |
| `dev/FpsSanityTutorial.tscn` | Tutorial C# clone |

**Read the HUD:** if you hold WASD and move the mouse and `motion_evt/0.5s` stays **0**, Godot is not receiving mouse motion — no controller rewrite will invent those events.

## If motion is starved

1. Fully quit Godot; relaunch (project prefers `wayland` again).
2. Try CLI override: `godot --display-driver wayland` vs `godot --display-driver x11`.
3. Temporary: `xset r off` (disable key repeat) then retest.
4. Prefer a real mouse over a touchpad for the test.

FPS look+move is easy **when the OS delivers mouse motion while keys are down**. The hard part here was diagnosing that shared delivery failure, not inventing a third controller.
