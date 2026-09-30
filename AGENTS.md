# AGENTS — genesis-mythos-master

**Before any Code-Exhibit write touching player / camera / look / move:**

1. Open [[Roadmap/Execution/Docs/Godot-Implementation-Decision-Matrix]] and [[Roadmap/Execution/Docs/Godot-Stock-Patterns]].
2. In the agent report, **quote** the matrix principle line **and** the Player move/look row.
3. Implement stock `CharacterBody3D` FPS only (`res://player/Player.tscn` pattern). Hosts select cameras; they do not own locomotion.
4. Missing quote or invent-a-camera / envelope-as-mover ⇒ **pass status = invalid** (do not push playable claim; do not mark Alpha Success).

Reject codes: `engine_pattern_miss` | `gui_input_steal` | `seat_ok_feel_fail` | `verify_mcp_only`.

Walk+look Done = **operator F5 only**. Ban: “MCP verified walk+look.”

Factory `factory_greenlit` remains false until operator greenlight. See Trinity Docs `Half-B-Alpha-Mode.md` PRECONDITIONS + gates `godot_stock_fps` / `operator_kinesthetic_walk_look`.
