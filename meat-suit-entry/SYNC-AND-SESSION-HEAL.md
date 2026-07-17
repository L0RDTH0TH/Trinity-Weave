# Sync and session heal

## Local-first

1. Workspace changes → harness regen indexes
2. `project_bridge_sync` → local commit on Trinity export checkout
3. `project_bridge_push` → remote push when budget allows

```bash
PYTHONPATH=scripts python3 -m scripts.eat_queue_core.harness project_bridge_sync --vault-root .
PYTHONPATH=scripts python3 -m scripts.eat_queue_core.harness grok_bridge_status --vault-root .
```

## Safe branch switch

One export checkout for Trinity-Weave:

1. Verify remote is **this** Trinity-Weave remote
2. Record session (export-session)
3. Checkout `project/<id>`, copy files, commit
4. Restore checkout to `main`

## Session heal (crash)

If a sync is interrupted, the next run restores `main` and clears the session. Check `Docs/Grok-Bridge-Status.md` for `recommendation`.

## Status

See `Docs/Grok-Bridge-Status.md` for `push_main_recommended`, `local_fresh`, `awaiting_push_window`, etc.
