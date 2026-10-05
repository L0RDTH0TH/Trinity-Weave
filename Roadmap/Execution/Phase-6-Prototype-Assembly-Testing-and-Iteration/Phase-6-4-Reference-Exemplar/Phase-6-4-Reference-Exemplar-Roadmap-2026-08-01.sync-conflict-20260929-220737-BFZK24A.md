---
title: Phase 6.4 — Reference Exemplar (Execution)
roadmap-level: secondary
phase-number: 6
subphase-index: "6.4"
project-id: genesis-mythos-master
roadmap_track: execution
conceptual_counterpart: '[[1-Projects/genesis-mythos-master/Roadmap/Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-4-Reference-Exemplar/Phase-6-4-Reference-Exemplar-Roadmap-2026-08-01]]'
status: active
deepen_complete: true
paint_ux_catalog: true
paint_status: woven
paint_campaign_id: exec-weave-stack-ux-20260929
package_id: pkg_world_shell
catalog_row_ids:
- ux_living_world_continuity
priority: high
progress: 68
handoff_readiness: 78
product_factory_run_id: overnight-exec-20260928
persona_id: half_a.execution_tech_lead
created: 2026-09-29
updated: 2026-09-29
tags:
- paint_ux_catalog
- pkg_world_shell
- roadmap
- genesis-mythos-master
- phase-6
- reference-exemplar
- dual-track
- execution
para-type: Project
links:
- '[[1-Projects/genesis-mythos-master/Roadmap/User-Story/scopes/ux_living_world_continuity/L5]]'
- '[[ux_living_world_continuity]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-4-Reference-Exemplar/Phase-6-4-Reference-Exemplar-Roadmap-2026-08-01]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-Prototype-Assembly-Testing-and-Iteration-Roadmap-2026-06-26-0914]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-1-Factory-Phase-0-Presentation-Shell/Phase-6-1-Factory-Phase-0-Presentation-Shell-Roadmap-2026-06-26-1912]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-2-Horizon-Demo-V1-Gameplay-Loop/Phase-6-2-Horizon-Demo-V1-Gameplay-Loop-Roadmap-2026-06-26-1951]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-3-Factory-vs-Demo-Track-Boundary-Glue/Phase-6-3-Factory-vs-Demo-Track-Boundary-Glue-Roadmap-2026-06-26-2031]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-2-Procedural-Generation-and-World-Building/Phase-2-Procedural-Generation-and-World-Building-Roadmap-2026-06-26-0914]]'
- '[[Ingest/Agent-Research/godot-worldshell-node-scenetree-citations-gmm-2026-09-29-0126]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Docs/SeamRegistry-CSharp-Host-Index]]'
- '[[1-Projects/genesis-mythos-master/Roadmap/Execution/Docs/Junior-Tech-Adapt-How-To]]'
weave_pass: exec-weave-stack-ux-20260929
---
# Phase 6.4 — Reference Exemplar (Execution)

Execution secondary: **ReferenceExemplarManifest** + **CampaignCapableDoDGate** + **ExemplarPackDefaultFiller** + **SwapMatrixSlotBinder** + **AuthorityPackageContract** (player cosmetics vs DM world). Third delivery track — not factory attestation, not 6.2 demo. Parallel spine under `Execution/Phase-6-…/Phase-6-4-…/`. **No Half B.** L5/SERIES advisory — Reference Exemplar is campaign-capable default fill with seat/agency DoD; not player world-author invent. **Paint spine terminal for Phase-6.**

### Intent Mapping

| Field | Value |
|-------|--------|
| Design intent | Medium Fantasy Reference Exemplar as campaign-capable default fill ([[conceptual 6.4]]) |
| Inspiration / L5 bar (advisory) | Reference Exemplar as campaign-capable default; DM retcon fill; seats respected |
| Inspiration (studied) | (1) Conceptual 6.4. (2) Execution 6.1 shell / 6.2 demo / 6.3 glue. (3) Phase-2 gen pipeline contracts. (4) Charter swap matrix |
| L5 / package crosswalk | phase-aligned `[[ux_living_world_continuity]]` / `pkg_world_shell` — seats + FP≠DM rail |
| Execution mechanism | RefCounted manifest + DoD gate; binds into 6.1 PlayRegionHost via 6.3 MountContractGlue ids |
| Validation | Catalog paint DoD met |

### ux_context crosswalk

| Envelope key | This run |
|--------------|----------|
| `catalog_row_ids` | `ux_living_world_continuity` |
| `package_id` | `pkg_world_shell` |
| `l5_path` | `Roadmap/User-Story/scopes/ux_living_world_continuity/L5.md` (read-only) |
| `conceptual_pin` | Frozen conceptual 6.4 |
| `dispatch_scope` | Execution secondary **6.4** mint (FAST wave) |

## Child links (conceptual twins → execution mint targets)

| Index | Conceptual twin | Execution status |
|-------|-----------------|------------------|
| _(none)_ | 6.4 is a roadmap leaf (no tertiary tree) | **n/a** — DFS continues at 6.1.1 |

## UX Catalog paint

| Field | Value (from SERIES / L5 — read-only; **phase-aligned**) |
|-------|-----------------------------------------------|
| `row_id` | `ux_living_world_continuity` |
| Label | World can move off-screen and show lasting readable costs |
| Seats | `shared_table`, `dm_as_player` |
| Envelope enablement | Phase-true moments → `Genesis.Exemplar.ReferenceExemplarGate` on Godot **4.6.3 .NET / C#** |
| `does_not_mandate` | world motion requires scripted companion betrayal; lasting costs only cosmic death pacts; one conspiracy skin; players get full sim-admin tools; this row owns quiet-between |
| Pin color keys | Living Amber · Rail Violet · Stack Teal |

### Moment → module map (junior)

| L5 moment / clause | Module / API | Guard | Residue |
|--------------------|--------------|-------|---------|
| `ux_sim_weather_pulse` | `slot.sim.weather` → `IWeatherModule` (3.1.2) | wrong seat / unpublished seam | WorldEventLog weather row |
| `ux_wa_faction_offscreen` | `slot.sim.faction` → FactionGraph (3.1.4) | player cannot author faction | off-screen edge + readable cost |
| `ux_wa_npc_agenda` | `ISimTickHost` + NPC agendas (3.1.3) via sim tick receipt | observe-only refuse write | agenda delta in log |
| `ux_canon_pipeline_feel` | `slot.gen.pipeline` → StageDAG + CanonCommitBoundary | CompletenessGate fail | seed-replay WorldMapData hash |

## Tech stack weave

| Manifest `id` | Contract | Junior path |
|---------------|----------|-------------|
| `stack-ui-hosts` | `IUiHost` / HUDLayerStack | `slot.ui.hosts` → 6.1 |
| `stack-procedural-terrain` | `ITerrainAuthority` | `slot.gen.terrain` · [[Docs/Junior-Tech-Adapt-How-To]] §1 |
| `stack-procedural-maps-gaea-parallel` | `IMapGenAuthority` → WorldMapData | `slot.gen.maps_parallel` · how-to §2 |
| `stack-rules-engine` | `IRulesPluginHost` + DiceRoller | `slot.rules.plugin` · how-to §3–4 |
| `stack-ci-gdunit4net` | gdUnit4Net | receipt happy/refuse tests |
| `engine-godot-463-dotnet` | Godot 4.6.3 .NET | game repo C# |

## Module map

| Module | Responsibility | Owner |
|--------|----------------|-------|
| `ReferenceExemplarManifest` | scope_id, pack defaults, track id `reference_exemplar`, module_bind table | 6.4 |
| `CampaignCapableDoDGate` | Fail closed unless **checkable receipts** present (graybox OK) | 6.4 |
| `ExemplarPackDefaultFiller` | Medium Fantasy chrome+world fill from pack_defaults | 6.4 |
| `SwapMatrixSlotBinder` | Bind Phase 1–5 hosts into swap slots until DM swaps | 6.4 |
| `AuthorityPackageContract` | Player cosmetics vs DM world package | 6.4 |

## Exemplar assembly map (1–5 → Manifest / swap slots)

**Bind recipe:** SessionComposer (1.1) publishes seams → CompletenessGate (1.3) → pack filler mounts into PlayRegionHost (6.1) via MountContractGlue (6.3). Demo track (6.2) may share hosts but **must not** satisfy Exemplar DoD with stub-only receipts.

### Junior assembly checklist (graybox OK — assembled prototype path)

**PMG end-state:** Medium Fantasy Reference Exemplar is the **assembled campaign-capable prototype** (not Horizon demo proof). Junior boots graybox Exemplar when every step below has a receipt; Half B game polish is out of scope.

Execute in order. Each step writes one receipt row into `ReceiptLedger` (`status: ok|graybox_ok|deferred` + `verify` string). Fail closed on `stub_only`.

| Step | Action (junior) | Host / artifact | Receipt id | Pass criterion |
|------|-----------------|-----------------|------------|----------------|
| 0 | Open Host Index + How-To | [[Docs/SeamRegistry-CSharp-Host-Index]] · [[Docs/Junior-Tech-Adapt-How-To]] | _(prep)_ | Index wins on signatures |
| 1 | SessionComposer publish 9 required seams | `ISeamRegistry` / CompletenessGate (1.3) | `R.seam.completeness` | `CompletenessGate.Check == Ok` |
| 2 | Bind gen pipeline → WorldMapData | `IMapGenAuthority` + StageDAG (2) | `R.gen.worldmap_hash` | seed replay hash match (flat RF OK) |
| 3 | Admit terrain height+splat | `ITerrainAuthority` (Terrain3D) How-To §1 | `R.gen.terrain_admit` | ImportHeightmap + ApplySplat Ok; Gaea **not** terrain |
| 4 | One living sim tick + log | `ISimTickHost` (+ weather/faction ports) | `R.sim.tick_once` | ≤1 tick + WorldEventLog row |
| 5 | Mount FP + DM cams; refuse wrong seat | `ICameraRig` 4.1 / 4.2 | `R.cam.fp_dm_split` | both mount; player→DM WorldCam = Unauthorized |
| 6 | Agency envelope assert | AgencyEnvelope / PilotHandoff (4.3) | `R.agency.envelope` | wrong seat → Unauthorized |
| 7 | Bind PF1 plugin | `IRulesPluginHost` + `IDiceRoller` How-To §3–4 | `R.rules.pf1_bind` | ActiveRuleset=`pathfinder_pf1`; Roll→IDiceRoller |
| 8 | Mount PlayRegion + HUD | `PlayRegionHost` / `IUiHost` (6.1) via 6.3 glue | `R.shell.mount` | mount_id resolves; DevLeakageGuard pass |
| 9 | Authority packages | AuthorityPackageContract | `R.authority.packages` | player pkg cannot write world |
| 10 | Name graybox art set | Exemplar pack materials | `R.art.astroneer_bar` | named mesh/material set (not empty) |
| 11 | PMG physics/econ + pre-LLM | deferred owners OK | `R.pmg.physics_econ` · `R.pmg.pre_llm_dm` | `deferred:true` + owner **or** named path |
| 12 | `SwapMatrixSlotBinder.bind_defaults` | module_bind from pack_defaults.swap_slots | _(bind)_ | no Stub host on gen/rules/sim |
| 13 | `ExemplarPackDefaultFiller.apply` | Medium Fantasy chrome+world fill | _(fill)_ | host Node under PlayRegion filled |
| 14 | `CampaignCapableDoDGate.Validate` | full ledger | _(gate)_ | Ok; omit any required → Unconfigured |

**Boot order (code):** `CompletenessGate` → `SwapMatrixSlotBinder.bind_defaults` → `ExemplarPackDefaultFiller.apply` → `PlayRegionHost` live → `ICampaignCapableDoDGate.Validate(ledger)`.

**Does not count:** `demo.loop_complete` alone; any gen/sim/rules receipt with `stub_only: true`; inventing 5.2.2+ twins; Half B.


### Module → swap-slot bind table

| Swap slot id | Phase / contract host | Pack key (`pack_defaults`) | Seat / authority | Graybox OK? |
|--------------|----------------------|----------------------------|------------------|-------------|
| `slot.shell.play_region` | 6.1 `PlayRegionHost` + 1.1 SessionComposer | `shell.mount_id` | `shared_table` / SessionComposer | yes — empty region + HUD stack |
| `slot.gen.pipeline` | 2.1 `IWorldGenStage` DAG + `IMapGenAuthority` | `gen.pipeline_id` | `dm_as_player` / WorldState | yes — deterministic seed → WorldMapData hash |
| `slot.gen.terrain` | 2.`ITerrainAuthority` (Terrain3D) — [[Docs/Junior-Tech-Adapt-How-To]] §1 | `gen.terrain_admit` | DM world package | yes — flat RF height + one splat |
| `slot.gen.maps_parallel` | Gaea/`IMapGenAuthority` → WorldMapData only (§2 how-to) | `gen.maps_gaea_parallel` | DM world | yes — adapter export only |
| `slot.sim.tick` | 3.1 `ISimTickHost` / SimClock | `sim.tick_host` | Simulation layer | yes — ≤1 tick + WorldEventLog row |
| `slot.sim.weather` | 3.1.2 `IWeatherModule` | `sim.weather` | Simulation | yes — one pulse event |
| `slot.sim.faction` | 3.1.4 FactionGraph | `sim.faction` | Simulation | yes — one off-screen edge |
| `slot.cam.fp` | 4.1 `ICameraRig` / PlayerFPRig | `cam.fp_rig` | `player` | yes — spawn + look |
| `slot.cam.dm` | 4.2 ModeTransitionGraph / DM cam | `cam.dm_rig` | `dm_as_player` | yes — one transition |
| `slot.agency.envelope` | 4.3 AgencyEnvelope / PilotHandoff | `agency.envelope` | FP≠DM rail | yes — refuse wrong seat |
| `slot.rules.plugin` | 5.1 `IRulesPluginHost` + `IDiceRoller` | `rules.plugin_id` = `pathfinder_pf1` | Simulation / rules.plugin.core | yes — one check schema |
| `slot.rules.spell_meta` | 5.2 / 5.2.1 SpellMetadataRegistry | `rules.spell_meta` | agency overlays only | yes — registry stub tables |
| `slot.rules.quest_pressure` | 5.3 Quest pressure → IntentResolver hints | `rules.quest_pressure` | IntentResolver | yes — one hint row |
| `slot.demo.proof_loop` | 6.2 beats (stubs OK) | `demo.loop_id` | shared_table | **never** counts as campaign_capable alone |
| `slot.ui.hosts` | 6.1 HUDLayerStack / `IUiHost` | `ui.hud_stack` | Presentation | yes |

### Pack-slot fill matrix (normative — do not invent slots)

Junior fills **only** the rows below. Pack key → swap slot → receipt → graybox artifact is closed; missing row ⇒ fail closed, not a new slot invent.

| # | Pack key | Swap slot | Receipt id | Graybox fill artifact (named) | `module_bind.host_type` |
|---|----------|-----------|------------|-------------------------------|-------------------------|
| 1 | `shell.mount_id` | `slot.shell.play_region` | `R.shell.mount` | NodePath `PlayRegionDefault` under Main | `Genesis.Ui.IPlayRegionHost` |
| 2 | `gen.pipeline_id` | `slot.gen.pipeline` | `R.gen.worldmap_hash` | seed `exemplar_seed_v0` → WorldMapData hash file | `Genesis.World.IMapGenAuthority` |
| 3 | `gen.terrain_admit` | `slot.gen.terrain` | `R.gen.terrain_admit` | flat RF height + splat `biome_grid_v0` | `Genesis.World.ITerrainAuthority` |
| 4 | `gen.maps_gaea_parallel` | `slot.gen.maps_parallel` | _(feeds #2)_ | Gaea adapter export only — **not** terrain | `Genesis.World.IMapGenAuthority` |
| 5 | `sim.tick_host` | `slot.sim.tick` | `R.sim.tick_once` | ≤1 tick + WorldEventLog row `tick_once` | `Genesis.Sim.ISimTickHost` |
| 6 | `sim.weather` | `slot.sim.weather` | _(feeds #5)_ | one `weather_pulse_v1` event | `Genesis.Sim.IWeatherModule` |
| 7 | `sim.faction` | `slot.sim.faction` | _(feeds #5)_ | one off-screen faction edge | `Genesis.Sim.IFactionGraph` |
| 8 | `cam.fp_rig` | `slot.cam.fp` | `R.cam.fp_dm_split` | PlayerFPRig mount at spawn | `Genesis.Perspective.ICameraRig` |
| 9 | `cam.dm_rig` | `slot.cam.dm` | `R.cam.fp_dm_split` | DM cam transition once | `Genesis.Perspective.ICameraRig` |
| 10 | `agency.envelope` | `slot.agency.envelope` | `R.agency.envelope` | wrong-seat refuse probe | `Genesis.Agency.IAgencyEnvelope` |
| 11 | `rules.plugin_id` | `slot.rules.plugin` | `R.rules.pf1_bind` | ActiveRuleset=`pathfinder_pf1`; Roll→IDiceRoller | `Genesis.Rules.IRulesPluginHost` |
| 12 | `rules.spell_meta` | `slot.rules.spell_meta` | _(feeds #11)_ | spell-list scaffold ≥5 ids from [[Docs/PF1-Ruleset-Content-Scaffold]] §4.6 | `Genesis.Rules.ISpellMetadataRegistry` |
| 13 | `rules.quest_pressure` | `slot.rules.quest_pressure` | _(feeds agency)_ | one IntentResolver hint row | `Genesis.Rules.IQuestPressureHint` |
| 14 | `ui.hud_stack` | `slot.ui.hosts` | `R.shell.mount` | HUDLayerStack under PlayRegion | `Genesis.Ui.IUiHost` |
| 15 | _(authority)_ | — | `R.authority.packages` | player cosmetics pkg ≠ world pkg | `AuthorityPackageContract` |
| 16 | _(art)_ | — | `R.art.astroneer_bar` | named graybox mesh/material set id `astroneer_bar_v0` | Exemplar pack |
| 17 | _(pmg)_ | — | `R.pmg.physics_econ` | `deferred:true` + owner string | deferred owner |
| 18 | _(pmg)_ | — | `R.pmg.pre_llm_dm` | named path **or** deferred+owner | deferred owner |
| 19 | _(seams)_ | — | `R.seam.completeness` | CompletenessGate OK on 9 seams | `ISeamRegistry` |
| — | `demo.loop_id` | `slot.demo.proof_loop` | **REJECT alone** | Horizon proof only | never sole DoD |

**Invent forbid:** no extra pack keys, no parallel `Demo*` host types for rows 1–14, no Gaea-as-terrain, no PF2e plugin id.

### `ReferenceExemplarManifest.pack_defaults` (normative shape)

```yaml
track_id: reference_exemplar
scope_id: medium_fantasy_default
ruleset_id: pathfinder_pf1
shell:
  mount_id: play_region_default
gen:
  pipeline_id: stage_dag_v1
  terrain_admit: terrain3d_authority
  maps_gaea_parallel: world_map_data_adapter  # NOT terrain authority
sim:
  tick_host: sim_tick_v1
  weather: weather_pulse_v1
  faction: faction_graph_v1
cam:
  fp_rig: player_fp_v1
  dm_rig: dm_cam_v1
agency:
  envelope: agency_envelope_v1
rules:
  plugin_id: pathfinder_pf1
  spell_meta: spell_agency_registry_v1
  quest_pressure: quest_hint_v1
ui:
  hud_stack: hud_layer_stack_v1
demo:
  loop_id: horizon_demo_v1  # proof only — not Exemplar attestation
swap_slots:
  - slot.shell.play_region
  - slot.gen.pipeline
  - slot.gen.terrain
  - slot.gen.maps_parallel
  - slot.sim.tick
  - slot.sim.weather
  - slot.sim.faction
  - slot.cam.fp
  - slot.cam.dm
  - slot.agency.envelope
  - slot.rules.plugin
  - slot.rules.spell_meta
  - slot.rules.quest_pressure
  - slot.ui.hosts
# slot.demo.proof_loop intentionally omitted from campaign bind set
```

### CampaignCapableDoDGate — checkable receipts (graybox OK)

Gate consumes a **receipt ledger** (Dictionary), not a boolean theater flag. Each required receipt must be present with `status: ok|graybox_ok|deferred` and a **`verify` string** a junior can assert in gdUnit4Net. Missing / `stub_only` → fail closed. Pack-slot fill matrix rows above are the only legal sources — do not invent receipt ids.

| Receipt id | Proves | Source host (phase) | Accept when | Normative `verify` template |
|------------|--------|---------------------|-------------|------------------------------|
| `R.seam.completeness` | Required seams PUBLISHED | 1.3 CompletenessGate | `check() == OK` | `CompletenessGate.Check==Ok;seams=9` |
| `R.gen.worldmap_hash` | Deterministic WorldMapData | 2 `IMapGenAuthority` | seed replay hash match | `seed=exemplar_seed_v0;hash_match=true` |
| `R.gen.terrain_admit` | Height+splat admitted | 2 `ITerrainAuthority` | ImportHeightmap + ApplySplat OK | `ImportHeightmap=Ok;ApplySplat=Ok;flat_rf=true` |
| `R.sim.tick_once` | Living world moved | 3 `ISimTickHost` | ≤1 tick + log append | `ticks<=1;WorldEventLog.contains=tick_once` |
| `R.cam.fp_dm_split` | FP≠DM rail | 4.1 + 4.2 | both mount; wrong-seat refuse | `fp_mount=Ok;dm_mount=Ok;player_to_dm=Unauthorized` |
| `R.agency.envelope` | Pilot/agency bounds | 4.3 | wrong seat → Unauthorized | `wrong_seat=Unauthorized` |
| `R.rules.pf1_bind` | Rules plugin bound | 5.1 `IRulesPluginHost` | ActiveRuleset=pathfinder_pf1; Roll→IDiceRoller | `ActiveRuleset=pathfinder_pf1;RollDelegate=IDiceRoller` |
| `R.shell.mount` | Play region live | 6.1 PlayRegionHost | mount_id resolves; DevLeakageGuard | `mount_id=play_region_default;DevLeakageGuard=pass` |
| `R.authority.packages` | Cosmetics ≠ world | AuthorityPackageContract | player pkg cannot write world | `player_write_world=Unauthorized` |
| `R.art.astroneer_bar` | PMG art fidelity named | Exemplar pack | named graybox set | `art_set_id=astroneer_bar_v0;empty=false` |
| `R.pmg.physics_econ` | PMG systems | deferred owner | deferred+owner | `deferred=true;owner=<named>` |
| `R.pmg.pre_llm_dm` | Pre-LLM adjudication | data path or defer | named path **or** deferred+owner | `path=<id>` **or** `deferred=true;owner=<named>` |

**Receipt row shape (junior copies):**

```json
{"id": "R.gen.terrain_admit", "status": "graybox_ok", "verify": "ImportHeightmap=Ok;ApplySplat=Ok;flat_rf=true", "pack_key": "gen.terrain_admit", "slot": "slot.gen.terrain"}
```

**Reject receipts:** `demo.loop_complete` alone; `stub_only: true` on any gen/sim/rules receipt; Gaea typed as terrain authority; any receipt id not in the table above; empty `verify`.

### Paper ledger (design) — full happy path (checkable end-to-end without game-repo Boot)

Junior copies this ledger and walks `CampaignCapableDoDGate.validate` **on paper** (How-To §6). All required ids present; `verify` non-empty; PMG rows deferred+owner. Omit any one id → fail closed. **Not** a runnable Boot receipt.

```json
{
  "R.seam.completeness": {"id": "R.seam.completeness", "status": "graybox_ok", "verify": "CompletenessGate.Check==Ok;seams=9"},
  "R.gen.worldmap_hash": {"id": "R.gen.worldmap_hash", "status": "graybox_ok", "verify": "seed=exemplar_seed_v0;hash_match=true", "pack_key": "gen.pipeline_id", "slot": "slot.gen.pipeline"},
  "R.gen.terrain_admit": {"id": "R.gen.terrain_admit", "status": "graybox_ok", "verify": "ImportHeightmap=Ok;ApplySplat=Ok;flat_rf=true", "pack_key": "gen.terrain_admit", "slot": "slot.gen.terrain"},
  "R.sim.tick_once": {"id": "R.sim.tick_once", "status": "graybox_ok", "verify": "ticks<=1;WorldEventLog.contains=tick_once", "pack_key": "sim.tick_host", "slot": "slot.sim.tick"},
  "R.cam.fp_dm_split": {"id": "R.cam.fp_dm_split", "status": "graybox_ok", "verify": "fp_mount=Ok;dm_mount=Ok;player_to_dm=Unauthorized"},
  "R.agency.envelope": {"id": "R.agency.envelope", "status": "graybox_ok", "verify": "wrong_seat=Unauthorized", "pack_key": "agency.envelope", "slot": "slot.agency.envelope"},
  "R.rules.pf1_bind": {"id": "R.rules.pf1_bind", "status": "graybox_ok", "verify": "ActiveRuleset=pathfinder_pf1;RollDelegate=IDiceRoller", "pack_key": "rules.plugin_id", "slot": "slot.rules.plugin"},
  "R.shell.mount": {"id": "R.shell.mount", "status": "graybox_ok", "verify": "mount_id=play_region_default;DevLeakageGuard=pass", "pack_key": "shell.mount_id", "slot": "slot.shell.play_region"},
  "R.authority.packages": {"id": "R.authority.packages", "status": "graybox_ok", "verify": "player_write_world=Unauthorized"},
  "R.art.astroneer_bar": {"id": "R.art.astroneer_bar", "status": "graybox_ok", "verify": "art_set_id=astroneer_bar_v0;empty=false"},
  "R.pmg.physics_econ": {"id": "R.pmg.physics_econ", "status": "deferred", "verify": "deferred=true;owner=pmg_physics_econ_owner", "owner": "pmg_physics_econ_owner"},
  "R.pmg.pre_llm_dm": {"id": "R.pmg.pre_llm_dm", "status": "deferred", "verify": "deferred=true;owner=pmg_pre_llm_dm_owner", "owner": "pmg_pre_llm_dm_owner"}
}
```

**Paper refuse probe:** delete `R.gen.terrain_admit` → expect `ERR_UNCONFIGURED` / `exemplar_receipt_missing`. Empty `verify` on any row → same. `stub_only: true` at ledger root → `ERR_INVALID_PARAMETER`.

## Interfaces

```text
ReferenceExemplarManifest (RefCounted):
  + scope_id: StringName
  + track_id: StringName  # reference_exemplar
  + pack_defaults: Dictionary  # see YAML shape above
  + module_bind: Dictionary    # slot_id -> { host_type, phase, seat }
  + to_dict() -> Dictionary

CampaignCapableDoDGate (RefCounted):
  + required_receipt_ids() -> PackedStringArray
  + validate(receipt_ledger: Dictionary) -> Error
  + last_fail_code() -> StringName
  + last_missing_receipts() -> PackedStringArray

ExemplarPackDefaultFiller (RefCounted):
  + apply(manifest: ReferenceExemplarManifest, host: Node) -> Error

SwapMatrixSlotBinder (RefCounted):
  + bind_defaults(manifest: ReferenceExemplarManifest, ports: PortBinder) -> Error
  + release_slot(slot_id: StringName) -> Error

AuthorityPackageContract (RefCounted):
  + assert_player_cosmetics(pkg: Dictionary) -> Error
  + assert_dm_world(pkg: Dictionary) -> Error
```

## Pseudo-code

```pseudo
JUNIOR WORK-ORDER (ux_living_world_continuity L5 — advisory) ===
# Seats: Exemplar fill must respect FP≠DM rail + agency defaults.
# Players do not author world: default fill is system/DM-retconnable — not player invent.
# DM rail vs player FP: Exemplar content usable from both seats without conflation.
# Agency: CampaignCapableDoDGate fails closed if receipt ledger incomplete.
# Bind: SwapMatrixSlotBinder wires Phase 1–5 hosts from pack_defaults.swap_slots — not demo stubs.
# ===========================================================

# 6.4 — Reference Exemplar assembly (Godot 4.6.3 .NET).
# Citations: RefCounted; Error/OK; StringName; Node host from 6.1; PortBinder from 1.3.
# Reject: equating Exemplar attestation with demo.loop_complete;
#         stub-only gen as campaign-capable; Half B/L5; rewriting 6.1–6.3;
#         Gaea as ITerrainAuthority.

class_name CampaignCapableDoDGate
extends RefCounted

var _last_fail: StringName = &""
var _missing: PackedStringArray = PackedStringArray()

func required_receipt_ids() -> PackedStringArray:
	return PackedStringArray([
		&"R.seam.completeness", &"R.gen.worldmap_hash", &"R.gen.terrain_admit",
		&"R.sim.tick_once", &"R.cam.fp_dm_split", &"R.agency.envelope",
		&"R.rules.pf1_bind", &"R.shell.mount", &"R.authority.packages",
		&"R.art.astroneer_bar", &"R.pmg.physics_econ", &"R.pmg.pre_llm_dm",
	])

func validate(receipt_ledger: Dictionary) -> Error:
	_missing = PackedStringArray()
	if bool(receipt_ledger.get("stub_only", false)):
		_last_fail = &"exemplar_stub_gen_rejected"
		return ERR_INVALID_PARAMETER
	for rid in required_receipt_ids():
		var row: Variant = receipt_ledger.get(rid, null)
		if row == null:
			_missing.append(rid)
			continue
		if typeof(row) != TYPE_DICTIONARY:
			_missing.append(rid)
			continue
		var st: String = str(row.get("status", ""))
		var verify: String = str(row.get("verify", ""))
		if verify.strip_edges() == "":
			_missing.append(rid)
			continue
		if st != "ok" and st != "graybox_ok" and st != "deferred":
			_missing.append(rid)
		# deferred allowed only for R.pmg.* with owner present
		if st == "deferred" and not str(row.get("owner", "")):
			_missing.append(rid)
	if _missing.size() > 0:
		_last_fail = &"exemplar_receipt_missing"
		return ERR_UNCONFIGURED
	_last_fail = &""
	return OK

func last_fail_code() -> StringName:
	return _last_fail

func last_missing_receipts() -> PackedStringArray:
	return _missing


class_name SwapMatrixSlotBinder
extends RefCounted

func bind_defaults(manifest: ReferenceExemplarManifest, ports: PortBinder) -> Error:
	# JUNIOR WORK-ORDER: bind real Phase 1–5 port types from module_bind — refuse demo-only stubs for gen/rules/sim
	for slot_id in manifest.pack_defaults.get("swap_slots", []):
		var bind: Dictionary = manifest.module_bind.get(slot_id, {})
		if bind.is_empty():
			return ERR_DOES_NOT_EXIST
		var host_type: StringName = bind.get("host_type", &"")
		if str(slot_id).begins_with("slot.gen.") or str(slot_id).begins_with("slot.rules.") or str(slot_id).begins_with("slot.sim."):
			if str(host_type).contains("Stub") and not bool(bind.get("graybox_host", false)):
				return ERR_INVALID_PARAMETER
		var err: Error = ports.bind(StringName(slot_id), bind.get("port"))
		if err != OK:
			return err
	return OK


class_name ReferenceExemplarDirector
extends RefCounted

var _manifest: ReferenceExemplarManifest
var _dod: CampaignCapableDoDGate
var _filler: ExemplarPackDefaultFiller
var _binder: SwapMatrixSlotBinder
var _ports: PortBinder

func boot(host: Node, receipt_ledger: Dictionary) -> Error:
	var err: Error = _dod.validate(receipt_ledger)
	if err != OK:
		return err
	err = _binder.bind_defaults(_manifest, _ports)
	if err != OK:
		return err
	return _filler.apply(_manifest, host)

# === WEAVE C# / .NET (Godot 4.6.3) ===
# Manifest: stack-ui-hosts, stack-procedural-terrain, stack-ci-gdunit4net, engine-godot-463-dotnet
# Catalog: ux_living_world_continuity | see [[Docs/Junior-Tech-Adapt-How-To]] for terrain/rules adapt
# Type: Genesis.Exemplar.ReferenceExemplarGate

namespace Genesis.Exemplar;
// JUNIOR WORK-ORDER (ux_living_world_continuity): assemble Phase 1–5 hosts into ReferenceExemplarManifest slots
// ACCEPT: wrong seat → Error.Unauthorized (never silent OK)
// ACCEPT: CampaignCapableDoDGate fails when any required receipt missing (graybox_ok allowed)
// REJECT: demo.loop_complete as sole campaign_capable proof
// VERIFY: gdUnit4Net ≥1 happy (all receipts graybox_ok) + ≥1 refuse (omit R.gen.terrain_admit)

public interface ICampaignCapableDoDGate {
    Error Validate(ReceiptLedger ledger);
    string LastFailCode { get; }
}

public sealed class ReferenceExemplarGate {
    // Junior-complete assembly path (graybox OK). Index hosts only — no Half B invent.
    public Error Boot(Node host, ReferenceExemplarManifest manifest, ReceiptLedger ledger, PortBinder ports,
                      ICampaignCapableDoDGate gate, SwapMatrixSlotBinder binder, ExemplarPackDefaultFiller filler) {
        if (host == null || manifest == null || ledger == null || ports == null) return Error.InvalidParameter;
        // 1) Fail closed on incomplete / stub_only ledger BEFORE bind
        var err = gate.Validate(ledger);
        if (err != Error.Ok) return err;
        // 2) Bind Phase 1–5 hosts into swap slots (refuse Stub on gen/rules/sim)
        err = binder.BindDefaults(manifest, ports);
        if (err != Error.Ok) return err;
        // 3) Fill Medium Fantasy defaults into PlayRegionHost / shell
        err = filler.Apply(manifest, host);
        if (err != Error.Ok) return err;
        // 4) Shell must already satisfy R.shell.mount (PlayRegionHost mount_id)
        return Error.Ok;
    }
}

// Concrete module_bind excerpt (junior copies into manifest; types from Host Index)
// slot.gen.terrain → Genesis.World.ITerrainAuthority
// slot.gen.maps_parallel → Genesis.World.IMapGenAuthority
// slot.sim.tick → Genesis.Sim.ISimTickHost
// slot.cam.fp / slot.cam.dm → Genesis.Perspective.ICameraRig
// slot.rules.plugin → Genesis.Rules.IRulesPluginHost
// slot.shell.play_region → Genesis.Ui.IPlayRegionHost
```

## Validation signals

| Signal | Meaning |
|--------|---------|
| DoD fail stub_only | ERR_INVALID_PARAMETER |
| receipt missing / bad status | ERR_UNCONFIGURED + `last_missing_receipts` |
| Swap bind Stub host on gen/rules/sim | ERR_INVALID_PARAMETER |
| Pack apply OK | Exemplar host filled; all campaign slots bound |

## Rejects

- Exemplar complete ≡ demo.loop_complete
- Stub gen counted as campaign-capable
- Boolean `campaign_capable: true` without receipt ledger
- Gaea as terrain authority
- Half B / L5 invent

## Junior acceptance / verify (weave)

- [ ] **Given** a receipt ledger with all required ids at `graybox_ok` (or `deferred`+owner for PMG physics/econ/pre-LLM), **When** `CampaignCapableDoDGate.validate`, **Then** returns OK
- [ ] **Given** ledger omits `R.gen.terrain_admit`, **When** validate, **Then** ERR_UNCONFIGURED and fail code `exemplar_receipt_missing`
- [ ] **Given** `pack_defaults.swap_slots`, **When** `SwapMatrixSlotBinder.bind_defaults`, **Then** each slot resolves a Phase 1–5 host type from module_bind (not parallel fake types)
- [ ] **Verify** `rules.plugin_id` == `pathfinder_pf1` and Roll path → `IDiceRoller`
- [ ] **Verify** Gaea path only fills `slot.gen.maps_parallel` → WorldMapData; terrain slot uses `ITerrainAuthority`
- [ ] **Verify** Godot 4.6.3 **.NET/C#** module path compiles; no GDScript-only Autoload theater for this leaf's authority
- [ ] **Verify** UX paint `row_id` is `ux_living_world_continuity` and moment→module rows are leaf-true (living continuity ≠ combat hosts)
- [ ] **PMG:** Astroneer-level art fidelity = Exemplar contract **present** (graybox OK; bar named); physics/econ = **deferred** with owner — not silent zeros
- [ ] **PMG:** pre-LLM DM adjudication = data-driven non-generative path named or deferred explicitly
- [ ] **Given** junior follows assembly checklist steps 0–14 with graybox receipts, **When** `ReferenceExemplarGate.Boot`, **Then** returns Ok and PlayRegionHost hosts Medium Fantasy default fill
- [ ] **Given** any gen/sim/rules receipt marked `stub_only`, **When** gate.Validate or binder.BindDefaults, **Then** InvalidParameter (fail closed)
- [ ] **Verify** Phase 6 end-state ≡ PMG Reference Exemplar as **assembled campaign-capable prototype** — Horizon demo (6.2) is proof-only and never sole attestation

## Status

`deepen_complete: true` + **`paint_status: woven`** + **Exemplar end-state path advanced** (`purge+assembly-20260929` + `fill-matrix-tighten-20260929` + `design-gate-paper-ledger-20260930`). Charter + bind table + **pack-slot fill matrix (19 closed rows)** + receipt ledger with **normative verify templates** + **paper ledger (design)** + junior assembly checklist (steps 0–14) + non-theater `ReferenceExemplarGate.Boot` (pseudo only). Assembled graybox **design** path is junior-executable without inventing pack slots; Half B polish / game-repo boot still deferred (`half_b_deferred`).

> **Execution roll-up policy:** Status/AC on this note (and children) are the execution-track roll-up; no separate `*Roll-up*` mint required on the Execution spine.

## Next

Hostile revalidate **against design gate only** (paper assembly DoD). **No Half B.** No 5.2.2+ invent. No project_bridge_push.

> **Weave:** `exec-weave-stack-ux-20260929` + `purge_ileafcontract_stubs_and_exemplar_endstate_path` + `design_pf1_thick_howto_exemplar_fill_20260929` + `design_gate_close_20260930`.
