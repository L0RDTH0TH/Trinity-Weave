# PIN-EXCERPT — `ux_backstory_legacy_integration` → [[Phase-2-2-Canon-Registry-and-Intent-Resolver-Roadmap-2026-06-26-1530]]

- heading: ## Behavior
- role: primary
- excerpt_note: Canon registry / intent resolver for legacy hooks
- source: `1-Projects/genesis-mythos-master/Roadmap/Phase-2-Procedural-Generation-and-World-Building/Phase-2-2-Canon-Registry-and-Intent-Resolver/Phase-2-2-Canon-Registry-and-Intent-Resolver-Roadmap-2026-06-26-1530.md`
- weld_rule: excerpt text is the weld; heading is the locator

---

**Actors:**

| Actor | Role |
|-------|------|
| **CanonRegistry** | Authoritative store for CanonFacts; indexes by era, entity, location, thread; emits `canon.fact_*` bus events |
| **IntentResolver** | Parses intent payloads (player-lite inbox, session 0 table, DM revise) → candidate CanonFacts; routes to validator |
| **CanonFactValidator** | Enforces schema, table bounds, and duplicate/conflict policy before `accepted`; delegates tone bounds to **ToneCompatibilityGate** |
| **ToneCompatibilityGate** | Validates canon facts against active **ToneProfileBundle** bounds; invoked by CanonFactValidator (**2.3** rules export) |
| **LoreHookRegistry** | Projects `hooked` facts into hook records with sim-facing tags consumed by POI/entity stages |
| **HookMaterializer** | Transforms accepted facts into hook candidates; DM/table accept gate before `hooked` promotion |
| **ProvenanceEnvelope** | Immutable audit trail: source intent id, actor, timestamp, revision chain |
| **RegistrySnapshot** | Point-in-time export for DryRunValidator replay against **2.1** pipeline inputs |
| **ConflictArbiter** | Surfaces contradictory facts to DM workbench; never silent merge on conceptual track |

**C

_…excerpt truncated (soft budget)…_
