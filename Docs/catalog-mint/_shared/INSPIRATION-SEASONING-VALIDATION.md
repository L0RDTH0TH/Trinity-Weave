---
title: Inspiration seasoning validation (shared Conceptual pin gate)
audience: grok_github_integration
updated: 2026-08-07
---

# Inspiration seasoning validation

**Same Conceptual pin gate** — **required close condition**, not optional memory. Second mine / receipt section with PIN-DERIVE. **Not** a separate ladder unlock. **Not** a form pin.

**Machine close:** `INSPIRATION-SEASONING-RECEIPT.md` frontmatter:

```yaml
inspiration_seasoning_disposition: open | applied | waived
inspiration_seasoning_waive_reason: ""   # required when waived
```

Harness fail-closed while `open` (or missing reason on waive): `greenlight_children`, `lock_child_batch`, L5 draft.

## Preconditions

1. Series Trinity published.  
2. Conceptual pin derive in the same board.  
3. Feedstock cards present → maps expected; **or** operator sets `waived` + reason (e.g. no feedstock this cycle).

## Weld / map contracts

1. Candidates from feedstock `cards/` only.  
2. Accepted map: `derived_pin_id` → series / Conceptual.  
3. ≥1 refuse; challenge hyper-fit.  
4. Never game titles as `conceptual_pin`.

## Failure modes

Leaving disposition `open` · waive without reason · treating seasoning as optional chat memory · Pass B / L5 while open.

## Mandatory receipt shape

```text
## Inspiration seasoning (shared pin gate) — <project_id>
disposition: applied | waived
waive_reason: …   # if waived

### Maps accepted
…

### Recommended next action
- Close shared pin gate → Pass B
```

## Operator close

- Set disposition `applied` after maps applied to ASSUMPTION-LOG / L5 cites, **or** `waived` + reason  
- Then Pass B  
- Do **not** greenlight/lock Pass B or draft L5 while disposition is `open`
