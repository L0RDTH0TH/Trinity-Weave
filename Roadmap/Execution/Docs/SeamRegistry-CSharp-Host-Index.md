---
title: SeamRegistry + C# Host Port Index (Execution) — genesis-mythos-master
created: 2026-09-29
updated: 2026-09-29
tags: [execution, seam-registry, csharp, host-index, junior-mandatory, genesis-mythos-master]
para-type: Project
project-id: genesis-mythos-master
roadmap_track: execution
status: active
canonical_for: [Phase-1.3.1, Phase-6.4, Phase-6.2]
---
# SeamRegistry + C# Host Port Index (junior-complete)

**Single index** for critical C# / seam hosts used by Phases 1–6. Leaves may excerpt; this note wins on conflict for method names, errors, and seat/authority.

Related: [[Junior-Tech-Adapt-How-To]] · [[../Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-3-Modularity-Seams-and-Safety-Invariants/Phase-1-3-1-SeamRegistry-Canonical-Index-Roadmap-2026-06-29-1037|1.3.1 SeamRegistry]] · [[../Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-4-Reference-Exemplar/Phase-6-4-Reference-Exemplar-Roadmap-2026-08-01|6.4 Exemplar]]

**Anti-pattern:** `return Error.Ok;` / `return new T();` with no refuse path on critical hosts. Every host below **must** document at least one Unauthorized / InvalidParameter / Unconfigured fail.

---

## A. SeamRegistry (canonical)

**Namespace:** `Genesis.Seams` · **Bind time:** SessionComposer / PortBinder only · **Not** Autoload

| Method | Seat / authority | Success | Failures |
|--------|------------------|---------|----------|
| `Error Publish(SeamEntry entry)` | `privileged_access` / SessionComposer | OK; entry DRAFT or PUBLISHED | `InvalidParameter` null id; `AlreadyExists` conflicting contract |
| `Error AssertPublished(StringName seamId)` | any reader | OK if lifecycle=PUBLISHED | `Unavailable` unpublished; `DoesNotExist` |
| `SeamEntry? Get(StringName seamId)` | any | entry or null | — |
| `Error Deprecate(StringName seamId)` | SessionComposer | OK; resolvable until session end | `DoesNotExist` |
| `Error SwapPort(StringName seamId, RefCounted port)` | PortBinder only | OK | `Unauthorized` late player bind; `Unavailable` not PUBLISHED |

**Required seam ids (CompletenessGate):**  
`gen.stage.terrain` · `gen.stage.biomes` · `gen.stage.pois` · `gen.stage.entities` · `gen.stage.sim_bootstrap` · `rules.plugin.core` · `bus.sub.sim_default` · `bus.sub.canon_default` · `input.parser.player_lite`

```csharp
namespace Genesis.Seams;

public enum SeamLifecycle { Draft, Published, Deprecated }
public enum SeamFamily { Generation, Rules, Bus, Input }

public sealed class SeamEntry {
    public required StringName SeamId { get; init; }
    public required SeamFamily Family { get; init; }
    public required StringName PortOwner { get; init; }
    public required SeamLifecycle Lifecycle { get; set; }
    public StringName LayerOwner { get; init; } = new("WorldState");
    public Dictionary SwapContract { get; init; } = new();
}

public interface ISeamRegistry {
    Error Publish(SeamEntry entry);
    Error AssertPublished(StringName seamId);
    SeamEntry? Get(StringName seamId);
    Error Deprecate(StringName seamId);
}

public interface IPortBinder {
    Error Bind(StringName seamId, GodotObject port, SeatContext seat);
    GodotObject? Resolve(StringName seamId);
}

public sealed class PortBinder : IPortBinder {
    private readonly Dictionary<StringName, GodotObject> _ports = new();
    public Error Bind(StringName seamId, GodotObject port, SeatContext seat) {
        if (port == null) return Error.InvalidParameter;
        if (!seat.AllowsSessionCompose()) return Error.Unauthorized; // never mid-session player
        _ports[seamId] = port;
        return Error.Ok;
    }
    public GodotObject? Resolve(StringName seamId) =>
        _ports.TryGetValue(seamId, out var p) ? p : null;
}

public sealed class CompletenessGate {
    public static readonly StringName[] Required = {
        "gen.stage.terrain","gen.stage.biomes","gen.stage.pois","gen.stage.entities",
        "gen.stage.sim_bootstrap","rules.plugin.core","bus.sub.sim_default",
        "bus.sub.canon_default","input.parser.player_lite"
    };
    public Error Check(ISeamRegistry registry) {
        foreach (var id in Required) {
            var err = registry.AssertPublished(id);
            if (err != Error.Ok) return err;
        }
        return Error.Ok;
    }
}
```

---

## B. Critical C# host index (Phases 1–5 → 6)

### B1. World gen / terrain / maps

| Host | Phase | Methods (normative) | Seat / authority | Must-fail cases |
|------|-------|---------------------|------------------|-----------------|
| `ISeedAuthority` | 1.3.2 | `ulong Channel(StringName name)`; `SeedSnapshot Capture()` | Session / WorldState | missing channel → Unconfigured |
| `IMapGenAuthority` | 2 | `WorldMapData Generate(WorldSeedState seed)` | DM world / gen | empty seed → InvalidParameter; Gaea types must not leak |
| `ITerrainAuthority` | 2 | `ImportHeightmap`; `ApplySplatFromBiomeGrid`; `ApplyHeightAndSplat` | DM world / Terrain3D | null image → InvalidParameter; **never** silent Ok without admit |
| `IWorldGenStage` | 2.1 | `StringName StageId`; `StageResult Run(GenContext)` | StageExecutorPort | CompletenessGate fail → Unavailable |

See [[Junior-Tech-Adapt-How-To]] §1–2 for Terrain3D / Gaea recipes.

### B2. Simulation

| Host | Phase | Methods | Seat / authority | Must-fail cases |
|------|-------|---------|------------------|-----------------|
| `ISimTickHost` | 3.1 | `Error Tick(double simTime, SimSnapshot snapshot)` | Simulation | second demo tick / pause → Bug or Busy; overflow → deferred signal **not** truncate |
| `IWeatherModule` | 3.1.2 | `StringName SlotId`; `WeatherTickDelta Tick(double, Dictionary)` | Simulation | budget overflow → `overflow:true` + deferred_regions (**non-empty delta or explicit overflow**) |
| `INPCScheduleModule` | 3.1.3 | `Error AdvanceAgenda(StringName npcId, SeatContext)`; `AgendaDelta Peek(...)` | Simulation | player write → **Unauthorized**; missing npc → DoesNotExist |
| `IFactionGraph` | 3.1.4 | `Error ApplyEdgePatch(FactionEdgePatch)`; `IReadOnlyList<FactionEdge> Snapshot()` | Simulation | player/canon invent → **Unauthorized**; silent truncate → Bug |

**Anti-collapse:** Phase-3 stack-weave must map weather→`IWeatherModule`, npc→`INPCScheduleModule`, faction→`IFactionGraph`, tick→`ISimTickHost` — never funnel all four to tick host.

```csharp
// Weather — refuse empty theater when snapshot requires work
public WeatherTickDelta Tick(double simTime, Dictionary snapshot) {
    if (snapshot == null) throw new ArgumentNullException(nameof(snapshot));
    var delta = ComputeDelta(simTime, snapshot); // may be graybox single-region
    if (OverBudget(delta)) delta.Overflow = true; // never silent drop
    Registry.Upsert(delta);
    return delta;
}

public interface INPCScheduleModule {
    Error AdvanceAgenda(StringName npcId, SeatContext seat); // Unauthorized if player authors
    AgendaDelta? Peek(StringName npcId);
}

public interface IFactionGraph {
    Error ApplyEdgePatch(FactionEdgePatch patch, SeatContext seat);
    IReadOnlyList<FactionEdge> Snapshot();
}
```

### B3. Perspective / agency

| Host | Phase | Methods | Seat / authority | Must-fail cases |
|------|-------|---------|------------------|-----------------|
| `ICameraRig` | 4.1.3 | `Activate(PerspectiveMode, SeatContext)`; `ApplyFov` — **selector only** (swap `Camera3D.Current`, enable/disable stock FPS). Must **not** implement player Move/Look/HandleInput (see [[Godot-Implementation-Decision-Matrix]] Seats row) | player vs dm_as_player | player on DM rail → **Unauthorized**; Move/Look on body via this host → **defect** |
| `IAgencyEnvelope` / PilotHandoff | 4.3 | `Error Assert(SeatContext)`; `Error Release(StringName pilotId)` | FP≠DM | wrong seat → Unauthorized; dominate without release path → reject |

```csharp
public interface IAgencyEnvelope {
    Error Assert(SeatContext seat);   // Unauthorized when seat conflates FP with DM rail
    Error Release(StringName pilotId); // DoesNotExist if no active pilot
}
```

### B4. Rules

| Host | Phase | Methods | Seat / authority | Must-fail cases |
|------|-------|---------|------------------|-----------------|
| `IDiceRoller` | 5 | `Roll(DiceExpression, RuleContextFrame)`; `RollExpression(string, ulong)` | rules channel seed | AGPL libs forbidden; empty expr → InvalidParameter |
| `IRulesPluginHost` | 5.1 | `BindPlugin(IRulesetPlugin)`; `Evaluate(CheckRequest)`; `Roll(DiceExpression, RuleContextFrame)`→`IDiceRoller.Roll`; `ActiveRuleset` | `rules.plugin.core` | Bind without seam → Unavailable; observe-only world write → empty/reject; UI must not call `IDiceRoller` directly |
| `ISpellMetadataRegistry` | 5.2.1 | `SpellMeta? Get(StringName spellId)`; `IReadOnlyList<StringName> ListIds()` | agency overlays only | CanonRegistry write → reject; unknown id → DoesNotExist |
| `IQuestPressureHint` | 5.3 | `Error EmitHint(IntentHint)` | IntentResolver only | direct WorldState mutate → reject |

Default plugin id: **`pathfinder_pf1`**. Remint recipes: [[Junior-Tech-Adapt-How-To]] §3–4. **Vault F2 tables:** [[PF1-Ruleset-Content-Scaffold]] (abilities, skills, conditions, **BAB/saves L1–20**, **spell slots L1–20**, spell-list ≥12 ids, check_schema, plugin_manifest, demo binder). DiceRoller remains behind `IDiceRoller` only.
### B5. Presentation / demo / exemplar

| Host | Phase | Methods | Seat / authority | Must-fail cases |
|------|-------|---------|------------------|-----------------|
| `IUiHost` / HUDLayerStack | 6.1 | mount layers | Presentation | DevLeakageGuard fail → Unavailable |
| `IPlayRegionHost` | 6.1.2 | `Error Mount(StringName mountId)`; `Error Unmount()` | Session | double-mount → AlreadyExists; DevLeakageGuard fail → Unavailable |
| Horizon demo beats | 6.2.x | proof-loop stubs | shared_table | **may** stub behavior but **must** type against B1–B4 hosts (Gap 4) |
| `ICampaignCapableDoDGate` | 6.4 | `Validate(ReceiptLedger)` | Exemplar | missing receipt → Unconfigured; stub_only → InvalidParameter; empty `verify` → missing |

```csharp
public interface IPlayRegionHost {
    Error Mount(StringName mountId, SeatContext seat);
    Error Unmount();
}
```

---

## C. Error vocabulary (shared)

| Godot.Error / meaning | When |
|----------------------|------|
| `Ok` | Contract satisfied **and** side-effects done (or explicitly no-op with documented reason) |
| `Unauthorized` | Wrong seat / late PortBinder / player on DM rail |
| `InvalidParameter` | Null image, empty expression, stub_only ledger |
| `Unconfigured` / `Unavailable` | Missing PUBLISHED seam, missing receipt, plugin not bound |
| `Busy` | Dry-run fail / DM pause (retconnable block) |
| `DoesNotExist` | Unknown seam / slot / snapshot |
| `AlreadyExists` | Duplicate publish / double mount |
| `Bug` | Demo one-shot violated (e.g. second SimTickStub) |

---

## D. Junior verify (index)

- [ ] CompletenessGate lists all nine required seams; AssertPublished fails closed
- [ ] PortBinder.Bind refuses non-compose seat
- [ ] ITerrainAuthority.ImportHeightmap rejects null/tiny image (not bare Ok)
- [ ] ICameraRig.Activate refuses player on DM WorldCam
- [ ] IRulesPluginHost.Roll always calls IDiceRoller; ActiveRuleset defaults **pathfinder_pf1**; F2 scaffold linked from How-To §4
- [ ] IWeatherModule.Tick never returns a silent empty delta when overflow/work required without setting overflow flags
- [ ] INPCScheduleModule / IFactionGraph are distinct from ISimTickHost (Phase-3 stack-weave de-collapse)
- [ ] Fill-matrix host_types resolve in this index: IPlayRegionHost, IAgencyEnvelope, ISpellMetadataRegistry, IQuestPressureHint
- [ ] 6.4 gate uses receipt ledger from this index’s hosts — not boolean theater

## Status

Minted Gap 3 (**2026-09-29**). Design-gate thicken **2026-09-30**: sim/agency/play-region signatures + anti-collapse note. Prefer this index over per-leaf duplicate empty `ILeafContract` stubs.
