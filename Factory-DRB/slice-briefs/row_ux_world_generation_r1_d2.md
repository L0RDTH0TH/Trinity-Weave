---
slice_id: row_ux_world_generation_r1_d2
catalog_row_id: ux_world_generation
catalog_row_ids:
  - ux_world_generation
package_id: pkg_world_shell
wave: alpha
fidelity: stub
dispatch_depth: 2
target_depth: 2
producer_run_id: sp-overnigh-1f9b7c
pillar_packet_hash: 73bf9c69a7c5f309
half_b_overlay: alpha0_worldgen_terrain3d_feed_r1
composed_at: 2026-10-01T21:08:41Z
---

# Slice Implementation Brief — DM can create (table can shape) a persistent living world

## 1. Product goal (UX)

**North star (L5):** Durable world container — DM creates initial form via wizard+preview (tone-aware shape families, cached/pre-existing assets); table can shape; players do not author the first world. Physical/settlement layers + monster-region tags; import/attach first-class; every world-hitting change is DM-retconnable. Multiple campaigns/casts attach to the same world.

**Child surface:** `ux_worldgen_gui` — propose → refine → preview → accept/regenerate.

**Dispatch depth L2 bar:** One honest vertical that proves the series contract without L3…L5 polish. This factory pass is further narrowed by Half-B Prefer overlay `alpha0_worldgen_terrain3d_feed_r1` (armed): craft/stamp must feed **Terrain3D** so Sparky inspects real Terrain3D terrain — not graybox GridMap/Multimesh alone.

**Upstream claims justifying this compose:**
- L5 moment inventory + contract clauses (`scopes/ux_world_generation/L5.md`)
- L2 depth slice (`scopes/ux_world_generation/L2.md`) — do not implement L3…L5 in this pass
- Execution pin Phase-2 primary — `WorldShellController` seat gates, preview→accept, Terrain3D via `ITerrainAuthority`
- Operator Prefer weld — `alpha0_worldgen_terrain3d_feed_r1` + `.armed.yaml` (catalog feed = this slice_id)

### UX bullets (stable ids)

- **UX-1:** Privileged world-author seats (`shared_table` / `dm_as_player` / `privileged_access`) can enter the worldgen craft surface (`WorldgenCraft` / `ux_worldgen_gui` path); wrong seat is refused visibly — never silent OK.
- **UX-2:** Craft/stamp yields durable, table-visible world residue: named stamp `stamp_oasis_desert` pushes height/region into **Terrain3D** so the Terrain3D mesh updates (Prefer-altitude stand-in for wizard+preview → accept durable container).
- **UX-3:** Players do not author the first world — player seat cannot accept/stamp/commit world-hitting writes.
- **UX-4:** Dual-grid Prefer locked — Terrain3D is height/world authority + GridMap (or stock grid) is craft-cell overlay; no second terrain/physics/voxel authority (`parallel_terrain_engine` / `graybox_only_world` = fail).
- **UX-5:** After stamp, `god_mode_sparky` is consumer-only inspect/fly over the Terrain3D mesh — Sparky does not author terrain; craft-cam authorship already landed in r1 and is not re-litigated here.

### Deferred above this Prefer (named — not wave-1 owned)

- L5 clause 4 import/attach first-class (Path B) — later depth
- Full settlement + monster-region tag matrices (thin physical honesty only via Terrain3D+GridMap)
- Multi-campaign/cast attach UX polish
- Full DM-retcon suite beyond stamp rewrite of Terrain3D data
- L3…L5 polish, ADC/TAC art, GUI chrome, chargen/seats/tricam

**Exit criteria (package `pkg_world_shell` / staging):** Operator F5 — place/stamp → Terrain3D updates → sparky flies that mesh; Matrix Dual-grid Prefer/Never quoted; `claim_class: staging`. Ban `verify_mcp_only`.

## 2. Shape lock (Conceptual)

Do not relitigate:

| Lock | Source |
|------|--------|
| Long-lived `WorldShellController` under Main→World; regenerate by swapping World children (not deleting `SceneTree.root`) | Phase-2 execution primary |
| Seat gate before accept/regenerate/import | L5 + JUNIOR WORK-ORDER paint |
| Preview residue ≠ durable world until accept | L5 wizard+preview moments |
| Terrain via `ITerrainAuthority` (Terrain3D); Gaea = map-data parallel only — not terrain authority | Phase-2 C# weave + Junior-Tech-Adapt |
| Dual-grid Prefer/Never (Terrain3D height + GridMap craft overlay) | Godot-Implementation-Decision-Matrix + Prefer overlay |
| LIVE write target | `5-Attachments/Code-Repos/genesis-mythos-alpha-20260930/genesis-mythos/` |
| Entry scene | `res://scenes/WorldgenCraft.tscn` (already exists from r1; update) |

Conceptual pin ref: `[[Phase-2-Procedural-Generation-and-World-Building-Roadmap-2026-06-26-0914]]` (packet `conceptual.body` empty — shape taken from execution paint + Prefer brief; flag if Architect needs conceptual body fill — not a pillar conflict for this Prefer).

## 3. Realization (Execution)

Crosswalk UX bullets → Phase-2 / Prefer acceptance (wave 1):

| UX id | Realization | Verify / done signal |
|-------|-------------|----------------------|
| UX-1 | Worldgen entry reachable; seat refuse on wrong context | Entry `WorldgenCraft.tscn`; wrong-seat refuse visible (shell-era seats may be waivable only if Prefer scope documents debt — do not waive Terrain3D proof) |
| UX-2 | `stamp_oasis_desert` → Terrain3D height/region data | Terrain3D mesh visibly updates after stamp |
| UX-3 | Author-seat gate on world-hitting stamp/accept | Player cannot commit first world |
| UX-4 | Terrain3D host under WorldgenCraft / DualGridCraftHost; ClassDB Prefer path | Quote Matrix Dual-grid Prefer/Never; no Multimesh-only Success |
| UX-5 | Sparky inspect/fly over Terrain3D mesh only | Consumer-only; not terrain author |

Execution pin excerpt (junior still open — lanes close Prefer subset):

- Verify Terrain3D via `ITerrainAuthority` import/splat path (Junior-Tech-Adapt §1)
- Verify module compiles on Godot 4.6.3 .NET/C# — no GDScript-only Autoload theater for this leaf
- Full `WorldShellController` Unauthorized leaf-true remains open debt if Prefer does not touch shell API this wave — cite debt; do not claim shell AC closed

## 4. Cell roster

| Lane | Role this Prefer | Owns |
|------|------------------|------|
| `module` | Wave 1 — Terrain3D host, stamp→Terrain3D, Sparky consume | UX-1…UX-5 |
| `presentation` | Deferred — only if `project.godot` plugin/main_scene touch required | (none unless un-deferred) |
| `asset` / `techart` | Skip — Terrain3D vendored; no ADC/TAC pass | — |

Wave 1 is **serial module-only** (`parallel: false`). Harness stages PQ from CDP — Producer does not append PQ.
