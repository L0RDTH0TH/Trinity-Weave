---
title: Gate-Precedence-Conflict-Doctrine-v1
project-id: godot-genesis-mythos-master
status: active
operator_signed: false
---

# Gate Precedence & Conflict Doctrine v1

**Normative.** Harness module: `scripts/eat_queue_core/weave/factory/gate_precedence.py`

## Tiers

| Tier | Meaning | Waivable at Closed Alpha? |
|------|---------|---------------------------|
| **A** | Hard veto — spine, integration, interpretation (meaning) | **No** |
| **B** | Human-facing — **Surface** (`usability_pass`), art, audio placeholder | **No** without degraded mode + operator_feedback |
| **C** | Polish — balance, juice, extensibility | Yes (Beta default) |
| **D** | Rollup only — `release_readiness_pass`, `closed_alpha_release_readiness_pass` | **Cannot waive A or B** |

## Surface vs Interpretation (mandatory split)

| Seat | Question |
|------|----------|
| `interpretation_pass` | What does Sparky **mean**? (DRB / IIB) |
| `surface_pass` / `usability_pass` | Can a human **operate** it? (playtest + checklist) |

**Anti-pattern:** `interpretation_pass` green while `surface_pass` red → **tier_d_waives_tier_b**

## Closed Alpha minimum (Product 2)

Tier **B** required before `closed_alpha_release_readiness_pass`:

- `surface_pass` green
- `operator_feedback` on all **kinesthetic** checklist IDs **pass: true**
- Six lane charters **active**

Tier **D** `operator_closed_alpha_vetted` without Surface green → **`premature_alpha_sign_without_surface_pass`**

## Enforcement

```bash
python -m eat_queue_core.weave.factory.cli surface-pass --vault-root .
python -m eat_queue_core.weave.factory.cli closed-alpha-passes --vault-root .
```

Config: `factory_orchestrator.surface_pass_gate: block`

## Related

- [[Factory-DRB/usability-navigation-v1]]
- [[Factory-DRB/usability-launch-v1]]
- [[Factory-DRB/Factory-Honesty-Recovery-Doctrine-v1]]
