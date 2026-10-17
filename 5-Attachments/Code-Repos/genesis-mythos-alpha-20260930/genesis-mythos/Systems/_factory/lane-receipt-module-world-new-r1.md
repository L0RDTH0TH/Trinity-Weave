# Lane receipt — alpha0_world_new_r1

- **ask_id:** `alpha0_world_new`
- **slice_id:** `alpha0_world_new_r1`
- **ticket_map:** `WORLD-new`
- **claim_class:** staging (awaiting operator F5 — **no ask_success**)
- **prior F5 fail (honesty):** first LIVE weld left `application/run/main_scene` on `uid://3pjdxlf6hwqa` = `scenes/WorldgenCraft.tscn` — LaunchShell/WorldPackage code existed but was **off the Play path** (orphan Success). Operator dropped straight into hex/craft grid.
- **amend weld (this pass):** `project.godot` `run/main_scene="res://LaunchShell.tscn"` — Playable entry = LaunchShell, not orphan classes.
- **weld path:** LaunchShell Create World → four gen biases → WorldPackage.OpenNew → PlayRegion → craft
- **brush KEEP:** owned Full = flat single-deck green (`EmitFullSingleDeckFromStage6`)
- **MCP verify:** `get_project_settings.main_scene=res://LaunchShell.tscn`; factory-runtime shows LaunchShell loaded then WORLD-new accept → craft
- **build:** `dotnet build` 0 errors (prior)
