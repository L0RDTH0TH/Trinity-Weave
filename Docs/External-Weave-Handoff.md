---
title: External Weave Handoff
created: 2026-06-09
updated: 2026-07-17
tags: [weave, trinity-weave]
status: draft
---

# External Weave Handoff

**Status:** Light architecture slice on [Trinity-Weave](https://github.com/L0RDTH0TH/Trinity-Weave). Enough to **read** the maintenance grammar; full adopter wrap is separate work.

## Weave Core (light)

| Layer | Receiver gets | Receiver mutates |
|-------|---------------|------------------|
| Harness + weave Python | `scripts/eat_queue_core/weave/`, schedule plane | Config knobs; host adapter |
| Locked maintenance_core meta | `weave/components/*.yaml` | Operator mutation + re-lock |
| Provisional corps cards | `weave/component-proposals/*.yaml` | Promote / evolve via harness |
| Host law | `weave/host-weld/live/` | Extend via host-weld pattern |
| Their factories / projects | — | Author on `project/<id>` branches |

## Mutation tiers

1. **maintenance_core** — automation read-only; operator ack + mutation flag to edit
2. **conceptual_spine** — consumable locked doctrine
3. **provisional** — active law on `main`; may evolve

## Reference deployment

The operator workspace that authors this export is private. Runtime queues and unpublished paths do not ship here.
