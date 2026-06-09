---
title: Grok observability contract
created: 2026-06-09
audience: grok_github_integration
---

# Grok observability contract

This doc defines what Grok **can** and **cannot** observe from Trinity-Weave, and which files to cite.

## Observable (committed git only)

| Signal | Location | Refresh |
|--------|----------|---------|
| Card catalog | `weave/CARD-INDEX.md`, `OBSERVABILITY.json` | Each `weave_public_sync` |
| Last publish time | `OBSERVABILITY.json` → `last_publish_utc` | Each sync |
| Content fingerprint | `OBSERVABILITY.json` → `fingerprint` | Each sync |
| Locked meta ids | `OBSERVABILITY.json` → `meta_card_ids` | Each sync |
| Registry | `weave/trinity-partition-registry.yaml` | Each sync |
| Harness entrypoint | `scripts/eat_queue_core/harness.py` | Each sync |

## Not observable (do not invent)

- Current prompt-queue contents
- `Ingest/Lane-Status-Board.md` live state
- Watcher-Result / Errors append-only tails unless user pastes
- Any path under `1-Projects/`, `Ingest/`, `.technical/parallel/`

## Citation rules

1. Name **repo + branch** (`L0RDTH0TH/Trinity-Weave`, `main`)
2. Cite **file path** from this repo (not vault-relative `3-Resources/...`)
3. For card questions, open `weave/components/<trinity_id>.yaml`
4. If `OBSERVABILITY.json` is stale vs user claim, say: *committed snapshot may lag private vault*

## Response template for "what happened last run?"

> I only see committed Trinity-Weave files. Last publish: `<last_publish_utc>` (commit `<last_commit_short>`). For live EAT-QUEUE or Watcher state, paste the artifact or check `genesis-mythos-master-roadmap` integration branch if exported.

## Related operator doc

Full multi-repo routing: `Docs/Grok-Second-Brain-Custom-Instructions.md` (also exported).
