# Conceptual / PMG excerpt (feedstock)

_Source: `/home/darth/Documents/Second-Brain/1-Projects/genesis-mythos-master/genesis-mythos-master-goal.md`_

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

- **`ToneProfile`** — one bundled profile per campaign (chosen at session 0), consumed by **world gen**, **weather**, **sim defaults**, **lore/event tone**,

…
