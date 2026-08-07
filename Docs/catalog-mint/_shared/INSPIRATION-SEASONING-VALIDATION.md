---
title: Inspiration seasoning validation (pin-gate shape)
audience: grok_github_integration
updated: 2026-08-07
---

# Inspiration seasoning validation

**First-class post-Conceptual MO (ladder v4)** — after `apply_pins`, **before Pass B**. Same receipt discipline as pin derive. **Not** PIN-INDEX Conceptual welds. **Not** a catalog form pin.

**Frame:** [[CATALOG-MINI-TRINITY]] · [[INSPIRATION-UX-FEEDSTOCK]]. Output = seasoning **slaved** to matched Conceptual/series.

## Preconditions

1. Series Trinity published.  
2. Conceptual pins applied (`apply_pins`) or lawful waive on planned rows.  
3. Inspiration feedstock present **or** operator **waives** seasoning mine (record waive on receipt).

## Weld / map contracts

1. Candidate ids come from feedstock `cards/` (derived move-pins) — not invented game-title Conceptual pins.  
2. Each accepted map: `derived_pin_id` → `maps_to_series[]` and/or Conceptual pin title/id.  
3. ≥1 **refuse** remains on the card / map.  
4. Hyper-fit (“this is basically Forge”) demoted to pattern language.  
5. Grok ≠ invent feedstock cards; propose maps and gate judgment only.

## Failure modes

Unmapped strong cards left silent · game title proposed as `conceptual_pin` · seasoning without Conceptual anchor when pins exist · Pass B started before board close · treating seasoning as join-key peer of Conceptual.

## Velocity rules

Digest-first · one receipt per turn · max ~5 highest-signal issues · open STATUS first; full cards only for yellow/red.

## Mandatory receipt shape

```text
## Inspiration seasoning validation — <project_id>
Batch scope: [all feedstock cards | subset: <ids>]
Schema: seasoning v1 (slaved to Conceptual; not form pin)

### Pass / Fail summary
…

### Maps accepted (derived_pin_id → series / conceptual)
…

### Deferred / refused
…

### Waive (if any)
- reason: …

### Recommended next action
- Board confirm → apply seasoning (ASSUMPTION-LOG + L5 cites) → Pass B
```

## Operator close

- Board confirm → apply seasoning → **Pass B**  
- Or waive → Pass B with waive on receipt  
- Do **not** start Pass B while seasoning board is open and feedstock exists without waive
