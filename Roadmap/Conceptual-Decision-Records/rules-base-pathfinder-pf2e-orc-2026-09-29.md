---
title: Conceptual decision record — Rules base Pathfinder PF2e / ORC (SUPERSEDED)
created: 2026-09-29
tags: [conceptual-decision-record, roadmap, genesis-mythos-master, rules-engine, character-creation, pathfinder, legal-posture, superseded]
para-type: Project
project-id: genesis-mythos-master
parent_roadmap_note: "[[Phase-5-1-Rule-Engine-Primitives-and-Plugin-Hooks-Roadmap-2026-06-26-2045]]"
decision_kind: other
queue_entry_id: null
master_goal: "[[genesis-mythos-master-goal]]"
validation_status: superseded
status: superseded
supersedes: "[[rules-base-srd-5-1-cc-by-2026-07-21]]"
superseded_by: "[[rules-base-pathfinder-pf1-2026-09-29]]"
related_research:
  - Ingest/Agent-Research/Stack-Gaps/gap-stack-rules-engine.md
  - Ingest/Agent-Research/Stack-Gaps/gap-stack-character-creation.md
---

# Conceptual decision record — Rules base Pathfinder PF2e / ORC (**SUPERSEDED**)

> **Superseded 2026-09-29** by [[rules-base-pathfinder-pf1-2026-09-29]] — operator correction: first plugin is **Pathfinder 1e (PF1)**, **not** PF2e/ORC. Keep this note for audit only.

## Summary

**Operator legal-posture switch (2026-09-29):** replace the prior **D&D / SRD 5.1 CC-BY** first-plugin lock with **Pathfinder Second Edition (PF2e)** as the default rules/IP posture for Genesis Mythos Master. Prefer **ORC**-compatible Pathfinder reference material for the first `RulesetPlugin` content base on the **Godot 4.6.3 .NET** host. Host primitives stay **ruleset-agnostic** (`IRulesPluginHost` / `IDiceRoller` / plugin load) — this is a **content/IP posture** change, not an engine swap.

**Edition:** Vault had **no prior Pathfinder (PF1/PF2) lock**. Grok share body was not machine-readable beyond title/meta (client-rendered). Default **PF2e + ORC** per operator intent and current industry open-licensing norm unless a later operator note locks PF1.

**Correction:** Later same-day operator lock chose **PF1** — see superseding CDR.

**Not legal advice.** This CDR records product intent and risk avoidance at a high level; counsel or license text review remains operator-owned before shipping branded packs.

## PMG alignment

Genesis needs a shippable fantasy rules surface for character creation, checks, and sim hooks while reducing exposure to **Wizards of the Coast / D&D / OGL-adjacent** IP and community-dump risk. Pathfinder (Paizo) + ORC-oriented open material is chosen as the **default Exemplar rules fill**; alternate rulesets remain swappable plugins.

## Alternatives and tradeoffs

| Alternative | Upside | Downside | Why not chosen |
| ------------- | ------ | -------- | -------------- |
| Keep SRD 5.1 CC-BY + 5e-bits seed ([[rules-base-srd-5-1-cc-by-2026-07-21]]) | Already researched; familiar 5e feel | Operator legal decision: exit D&D/WotC orbit | Superseded by this CDR |
| OGL / SRD 5.1 OGL mirrors | Familiar dumps | OGL policy risk; prior CDR already forbade OGL strings | Still forbidden |
| Pathfinder 1e (OGL-era lineage) | Familiar older PF community | PF1 licensing/history more tangled; not industry default for new digital tools | Default PF2e unless operator locks PF1 |
| Pure homebrew / system-neutral only | Max IP distance | Slows Exemplar campaign bar; weaker shared vocabulary | Exemplar still needs a concrete first plugin |
| ToV / A5E as first plugin | Compatible-ish with prior 5e research | Still in D&D-compatible product space operator is exiting | Deferred as optional later plugins if ever desired |

**Chosen path:** **PF2e / ORC** first `RulesetPlugin` posture; DiceRoller + ruleset-agnostic host retained; SRD 5.1 / 5e-bits / “D&D-like” first-plugin lock **superseded**; Execution notes **pending repaint/deepen** (no full 64-note rewrite this pass).

## Validation evidence

- Operator decision (this session): switch D&D → Pathfinder for legal reasons.
- Grok share (operator cite; body not fully fetchable here): [Pathfinder IP: Homebrew Legal?](https://grok.com/share/c2hhcmQtMw_57ad38df-53eb-410e-bc1e-bbb62068f8d9) — title + meta snippet compare Paizo forgiveness vs WotC / licensing hubbub; treat as conversation pointer, not counsel.
- Prior (superseded) lock: [[rules-base-srd-5-1-cc-by-2026-07-21]]
- Gap synth (architecture still useful; content base outdated): [[Ingest/Agent-Research/Stack-Gaps/gap-stack-rules-engine]] · [[Ingest/Agent-Research/Stack-Gaps/gap-stack-character-creation]]
- Host modularity parent: [[Phase-5-1-2-RulesetPlugin-PluginHookManifest-and-PluginLoader-Roadmap-2026-07-16-0928]]

## Links

- Parent roadmap note: see frontmatter `parent_roadmap_note`
- PMG: [[genesis-mythos-master-goal]]
- Manifest: `1-Projects/genesis-mythos-master/Factory-DRB/Tech-Stack-Manifest-v1.yaml`
- Execution state stamp: [[Roadmap/Execution/roadmap-state-execution]] (`ruleset_lock`)
- Currency pass (historical 2026-07-21): [[1-Projects/genesis-mythos-master/Factory-DRB/Currency-Pass-2026-07-21]]
