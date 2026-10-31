---
title: Conceptual decision record — Rules base Pathfinder 1e (PF1)
created: 2026-09-29
tags: [conceptual-decision-record, roadmap, genesis-mythos-master, rules-engine, character-creation, pathfinder, pf1, legal-posture]
para-type: Project
project-id: genesis-mythos-master
parent_roadmap_note: "[[Phase-5-1-Rule-Engine-Primitives-and-Plugin-Hooks-Roadmap-2026-06-26-2045]]"
decision_kind: other
queue_entry_id: null
master_goal: "[[genesis-mythos-master-goal]]"
validation_status: needs_human
supersedes: "[[rules-base-pathfinder-pf2e-orc-2026-09-29]]"
also_supersedes: "[[rules-base-srd-5-1-cc-by-2026-07-21]]"
related_research:
  - Ingest/Agent-Research/Stack-Gaps/gap-stack-rules-engine.md
  - Ingest/Agent-Research/Stack-Gaps/gap-stack-character-creation.md
---

# Conceptual decision record — Rules base Pathfinder 1e (PF1)

## Summary

**Operator correction (2026-09-29):** lock the default first `RulesetPlugin` / Reference Exemplar rules fill to **Pathfinder 1e (PF1 / “Pathfinder v1”)**, **not** Pathfinder 2e / ORC. The earlier same-day default to PF2e+ORC ([[rules-base-pathfinder-pf2e-orc-2026-09-29]]) was wrong and is **superseded**.

**Product id:** `pathfinder_pf1`. Host primitives stay **ruleset-agnostic** (`IRulesPluginHost` / `IDiceRoller` / plugin load) — this is a **content/IP posture** change, not an engine swap. DiceRoller (skizzerz, MIT) remains behind `IDiceRoller`.

**Naming (operator clarity, not counsel):**

| Phrase | Meaning in this vault |
|--------|------------------------|
| **PF1 / Pathfinder 1e / “Pathfinder v1”** | First-edition Pathfinder RPG rules vocabulary (d20 + modifiers, BAB/saves, skills, feats, spells-as-slots, etc.) used as the **first plugin content** target |
| **Paizo “Pathfinder” product naming** | Trademarked Paizo product line; do not treat vault shorthand as a license grant to ship Paizo marks or Golarion IP |
| **OGL / legacy PF1 open material** | Historical open-content lineage often discussed for PF1-era SRD/PRD-style tables; **operator owns** which open texts, Community Use / Compatibility statements, and trademark filters apply before ship |
| **PF2e / ORC** | Explicitly **not** the locked first plugin (superseded CDR) |

**Not legal advice.** This CDR records product intent and risk avoidance at a high level; counsel or license-text review remains operator-owned before shipping branded packs.

## PMG alignment

Genesis needs a concrete fantasy rules surface for character creation, checks, and sim hooks while staying out of **Wizards of the Coast / D&D / SRD 5.1** first-plugin orbit. Operator locks **PF1** as the Exemplar default fill; alternate rulesets (including a later PF2e plugin) remain swappable on the agnostic host.

## Alternatives and tradeoffs

| Alternative | Upside | Downside | Why not chosen |
| ------------- | ------ | -------- | -------------- |
| Keep PF2e / ORC ([[rules-base-pathfinder-pf2e-orc-2026-09-29]]) | Prior same-day lock; ORC-oriented tooling | **Operator correction:** wrong edition | Superseded |
| Keep SRD 5.1 CC-BY ([[rules-base-srd-5-1-cc-by-2026-07-21]]) | Already researched | Operator legal exit from D&D/WotC orbit | Still superseded |
| Pure homebrew / system-neutral only | Max IP distance | Slows Exemplar campaign bar | Exemplar still needs a first plugin |
| Dual-lock PF1+PF2e as “default” | Flexibility | Ambiguous junior remint path | Single first-plugin id: `pathfinder_pf1` |

**Chosen path:** **`pathfinder_pf1`** first `RulesetPlugin` posture; DiceRoller + ruleset-agnostic host retained; PF2e/ORC and SRD 5.1 / 5e-bits first-plugin locks **superseded**.

## Validation evidence

- Operator correction (this session): **PF1, not PF2e/ORC.**
- Grok share (operator cite; conversation pointer, not counsel): [Pathfinder IP: Homebrew Legal?](https://grok.com/share/c2hhcmQtMw_57ad38df-53eb-410e-bc1e-bbb62068f8d9)
- Superseded PF2e lock: [[rules-base-pathfinder-pf2e-orc-2026-09-29]]
- Prior (still superseded) SRD lock: [[rules-base-srd-5-1-cc-by-2026-07-21]]
- Gap synth (architecture still useful): [[Ingest/Agent-Research/Stack-Gaps/gap-stack-rules-engine]] · [[Ingest/Agent-Research/Stack-Gaps/gap-stack-character-creation]]
- Junior remint + tables scaffold: [[Roadmap/Execution/Docs/Junior-Tech-Adapt-How-To]] §4 · [[Roadmap/Execution/Docs/PF1-Ruleset-Content-Scaffold]]
- Host index bind: [[Roadmap/Execution/Docs/SeamRegistry-CSharp-Host-Index]] §B4

## Links

- Parent roadmap note: see frontmatter `parent_roadmap_note`
- PMG: [[genesis-mythos-master-goal]]
- Manifest: `1-Projects/genesis-mythos-master/Factory-DRB/Tech-Stack-Manifest-v1.yaml`
- Execution state stamp: [[Roadmap/Execution/roadmap-state-execution]] (`ruleset_lock: pathfinder_pf1`)
