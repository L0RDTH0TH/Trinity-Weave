---
title: Staging receipt — alpha0_stalberg_dual_terrain_tile_r1
slice_id: alpha0_stalberg_dual_terrain_tile_r1
ask_id: alpha0_stalberg_dual_visual
series_id: alpha0_stalberg_grid_kernel_r1
series_step: 2o
producer_run_id: sp-terrain-tile-r1-greenlight-weld
claim_class: staging
factory_greenlit: true
live_weld_greenlit: true
prefer_authorship_pass: ok
prefer_path: concept
concept_prefer_ok: true
success_object: dual_offset_terrain_tile
contract: C_dual_offset_terrain_tile_land_water_read
completed: 2026-10-04T21:38:24Z
status: greenlit_weld_live_staging_awaiting_f5
prior_slice_id: alpha0_stalberg_dual_mesh_fit_r1
supersedes_success: alpha0_stalberg_dual_art_style_r1
discrete_bind_cite: alpha0_stalberg_dual_visual_r3
prefer_harden: prefer_dual_terrain_tile_authorship_r1
gold_sixpack_evidence: 1-Projects/genesis-mythos-master/Factory-DRB/slice-briefs/_evidence/gold_dual_offset_terrain_tile_sixpack/
live_path: 5-Attachments/Code-Repos/genesis-mythos-alpha-20260930/genesis-mythos/
meshlibrary_path: assets/craft/dual_grid/
trinity_branch: project/genesis-mythos-master
trinity_project_sha: ae6f1c9c249c91ba83d61adb582d87e9b5fe8f30
trinity_main_sha: 5a0df6800bed01b143b14f643a48c821f7a31c78
trinity_push: direct_export_project_push
curator_snapshot: skipped_unsafe_mass_cursor_rules_deletes
---

# Staging receipt — alpha0_stalberg_dual_terrain_tile_r1

**GREENLIGHT WELD LIVE** landed. Prefer concept ok. Gold sixpack authored. LIVE cream/sage plinth MeshLibrary replaced with land/water terrain tiles. **claim_class: staging** until operator F5. **No ask_success** from MCP.

## Prefer concept (prior)

| Check | Evidence |
|-------|----------|
| Prefer | alpha0_stalberg_dual_terrain_tile_r1.prefer-result.json → ok · concept_prefer_ok: true |
| Harden | [[prefer_dual_terrain_tile_authorship_r1]] — cream packets Prefer-fail |

## LIVE weld

| Item | Note |
|------|------|
| GLB sixpack | assets/craft/dual_grid/craft_dual_Empty|Full|Edge|Corner|InverseCorner|Diagonal.glb (Blender MCP) |
| Gold stills | _evidence/gold_dual_offset_terrain_tile_sixpack/gold_*.png |
| Host | DualGridCraftHost.cs — SliceId terrain_tile_r1; sixpack enum; no cream MaterialOverride; Empty uses GLB mesh_fit; organic faces Visible=false |
| HUD | WorldgenCraft.cs — DUAL TERRAIN-TILE r1 |
| Keep | mesh_fit warp · Stage-6 · secondary glow · squarify · rings=5 spacing=210 |
| Refuse | cream_quarter Success · FaceCornersLocal-as-dual · gray_ramp/stretch |

## Operator F5 bar

1. Open res://scenes/WorldgenCraft.tscn, F5; dual overlay on (D).
2. Filled cluster reads as **terrain/ground** (moss/earth/stone/water) — not cream/sage plinths.
3. Name Empty vs Full vs Corner without debug overlay.
4. Cream underlay not the readable surface; organic faces receded.
5. Attest ask_success only when house bar met — MCP alone ≠ Success.

## Related

- Brief [[alpha0_stalberg_dual_terrain_tile_r1]] · Harden [[prefer_dual_terrain_tile_authorship_r1]] · Series [[alpha0_stalberg_grid_kernel_r1]]

## Trinity / Grok

| Branch | SHA |
|--------|-----|
| project/genesis-mythos-master | ae6f1c9c249c91ba83d61adb582d87e9b5fe8f30 |
| main | 5a0df6800bed01b143b14f643a48c821f7a31c78 (already up to date; Prefer harden prior sync) |

Direct export push (vault git.push_enabled left false). Curator snapshot **skipped** — vault dirty with unrelated mass `.cursor/rules` deletes (rsync --delete unsafe).
