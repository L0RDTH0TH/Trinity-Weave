---
title: REFERENCE-EXEMPLAR-CHARTER — genesis-mythos-master
created: 2026-08-01
updated: 2026-09-29
tags: [reference-exemplar, genesis-mythos-master, modularity, charter]
para-type: Project
project-id: genesis-mythos-master
status: active
ruleset_lock: pathfinder_pf1
links:
  - "[[genesis-mythos-master-goal]]"
  - "[[Conceptual-Decision-Records/reference-exemplar-dual-goal-2026-08-01]]"
  - "[[Phase-6-4-Reference-Exemplar-Roadmap-2026-08-01]]"
  - "[[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-4-Reference-Exemplar/Phase-6-4-Reference-Exemplar-Roadmap-2026-08-01]]"
  - "[[api-core-protection-inventory]]"
  - "[[Conceptual-Decision-Records/api-core-protection-boundary-2026-09-28]]"
  - "[[1-Projects/genesis-mythos-master/Roadmap/Execution/Docs/Junior-Tech-Adapt-How-To]]"
  - "[[1-Projects/genesis-mythos-master/Roadmap/Execution/Docs/SeamRegistry-CSharp-Host-Index]]"
---

# REFERENCE-EXEMPLAR-CHARTER

Charter for the Medium Fantasy **Reference Exemplar** and the **swap matrix** it fills. Not an art bible. Not factory start. Normative Execution assembly path: [[1-Projects/genesis-mythos-master/Roadmap/Execution/Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-4-Reference-Exemplar/Phase-6-4-Reference-Exemplar-Roadmap-2026-08-01|Execution 6.4]].

## In scope

- Medium Fantasy default pack: coherent **chrome + world** visuals (solid, not spectacular)
- **Campaign-capable** worldgen DoD: generate a world that can run a complete campaign (not only a hand-placed ~30 min slice)
- Exemplar as **default filled row** of the swap matrix
- Authority split + invite package + DM push (**contracts named**; no protocol design here)
- Closed **pack-slot fill matrix** so juniors do not invent slots (Execution 6.4)

## Out of scope

- Freezing Exemplar as product law / only legal skin
- New UX mint series parents or remine
- Replacing horizon demo (6.2)
- Full modding L5, art bible, push/sync conflict UI, offline players
- Half B implementation / runnable game-repo Boot this pass

## Authority (footnote)

| Seat | What they can change | Gate |
|------|----------------------|------|
| **Player / character** | Visuals only (cosmetic) | Own character; no world/rules authority |
| **DM** | Calculation, lore, homebrew, rules packs, world-hitting content | World / campaign; campaign hooks may reference world package content but do not bypass world rules authority |
| **Invite accept** | Bound **world/campaign** package (rules, mods, content, visual defaults) | Attach on accept — not account-global |
| **Later DM updates** | Pack revisions → push to attached players | Same gate; players do not silently author the package |

*Invite acceptance installs the DM’s bound package; player cosmetics never substitute for package authority.* Cosmetics/backstory never auto-write world canon (DM gate).

## Swap matrix (charter ↔ Execution pack keys)

| Charter slot | Execution pack key / swap slot | Authority | Human path (DoD sketch) |
|--------------|-------------------------------|-----------|-------------------------|
| Rules / Pathfinder pack / calculation | `rules.plugin_id` → `slot.rules.plugin` (**pathfinder_pf1**) | DM / world | Pick → validate → attach; receipt `R.rules.pf1_bind` |
| Lore / homebrew / content | `rules.spell_meta` + quest pressure + faction | DM / world | Import → accept/revise → sim-active |
| Tone profile | ToneProfile / ProfileWeight (Phase 2.3) | DM / campaign | Session 0 / frame |
| World visual / biome language | `gen.terrain_admit` + `gen.pipeline_id` | DM / world | Import → preview → apply; Exemplar default kit |
| Visual / chrome pack | `ui.hud_stack` + art set `astroneer_bar_v0` | DM or table | Import → preview → apply; must not override world rules |
| Character cosmetic visuals | AuthorityPackageContract player pkg | Player | Local customize; not world law |
| System modules | API ports only (not core replacement) | Advanced / DM | Not required to run Exemplar; [[api-core-protection-inventory]] |

**Default-of-swap-matrix:** Exemplar occupies the official filled slots for rules + tone + world visual + chrome defaults until the DM swaps packs.

**Closed fill:** Junior uses Execution 6.4 **Pack-slot fill matrix** rows 1–19 only — no invent. Graybox OK. Demo loop never sole attestation.

**API boundary:** System modules and packs talk to core through the published API; protected core (cameras, agency, tick, re-gen) stays owned by System. See [[api-core-protection-inventory]] and [[Conceptual-Decision-Records/api-core-protection-boundary-2026-09-28]].

**CampaignCapableDoDGate:** Fail closed unless receipt ledger has all required ids with non-empty `verify` (templates on Execution 6.4).

## Status

Active charter aligned to Execution 6.4 fill-matrix tighten (2026-09-29). Roadmap leaf: [[Phase-6-4-Reference-Exemplar-Roadmap-2026-08-01]]. Game-repo Boot deferred (Half B).
