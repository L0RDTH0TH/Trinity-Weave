---
title: Meta lens review bundle 2026-06-05
created: 2026-06-05
tags: [maintenance-trinity, meta, review]
status: review_before_lock
---

# Meta lens review bundle (2026-06-05)

Operator review bundle — **do not lock** until reviewed. Apply with `--operator-mutation` to `components/` or promote from proposals per Phase 11 charter.

## New A-meta (provisional drafts)

| id | File |
|----|------|
| `factory_lifecycle_doctrine` | [[.technical/weave/component-proposals/meta-review-20260605/factory_lifecycle_doctrine.yaml]] |
| `config_knob_parity` | [[.technical/weave/component-proposals/meta-review-20260605/config_knob_parity.yaml]] |
| `maintenance_honesty_anchor` | [[.technical/weave/component-proposals/meta-review-20260605/maintenance_honesty_anchor.yaml]] |

## Amendments to locked meta (re-lock after review)

| id | File | Changes |
|----|------|---------|
| `agent_implementation_style` | [[.technical/weave/component-proposals/meta-review-20260605/agent_implementation_style.yaml]] | efficiency/robustness/maintainability precedence; honesty Rules; anti-overconfidence |
| `harness_runtime_contract` | [[.technical/weave/component-proposals/meta-review-20260605/harness_runtime_contract.yaml]] | host capability tiers; honesty budget per speed_mode; knob parity proof expectation |
| `trinity_prompt_context` | *(incl. **Face C Query**)* | [[.technical/weave/component-proposals/meta-review-20260605/trinity_prompt_context.yaml]] | meta_prepend_order; task_meta_faces; redesign_factory + expand_self task kinds |
| `trinity_card_authoring` | [[.technical/weave/component-proposals/meta-review-20260605/trinity_card_authoring.yaml]] | `factory_run` card_kind extension; factory_lifecycle cross-ref |

## Operator decisions before lock

1. **Three new meta vs two** — keep `maintenance_honesty_anchor` separate or merge into `agent_implementation_style` (precedence line documents either).
2. **11b code sync** — after lock, update `trinity_prompt_context_slice.py` `META_PREPEND_ORDER`, `LEG_INCLUSION`, `TaskKind` to match amended `trinity_prompt_context` (not in this bundle).
3. **Query slice** — implement `resolve_trinity_query` + `TrinityQueryResult` in `trinity_prompt_context_slice.py` (read-only guards).
4. **Registry** — add three ids to maintenance partition meta registry row count (18 + meta → explicit expand).

## Lock order (suggested)

1. `maintenance_honesty_anchor` OR merge into #1 first (your call)
2. `config_knob_parity`
3. `factory_lifecycle_doctrine`
5. Amendments: `agent_implementation_style` → `harness_runtime_contract` → `trinity_card_authoring` → `trinity_prompt_context`
