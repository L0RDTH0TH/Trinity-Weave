---
title: Godot Implementation Decision Matrix (Execution) — genesis-mythos-master
created: 2026-09-30
updated: 2026-10-01
tags: [execution, godot, decision-matrix, junior-mandatory, genesis-mythos-master]
para-type: Project
project-id: genesis-mythos-master
roadmap_track: execution
status: active
paint_ux_catalog: false
---
# Godot Implementation Decision Matrix

**Principle (quotable):** Copy the masters. ClassDB / locked stack row / Host Index first. Convert Pathfinder → computer calcs; route results and relationship/history context to the correct seat (Player vs DM). Prefer stock Godot/vendor; extend only at seat/authority boundaries. Never invent a parallel physics, terrain, rules, or notify/RP channel when a master already owns the concern.

**Law:** Trinity `engine_stock_authority` — gate `engine_stock_first` (block). Specialized FPS gate `godot_stock_fps` still applies under that umbrella.

**Junior-mandatory** before **any** Code-Exhibit write whose concern appears in this matrix or a Tech-Stack-Manifest `stack-*` row. Name the stock authority; quote Prefer/Never or [[Junior-Tech-Adapt-How-To]] reject. Player/camera also pair [[Godot-Stock-Patterns]] + [[PIN-stock_godot_fps]].

**Recipe-complete in v0 (no research blocker):** FPS locomotion/look, input focus after Control menus, multi-camera `Current` swap. Terrain3D / PF1 adapt recipes live in How-To (research not required to refuse inventing parallels).

## Matrix

| Concern | Prefer stock Godot | Extend / wrap | Never |
|---------|-------------------|---------------|-------|
| Player move/look | `CharacterBody3D` + child `Camera3D` at eye height; `Input.MouseMode = Captured`; yaw on body (Y); pitch on camera (X) ~±1.4 rad; WASD → `Velocity` XZ + gravity + `MoveAndSlide()`; Esc → `Visible` (**do not bind Esc to quit while in play**) | Thin host may **enable/disable** the FPS script and expose the eye `Camera3D` to seat code | Free-fly `Camera3D` as the only mover; PerspectiveEnvelope / “FP rail” owning locomotion; HUD/label as proof of FP |
| Collision / floor | Floor/walls with `StaticBody3D` / collision shapes under the place | — | Visual meshes only (no collider under feet) |
| UI vs gameplay input | After Enter play: release GUI focus; overlays must not eat capture/WASD | Table chrome UI | Full-screen `Control` permanently stealing mouse/keys |
| Seats / Unauthorized | Wrong seat → on-screen `Error.Unauthorized`; seats **only** swap `Camera3D.Current` + enable/disable FPS | `ICameraRig` / Host Index = **selector, not mover**. Any host method named Move / Look / HandleInput that drives the player body = **defect** | Silent Ok; second look-move stack per seat |
| Rules / dice | PF1 → calcs via Host Index §B4 + [[PF1-Ruleset-Content-Scaffold]] / How-To §3–4; surface results to calling seat (DM-called check → DM sees result without player call-out as only channel) | Plugin host bind | Hardcoded combat/dice bypassing rules host; parallel RPG resolution |
| Terrain / maps | Terrain3D `res://addons/terrain_3d/` (`stack-procedural-terrain`) via `ITerrainAuthority` — How-To §1–2 | Authority wrappers only | Second terrain authority; Gaea GridMap/TileMap as 3D terrain authority |
| Dual-grid world craft | **This round (Hot Wheels):** stock **GridMap** dual-grid craft per [[Townscaper-Dual-Grid-Craft-Grammar-Y19Mw5YsgjI]] / [[alpha0_townscaper_craft_core_r1]] — Terrain3D **not armed** on craft path. **Later Prefer:** Terrain3D as world/height authority + GridMap craft overlay — **one** craft cell data authority | Thin craft overlay / cell-commit glue only | Second parallel terrain or physics authority; custom voxel engine; GridMap as a second height/terrain authority beside Terrain3D; craft F5 Terrain3D leak |
| Seat result / DM context | Host Index routes skill/combat results + NPC relationship/history to DM/Player seats for RP | Thin seat UI | Parallel notify/RP channel that bypasses Host Index |
| Scene structure | Editor-visible `res://player/Player.tscn` (body + eye cam + collision); instance into site | SessionComposer mounts prefab | Runtime-only invent tree with no openable prefab |

**Acceptance:** Does a master already own this (ClassDB, Terrain3D, PF1 host, Host Index seam)? If yes, stock/wrap first and seat-route — do not invent.

## Stock authority index

| Concern | Stock id | Recipe |
|---------|----------|--------|
| Player FPS | `player_fps` / `godot_stock_fps` | [[PIN-stock_godot_fps]] · [[ENGINE-COMPILE-PACK-stock_godot_fps]] · [[Godot-Stock-Patterns]] |
| Terrain | `procedural_terrain` / `stack-procedural-terrain` | [[Junior-Tech-Adapt-How-To]] §1 · Terrain3D addon |
| Rules / dice | `rules_pf1` | [[Junior-Tech-Adapt-How-To]] §3–4 · [[PF1-Ruleset-Content-Scaffold]] · Host Index §B4 |
| Seats / context | `host_index_seams` | [[SeamRegistry-CSharp-Host-Index]] |
| Other stack rows | matching `stack-*` in [[Tech-Stack-Manifest-v1]] | Manifest + How-To / DRB |

**Law pointer:** Trinity card `engine_stock_authority` (gate `engine_stock_first`). Combined stack list = [[Tech-Stack-Manifest-v1]] — do not dump full BOM here.

## Related

- [[Godot-Stock-Patterns]] — copy-paste FPS skeleton + anti-patterns
- [[PIN-stock_godot_fps]] — alpha_0 pin
- [[Junior-Tech-Adapt-How-To]] — Terrain3D / dice / PF1 adapt recipes
- [[Tech-Stack-Manifest-v1]] — combined locked stack
- Trinity Half-B Alpha mode — PRECONDITIONS / invalid pass / gates
