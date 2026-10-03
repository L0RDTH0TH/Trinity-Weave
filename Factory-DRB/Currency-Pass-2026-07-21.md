---
title: Currency Pass — Tech Stack 2026-07-21
created: 2026-07-21
tags: [factory-drb, currency-pass, genesis-mythos-master]
para-type: Project
project-id: genesis-mythos-master
status: complete
---

# Currency Pass — 2026-07-21

Receipt for pre-mint stack currency. Manifest header stamped `currency_pass_at: "2026-07-21"`. **`operator_stack_baseline_vetted` remains `false`** pending operator sign-off.

## Affirmed / updated

| Domain / row | Decision |
| ------------ | -------- |
| Engine | Stay **Godot 4.6.3 .NET / .NET 8**; not engine-swappable; **4.7 rc1 only** — do not move |
| CI (`stack-ci-gdunit4net`) | Org **MikeSchulze → godot-gdunit-labs**; pins **gdUnit4 6.1.x**, **gdUnit4.api 5.x**, **gdUnit4.test.adapter 3.0.0**, **Microsoft.NET.Test.Sdk 18.0.0** |
| Rules (`stack-rules-engine`) | **skizzerz/DiceRoller** behind `IDiceRoller` / `IRulesPluginHost.Roll`; ref opencombatengine; exclude AGPL libsrd5 + vokimon dice roller; **PF1 first-plugin** (2026-09-29; was 5e-bits CC-BY seed) |
| Character creation | **Pathfinder 1e (PF1)** tables pending remint (was SRD 5.1 species-baked) |
| Seed / UI | Re-affirm **first-party** `ISeedAuthority` / `IUiHost`; Toolkit.Mvvm default; DotPudica / GUML optional currency |
| Remaining domains | Light pass — `currency_checked_at: "2026-07-21"` on registry domains + gap docs |

## CDR

[[Roadmap/Conceptual-Decision-Records/rules-base-pathfinder-pf1-2026-09-29]] — anchors `rules_engine` + `character_creation` manifest rows (supersedes [[rules-base-pathfinder-pf2e-orc-2026-09-29]] and [[rules-base-srd-5-1-cc-by-2026-07-21]]).

## Surfaces touched

- `Factory-DRB/Tech-Stack-Manifest-v1.yaml`
- `Factory-DRB/Stack-Domain-Registry-v1.yaml`
- `Ingest/Agent-Research/Stack-Gaps/gap-stack-*.md`
