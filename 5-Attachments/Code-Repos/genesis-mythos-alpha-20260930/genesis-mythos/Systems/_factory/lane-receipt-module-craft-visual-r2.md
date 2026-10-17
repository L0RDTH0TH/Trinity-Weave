# Module lane receipt — alpha0_townscaper_craft_visual_r2

- **slice_id:** `alpha0_townscaper_craft_visual_r2`
- **ask_id:** `alpha0_townscaper_craft_visual`
- **bind:** `DualGridCraftHost.TryBuildAssetMeshLibrary` → `res://assets/craft/dual_grid/craft_dual_*.glb` source=`asset_adc`
- **lifts:** uniform `0` (shared foundation in ADC meshes — Townscaper craft-density coalesce)
- **visual_bar:** Visual-Factory-Direction-Stylized-Low-Poly
- **variants:** Empty/Full/Corner/Edge/Diagonal/InverseCorner ids 0–5 distinct
- **chrome:** craft HUD cleaned — no sparky / Terrain3D / raise-as-height active craft hints (`WorldgenCraftControls`, `GameHud` craft path)
- **preserve:** dual grammar, LMB/RMB under mouse, no cam yank, Terrain3D hard-disabled
- **procedural Make*Mesh:** fail-visible only (`procedural_fail_visible`)
- **depth:** `alpha0_townscaper_df_depth_r1` still blocked until operator F5 green
- **prefer seat:** `prefer_authorship_pass` — asset MeshLibrary not procedural Success
- **operator attest:** **F5 only** — ban `verify_mcp_only`
- **staging amend (2026-10-16):** post-GEN LMB place — `SetCellFill` primary path **always toggles** `FlipOrganicCorner` (refuse `want==cur` silent no-op). Sync `_genBiomeByVertex` after flip so hover tip leaves `Biome Water` when land commits; re-`UpdateFour` for tint. Factory log: Cell_Commit Ok without Corner_Flip on already-filled verts was the Water-tooltip no-op.
- **staging amend (2026-10-16 dual place/render honesty):** `ResolveOrganicDualVisualFamily` — owner ON → Full plate; owner OFF → Empty unless `IsTrueCoastlineBoundary` (neighbor-bit Corner/Edge spray closed — killed GEN trapezoid confetti). `ApplyGenTerrainPass` seeds every DualCell owner land/water then `RefreshAllDualSlots` → land Full / water Empty. Ghost = Stage-6 Full footprint (`MakeStage6FullFootprintGhost`). LMB toggle + biome sync KEEP.
- **staging amend (2026-10-16 SeatPolygon weld):** Ghost + place emit share `TrySeatPolygon(V)` (OwnedDualCell DualCorners n=3|4 only). Removed OccupancyCorners length early-return / Full_Force confetti. No seat → ghost hide + `place_refused`. `Cell_Commit Ok` only after seat mesh exists; Plains tip only when Full in slot. Coast gate KEEP.
- **staging amend (2026-10-16 LMB stamp-on):** Killed LMB toggle-off. `SetCellFill` non-Empty → SET `_cornerLogic[V]=true` + `PlaceStage6DualCellLibraryItem(..., Full)` on same `TrySeatPolygon` corners as `UpdateGhost` (idempotent add). Never Flip for LMB add; never gate Ok on `UpdateFour` count. Ok only when `SeatMeshPresent(seat.Key)`; else Failed + `place_refused`. RMB Empty clears seat. Plains tip only when Full in slot. Coast gate KEEP. `FlipOrganicCorner` returns ≥1 after successful bit write.
- **staging amend (2026-10-16 stamp persistence):** Root cause — Full/biome mats used `CullMode.Back` while DualCorners are CCW-from-+Y (ghost/highlight used Cull Disabled), so committed Fulls vanished after highlight restore / mouse leave while ghost still previewed. Fix: Cull Disabled on Full/biome/coast; `ClearDualSlot` refuses while owner ON; Empty resolve never wipes owner-ON seats; UpdateFour re-asserts Full on all owner-ON touching seats; ghost never aliased into `_dualSlots`; RestoreCream restores biome/Full tint (not null).
- **ROLLBACK RECOVERY (2026-10-16):** Place thrash stack above (toggle / Stage6-ghost / SeatPolygon / stamp-on / Cull persist / piggyback) **SUPERSEDED**. Surgical restore of `DualGridCraftHost.cs` + `OrganicDualOffsetLattice.cs` from Trinity **`2675d22`** (GEN-biomes tip — FlipOrganicCorner place). WorldgenCraft LMB log un-piggybacked. GEN/PACK/biomes kept. **No F5 pass · no place KEEP · no GREENLIGHT · no piggyback v2.** Piggyback receipt parked. Next Prefer: `alpha0_stalberg_dual_place_product_r1` (`PLACE-product`) — write only. See `Factory-DRB/slice-briefs/alpha0_place_thrash_rollback_r1.receipt.md`.
