---
title: World Builder + Session Prep Ticket Map
created: 2026-10-19
updated: 2026-10-24
ticket_map: true
map_id: world-builder-session-prep
project-id: genesis-mythos-master
map_status: active
para-type: Resource
schema: "[[Ticket-Map-Schema]]"
claim_class: clean_slate
prior_map_id: world-builder-mini-game
prior_map_disposition: deferred_not_extended
feeds: world-builder-and-session-prep-one-surface
active_recovery: WB-polygon-substrate
active_recovery_slice: alpha0_wb_polygon_substrate_r4
# 2026-10-24 — WB-polygon-substrate stays open. Moment Prefer r4 armed (Ticketment). Prior Prefer/weld scrap: wb-polygon-substrate-ticket-and-weld-scrapped-20261024T171321Z; r3 scope-cut reject archived. Align virgin until GREENLIGHT. Do not Prefer-join archives.
tags:
  - world-builder
  - session-prep
  - ticket-map
  - clean-slate
  - genesis-mythos-master
---

# World Builder + Session Prep Ticket Map

**Map id:** `world-builder-session-prep`  
**Project:** `genesis-mythos-master`  
**Status:** `active`  
**Schema:** [[Ticket-Map-Schema]]  
**This note is an ordered concordance.** It is not a Prefer and not a weldable unit. Cursor still authors one Prefer per ticket from this map plus vault feedstock. Consuming tickets one at a time is the delivery law. Combining the surfaces here does not authorize a combined implementation blob.

## Hierarchy (binding)

Session prep is the star. It is the product target and the pressure forcing growth.

The World Builder is the foundation. It is the load-bearing surface that must become complete because session prep sits on it and demands more than a map tool can give.

The two stay one map because they share one simulation, one polygon world, multi-campaign nesting, one dial surface, and a live rail that flies the same world the deep prep tools edit. Splitting them into two maps would let a later agent ship a wiki beside a toy map and call both done. Even if the codebases remain distinct under the hood, this concordance treats them as one inseparable surface.

All current code is archived. The LIVE implementation is scrap and prior art only. Nothing on this map is already done. No inherited `f5_good`. No “this host already does X.” No laundering of `world-builder-mini-game` greens, gap-audit `match` rows, or mini-game KEEP lines into this map. Every capability below is fresh work on a fresh stack.

Sibling map `world-builder-mini-game` is already archived under `4-Archives/…world-builder-mini-game-ticket-map-retired-…` (see `factory-project.yaml` → `ticket_map_runtime.prior_map_archive`). Do not extend that id. Do not arm Prefers against archived ticket ids (`GEN-sites`, mini-game `WORLD-*` / `PLACE-*`, etc.). Active map authority is `world-builder-session-prep` only.

## What done means

A GM can select a campaign inside a shared living world and then do full Pathfinder 1E session preparation — deep pre-session work and live mid-table inspection and light authoring — against a world that is itself a Dwarf Fortress-class running history (history, civilizations, sites, economy, legends, cause and effect that continue whether any campaign is looking), edited in Anno-class cheat mode (immediate place, query, override), with every dial a precise user would demand left visible and persistent, drawn as deliberately low-fidelity Townscaper-style polygon solids.

World Anvil-class campaign management and Fantasy Grounds-class live table tools are the depth bar. They are realized on the 3D polygon world, not as a separate wiki and not as a traditional 2D overlay. The World Builder is the substrate. Campaign management and live inspection sit on it.

Graphics stay low-fidelity on purpose. The polygon layer exists so spatial relationships, occupancy, hierarchy, and control surfaces stay legible, including during live flight. Art upgrade is a later reskin of stable sim, dial, and control contracts. ARD polish is `deferred` until the first real-gap seat on this map has operator F5. That deferral is the only status on this map that is not `open`.

## Prior-art law (do not join)

Cite old hosts and Prefer ids in backticks only. Do **not** wiki-link slice ids. A wiki-link to an armed slice would let the picker join an old Prefer onto this clean-slate map.

Anti-pattern, not feedstock to copy:

- `world-builder-mini-game` (Factory-DRB `World-Builder-Mini-Game-Ticket-Map.md`, tip through 2026-10-19) explicitly stopped before friends-in-FP, rules, combat, living tick, and campaign play. That truncation is why this map exists. Its `f5_good` rows (`WORLD-s0-intents`, `WORLD-import`, brush KEEP cites, gap-audit `match` rows, `alpha0_gen_sites_r1` awaiting F5, `alpha0_stalberg_dual_place_product_r2`) are evidence of an old ladder, not seats on this one.
- Gap audit `World-Builder-Greenfield-Gap-Audit-20261018` measured dead LIVE code. It does not score this map.
- Generate-button theater, salt-only lore, decals without records, ghost-mesh that is not the commit mesh, and paint-ramp-as-terrain are refuses if they reappear.
- Collapsing the live rail into one ticket is a refuse.
- A disconnected campaign wiki, or session prep that creates or replaces the world or the campaign frame, is a refuse (`ux_dm_session_prep` does-not-mandate).
- Player first-person, character creation, and dominate/pilot are out of this map. They remain PMG work elsewhere. Do not drag them in to look complete.

## Grounding (published only)

Conceptual: perspective split; DM rail is WorldCam (free flight), MapCam (separate plane-locked orthographic rig — not a tilted WorldCam), Sensorium Attach (read-only, always exit to the prior DM rig). Campaign tone profiles are four only (High Fantasy, Medium Fantasy, Low Fantasy, Grimdark); extra tone tags stay deferred per the goal note. Canon pipeline is `proposed → accepted → hooked → sim-active`. World continuity is the point: actions change the world between sessions. World is the durable container; campaigns nest inside it and do not equal it.

Pins used below are titles from `PIN-INDEX.md` only. Primary seats named in notes:

- [[Phase-2-Procedural-Generation-and-World-Building-Roadmap-2026-06-26-0914]]
- [[Phase-2-3-ToneProfile-Profile-Bundle-on-World-Seed-Roadmap-2026-06-26-1535]]
- [[Phase-3-1-Tick-Based-Simulation-Core-Roadmap-2026-06-26-1600]]
- [[Phase-3-2-Off-Screen-Faction-Tribe-Activity-Roadmap-2026-06-26-1615]]
- [[Phase-3-3-DM-Overwrite-vs-Deliberate-Re-Generation-Policy-Roadmap-2026-06-26-1630]]
- [[Phase-4-1-3-WorldCam-MapCam-and-SensoriumAttach-FOV-Roadmap-2026-07-16-0845]]
- [[Phase-4-2-1-TransitionGuardRegistry-and-DM-Session-Authority-Roadmap-2026-07-16-0456]]
- [[Phase-4-2-3-DM-Rail-Chrome-and-DMRailUXContract-Roadmap-2026-07-16-0653]]
- [[amend-campaign-frame-bootstrap-inside-world-Roadmap-2026-08-04]]
- [[Phase-5-1-Rule-Engine-Primitives-and-Plugin-Hooks-Roadmap-2026-06-26-2045]]
- [[Phase-6-1-1-Launch-Flow-and-DevLeakageGuard-Session-Bootstrap-Roadmap-2026-06-27-0406]]

Series that shape this map (targets, not done work): `ux_world_generation`, `ux_dm_campaign_creation`, `ux_dm_session_prep`, `ux_living_world_continuity` and its economy / faction / location / timeline / canon children, `ux_world_authorship_modability`, `ux_camera_control_envelopes` (`ux_dm_worldcam`, `ux_dm_mapcam`, `ux_dm_sensorium`), `ux_session0_bootstrap`, `ux_tone_profile_surface`, `ux_dm_workbench_lore_gui`, `ux_quiet_between_pillars`, `ux_combat_play_surface`.

Actual-play thickeners, not plot: `WB-control-surface-mapping`, `WB-human-operated-story`, `WB-ordinary-progression-rhythm`, `WB-quiet-between-pillars`.

`session-prep-accelerator-loop` was named by the operator and was **not** found on published `main` pack `Docs/catalog-mint/genesis-mythos-master/` at SHA `81eb3b81`. It is not invented here. See open questions.

## Dial families (visible ambition — not a nursery)

These families are tickets in section D. They are listed here so a later cut cannot “simplify” them into one slider.

**World-level defaults** (persist on the world; every campaign inherits until it overrides):

| Family | Ticket |
|--------|--------|
| Tone-profile default (four profiles only) | `DIAL-W-tone-default` |
| Site / population / encounter density | `DIAL-W-density` |
| Consequence weight | `DIAL-W-consequence` |
| Information scent | `DIAL-W-scent` |
| Random-seed behavior (lock, inspect, reroll) | `DIAL-W-seed` |
| Encounter pressure curve | `DIAL-W-pressure` |
| Faction reactivity | `DIAL-W-faction-reactivity` |
| Resource scarcity | `DIAL-W-scarcity` |
| Economy volatility and price stickiness | `DIAL-W-economy` |
| History and civilization tempo; legend verbosity | `DIAL-W-history-tempo` |
| Off-screen activity rate | `DIAL-W-offscreen-rate` |
| Weather harshness | `DIAL-W-weather` |
| Magic-density component (explicit; not buried inside tone) | `DIAL-W-magic-density` |
| Visual noise of the polygon layer | `DIAL-W-visual-noise` |
| Sensory load | `DIAL-W-sensory-load` |
| Pacing of reveals | `DIAL-W-reveal-pace` |
| Moral-fork sharpness | `DIAL-W-moral-fork` |
| Loyalty and trust decay | `DIAL-W-loyalty-decay` |
| Soft-exit path availability | `DIAL-W-soft-exit` |
| Canon-pipeline strictness (`proposed` → `sim-active`) | `DIAL-W-canon-strictness` |
| Human-operated vs sim-operated story mix | `DIAL-W-story-operator` |
| Mythic weight | `DIAL-W-mythic-weight` |
| Quiet-between / downtime density | `DIAL-W-quiet-density` |
| Session clock policy (pause, step, or advance while a session is live) | `DIAL-W-session-clock` |
| Labeled persistent dial surface; hidden smart default is not a control | `DIAL-W-surface` |

**Campaign overrides** (do not rewrite the world default or any other campaign):

| Family | Ticket |
|--------|--------|
| Override contract for every world dial | `DIAL-C-override` |
| Campaign ToneProfile chosen at Session 0 | `DIAL-C-tone` |
| Known-to-cast mask vs GM-omniscient | `DIAL-C-known-mask` |
| Power-band consequence amplitude (early / mid / late) | `DIAL-C-power-band` |

**Live-inspection filters:**

| Family | Ticket |
|--------|--------|
| Filter set: economy, faction, history, site type, campaign delta, known-to-party, sensory load | `DIAL-L-filters` |
| Filter persistence per campaign and per live session | `DIAL-L-persist` |
| Live light-edit ceiling vs deep authoring | `DIAL-L-edit-ceiling` |

## Order

Container and campaign entry gate → Dwarf Fortress generation and living sim → Anno authoring and inspection → full dial surface → camera and control contracts that both modes share → live-rail stack → session-prep flows → Pathfinder 1E wave → continuity and export → fidelity proofs. Art reskin stays last and `deferred`.

## Out of this map

Player first-person embodiment and player camera. Character creation. Dominate, absent-proxy pilot, and other agency-envelope play. A Terrain3D or high-fidelity scene. Fifth tone profiles or optional tone tags. Kingdom-building, mass combat, and other PF1E supplements not named in the fidelity bar (see open questions). Networking and account services.

---

## A — Container and campaign entry gate

The world exists before any campaign. Prep is not allowed to start without one. These seats are early so later agents cannot build prep campaign-blind or treat the world as a single-campaign save.

| Ticket | Status | Product job | Notes |
|--------|--------|-------------|-------|
| `WB-polygon-substrate` | `open` | Foundation — A GM can point at a low-fidelity polygon solid and that solid stays the same polygon that was pointed at. | Point-and-stay only. Not living (`WB-sim-clock`). Not save (`WB-world-container` / `WB-world-document`). Not occupancy / hierarchy / site records (`WB-gen-*` / `WB-insp-*`). Not dials (section D). Not flight or live rail (sections E–F). Not deep authoring cheat-mode (section C). Art reskin is not this ticket. Prior Prefer/weld attempts are in `4-Archives` only — do not Prefer-join. |
| `WB-world-container` | `open` | Foundation — A GM can create, save, and reopen one durable world that is allowed to contain many campaigns, or zero, and that keeps existing when no campaign is open. | Series `ux_world_generation`. Pin [[Phase-2-Procedural-Generation-and-World-Building-Roadmap-2026-06-26-0914]]. World ≠ campaign. Old `WORLD-empty-campaigns` / `WORLD-new` KEEP is prior art only, not done. |
| `WB-sim-clock` | `open` | Foundation — The world clock and its subsystems keep state and can advance while no campaign is selected and while the GM is not looking at a site. | Pin [[Phase-3-1-Tick-Based-Simulation-Core-Roadmap-2026-06-26-1600]]. Mini-game law “nothing ticking” is an anti-pattern for this map. |
| `WB-world-document` | `open` | Foundation — Quit and reload restores the world document: sim snapshot, generated facts, hand edits, dials, and campaign frames, and a document that cannot round-trip the fields landed so far fails. | Old `PACK-save-load` / `PACK-schema` on the mini-game is prior art only. Empty schema is not success. |
| `CAMP-create` | `open` | Weld — A GM can create or revise a campaign frame inside an existing world: tone, bounds, public facts, cast expectations, chronicle seam, and an exit into session prep, without regenerating the world and without opening character creation. | Series `ux_dm_campaign_creation`. Primary pin [[amend-campaign-frame-bootstrap-inside-world-Roadmap-2026-08-04]]. Supporting pin [[Phase-4-2-1-TransitionGuardRegistry-and-DM-Session-Authority-Roadmap-2026-07-16-0456]]. |
| `CAMP-select` | `open` | Prep — Session prep will not open until the GM has selected a campaign; the selection names the scope of every prep and live-rail action that follows. | Mandatory entry gate. A world with zero campaigns offers create, not prep. |
| `CAMP-switch` | `open` | Weld — A GM can leave one campaign and enter another in the same world; world facts remain, the previous campaign’s secrets and deltas do not become the next campaign’s, and prep re-scopes. | Second-campaign case is in `ux_world_generation` alternatives, not a special mode. |
| `CAMP-scope-split` | `open` | Weld — Every fact is stored as world-owned or campaign-owned, and the GM can see which; a campaign edit does not silently rewrite the shared world. | World ≠ campaign. Campaign-owned secrets stay campaign-owned until a DM-gated handoff (`PREP-batch-handoff`). |
| `CAMP-cast-seam` | `open` | Prep — The campaign frame can name cast expectations and a chronicle seam so later prep and continuity can point at those people, and it still does not author player characters. | Not old `CAMP-roster-attach`. Character creation stays out of this map. |
| `WELD-one-world` | `open` | Weld — Deep authoring, session prep, and the live rail are three ways of using one polygon world and one sim; a separate wiki or a 2D-only table does not satisfy any of them. | Depth bar: World Anvil-class and Fantasy Grounds-class on this substrate. Refusing a second map is the job. |

## B — Dwarf Fortress generation and living sim

The world must be generable and then keep going. Generation tickets create records. Sim tickets advance them. Decals, flavor logs, and “DM paints the world” are refuses.

| Ticket | Status | Product job | Notes |
|--------|--------|-------------|-------|
| `WB-gen-landform` | `open` | Foundation — Create World produces a readable landform on the polygon substrate: relief, water, climate, rivers, and biomes with mechanical tags, and the dials that claim to change it actually change it. | Substrate for sites, not the product. Old `GEN-terrain-product` / `GEN-tone` / `GEN-biomes` cites are prior art only. Paint-ramp-as-success is a refuse. |
| `WB-gen-history` | `open` | Foundation — The world generates a multi-step history the GM can read and edit, and an edited line persists as an authored fact distinct from a generated line. | Old `GEN-history` was deferred on the mini-game and never built. Not done. |
| `WB-gen-civ` | `open` | Foundation — Civilizations and peoples generate as records tied to regions and sites, with goals a later sim can pursue. | Not a name list. No off-screen action required in this ticket; `WB-sim-factions` owns the running graph. |
| `WB-gen-sites` | `open` | Foundation — Settlements, ruins, lairs, and wilderness generate as openable records placed from bounds and history, not as decals. | Do not reuse ticket id `GEN-sites` or join `alpha0_gen_sites_r1`. That Prefer is prior art on the deferred map. |
| `WB-gen-economy` | `open` | Foundation — Each settlement generates an economy: production, stock, trade links, and prices, including prices a spellcaster would pay for materials. | Series child `ux_economy_resources`, `ux_economy_trade`. The diamond-price rail has nothing to read until this exists. |
| `WB-gen-legends` | `open` | Foundation — The GM can read a legend that states a cause-and-effect chain from generated history through to a site, people, or price, and can jump to those records. | Legends are derived, not a separate short-story button. Series child `ux_wa_timelines`, `ux_wa_lore_articles`. |
| `WB-gen-monsters` | `open` | Foundation — Regions carry monster and habitat tags as data the encounter tools can query; the tags are not combatants and not a fight. | Feeds section H. Old `GEN-monsters` prior art only. |
| `WB-gen-routes` | `open` | Foundation — Routes between sites are generated when sites exist; drawing them by hand is an optional override, not the only way they appear. | Old `GEN-roads` prior art only. |
| `WB-import-canon` | `open` | Foundation — A GM can import an offline history canon bundle into the world document and see it become world facts, or the import is refused with a reason. | Not the mini-game stub, and not a KEEP inherited from `alpha0_world_import_r2`. |
| `WB-sim-weather` | `open` | Foundation — Weather advances on the world clock and is readable at a place, and campaign tone and the weather dial change it. | Pin family Phase-3-1-2 (supporting; primary sim pin is the tick core). Series child `ux_sim_weather_pulse`. |
| `WB-sim-npc` | `open` | Foundation — NPCs have agenda and schedule records that move when the clock advances, and the GM can read them without opening a dialogue wheel. | Series children `ux_wa_npc_agenda`, `ux_wa_npc_sheet`, `ux_wa_npc_relations`, `ux_wa_npc_secrets`. Pin [[Phase-3-1-3-NPC-Agendas-Subsystem-Roadmap-2026-06-29-2330]] as supporting. |
| `WB-sim-factions` | `open` | Foundation — Faction graph (goals, hierarchy, territory, reputation) advances off-screen while a campaign looks elsewhere, and the change is stored even if no GM has the site open. | Pin [[Phase-3-2-Off-Screen-Faction-Tribe-Activity-Roadmap-2026-06-26-1615]]. Series `ux_living_world_continuity`. Distinct from `WB-gen-civ`, which only creates the records. |
| `WB-sim-economy-tick` | `open` | Foundation — Prices, stock, and trade move on the world clock when no campaign is looking, and a later inspection shows the new value and why it moved. | This is what makes a live diamond price a world fact rather than a note. |
| `WB-sim-unobserved` | `open` | Foundation — A GM can leave the world, advance time, return, and find civilization, faction, economy, and weather changes that were not hand-authored. | Stranger test for “the world runs.” Cause links must be openable via `WB-gen-legends` / `CONT-cause-chain`. |

## C — Anno authoring and inspection

Cheat mode means the GM does not fight the interface. Overrides are recorded. They are not silent rewrites of history.

| Ticket | Status | Product job | Notes |
|--------|--------|-------------|-------|
| `WELD-overwrite-ledger` | `open` | Weld — Place, region regen, prep handoff, and live light-edits all write one overwrite ledger that stays visually distinct from generated history. | Pin [[Phase-3-3-DM-Overwrite-vs-Deliberate-Re-Generation-Policy-Roadmap-2026-06-26-1630]]. One ledger so the three modes cannot invent three histories. |
| `WB-auth-place` | `open` | Foundation — From the polygon view the GM can place a site, route, or region feature immediately, see the committed solid (not a different ghost), and have that fact survive neighbor updates. | Anno cheat-mode. Old `PLACE-product` Prefer is prior art only; do not join it. |
| `WB-auth-edit` | `open` | Foundation — The GM can edit a world or campaign fact in place (name, type, price, owner, tag) and the edit persists in the correct scope. | Scope comes from `CAMP-scope-split`. |
| `WB-auth-query` | `open` | Foundation — The GM can ask a direct question (“price of diamonds in this settlement”, “who holds this region”) and get the record, not a search essay and not a hidden guess. | Explicit query. Smart search may assist; it may not replace the labeled query. |
| `WB-auth-override` | `open` | Foundation — The GM can override a sim result; the override is marked as authored, survives a later tick unless cleared, and does not pretend to be generated history. | Uses `WELD-overwrite-ledger`. |
| `WB-auth-region` | `open` | Foundation — The GM can select a region and stamp, clear, or deliberately regenerate it; local overrides outside that region survive. | Pairs with `CONT-regen-survive`. |
| `WB-auth-settlement` | `open` | Foundation — The GM can open a settlement and edit its economy, sites, and people with the same cheat-mode verbs, without a loading screen. | Nest is data, not a second game. |
| `WB-auth-bulk` | `open` | Foundation — The GM can multi-select and apply one labeled operation (stamp, delete, reseed, retag) and undo that operation as one step. | Cheat mode includes bulk. One-at-a-time only is a fail. |
| `WB-auth-undo` | `open` | Foundation — Undo and redo cover place, generate, override, and a history or price edit. | Hotkey-only with no visible undo is a fail. |
| `WB-insp-world` | `open` | Foundation — The GM can inspect world-level sim state (clock, civ, economy, weather, factions) without entering a campaign. | Foundation inspection. Campaign filters are off in this seat. |
| `WB-insp-campaign` | `open` | Weld — With a campaign selected, the same inspection shows campaign-owned deltas and secrets beside world facts and labels which is which. | Prep and live rail both use this split. |
| `WB-insp-cause` | `open` | Foundation — From any inspected fact the GM can open the cause chain (what tick, legend, or override produced it) and jump back to the parents. | Empty “because the world” copy is a fail. |
| `WB-nest-zoom` | `open` | Weld — The GM can go world → region → settlement → building by zoom or selection with no loading screen, in both the authoring desk and the live rail. | Old `LOOP-inspect` prior art only. Same polygon world (`WELD-one-world`). |

## D — Dial surface

Every row is a labeled, persistent control on `DIAL-W-surface` or its campaign / live companions. A hidden smart default that the GM cannot see and set is a fail for that row. Do not merge these rows.

| Ticket | Status | Product job | Notes |
|--------|--------|-------------|-------|
| `DIAL-W-surface` | `open` | Foundation — Every world dial in this section is visible, named, and saved on the world; there is no mode where the only way to change behavior is an unlabeled default. | Contract for the families below. Precise and autistic users are the acceptance test: the mechanism stays on the surface. |
| `DIAL-W-tone-default` | `open` | Foundation — The world has a default tone profile of exactly one of High Fantasy, Medium Fantasy, Low Fantasy, or Grimdark, and generation, weather, and sim defaults consume it. | Pin [[Phase-2-3-ToneProfile-Profile-Bundle-on-World-Seed-Roadmap-2026-06-26-1535]]. No fifth profile. Campaign override is `DIAL-C-tone`, not a rewrite of this default. |
| `DIAL-W-density` | `open` | Foundation — The GM can set site, population, and encounter density, and a new generate or region regen reflects the value. | Stored number with unchanged output is a fail. |
| `DIAL-W-consequence` | `open` | Foundation — The GM can set how hard world changes scar factions, economies, and places, and an off-screen advance shows a lighter or heavier scar. | Series `ux_living_world_continuity` amplitude. Not a cosmic-death-only switch. |
| `DIAL-W-scent` | `open` | Foundation — The GM can set how strongly clues, rumors, and legends advertise causes, and inspection of the same fact yields more or less scent as the dial moves. | Actual-play pattern `WB` information scent is a thickener only. The dial is the product. |
| `DIAL-W-seed` | `open` | Foundation — The GM can lock, inspect, and reroll the world seed, and a reroll is an explicit action that does not happen because a menu closed. | Inspectable seed. Hidden reseed is a fail. |
| `DIAL-W-pressure` | `open` | Foundation — The GM can set an encounter pressure curve over world time or travel, and planned encounters read that curve instead of a flat random. | Feeds `PF-encounter-budget`. |
| `DIAL-W-faction-reactivity` | `open` | Foundation — The GM can set how fast factions answer insults, losses, and opportunities, and an off-screen advance shows a faster or slower answer. | Distinct from `DIAL-W-offscreen-rate`, which sets how often the sim steps, not how sharp each answer is. |
| `DIAL-W-scarcity` | `open` | Foundation — The GM can set resource scarcity, and settlement stocks and prices move with it. | Feeds economy and treasure. |
| `DIAL-W-economy` | `open` | Foundation — The GM can set price volatility and stickiness, and two advances of the same shock produce a jumpy or a sticky price accordingly. | The diamond example must be dialable, not only simulated. |
| `DIAL-W-history-tempo` | `open` | Foundation — The GM can set how fast history and civilizations move and how verbose legends are, without changing the off-screen step rate by a second hidden knob. | If this and `DIAL-W-offscreen-rate` ever share one control, this ticket fails. |
| `DIAL-W-offscreen-rate` | `open` | Foundation — The GM can set how often unobserved sim steps run relative to the world clock. | Pairs with `WB-sim-unobserved`. |
| `DIAL-W-weather` | `open` | Foundation — The GM can set weather harshness independently of the tone profile’s bias, and the weather sim shows the override. | Tone may suggest a default. The dial must still be settable. |
| `DIAL-W-magic-density` | `open` | Foundation — The GM can set magic density as its own labeled control; tone may propose the initial value and may not hide this control. | Prevents “it’s just in the tone bundle” from burying the mechanism. |
| `DIAL-W-visual-noise` | `open` | Foundation — The GM can set how much incidental polygon detail and motion the world view uses, and the live flight view obeys it. | Even the low-fidelity layer has a sensory dial. Not an art-upgrade ticket. |
| `DIAL-W-sensory-load` | `open` | Foundation — The GM can set a sensory-load ceiling (flash, shake, audio density, simultaneous labels) that both the desk and the live rail obey. | Explicit accessibility control. A buried “reduce motion” OS guess is not this ticket. |
| `DIAL-W-reveal-pace` | `open` | Foundation — The GM can set how fast prep-staged reveals become eligible to surface in play. | Does not auto-reveal secrets. Visibility law stays in `PREP-visibility`. |
| `DIAL-W-moral-fork` | `open` | Foundation — The GM can set how sharp moral forks are (how hard the world scars either choice) without forcing a single betrayal plot. | Actual-play moral-fork cards are thickeners. One conspiracy skin is a fail (`ux_living_world_continuity`). |
| `DIAL-W-loyalty-decay` | `open` | Foundation — The GM can set loyalty and trust decay and recovery rates, and an NPC or faction record shows the rate that applies. | Not a single global “everyone hates you” switch. |
| `DIAL-W-soft-exit` | `open` | Foundation — The GM can set how available walk-away, flee, and silence exits are, as data later prep and play can honor. | Pattern `WB-control-surface-mapping`: soft-exit is a verb, not a cancel button. This ticket stores the dial; `RAIL-soft-exit` performs the live exit. |
| `DIAL-W-canon-strictness` | `open` | Foundation — The GM can set how quickly a proposed intent may move through `proposed → accepted → hooked → sim-active`, and the pipeline UI shows the gate that is currently required. | Series child `ux_canon_pipeline_feel`. Auto-sim-active with no visible gate is a fail. |
| `DIAL-W-story-operator` | `open` | Foundation — The GM can set the mix of human-operated story versus sim-operated reaction, and prep shows which beats are GM-steered, sim-proposed, or both. | Pattern `WB-human-operated-story`. Dialogue-wheel-only is a fail at any mix. |
| `DIAL-W-mythic-weight` | `open` | Foundation — The GM can set mythic weight off or on by degree, and encounter and continuity tools gain or hide mythic fields accordingly. | Off must stay a clean Pathfinder 1E table, not a disabled mythic UI left in the way. |
| `DIAL-W-quiet-density` | `open` | Foundation — The GM can set how much quiet-between (camp, road, linger) the world and prep suggest between pillars. | Series `ux_quiet_between_pillars`. Pattern `WB-quiet-between-pillars`. Not “press rest to refill.” |
| `DIAL-W-session-clock` | `open` | Foundation — The GM can set whether the world sim pauses, single-steps, or keeps advancing while a session is live, and the live rail shows which policy is in force. | The diamond price must still be readable under pause. A running price under “advance” must show as of the current tick. |
| `DIAL-C-override` | `open` | Weld — For a selected campaign the GM can override any world dial; the override is labeled, stored on the campaign, and does not change the world default or any other campaign. | Campaign-specific overrides. Hidden inheritance is a fail. |
| `DIAL-C-tone` | `open` | Prep — At Session 0 the GM sets that campaign’s ToneProfile to one of the four profiles; prep, weather bias, and sim defaults for that campaign consume it. | Series `ux_tone_profile_surface`. Does not regenerate the world. |
| `DIAL-C-known-mask` | `open` | Weld — The GM can set what the cast is treated as knowing versus what the GM can inspect; live filters and prep visibility can use that mask. | GM omniscience stays available. The mask never blinds the GM. |
| `DIAL-C-power-band` | `open` | Prep — The GM can set the campaign’s power band (early, mid, late) and off-screen costs and encounter pressure respect it. | Series `ux_early_game`, `ux_mid_game`, `ux_late_game` as targets. Band is explicit, not inferred only from average party level. |
| `DIAL-L-filters` | `open` | Weld — During inspection and on the live rail the GM can toggle labeled filters for economy, faction, history, site type, campaign delta, known-to-party, and sensory load, and the polygon view shows only what those filters allow. | Live-inspection family. Filters dim or hide; they do not delete facts. |
| `DIAL-L-persist` | `open` | Weld — Live filter choices persist per campaign and per session and are listed somewhere the GM can clear them. | A filter that resets on every rail pop without a visible reason is a fail. |
| `DIAL-L-edit-ceiling` | `open` | Weld — The GM can set what a live-rail edit is allowed to change (read-only, light edit, or handoff into deep prep) and the rail enforces that ceiling. | Prevents the rail from becoming a second hidden authoring mode, or from being too weak to fix a price. |

## E — Camera and control contracts

These rigs serve both the deep desk and the live rail. MapCam is not a tilted WorldCam. Sensorium does not grant control.

| Ticket | Status | Product job | Notes |
|--------|--------|-------------|-------|
| `CAM-worldcam` | `open` | Weld — The GM can free-fly the polygon world: orbit, pan, zoom, tilt, soar, and dive, and can use that rig for both deep authoring and live flight. | Series `ux_dm_worldcam`. Pin [[Phase-4-1-3-WorldCam-MapCam-and-SensoriumAttach-FOV-Roadmap-2026-07-16-0845]]. Players never receive this rig. Old `DESK-cam` prior art only. |
| `CAM-mapcam` | `open` | Foundation — The GM can switch to a separate map-fixed orthographic rig that pans and yaws on the horizontal plane for measurement and long authoring, and tilting WorldCam does not count as this rig. | Series `ux_dm_mapcam`. Distinct frame of reference. |
| `CAM-sensorium` | `open` | Weld — The GM can attach a read-only view to a creature’s perception to answer “what can they sense?”, then exit to the previous WorldCam or MapCam, and the attach never moves that creature. | Series `ux_dm_sensorium`. Not DM pilot. Agency delegation stays out of this map. |
| `CAM-transition` | `open` | Weld — WorldCam, MapCam, Sensorium, deep desk, and live rail have an explicit transition graph the GM can see; an illegal hop is refused with the guard that blocked it. | Pin [[Phase-4-2-1-TransitionGuardRegistry-and-DM-Session-Authority-Roadmap-2026-07-16-0456]]. Comfort interpolation is allowed; conflating rigs is not. |
| `CTRL-region-verb` | `open` | Weld — Each major GM action declares a screen region, an input verb, and a persistence (always-on, ephemeral, or mode-only) and those declarations are visible in the control surface. | Pattern `WB-control-surface-mapping`. “Interact” as the only verb is a fail. |
| `CTRL-cheat-vs-rail` | `open` | Weld — Anno cheat verbs and live-rail verbs are two labeled sets on the same world; the GM can tell which set is active and cannot fire a bulk regen from the live set unless the edit ceiling allows it. | Depends on `DIAL-L-edit-ceiling`. |

## F — Live rail stack

Do not collapse this section into one ticket. Canonical scene: session is live; the GM needs the price of diamonds in a dwarf kingdom; they enter the rail, fly, click, read or lightly edit, and leave; the table is still in the same scene.

| Ticket | Status | Product job | Notes |
|--------|--------|-------------|-------|
| `RAIL-session-contract` | `open` | Prep — While a session is running the GM can enter the live rail and later return, and initiative, scene, whose turn, and open rolls are the same as when they left. | Enter/exit contract. Pin [[Phase-4-2-3-DM-Rail-Chrome-and-DMRailUXContract-Roadmap-2026-07-16-0653]]. A rail that saves-and-quits the fight is a fail. |
| `RAIL-flight` | `open` | Weld — On that rail the GM can move across the polygon world with WASD or an equivalent free-flight control and reach a distant settlement without a menu teleport being the only path. | Uses `CAM-worldcam`. Menu jump may exist as a labeled extra; it is not the flight. |
| `RAIL-click` | `open` | Weld — The GM can click a settlement, site, or region under the flight camera and open its inspection surface without leaving the rail. | Click-to-inspect. A full workbench takeover fails this ticket (see `RAIL-not-workbench`). |
| `RAIL-economy` | `open` | Weld — From that click the GM can read a settlement’s prices and stocks, including a material such as diamonds, and can make a light edit if the edit ceiling allows. | Depends on `WB-gen-economy`, `WB-sim-economy-tick`, `DIAL-L-edit-ceiling`. The canonical diamond case. |
| `RAIL-faction` | `open` | Weld — From the same flight and click path the GM can open the faction surface for that place (goals, standing, territory) and apply a light edit only inside the ceiling. | Depends on `WB-sim-factions`. Not a second navigation app. |
| `RAIL-history` | `open` | Weld — From the same path the GM can open history and legends for that place and see the cause chain. | Depends on `WB-gen-history` and `WB-gen-legends`. Light edit of a history line writes the overwrite ledger. |
| `RAIL-site` | `open` | Weld — From the same path the GM can open the site record (type, occupants, tags, linked encounters) and lightly edit allowed fields. | Encounter deep-edit stays in prep. This ticket is inspect plus light edit. |
| `RAIL-campaign-filter` | `open` | Weld — Rail filters and the known-to-cast mask apply to the campaign that owns the live session; switching nothing under the hood cannot show another campaign’s secrets. | Depends on `DIAL-L-filters`, `DIAL-C-known-mask`, `CAMP-select`. |
| `RAIL-light-edit` | `open` | Weld — A light edit made on the rail is written to the overwrite ledger, scoped correctly, and visible as authored when the GM returns to the desk. | No silent sim rewrite. Depends on `WELD-overwrite-ledger`. |
| `RAIL-soft-exit` | `open` | Prep — The GM can leave the rail by a short, labeled exit and land back in the live session without a hard stop, a loading break, or a forced recap. | Soft-exit. Distinct from `DIAL-W-soft-exit`, which stores how available fiction exits are. |
| `RAIL-not-workbench` | `open` | Weld — The rail never dumps the GM into the full prep workbench; opening deep prep is a separate, labeled choice that still does not tear down the session. | Keeps Fantasy Grounds-class live use from becoming World Anvil-class authoring by accident. |

## G — Session prep flows

Prep is the star. It consumes the foundation. It does not create the world, does not replace the campaign frame, and is not an offline app.

| Ticket | Status | Product job | Notes |
|--------|--------|-------------|-------|
| `PREP-gate` | `open` | Prep — Choosing session prep with no campaign selected is refused and the GM is sent to select or create one. | Enforces `CAMP-select`. Series `ux_dm_session_prep`: prep does not create the campaign frame. |
| `PREP-deep` | `open` | Prep — With a campaign selected the GM can spend a long pre-session sitting on the polygon world: read sim state, place and override, stage beats, and review secrets, without a separate wiki. | World Anvil-class depth on the substrate. Series `ux_dm_session_prep`. |
| `PREP-workbench` | `open` | Prep — The GM has a workbench for lore, beats, and continuity that is anchored to world and campaign records, not a free-floating document the sim cannot see. | Series child `ux_dm_workbench_lore_gui`. Unlinked notes may exist only as drafts until attached. |
| `PREP-between` | `open` | Prep — Between sessions the GM can review what the world did and what this campaign already changed, then accept, reject, or revise before the next session. | Star pressure on `WB-sim-unobserved` and `PREP-continuity-delta`. |
| `PREP-visibility` | `open` | Prep — Each staged fact is unmarked (secret) unless the GM opts into whole-table and/or per-player visibility. | Series law on `ux_dm_session_prep`. A single whole-table tag as the only control is a fail. |
| `PREP-batch-handoff` | `open` | Weld — World-hitting prep edits batch and enter the world only through the DM gate and the overwrite / regen rules; prep cannot sneak a world change around that gate. | Series does-not-mandate: prep is not a back door. Depends on `WELD-overwrite-ledger` and `DIAL-W-canon-strictness`. |
| `PREP-session0` | `open` | Prep — Session 0 for a campaign, in tool, sets table bounds, tone, shared intents, and DM accept-or-revise, and it never regenerates the world and never owns character creation. | Series `ux_session0_bootstrap` inside `ux_dm_campaign_creation`. Canon pipeline starts here. Offline Microscope play is not required. |
| `PREP-opening` | `open` | Prep — The GM can author the opening situation, temporary constraints, and multi-path goals for session 1 or session N as prep, and that authorship is not a separate product mode. | Series `ux_dm_session_prep`: opening is prep, not another series parent. A single captivity start is not the default. |
| `PREP-bootstrap` | `open` | Prep — The GM can start the live session from the prepared state and land in the table frame with that state loaded. | Pin [[Phase-6-1-1-Launch-Flow-and-DevLeakageGuard-Session-Bootstrap-Roadmap-2026-06-27-0406]] is supporting only. Dev-leakage chrome is not the product. |
| `PREP-human-story` | `open` | Prep — Social beats can be staged as GM soft framing plus room for a player move the GM did not list; a three-button dialogue wheel cannot be the only social tool. | Pattern `WB-human-operated-story`. Depends on `DIAL-W-story-operator`. |
| `PREP-quiet` | `open` | Prep — The GM can stage camp, road, and linger beats that keep fiction continuous between combat, social, and exploration, and rest is not only a resource button. | Series `ux_quiet_between_pillars`. Pattern `WB-quiet-between-pillars`. |
| `PREP-ordinary-rhythm` | `open` | Prep — The GM can stage ordinary advancement (a new option, a small reputation shift, a tool the next fight will feel) without a mythic set-piece. | Pattern `WB-ordinary-progression-rhythm`. Mythic weight may be off. |
| `PREP-continuity-delta` | `open` | Prep — The GM can read a between-session delta for this campaign: world motion, campaign-owned changes, and costs the cast could notice, with machinery visible to the GM. | Series `ux_living_world_continuity`. Players-feel-residue is out of this map except as notes the GM can mark visible. |
| `PREP-export` | `open` | Prep — The GM can hand off a prepared session package that the same campaign can run at full fidelity: beats, encounters, visibility, dials in force, and links into world records. | Not a PDF of notes. A package that loses site links or dial overrides fails. |

## H — Pathfinder 1E wave

Not one row. These are the surfaces a GM needs to run real Pathfinder 1E encounters, exploration, social play, downtime, adjudication, and continuity, with mythic weight only when the dial says so. They sit on the world; they are not a side binder.

| Ticket | Status | Product job | Notes |
|--------|--------|-------------|-------|
| `PF-rules-engine` | `open` | Foundation — The selected campaign can resolve Pathfinder 1E checks (d20, BAB, saves, skills, AC, CMB/CMD, spells, conditions) through an explicit rules surface that prep and the live table both call. | Pin [[Phase-5-1-Rule-Engine-Primitives-and-Plugin-Hooks-Roadmap-2026-06-26-2045]]. A notes field that says “roll high” is a fail. One ruleset binding, not a second engine inside prep. |
| `PF-ruleset-bind` | `open` | Weld — The campaign frame shows that it is bound to Pathfinder 1E, and world tags (biome, monster region, scarcity) are readable by that ruleset. | Clean-slate bind. Old `PACK-rules-tags` prior art only. |
| `PF-encounter-site` | `open` | Prep — The GM can attach an encounter to a polygon site so the fight has a place, a terrain, and a parent settlement or wilderness record. | Floating encounter with no site fails. |
| `PF-encounter-budget` | `open` | Prep — The GM can see and set APL, CR, and XP budget for that encounter, and the pressure dial’s suggestion is visible and overridable. | Depends on `DIAL-W-pressure` and `DIAL-C-power-band`. |
| `PF-roster` | `open` | Prep — The GM can place creatures on that encounter with stats the rules engine can use, plus tactics notes and terrain tags. | Monster-region tags may suggest; they do not auto-fill a fight the GM did not accept. |
| `PF-hazards` | `open` | Prep — The GM can author traps, haunts, and hazards on a site with trigger, effect, and disable information the rules engine can adjudicate. | Not a sticker on the polygon. |
| `PF-treasure` | `open` | Weld — The GM can place or generate treasure and see it against local prices and the scarcity dial, then override either number. | Depends on `WB-gen-economy` and `DIAL-W-scarcity`. |
| `PF-spellcasting` | `open` | Prep — The GM can prepare or inspect spell lists, slots, and material components for combatants, and component prices can be read from the settlement economy. | Live rail may show a component price; this ticket is the prep and adjudication surface. |
| `PF-initiative` | `open` | Prep — During a live session the GM can run initiative and turn order, and that tracker is still there after a rail pop and soft exit. | Depends on `RAIL-session-contract`. Fantasy Grounds-class bar for this seat. |
| `PF-combat-adjudicate` | `open` | Prep — During a fight the GM can adjudicate attacks, damage, spells, and maneuvers on the combatants in the encounter, with the rules engine showing the inputs and the result. | Series `ux_combat_play_surface`. Hidden “the computer decided” with no inputs is a fail. |
| `PF-conditions` | `open` | Prep — The GM can apply, read, and expire conditions with duration on combatants, and those conditions survive into the next beat of the same session. | Includes ongoing world scars only when written through continuity, not by accident. |
| `PF-exploration` | `open` | Prep — The GM can adjudicate exploration (perception, stealth, light, travel time) against the polygon place, weather, and scent dial. | Not a hex-map clone unless the polygon distances are the source. |
| `PF-social` | `open` | Weld — The GM can adjudicate social checks against NPC attitude and faction reputation, and still record a player move that was not on a list. | Depends on `PREP-human-story` and `WB-sim-factions`. Series children `ux_wa_faction_reputation`, `ux_wa_npc_dialogue_hooks`. |
| `PF-knowledge` | `open` | Weld — A knowledge check can be adjudicated against legends and information scent, and the GM sees both the roll inputs and what the dial would reveal. | Depends on `DIAL-W-scent` and `WB-gen-legends`. |
| `PF-downtime` | `open` | Weld — The GM can resolve downtime (craft, earn, recover, train) against the economy and loyalty rules, and the results can write a campaign delta. | Not a kingdom-building game. See open questions before adding mass or realm subsystems. |
| `PF-resources` | `open` | Prep — The GM can track party wealth and consumables for the campaign cast seam, priced where relevant from the living economy. | Uses `CAMP-cast-seam`. Does not create characters. |
| `PF-rest` | `open` | Prep — The GM can run a rest as both a rules refill and a quiet-between beat, and lingering conditions and story residue are still there afterward. | Depends on `PREP-quiet`. Refill-only is a fail. |
| `PF-mythic` | `open` | Prep — When mythic weight is above off, the GM can track mythic tier, path, and surge for combatants; when it is off, those controls are not in the way. | Depends on `DIAL-W-mythic-weight`. |
| `PF-ruling-log` | `open` | Prep — Every adjudication can be accepted, overridden, or deferred, and the choice is appended to a ruling log the GM can reread next session. | No hidden automation as the only path. Overrides hit `WELD-overwrite-ledger` when they change world or campaign facts. |
| `PF-continuity-write` | `open` | Weld — When the session ends, HP, conditions, wealth, reputation, and story awards the GM confirms write a campaign delta, and world-hitting pieces wait on the DM gate. | Depends on `PREP-batch-handoff`. Sheet-only memory is a fail. |

## I — Continuity and the session hand-off

| Ticket | Status | Product job | Notes |
|--------|--------|-------------|-------|
| `CONT-offscreen-read` | `open` | Foundation — The GM can list what factions, economies, and places did while unobserved, with a time range and a link to each record. | Pin [[Phase-3-2-Off-Screen-Faction-Tribe-Activity-Roadmap-2026-06-26-1615]]. |
| `CONT-cause-chain` | `open` | Foundation — The GM can walk from a visible change back through ticks, legends, and overrides to a cause, and can stop at any parent and edit only through the ledger. | Shared by desk, prep, and rail. |
| `CONT-regen-survive` | `open` | Foundation — A deliberate regional regeneration rewrites only that region’s generated facts; overrides and edits outside it, and overrides inside it that the GM marks keep, survive. | Pin [[Phase-3-3-DM-Overwrite-vs-Deliberate-Re-Generation-Policy-Roadmap-2026-06-26-1630]]. |
| `CONT-two-histories` | `open` | Weld — World history and the campaign chronicle stay two labeled streams; a campaign’s public recap does not become world canon unless the GM hands it across the gate. | Series chronicle seam on the campaign frame. `ux_backstory_legacy_integration` is a neighbor, not this ticket’s owner. |
| `CONT-power-band` | `open` | Weld — Readable costs on return match the campaign power band: early stays local, mid can scar a region, late can threaten the campaign’s scale, and the band in force is shown. | Series `ux_living_world_continuity` plus early/mid/late series. The GM sees the machinery. |

## J — Fidelity proofs

These are product proofs of the combined surface, not engine unit tests. Each one fails if a stranger cannot watch the GM do the sentence.

| Ticket | Status | Product job | Notes |
|--------|--------|-------------|-------|
| `PROOF-two-campaigns` | `open` | Weld — A stranger watches the GM run two campaigns in one world, switch between them, and show that world history is shared while secrets and dial overrides are not. | Depends on section A and `CONT-two-histories`. |
| `PROOF-df-anno` | `open` | Foundation — A stranger watches a generated world advance unobserved, then watches the GM cheat-place or override a site, and the legend and ledger both show what was generated and what was authored. | Depends on sections B and C. |
| `PROOF-dials` | `open` | Foundation — A stranger watches the GM find, name, change, save, reload, and campaign-override every dial family in section D without hunting through unmarked defaults. | Fails if any family is missing from the surface. |
| `PROOF-pre-session` | `open` | Prep — A stranger watches the GM select a campaign, set Session 0 tone, read the economy, author a Pathfinder encounter on a site, stage a quiet beat, and export a session package. | Star proof, pre-session. |
| `PROOF-live-diamond` | `open` | Weld — A stranger watches a live session, the GM enter the rail, fly to a dwarf settlement, read or lightly edit the diamond price, soft-exit, and resume the same initiative. | Canonical live-rail proof. All section F seats required. |
| `PROOF-pf1e-night` | `open` | Prep — A stranger watches one Pathfinder 1E slice that includes a fight, a social beat with a move that was not prelisted, an exploration check, and a downtime or rest residue, then a campaign delta written on confirm. | Mythic fields appear only if the dial is on. |
| `PROOF-export-fidelity` | `open` | Prep — A stranger watches the exported package start inside the same campaign and still show the encounter’s site, the dial overrides, the visibility tags, and the prices that were current at export. | `PREP-export` is not done until this proof can pass. |

## K — Deferred art

Pointable polygon solids are already required in `WB-polygon-substrate`. This row is the reskin, not the product.

| Ticket | Status | Product job | Notes |
|--------|--------|-------------|-------|
| `VIS-ard-reskin` | `deferred` | Foundation — An artist or later agent can replace polygon materials and meshes with a richer look without changing sim results, dial values, or control verbs. | ARD polish. Not launchable until the first real-gap seat on this map has operator F5. Never first. Old `VIS-water-polish`, `VIS-style`, `VIS-variants` are prior art on the deferred mini-game, not this row’s KEEP. |
| `WB-art-seam` | `open` | Foundation — Sim, dial, and control contracts are documented as the stable surface that `VIS-ard-reskin` must honor, and a visual change that requires a sim rewrite fails this ticket. | The seam is work now. The pretty picture stays deferred. |

---

## Status policy

- Every capability row is `open`. None are `f5_good`.
- `VIS-ard-reskin` is the only `deferred` row, by the ARD-until-first-real-gap law.
- `WB-polygon-substrate` stays `open`. Failed Prefer/weld attempts live only under `4-Archives` (`wb-polygon-substrate-ticket-and-weld-scrapped-*` and Prefer chain). Align virgin. Do not Prefer-join archives.
- Old Prefer / weld ids (archived `wb-polygon-substrate-prefer-retired-*`, `wb-polygon-substrate-r1-superseded-*`, `wb-polygon-substrate-r2-retired-*`, `wb-polygon-substrate-r3-scope-cut-rejected-*`, `wb-polygon-substrate-ticket-and-weld-scrapped-*`) are not candidates. Do not Prefer-join them.
- Next Prefer: Ticketment against an **open** map row; do not Prefer-join archived polygon attempts.

## Open questions (operator, before this map is green)

1. **Sibling flip.** Confirm Cursor should set `world-builder-mini-game` to `map_status: deferred` in the same change that lands this note. This pass did not edit that file.
2. **ARD status.** Confirm `VIS-ard-reskin` stays `deferred` while every other row stays `open`. The alternative is all rows `open`, which would let the picker treat art as a normal candidate once a Prefer exists.
3. **PF1E supplement edge.** This map includes core play: combat, spells, conditions, exploration, social, downtime, wealth, mythic when dialed on. It does not include kingdom-building, mass combat, or a full Ultimate Campaign realm layer. Say if those are in this map or a later one.
4. **Rules engine ownership.** `PF-rules-engine` is on this map because prep cannot be honest without it and the stack is clean-slate. Say if the engine must stay a different map that this one only binds.
5. **`session-prep-accelerator-loop`.** Named in the brief; no body on the published pack at SHA `81eb3b81`. Republish or paste it before any Prefer treats it as feedstock. It was not invented here.
6. **Player-visible residue.** Continuity tickets let the GM mark what the cast could notice. Actual player-facing first-person presentation of that residue is out of scope. Confirm that split.
7. **First Prefer.** `WB-polygon-substrate` stays `open`; prior attempts are archive-only. Do not Prefer-join (`wb-polygon-substrate-prefer-retired-*`, `wb-polygon-substrate-r1-superseded-*`, `wb-polygon-substrate-r2-retired-*`, `wb-polygon-substrate-r3-scope-cut-rejected-*`, `wb-polygon-substrate-ticket-and-weld-scrapped-*`). Not `GEN-sites`.
