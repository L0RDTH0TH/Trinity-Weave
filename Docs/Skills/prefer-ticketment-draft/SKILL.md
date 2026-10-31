---
name: prefer-ticketment-draft
description: >-
  Draft one Prefer from an open ticket-map row before Gate A / B₁. Loads only
  the Ticketment bundle (active map, done-sentence, Order, section charter,
  this row, same-section open neighbors as out_of_scope). Does not weld.
  Use when writing a map Prefer. f5 uses operator after_build (empty checks).
  B₁ terminal → archive. Do not free-re-author from B₁ refuse strings.
---

# Prefer Ticketment draft (before Gate A / B₁)

## When

- Before any Prefer∩map Success claim
- When Gate A reports `forms_fail` (sibling consume / OOS / form bind / Walk paste) and the Prefer must be rewritten from the bundle
- **Not** for welding LIVE, Gate B₂, GREENLIGHT, or FactoryEat
- **Not** to shop catalog stubs so Gate A stays green
- **Not** to mint rN+1 from a B₁ terminal stand-in refuse (archive that packet)
- **Not** to extend Trinity / harness so a Prefer may leave incomplete

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
| `behavior_key_checks` | `{}` before eat is legal. Bind real probes only when harness owns them — never stubs |
| `observer` / `observer_when` | **`f5` only:** `operator` / `after_build`. Omit on `none` |
| `missing_observer` | **Do not emit.** Gate A fails it |
| `success_object` | Capability / visible board act for this row only |
| `do_not_waive` | Full product-map set |
| `checklist_ids` | Prefer-declared only. Contract default = `[]` |
| `welds` / `W1`… | Only if the row’s **Welds** column explicitly lists them |
| `topology_law` | `true` **only** when this Prefer truly rewrites topology |

### Touch rules (binding)

Map `Touch` is `f5` or `none` and matches `Observe`. Ticketment does **not** write Touch.

- **`f5` (`person`)** → `observer: operator`, `observer_when: after_build`, `behavior_key_checks: {}`. Do **not** emit `person_window_pointer`. Do **not** stop for a missing harness robot. You are the person check after build.
- **`none` (`record`)** → do **not** emit person observer fields or incomplete person path. Empty checks legal. Do not use `proof_shape: moment` / ask_success as an F5 claim on `none`.

Do **not** set `factory_greenlit: true`. Do **not** FactoryEat. Do **not** set hostile ok bits.

## After draft

1. Gate A: `prefer_map_fidelity_check.py --armed …`
   - `forms_ok` → continue
   - `forms_fail` → fix from the bundle (Walk paste / missing Touch / none_demands_person / missing_observer)
2. Gate B₁: **only** when `forms_ok`:
   `prefer_senior_gate --gate b1 --factory-order --armed …`
3. Operator GREENLIGHT only after stored B₁ `ok: true` → weld → B₂ → **F5 only for `f5`/moment**; contract/`none` closes on probe pass

B₁ terminal → archive. B₂ (after build) may cite the section Walk as a gap question / f5 handoff list and **cannot** stamp Walk done / GREENLIGHT / hostile bits.

## Observe (binding)

Copy the row. `structural_success` = product job **verbatim**. Shape/claim from `observe`. Empty checks legal before eat. Do **not** shop the catalog for Gate A. Do **not** extend Trinity to pass a gate.
