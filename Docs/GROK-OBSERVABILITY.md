---
title: Grok observability contract
created: 2026-06-09
updated: 2026-07-17
audience: grok_github_integration
---

# Grok observability contract

What Grok **can** and **cannot** observe from Trinity-Weave, and which files to cite.

## Observable (committed git only)

| Signal | Location | Refresh |
|--------|----------|---------|
| Card catalog | `weave/CARD-INDEX.md`, `OBSERVABILITY.json` | Each weave sync |
| **Product** slice-catalog (mint) | `Docs/catalog-mint/<project_id>/slice-catalog.yaml` (+ card `catalog_mint`) | `catalog_mint_pack_emit` / weave publish |
| Last publish time | `OBSERVABILITY.json` → `last_publish_utc` | Each sync |
| Content fingerprint | `OBSERVABILITY.json` → `fingerprint` | Each sync |
| Locked / provisional ids | `OBSERVABILITY.json` | Each sync |
| Registry | `weave/trinity-partition-registry.yaml` | Each sync |
| Project instances | `project/<id>` branch root | Each project sync |
| Bridge status | `Docs/Grok-Bridge-Status.json` | Status harness |

## Not observable (do not invent)

- Live prompt-queue contents
- Live Watcher / error tails unless pasted
- Fulfill resolve maps and pack bodies until a pack is pasted
- Unpublished local edits

## Citation rules

1. Name **repo + branch** (`L0RDTH0TH/Trinity-Weave`, `main` or `project/<id>`)
2. Cite **paths as they appear in this repo**
3. For card questions, open locked or provisional YAML and **cite promotion tier**
4. If `OBSERVABILITY.json` is stale vs operator claim, say committed snapshot may lag

## Response template for "what happened last run?"

> I only see committed Trinity-Weave files. Last publish: `<last_publish_utc>` (commit `<last_commit_short>`). For live runtime state, paste the artifact.

## Related

- `Docs/Grok-Second-Brain-Custom-Instructions.md` — pasteable Grok Chat contract (Trinity-only)
- `Docs/GROK-PROJECT-BRIDGE.md` — bridge tiers
