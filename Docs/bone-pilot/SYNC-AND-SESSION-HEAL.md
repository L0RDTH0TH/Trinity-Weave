# Sync and session heal

## Local-first

1. Vault changes → harness regen indexes (free)
2. `project_bridge_sync` → local commit on Trinity export checkout (free vs GitHub)
3. `project_bridge_push` → remote push when budget allows

```bash
PYTHONPATH=scripts python3 -m scripts.eat_queue_core.harness project_bridge_sync --vault-root .
PYTHONPATH=scripts python3 -m scripts.eat_queue_core.harness grok_bridge_status --vault-root .
```

## Safe branch switch

The harness uses **one export checkout** (`trinity-weave-export`):

1. Verify remote is **Trinity-Weave** (not gmmr / Curator)
2. Record session in `.technical/grok-bridge/export-session.json`
3. Checkout `project/<id>`, copy files, commit
4. Restore checkout to `main`

## Session heal (crash)

If a sync is interrupted, the next run reads `export-session.json`, restores `main`, and clears the session. Check [[../Grok-Bridge-Status|Grok-Bridge-Status]] for `recommendation`.

## Status

See `Docs/Grok-Bridge-Status.md` for `push_main_recommended`, `local_fresh`, etc.
