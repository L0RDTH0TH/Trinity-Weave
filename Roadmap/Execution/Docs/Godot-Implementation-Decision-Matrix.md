---
title: Godot Implementation Decision Matrix (Execution) — genesis-mythos-master
created: 2026-09-30
updated: 2026-09-30
tags: [execution, godot, decision-matrix, junior-mandatory, genesis-mythos-master]
para-type: Project
project-id: genesis-mythos-master
roadmap_track: execution
status: active
paint_ux_catalog: false
---
# Godot Implementation Decision Matrix

**Principle (quotable):** ClassDB first. Host Index binds. Never parallel physics/controller. Prefer stock Godot; extend only at seat/authority boundaries.

**Junior-mandatory** before any Code-Exhibit write touching player / camera / look / move. Pair with [[Godot-Stock-Patterns]] and [[PIN-stock_godot_fps]].

**Recipe-complete in v0 (no research blocker):** FPS locomotion/look, input focus after Control menus, multi-camera `Current` swap.

## Matrix

| Concern | Prefer stock Godot | Extend / wrap | Never |
|---------|-------------------|---------------|-------|
| Player move/look | `CharacterBody3D` + child `Camera3D` at eye height; `Input.MouseMode = Captured`; yaw on body (Y); pitch on camera (X) ~±1.4 rad; WASD → `Velocity` XZ + gravity + `MoveAndSlide()`; Esc → `Visible` (**do not bind Esc to quit while in play**) | Thin host may **enable/disable** the FPS script and expose the eye `Camera3D` to seat code | Free-fly `Camera3D` as the only mover; PerspectiveEnvelope / “FP rail” owning locomotion; HUD/label as proof of FP |
| Collision / floor | Floor/walls with `StaticBody3D` / collision shapes under the place | — | Visual meshes only (no collider under feet) |
| UI vs gameplay input | After Enter play: release GUI focus; overlays must not eat capture/WASD | Table chrome UI | Full-screen `Control` permanently stealing mouse/keys |
| Seats / Unauthorized | Wrong seat → on-screen `Error.Unauthorized`; seats **only** swap `Camera3D.Current` + enable/disable FPS | `ICameraRig` / Host Index = **selector, not mover**. Any host method named Move / Look / HandleInput that drives the player body = **defect** | Silent Ok; second look-move stack per seat |
| Rules / dice | See [[Junior-Tech-Adapt-How-To]] §3–4 + [[SeamRegistry-CSharp-Host-Index]] §B4 | Plugin host bind | Hardcoded combat that bypasses rules host for “demo” |
| Terrain / maps | See [[Junior-Tech-Adapt-How-To]] §1–2 | Authority wrappers | Second terrain authority |
| Scene structure | Editor-visible `res://player/Player.tscn` (body + eye cam + collision); instance into site | SessionComposer mounts prefab | Runtime-only invent tree with no openable prefab |

**Acceptance for any Alpha player/camera write:** Does ClassDB already solve this? If yes, stock first.

## Related

- [[Godot-Stock-Patterns]] — copy-paste FPS skeleton + anti-patterns
- [[PIN-stock_godot_fps]] — alpha_0 pin
- Trinity Half-B Alpha mode — PRECONDITIONS / invalid pass / gates (public weave Docs)
