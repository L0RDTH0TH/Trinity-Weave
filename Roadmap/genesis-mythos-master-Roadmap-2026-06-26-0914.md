---
title: genesis-mythos-master Roadmap
roadmap-level: master
phase-number: 0
project-id: genesis-mythos-master
status: active
priority: high
progress: 0
progress_rollup: aggregate_deferred
created: 2026-06-26
tags: [roadmap, project, genesis-mythos-master, genesis-mythos]
para-type: Project
links:
  - "[[genesis-mythos-master-Roadmap-MOC]]"
roadmap_generation_status: complete
---

# genesis-mythos-master Roadmap

> [!info] Generation provenance
> Generated from `[[genesis-mythos-master-goal]]` on `2026-06-26T09:14:11.000Z`
> Mode: ROADMAP_MODE (greenfield gen-test-3, godot lane)
> Guidance: Greenfield factory launch — master + 6 phases + MOC from PMG; preserve canonical PMG at project root; then product factory conductor.
> Intent confidence: high

> [!note] Master progress rollup (`progress_rollup: aggregate_deferred`)
> Master `progress: 0` is intentional on conceptual_v1: phase primaries may reach `progress: 100` at breadth-complete without rolling up to the master note until execution-track factory attestation (ROADMAP_FACTORY_RELAUNCH Half A) or explicit advance-phase rollup. Reconciled 2026-06-27 IRA verify (`architect-rm-gmm-gree-d61f36aa`).

Source: [[genesis-mythos-master-goal]]

## Phase 1 — Conceptual Foundation and Core Architecture

Establish the modular blueprint for immersion, collaboration, and extensibility on Godot 4.6.3 .NET. Decouple world state, simulation, rendering, and input; outline the procedural generation graph and intent population pipeline; identify modularity seams and embed seed-snapshot safety invariants.

```dataview
TABLE WITHOUT ID roadmap-level AS "Level", file.link AS "Note", subphase-index AS "Index", status, progress AS "%"
FROM "1-Projects/genesis-mythos-master/Roadmap/Phase-1-Conceptual-Foundation-and-Core-Architecture"
WHERE roadmap-level = "primary" OR roadmap-level = "secondary" OR roadmap-level = "tertiary"
SORT subphase-index ASC, file.name ASC
```

## Phase 2 — Procedural Generation and World Building

Collaborative forge for emergent worlds from shared intents. Build seed parsing through terrain, biomes, POIs, and simulation bootstrap; canon registry and intent resolver; ToneProfile on world seed from session 0.

```dataview
TABLE WITHOUT ID roadmap-level AS "Level", file.link AS "Note", subphase-index AS "Index", status, progress AS "%"
FROM "1-Projects/genesis-mythos-master/Roadmap/Phase-2-Procedural-Generation-and-World-Building"
WHERE roadmap-level = "primary" OR roadmap-level = "secondary" OR roadmap-level = "tertiary"
SORT subphase-index ASC, file.name ASC
```

## Phase 3 — Living Simulation and Dynamic Agency

Persistent simulation with DM authority: tick-based weather, NPC agendas, off-screen faction activity, DM overwrites vs deliberate re-generation, consequence graphs weighted by ToneProfile.

```dataview
TABLE WITHOUT ID roadmap-level AS "Level", file.link AS "Note", subphase-index AS "Index", status, progress AS "%"
FROM "1-Projects/genesis-mythos-master/Roadmap/Phase-3-Living-Simulation-and-Dynamic-Agency"
WHERE roadmap-level = "primary" OR roadmap-level = "secondary" OR roadmap-level = "tertiary"
SORT subphase-index ASC, file.name ASC
```

## Phase 4 — Perspective Split and Control Systems

Role-tailored views: player FP baseline, perspective and agency envelopes, DM WorldCam / MapCam / read-only Sensorium Attach, pilot graph for dominate and absent-proxy, unified scene graph with swappable camera interpolator.

```dataview
TABLE WITHOUT ID roadmap-level AS "Level", file.link AS "Note", subphase-index AS "Index", status, progress AS "%"
FROM "1-Projects/genesis-mythos-master/Roadmap/Phase-4-Perspective-Split-and-Control-Systems"
WHERE roadmap-level = "primary" OR roadmap-level = "secondary" OR roadmap-level = "tertiary"
SORT subphase-index ASC, file.name ASC
```

## Phase 5 — Rule System Integration and Extensibility

Plugin rule engine with agency and perspective spell metadata; quest pressure from canon graph; swap-in modules and documented community seams.

```dataview
TABLE WITHOUT ID roadmap-level AS "Level", file.link AS "Note", subphase-index AS "Index", status, progress AS "%"
FROM "1-Projects/genesis-mythos-master/Roadmap/Phase-5-Rule-System-Integration-and-Extensibility"
WHERE roadmap-level = "primary" OR roadmap-level = "secondary" OR roadmap-level = "tertiary"
SORT subphase-index ASC, file.name ASC
```

## Phase 6 — Prototype Assembly, Testing, and Iteration

Dual track: factory spine (catalog, operator-attested scopes) vs horizon demo (~30 min gameplay loop). Factory Phase 0 presentation shell; horizon demo v1; defer full proc-gen and multiplayer.

```dataview
TABLE WITHOUT ID roadmap-level AS "Level", file.link AS "Note", subphase-index AS "Index", status, progress AS "%"
FROM "1-Projects/genesis-mythos-master/Roadmap/Phase-6-Prototype-Assembly-Testing-and-Iteration"
WHERE roadmap-level = "primary" OR roadmap-level = "secondary" OR roadmap-level = "tertiary"
SORT subphase-index ASC, file.name ASC
```

## Related

- [[genesis-mythos-master-Roadmap-MOC]]
- [[genesis-mythos-master-goal]]
