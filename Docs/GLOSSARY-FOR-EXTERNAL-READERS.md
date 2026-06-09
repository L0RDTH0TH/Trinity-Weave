---
title: Glossary for external readers
created: 2026-06-09
audience: grok_github_integration
---

# Glossary (jargon → plain English)

Use this when YAML or docs use internal terms.

| Term | Plain meaning |
|------|----------------|
| **Trinity card** | YAML spec for one system concern (id, conceptual story, code touchpoints, rules, tests) |
| **Meta card** | Card with `card_kind: meta` — doctrine for how other cards or hosts behave |
| **Maintenance core** | Frozen registry ids; system read-only, operator may edit with logged harness flag |
| **Provisional** | Draft card under `component-proposals/` — **not shipped** to Trinity-Weave |
| **Touch** | Card leg listing primary code paths and harness commands |
| **Conduct / nerve test** | Automated check that card behavior signals match proof obligations |
| **Self-wrap** | Full maintenance pass: align cards, run corps tests, optional repair loop |
| **Schedule tick** | Periodic background orchestrator (`schedule_tick` / legacy `pseudo_clock_tick`) |
| **EAT-QUEUE** | Process prompt-queue JSONL lines and dispatch agent pipelines |
| **Host-weld** | Compiled host law (safety, bridge) — not the full `.cursor/rules` tree |
| **GitForge** | Post-queue git export to `genesis-mythos-master-roadmap` (separate from Trinity-Weave) |
| **Curator** | Private full-vault git backup |
| **Lane** | Parallel execution track (e.g. institute, godot, sandbox) |
| **Factory** | Pipeline that produces project output (ingest, roadmap deepen, etc.) |
| **Phase 18** | Deferred plan milestone for full external adopter packaging; Trinity-Weave is the light slice |
| **`[[wiki-link]]`** | Obsidian link — in public repo, resolve to path under `weave/` or `Docs/` |
