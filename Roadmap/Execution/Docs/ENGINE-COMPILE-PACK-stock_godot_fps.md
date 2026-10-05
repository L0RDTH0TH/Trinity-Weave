---
title: ENGINE COMPILE PACK — stock_godot_fps
created: 2026-09-30
updated: 2026-09-30
tags: [execution, engine-compile-pack, stock_godot_fps, alpha_0, genesis-mythos-master]
para-type: Project
project-id: genesis-mythos-master
roadmap_track: execution
status: active
paint_ux_catalog: false
factory_greenlit: false
---
# ENGINE COMPILE PACK — stock_godot_fps

**Authority:** Execution maintainer pack for Alpha player/camera assembly. Not a coding-agent product brief and not a seat essay.

## Product moment (1 sentence)

Operator F5 on `res://dev/FpsSanity.tscn` walks with WASD and looks with mouse on a stock `CharacterBody3D` + eye `Camera3D` before any table Host/module UI returns to `main_scene`.

## Pins

| Pin | Role |
|-----|------|
| `stock_godot_fps` | Canonical locomotion/look recipe — [[PIN-stock_godot_fps]] |
| `input_focus_contract` | Capture / GUI release after menus — same PIN note + matrix UI row |

## Matrix / recipe pointers

- [[Godot-Implementation-Decision-Matrix]] — principle + Player move/look row (quote before Code-Exhibit write)
- [[Godot-Stock-Patterns]] — FPS skeleton, Esc→Visible, anti-patterns
- Prefab: `res://player/Player.tscn` · Sanity site: `res://dev/FpsSanity.tscn`

## Metaphor quarantine

Do **not** invent seams, Horizon/Exemplar regen, PerspectiveEnvelope-as-mover, free-fly-as-player, or HUD/label as FP proof. Hosts **select** cameras; they do **not** own Move/Look/HandleInput on the body.

## Assembly checklist (machine-checkable yes/no)

Fill with `file:line` or MCP structural evidence. **Do not** claim operator feel Done or “MCP verified walk+look.”

| # | Check | yes/no | Evidence |
|---|--------|--------|----------|
| 1 | Player root is `CharacterBody3D` + `PlayerFp` script | **yes** | `player/Player.tscn:9-12` type CharacterBody3D + script `PlayerFp.cs`; MCP `read_scene` root type CharacterBody3D |
| 2 | Child eye `Camera3D` at eye height | **yes** | `player/Player.tscn` Camera3D direct child of CharacterBody3D at y=1.65 (body yaw / cam pitch Prefer; no Head pivot) |
| 3 | Player has collision shape | **yes** | `player/Player.tscn` CapsuleShape3D CollisionShape3D |
| 4 | InputMap has `move_forward/back/left/right` | **yes** | `project.godot` `[input]` move_* (physical_keycode WASD+arrows, deadzone 0.2); `PlayerFp.EnsureMoveActions` runtime backup; `dotnet` `assembly_name=GenesisMythos` must match DLL |
| 5 | Player instanced in FpsSanity (no Host/module UI) | **yes** | `dev/FpsSanity.tscn` instance Player @ (0,2,0); scene nodes = Floor, Light, Player only |
| 6 | Floor = mesh + `StaticBody3D` + `CollisionShape3D` | **yes** | `dev/FpsSanity.tscn` PlaneMesh 40×40 + StaticBody3D + BoxShape3D |
| 7 | Capture on ready (`MouseMode` Captured) | **yes** | `PlayerFp.cs` SetCaptured(true) in `_Ready` |
| 8 | Eye cam `Current=true` on ready | **yes** | `PlayerFp.cs` `_cam.Current = true`; `player/Player.tscn` `current = true` |
| 9 | No other cam `Current` in FpsSanity tree | **yes** | `dev/FpsSanity.tscn` — only Player’s Camera3D; no DmCamera/Host/UI cams |
| 10 | Physics engine for FpsSanity path | **yes** | `project.godot` `3d/physics_engine="GodotPhysics3D"` (Jolt deferred until F5 walk+look) |

## Kinesthetic

**Only** operator F5 on FpsSanity (with `run/main_scene="res://dev/FpsSanity.tscn"`). Ban: “MCP verified walk+look.”

## Non-goals

- Table/Main UI reattach before operator FpsSanity walk+look attest
- Factory greenlight (`factory_greenlit` stays false)
- Catalog mint / Horizon / Exemplar regen from this pack
- Claiming Alpha Success from assembly checklist alone

## Invalid to start without pack

Any Code-Exhibit write touching player / camera / look / move that skips this pack + matrix quote ⇒ **pass status = invalid** (`engine_pattern_miss` risk).

## Revert main_scene (after operator F5)

```ini
run/main_scene="res://scenes/Main.tscn"
```

Do **not** restore Main until after operator FpsSanity F5.
