---
title: Conceptual decision record — Rules base SRD 5.1 CC-BY
created: 2026-07-21
tags: [conceptual-decision-record, roadmap, genesis-mythos-master, rules-engine, character-creation]
para-type: Project
project-id: genesis-mythos-master
parent_roadmap_note: "[[Phase-5-1-Rule-Engine-Primitives-and-Plugin-Hooks-Roadmap-2026-06-26-2045]]"
decision_kind: other
queue_entry_id: null
master_goal: "[[genesis-mythos-master-goal]]"
validation_status: cited
related_research:
  - Ingest/Agent-Research/Stack-Gaps/gap-stack-rules-engine.md
  - Ingest/Agent-Research/Stack-Gaps/gap-stack-character-creation.md
---

# Conceptual decision record — Rules base SRD 5.1 CC-BY

## Summary

Lock **SRD 5.1** under **CC-BY-4.0** as the first `RulesetPlugin` content base on the **Godot 4.6.3 .NET** host. Use **5e-bits** packs only as a **convenience seed** (re-verify every string against CC-BY SRD; **no OGL** strings). Keep host primitives **ruleset-agnostic** (`IRulesPluginHost` / `IDiceRoller` / plugin load) so **ToV/A5E** can land as a **second RulesetPlugin** later — this is **RulesetPlugin modularity**, **not** an engine swap.

## PMG alignment

Genesis needs a lawful, shippable D&D-like rules surface for character creation, checks, and sim hooks without licensing landmines, while preserving the ability to host alternate tabletop rulesets behind the same Godot spine.

## Alternatives and tradeoffs

| Alternative | Upside | Downside | Why not chosen |
| ------------- | ------ | -------- | -------------- |
| OGL / SRD 5.1 OGL mirror | Familiar community dumps | OGL policy risk; forbidden strings | Explicit no-OGL; CC-BY only |
| AGPL libsrd5 (kupka) as engine | Ready SRD code | AGPL contaminates core | Excluded from spine |
| Engine-swap to another runtime for rules | Different ecosystem libs | Breaks locked Godot 4.6.3 .NET stack | Engine not swappable; plugins swap instead |
| Single monolithic rules binary | Faster first ship | Blocks ToV/A5E and homebrew | Host stays ruleset-agnostic |
| Floating ASI (post-5.1 style) for creation | Modern PHB familiarity | Diverges from locked SRD 5.1 species-baked bonuses | Character creation locks species-baked ASI |

**Chosen path:** SRD 5.1 CC-BY first plugin + DiceRoller behind `IDiceRoller` + Godot-hosted `IRulesPluginHost`; ToV/A5E deferred as second plugin; 5e-bits seed with provenance gate.

## Validation evidence

- Gap synth: [[Ingest/Agent-Research/Stack-Gaps/gap-stack-rules-engine]]
- Gap synth: [[Ingest/Agent-Research/Stack-Gaps/gap-stack-character-creation]]
- Live manifest rows `stack-rules-engine`, `stack-character-creation` → this CDR
- Dice: [skizzerz/DiceRoller](https://github.com/skizzerz/DiceRoller) (MIT)
- Architecture ref: [jamesplotts/opencombatengine](https://github.com/jamesplotts/opencombatengine)
- Prior tertiary: [[Phase-5-1-2-RulesetPlugin-PluginHookManifest-and-PluginLoader-Roadmap-2026-07-16-0928]]

## Links

- Parent roadmap note: see frontmatter `parent_roadmap_note`
- Manifest: `1-Projects/genesis-mythos-master/Factory-DRB/Tech-Stack-Manifest-v1.yaml`
- Currency pass: [[1-Projects/genesis-mythos-master/Factory-DRB/Currency-Pass-2026-07-21]]
