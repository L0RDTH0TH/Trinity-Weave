---
title: Weld receipt — alpha0_townscaper_tutorial_s2_dual_offset_r1 (attempt 2)
slice_id: alpha0_townscaper_tutorial_s2_dual_offset_r1
ask_id: alpha0_townscaper_tutorial
series_id: alpha0_townscaper_tutorial_r1
created: 2026-10-03T05:57:44Z
claim_class: staging
ask_success: false
factory_greenlit: true
status: staging_awaiting_operator_f5
lane: module
curator: forbidden
law: dual_half_offset_quads_update_four_toggle
attempt: 2
producer_run_id: sp-s2dual2-35fcaa
superseded_producer_run_id: sp-s2dual-a-eb9041
queue_entry_id: factory-s2d2-aa9a72-module
keep_s1: true
f5_pending_on: update_four_unique_dual_offset_and_dual_toggle
---

# Weld receipt — tutorial s2 dual offset attempt 2 (**STAGING**)

Operator retry: attempt 1 was markers-only / visually like s1. Attempt 2 rewrites dual as **unique half-offset quads** with **DualCellsTouching update-four** + Prefer dual LIVE seat. **Not Success** — operator **F5** only.

| Field | Value |
|-------|--------|
| `ask_id` | `alpha0_townscaper_tutorial` |
| `slice_id` | `alpha0_townscaper_tutorial_s2_dual_offset_r1` |
| `producer_run_id` | `sp-s2dual2-35fcaa` |
| Supersedes | `sp-s2dual-a-eb9041` (attempt 1) |
| Queue entry | `factory-s2d2-aa9a72-module` |
| Lane | `module` **only** — s3–s6 not opened |
| LIVE write target | `5-Attachments/Code-Repos/genesis-mythos-alpha-20260930/genesis-mythos/` |
| Build | `dotnet build` — **0 errors** |
| Prefer | `prefer_authorship_pass_ok` — violations `[]`; dual_offset LIVE green |
| `claim_class` | **`staging`** — awaiting operator F5 |
| Curator | **not run** (hard forbid) |

## What made attempt 2 different from s1 / attempt 1

| | s1 | attempt 1 (failed altitude) | attempt 2 (this weld) |
|--|----|-----------------------------|------------------------|
| Dual cells | none | 19×4 overlapping offset markers | **~30 unique** dual quads (union of update-four) |
| Corner reads | n/a | NearestInLattice ±0.25 → often 1 cell | **Explicit** CornerAxialOffsets (q,r)/(q+1,r)/(q,r+1)/(q+1,r+1) |
| Update-four | n/a | DualSlotsAround spray refresh | **DualCellsTouching** → exactly 4 dual origins |
| Visual | lattice only | tiny plates near centres (read as s1) | Quads **span four occupancy corners** (inset); TileFamilyIndex 0–5 height |
| Prefer | topology edges+faces | greens on s1 topology alone | **skip_dual_offset** LIVE seat requires update-four + corners + half-offset + dual toggle |

## Prefer evidence (post-weld)

| Axis | Result |
|------|--------|
| `has_edges` / `has_faces_or_cells` | **true** / **true** |
| `points_only` / `missing_axes` | **false** / **[]** |
| dual `has_update_four` | **true** (`DualCellsTouching` + `UpdateFourDualSlots`) |
| dual `has_corner_reads` | **true** |
| dual `has_half_offset` | **true** |
| dual `has_dual_toggle` | **true** |
| dual `markers_only` | **false** |
| violations | **`[]`** |

## LIVE files

| File | Change |
|------|--------|
| `Core/WorldGen/Hex19DualOffsetLattice.cs` | Rewritten — DualCell, DualCellsTouching, TileFamilyIndex, IsHalfStepOffset |
| `Systems/DualGridCraftHost.cs` | Unique dual overlay; MakeDualCornerQuad; Prove refuses 19×4 spray |
| `prefer_authorship_contract.py` | s2 dual LIVE heuristics + `skip_dual_offset` non-waive |

## Operator F5 bar (Success gate)

1. **Update-four:** Paint/clear one hex-19 cell → **exactly four** dual quads that share that site refresh (family/height change) — not a global flash, not invisible.
2. **Half-offset quads:** Dual plates sit **between** occupancy centres and span four corners (readable vs lattice faces).
3. **Dual toggle:** **D** hides/shows dual independently of **G**; Shift+G paired OK.
4. **≠ s1:** With dual visible, scene must not read as occupancy-only; with dual hidden, s1 lattice/ghost/paint still work.
5. No Terrain3D / connectors / art; graybox OK.

## Explicit wait

**`claim_class: staging`.** Prefer green ≠ Success. Only operator F5 closes s2. Do not open s3–s6. Curator **not run**.

## Cross-links

- Brief [[alpha0_townscaper_tutorial_s2_dual_offset_r1]] · armed packet sibling
- Keep [[alpha0_townscaper_tutorial_s1_occupancy_r1]] · series [[alpha0_townscaper_tutorial_r1]]
- Grammar [[Townscaper-Dual-Grid-Craft-Grammar-Y19Mw5YsgjI]] · oskar docs/03 reference only
