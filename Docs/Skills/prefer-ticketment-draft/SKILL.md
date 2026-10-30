---
name: prefer-ticketment-draft
description: >-
  Draft one Prefer from an open ticket-map row before Gate A / B₁. Loads only
  the Ticketment bundle (active map, done-sentence, Order, section charter,
  this row, same-section open neighbors as out_of_scope). Does not weld.
  Use when writing a map Prefer. Incomplete when no harness person observer.
  B₁ terminal → archive. Do not free-re-author from B₁ refuse strings.
---

# Prefer Ticketment draft (before Gate A / B₁)

## When

- Before any Prefer∩map Success claim
- When Gate A reports `forms_fail` (sibling consume / OOS / form bind / Walk paste) and the Prefer must be rewritten from the bundle
- **Not** for welding LIVE, Gate B₂, GREENLIGHT, or FactoryEat
- **Not** to shop catalog stubs so Gate A stays green
- **Not** to mint rN+1 from a B₁ terminal stand-in refuse (archive that packet)

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
4. `row` verbatim (`product_job` + notes + `observe` + `touch`)
5. `section_open_neighbors` / `out_of_scope_ticket_ids` — each marked out of scope
6. Dual-grid / place host law **only** when `load_dual_grid_host_law: true`
7. `person_observer_ready` from the harness (bundle reports it). Prefer YAML cannot set it true.

Do **not** load the mini-game archive, dual-grid Prefer seats, or other sections unless this row is the place/dual seat. Do **not** emit System or Walk into Prefer fields. Do **not** write the map `Touch` cell (human-authored on the map only).

## Emit

Write/update `{slice_id}.armed.yaml` (and Prefer brief if used) with:

| Field | Rule |
|-------|------|
| `ticket_map_id` | Exact row id |
| `proof_shape` / `claim_class` | **From map `observe`:** `person` → moment / ask_success; `record` → contract / component. Do not blur |
| `prefer_class` | `foundation` for contract substrate rows; `place` / `craft` only when the row is that seat **and** you set `topology_law: true` |
| `structural_success` | This row’s **product_job verbatim only**. Never System. Never Walk. Gate A fails Walk paste |
| `out_of_scope_ticket_ids` | **Exact** list from the bundle |
| `behavior_keys` | **Contract:** ≥1 invariant/operation key; **zero** visibility. **Moment (`f5`):** 3–5 stranger-watchable keys from **this** row — not Walk steps |
| `behavior_key_checks` | See Touch rules below |
| `missing_observer` | Only on the incomplete person path (below) |
| `status` | `incomplete_missing_observer` only on that path. Do **not** set factory `armed_*` |
| `success_object` | Capability / visible board act for this row only |
| `do_not_waive` | Full product-map set |
| `checklist_ids` | Prefer-declared only. Contract default = `[]` |
| `welds` / `W1`… | Only if the row’s **Welds** column explicitly lists them |
| `topology_law` | `true` **only** when this Prefer truly rewrites topology |

### Touch rules (binding)

Map `Touch` is `f5` or `none` and matches `Observe`. Ticketment does **not** write Touch.

- **`f5` (`person`)** and harness `person_observer_ready` is **false** → `behavior_key_checks: {}`, `missing_observer: person_window_pointer` (or the named missing person harness), `status: incomplete_missing_observer`. Do not arm. Do not call B₁.
- **`f5`** and harness person observer **ready** → attach only harness-owned window+click probes. Catalog `argv` does not qualify.
- **`none` (`record`)** → do **not** emit `person_window_pointer` or any person incomplete path. Bind a harness **record** probe, or stop. Do not shop a print stub so Gate A stays green. Do not use `proof_shape: moment` / ask_success as an F5 claim on `none`.

Do **not** set `factory_greenlit: true`. Do **not** FactoryEat. Do **not** set hostile ok bits.

## After draft

1. Gate A: `prefer_map_fidelity_check.py --armed …`
   - `forms_ok` → continue
   - `incomplete_missing_observer` → stop (exit ≠ 0; no B₁)
   - `forms_fail` → fix from the bundle (incl. Walk paste / missing Touch / none_demands_person)
2. Gate B₁: **only** when `forms_ok`:
   `prefer_senior_gate --gate b1 --factory-order --armed …`
3. Operator GREENLIGHT only after stored B₁ `ok: true` → weld → B₂ → **F5 only for `f5`/moment**; contract/`none` closes on probe pass

B₁ terminal → archive. Incomplete → wait for harness person observer on `main`. B₂ may cite the section Walk as a gap question and **cannot** stamp Walk done / GREENLIGHT / hostile bits.

## Observe (binding)

Copy the row. `structural_success` = product job **verbatim**. Shape/claim from `observe`. Attach probes only when harness-owned for that observe class. Else incomplete (person/`f5` only) or stop (`none`). Do **not** shop the catalog for Gate A.
