---
title: Genesis Mythos Master Goal
created: 2026-06-24
tags:
  - project
  - genesis-mythos
  - master-goal
para-type: Project
project-id: genesis-mythos-master
status: active
is_master_goal: true
links:
  - "[[3-Resources/Second-Brain/Docs/Roadmap-Factory-Pipeline|Roadmap-Factory-Pipeline]]"
  - "[[3-Resources/Second-Brain/Docs/Five-Factories-Trail|Five-Factories-Trail]]"
---

# Genesis Mythos Master Goal

## One-line

Build an open-source, monetizable, aggressively modular first-person 3D VTT generator that procedurally creates living, collaborative open worlds from shared DM and player intents — mandatory in-tool session 0, visible world continuity, player-lite legacies and chronicle — players in first-person by default with rules-driven perspective and agency envelopes, DMs on a dedicated rail (WorldCam, map-fixed Tabletop MapCam, read-only Sensorium Attach), player lore woven into systemic depth, major structural changes via intentional re-generation, every layer built for community remixing.

## Vision

**Perspective split** delivers immersion for players and commanding mastery for the DM.

- **Players default to first-person** — immediate, personal, experiential. No casual third-person orbit or free tactical camera for players.
- **Perspective overrides** (Scry/Clairvoyance, divination, astral travel, DM-granted visions, unconscious/liminal states, etc.) are **explicit, temporary, rules-bound** departures from baseline FP — not a permanent camera mode. Overrides use contract-defined presentation (remote fixed POV, sensory UI, liminal states) and **always return to FP** when the effect ends. Third-person **character orbit is out of scope** as default exploration; polymorph and similar effects stay **FP from the new body**.
- **Agency delegation (player rail)** — separate from DM adjudication attach. **Who may issue intents** for an entity is rules- or session-bound:
  - **Dominate (player dominator)** — when a player casts Dominate Monster/Person (or equivalent), the dominator **pilots the target** — FP and control from the dominated body. A core **virtual VTT advantage** over physical tabletop (direct embodiment, not menu-only command).
  - **Dominate (victim)** — dominated PC: presentation policy is spell-bound (e.g. passenger FP with locked input, liminal UI); exact default locked at Phase 5 spell metadata.
  - **Absent-player proxy** — session policy allows a delegate (another player or DM) to **pilot** an absent PC with explicit handoff when the owner returns.
  - **Enter/exit** — every delegation declares controller, victim presentation, duration, and clean return to `agency: self` + baseline FP.
- **DM perspective rail** (players never use this rail for WorldCam/MapCam):
  - **WorldCam (Sparky)** — free flight in world space: orbit, pan, zoom, tilt, soar, dive.
  - **Tabletop MapCam** — **map-fixed orthographic plane** (Anno / Civilization / Cities: Skylines style): camera translates and rotates **on the horizontal map plane** with orthographic projection; tokens, measurements, fog, LOS adjudication. **Not** “tilt the world-cam to top-down” — separate rig, separate frame of reference. Sparky-like responsiveness but **plane-locked** (pan on map, yaw, zoom; no soar/dive off the plane).
  - **Sensorium Attach (read-only)** — DM binds **sight** to an entity’s perception rig (monster, NPC, or player) to adjudicate LOS, awareness, and “what do they see?” — **no intent/control transfer** on the DM rail. Compare multiple viewpoints for ruling. Operator debug attach uses the same read-only contract. Always **exit back** to prior DM mode (WorldCam or MapCam).
  - **DM pilot** — when rules or session policy puts the DM in control of an entity (e.g. NPC dominate, absent PC), that uses the **agency delegation** system (pilot envelope), not Sensorium Attach. DM may pilot with FP from that body where the spell/session declares it.
  - Mode switches may interpolate for comfort; **MapCam and WorldCam remain distinct rigs** with an explicit transition graph (Phase 4).

**World continuity** — players tied to a living world.

- **Primary goal:** show that **actions change the world** — visibly, between sessions, not only in the current scene.
- Factions, tribes, and threads from player/DM intents are **canon entities** with history and goals — **active off-screen** while PCs are elsewhere, or **gone with a recorded cause** that can be explored.
- **Lore and narrative stay emergent** (not hardcoded plot). **Systems** are in scope: intent population pipelines, reputation and consequence graphs, dynamic event triggers, feedback loops where choices reshape simulation over sessions.
- Hooks ripple through NPCs, events, and environment — haunted villages, rival bloodlines, prophecy fragments — so quests integrate with the world graph, not generic fetch loops.

**Collaborative canon & session bootstrap.**

- **Session 0 (required, in-tool):** world bootstrap before campaign play — table bounds, **campaign tone profile** (see below), player intents, DM/table accept or revise canon. Collaborative-history patterns (shared eras, legacies, non-linear threads) are **Microscope-informed** — see [[Ingest/Microscope PDF]] — **not** dependent on playing a separate RPG. Optional offline history may **import** as a canon bundle (power-user path).
- **Canon pipeline:** `proposed → accepted → hooked → sim-active` — intents become facts, then systemic hooks, then visible ripples and quest pressure.

**Campaign tone profiles** — one session-level vibe that biases every subsystem (Palette for *how* the world feels, not plot).

Core set (**four only for now**; optional tags/modifiers deferred):

| Profile | Vibe (reference) | System bias |
|---------|------------------|-------------|
| **High Fantasy** | Wonder, abundant magic (Eberron-like) | Exotic biomes, high magic density, wondrous weather mix |
| **Medium Fantasy** | Default adventure table — magic present, bounded | Functional societies, balanced intrigue + adventure |
| **Low Fantasy** | Grounded, rare dangerous magic | Muted world, political human-scale conflict |
| **Grimdark** | Moral gray, harsh consequences (Witcher-like) | Bleak weather bias, costly hope, persistent scars |

- **`ToneProfile`** — one bundled profile per campaign (chosen at session 0), consumed by **world gen**, **weather**, **sim defaults**, **lore/event tone**, and **quest framing** — not siloed presets per subsystem.
- Profiles are **defaults**, not stereotypes; table Palette can veto elements.

**Player & DM surfaces.**

| Surface | Role |
|---------|------|
| **Player-lite** | Intent inbox (backstory, tribe, artifact, quest seed) · **My Legacies** (canon ripples — tribe status, threads, “since you left…”) · **Last session** recap · **My chronicle** (personal notes by session, search) · optional export/mirror for note-taking players. **Not** timeline editing, contradiction resolution, or sim admin. |
| **DM workbench** | Full canon graph, faction/tribe off-screen activity, accept/revise intents, quest integration from active hooks. |

Keep three **data buckets** distinct in UX: **world ripples** (system/DM canon) · **session chronicle** (table recap) · **personal archive** (player-owned notes — may disagree with canon).

**The world pulses with life, customization, and balanced agency.**

- Layered simulation: weather, NPC agendas, ambient surprises, persistent scars from play — **weighted by campaign tone profile**.
- **DM overwrites:** in-session tweaks (tokens, weather, events, whispers) vs. deliberate re-generation for terrain reshaping or biome relocation.
- Extensibility: swap simulation flavors, visual styles, rule behaviors, and **tone profiles** without breaking cohesion.

**Open source and aggressive modularity** — every system (generation stages, simulation ticks, camera controllers, input loops) replaceable via clear interfaces.

**Generation is collaborative dialogue** between intents and machine: DM and players feed seeds; the system proposes scaffolds refined through choice loops.

### Delivery goals (three layers)

Build the modular system; ship one solid Medium Fantasy **Reference Exemplar** you can run a full campaign in; make every major layer (rules, visuals, content) human-swappable so the Exemplar is the **default fill**, not the only law.

| Layer | Role |
|-------|------|
| **System (primary)** | Modular VTT platform — contracts, envelopes, gates, and **human-usable swap/import structure** (pack bind, preview, attach, update). Structure and patterns for modularity are first-class, not afterthought. |
| **Reference Exemplar (primary secondary)** | Official **Medium Fantasy** pack: coherent chrome + world look + **campaign-capable** worldgen. Solid, not spectacular — play a full campaign here before ripping seams. Graphics for this pack are in scope. Anti-mandate: Exemplar ≠ the only legal product shape. |
| **Operator modularity (primary)** | How DMs replace or extend Exemplar pieces without forking the engine. Pack swap is product responsibility — not modder homework or post-1.0-only. |

**Swap / import (system responsibility).** Slots include rules/calculation packs, tone profile, visual/chrome packs, world visual/biome language, content packs (locations, NPCs, factions), and advanced system modules. Exemplar occupies the official default filled slots. Full matrix and DoD sketches: [[Roadmap/User-Story/REFERENCE-EXEMPLAR-CHARTER|REFERENCE-EXEMPLAR-CHARTER]]. Catalog mint stays capability altitude — do not promote Exemplar chrome to series parents.

**Authority and packages.** Players may customize **character visuals only** (cosmetic; no rules or canon rewrite). **Calculation, lore, homebrew, rules packs, and world-hitting content** are DM-gated on the **world** (campaign hooks may reference world package content but do not become a second rules authority that bypasses world). On **world/campaign invite accept**, the player receives a **bound package** (rules, mods, content, visual defaults for that world/campaign) — not account-global mod soup, not Steam-workshop-on-the-character. Later DM pack revisions **push** to attached players. Invite acceptance installs the DM’s bound package; player cosmetics never substitute for package authority. Cosmetics and backstory never auto-write world canon (DM gate / series anti-mandate unchanged).

Decision stamp: [[Roadmap/Conceptual-Decision-Records/reference-exemplar-dual-goal-2026-08-01|CDR — three-layer delivery]]. Roadmap leaf: Phase **6.4** Reference Exemplar (manual mint; not factory start).

### Operator contract

Constraints for **this generation** — normative factory and stack policy. Architecture: [[3-Resources/Second-Brain/Docs/Five-Factories-Trail|Five-Factories-Trail]].

**Stack & platform (locked)**

- **Godot 4.6.3 .NET** — implementation engine.
- **Linux primary**, Windows secondary (dev, CI smoke, contributor parity).
- **C#** for gameplay and systems; GDScript only at documented interop boundaries.

**Third-party stack (addons, plugins, libraries)**

- PMG defines **stack domains** and **host interfaces** (terrain, camera rig, UI host, editor MCP bridge, rules middleware, etc.) — not specific vendor paths.
- **Selection authority:** addon/plugin/library locks are recorded when Half A mints factory artifacts and stack-domain research ([[Ingest/Agent-Research/Stack-Gaps/|Stack-Gaps]]) informs re-evaluation — **not** in this note alone.
- **Prior vetting may inform, not bind:** earlier research may guide what to re-evaluate; **this generation re-affirms** each lock (license, interop, wrap policy) before it ships in the fresh repo.
- **Modularity rule:** gameplay code talks to **interfaces** (`ICameraRig`, seed authority, intent resolver, …); vendors live under `addons/` or NuGet with documented wrap/adapters.

**Product & repo**

- **One product:** Genesis Mythos — first-person 3D VTT on Godot.
- **Horizon demo proof:** ~30-minute gameplay loop — spawn → explore → intent → sim → rules → DM cam → overwrite → feedback (M0–M8; Phase 6.2). Proves shell + loop wiring — **not** the campaign ceiling.
- **Shippable campaign bar:** Medium Fantasy **Reference Exemplar** (Phase 6.4 + charter) — campaign-capable generated world + coherent pack graphics.
- **Game repo:** vault-local under **`5-Attachments/Code-Repos/`**; factory and CI weld against that tree.

**Five factories (mandatory shape)**

This PMG is **loop 1 only** — vision and phases; it does **not** replace catalog, scopes, or factory beats.

| Factory | Use |
|---------|-----|
| **Knowledge** | Ingest, distill, research — feeds PMG and design notes only |
| **Roadmap (Half A)** | PMG → catalog mint → operator-attested scopes (`L5→target_depth`) → loop-3 slice pick → `factory_staged` |
| **Implementation (Half B)** | Lane seats, Slice Producer, depth bump — welds **catalog rows**, not ad-hoc execution-tree deepen |
| **Queue bus** | EAT-QUEUE on laptop |

**Non-negotiables for generation**

- Factory artifacts (`slice-catalog.yaml`, scopes, `Factory-DRB/`, etc.) are **created through Half A** — not hand-accreted phase trees.
- Loop 2 requires **operator-attested** scope levels; machine-drafted L4–L1 alone does not pass.
- First factory row: presentation shell (`ui_presentation_shell` or successor) — proves lanes before full proc-gen.

## Phases

### Phase 1 — Conceptual Foundation and Core Architecture

Establish the high-level blueprint and modular skeleton: immersion, collaboration, extensibility.

- Decouple world state, simulation, rendering, and input.
- Outline the procedural generation graph and intent population pipeline (seeds, overrides, lore injections).
- Identify modularity seams (generation stages, rule hooks, event bus).
- Embed safety invariants: seed snapshots, dry-run validation.

### Phase 2 — Procedural Generation and World Building

Collaborative forge for emergent worlds — shared intents, not hardcoded narratives.

- Generation pipeline: seed parsing → terrain → biomes → POIs → entities → simulation bootstrap.
- **Canon registry** + intent resolver: faction/tribe registration from session 0; player/DM intents → accepted facts → hooks (reputation, event triggers).
- **`ToneProfile` on world seed** — session 0 choice drives proc-gen, biome/fantasy features, and lore-tone defaults (`data/archetypes/` or equivalent profile bundle).
- Collaborative dialogue: system proposes scaffolds; users refine via choices.

### Phase 3 — Living Simulation and Dynamic Agency

Persistent, balanced elements; DM authority respected.

- Tick-based simulation: weather, NPC agendas, factions, persistent state — **weather and NPC defaults consume `ToneProfile` weights**.
- **Off-screen faction/tribe activity** (tiered fidelity): state advances while PCs are away; **“since you left…”** deltas surfaced to player-lite Legacies.
- DM overwrites vs. deliberate re-generation for major changes.
- Vitality: ambient surprises, consequence graphs, campaign evolution.
- Simulation decoupled from visuals (lightweight previews where useful).

### Phase 4 — Perspective Split and Control Systems

Role-tailored views with seamless transitions.

- Player baseline: first-person + interaction (raycasts, sensory feedback).
- **Perspective envelope:** `baseline_fp → [spell | ability | status] → baseline_fp` — sensory presentation; spell metadata in Phase 5.
- **Agency envelope:** `agency_self → [pilot | dominated | delegated] → agency_self` — who issues intents for an entity. Linked to but distinct from perspective (e.g. dominator **pilots** target with FP from that body; victim may be passenger FP). Session proxy for absent PCs uses the same machinery.
- **DM mode graph:** `WorldCam ↔ MapCam ↔ SensoriumAttach(entity)` — **read-only sight** on DM rail; no control transfer.
- **Pilot graph (player + DM controllers):** rules/session declares `PilotEnvelope(entity, controller, reason)` — dominate, absence proxy, etc.
- Unified scene graph; multiple DM rigs + player rigs on one world state; orchestrator pairs agency + perspective; camera interpolator module (swappable easing).
- Role-based agency: experience vs. dominion.

### Phase 5 — Rule System Integration and Extensibility

RPG mechanics with open-source remixing.

- Core rule engine + primitives; initial ruleset as plugin (hooks, conflict resolution). Spells declare **agency** and **perspective** metadata (e.g. dominate → dominator `pilot_fp` on target; victim `passenger_fp` or liminal — per spell).
- **Quest pressure from canon graph** — integrated quests from active hooks and faction state; not fetch-only encounter tables; **quest moral tone** biased by `ToneProfile`.
- Demonstrate swap-in modules (biome generators, event types).
- Customization via interfaces (visual styles, simulation flavors, input types).
- Document seams for community contribution.

### Phase 6 — Prototype Assembly, Testing, and Iteration

**Three tracks** — do not conflate them.

| Track | Purpose | Authority |
|-------|---------|-----------|
| **Factory (Half A/B)** | Catalog rows, operator-attested scopes, lane implementation, kinesthetic honesty | [[3-Resources/Second-Brain/Docs/Roadmap-Factory-Pipeline\|Roadmap-Factory-Pipeline]] |
| **Horizon demo** | ~30 min playable gameplay loop on Godot (proof loop) | Phase 6.2 / M0–M8 |
| **Reference Exemplar** | Medium Fantasy default pack: campaign-capable gen + coherent graphics; default swap-matrix fill | Phase 6.4 + [[Roadmap/User-Story/REFERENCE-EXEMPLAR-CHARTER\|REFERENCE-EXEMPLAR-CHARTER]] |

- **Factory Phase 0:** First catalog row — presentation shell (launch → PlayRegion → HUD; DM/ortho kinesthetic checklist; no dev-only leakage). Proves factory law before full proc-gen.
- **Horizon demo v1:** Spawn → FP explore → intent stub → sim stub → rule check → DM cam → DM overwrite → feedback. May stub gen for the proof loop.
- **Reference Exemplar:** Requires **campaign-capable** generation + visual pack (consumes Phase 2 contracts). Not a hand-placed slice and not a substitute for system modularity.
- **Still deferred:** Azgaar/WebView, multiplayer (and full push-protocol design beyond invite package + push contracts).

## Technical Integration

- **Procedural core + intent population** — Modular generation graph; intent resolver populates systemic hooks without hardcoding story.
- **Lore canon graph** — entities, legacies, era threads; intent → hook → sim/event; player-lite read paths vs DM write paths; personal chronicle separate from canon truth.
- **`ToneProfile`** — session 0 campaign tone (High / Medium / Low / Grimdark); bundles weights for world gen, weather, sim, lore events, and quest framing via one replaceable profile contract.
- **Living simulation decoupled from rendering** — Tick layer independent of visual engine; re-generation only on explicit structural change.
- **Perspective and agency orchestration** — Unified scene graph; **perspective** (what each role sees) and **agency** (who controls each entity) as paired envelopes. Player rig (FP baseline + overrides); **pilot** (dominator/absent-proxy FP from target body); DM rigs (WorldCam, map-plane MapCam, read-only Sensorium Attach); explicit transition graphs; camera interpolator module.
- **Modularity boundaries** — World-gen stages, rule engine plugins, simulation event bus, intent parser, visual overlay layers; **vendor addons** behind interface wraps per Operator contract (third-party stack).
- **Safety and iteration invariants** — Snapshot seed + overrides + intent state; dry-run before commit; provenance traceable in-game or via export metadata.

## TL;DR

Build the modular system; ship one solid Medium Fantasy **Reference Exemplar** you can run a full campaign in; make rules, visuals, and content human-swappable so the Exemplar is the default fill, not the only law. Players customize character visuals; rules/lore/homebrew stay DM-gated and arrive via world/campaign invite package + DM push. Open-source FP 3D VTT: session 0 + tone profiles, living continuity, player-lite Legacies, DM rail (WorldCam + MapCam + read-only attach), five-factory path. **Godot 4.6.3 .NET on Linux.** Factory Phase 0 proves shell; horizon demo proves the ~30 min loop; Exemplar is the campaign bar (Phase 6.4). Catalog mint = System capability altitude — not Exemplar art inventory.

## Related

- [[3-Resources/Second-Brain/Docs/Roadmap-Factory-Pipeline|Roadmap-Factory-Pipeline]] — Half A → Half B
- [[3-Resources/Second-Brain/Docs/Five-Factories-Trail|Five-Factories-Trail]] — factory architecture
- [[Roadmap/User-Story/REFERENCE-EXEMPLAR-CHARTER|REFERENCE-EXEMPLAR-CHARTER]] — Exemplar DoD + stub swap matrix
- [[Roadmap/Conceptual-Decision-Records/reference-exemplar-dual-goal-2026-08-01|CDR — three-layer delivery]]
- [[Ingest/Microscope PDF]] — collaborative-history design patterns (reference)
- [[Ingest/Agent-Research/Stack-Gaps/|Stack-Gaps research]] — stack-domain vetting for addon selection
- [[Ingest/Agent-Research/Stack-Gaps/gap-stack-intent-lore-loop]] — intent resolver / lore hooks
- [[3-Resources/genesis-mythos-master/Godot-CSharp-Best-Practices/Godot-CSharp-Best-Practices-Study-Guide-MOC|Godot C# Best Practices Study Guide]]
