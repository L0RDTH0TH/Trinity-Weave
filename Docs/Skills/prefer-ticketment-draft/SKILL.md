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
| `proof_shape` | **Required.** `contract` (function/file fact; probe-only) or `moment` (point/watch act on a tiny board). Pick one — do not blur |
| `claim_class` | Map tickets: `component` (with contract) or `ask_success` (with moment). **Never** `staging` |
| `prefer_class` | `foundation` for contract substrate rows; `place` / `craft` only when the row is that seat **and** you set `topology_law: true` |
| `structural_success` | This row’s **capability** after sibling words are removed — narrowing is correct; copying a fat neighbor job is wrong. You may drop sibling jobs; you may **not** replace this row’s act with a lookup/shell while keeping the act’s words. **Contract:** no “point,” “see,” “GM,” or “board.” **Moment:** the same act you will F5 (point/see/stay on a tiny board) |
| `out_of_scope_ticket_ids` | **Exact** list from the bundle (Gate A fails if missing or mismatched) |
| `behavior_keys` | **Contract:** ≥1 invariant/operation key; **zero** visibility keys (mixed fails). **Moment:** 3–5 stranger-watchable keys. Do not fatten contract Prefers to 3–8. Classify by role, not a denylist of two example strings |
| `behavior_key_checks` | **Required when `behavior_keys` non-empty.** Map each key → one opaque proof-catalog probe id. Play-path Prefer text **or** play-path map-row job → every probe op must be costume-free `point_hits_solid` (no `equals_from` / `entrypoint` / `selector`). `entrypoint_result_equals` fails. Empty/unresolved checks fail. One probe must not green every key |
| `success_object` | **Contract:** capability outcome for this row. **Moment:** the visible board act. “Demo” = sibling system / LaunchShell — not the board; do not delete the act by framing success as “not a demo” |
| `do_not_waive` | Full product-map set (incl. session-prep codes on this map) |
| `checklist_ids` | Prefer-declared only. Contract default = `[]`. `None` on a map eat fails closed. Not a substitute for `behavior_key_checks` |
| `welds` / `W1`… | Only if the row’s **Welds** column explicitly lists them — never invent from free Notes |
| `catalog_row_id` / `lane` / `launch_scene` | Only if the **map row names** that exact value. Body prose (“not LaunchShell”) does not set `launch_scene` |
| `topology_law` | Set `true` **only** when this Prefer truly rewrites topology. Refuse codes / “lattice” prose do **not** arm it |

Do **not** set `factory_greenlit: true`. Do **not** FactoryEat.

## After draft

1. Gate A: `prefer_map_fidelity_check.py --armed …` (play-path Prefer **or** map-row job → every check must be `point_hits_solid`; unresolved = fail)
2. Gate B₁: `prefer-map-fidelity-validate` (sibling swallow still fails; Gate A non-zero blocks B₁ stamp)
3. Operator GREENLIGHT only → weld → B₂ → **F5 only for moment**; contract closes on probe pass (do not ask F5)

If B₁ can pass a Prefer whose success describes a different open ticket, Ticketment is not done — re-draft from the bundle. If the map job is a point/see/board ask, Prefer checks must be `point_hits_solid` — do not use `entrypoint_result_equals` / yaml lookup wearing a coordinate.
