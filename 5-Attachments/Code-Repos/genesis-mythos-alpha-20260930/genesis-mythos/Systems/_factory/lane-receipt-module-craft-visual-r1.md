# Module lane receipt — `alpha0_townscaper_craft_visual_r1`

| Field | Value |
|-------|--------|
| receipt_id | `sp-craft-vis-032901-module` |
| slice_id | `row_ux_world_generation_r1_d6` |
| weld / overlay | `alpha0_townscaper_craft_visual_r1` |
| ask_id | `alpha0_townscaper_craft_visual` |
| UX bullets | UX-1 unmet_or_deferred · UX-3 preserved_prior · UX-5 preserved_prior · UX-7 unmet_or_deferred |
| visual bar | [[Visual-Factory-Direction-Stylized-Low-Poly]] (`stylized_low_poly`) |
| claim_class | staging |
| dotnet_build | (see module-lane-receipt.json) |

## Prefer proof designed for F5

- Placed dual-grid tiles read **stylized low-poly** (ArrayMesh facets — not BoxMesh graybox cubes)
- MeshLibrary variant ids still differ: Empty=0, Full=1, Corner=2, Edge=3, Diagonal=4, InverseCorner=5
- LMB place / RMB remove under mouse (logic-point lattice) — no cam yank
- Dual-grid neighbor-derived MeshLibrary path preserved (not raw-cell-only)
- Terrain3D absent/hard-disabled under craft; Tab refuses Terrain3D handoff
- Player seat Enter → Unauthorized (UX-3) — preserved prior, not this Prefer delta
- ImportAttach first-class (I key / auto-load persist) (UX-5) — preserved prior
- UX-1 collaborative propose/refine/preview/accept dialogue — **unmet_or_deferred** (not this Prefer ticket)
- UX-7 ux_worldgen_gui dialogue chrome — **unmet_or_deferred** (not this Prefer ticket)
- operator_f5_attest: **pending_operator** (claim_class staging)

## Matrix quote

**Prefer:** Stock GridMap dual-grid craft: interaction cell commit under mouse; visual/module form neighbor-derived; re-skin Full/Corner/Edge/Diagonal/InverseCorner+Empty to stylized low-poly — do not collapse masks to one cube. Terrain3D Prefer OUT OF SCOPE.

**Never:** Camera-center aim; cam recenter on place/remove; Terrain3D under craft; single cube for all masks; raw-cell-only visual authority.

## Ban

`verify_mcp_only` · `camera_center_aim` · `craft_cam_recenter_on_place` · `craft_terrain_blend` · `terrain3d_in_scope` · `terrain3d_leak_f5` · `inspiration_shape_miss` · `graybox_only_craft` · `raw_cell_only_visual` · `grammar_regress` · `biome_atlas_scope_creep`
