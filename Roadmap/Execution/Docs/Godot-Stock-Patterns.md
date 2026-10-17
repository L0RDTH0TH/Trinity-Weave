---
title: Godot Stock Patterns (Execution) — genesis-mythos-master
created: 2026-09-30
updated: 2026-09-30
tags: [execution, godot, stock-patterns, junior-mandatory, fps, genesis-mythos-master]
para-type: Project
project-id: genesis-mythos-master
roadmap_track: execution
status: active
paint_ux_catalog: false
---
# Godot Stock Patterns

**Mandatory** with [[Godot-Implementation-Decision-Matrix]] before player/camera Code-Exhibit writes.

**Preferred prefab:** `res://player/Player.tscn` (CharacterBody3D root + eye Camera3D + collision). Adjust path in a later code pass only if wrong — do not leave “somewhere.”

**Align with:** [CharacterBody3D](https://docs.godotengine.org/en/stable/classes/class_characterbody3d.html) + [Input](https://docs.godotengine.org/en/stable/classes/class_input.html) (Godot 4). Do not invent APIs that diverge from ClassDB.

FPS / input focus / multi-cam Current = **recipe-complete in v0** (no research blocker).

---

## 1. Stock FPS skeleton (C# — match this structure)

```csharp
using Godot;

public partial class PlayerFp : CharacterBody3D
{
    public const float Speed = 5f;
    public const float Gravity = 24f;
    public const float Sens = 0.0025f;
    public const float PitchMin = -1.4f;
    public const float PitchMax = 1.4f;

    private Camera3D _cam = null!;
    private float _pitch;

    public override void _Ready()
    {
        _cam = GetNode<Camera3D>("Camera3D"); // eye-height child on this body
    }

    public void SetCaptured(bool on)
    {
        Input.MouseMode = on ? Input.MouseModeEnum.Captured : Input.MouseModeEnum.Visible;
    }

    public override void _UnhandledInput(InputEvent e)
    {
        if (Input.MouseMode != Input.MouseModeEnum.Captured) return;
        if (e is InputEventMouseMotion m)
        {
            RotateY(-m.Relative.X * Sens);
            _pitch = Mathf.Clamp(_pitch - m.Relative.Y * Sens, PitchMin, PitchMax);
            _cam.Rotation = new Vector3(_pitch, 0f, 0f);
        }
    }

    public override void _PhysicsProcess(double delta)
    {
        if (Input.MouseMode != Input.MouseModeEnum.Captured) return;
        var v = Velocity;
        if (!IsOnFloor()) v.Y -= Gravity * (float)delta;
        var input = Input.GetVector("move_left", "move_right", "move_forward", "move_back");
        var dir = (Transform.Basis * new Vector3(input.X, 0, input.Y)).Normalized();
        v.X = dir.X * Speed;
        v.Z = dir.Z * Speed;
        Velocity = v;
        MoveAndSlide();
    }
}
```

**Scene:** `Player.tscn` → root `CharacterBody3D` (script above) → child `Camera3D` at eye height → `CollisionShape3D`. Floor under site must collide.

**Esc in play:** `Input.MouseMode = Input.MouseModeEnum.Visible` only — **never** `GetTree().Quit()` while table play is active. Recapture on resume Player / click into play.

---

## 2. Input focus after menus

After Host / role UI closes Enter play:

1. Hide or disable front-door / role `Control`s.
2. `GetViewport().GuiGetFocusOwner()?.ReleaseFocus();`
3. Ensure overlays use `MouseFilter` so they do not permanently eat mouse/keys.
4. Call FPS `SetCaptured(true)` for Player seat.

---

## 3. DM cam (seats only swap cameras)

- Separate aerial `Camera3D` (DM WorldCam).
- On DM: set DM cam `Current = true`; **disable** FPS script / control flag; mouse Visible or DM-appropriate.
- On Player: FP eye cam `Current = true`; **enable** FPS; Captured again.
- Hosts **select** cameras; they do **not** implement Move/Look/HandleInput on the player body.

---

## 4. Anti-patterns (named defects)

- PerspectiveEnvelope / “FP rail” owning locomotion
- Free-fly `Camera3D` as the player (no CharacterBody3D movement)
- Label / HUD “RAIL — first-person” as proof of FP
- Host `Move` / `Look` / `HandleInput` driving the player body (`ICameraRig` selector defect)
- Esc → quit while in play

See matrix [[Godot-Implementation-Decision-Matrix]] Player move/look row.
