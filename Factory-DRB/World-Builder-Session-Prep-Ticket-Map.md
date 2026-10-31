---
title: World Builder + Session Prep Ticket Map
created: 2026-10-19
updated: 2026-10-31
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
active_recovery_slice: alpha0_wb_polygon_substrate_r9
# prior live map archive: 4-Archives/Projects/genesis-mythos-master/world-builder-session-prep-ticket-map-pre-touch-20261030T071132Z
# 2026-10-31 — Armed Prefer alpha0_wb_polygon_substrate_r9 (B1 ok, stageable). factory_greenlit false. tip 9eb70d5. Awaiting GREENLIGHT.
# 2026-10-30 — Revision: Touch is f5|none and matches Observe. System + Walk are operator text for B2, not Gate A.
# 2026-10-30 — Scope locked: kingdom under factions; mass combat own family; PF options / house rule / spell gate in; accelerator feedstock ticketed. No GREENLIGHT.
# 2026-10-30 — r7 print-flag B1 terminal archived.
# 2026-10-29 — (r7 was armed then scraped.) r6 label-check archived. Senior B1 tip main 49cdc8e.
# 2026-10-26 — Observe person|record on map. r4/r5 Prefers archived. Align virgin. Do not Prefer-join archives.
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

**Columns:** Ticket, Status, Product job, Notes, and two closed cells: Observe (`person` or `record`) and Touch (`f5` or `none`). System and Walk blocks are not columns and not tickets.

**Count:** 153 tickets. 152 `open`. 1 `deferred` (`VIS-ard-reskin`). 92 `f5`. 61 `none`. No `f5_good`.

## Hierarchy (binding)

Session prep is the star. It is the product target and the pressure forcing growth.

The World Builder is the foundation. It is the load-bearing surface that must become complete because session prep sits on it and demands more than a map tool can give.

The two stay one map because they share one simulation, one polygon world, multi-campaign nesting, one dial surface, and a live rail that flies the same world the deep prep tools edit. Splitting them into two maps would let a later agent ship a wiki beside a toy map and call both done. Even if the codebases remain distinct under the hood, this concordance treats them as one inseparable surface.

All current code is archived. The LIVE implementation is scrap and prior art only. Nothing on this map is already done. No inherited `f5_good`. No “this host already does X.” No laundering of `world-builder-mini-game` greens, gap-audit `match` rows, or mini-game KEEP lines into this map. Every capability below is fresh work on a fresh stack.

Session prep stays the star capability. Using it is optional. The living world must stay coherent with zero formal prep. A mandatory prep ritual is a refuse. That is `session-prep-accelerator-loop`, not a softening of the depth bar.

Sibling map `world-builder-mini-game` is already archived under `4-Archives/Projects/genesis-mythos-master/world-builder-mini-game-ticket-map-retired-20261019T203200Z` (see `factory-project.yaml` → `ticket_map_runtime.prior_map_archive`). Do not extend that id. Do not arm Prefers against archived ticket ids (`GEN-sites`, mini-game `WORLD-*` / `PLACE-*`, etc.). Active map authority is `world-builder-session-prep` only.

## What done means

A GM can select a campaign inside a shared living world and then do full Pathfinder 1E session preparation — deep pre-session work and live mid-table inspection and light authoring — against a world that is itself a Dwarf Fortress-class running history (history, civilizations, sites, economy, legends, cause and effect that continue whether any campaign is looking), edited in Anno-class cheat mode (immediate place, query, override), with every dial a precise user would demand left visible and persistent, drawn as deliberately low-fidelity Townscaper-style polygon solids.

World Anvil-class campaign management and Fantasy Grounds-class live table tools are the depth bar. They are realized on the 3D polygon world, not as a separate wiki and not as a traditional 2D overlay. The World Builder is the substrate. Campaign management and live inspection sit on it.

Kingdom-scale play sits on factions in section B. It is not a later map. Mass combat is its own family (section I). The Pathfinder rules surface stays on this map and includes option switches, house rules, and spell allow or ban. Player-facing graphics of residue or recaps do not.

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

`session-prep-accelerator-loop` is operator feedstock, pattern only, not a clone. Body lives under `Roadmap/User-Story/Inspiration-UX-Feedstock/cards/session-prep-accelerator-loop` (mirrored in catalog-mint). Section G tickets that doctrine and does not add mechanics past it. Series it names: `ux_dm_session_prep`, `ux_collaborative_table_agency`, `ux_living_world_continuity`, `ux_dm_campaign_creation`.

## Touch and section text (binding)

`Touch` is a closed cell on every ticket row. It is only `f5` or `none`.

- `f5` means this row contains the user act. `Observe` is `person`. The operator F5 is that row's one product-job sentence. A section Walk is not that F5.
- `none` means this row does not contain a user act. `Observe` is `record`. A probe closes it. The operator is not called. Demanding an F5 on a `none` row is a fail.
- The two cells match. `person` is `f5`. `record` is `none`. A mismatch is a broken row.
- There is no third token and no `wait:<ticket>` pointer. A later `f5` row must not be turned into a second test of an earlier `none` row. Do not skip a spine, and do not invent a ticket type to hold one.
- `deferred` is not mintable. `VIS-ard-reskin` stays `deferred` even though its Touch is `f5`.
- First Prefer remains `WB-polygon-substrate` (`person`, `f5`). This revision does not arm it, does not repair `alpha0_wb_polygon_substrate_r8`, and does not GREENLIGHT.

Gate A may check that Touch is one of those two tokens and that it matches Observe. Gate A must not copy a System paragraph or a Walk into `structural_success`, `behavior_keys`, or `behavior_key_checks`. Pasting a Walk into a Prefer is a thin copy, not fidelity.

Each lettered section has a **System** paragraph and a **Walk**. Both are required operator text. They say what system the rows serve, and what a person can check so a glitch is not waved through.

- They are not Prefer fields. The factory cannot stamp them done.
- Gate B2 may read the Walk and report gaps. A gap names the row in the step: the welded row does that step, or the step is missing, substituted, or only named. B2 cannot mark the Walk done, cannot set `f5_good`, cannot set `map_fidelity_hostile_ok`, and cannot GREENLIGHT.
- A Walk is not a section pass and not eat order. Rows still close one at a time. `none` steps in a Walk are probe reminders, not F5s.

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

Container and campaign entry gate → Dwarf Fortress generation and living sim, kingdom included as faction-scale → Anno authoring and inspection → full dial surface → camera and control contracts that both modes share → live-rail stack → session-prep flows, including the optional accelerator → Pathfinder 1E wave, including the rules family → mass combat → continuity and export → fidelity proofs. Art reskin stays last and `deferred`.

## Out of this map

Player first-person embodiment and player camera. Character creation. Dominate, absent-proxy pilot, and other agency-envelope play. A Terrain3D or high-fidelity scene. Fifth tone profiles or optional tone tags. Player-facing graphics for residue, recaps, or secrets. The GM may mark what the cast could notice, and may generate a recap from player logs; showing that recap through player graphics is not this map. Networking and account services.

In this map, on purpose: kingdom-scale play under factions, mass combat as its own family, the Pathfinder 1E rules engine, house rules, and spell allow or ban.

---

## A — Container and campaign entry gate

The world exists before any campaign. Prep is not allowed to start without one. These seats are early so later agents cannot build prep campaign-blind or treat the world as a single-campaign save.


### System (operator text — not a Prefer, not Gate A)

One durable world can hold many campaigns or none. Prep cannot start without a selected campaign, and prep cannot create the world. The first person act on this map is pointing at one polygon and having that same solid remain. Create, select, switch, scope, cast seam, and the one-world weld are user acts. The clock and the document round-trip are records. The operator is not called for those two.

### Walk (operator text — B2 may report gaps; nobody stamps this done)

Not eat order. The first Prefer is only step 1. Later steps are not its success.

1. `WB-polygon-substrate` — Point at one solid. Come back to the same view. It is the same polygon. Do not require a campaign, a tick, a save, or a site.
2. `WB-world-container` — Create a world, leave, reopen. It exists with zero campaigns.
3. `CAMP-create` — Add a campaign frame inside it. The world does not regenerate. Character creation does not open.
4. `CAMP-select` — Open prep with nothing selected. It refuses. Select the campaign. Later prep names that campaign.
5. `CAMP-switch` — Enter a second campaign. World facts remain. The first campaign's secrets are not the second's.
6. `CAMP-scope-split` — Edit a campaign secret and a world fact. Labels show which is which. The secret does not rewrite the world fact.
7. `CAMP-cast-seam` — Name cast expectations and a chronicle seam. No player character is created.
8. `WELD-one-world` — Authoring, prep, and the live rail are the same polygon world. A wiki or a flat table does not pass.
9. Do not F5 `WB-sim-clock` or `WB-world-document`. Those are `none`. A probe owns clock advance with no campaign open, and quit/reload of the fields landed so far.

| Ticket | Status | Product job | Notes | Observe | Touch |
|--------|--------|-------------|-------|---------|-------|
| `WB-polygon-substrate` | `open` | Foundation — A GM can point at a low-fidelity polygon solid and that solid stays the same polygon that was pointed at. | First Prefer. Touch is `f5`. The section A Walk is not this row's success. Point-and-stay only. Not living (`WB-sim-clock`). Not save (`WB-world-container` / `WB-world-document`). Not occupancy / hierarchy / site records (`WB-gen-*` / `WB-insp-*`). Not dials (section D). Not flight or live rail (sections E–F). Not deep authoring cheat-mode (section C). Art reskin is not this ticket. Prior Prefer/weld attempts (including r4 lookup-shell) are in `4-Archives` only — do not Prefer-join. | `person` | `f5` |
| `WB-world-container` | `open` | Foundation — A GM can create, save, and reopen one durable world that is allowed to contain many campaigns, or zero, and that keeps existing when no campaign is open. | Series `ux_world_generation`. Pin [[Phase-2-Procedural-Generation-and-World-Building-Roadmap-2026-06-26-0914]]. World ≠ campaign. Old `WORLD-empty-campaigns` / `WORLD-new` KEEP is prior art only, not done. | `person` | `f5` |
| `WB-sim-clock` | `open` | Foundation — The world clock and its subsystems keep state and can advance while no campaign is selected and while the GM is not looking at a site. | Pin [[Phase-3-1-Tick-Based-Simulation-Core-Roadmap-2026-06-26-1600]]. Mini-game law “nothing ticking” is an anti-pattern for this map. | `record` | `none` |
| `WB-world-document` | `open` | Foundation — Quit and reload restores the world document: sim snapshot, generated facts, hand edits, dials, and campaign frames, and a document that cannot round-trip the fields landed so far fails. | Old `PACK-save-load` / `PACK-schema` on the mini-game is prior art only. Empty schema is not success. | `record` | `none` |
| `CAMP-create` | `open` | Weld — A GM can create or revise a campaign frame inside an existing world: tone, bounds, public facts, cast expectations, chronicle seam, and an exit into session prep, without regenerating the world and without opening character creation. | Series `ux_dm_campaign_creation`. Primary pin [[amend-campaign-frame-bootstrap-inside-world-Roadmap-2026-08-04]]. Supporting pin [[Phase-4-2-1-TransitionGuardRegistry-and-DM-Session-Authority-Roadmap-2026-07-16-0456]]. | `person` | `f5` |
| `CAMP-select` | `open` | Prep — Session prep will not open until the GM has selected a campaign; the selection names the scope of every prep and live-rail action that follows. | Mandatory entry gate. A world with zero campaigns offers create, not prep. | `person` | `f5` |
| `CAMP-switch` | `open` | Weld — A GM can leave one campaign and enter another in the same world; world facts remain, the previous campaign’s secrets and deltas do not become the next campaign’s, and prep re-scopes. | Second-campaign case is in `ux_world_generation` alternatives, not a special mode. | `person` | `f5` |
| `CAMP-scope-split` | `open` | Weld — Every fact is stored as world-owned or campaign-owned, and the GM can see which; a campaign edit does not silently rewrite the shared world. | World ≠ campaign. Campaign-owned secrets stay campaign-owned until a DM-gated handoff (`PREP-batch-handoff`). | `person` | `f5` |
| `CAMP-cast-seam` | `open` | Prep — The campaign frame can name cast expectations and a chronicle seam so later prep and continuity can point at those people, and it still does not author player characters. | Not old `CAMP-roster-attach`. Character creation stays out of this map. | `person` | `f5` |
| `WELD-one-world` | `open` | Weld — Deep authoring, session prep, and the live rail are three ways of using one polygon world and one sim; a separate wiki or a 2D-only table does not satisfy any of them. | Depth bar: World Anvil-class and Fantasy Grounds-class on this substrate. Refusing a second map is the job. | `person` | `f5` |
## B — Dwarf Fortress generation and living sim

The world must be generable and then keep going. Generation tickets create records. Sim tickets advance them. Decals, flavor logs, and “DM paints the world” are refuses. Kingdom rows sit in this section, immediately after the faction graph: a kingdom is faction-scale, not a second world and not its own map.


### System (operator text — not a Prefer, not Gate A)

Generation writes records. The sim advances them when nobody is looking. A kingdom is a faction holding: settlements that already exist, roles, treasury, unrest, edicts. It is not a nameplate and not a second game. Decals, salt lore, and paint-as-terrain are refuses. The operator is called for landform, history, routes, weather, and an edict. Every other row in this section is a probe.

### Walk (operator text — B2 may report gaps; nobody stamps this done)

1. `WB-gen-landform` — Generate. Read relief, water, climate, rivers, biomes. Change a dial that claims to affect the landform and generate again. The output changes. A painted ramp fails.
2. `WB-gen-history` — Read a multi-step history. Edit one line. Reload. The edit is authored, not generated.
3. `WB-gen-routes` — With sites present, routes exist that nobody drew. A hand-drawn route is only an override.
4. `WB-sim-weather` — Read weather at a place. Advance the clock. It changed. Tone bias and the weather dial are both visible in the result.
5. `WB-fact-edict` — On a kingdom that is a faction holding, set an edict or an unrest figure. The write is authored on the ledger. It does not become a generated history line. No kingdom minigame menu.
6. Do not F5 the `none` rows: civs, sites, economies, legends, monster tags, import, NPC agendas, the faction graph, the kingdom record, the kingdom turn, price ticks, unobserved change. Each probe must show a stored fact and, where the row says so, a cause. A later person row that uses a price or a site does not re-close these rows.

| Ticket | Status | Product job | Notes | Observe | Touch |
|--------|--------|-------------|-------|---------|-------|
| `WB-gen-landform` | `open` | Foundation — Create World produces a readable landform on the polygon substrate: relief, water, climate, rivers, and biomes with mechanical tags, and the dials that claim to change it actually change it. | Substrate for sites, not the product. Old `GEN-terrain-product` / `GEN-tone` / `GEN-biomes` cites are prior art only. Paint-ramp-as-success is a refuse. | `person` | `f5` |
| `WB-gen-history` | `open` | Foundation — The world generates a multi-step history the GM can read and edit, and an edited line persists as an authored fact distinct from a generated line. | Old `GEN-history` was deferred on the mini-game and never built. Not done. | `person` | `f5` |
| `WB-gen-civ` | `open` | Foundation — Civilizations and peoples generate as records tied to regions and sites, with goals a later sim can pursue. | Not a name list. No off-screen action required in this ticket; `WB-sim-factions` owns the running graph. | `record` | `none` |
| `WB-gen-sites` | `open` | Foundation — Settlements, ruins, lairs, and wilderness generate as openable records placed from bounds and history, not as decals. | Do not reuse ticket id `GEN-sites` or join `alpha0_gen_sites_r1`. That Prefer is prior art on the deferred map. | `record` | `none` |
| `WB-gen-economy` | `open` | Foundation — Each settlement generates an economy: production, stock, trade links, and prices, including prices a spellcaster would pay for materials. | Series child `ux_economy_resources`, `ux_economy_trade`. The diamond-price rail has nothing to read until this exists. | `record` | `none` |
| `WB-gen-legends` | `open` | Foundation — The GM can read a legend that states a cause-and-effect chain from generated history through to a site, people, or price, and can jump to those records. | Legends are derived, not a separate short-story button. Series child `ux_wa_timelines`, `ux_wa_lore_articles`. | `record` | `none` |
| `WB-gen-monsters` | `open` | Foundation — Regions carry monster and habitat tags as data the encounter tools can query; the tags are not combatants and not a fight. | Feeds section H. Mass combat may query the tags later; this row does not build armies. Old `GEN-monsters` prior art only. | `record` | `none` |
| `WB-gen-routes` | `open` | Foundation — Routes between sites are generated when sites exist; drawing them by hand is an optional override, not the only way they appear. | Old `GEN-roads` prior art only. | `person` | `f5` |
| `WB-import-canon` | `open` | Foundation — A GM can import an offline history canon bundle into the world document and see it become world facts, or the import is refused with a reason. | Not the mini-game stub, and not a KEEP inherited from `alpha0_world_import_r2`. | `record` | `none` |
| `WB-sim-weather` | `open` | Foundation — Weather advances on the world clock and is readable at a place, and campaign tone and the weather dial change it. | Pin family Phase-3-1-2 (supporting; primary sim pin is the tick core). Series child `ux_sim_weather_pulse`. | `person` | `f5` |
| `WB-sim-npc` | `open` | Foundation — NPCs have agenda and schedule records that move when the clock advances, and the GM can read them without opening a dialogue wheel. | Series children `ux_wa_npc_agenda`, `ux_wa_npc_sheet`, `ux_wa_npc_relations`, `ux_wa_npc_secrets`. Pin [[Phase-3-1-3-NPC-Agendas-Subsystem-Roadmap-2026-06-29-2330]] as supporting. | `record` | `none` |
| `WB-sim-factions` | `open` | Foundation — Faction graph (goals, hierarchy, territory, reputation) advances off-screen while a campaign looks elsewhere, and the change is stored even if no GM has the site open. | Pin [[Phase-3-2-Off-Screen-Faction-Tribe-Activity-Roadmap-2026-06-26-1615]]. Series `ux_living_world_continuity`. Distinct from `WB-gen-civ`, which only creates the records. | `record` | `none` |
| `WB-fact-kingdom` | `open` | Foundation — A kingdom is a faction-scale record on an existing faction: holdings, roles, and treasury tied to settlements that already exist. | Not a second world and not a nameplate on the faction. Sits on `WB-sim-factions` and `WB-gen-sites`. | `record` | `none` |
| `WB-fact-kingdom-turn` | `open` | Foundation — While unobserved, a kingdom turn can change holdings, unrest, or treasury, and the change is stored on the faction graph with a cause. | Same clock as `WB-sim-factions`. A kingdom minigame menu is a fail. | `record` | `none` |
| `WB-fact-edict` | `open` | Foundation — The GM can set or strike an edict, a holding, or an unrest figure in cheat mode; the write is authored, ledgered, and does not become generated history. | Uses `WELD-overwrite-ledger`. Pairs with `WB-auth-override`. | `person` | `f5` |
| `WB-sim-economy-tick` | `open` | Foundation — Prices, stock, and trade move on the world clock when no campaign is looking, and a later inspection shows the new value and why it moved. | This is what makes a live diamond price a world fact rather than a note. | `record` | `none` |
| `WB-sim-unobserved` | `open` | Foundation — A GM can leave the world, advance time, return, and find civilization, faction, economy, and weather changes that were not hand-authored. | Stranger test for “the world runs.” Cause links must be openable via `WB-gen-legends` / `CONT-cause-chain`. | `record` | `none` |
## C — Anno authoring and inspection

Cheat mode means the GM does not fight the interface. Overrides are recorded. They are not silent rewrites of history.


### System (operator text — not a Prefer, not Gate A)

Cheat mode is immediate place, edit, query, override, region regen, settlement edit, and bulk, on the committed solid. One overwrite ledger serves place, regen, prep handoff, and live light-edit. World inspection does not require a campaign. Campaign inspection labels world facts and campaign secrets apart. Cause is openable. Zoom from world to building does not load a second scene.

### Walk (operator text — B2 may report gaps; nobody stamps this done)

1. `WB-auth-place` — Place a site from the polygon view. The solid that stays is the one just placed, not a ghost. A neighbor update does not delete it.
2. `WB-auth-edit` — Change name, type, price, owner, or tag. Reload. The scope is the one `CAMP-scope-split` would show.
3. `WB-auth-query` — Ask the price of a named good in a settlement, and who holds a region. The answer is the record. An essay or a hidden guess fails.
4. `WB-auth-override` — Override a sim result. A later tick keeps the override until it is cleared. It is marked authored.
5. `WB-auth-region` — Regenerate one region. An override outside it survives.
6. `WB-auth-settlement` — Open a settlement and edit economy, sites, and people with the same verbs. No loading screen.
7. `WB-auth-bulk` — Multi-select, apply one labeled operation, undo that operation as one step.
8. `WB-insp-world` — With no campaign open, read clock, civ, economy, weather, and factions.
9. `WB-insp-cause` — From one of those facts, open the cause and jump to a parent. Empty "because the world" fails.
10. `WB-nest-zoom` — World, region, settlement, building, by zoom or selection, on the desk and on the rail. No load.
11. Do not F5 `WELD-overwrite-ledger`, `WB-auth-undo`, or `WB-insp-campaign`. Probes own the single ledger, undo of place/generate/override/price, and the labeled campaign split.

| Ticket | Status | Product job | Notes | Observe | Touch |
|--------|--------|-------------|-------|---------|-------|
| `WELD-overwrite-ledger` | `open` | Weld — Place, region regen, prep handoff, and live light-edits all write one overwrite ledger that stays visually distinct from generated history. | Pin [[Phase-3-3-DM-Overwrite-vs-Deliberate-Re-Generation-Policy-Roadmap-2026-06-26-1630]]. One ledger so the three modes cannot invent three histories. | `record` | `none` |
| `WB-auth-place` | `open` | Foundation — From the polygon view the GM can place a site, route, or region feature immediately, see the committed solid (not a different ghost), and have that fact survive neighbor updates. | Anno cheat-mode. Old `PLACE-product` Prefer is prior art only; do not join it. | `person` | `f5` |
| `WB-auth-edit` | `open` | Foundation — The GM can edit a world or campaign fact in place (name, type, price, owner, tag) and the edit persists in the correct scope. | Scope comes from `CAMP-scope-split`. | `person` | `f5` |
| `WB-auth-query` | `open` | Foundation — The GM can ask a direct question (“price of diamonds in this settlement”, “who holds this region”) and get the record, not a search essay and not a hidden guess. | Explicit query. Smart search may assist; it may not replace the labeled query. | `person` | `f5` |
| `WB-auth-override` | `open` | Foundation — The GM can override a sim result; the override is marked as authored, survives a later tick unless cleared, and does not pretend to be generated history. | Uses `WELD-overwrite-ledger`. | `person` | `f5` |
| `WB-auth-region` | `open` | Foundation — The GM can select a region and stamp, clear, or deliberately regenerate it; local overrides outside that region survive. | Pairs with `CONT-regen-survive`. | `person` | `f5` |
| `WB-auth-settlement` | `open` | Foundation — The GM can open a settlement and edit its economy, sites, and people with the same cheat-mode verbs, without a loading screen. | Nest is data, not a second game. | `person` | `f5` |
| `WB-auth-bulk` | `open` | Foundation — The GM can multi-select and apply one labeled operation (stamp, delete, reseed, retag) and undo that operation as one step. | Cheat mode includes bulk. One-at-a-time only is a fail. | `person` | `f5` |
| `WB-auth-undo` | `open` | Foundation — Undo and redo cover place, generate, override, and a history or price edit. | Hotkey-only with no visible undo is a fail. | `record` | `none` |
| `WB-insp-world` | `open` | Foundation — The GM can inspect world-level sim state (clock, civ, economy, weather, factions) without entering a campaign. | Foundation inspection. Campaign filters are off in this seat. | `person` | `f5` |
| `WB-insp-campaign` | `open` | Weld — With a campaign selected, the same inspection shows campaign-owned deltas and secrets beside world facts and labels which is which. | Prep and live rail both use this split. | `record` | `none` |
| `WB-insp-cause` | `open` | Foundation — From any inspected fact the GM can open the cause chain (what tick, legend, or override produced it) and jump back to the parents. | Empty “because the world” copy is a fail. | `person` | `f5` |
| `WB-nest-zoom` | `open` | Weld — The GM can go world → region → settlement → building by zoom or selection with no loading screen, in both the authoring desk and the live rail. | Old `LOOP-inspect` prior art only. Same polygon world (`WELD-one-world`). | `person` | `f5` |
## D — Dial surface

Every row is a labeled, persistent control on `DIAL-W-surface` or its campaign / live companions. A hidden smart default that the GM cannot see and set is a fail for that row. Do not merge these rows.


### System (operator text — not a Prefer, not Gate A)

Every dial family is its own labeled, persistent control. A hidden smart default is not a control. Campaign overrides store on the campaign and do not rewrite the world default or any other campaign. Live filters hide or dim; they do not delete. The light-edit ceiling is what the rail is allowed to change. Merging two families onto one slider fails both rows. Kingdom and mass combat do not add a buried dial.

### Walk (operator text — B2 may report gaps; nobody stamps this done)

1. `DIAL-W-surface` — Every world dial in this section is visible and named on the world. There is no mode whose only control is an unlabeled default.
2. For each other `f5` row in this section — Find it by its label. Set it off the default. Cause the effect that row names. Reload. The value is still set. If the row is a campaign override, the world default is unchanged and a second campaign is unchanged.
3. `DIAL-C-override` — Override one world dial on campaign A. Campaign B and the world default stay put. The override is labeled.
4. `DIAL-L-edit-ceiling` — Set the rail ceiling to read-only, then to light edit. The rail obeys. It does not become a second authoring desk.
5. Do not F5 `DIAL-W-tone-default`, `DIAL-W-density`, `DIAL-C-tone`, `DIAL-L-filters`, or `DIAL-L-persist`. Those are `none`. Probes must show the stored value changing generation, tone consumption, or filter output. A screenshot of a slider does not close them.
6. `PROOF-dials` is the stranger pass of this section. It is not a substitute for closing each row, and this Walk is not that proof's Prefer.

| Ticket | Status | Product job | Notes | Observe | Touch |
|--------|--------|-------------|-------|---------|-------|
| `DIAL-W-surface` | `open` | Foundation — Every world dial in this section is visible, named, and saved on the world; there is no mode where the only way to change behavior is an unlabeled default. | Contract for the families below. Precise and autistic users are the acceptance test: the mechanism stays on the surface. | `person` | `f5` |
| `DIAL-W-tone-default` | `open` | Foundation — The world has a default tone profile of exactly one of High Fantasy, Medium Fantasy, Low Fantasy, or Grimdark, and generation, weather, and sim defaults consume it. | Pin [[Phase-2-3-ToneProfile-Profile-Bundle-on-World-Seed-Roadmap-2026-06-26-1535]]. No fifth profile. Campaign override is `DIAL-C-tone`, not a rewrite of this default. | `record` | `none` |
| `DIAL-W-density` | `open` | Foundation — The GM can set site, population, and encounter density, and a new generate or region regen reflects the value. | Stored number with unchanged output is a fail. | `record` | `none` |
| `DIAL-W-consequence` | `open` | Foundation — The GM can set how hard world changes scar factions, economies, and places, and an off-screen advance shows a lighter or heavier scar. | Series `ux_living_world_continuity` amplitude. Not a cosmic-death-only switch. | `person` | `f5` |
| `DIAL-W-scent` | `open` | Foundation — The GM can set how strongly clues, rumors, and legends advertise causes, and inspection of the same fact yields more or less scent as the dial moves. | Actual-play pattern `WB` information scent is a thickener only. The dial is the product. | `person` | `f5` |
| `DIAL-W-seed` | `open` | Foundation — The GM can lock, inspect, and reroll the world seed, and a reroll is an explicit action that does not happen because a menu closed. | Inspectable seed. Hidden reseed is a fail. | `person` | `f5` |
| `DIAL-W-pressure` | `open` | Foundation — The GM can set an encounter pressure curve over world time or travel, and planned encounters read that curve instead of a flat random. | Feeds `PF-encounter-budget`. | `person` | `f5` |
| `DIAL-W-faction-reactivity` | `open` | Foundation — The GM can set how fast factions answer insults, losses, and opportunities, and an off-screen advance shows a faster or slower answer. | Distinct from `DIAL-W-offscreen-rate`, which sets how often the sim steps, not how sharp each answer is. | `person` | `f5` |
| `DIAL-W-scarcity` | `open` | Foundation — The GM can set resource scarcity, and settlement stocks and prices move with it. | Feeds economy and treasure. | `person` | `f5` |
| `DIAL-W-economy` | `open` | Foundation — The GM can set price volatility and stickiness, and two advances of the same shock produce a jumpy or a sticky price accordingly. | The diamond example must be dialable, not only simulated. | `person` | `f5` |
| `DIAL-W-history-tempo` | `open` | Foundation — The GM can set how fast history and civilizations move and how verbose legends are, without changing the off-screen step rate by a second hidden knob. | If this and `DIAL-W-offscreen-rate` ever share one control, this ticket fails. | `person` | `f5` |
| `DIAL-W-offscreen-rate` | `open` | Foundation — The GM can set how often unobserved sim steps run relative to the world clock. | Pairs with `WB-sim-unobserved`. | `person` | `f5` |
| `DIAL-W-weather` | `open` | Foundation — The GM can set weather harshness independently of the tone profile’s bias, and the weather sim shows the override. | Tone may suggest a default. The dial must still be settable. | `person` | `f5` |
| `DIAL-W-magic-density` | `open` | Foundation — The GM can set magic density as its own labeled control; tone may propose the initial value and may not hide this control. | Prevents “it’s just in the tone bundle” from burying the mechanism. | `person` | `f5` |
| `DIAL-W-visual-noise` | `open` | Foundation — The GM can set how much incidental polygon detail and motion the world view uses, and the live flight view obeys it. | Even the low-fidelity layer has a sensory dial. Not an art-upgrade ticket. | `person` | `f5` |
| `DIAL-W-sensory-load` | `open` | Foundation — The GM can set a sensory-load ceiling (flash, shake, audio density, simultaneous labels) that both the desk and the live rail obey. | Explicit accessibility control. A buried “reduce motion” OS guess is not this ticket. | `person` | `f5` |
| `DIAL-W-reveal-pace` | `open` | Foundation — The GM can set how fast prep-staged reveals become eligible to surface in play. | Does not auto-reveal secrets. Visibility law stays in `PREP-visibility`. | `person` | `f5` |
| `DIAL-W-moral-fork` | `open` | Foundation — The GM can set how sharp moral forks are (how hard the world scars either choice) without forcing a single betrayal plot. | Actual-play moral-fork cards are thickeners. One conspiracy skin is a fail (`ux_living_world_continuity`). | `person` | `f5` |
| `DIAL-W-loyalty-decay` | `open` | Foundation — The GM can set loyalty and trust decay and recovery rates, and an NPC or faction record shows the rate that applies. | Not a single global “everyone hates you” switch. | `person` | `f5` |
| `DIAL-W-soft-exit` | `open` | Foundation — The GM can set how available walk-away, flee, and silence exits are, as data later prep and play can honor. | Pattern `WB-control-surface-mapping`: soft-exit is a verb, not a cancel button. This ticket stores the dial; `RAIL-soft-exit` performs the live exit. | `person` | `f5` |
| `DIAL-W-canon-strictness` | `open` | Foundation — The GM can set how quickly a proposed intent may move through `proposed → accepted → hooked → sim-active`, and the pipeline UI shows the gate that is currently required. | Series child `ux_canon_pipeline_feel`. Auto-sim-active with no visible gate is a fail. | `person` | `f5` |
| `DIAL-W-story-operator` | `open` | Foundation — The GM can set the mix of human-operated story versus sim-operated reaction, and prep shows which beats are GM-steered, sim-proposed, or both. | Pattern `WB-human-operated-story`. Dialogue-wheel-only is a fail at any mix. | `person` | `f5` |
| `DIAL-W-mythic-weight` | `open` | Foundation — The GM can set mythic weight off or on by degree, and encounter and continuity tools gain or hide mythic fields accordingly. | Off must stay a clean Pathfinder 1E table, not a disabled mythic UI left in the way. | `person` | `f5` |
| `DIAL-W-quiet-density` | `open` | Foundation — The GM can set how much quiet-between (camp, road, linger) the world and prep suggest between pillars. | Series `ux_quiet_between_pillars`. Pattern `WB-quiet-between-pillars`. Not “press rest to refill.” | `person` | `f5` |
| `DIAL-W-session-clock` | `open` | Foundation — The GM can set whether the world sim pauses, single-steps, or keeps advancing while a session is live, and the live rail shows which policy is in force. | The diamond price must still be readable under pause. A running price under “advance” must show as of the current tick. | `person` | `f5` |
| `DIAL-C-override` | `open` | Weld — For a selected campaign the GM can override any world dial; the override is labeled, stored on the campaign, and does not change the world default or any other campaign. | Campaign-specific overrides. Hidden inheritance is a fail. | `person` | `f5` |
| `DIAL-C-tone` | `open` | Prep — At Session 0 the GM sets that campaign’s ToneProfile to one of the four profiles; prep, weather bias, and sim defaults for that campaign consume it. | Series `ux_tone_profile_surface`. Does not regenerate the world. | `record` | `none` |
| `DIAL-C-known-mask` | `open` | Weld — The GM can set what the cast is treated as knowing versus what the GM can inspect; live filters and prep visibility can use that mask. | GM omniscience stays available. The mask never blinds the GM. | `person` | `f5` |
| `DIAL-C-power-band` | `open` | Prep — The GM can set the campaign’s power band (early, mid, late) and off-screen costs and encounter pressure respect it. | Series `ux_early_game`, `ux_mid_game`, `ux_late_game` as targets. Band is explicit, not inferred only from average party level. | `person` | `f5` |
| `DIAL-L-filters` | `open` | Weld — During inspection and on the live rail the GM can toggle labeled filters for economy, faction, history, site type, campaign delta, known-to-party, and sensory load, and the polygon view shows only what those filters allow. | Live-inspection family. Filters dim or hide; they do not delete facts. | `record` | `none` |
| `DIAL-L-persist` | `open` | Weld — Live filter choices persist per campaign and per session and are listed somewhere the GM can clear them. | A filter that resets on every rail pop without a visible reason is a fail. | `record` | `none` |
| `DIAL-L-edit-ceiling` | `open` | Weld — The GM can set what a live-rail edit is allowed to change (read-only, light edit, or handoff into deep prep) and the rail enforces that ceiling. | Prevents the rail from becoming a second hidden authoring mode, or from being too weak to fix a price. | `person` | `f5` |
## E — Camera and control contracts

These rigs serve both the deep desk and the live rail. MapCam is not a tilted WorldCam. Sensorium does not grant control.


### System (operator text — not a Prefer, not Gate A)

WorldCam, MapCam, and Sensorium are three rigs used by the desk and the rail. MapCam is a separate plane-locked orthographic rig, not a tilted WorldCam. Sensorium is read-only and never moves the creature. Players never receive WorldCam. Cheat verbs and rail verbs are two labeled sets. "Interact" as the only verb is a fail.

### Walk (operator text — B2 may report gaps; nobody stamps this done)

1. `CAM-worldcam` — Orbit, pan, zoom, tilt, soar, and dive. Use the same rig in authoring and in live flight. No player path grants it.
2. `CAM-mapcam` — Switch to the orthographic rig. Pan and yaw on the horizontal plane. Tilting WorldCam does not satisfy the switch.
3. `CTRL-region-verb` — A major GM action shows its screen region, its verb, and whether it is always-on, ephemeral, or mode-only.
4. `CTRL-cheat-vs-rail` — The active set is labeled. A bulk regen from the live set is refused unless the edit ceiling allows it.
5. Do not F5 `CAM-sensorium` or `CAM-transition`. Probes own attach, read-only, exit to the prior rig, creature unmoved, and a refused illegal hop that names the guard.

| Ticket | Status | Product job | Notes | Observe | Touch |
|--------|--------|-------------|-------|---------|-------|
| `CAM-worldcam` | `open` | Weld — The GM can free-fly the polygon world: orbit, pan, zoom, tilt, soar, and dive, and can use that rig for both deep authoring and live flight. | Series `ux_dm_worldcam`. Pin [[Phase-4-1-3-WorldCam-MapCam-and-SensoriumAttach-FOV-Roadmap-2026-07-16-0845]]. Players never receive this rig. Old `DESK-cam` prior art only. | `person` | `f5` |
| `CAM-mapcam` | `open` | Foundation — The GM can switch to a separate map-fixed orthographic rig that pans and yaws on the horizontal plane for measurement and long authoring, and tilting WorldCam does not count as this rig. | Series `ux_dm_mapcam`. Distinct frame of reference. | `person` | `f5` |
| `CAM-sensorium` | `open` | Weld — The GM can attach a read-only view to a creature’s perception to answer “what can they sense?”, then exit to the previous WorldCam or MapCam, and the attach never moves that creature. | Series `ux_dm_sensorium`. Not DM pilot. Agency delegation stays out of this map. | `record` | `none` |
| `CAM-transition` | `open` | Weld — WorldCam, MapCam, Sensorium, deep desk, and live rail have an explicit transition graph the GM can see; an illegal hop is refused with the guard that blocked it. | Pin [[Phase-4-2-1-TransitionGuardRegistry-and-DM-Session-Authority-Roadmap-2026-07-16-0456]]. Comfort interpolation is allowed; conflating rigs is not. | `record` | `none` |
| `CTRL-region-verb` | `open` | Weld — Each major GM action declares a screen region, an input verb, and a persistence (always-on, ephemeral, or mode-only) and those declarations are visible in the control surface. | Pattern `WB-control-surface-mapping`. “Interact” as the only verb is a fail. | `person` | `f5` |
| `CTRL-cheat-vs-rail` | `open` | Weld — Anno cheat verbs and live-rail verbs are two labeled sets on the same world; the GM can tell which set is active and cannot fire a bulk regen from the live set unless the edit ceiling allows it. | Depends on `DIAL-L-edit-ceiling`. | `person` | `f5` |
## F — Live rail stack

Do not collapse this section into one ticket. Canonical scene: session is live; the GM needs the price of diamonds in a dwarf kingdom; they enter the rail, fly, click, read or lightly edit, and leave; the table is still in the same scene.


### System (operator text — not a Prefer, not Gate A)

The rail is eleven seats. The scene is one: a session is live, the GM needs the price of diamonds in a dwarf settlement, they enter the rail, cross the polygon world, click, read or lightly edit, and leave, and the initiative is the same. Collapsing the stack into one ticket is a refuse. The rail is not the prep workbench. Flight and click are probes on this map, not a second F5 piled onto the diamond row.

### Walk (operator text — B2 may report gaps; nobody stamps this done)

1. `RAIL-economy` — From a click on a settlement, read prices and stocks, including diamonds. A light edit happens only if the ceiling allows it.
2. `RAIL-faction` — From that same path, open goals, standing, and territory. Light edit stays inside the ceiling.
3. `RAIL-history` — From that path, open history and the cause chain. A history edit hits the overwrite ledger.
4. `RAIL-site` — From that path, open type, occupants, tags, and linked encounters. Deep encounter edit is not this seat.
5. `RAIL-light-edit` — Return to the desk. The rail edit is visible as authored, in the right scope.
6. `RAIL-soft-exit` — Leave by a short labeled exit. Same scene, no load, no forced recap.
7. Do not F5 `RAIL-session-contract`, `RAIL-flight`, `RAIL-click`, `RAIL-campaign-filter`, or `RAIL-not-workbench`. Probes own same initiative after return, a flight that is not menu-teleport-only, click-without-leaving-the-rail, this campaign's mask only, and no dump into the workbench.

| Ticket | Status | Product job | Notes | Observe | Touch |
|--------|--------|-------------|-------|---------|-------|
| `RAIL-session-contract` | `open` | Prep — While a session is running the GM can enter the live rail and later return, and initiative, scene, whose turn, and open rolls are the same as when they left. | Enter/exit contract. Pin [[Phase-4-2-3-DM-Rail-Chrome-and-DMRailUXContract-Roadmap-2026-07-16-0653]]. A rail that saves-and-quits the fight is a fail. | `record` | `none` |
| `RAIL-flight` | `open` | Weld — On that rail the GM can move across the polygon world with WASD or an equivalent free-flight control and reach a distant settlement without a menu teleport being the only path. | Uses `CAM-worldcam`. Menu jump may exist as a labeled extra; it is not the flight. | `record` | `none` |
| `RAIL-click` | `open` | Weld — The GM can click a settlement, site, or region under the flight camera and open its inspection surface without leaving the rail. | Click-to-inspect. A full workbench takeover fails this ticket (see `RAIL-not-workbench`). | `record` | `none` |
| `RAIL-economy` | `open` | Weld — From that click the GM can read a settlement’s prices and stocks, including a material such as diamonds, and can make a light edit if the edit ceiling allows. | Depends on `WB-gen-economy`, `WB-sim-economy-tick`, `DIAL-L-edit-ceiling`. The canonical diamond case. | `person` | `f5` |
| `RAIL-faction` | `open` | Weld — From the same flight and click path the GM can open the faction surface for that place (goals, standing, territory) and apply a light edit only inside the ceiling. | Depends on `WB-sim-factions`. Not a second navigation app. | `person` | `f5` |
| `RAIL-history` | `open` | Weld — From the same path the GM can open history and legends for that place and see the cause chain. | Depends on `WB-gen-history` and `WB-gen-legends`. Light edit of a history line writes the overwrite ledger. | `person` | `f5` |
| `RAIL-site` | `open` | Weld — From the same path the GM can open the site record (type, occupants, tags, linked encounters) and lightly edit allowed fields. | Encounter deep-edit stays in prep. This ticket is inspect plus light edit. | `person` | `f5` |
| `RAIL-campaign-filter` | `open` | Weld — Rail filters and the known-to-cast mask apply to the campaign that owns the live session; switching nothing under the hood cannot show another campaign’s secrets. | Depends on `DIAL-L-filters`, `DIAL-C-known-mask`, `CAMP-select`. | `record` | `none` |
| `RAIL-light-edit` | `open` | Weld — A light edit made on the rail is written to the overwrite ledger, scoped correctly, and visible as authored when the GM returns to the desk. | No silent sim rewrite. Depends on `WELD-overwrite-ledger`. | `person` | `f5` |
| `RAIL-soft-exit` | `open` | Prep — The GM can leave the rail by a short, labeled exit and land back in the live session without a hard stop, a loading break, or a forced recap. | Soft-exit. Distinct from `DIAL-W-soft-exit`, which stores how available fiction exits are. | `person` | `f5` |
| `RAIL-not-workbench` | `open` | Weld — The rail never dumps the GM into the full prep workbench; opening deep prep is a separate, labeled choice that still does not tear down the session. | Keeps Fantasy Grounds-class live use from becoming World Anvil-class authoring by accident. | `record` | `none` |
## G — Session prep flows

Prep is the star. It consumes the foundation. It does not create the world, does not replace the campaign frame, and is not an offline app. The accelerator rows at the bottom of this table are `session-prep-accelerator-loop`. They do not make prep a ritual. `PREP-gate` still refuses prep when no campaign is selected. `PREP-optional` refuses a gate that blocks play until prep is finished.


### System (operator text — not a Prefer, not Gate A)

Prep is the depth bar and an optional accelerator. It does not create the world or the campaign frame. With a campaign selected, the GM can do long pre-session work on the polygon world, review what the world did between sessions, stage visibility, hand world-hitting edits through the DM gate, run Session 0, and export a package that still points at world records. From table history the system distills a few patterned branches. The GM selects or overrides. Recaps, when used, come from player logs and do not leak DM secrets. Slow surfaces are managed here; large changes are regen or ledger, not silent rewrites. Play with zero prep must still be coherent. The workbench is DM-facing. Player graphics of the recap are out.

### Walk (operator text — B2 may report gaps; nobody stamps this done)

1. `PREP-gate` — Choose prep with no campaign. Refused. Sent to select or create.
2. `PREP-deep` — With a campaign selected, read sim state, place or override, stage beats, review secrets, on the polygon world. No wiki.
3. `PREP-between` — Between sessions, read what the world did and what this campaign changed. Accept, reject, or revise one item.
4. `PREP-session0` — Set bounds, tone, shared intents, and DM accept-or-revise. The world does not regenerate. Character creation does not open.
5. `PREP-continuity-delta` — Read world motion, campaign-owned changes, and costs the cast could notice. The machinery is visible to the GM. Player-facing graphics of that residue are not this step.
6. `PREP-optional` — Start or continue play with an empty prep queue. The world is still coherent. A "finish prep to play" gate fails.
7. `PREP-branches` — Mark an arc. Get a small set of branches from table history, not a map of every path. Select one, rewrite one, override one. It does not feel like a second game.
8. `PREP-warm-handoff` — Enter the table. Queued branches, pressures, agents, floated knowledge, and location are loaded. The GM is not forced to re-explain the world from memory.
9. `PREP-recap-player` — Generate a recap. It quotes player notes or logs. A planted DM-only secret is absent. Generating no recap is allowed.
10. `PREP-stable-surfaces` — Adjust a slow surface between sessions. A large change is an explicit regen or a ledgered override.
11. `PREP-hirelings` — Set hireling loyalty or staffing on the campaign. No player character is created. A branch can quote that record.
12. Do not F5 the `none` rows in this section (`PREP-workbench`, `PREP-visibility`, `PREP-batch-handoff`, `PREP-opening`, `PREP-bootstrap`, `PREP-human-story`, `PREP-quiet`, `PREP-ordinary-rhythm`, `PREP-export`, `PREP-history-return`, `PREP-pressure-sources`). Probes own anchored notes, per-player visibility, the DM gate, opening authorship, session start, non-wheel social staging, quiet beats, ordinary advancement, package links, history write-back, and pressure rows that quote existing seats instead of inventing a minigame per noun.

| Ticket | Status | Product job | Notes | Observe | Touch |
|--------|--------|-------------|-------|---------|-------|
| `PREP-gate` | `open` | Prep — Choosing session prep with no campaign selected is refused and the GM is sent to select or create one. | Enforces `CAMP-select`. Series `ux_dm_session_prep`: prep does not create the campaign frame. | `person` | `f5` |
| `PREP-deep` | `open` | Prep — With a campaign selected the GM can spend a long pre-session sitting on the polygon world: read sim state, place and override, stage beats, and review secrets, without a separate wiki. | World Anvil-class depth on the substrate. Series `ux_dm_session_prep`. | `person` | `f5` |
| `PREP-workbench` | `open` | Prep — The GM has a workbench for lore, beats, and continuity that is anchored to world and campaign records, not a free-floating document the sim cannot see. | Series child `ux_dm_workbench_lore_gui`. Unlinked notes may exist only as drafts until attached. | `record` | `none` |
| `PREP-between` | `open` | Prep — Between sessions the GM can review what the world did and what this campaign already changed, then accept, reject, or revise before the next session. | Star pressure on `WB-sim-unobserved` and `PREP-continuity-delta`. | `person` | `f5` |
| `PREP-visibility` | `open` | Prep — Each staged fact is unmarked (secret) unless the GM opts into whole-table and/or per-player visibility. | Series law on `ux_dm_session_prep`. A single whole-table tag as the only control is a fail. | `record` | `none` |
| `PREP-batch-handoff` | `open` | Weld — World-hitting prep edits batch and enter the world only through the DM gate and the overwrite / regen rules; prep cannot sneak a world change around that gate. | Series does-not-mandate: prep is not a back door. Depends on `WELD-overwrite-ledger` and `DIAL-W-canon-strictness`. | `record` | `none` |
| `PREP-session0` | `open` | Prep — Session 0 for a campaign, in tool, sets table bounds, tone, shared intents, and DM accept-or-revise, and it never regenerates the world and never owns character creation. | Series `ux_session0_bootstrap` inside `ux_dm_campaign_creation`. Canon pipeline starts here. Offline Microscope play is not required. | `person` | `f5` |
| `PREP-opening` | `open` | Prep — The GM can author the opening situation, temporary constraints, and multi-path goals for session 1 or session N as prep, and that authorship is not a separate product mode. | Series `ux_dm_session_prep`: opening is prep, not another series parent. A single captivity start is not the default. | `record` | `none` |
| `PREP-bootstrap` | `open` | Prep — The GM can start the live session from the prepared state and land in the table frame with that state loaded. | Pin [[Phase-6-1-1-Launch-Flow-and-DevLeakageGuard-Session-Bootstrap-Roadmap-2026-06-27-0406]] is supporting only. Dev-leakage chrome is not the product. | `record` | `none` |
| `PREP-human-story` | `open` | Prep — Social beats can be staged as GM soft framing plus room for a player move the GM did not list; a three-button dialogue wheel cannot be the only social tool. | Pattern `WB-human-operated-story`. Depends on `DIAL-W-story-operator`. | `record` | `none` |
| `PREP-quiet` | `open` | Prep — The GM can stage camp, road, and linger beats that keep fiction continuous between combat, social, and exploration, and rest is not only a resource button. | Series `ux_quiet_between_pillars`. Pattern `WB-quiet-between-pillars`. | `record` | `none` |
| `PREP-ordinary-rhythm` | `open` | Prep — The GM can stage ordinary advancement (a new option, a small reputation shift, a tool the next fight will feel) without a mythic set-piece. | Pattern `WB-ordinary-progression-rhythm`. Mythic weight may be off. | `record` | `none` |
| `PREP-continuity-delta` | `open` | Prep — The GM can read a between-session delta for this campaign: world motion, campaign-owned changes, and costs the cast could notice, with machinery visible to the GM. | Series `ux_living_world_continuity`. Players-feel-residue is out of this map except as notes the GM can mark visible. | `person` | `f5` |
| `PREP-export` | `open` | Prep — The GM can hand off a prepared session package that the same campaign can run at full fidelity: beats, encounters, visibility, dials in force, and links into world records. | Not a PDF of notes. A package that loses site links or dial overrides fails. | `record` | `none` |
| `PREP-optional` | `open` | Prep — The GM can start or continue a session with zero formal prep, and the world stays coherent. A gate that blocks play until prep is finished is a fail. | Feedstock `session-prep-accelerator-loop`. Does not weaken `PREP-gate`: prep still requires a campaign; play does not require prep. | `person` | `f5` |
| `PREP-branches` | `open` | Prep — From a marked arc and table history, the GM gets a small set of patterned branches and can select, rewrite, or override them, and is not handed an exhaustive map of every path. | Distill, do not simulate every future. Flavor or skin is not a second game. DM-facing. | `person` | `f5` |
| `PREP-warm-handoff` | `open` | Prep — Starting play loads queued branches, current pressures, active agents, floated knowledge, and location, so the GM is not forced to re-explain the world from memory. | Refuse: cold start. Not a cutscene. Not the dev-leakage chrome in `PREP-bootstrap`. | `person` | `f5` |
| `PREP-recap-player` | `open` | Prep — When a recap is generated, it is built from player notes or logs, and a planted DM-only secret does not appear in it. | DM-facing tool. No recap is legal. Player-facing graphics of the recap stay out of this map. | `person` | `f5` |
| `PREP-stable-surfaces` | `open` | Prep — Between sessions the GM can manage slow surfaces (economy, institutional weather, ecological pressure), and a large change is an explicit regen or ledgered override, not a silent rewrite. | Real-time adjustment stays possible and is the exception for large shifts. Does not create a second economy beside `WB-gen-economy`. | `person` | `f5` |
| `PREP-history-return` | `open` | Prep — Confirmed outcomes, residue, and state changes are written back into history so the next branch pass can quote them. | Not a second chronicle. Campaign-owned returns stay campaign-owned until `PREP-batch-handoff`. | `record` | `none` |
| `PREP-hirelings` | `open` | Prep — The GM can keep hireling loyalty and staffing on the campaign without creating player characters, and a branch can quote that record. | Not character creation. Not `CAMP-cast-seam` by itself. | `person` | `f5` |
| `PREP-pressure-sources` | `open` | Prep — The branch distiller can read labeled pressure rows the GM can set: background residual, lingering conditions, monster vacuum, trap residue, hireling loyalty, treasure heat, pantheon or institutional weather, apex pressure, holdings, and capacity. A missing source is an empty list, not a fabricated plot. | One record shape, many labels. A minigame per noun is a fail. Seats that already exist stay the owners of those facts; this row only requires they can be quoted. | `record` | `none` |
## H — Pathfinder 1E wave

Not one row. These are the surfaces a GM needs to run real Pathfinder 1E encounters, exploration, social play, downtime, adjudication, and continuity, with mythic weight only when the dial says so. They sit on the world; they are not a side binder.

The rules family is one engine: `PF-rules-engine`, `PF-ruleset-bind`, `PF-options-bind`, `PF-house-rule`, and `PF-spell-gate`. Homebrew, option switches, and spell allow or ban are rows here, not a different map and not a notes field. Mass combat is not in this family. It is section I.


### System (operator text — not a Prefer, not Gate A)

One Pathfinder 1E rules surface serves prep and the live table. The GM can see which options are on, can write a house rule the surface actually applies, and can ban or allow spells on a list. Encounters belong to polygon sites. Mythic controls appear only when the mythic dial is above off. Adjudication shows inputs. Confirming the end of a session writes a campaign delta; world-hitting pieces wait on the gate. This section is not mass combat and not kingdom turns.

### Walk (operator text — B2 may report gaps; nobody stamps this done)

1. `PF-options-bind` — Set the option switches. Read them back. An empty set is not everything-on. The world does not regenerate.
2. `PF-house-rule` — Write a house rule. Resolve a case it covers. The result names the house rule, not the book rule hiding under a note.
3. `PF-spell-gate` — Ban one spell. Read the list. A cast of that spell does not resolve as legal.
4. `PF-encounter-site` — Attach an encounter to a polygon site. A floating encounter with no site fails.
5. `PF-encounter-budget` — Set APL, CR, and XP. The pressure dial's suggestion is visible and overridable.
6. `PF-roster` — Place creatures with stats the engine can use. A monster-region tag does not auto-fill a fight the GM did not accept.
7. `PF-spellcasting` — Inspect slots and material components. A component price can be read from the settlement economy.
8. `PF-exploration` — Adjudicate perception, stealth, light, or travel against the polygon place, weather, and the scent dial.
9. `PF-knowledge` — Adjudicate a knowledge check. The GM sees the roll inputs and what the scent dial would reveal.
10. Do not F5 the `none` rows (engine, ruleset bind, hazards, treasure, initiative, combat math, conditions, social, downtime, resources, rest, mythic, ruling log, continuity write). Probes own inputs-and-result, the bind, and the refuse of hidden automation. Looking at a fight does not close `PF-combat-adjudicate`.

| Ticket | Status | Product job | Notes | Observe | Touch |
|--------|--------|-------------|-------|---------|-------|
| `PF-rules-engine` | `open` | Foundation — The selected campaign can resolve Pathfinder 1E checks (d20, BAB, saves, skills, AC, CMB/CMD, spells, conditions) through an explicit rules surface that prep and the live table both call. | Pin [[Phase-5-1-Rule-Engine-Primitives-and-Plugin-Hooks-Roadmap-2026-06-26-2045]]. A notes field that says “roll high” is a fail. One ruleset binding, not a second engine inside prep. | `record` | `none` |
| `PF-ruleset-bind` | `open` | Weld — The campaign frame shows that it is bound to Pathfinder 1E, and world tags (biome, monster region, scarcity) are readable by that ruleset. | Clean-slate bind. Old `PACK-rules-tags` prior art only. | `record` | `none` |
| `PF-options-bind` | `open` | Foundation — The GM can set which Pathfinder 1E options this campaign's rules surface will accept, and can read that set back; an empty set is not everything on. | World building and Session 0 may both set it. Does not regenerate the world. Distinct from a house rule and from a spell ban. | `person` | `f5` |
| `PF-house-rule` | `open` | Foundation — The GM can write a house rule the same rules surface applies, labeled as house, and a resolution shows that house rule instead of silently keeping the book rule under it. | Same engine as `PF-rules-engine`. A note that says "we play it this way" and is never called is a fail. | `person` | `f5` |
| `PF-spell-gate` | `open` | Foundation — The GM can allow or ban spells on a list they can read. A banned spell does not resolve as a legal cast. The full book does not stay secretly legal. | Greenlight and blacklist. Component prices stay `PF-spellcasting`. | `person` | `f5` |
| `PF-encounter-site` | `open` | Prep — The GM can attach an encounter to a polygon site so the fight has a place, a terrain, and a parent settlement or wilderness record. | Floating encounter with no site fails. | `person` | `f5` |
| `PF-encounter-budget` | `open` | Prep — The GM can see and set APL, CR, and XP budget for that encounter, and the pressure dial’s suggestion is visible and overridable. | Depends on `DIAL-W-pressure` and `DIAL-C-power-band`. | `person` | `f5` |
| `PF-roster` | `open` | Prep — The GM can place creatures on that encounter with stats the rules engine can use, plus tactics notes and terrain tags. | Monster-region tags may suggest; they do not auto-fill a fight the GM did not accept. | `person` | `f5` |
| `PF-hazards` | `open` | Prep — The GM can author traps, haunts, and hazards on a site with trigger, effect, and disable information the rules engine can adjudicate. | Not a sticker on the polygon. | `record` | `none` |
| `PF-treasure` | `open` | Weld — The GM can place or generate treasure and see it against local prices and the scarcity dial, then override either number. | Depends on `WB-gen-economy` and `DIAL-W-scarcity`. | `record` | `none` |
| `PF-spellcasting` | `open` | Prep — The GM can prepare or inspect spell lists, slots, and material components for combatants, and component prices can be read from the settlement economy. | Live rail may show a component price; this ticket is the prep and adjudication surface. | `person` | `f5` |
| `PF-initiative` | `open` | Prep — During a live session the GM can run initiative and turn order, and that tracker is still there after a rail pop and soft exit. | Depends on `RAIL-session-contract`. Fantasy Grounds-class bar for this seat. | `record` | `none` |
| `PF-combat-adjudicate` | `open` | Prep — During a fight the GM can adjudicate attacks, damage, spells, and maneuvers on the combatants in the encounter, with the rules engine showing the inputs and the result. | Series `ux_combat_play_surface`. Hidden “the computer decided” with no inputs is a fail. | `record` | `none` |
| `PF-conditions` | `open` | Prep — The GM can apply, read, and expire conditions with duration on combatants, and those conditions survive into the next beat of the same session. | Includes ongoing world scars only when written through continuity, not by accident. | `record` | `none` |
| `PF-exploration` | `open` | Prep — The GM can adjudicate exploration (perception, stealth, light, travel time) against the polygon place, weather, and scent dial. | Not a hex-map clone unless the polygon distances are the source. | `person` | `f5` |
| `PF-social` | `open` | Weld — The GM can adjudicate social checks against NPC attitude and faction reputation, and still record a player move that was not on a list. | Depends on `PREP-human-story` and `WB-sim-factions`. Series children `ux_wa_faction_reputation`, `ux_wa_npc_dialogue_hooks`. | `record` | `none` |
| `PF-knowledge` | `open` | Weld — A knowledge check can be adjudicated against legends and information scent, and the GM sees both the roll inputs and what the dial would reveal. | Depends on `DIAL-W-scent` and `WB-gen-legends`. | `person` | `f5` |
| `PF-downtime` | `open` | Weld — The GM can resolve downtime (craft, earn, recover, train) against the economy and loyalty rules, and the results can write a campaign delta. | Not the kingdom rows and not mass combat. Those are `WB-fact-kingdom` and section I. This seat is craft, earn, recover, and train only. | `record` | `none` |
| `PF-resources` | `open` | Prep — The GM can track party wealth and consumables for the campaign cast seam, priced where relevant from the living economy. | Uses `CAMP-cast-seam`. Does not create characters. | `record` | `none` |
| `PF-rest` | `open` | Prep — The GM can run a rest as both a rules refill and a quiet-between beat, and lingering conditions and story residue are still there afterward. | Depends on `PREP-quiet`. Refill-only is a fail. | `record` | `none` |
| `PF-mythic` | `open` | Prep — When mythic weight is above off, the GM can track mythic tier, path, and surge for combatants; when it is off, those controls are not in the way. | Depends on `DIAL-W-mythic-weight`. | `record` | `none` |
| `PF-ruling-log` | `open` | Prep — Every adjudication can be accepted, overridden, or deferred, and the choice is appended to a ruling log the GM can reread next session. | No hidden automation as the only path. Overrides hit `WELD-overwrite-ledger` when they change world or campaign facts. | `record` | `none` |
| `PF-continuity-write` | `open` | Weld — When the session ends, HP, conditions, wealth, reputation, and story awards the GM confirms write a campaign delta, and world-hitting pieces wait on the DM gate. | Depends on `PREP-batch-handoff`. Sheet-only memory is a fail. | `record` | `none` |

## I — Mass combat

Its own family. Not a large `PF-encounter-site`, not a kingdom turn, and not a second rules engine. Armies belong to factions and stand on the polygon. A pass shows inputs and a result. A confirmed outcome can change territory or population only through the same gate as any other world-hitting write.

### System (operator text — not a Prefer, not Gate A)

The GM defines an army on a faction and a region, places a field that is not a skirmish, and can have one mass-combat pass resolved with the inputs showing. Aftermath is a ledgered faction and campaign delta, not a skipped scene that repaints the map. Single-creature Pathfinder combat stays in section H.

### Walk (operator text — B2 may report gaps; nobody stamps this done)

1. `MASS-army` — Define an army or unit on a faction and a polygon region, with size and stance. A copied skirmish roster scaled up fails.
2. `MASS-field` — Place a mass battle: sides, terrain, objective. `PF-encounter-site` does not satisfy this.
3. Do not F5 `MASS-resolve` or `MASS-aftermath`. Probes own a pass that shows inputs and result, and a confirmed write that waits on the DM gate. "The computer decided" fails the resolve probe. A silent territory rewrite fails the aftermath probe.

| Ticket | Status | Product job | Notes | Observe | Touch |
|--------|--------|-------------|-------|---------|-------|
| `MASS-army` | `open` | Foundation — The GM can define an army or unit on a faction and a polygon region, with size and stance the mass rules can query. | Not a skirmish roster scaled up. The parent is the faction, not a new world. | `person` | `f5` |
| `MASS-field` | `open` | Prep — The GM can place a mass battle on the polygon: sides, terrain, and an objective, distinct from a single Pathfinder encounter. | `PF-encounter-site` does not satisfy this row. The field is a place. | `person` | `f5` |
| `MASS-resolve` | `open` | Prep — A mass-combat pass can be adjudicated and the rules surface shows the inputs and the result. | Not "the computer decided." Not a single-creature attack macro. Same honesty bar as `PF-combat-adjudicate`. | `record` | `none` |
| `MASS-aftermath` | `open` | Weld — A confirmed mass-combat outcome can write faction territory, population, and a campaign delta, and world-hitting pieces wait on the DM gate. | Uses `PREP-batch-handoff` and `WELD-overwrite-ledger`. A skipped scene that rewrites the map fails. | `record` | `none` |

## J — Continuity and the session hand-off


### System (operator text — not a Prefer, not Gate A)

World history and the campaign chronicle are two labeled streams. Unobserved motion is listable. A visible change can be walked back to a tick, a legend, or an override, and edited only through the ledger. Regional regen does not eat keeps outside its scope. Costs on return match the campaign power band, and the band in force is shown.

### Walk (operator text — B2 may report gaps; nobody stamps this done)

1. `CONT-cause-chain` — From a visible change, walk to a parent. Stop. Edit only through the ledger.
2. Do not F5 `CONT-offscreen-read`, `CONT-regen-survive`, `CONT-two-histories`, or `CONT-power-band`. Probes own the unobserved list, regen survival, the two streams, and a shown power band whose costs match it.

| Ticket | Status | Product job | Notes | Observe | Touch |
|--------|--------|-------------|-------|---------|-------|
| `CONT-offscreen-read` | `open` | Foundation — The GM can list what factions, economies, and places did while unobserved, with a time range and a link to each record. | Pin [[Phase-3-2-Off-Screen-Faction-Tribe-Activity-Roadmap-2026-06-26-1615]]. | `record` | `none` |
| `CONT-cause-chain` | `open` | Foundation — The GM can walk from a visible change back through ticks, legends, and overrides to a cause, and can stop at any parent and edit only through the ledger. | Shared by desk, prep, and rail. | `person` | `f5` |
| `CONT-regen-survive` | `open` | Foundation — A deliberate regional regeneration rewrites only that region’s generated facts; overrides and edits outside it, and overrides inside it that the GM marks keep, survive. | Pin [[Phase-3-3-DM-Overwrite-vs-Deliberate-Re-Generation-Policy-Roadmap-2026-06-26-1630]]. | `record` | `none` |
| `CONT-two-histories` | `open` | Weld — World history and the campaign chronicle stay two labeled streams; a campaign’s public recap does not become world canon unless the GM hands it across the gate. | Series chronicle seam on the campaign frame. `ux_backstory_legacy_integration` is a neighbor, not this ticket’s owner. | `record` | `none` |
| `CONT-power-band` | `open` | Weld — Readable costs on return match the campaign power band: early stays local, mid can scar a region, late can threaten the campaign’s scale, and the band in force is shown. | Series `ux_living_world_continuity` plus early/mid/late series. The GM sees the machinery. | `record` | `none` |
## K — Fidelity proofs

These are product proofs of the combined surface, not engine unit tests. Each one fails if a stranger cannot watch the GM do the sentence.


### System (operator text — not a Prefer, not Gate A)

These are stranger sentences for the combined surface, not engine unit tests. Each proof closes on its own. A proof does not mark the rows it depends on done. `PROOF-pf1e-night` is a probe. The others are operator F5s. Mass combat has its own proof and is not required for the night proof.

### Walk (operator text — B2 may report gaps; nobody stamps this done)

1. `PROOF-two-campaigns` — A stranger watches two campaigns in one world. Shared history. Secrets and dial overrides do not cross.
2. `PROOF-df-anno` — A stranger watches an unobserved advance, then a cheat place or override. Legend and ledger both show generated versus authored. A kingdom edict is not required for this proof.
3. `PROOF-dials` — A stranger watches every section D family found, named, changed, saved, reloaded, and campaign-overridden. A missing family fails.
4. `PROOF-pre-session` — A stranger watches campaign select, Session 0 tone, an economy read, a Pathfinder encounter on a site, a quiet beat, and an export.
5. `PROOF-live-diamond` — A stranger watches enter, fly, diamond price read or light edit, soft exit, same initiative.
6. `PROOF-export-fidelity` — A stranger watches the package start in the same campaign and still show site, dial overrides, visibility, and prices from export time.
7. `PROOF-mass` — A stranger watches an army on a region, one mass-combat pass with inputs visible, and a territory or population change that is caused or authored.
8. Do not F5 `PROOF-pf1e-night`. A probe owns the fight, the unlisted social move, the exploration check, the downtime or rest residue, and the confirmed delta. Mythic fields appear only if the dial is on.

| Ticket | Status | Product job | Notes | Observe | Touch |
|--------|--------|-------------|-------|---------|-------|
| `PROOF-two-campaigns` | `open` | Weld — A stranger watches the GM run two campaigns in one world, switch between them, and show that world history is shared while secrets and dial overrides are not. | Depends on section A and `CONT-two-histories`. | `person` | `f5` |
| `PROOF-df-anno` | `open` | Foundation — A stranger watches a generated world advance unobserved, then watches the GM cheat-place or override a site, and the legend and ledger both show what was generated and what was authored. | Depends on sections B and C. | `person` | `f5` |
| `PROOF-dials` | `open` | Foundation — A stranger watches the GM find, name, change, save, reload, and campaign-override every dial family in section D without hunting through unmarked defaults. | Fails if any family is missing from the surface. | `person` | `f5` |
| `PROOF-pre-session` | `open` | Prep — A stranger watches the GM select a campaign, set Session 0 tone, read the economy, author a Pathfinder encounter on a site, stage a quiet beat, and export a session package. | Star proof, pre-session. | `person` | `f5` |
| `PROOF-live-diamond` | `open` | Weld — A stranger watches a live session, the GM enter the rail, fly to a dwarf settlement, read or lightly edit the diamond price, soft-exit, and resume the same initiative. | Canonical live-rail proof. All section F seats required. | `person` | `f5` |
| `PROOF-pf1e-night` | `open` | Prep — A stranger watches one Pathfinder 1E slice that includes a fight, a social beat with a move that was not prelisted, an exploration check, and a downtime or rest residue, then a campaign delta written on confirm. | Mythic fields appear only if the dial is on. | `record` | `none` |
| `PROOF-export-fidelity` | `open` | Prep — A stranger watches the exported package start inside the same campaign and still show the encounter’s site, the dial overrides, the visibility tags, and the prices that were current at export. | `PREP-export` is not done until this proof can pass. | `person` | `f5` |
| `PROOF-mass` | `open` | Weld — A stranger watches the GM put a faction army on a region, resolve one mass-combat pass with inputs visible, and read a territory or population change that is caused or authored. | Depends on section I and `WB-sim-factions`. Not required for `PROOF-pf1e-night`. | `person` | `f5` |
## L — Deferred art

Pointable polygon solids are already required in `WB-polygon-substrate`. This row is the reskin, not the product.


### System (operator text — not a Prefer, not Gate A)

The polygon substrate is already a product seat. This section is the seam that a later reskin must honor, and the reskin itself, which stays deferred until the first real-gap seat has operator F5. A visual change that rewrites sim, dials, or verbs fails the seam. Mint must not pick the reskin.

### Walk (operator text — B2 may report gaps; nobody stamps this done)

1. `WB-art-seam` — Read the sim, dial, and control contracts the reskin must honor. A note that says art may change a sim result fails.
2. Do not build `VIS-ard-reskin`. It stays `deferred`. Do not author a Prefer for it.

| Ticket | Status | Product job | Notes | Observe | Touch |
|--------|--------|-------------|-------|---------|-------|
| `VIS-ard-reskin` | `deferred` | Foundation — An artist or later agent can replace polygon materials and meshes with a richer look without changing sim results, dial values, or control verbs. | ARD polish. Not launchable until the first real-gap seat on this map has operator F5. Never first. Old `VIS-water-polish`, `VIS-style`, `VIS-variants` are prior art on the deferred mini-game, not this row’s KEEP. | `person` | `f5` |
| `WB-art-seam` | `open` | Foundation — Sim, dial, and control contracts are documented as the stable surface that `VIS-ard-reskin` must honor, and a visual change that requires a sim rewrite fails this ticket. | The seam is work now. The pretty picture stays deferred. | `person` | `f5` |
---

## Status policy

- Every capability row is `open` except `VIS-ard-reskin`. None are `f5_good`.
- `VIS-ard-reskin` is the only `deferred` row, so mint cannot pick it. Touch `f5` does not make it eligible.
- `Touch` is `f5` exactly when `Observe` is `person`, and `none` exactly when `Observe` is `record`.
- System and Walk are operator text. Gate A must not copy them into a Prefer. Gate B2 may report a gap against a Walk step and must not stamp the Walk done.
- `WB-polygon-substrate` stays `open`. It is the first Prefer. Failed Prefer/weld attempts live only under `4-Archives` (`wb-polygon-substrate-ticket-and-weld-scrapped-*`, `wb-polygon-substrate-r4-lookup-shell-rejected-*`, `wb-polygon-substrate-r5-pre-observe-gates-rejected-*`, `wb-polygon-substrate-r6-label-check-rejected-*`, `wb-polygon-substrate-r7-print-flag-b1-refused-*`, `wb-polygon-substrate-r8-incomplete-until-robot-retired-*`, and Prefer chain). Align virgin. Do not Prefer-join archives.
- Old Prefer / weld ids (archived `wb-polygon-substrate-prefer-retired-*`, `wb-polygon-substrate-r1-superseded-*`, `wb-polygon-substrate-r2-retired-*`, `wb-polygon-substrate-r3-scope-cut-rejected-*`, `wb-polygon-substrate-ticket-and-weld-scrapped-*`) are not candidates. Do not Prefer-join them.
- Active Prefer: `alpha0_wb_polygon_substrate_r9` (`observer: operator`, `observer_when: after_build`, empty checks). Gate A + B₁ green; factory `armed_slice_id` set / stageable. `factory_greenlit` false until operator GREENLIGHT. Do not Prefer-join archived polygon attempts (r1–r8).
- Sibling `world-builder-mini-game` stays deferred. Do not arm it. Do not extend that id.

## Decisions locked (2026-10-30)

These were the open questions. They are not open.

1. **Sibling map.** `world-builder-mini-game` stays deferred. Do not Prefer-join it.
2. **Art.** `VIS-ard-reskin` stays `deferred`. Every other row stays `open`.
3. **Kingdom and mass combat.** In this map. Kingdom is three rows under factions in section B, not a second simulation. Mass combat is section I. Downtime is neither.
4. **Rules engine.** Stays on this map. Option switches, house rules, and spell allow or ban are rows in the same family. Not a map this one only binds. Not folded into `PF-rules-engine` as one blob.
5. **Accelerator.** `session-prep-accelerator-loop` is feedstock. Section G tickets it. Nothing past the pasted doctrine was added.
6. **Player-facing residue.** Out. GM-side notes and a player-log recap are in. Player graphics of either are out.
7. **First Prefer.** `WB-polygon-substrate`. Not a later seat. Not `GEN-sites`.

No `wait:<ticket>` cell was added. Touch is only `f5` or `none`, matched to Observe, so a later row cannot become a piled-up F5 of earlier spines. Say if that pointer is still wanted.

Arrangement can still be rejected without reopening the decisions: kingdom as three faction rows, mass combat as four rows plus `PROOF-mass`, rules family as three new rows beside the engine, accelerator as eight rows. Split or merge if that grouping is wrong.
