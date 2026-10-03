---
title: Module lane receipt — alpha0_townscaper_tutorial_s1_occupancy_r1 (hex-19 re-WELD)
slice_id: alpha0_townscaper_tutorial_s1_occupancy_r1
ask_id: alpha0_townscaper_tutorial
lane: module
created: 2026-10-02T20:45:30Z
claim_class: staging
dotnet_build: succeeded
curator: forbidden
---

# Module lane — tutorial s1 hex-19 re-WELD

## Changed paths (module zone)

- `Core/WorldGen/Hex19OccupancyLattice.cs` (new) — fixed 19 axial points (1+6+12)
- `Systems/DualGridCraftHost.cs` — **removed GridMap**; hex-19 markers + placement ghost + occupancy grid toggle
- `Systems/WorldgenCraft.cs` — hex pick, ghost update, **G** occupancy-grid toggle; dual toggle stubbed
- `Player/CraftFocusAnchor.cs` / `PlayRegion.cs` — doc align (pick owned by host)

## Success bar (staging — await operator F5)

1. Fixed hex-19 occupancy (center + 2 rings)
2. Placement ghost under cursor before commit
3. Occupancy grid display toggle (G)
4. LMB add / RMB remove under mouse; no cam yank; no Terrain3D; gray/ghost only

## Explicitly stripped / refused

- Dual MeshLibrary / connector / art Success
- Unbounded/rect GridMap as hex-19 (`infinite_rect_as_hex19`)
- `verify_mcp_only` · `bundle_tutorial_steps` · `terrain3d_in_scope` · cam yank

## Matrix quote

**Prefer:** Fixed hex-19 occupancy (1+6+12); placement ghost under cursor before commit; occupancy grid toggle; LMB place / RMB remove under mouse; gray/ghost marker OK this step; Terrain3D Prefer feed OUT OF SCOPE.

**Never:** Unbounded/rect GridMap as hex-19 Success; camera-center aim; cam recenter on place/remove; Terrain3D under craft; dual MeshLibrary / connector / art claimed as this step Success; bundle tutorial steps 2–5.
