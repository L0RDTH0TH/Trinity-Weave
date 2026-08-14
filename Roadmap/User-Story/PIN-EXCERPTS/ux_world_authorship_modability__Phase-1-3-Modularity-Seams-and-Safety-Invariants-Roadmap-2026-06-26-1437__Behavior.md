# PIN-EXCERPT — `ux_world_authorship_modability` → [[Phase-1-3-Modularity-Seams-and-Safety-Invariants-Roadmap-2026-06-26-1437]]

- heading: ## Behavior
- role: primary
- excerpt_note: Modularity/safety seams for authorship contracts
- source: `1-Projects/genesis-mythos-master/Roadmap/Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-3-Modularity-Seams-and-Safety-Invariants/Phase-1-3-Modularity-Seams-and-Safety-Invariants-Roadmap-2026-06-26-1437.md`
- weld_rule: excerpt text is the weld; heading is the locator

---

**Actors:**

| Actor | Role |
|-------|------|
| **SeamRegistry** | Canonical index of replaceability seams — generation stages, rule hooks, bus subscriptions, input parsers — each with swap contract and neighbor guarantees |
| **StageExecutorPort** | Generation seam — one port per canonical stage (`terrain` … `sim_bootstrap`); inherits per-node contracts from [[Phase-1-2-1-Stage-DAG-Node-Contracts-Roadmap-2026-06-26-1105]] |
| **RulePluginPort** | Rule engine seam — core primitives only; rulesets declare hook points and conflict resolution policy |
| **BusSubscriptionPort** | Simulation event bus seam — behaviors subscribe to `sim.*` / `canon.*` categories without owning the bus implementation |
| **IntentParserPort** | Input loop seam — intent envelope parsing + population resolver; extensible for voice, forms, chat without rewriting Simulation |
| **SeedSnapshotAuthority** | Captures immutable snapshot of SeedBundle + ToneProfile + accepted CanonFacts + active ruleset IDs before destructive generation or DM overwrite |
| **DryRunValidator** | Read-only pre-flight on proposed generation compile or DM structural overwrite — estimates validity and performance envelope; **no world w

_…excerpt truncated (soft budget)…_
