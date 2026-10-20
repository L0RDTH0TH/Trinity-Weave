---
name: prefer-ticketment-draft
description: >-
  Draft one Prefer from an open ticket-map row before Gate A / B₁. Loads only
  the Ticketment bundle (active map, done-sentence, Order, section charter,
  this row, same-section open neighbors as out_of_scope). Does not weld.
  Use when writing or rewriting a map Prefer, or when B₁ / sibling-consume
  fails and the Prefer must be re-authored.
---

# Prefer Ticketment draft (before Gate A / B₁)

## When

- Before any Prefer∩map Success claim
- When Gate A reports `job_consumes_sibling` / `out_of_scope_ticket_ids_*`
- When B₁ fails because the Prefer swallowed a neighbor row
- **Not** for welding LIVE, Gate B₂, GREENLIGHT, or FactoryEat

## Fixed load (nothing else)

Run:

```bash
PYTHONPATH=scripts python3 scripts/prefer_ticketment_bundle.py \
  --ticket <TICKET_MAP_ID>
```

Use **only** that JSON:

1. `map_id` / `map_note` from `factory-project.yaml` → `ticket_map_runtime` (ignore `release_tier`)
2. `done_sentence` + `order` — one screen, not the whole map note
3. `section_heading` + `section_charter`
4. `row` verbatim (`product_job` + notes)
5. `section_open_neighbors` / `out_of_scope_ticket_ids` — each marked out of scope
6. Dual-grid / place host law **only** when `load_dual_grid_host_law: true`

Do **not** load the mini-game archive, dual-grid Prefer seats, or other sections unless this row is the place/dual seat.

## Emit

Write/update `{slice_id}.armed.yaml` (and Prefer brief if used) with:

| Field | Rule |
|-------|------|
| `ticket_map_id` | Exact row id |
| `structural_success` | This row’s product job **after sibling words are removed** — narrowing is correct; copying a fat neighbor job is wrong |
| `out_of_scope_ticket_ids` | **Exact** list from the bundle (Gate A fails if missing or mismatched) |
| `behavior_keys` | 3–5 stranger-watchable claims on **this** row only (not `file_exists` / `compiles` / `menu_opens` / the two generic B₂ booleans alone) |
| `success_object` | Player-visible outcome for this row |
| `do_not_waive` | Full product-map set (incl. session-prep codes on this map) |
| `prefer_class` | Set `place` **only** if this ticket really is dual-grid place |

Do **not** set `factory_greenlit: true`. Do **not** FactoryEat.

## After draft

1. Gate A: `prefer_map_fidelity_check.py --armed …`
2. Gate B₁: `prefer-map-fidelity-validate` (sibling swallow still fails)
3. Operator GREENLIGHT only → weld → B₂ → F5

If B₁ can pass a Prefer whose success describes a different open ticket, Ticketment is not done — re-draft from the bundle.
