---
title: Staging receipt — alpha0_stalberg_dual_secondary_glow_center_r1
slice_id: alpha0_stalberg_dual_secondary_glow_center_r1
ask_id: alpha0_stalberg_dual_secondary_glow_center
series_id: alpha0_stalberg_grid_kernel_r1
series_step: 2k
producer_run_id: sp-dsgc1-manual-greenlight
claim_class: staging
factory_greenlit: true
prefer_authorship_pass: ok
prefer_path: concept
concept_prefer_ok: true
success_object: dual_offset_cells
geometric_success: secondary_glow_center_keep_stage6_wire_small_corner_units
contract: C_secondary_glow_center_keep_stage6_wire_small_corner_units
intent_invariant: "Stage-6 DualCell identity (OwnedDualCellKeys=one; dual verts=face centroids; dual edges centroid–centroid) remains lattice wire/topology; pick/glow/populate centers on the secondary grid — nearest face-centroid dual vert — via SmallCornerQuadsAroundFace(F) (typically 4 pie sectors meeting at the coral/cyan secondary locus); SmallCornerQuadsAround(V) primary-star is not Prefer Success; Stage-6 wire kept; refuse primary_star_glow_as_success / primary_face_as_dual / stage6_union_as_single_glow_tile."
completed: 2026-10-04T07:15:00Z
status: staging_prefer_ok_awaiting_operator_f5
prior_slice_id: alpha0_stalberg_dual_glow_neighborhood_r1
keeps_geometry: alpha0_stalberg_dual_stage6_cell_r1
logic_prior_slice_id: alpha0_stalberg_primal_graph_r1
kernel_foundation: alpha0_stalberg_topology_base_r1
trinity_branch: project/genesis-mythos-master
trinity_push: skipped_push_disabled
trinity_push_note: "project_bridge_push skipped reason=push_disabled (branch=project/genesis-mythos-master); curator_snapshot local commit only (git.push_enabled false)"
density_lift: deferred_until_pipeline_ask_success
dual_visual_ask_success: paused_until_secondary_glow_center_concept_and_operator_f5
goal_image: Ingest/Final-grid-state.jpg
annotate_proof: Ingest/Screenshot from 2026-10-04 01-19-00.png
bug_image: Ingest/Screenshot from 2026-10-04 01-19-00.png
live_path: 5-Attachments/Code-Repos/genesis-mythos-alpha-20260930/genesis-mythos/
dual_report_a: Factory-DRB/slice-briefs/alpha0_stalberg_dual_secondary_glow_center_r1.dual-report-a.md
dual_report_b: Factory-DRB/slice-briefs/alpha0_stalberg_dual_secondary_glow_center_r1.dual-report-b.md
mcp_evidence_a: Factory-DRB/slice-briefs/_evidence/dual_secondary_glow_center_r1_verify_a.png
mcp_evidence_b: Factory-DRB/slice-briefs/_evidence/dual_secondary_glow_center_r1_verify_b.png
mcp_note: "MCPRuntime Stable_Neighborhood_Ready stable_secondary_glow_center secondary_faces=48 sec4=48 glow_mode=secondary_face_center primary_star_glow_as_success=false; Secondary_Flip face=8 small_count=4 keys sc_v*_f8"
---

# Staging receipt — `alpha0_stalberg_dual_secondary_glow_center_r1`

**claim_class: staging** until operator F5. Prefer **concept** ok (`dual_offset_cells` + secondary-centered glow invariant). Stage-6 geometry + small-corner-quad units **kept**. Dual-visual / MeshLibrary models remain **out**. Curator snapshot per operator GREENLIGHT WELD.

## Conceptual leg

| Field | Value |
|-------|--------|
| Project end-state | Authorable irregular dual-grid craft plane on organic all-quad board |
| Path | glow_neighborhood small-corner units kept → **this** secondary glow center → dual_visual_r3 |
| Intent invariant | Pick/glow center on secondary face centroid via `SmallCornerQuadsAroundFace` |
| `success_object` | `dual_offset_cells` |
| Contract | **(C)** secondary glow center; keep Stage-6 wire + small-corner units |

## Prefer concept

| Check | Evidence |
|-------|----------|
| Prefer | `alpha0_stalberg_dual_secondary_glow_center_r1.prefer-result.json` → ok · `concept_prefer_ok: true` · `prefer_path: concept` |
| Bind | `.technical/weave/factory/genesis-mythos-master/alpha0_stalberg_dual_secondary_glow_center_r1/implicit-intent-bind.json` |
| Compose | Slice Producer judgment `sp-dsgc1-manual-greenlight` |
| LIVE compile | `dotnet build` GenesisMythos.csproj — **0 errors** |

## LIVE weld (secondary glow center)

| Check | Evidence |
|-------|----------|
| Pick | `TryPickOrganicSecondary` → nearest editable face centroid (Y=2 encoder) |
| Glow | `HighlightSecondaryDualCells` → `SmallCornerQuadsAroundFace(F)` |
| UpdateFour | Y=2 refreshes face-incident small corner quads |
| Stage-6 wire | centroid–centroid **kept** (DualLatticeDebug) |
| Refuse | `primary_star_glow_as_success=false` in prove + flip logs |
| Host | `WeldSliceId=alpha0_stalberg_dual_secondary_glow_center_r1`; HUD **SEC-GLOW r1** |
| Preserved | MeshGraph · organic underlay · craft authority · craft cam 7× / zoom · DualLatticeDebug spheres · Terrain3D OFF |

## Before → after pick/glow

| | Before (glow_neighborhood_r1) | After (this Prefer) |
|--|-------------------------------|---------------------|
| Pick | nearest **primary** V (`TryPickOrganicCorner`) | nearest **secondary** face centroid |
| Glow set | `SmallCornerQuadsAround(V)` star from amber | `SmallCornerQuadsAroundFace(F)` pie at coral/cyan |
| Visual center | orange primary vertex | secondary dual vert |
| Stage-6 wire | kept | **kept** |
| Small-corner units | kept | **kept** |

## F5 attest (operator)

1. Open `res://scenes/WorldgenCraft.tscn`, F5 / play.
2. Click near a coral/cyan secondary point → glow centers there.
3. Confirm not a star locked to amber primary V.
4. Cyan crosses amber; spheres at face centres; HUD `SEC-GLOW r1`.
5. Craft cam 7× / zoom / DualLatticeDebug intact.

## Out of scope

MeshLibrary dual_visual / models · density lift · Terrain3D · Hex19 Success · chain-advance without operator F5
