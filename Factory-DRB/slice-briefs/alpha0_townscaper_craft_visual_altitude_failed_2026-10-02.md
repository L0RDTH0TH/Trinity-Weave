---
title: Archive receipt — craft Prefer altitude failed (metrics_only / failed_altitude)
created: 2026-10-02T19:21:45Z
updated: 2026-10-02T19:35:00Z
project-id: genesis-mythos-master
claim_class: staging
status: archived_failed_altitude
disposition: failed_altitude_metrics_only
failed_ask_ids:
  - alpha0_townscaper_craft_visual
  - alpha0_townscaper_craft_core
failed_slices:
  - alpha0_townscaper_craft_visual_r1
  - alpha0_townscaper_craft_visual_r2
  - alpha0_townscaper_craft_core_r1
disposition_note: do_not_prefer_again_for_art_reskin__do_not_audit_craft_core_as_tutorial_s1_success
superseded_by_series: alpha0_townscaper_tutorial_r1
active_slice: alpha0_townscaper_tutorial_s1_occupancy_r1
---

# Archive receipt — craft Prefer altitude failed

| Field | Value |
|-------|--------|
| **timestamp** | `2026-10-02T19:35:00Z` (reset) |
| **disposition** | **`failed_altitude` / `metrics_only`** — **not** Success |
| **operator reset** | START FROM THE BEGINNING — do **not** audit `craft_core` as green; tutorial step 1 = occupancy-only weld |

## Failed / archived Prefer targets (keep files for history)

| Slice | Ask | Why archived |
|-------|-----|----------------|
| [[alpha0_townscaper_craft_visual_r1]] | `alpha0_townscaper_craft_visual` | Metrics-only art / dual MeshLibrary Prefer — visually identical / scatter read |
| [[alpha0_townscaper_craft_visual_r2]] | `alpha0_townscaper_craft_visual` | Same altitude; asset bind still metrics-only |
| [[alpha0_townscaper_craft_core_r1]] | `alpha0_townscaper_craft_core` | Bundled dual MeshLibrary / connector Success claims ahead of tutorial ladder — **reset**; occupancy paint alone may remain on disk but is **not** attested as ladder step-1 Success |

Fused dual+art Prefer claims (craft_core → visual r1/r2 chain treated as one altitude) = **`failed_altitude_metrics_only`**.

## What stays on disk

- LIVE Code-Repos craft host / assets / MeshLibrary drops — reference / salvage only.
- Briefs + armed YAML packets — history; **disarmed**; Half-B active pointer must **not** target them.

## What is forbidden next

- Prefer art re-skin / MeshLibrary Success before tutorial mass steps.
- Treating craft_core Prefer-land or s1_attest as tutorial step-1 Success.
- Opening [[alpha0_townscaper_df_depth_r1]] until ladder clears.
- Bundling steps 2–5 / jumping to art.

## Next altitude (active)

Series [[alpha0_townscaper_tutorial_r1]] → **only** [[alpha0_townscaper_tutorial_s1_occupancy_r1]] greenlit + WELD now. Steps 2–6 draft only. Awaiting operator **F5** before step 2.
