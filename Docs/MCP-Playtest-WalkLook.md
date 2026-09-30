---
title: MCP Playtest — Walk / Look (necessary, not sufficient)
created: 2026-09-30
updated: 2026-09-30
audience: bone_pilot
status: provisional
factory_greenlit: false
---

# MCP Playtest — Walk / Look

**Necessary before asking the operator to F5. Never sufficient for Success.**

Ban: “MCP verified walk+look.” Walk+look Done = **operator F5 only** (gate `operator_kinesthetic_walk_look` = **block**).

Canonical patterns: project Execution Docs `Godot-Implementation-Decision-Matrix.md` + `Godot-Stock-Patterns.md`. Half-B PRECONDITIONS: [[Half-B-Alpha-Mode]].

## Necessary checks (agent / Godot MCP)

1. Resolve player scene/script — prefer `res://player/Player.tscn` or equivalent CharacterBody3D root.  
2. Assert **CharacterBody3D** + child **Camera3D** (eye height).  
3. Assert mouse capture path (`Input.MouseModeEnum.Captured` on Enter play / Player seat).  
4. Optional: position and/or camera basis change over time under input — still **not** Success.  
5. Esc → mouse Visible **without** quitting play.  
6. DM seat → aerial cam Current; FPS control disabled; return Player → FPS re-enabled.  

If any structural check fails → reject with `engine_pattern_miss` or `gui_input_steal` as appropriate. Do not mark Alpha Success.

## Operator

After necessary MCP checks pass, ask bone pilot to F5 and attest walk+look. Only then may `operator_kinesthetic_walk_look` pass.
