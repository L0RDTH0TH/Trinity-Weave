# Pin excerpt — Phase 4.1 Player FP / Perspective Envelope

_Cite-only mirror for Grok mint dialogue. Full note lives in vault Roadmap._

## Actors

| Actor | Role |
|-------|------|
| **PerspectiveEnvelope** | Declares legal perspective modes (`player_fp`, `dm_world`, `dm_map`, `dm_sensorium_attach`) and which modes may emit **InputIntent** vs read-only observe; dominated-victim **passenger_fp** / spell-bound presentation is **not** an envelope mode — overlay deferred Phase 5 (PMG [[genesis-mythos-master-goal]]) |
| **UnifiedSceneGraph** | Single scene composition root; all rigs attach as **PerspectiveAnchor** nodes; no duplicate world mutation paths |
| **CameraInterpolatorRegistry** | Named interpolators (`ease_default`, `snap_cut`, `dm_orbit`) swappable per transition edge without rewiring graph |
| **PlayerFPRig** | Default FP anchor; binds local player avatar presentation; routes self-agency intents upward |
| **WorldCam** | DM tactical overview rig; read-only WorldState projection; no **InputIntent** except mode-switch envelopes |
| **MapCam** | Strategic map rig; read-only faction/terrain overlays from projected state |
| **SensoriumAttach** | Read-only bind to NPC/entity sensorium — **not** agency delegation (distinct from **PilotGraph** dominate) |
| **PilotGraph** | Agency delegation state machine: **self** → **dominate** (possess target envelope) → **absent-proxy** (NPC acts per policy while player away) |
| **ModeTransitionGraph** | Directed edges among rigs with guard predicates (DM session authority, **DMPauseGate** from 3.1, narrative veto from 3.3) |
| **PresentationShell** | Session-scoped composer child (1.1); owns rig activation and interpolator selection |

## Ordering (mode transition)

1. **ModeTransitionGraph** evaluates guard (DM authority, pause state, overwrite class from 3.3 if live patch active)
2. Source rig **deactivate** (flush pending interpolator)
3. **CameraInterpolatorRegistry** blend from source **PerspectiveAnchor** to target over `transition_ms` or snap
4. Target rig **activate**; **PerspectiveEnvelope** updates legal intent routes
5. **PilotGraph** reconciles agency: dominate transfers **InputIntent** router target; absent-proxy installs proxy policy without sim write from Presentation
6. Emit `presentation.mode_changed` on `presentation.*` bus (Phase 1.1)

## Inputs / outputs

- *Into 4.1:* **WorldState** projections (1.1); `sim.tick_committed` read-only (3.1); **DMPauseGate** + speculative queue awareness (3.1/3.3); **NarrativeDeltaVetoPolicy** may block transitions that contradict live narrative (3.3)
- *Out of 4.1:* **PerspectiveEnvelope** contract for 4.2 DM rigs deep-dive; **PilotGraph** export for 4.3 agency glue; stable rig IDs for factory catalog mint

## Interfaces

**Imports from Phase 1:**

| Phase 1 export | How 4.1 consumes it |
|----------------|----------------------|
| Presentation / InputIntent layers (1.1) | PresentationShell owns rigs; InputIntent router respects **PerspectiveEnvelope** |
| `presentation.*` bus category (1.1) | `presentation.mode_changed`, `presentation.rig_active` |
| Agency delegation envelopes (1.1) | **PilotGraph** specializes dominate + absent-proxy |

**Imports from Phase 3:**

| Phase 3 export | How 4.1 consumes it |
|----------------|----------------------|
| **DMPauseGate** (3.1) | Mode transitions may be frozen while DM holds narrative authority |
| **WorldEventLog** subscribe (3.1) | Presentation refreshes projections on `sim.tick_committed` — never blocks sim |
| **NarrativeDeltaVetoPolicy** (3.3) | Blocks mode edges that would surface contradictory live patches |

**Exports to Phase 

…
