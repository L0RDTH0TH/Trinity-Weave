---
title: API core-protection inventory — genesis-mythos-master
created: 2026-09-28
updated: 2026-09-28
tags: [genesis-mythos-master, api, modularity, core-protection, inventory]
para-type: Project
project-id: genesis-mythos-master
status: active
roadmap_track: conceptual
links:
  - "[[Conceptual-Decision-Records/api-core-protection-boundary-2026-09-28]]"
  - "[[gmm-api-surface-v0]]"
  - "[[genesis-mythos-master-goal]]"
  - "[[Phase-1-3-1-SeamRegistry-Canonical-Index-Roll-up-2026-06-29]]"
  - "[[REFERENCE-EXEMPLAR-CHARTER]]"
---

# API core-protection inventory

**Single living classification source** for protected core vs API ports vs packs vs provisional slots. Other doctrine surfaces **point here**; they do not restate this table.

CDR: [[Conceptual-Decision-Records/api-core-protection-boundary-2026-09-28]]. Schema: [[gmm-api-surface-v0]].

## Rules (summary)

| Rule | Statement |
|------|-----------|
| **Provisional promotion** | Promote to a real versioned port when a first-party flavor is required by the exemplar loop **or** when a pack swap needs it. Until then: named-only; no direct core reach. |
| **Deeper-access sunset** | Factory/demo deeper binding is temporary and justified. By Phase **6.4** acceptance: remove or promote to a documented **internal-only** port. Public path = API-only. |
| **`propose`** | Always gated by ConflictArbiter / NarrativeDeltaVetoPolicy / overwrite–regen path — never a soft write. |

## Protected core

Never replaceable by community modules. First-party may not rewrite these without a new CDR.

| Module / surface | Notes |
|------------------|-------|
| SessionComposer / LayerGraph / four-layer contracts | WorldState, Simulation, Presentation, InputIntent |
| BusCategoryRegistry + CanonCommitBoundary ownership | Categories + commit lifecycle |
| SimClock / SimTickPipeline / WorldStateCommitter / DMPauseGate | Tick authority |
| PerspectiveEnvelope + AgencyEnvelope | Player/DM perspective + who issues intents |
| DM mode graph (WorldCam / MapCam / SensoriumAttach) + TransitionGuardRegistry | Dual-perspective highlight |
| ReGenerationIntentQueue + DMOverwriteClass + NarrativeDeltaVetoPolicy | Intentional re-gen / overwrite policy |
| RuleEffectBus **ownership** | Plugins subscribe; they do not own the bus |

## API / extension surface (versioned ports)

| Port / family | Layer | Status |
|---------------|-------|--------|
| `gen.stage.*` (terrain → sim_bootstrap) | WorldState / Simulation | active (SeamRegistry seed) |
| Weather / NPC agendas / FactionGraph **flavors** | Simulation (tick slots) | active conceptual |
| Ruleset plugins / conflict policies / quest-pressure plugins | Simulation | active conceptual |
| `input.intent.*` parsers | InputIntent | active (SeamRegistry seed) |
| Camera interpolator **easing** (not camera authority) | Presentation | active conceptual |
| Tone / visual / chrome / content packs | Pack matrix | active (Exemplar charter) |

## Pack slots (data, not behavior ports)

See [[REFERENCE-EXEMPLAR-CHARTER]] swap matrix. Packs attach through the API / bind path; they do not replace protected core.

## Provisional slots

Named only until promotion rule fires. Must not be implemented as direct core reaches.

| Slot | Layer / surface | Promotion trigger |
|------|-----------------|-------------------|
| Physics | Simulation (provisional) | Exemplar first-party flavor **or** pack swap need |
| Economics | Simulation (provisional) | Same |
| LOD | **Presentation** API surface | Same — display/perf; never owns sim or re-gen |
| Lighting | **Presentation** API surface | Same |
| GraphicsSettings | **Presentation** API surface | Same |

## First-party deeper access

Allowed early for factory / horizon demo only under the sunset rule above. Track open deeper bindings in Half B / execution receipts; clear by 6.4.
