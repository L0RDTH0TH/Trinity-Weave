---
name: prefer-ticketment-draft
description: >-
  Draft one Prefer from an open ticket-map row before Gate A / B₁. Loads only
  the Ticketment bundle (active map, done-sentence, Order, section charter,
  this row, same-section open neighbors as out_of_scope). Does not weld.
  Use when writing a map Prefer. Incomplete when no harness observer exists.
  B₁ terminal → archive. Do not free-re-author from B₁ refuse strings.
---

# Prefer Ticketment draft (before Gate A / B₁)

## When

- Before any Prefer∩map Success claim
- When Gate A reports `forms_fail` (sibling consume / OOS / form bind) and the Prefer must be rewritten from the bundle
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
4. `row` verbatim (`product_job` + notes + `observe`)
5. `section_open_neighbors` / `out_of_scope_ticket_ids` — each marked out of scope
6. Dual-grid / place host law **only** when `load_dual_grid_host_law: true`
7. `person_observer_ready` from the harness (bundle reports it). Prefer YAML cannot set it true.

Do **not** load the mini-game archive, dual-grid Prefer seats, or other sections unless this row is the place/dual seat.

## Emit

Write/update `{slice_id}.armed.yaml` (and Prefer brief if used) with:

| Field | Rule |
|-------|------|
| `ticket_map_id` | Exact row id |
| `proof_shape` / `claim_class` | **From map `observe`:** `person` → moment / ask_success; `record` → contract / component. Do not blur |
| `prefer_class` | `foundation` for contract substrate rows; `place` / `craft` only when the row is that seat **and** you set `topology_law: true` |
| `structural_success` | This row’s **product_job verbatim**. Narrowing sibling words is wrong here — copy the job. |
| `out_of_scope_ticket_ids` | **Exact** list from the bundle (Gate A fails if missing or mismatched) |
| `behavior_keys` | **Contract:** ≥1 invariant/operation key; **zero** visibility keys. **Moment:** 3–5 stranger-watchable keys. |
| `behavior_key_checks` | Attach a probe **only** when that probe’s runner is harness-owned for `observe` (person = Trinity opens a window and injects the click). Catalog `argv` does **not** qualify. Otherwise `{}` |
| `missing_observer` | **Required** when checks are empty — name the missing harness observer (e.g. `person_window_pointer`). |
| `status` | `incomplete_missing_observer` when checks empty + missing observer named. Do **not** set factory `armed_*` |
| `success_object` | Capability / visible board act for this row only |
| `do_not_waive` | Full product-map set |
| `checklist_ids` | Prefer-declared only. Contract default = `[]`. `None` on a map eat fails closed |
| `welds` / `W1`… | Only if the row’s **Welds** column explicitly lists them |
| `topology_law` | `true` **only** when this Prefer truly rewrites topology |

Do **not** set `factory_greenlit: true`. Do **not** FactoryEat. Do **not** set `map_fidelity_hostile_ok` or nested hostile. Do **not** invent probes so Gate A can pass.

## After draft

1. Gate A: `prefer_map_fidelity_check.py --armed …`
   - `status: forms_ok` → continue
   - `status: incomplete_missing_observer` → stop (exit ≠ 0; not launchable; do **not** call B₁)
   - `status: forms_fail` → fix forms from the bundle
2. Gate B₁: **only** when Gate A `status` is `forms_ok`:
   `PYTHONPATH=scripts python3 -m eat_queue_core.harness prefer_senior_gate --gate b1 --factory-order --armed …`
   Trinity stamps `source`. Chat `VALIDATE` / `prefer-map-fidelity-validate` is **not** B₁.
3. Operator GREENLIGHT only after stored B₁ `ok: true` → weld → B₂ → **F5 for moment**; contract closes on probe pass

B₁ terminal (stand-in / print / argv) → archive the packet. Do not re-author from the violation strings. Incomplete → wait for the named observer on `main`.

## Observe (binding)

Copy the row. Set `proof_shape`/`claim_class` from map `observe`. `structural_success` = product job **verbatim**. Attach a probe only when its runner class matches `observe` **and** the harness owns that observer (`person_observer_ready` for person). Otherwise leave `behavior_key_checks` empty, set `missing_observer`, `status: incomplete_missing_observer`. Do **not** shop the catalog for Gate A. Do **not** set hostile ok bits.
