---
title: Camera mode taxonomy (live)
created: 2026-10-01
updated: 2026-10-01
project-id: genesis-mythos-master
claim_class: staging
factory_greenlit: false
status: active_pointer
---

# Camera mode taxonomy (live)

**`claim_class: staging`.** `factory_greenlit: false`.

Promoted live from archived horizon interaction map so agents do **not** only find this in `4-Archives/`. Locked also in [[FEEDSTOCK-SHAPE]] §4 — all three **included and functional**; conflating modes = honesty miss.

| `camera_mode_id` | Feel | Not |
|------------------|------|-----|
| `anchored_actor` | Body-bound (FP player / NPC / monster sensorium) | Free soar or classic VTT plane |
| `vtt_planar_ortho` | Classic VTT: **2D planar locked**, slight angle, **180° rotation about a central point** | Sparky god mode; actor-anchored |
| `god_mode_sparky` | Free / sparky mastery DM cam (WorldCam-family) | Planar ortho VTT; body-anchored |

**Authority:** Hosts **select** cameras; they do not own locomotion. Prefer/Never: [[Godot-Implementation-Decision-Matrix]] (seat camera swap = `Camera3D.Current` only).

**Active craft-chain cam (pointer only):** Townscaper dual-grid authorship uses `vtt_planar_ortho` (or craft envelope — planar locked, slight angle, 180° about center). See [[alpha0_townscaper_craft_core_r1]] · [[Townscaper-Dual-Grid-Craft-Grammar-Y19Mw5YsgjI]]. `god_mode_sparky` / Terrain3D inspect handoff is **deferred** this round (not armed on craft path). Legacy: [[alpha0_worldgen_dualgrid_sparky_r1]].

### Craft-phase bindings (worldgen weld)

Under craft cam (`vtt_planar_ortho` / craft envelope) for [[alpha0_townscaper_craft_core_r1]]:

| Binding | Craft phase | Deferred later |
|---------|-------------|----------------|
| Planar lock | **On** (locked craft plane) | Sparky free soar (later Prefer) |
| Orbit about focus | **≤180°** about craft focus | Sparky inspect/fly |
| WASD (or equiv) | **Pan on the craft plane** | Sparky move bindings |
| Primary action | **Place/remove dual-grid point** (mouse-aim; four dual cells refresh) | Not Terrain3D height paint |
| Sparky / Terrain3D bindings | **Off / hard-disabled on craft path** | Later ticket after DF-depth |

Refuse: craft phase using sparky free soar; free-orbit authorship; camera-center aim; Terrain3D leak under F5 → `inspiration_shape_miss` / `terrain3d_leak_f5` / camera conflation.

**Inspiration peers:** Fantasy Grounds / TaleSpire (ortho VTT) · BG3 / stock FPS (anchored) · Halo Forge validity for cam ownership — focus-scoped per weld.

## Related

- [[FEEDSTOCK-SHAPE]] · [[Ask-Fidelity-Exemplars]] · [[Half-B-Weld-Brief-Template]] · [[alpha0_townscaper_craft_core_r1]] · [[Townscaper-Dual-Grid-Craft-Grammar-Y19Mw5YsgjI]]
