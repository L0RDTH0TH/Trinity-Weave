---
title: Conceptual decision record — API core-protection boundary
created: 2026-09-28
tags: [conceptual-decision-record, roadmap, genesis-mythos-master, api, modularity, core-protection]
para-type: Project
project-id: genesis-mythos-master
parent_roadmap_note: "[[Phase-1-Conceptual-Foundation-and-Core-Architecture-Roadmap-2026-06-26-0914]]"
decision_kind: other
queue_entry_id: null
master_goal: "[[genesis-mythos-master-goal]]"
validation_status: pattern_only
---

# Conceptual decision record — API core-protection boundary

## Summary

Lock **core protection via a versioned API boundary**. Modules (first-party or community) do not reach into protected core. They interact only through published API ports indexed by SeamRegistry. This is an **authority upgrade** of existing modularity seams — not a remine of frozen Phase 1–4 trees and not a Godot implementation pass.

Living classification: [[api-core-protection-inventory]]. Contract sketch: [[gmm-api-surface-v0]].

## PMG alignment

Serves open-source aggressive modularity, Operator modularity (pack/system-module swap without forking the engine), and the dual-perspective + intentional re-generation selling points by keeping camera/agency/tick/regen authority stable while still allowing remixable flavors and packs.

## Alternatives and tradeoffs

| Alternative | Upside | Downside | Why not chosen |
| ----------- | ------ | -------- | -------------- |
| Keep direct seam-slotting forever | Zero new doctrine | Community modules can break FP/DM and re-gen invariants | Rejected — open remixing without a boundary erodes the highlight |
| Full public API design before exemplar | Clear contracts early | Velocity death; designs without play proof | Rejected — v0 internal only; Phase 5 formalizes public |
| Remine Phase 1–4 for API language | Uniform wording | Burns freeze; dual-rail camera work | Rejected — CDR + inventory + thin amends |
| Deeper first-party access with no sunset | Faster factory/demo | Public API-only rule erodes by 6.4 | Rejected — sunset rule below |

**Chosen path:** CDR + single living inventory + thin PMG/charter/Phase amends + `gmm-api-surface-v0.yaml`.

## Binding rules (normative)

1. **Provisional promotion:** A provisional slot becomes a real versioned port when a first-party flavor is required by the exemplar loop **or** when a pack swap needs it. Until then it stays named-only and must **not** be implemented as a direct core reach.
2. **Deeper-access sunset:** First-party deeper binding (factory/demo) is temporary and must be justified. Any deeper binding still present at **Phase 6.4 acceptance** must be **removed** or **promoted into a documented internal-only port**. Public path remains API-only.
3. **`propose` is not mutate:** Capability verb `propose` (especially for re-generation or canon) is always subject to ConflictArbiter / NarrativeDeltaVetoPolicy / existing overwrite–regen gates — never a direct write of protected state.

## Consequences

- Inventory note is the **only** full classification table; other surfaces point at it.
- Phase 5 owns the versioned public extension API when formalized; v0 is internal/first-party.
- Phase 6.2 / 6.4 acceptance: exercise **both** a systemic flavor port and a pack-level swap; check deeper-access sunset at 6.4.
- LOD / Lighting / GraphicsSettings provisional ports sit under **Presentation**, not Simulation.
- No Code-Repos / Godot skeleton in this pass.

## Validation evidence

- Operator plan + refinements 2026-09-28 (API sheet; provisional promotion; deeper-access sunset; propose gate; Presentation placement; dual-hole Phase 6 acceptance; inventory as single source)
- Pattern: Factorio / Forge-style mediated extension (authority + published surface) — pattern_only
- Existing SeamRegistry seed: [[Phase-1-3-1-SeamRegistry-Canonical-Index-Roll-up-2026-06-29]]

## Links

- Master goal: [[genesis-mythos-master-goal]]
- Parent: [[Phase-1-Conceptual-Foundation-and-Core-Architecture-Roadmap-2026-06-26-0914]]
- Inventory: [[api-core-protection-inventory]]
- Schema: [[gmm-api-surface-v0]]
- Related: [[Conceptual-Decision-Records/reference-exemplar-dual-goal-2026-08-01]]
- Charter: [[REFERENCE-EXEMPLAR-CHARTER]]
