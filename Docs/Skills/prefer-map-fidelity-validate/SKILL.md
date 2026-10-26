---
name: prefer-map-fidelity-validate
description: >-
  Hostile Prefer validation (Gate B₁) — MAP job+proofs vs armed Prefer packet.
  Prefer must bind this row and must not consume a sibling open row's job.
  Use for VALIDATE prefer_map_fidelity or before any Prefer Success claim
  (staging or KEEP) on Prefer-applicable product slices.
  Does not replace Gate B₂ weld intent (prefer_weld_intent) or operator F5.
---

# Prefer map fidelity validate (Gate B₁ — hostile Prefer)

## When

- Queue / Task: `VALIDATE` with `params.validation_type: prefer_map_fidelity`
- After Ticketment draft (`prefer-ticketment-draft`) and Gate A green
- Before **any** Prefer `claim_class` Success altitude on Prefer-applicable product slices
- Mechanical Gate A alone must **never** green Success to the operator

## Inputs

1. **Ticketment bundle** for `ticket_map_id` (same load as Ticketment — section neighbors out of scope)
2. **Active ticket MAP** — `factory-project.yaml` → `ticket_map_runtime` (no hardcoded product map filename)
3. Armed packet: `{slice_id}.armed.yaml`
4. Prefer brief + `prefer-result.json` if present
5. Gate A CLI (must already be green when Gate A applies):

```bash
PYTHONPATH=scripts python3 scripts/prefer_map_fidelity_check.py \
  --armed 1-Projects/genesis-mythos-master/Factory-DRB/slice-briefs/<slice>.armed.yaml
```

If Gate A exits non-zero → verdict **fail** (do not soft-pass).

## Rubric (fail closed)

Pass only if **all** are true:

1. **Own row bind.** `structural_success` matches **this** MAP product job (necessary). Narrowing after sibling words are removed is **correct**. You may remove sibling jobs; you may **not** replace this row’s act with a lookup/shell while keeping the act’s words. If the row says point/see/stay, Prefer is that act on a tiny board.
2. **No sibling swallow.** Prefer success / `behavior_keys` must not overlap any other **open** map row’s job more than they overlap this row. If they describe a different open ticket → **fail** (`job_consumes_sibling`). This is the regression that matters.
3. `out_of_scope_ticket_ids` present and equal to same-section open neighbors from the map (Gate A already checks; B₁ re-checks intent).
4. `success_object`: **Contract / foundation** — names this row’s invariant capability (operation + identity result); success text must **not** say point / see / GM / board. **Moment** — object is the **visible act** on a tiny board (point/see/stay). “Demo” means sibling system / LaunchShell — **not** the board act. Do not frame moment `success_object` as “not a demo” in a way that deletes the board act. Refuse `contract_bound` / `meta_written` / `hotkey_bound`. Do not fatten a contract Prefer into a Play-path LaunchShell; do not slim a moment into an index/shell lookup.
5. Required `do_not_waive` includes product-map codes plus session-prep codes on `world-builder-session-prep`.
6. `behavior_keys`: **Contract / foundation** — ≥1 invariant/operation key, zero visibility. **Moment** — 3–5 stranger-watchable keys from **this** row. Do not fatten a contract Prefer to 3–8 to satisfy an old habit. Reject `file_exists`, `compiles`, `menu_opens`, and the two generic B₂ booleans alone. Gate A allowlist: play-path words in Prefer text **or** the map-row product job → every `behavior_key_check` op must be costume-free `point_hits_solid` (`map_fidelity:play_path_success_requires_point_hits_solid`). Empty / unresolved / missing probe = fail. `entrypoint_result_equals` (even with `selector.point`) fails. Do **not** stamp `map_fidelity_hostile_ok: true` when Gate A is red.
7. Inspiration altitude (Azgaar / Townscaper / FG / etc.) **only** when the Prefer cites that exemplar.
8. Partial hit → **staging incomplete**, never KEEP. Staging without hostile → **fail**.
9. Do **not** treat project `factory_greenlit: true` as Prefer Success.

## Operator F5 (not this skill)

**Moment** Prefers: operator F5 validates intended behavior/feel — no stamp without the visible act. **Contract** Prefers: do **not** ask F5; probe pass closes. Do not treat Gate A green as F5.

## Output

Write/update `{slice_id}.prefer-result.json` fields:

```json
{
  "map_fidelity_hostile_ok": true,
  "map_fidelity_hostile": {
    "ok": true,
    "verdict": "pass|fail",
    "summary": "one sentence",
    "checked_ticket_map_id": "WB-polygon-substrate",
    "gate_a_ok": true,
    "sibling_consume_ok": true
  }
}
```

On fail: `map_fidelity_hostile_ok: false` and name which sibling job was swallowed.

## Not your job

- Welding LIVE code
- Gate B₂ (`prefer-weld-intent-validate`)
- Operator F5
- Quietly rewriting Prefer Success to fit LIVE — send sibling hits back to Ticketment
- Stamping `factory_greenlit: true` on bypass
