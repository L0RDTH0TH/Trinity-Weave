---
title: Phase 3.1.2 — Roll-up & Region Weather Tables
roadmap-level: rollup
phase-number: 3
subphase-index: 3.1.2
project-id: genesis-mythos-master
status: complete
roadmap_track: conceptual
parent-tertiary: '[[Phase-3-1-2-Weather-Environmental-State-Subsystem-Roadmap-2026-06-29-2230]]'
created: 2026-06-29
tags:
- roadmap
- genesis-mythos-master
- phase-3
- rollup
- weather
- environmental-state
para-type: Project
frozen: true
conceptual_frozen_at: '2026-07-17T05:59:24Z'
---

## Actors

| Actor | Role |
|-------|------|
| **WeatherSubsystem** | First **SimTickPipeline** slot after clock increment |
| **RegionWeatherRegistry** | region_id → { phase, mood_scalar, humidity_band, temperature_band, wind_band } |
| **EnvironmentalCycleProfile** | Seed-derived tables mapping sim time → cycle phase |
| **MoodModifierBinding** | Scales drift from **ToneProfileConsequenceWeights** mood channel |
| **WeatherTickDelta** | Proposed environmental patches only — never NPC/faction keys |
| **RegionScopeResolver** | play_region vs background_region fidelity split |
| **WeatherNoisePolicy** | Per-tick max delta caps per environmental key |

## Environmental keys (conceptual v1)

| key | Description | Drift source |
|-----|-------------|--------------|
| `phase` | season / day-night enum | **EnvironmentalCycleProfile** deterministic |
| `mood_scalar` | narrative mood 0..1 | cycle + **MoodModifierBinding** + bounded noise |
| `humidity_band` | discrete band index | cycle table + noise |
| `temperature_band` | discrete band index | cycle table + noise |
| `wind_band` | discrete band index | noise only (no canon hooks) |

## Per-tick pass (algorithm sketch)

```
for region in RegionScopeResolver.active_regions(snapshot):
  phase = EnvironmentalCycleProfile.lookup(sim_time t, region.seed_offset)
  mood_scale = MoodModifierBinding.from_tone_profile(active_tone_profile)
  delta = WeatherNoisePolicy.propose(region.state, phase, mood_scale)
  emit WeatherTickDelta(region_id, delta)
// background regions: same loop, lower tick fidelity (every N ticks) — 3.2 may summarize
```

## Interface tables

### Imports

| Source | Consumption |
|--------|-------------|
| **3.1.1** **SimClock** | `t`, `n` for cycle lookup |
| **2.1** **SimGraphSeed** | Initial registry from worldgen climate bands |
| **2.3** **ToneProfileBundle** | Mood weight namespace |
| Parent 3.1 **ConsequenceResolver** | Merge precedence: weather lowest among subsystem deltas |

### Exports

| Export | Consumer |
|--------|----------|
| **RegionWeatherRegistry** | **3.2** **SinceYouLeftCompiler** mood context |
| **WeatherTickDelta** schema | **ConsequenceResolver** |
| `environmental_mood_context` read-only view | Phase 4 presentation |

## Edge cases

- **Empty region set:** Valid degenerate — no **WeatherTickDelta** emitted; tick still commits if clock advanced (parent 3.1 zero-NPC case).
- **Conflicting weather + canon hook:** **ConsequenceResolver** drops weather delta; emit `sim.tick_blocked` only if no merge possible (parent 3.1 precedence).
- **ToneProfile fallback at runtime:** Use **2.3** **ToneFallbackResolver** + `sim.tone_fallback_applied`; weather drift uses Medium Fantasy mood scale — not silent zero.
- **Long absence catch-up:** **3.1.1** variable step may advance multiple cycle phases in one tick — **EnvironmentalCycleProfile** must support multi-phase jump without skipping veto checks.
- **DM pause mid-weather pass:** Weather proposals stay speculative until **WorldStateCommitter** — same atomicity as parent 3.1 pause-during-commit.

## Open questions

- **Background region fidelity N:** Every N ticks vs every tick — operator attestation via factory catalog; default N=4 conceptual placeholder.
- **Cross-region weather sync:** Shared macro-climate vs independent micro-climates — lean independent per **SimGraphSeed** region graph; tertiary refine if PMG demands sync.
- **Presentation coupling:** Skybox state is read-only subscribe — no sim block on render; execution mirror defines subscribe contract.

## Handoff readiness

| Criterion | Status | Evidence |
|---|---|---|
| Scope (in/out) | pass | § Scope on parent tertiary |
| Behavior (actors, ordering) | pass | § Actors + per-tick sketch |
| Interfaces (adjacent contracts) | pass | § Interface tables |
| Edge cases | pass | § Edge cases |
| Open questions | pass | § Open questions |
| Pseudo-code readiness | pass | Per-tick pass traceable |
| **`handoff_readiness` aggregate** | **80%** | second Phase 3 tertiary under factory feed gate |

> Execution-deferred / advisory on conceptual track: Godot weather scene graph, typed band enums, REGISTRY-CI — execution track or factory harness (`1373c0c3408d`).

## Responsibilities (rollup authority)

- [x] Document environmental key catalog and drift sources
- [x] Document **SimTickPipeline** first-slot ordering
- [x] Bind mood drift to **ToneProfile** from **2.3**

## Tasks (rollup authority)

- [x] Mint 3.1.2 rollup with region weather tables and per-tick sketch
- [ ] Refine background region fidelity N when execution mirror mints typed **RegionScopeResolver**
