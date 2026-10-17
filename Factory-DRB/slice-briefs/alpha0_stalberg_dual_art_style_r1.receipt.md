---
title: Staging receipt — alpha0_stalberg_dual_art_style_r1
slice_id: alpha0_stalberg_dual_art_style_r1
ask_id: alpha0_stalberg_dual_visual
series_id: alpha0_stalberg_grid_kernel_r1
series_step: 2n
producer_run_id: sp-art-style-r1-manual-greenlight
claim_class: staging
factory_greenlit: true
prefer_authorship_pass: ok
prefer_path: concept
concept_prefer_ok: true
success_object: dual_offset_cells
contract: C_cream_quarter_platform_art_style_on_mesh_fit
completed: 2026-10-04T20:03:34Z
status: staging_prefer_ok_awaiting_operator_f5
prior_slice_id: alpha0_stalberg_dual_mesh_fit_r1
keeps_geometry: alpha0_stalberg_dual_stage6_cell_r1
kernel_foundation: alpha0_stalberg_topology_base_r1
trinity_push: skipped_push_disabled
trinity_push_note: "curator_snapshot local commit only (git.push_enabled false)"
density_lift: live_rings_5_spacing_210
art_style: cream_quarter_platform_yt_Y19Mw5YsgjI
camera_separate_live: CraftPlanarCamRig_pitch_35_55
meshlibrary_path: assets/craft/dual_grid/
live_path: 5-Attachments/Code-Repos/genesis-mythos-alpha-20260930/genesis-mythos/
---

# Staging receipt — `alpha0_stalberg_dual_art_style_r1`

**claim_class: staging** until operator F5. Prefer **concept** ok. Cream quarter-platform restyle on mesh_fit sectors. Craft-cam pitch tilt shipped as **separate LIVE** (not Prefer Success). Curator **local** only (`git.push_enabled: false`).

## Prefer concept

| Check | Evidence |
|-------|----------|
| Prefer | `alpha0_stalberg_dual_art_style_r1.prefer-result.json` → ok · `concept_prefer_ok: true` |
| Bind | `.technical/weave/factory/genesis-mythos-master/alpha0_stalberg_dual_art_style_r1/implicit-intent-bind.json` |
| LIVE compile | `dotnet build` GenesisMythos.csproj — succeeded |

## LIVE weld (style)

| Item | Note |
|------|------|
| MeshLibrary GLBs | Blender cream restyle → `assets/craft/dual_grid/craft_dual_{Empty,Edge,Corner,Full}.glb` |
| Host materials | `MakeCreamQuarterPlatformMaterial` + yLift 0.22; shared cream + soft under-glow emission |
| Craft plane / env | Teal water face tint + orange grid; sky/ambient tint in `WorldgenCraft.BuildEnvironment` |
| Mesh fit KEEP | Bilinear warp to `SmallCornerQuad.Corners` untouched in method |
| Cam (separate) | `CraftPlanarCamRig` PitchDegrees −45° band −55…−35; height from pitch |

## Evidence

- `_evidence/yt_Y19Mw5YsgjI_operator_cream_quarters.jpg`
- `_evidence/townscaper_product_orbit_ref.jpg`
- `_evidence/yt_Y19Mw5YsgjI_t*.jpg` (YT stills)
- Cam note: `alpha0_stalberg_craft_cam_pitch_tilt_live.md`

## Operator F5

1. F5 `WorldgenCraft.tscn` — tilted cam (~45°), cream quarters on secondary slots over teal water.
2. Families still silhouette-distinct; Stage-6 + secondary glow + rings=5/spacing=210.
3. MCP alone ≠ Success.
