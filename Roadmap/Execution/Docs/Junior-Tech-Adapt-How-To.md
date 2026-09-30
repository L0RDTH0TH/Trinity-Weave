---
title: Junior Tech-Adapt How-To (Execution) — genesis-mythos-master
created: 2026-09-29
updated: 2026-09-30
tags: [execution, tech-adapt, junior-mandatory, genesis-mythos-master, terrain3d, gaea, diceroller, pf1, godot-stock]
para-type: Project
project-id: genesis-mythos-master
roadmap_track: execution
status: active
paint_ux_catalog: false
sources:
  - Factory-DRB/Tech-Stack-Manifest-v1.yaml
  - Ingest/Agent-Research/Stack-Gaps/gap-stack-procedural-terrain.md
  - Ingest/Agent-Research/Stack-Gaps/gap-stack-procedural-maps.md
  - Ingest/Agent-Research/Stack-Gaps/gap-stack-rules-engine.md
  - Roadmap/Conceptual-Decision-Records/rules-base-pathfinder-pf1-2026-09-29.md
  - Roadmap/Execution/Docs/PF1-Ruleset-Content-Scaffold.md
---
# Junior Tech-Adapt How-To (Execution)

**Junior-mandatory.** Leaves that name Terrain3D / Gaea / DiceRoller / PF1 / C# host **must** point here (or paste a recipe section). “Spike required” alone is **not** an adapt recipe.

Game repo: `5-Attachments/Code-Repos/genesis-mythos-alpha/` · Engine: **Godot 4.6.3 .NET / .NET 8**.

Authority sources: [[../../Factory-DRB/Tech-Stack-Manifest-v1|Tech-Stack-Manifest-v1]] · Stack-Gaps under `Ingest/Agent-Research/Stack-Gaps/` · CDR [[../../Conceptual-Decision-Records/rules-base-pathfinder-pf1-2026-09-29|PF1]] · Content scaffold [[PF1-Ruleset-Content-Scaffold]].

---

## 0. C# / .NET host conventions (all recipes)

**Player FP / cameras (mandatory before Code-Exhibit player/camera write):** Open [[Godot-Implementation-Decision-Matrix]] + [[Godot-Stock-Patterns]] (pin [[PIN-stock_godot_fps]]). Quote the matrix principle line and the Player move/look row in the agent report. Stock `CharacterBody3D` FPS only — Host Index binds; PerspectiveEnvelope / “FP rail” must not own locomotion. Missing quote ⇒ invalid pass (Half-B PRECONDITIONS).

| Rule | Junior action |
|------|----------------|
| Language | Prefer **C#** for authority hosts (`ITerrainAuthority`, `IRulesPluginHost`, `ISimTickHost`, …). GDScript OK for UI glue only. |
| Namespaces | `Genesis.<Domain>` (e.g. `Genesis.WorldGen`, `Genesis.Rules`, `Genesis.Demo`, `Genesis.Exemplar`) |
| Errors | Return `Godot.Error` / typed result — **never** silent `Error.Ok` on wrong seat, missing seam, or refuse path |
| Seats | Take `SeatContext`; refuse with `Error.Unauthorized` (or project enum) when seat ≠ contract |
| Binding | Concrete ports bind **only** via SessionComposer / `PortBinder` (Phase 1.3) — no Autoload authority tables |
| Packages | NuGet packages declared in game `.csproj`; no AGPL dice/rules libs in core |
| Tests | gdUnit4Net (`stack-ci-gdunit4net`): ≥1 happy + ≥1 refuse path per host |
| Half B | This note is **roadmap/pseudo**. Do not implement Half B unless operator asks |

```csharp
// Shared refuse pattern (every host)
public Error GuardSeat(SeatContext seat, SeatId required) {
    if (seat.Id != required) return Error.Unauthorized;
    return Error.Ok;
}
```

---

## 1. Terrain3D — install / wrap / ImportHeightmap → splat

**Manifest:** `stack-procedural-terrain` · **Wrap:** `ITerrainAuthority` · **Addon path:** `res://addons/terrain_3d/` (vendor lock; gap also names `addons/vendor_terrain_3d/`)

**Gap synth:** [[Ingest/Agent-Research/Stack-Gaps/gap-stack-procedural-terrain]]

### Recipe A — Install + wrap

1. Vendor **Terrain3D ≥1.0.2** (MIT, GDExtension) into game `addons/terrain_3d/` (or `vendor_terrain_3d/` → enable in `project.godot`).
2. Create C# wrapper `Genesis.WorldGen.Terrain3DAuthority : ITerrainAuthority` that **only** talks to Terrain3D through Godot interop — no other scene node owns heightfield.
3. Register seam `gen.stage.terrain` → StageExecutorPort that resolves `ITerrainAuthority` (Phase 1.3 CompletenessGate required).
4. **Reject:** Gaea GridMap/TileMap as 3D terrain authority; TerraBrush as second runtime layer; Autoload `Terrain3D` without wrapper.

### Recipe B — ImportHeightmap → control/splat maps

Contract (spine from Stack-Gaps; Execution leaves must implement, not stub-`Ok`):

```csharp
namespace Genesis.WorldGen;

public interface ITerrainAuthority {
    /// Admit RF/R16 heightmap from WorldMapData into Terrain3D regions.
    Error ImportHeightmap(Image heightmap, float minH, float maxH, Vector3 worldOrigin);
    /// Apply biome/control splat weights (control maps) after height admit.
    Error ApplySplatFromBiomeGrid(Image biomeGridOrControl, SeedSnapshot seed);
    Aabb GetTerrainBounds();
    Image? GetControlMapLayer(StringName biomeId);
}

public sealed class Terrain3DAuthority : ITerrainAuthority {
    // NodePath → Terrain3D instance under WorldHost (not Autoload)
    private Terrain3D _terrain = null!;

    public Error ImportHeightmap(Image heightmap, float minH, float maxH, Vector3 worldOrigin) {
        if (heightmap == null || heightmap.GetWidth() < 2)
            return Error.InvalidParameter;
        // 1) Convert to Terrain3D-accepted format (RF/R16 per Terrain3D docs).
        // 2) Call Terrain3D import / set region height data at worldOrigin.
        // 3) Update streaming bounds; do NOT mutate WorldMapData (maps stay authority for 2D).
        // VERIFY: dry-run leaves no durable WorldHost child; regen swaps container children.
        return Error.Ok; // only after import succeeded
    }

    public Error ApplySplatFromBiomeGrid(Image biomeGridOrControl, SeedSnapshot seed) {
        if (biomeGridOrControl == null) return Error.InvalidParameter;
        // Map biome cells → Terrain3D control maps / material weights (IBiomeStage output).
        // Refuse if CompletenessGate missing gen.stage.biomes PUBLISHED.
        return Error.Ok;
    }

    public Aabb GetTerrainBounds() => _terrain.GetAabb(); // or wrapper bounds
    public Image? GetControlMapLayer(StringName biomeId) => null; // implement per control layer id
}
```

**Admit stage order:** `IMapGenAuthority` / Gaea parallel → `WorldMapData` → **`ITerrainAuthority.ImportHeightmap`** → `ApplySplatFromBiomeGrid` → foliage/nav later waves.

**Structural DM reshape:** height edit = regional/full re-gen (PMG) — not live in-session sculpt as default product behavior.

---

## 2. Gaea → WorldMapData → terrain admit (Gaea ≠ terrain authority)

**Manifest:** `stack-procedural-maps-gaea-parallel` (+ first-party `stack-procedural-maps` / `IMapGenAuthority`)

**Gap synth:** [[Ingest/Agent-Research/Stack-Gaps/gap-stack-procedural-maps]]

### Hard authority split

| Concern | Owner | Not |
|---------|-------|-----|
| 2D overland / heightfield export | `IMapGenAuthority` → `WorldMapData` (first-party **or** Gaea adapter) | Terrain3D |
| 3D mesh/streaming admit | `ITerrainAuthority` (Terrain3D) | Gaea GridMap renderer |
| Pipeline orchestration | `IWorldGenStage` DAG | Gaea monolith skipping seams |

### Recipe C — Gaea parallel path

1. Prefer **first-party** `MapGenAuthority.Generate(WorldSeedState) → WorldMapData` as primary lock.
2. Optional **Gaea 2.0** adapter: run graph → custom export node → RF `Image` + metadata into **`WorldMapData` only** (no vendor types leak past adapter).
3. Handoff: `WorldMapData.HeightmapImage` → `ITerrainAuthority.ImportHeightmap(...)`.
4. Replay gate: same seed → same `WorldMapData` heightmap hash before Terrain3D admit.
5. **Reject:** Gaea as `ITerrainAuthority`; SimpleXTerrain bundle collapsing map+terrain without operator choice; Azgaar/FMG as default runtime.

```csharp
public interface IMapGenAuthority {
    WorldMapData Generate(WorldSeedState seed);
}

public sealed class GaeaMapGenAdapter : IMapGenAuthority {
    public WorldMapData Generate(WorldSeedState seed) {
        // Run Gaea graph offline/editor or runtime glue → fill WorldMapData:
        // HeightmapImage, BiomeGridRef, Bounds, Metadata — no Gaea node refs stored.
        return new WorldMapData(/* ... */);
    }
}

public sealed class TerrainAdmitStage : IWorldGenStage {
    public StringName StageId => "terrain";
    private readonly ITerrainAuthority _terrain;
    public StageResult Run(GenContext ctx) {
        var map = ctx.RequireWorldMapData();
        var err = _terrain.ImportHeightmap(map.HeightmapImage, map.MinH, map.MaxH, map.Origin);
        if (err != Error.Ok) return StageResult.Fail(err);
        err = _terrain.ApplySplatFromBiomeGrid(map.BiomeGridOrControl, ctx.Seed);
        return err == Error.Ok ? StageResult.Ok() : StageResult.Fail(err);
    }
}
```

---

## 3. DiceRoller NuGet behind `IDiceRoller`

**Manifest:** `stack-rules-engine` · **Wrap:** `IRulesPluginHost` · NuGet: **DiceRoller** (skizzerz, **MIT**)

**Gap synth:** [[Ingest/Agent-Research/Stack-Gaps/gap-stack-rules-engine]] (architecture still valid; content base superseded by PF1 CDR)

### Recipe D — Wire dice

1. Add NuGet `DiceRoller` to game `.csproj`.
2. Implement `IDiceRoller` wrapping DiceRoller API; pin PRNG from `ISeedAuthority` sub-seed channel `rules` (see Host Index §B4).
3. `IRulesPluginHost.Roll(DiceExpression, RuleContextFrame)` **must** delegate to `IDiceRoller.Roll` — UI must not roll directly. String probes use `IDiceRoller.RollExpression`.
4. Emit audit row (expression, seed channel, result) for contested checks. Empty expression → `InvalidParameter` (never silent Ok).
5. **Exclude from core:** kupka/libsrd5 (**AGPL**), vokimon/godot-dice-roller (**AGPL**).
6. **Signature source of truth:** [[SeamRegistry-CSharp-Host-Index]] §B4 — do not invent a second `Roll(string, ulong)` on `IDiceRoller` alone.

```csharp
namespace Genesis.Rules;

// Normative signatures — [[SeamRegistry-CSharp-Host-Index]] §B4 wins on conflict.
public readonly record struct DiceExpression(string Text) {
    public static DiceExpression Parse(string text) =>
        string.IsNullOrWhiteSpace(text)
            ? throw new ArgumentException("empty")
            : new(text.Trim());
}

public interface IDiceRoller {
    /// Contested check: typed expression + RuleContextFrame (seed channel from frame).
    DiceAudit Roll(DiceExpression expression, RuleContextFrame frame);
    /// Convenience for plugin probe / audit; empty expr → InvalidParameter (not silent Ok).
    DiceAudit RollExpression(string expression, ulong rulesSubSeed);
}

public interface IRulesPluginHost {
    Error BindPlugin(IRulesetPlugin plugin);     // requires seam rules.plugin.core PUBLISHED
    CheckResult Evaluate(CheckRequest req);
    DiceAudit Roll(DiceExpression expression, RuleContextFrame frame); // → IDiceRoller.Roll
    StringName ActiveRuleset { get; }            // default pathfinder_pf1
}

public sealed class SkizzerzDiceRoller : IDiceRoller {
    public DiceAudit Roll(DiceExpression expression, RuleContextFrame frame) {
        // Pin PRNG from frame.RulesSubSeed (ISeedAuthority channel "rules"); return audit.
        throw new NotImplementedException("Half B — recipe contract only");
    }
    public DiceAudit RollExpression(string expression, ulong rulesSubSeed) {
        if (string.IsNullOrWhiteSpace(expression))
            throw new ArgumentException("empty expression"); // callers map → InvalidParameter
        return Roll(DiceExpression.Parse(expression), RuleContextFrame.FromRulesSeed(rulesSubSeed));
    }
}
```

---

## 4. PF1 plugin + content remint path

**CDR:** [[../../Conceptual-Decision-Records/rules-base-pathfinder-pf1-2026-09-29|rules-base-pathfinder-pf1-2026-09-29]]  
**Lock id:** `pathfinder_pf1` · **Host:** ruleset-agnostic · **First plugin content:** PF1 (not SRD 5.1 / 5e-bits; not PF2e/ORC)  
**Vault F2 scaffold (tables/slots/check schema):** [[PF1-Ruleset-Content-Scaffold]] · **Host bind:** [[SeamRegistry-CSharp-Host-Index]] §B4

### Recipe E — Plugin posture (architecture — already woven on Phase-5 / 6.2.5)

1. `RulesetPluginId = "pathfinder_pf1"`.
2. `PluginLoader.load_from_path` gated by SeamRegistry seam `rules.plugin.core`.
3. Mid-session swap only via ReGenerationIntentQueue (Phase 3.3) + seam assert — never Autoload table swap.
4. `IRulesPluginHost.Roll` **must** delegate to `IDiceRoller` (Recipe D) — DiceRoller stays behind the interface.

### Recipe F — Content remint path (prefer deepen existing; invent 5.2.2+ only if required)

| Step | Action | Owner note |
|------|--------|------------|
| F1 | Inventory Phase-5 Resources/JSON still naming SRD/5e/D&D **or PF2e** checks, skills, conditions | Phase-5 primary + 5.1.x |
| F2 | Remint tables to **PF1** vocabulary (d20 checks, BAB/saves L1–20, skills, conditions, spell slots L1–5+, spell-list scaffold) under `res://rules/pathfinder_pf1/` — **shapes + junior tables live in** [[PF1-Ruleset-Content-Scaffold]] | Content pack; host unchanged |
| F3 | Character creation spine (`ICharacterCreationHost`) consumes reminted pack — not 5e-bits | Phase-5 / later; deepen existing |
| F4 | 6.2.5 `RuleCheckProbe` binder uses `pathfinder_pf1` / `demo_ruleset_pf1` + `pf1_check_v0` | Demo beat |
| F5 | Exemplar 6.4 pack_defaults.ruleset_id → same plugin id; receipt `R.rules.pf1_bind` | Reference Exemplar |
| Halt | Do **not** invent 5.2.2+ tertiaries for remint — deepen 5.1 / 5.2 / 5.2.1 + this recipe + scaffold | Operator order |

**Not legal advice.** Operator owns license review before shipping branded packs.

---

## 5. Leaf pointer checklist

Execution leaves that mention these nouns should link this note and/or include a `# see Junior-Tech-Adapt-How-To` comment in ```pseudo / C# weave:

- Phase-2 primary + 2.1 terrain/pipeline → Recipes A–C  
- Phase-3 primary + 3.1.x sim → Host Index §B2 (tick ≠ weather ≠ npc ≠ faction)  
- Phase-5 primary + 5.1.x + 6.2.5 → Recipes D–F  
- Phase-6.4 Exemplar → Recipes A–C + F (pack defaults) + **§6 paper design assembly**  
- Phase-1.3 SeamRegistry host index → §0 conventions + seam ids used above  
- Phase-4 / Phase-6 player FP / cameras / seats → [[Godot-Implementation-Decision-Matrix]] + [[Godot-Stock-Patterns]] (not envelope-as-mover)

---

## 6. Design-gate paper assembly (Exemplar without inventing seams)

**Goal (design gate only):** A junior can walk API + PF1 tables + fill matrix + DoDGate receipts + this How-To **on paper** and produce a complete receipt ledger / module_bind plan — **without inventing seams, pack keys, or host types**. Half B game-repo Boot is **out of scope** (`half_b_deferred`).

### Paper walk (ordered)

| Step | Open | Prove on paper |
|------|------|----------------|
| 0 | [[SeamRegistry-CSharp-Host-Index]] §A–B5 + this note §0–4 | Nine required seam ids; every fill-matrix `host_type` resolves in Index |
| 1 | [[PF1-Ruleset-Content-Scaffold]] §4.4–4.6 | BAB L1–20; spell slots L1–20; ≥12 `spell_id`s; plugin id `pathfinder_pf1` |
| 2 | Execution 6.4 **Pack-slot fill matrix** rows 1–19 | No invent: only listed pack keys / slots / receipt ids |
| 3 | 6.4 **CampaignCapableDoDGate** verify templates | Each required receipt has non-empty `verify` matching template shape |
| 4 | 6.4 **Paper ledger (design)** block | Copy filled JSON; mentally run `Validate` → Ok; omit one id → Unconfigured |
| 5 | Phase-3 stack-weave | Weather→`IWeatherModule`, NPC→`INPCScheduleModule`, faction→`IFactionGraph`, tick→`ISimTickHost` (no collapse) |

**Pass criterion (design_gate):** Steps 0–5 checkable without opening the game repo. **Fail closed** if junior would need a new seam id, pack key, or host interface not in Index/fill matrix.

**Explicitly deferred:** `res://rules/pathfinder_pf1/` mint; runnable `ReferenceExemplarGate.Boot` in game repo; Half B code.

---

## Status

Minted **2026-09-29** for operator Gap 1 (tech-adapt how-to). Design-gate **2026-09-30**: §6 paper assembly walk. Depth > stamp: recipes are implementable without inventing alternate stacks.
