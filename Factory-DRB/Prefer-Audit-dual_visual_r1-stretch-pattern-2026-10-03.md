---
title: Prefer audit — dual_visual_r1 stretch-as-shape failure pattern
created: 2026-10-03
updated: 2026-10-03
project-id: genesis-mythos-master
status: active
slice_id: alpha0_stalberg_dual_visual_r1
verdict: failure_pattern
altitude: failed_altitude_partial_visual_fidelity
tags: [prefer, audit, dual-visual, stretch_as_variant, over_neighbor_paint]
---

# Prefer audit — `alpha0_stalberg_dual_visual_r1` (stretch pattern)

## Verdict

**Failure pattern** (not a one-off glitch). Prefer passed; product dual grammar failed altitude visual fidelity.

Do **not** greenlight `dual_visual_r1` as product Success — mark **partial / failed_altitude**.

## What F5 / Grok saw

- One logic fill lights ~3 neighbor dual cells (neighborhood readable, but silhouette wrong).
- N/S fill → N/S elongation; E/W → E/W stretch — not discrete empty / edge / corner / full.
- N+E defaults to E/W bar look (stretch orientation), not L-corner silhouette.
- Organic underlay OK; craft-plane authority OK.

## Root cause (weave / Prefer)

1. **Ticket gap:** `done_when` allowed “approved shape-distinct graybox stand-ins” without forbidding **stretch-into-face** or requiring **discrete MeshLibrary item placement**.
2. **Half-B implementation:** `MakeShapeDistinctDualVariant` warped family walls onto `FaceCornersLocal` — irregular organic aspect became elongation. That satisfied “geometry differs” AABB heuristics without Townscaper silhouettes.
3. **Prefer gap:** scanners checked symbol presence (`MakeShapeDistinctDualVariant`, four families, prove AABB on **unit** MeshLibrary prototypes) + absence of `DualFamilyColor` ramp. No scanners for:
   - `stretch_as_variant` (face-warp / non-uniform Scale)
   - `over_neighbor_paint` (cardinality gate ≤4 dual cells per logic flip)
   - discrete `GetItemMesh` / place path
4. **Neighborhood:** `UpdateFourDualSlots` incident-face foreach was correct in spirit but **uncapped** and Prefer did not require `MaxDualCellsPerLogicFlip` / prove gate — over-broad paint could pass silently.

## Classification table

| Hypothesis | Verdict |
|------------|---------|
| One-off mesh instance bug | Rejected — systematic stretch along face axes |
| Wrong vertex→face index | Secondary — valence usually ≤4; visual failure is silhouette |
| Ticket + Prefer under-spec | **Accepted** — pattern defense required |

## Harden (done this pass)

- Refuse codes (do_not_waive): `stretch_as_variant`, `over_neighbor_paint` (+ keep `gray_ramp_only`, `inspiration_shape_miss`)
- Scanners in `prefer_authorship_contract.py` (`DUAL_VISUAL_DO_NOT_WAIVE`)
- Host law cites: [[Prefer-Authorship-Host-Law]] § C.1 · [[Grid-Topology-Host-Law]] dual silhouette/cardinality
- Next ticket: [[alpha0_stalberg_dual_visual_r2]] — discrete variants + cardinality; Prefer must fail r1 LIVE and pass r2

## Related

- Slice [[alpha0_stalberg_dual_visual_r1]] · Series [[alpha0_stalberg_grid_kernel_r1]]
- Harness: `scripts/eat_queue_core/weave/factory/prefer_authorship_contract.py`
