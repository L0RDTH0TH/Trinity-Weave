# Lane receipt — presentation WORLD-bounds r1

- slice_id: alpha0_world_bounds_r1
- ticket_map: WORLD-bounds
- series_step: 1b
- prior_keep: alpha0_world_new_r1 KEEP/ask_success
- play_path: res://LaunchShell.tscn
- files:
  - Core/WorldGen/WorldBoundsDials.cs
  - Core/WorldGen/WorldPackage.cs
  - Core/WorldGen/WorldPackageSession.cs
  - UI/WorldgenGui.cs
  - UI/WorldgenGui.tscn
  - LaunchShell.cs
- module_keep: Systems/DualGridCraftHost.cs unchanged
- claim_class: staging until operator F5
