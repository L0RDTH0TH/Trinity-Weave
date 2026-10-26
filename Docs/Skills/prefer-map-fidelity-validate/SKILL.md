---
name: prefer-map-fidelity-validate
description: >-
  Gate B₁ is harness-owned. This skill must NOT stamp map_fidelity_hostile_ok.
  Use after Ticketment + Gate A to remind: run prefer_map_fidelity_check.py --write-b1.
  Does not replace Gate B₂ weld intent or operator F5.
---

# Prefer map fidelity (Gate B₁ — harness only)

## When

- After Ticketment draft and Gate A green
- Before any Prefer Success altitude on Prefer-applicable product slices

## Do not stamp

**Forbidden:** writing `map_fidelity_hostile_ok: true` or nested `map_fidelity_hostile.ok` from this skill / the same invocation that drafted the Prefer.

Harness only:

```bash
PYTHONPATH=scripts python3 scripts/prefer_map_fidelity_check.py \
  --armed 1-Projects/<project>/Factory-DRB/slice-briefs/<slice>.armed.yaml \
  --write-b1
```

Pass bit requires `map_fidelity_hostile.source == harness_b1`. Bare author `map_fidelity_hostile_ok: true` is ignored everywhere.

## What B₁ checks

Inputs: map row + `observe` + runner source for each named probe. Not the author’s summary.

Runner class (from code path, not catalog text) must equal row `observe`:

- window + pointer inject → `person`
- stdout / file / command compare → `record`

A `person` row whose probe runs a script and reads yaml fails here, whatever the op is called.

## Gate A (forms) reminder

Gate A does not decide truth. A form-complete stand-in can pass A and still fail B₁.

## Not your job

- Welding LIVE code
- Gate B₂ (`prefer-weld-intent-validate` / harness B₂)
- Operator F5
- Shopping the catalog for an op Gate A “accepts”
