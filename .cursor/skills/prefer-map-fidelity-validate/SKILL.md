---
name: prefer-map-fidelity-validate
description: >-
  Hostile Prefer validation (Gate B₁) — MAP job+proofs vs armed Prefer packet.
  Use for VALIDATE prefer_map_fidelity or before any Prefer Success claim
  (staging or KEEP) on Prefer-applicable product slices (WORLD/GEN/PLACE/craft/stalberg).
  Does not replace Gate B₂ weld intent (prefer_weld_intent) or operator F5.
---

# Prefer map fidelity validate (Gate B₁ — hostile Prefer)

## When

- Queue / Task: `VALIDATE` with `params.validation_type: prefer_map_fidelity`
- Before **any** Prefer `claim_class` Success altitude (`staging`, `staging_awaiting_f5`, `ask_success` / KEEP) on Prefer-applicable product slices — WORLD / GEN / VIS / LOOP / PACK / PLACE / craft / stalberg (align `slice_requires_prefer_authorship`)
- Mechanical Gate A alone must **never** green Success to the operator

## Inputs

1. Ticket MAP (when `ticket_map_id` / map Prefer): `1-Projects/genesis-mythos-master/Factory-DRB/World-Builder-Mini-Game-Ticket-Map.md` row for `ticket_map_id`
2. Armed packet: `{slice_id}.armed.yaml`
3. Prefer brief + `prefer-result.json` if present
4. Gate A CLI (must already be green when Gate A applies):

```bash
PYTHONPATH=scripts python3 scripts/prefer_map_fidelity_check.py \
  --armed 1-Projects/genesis-mythos-master/Factory-DRB/slice-briefs/<slice>.armed.yaml
```

If Gate A exits non-zero → verdict **fail** (do not soft-pass). Prefer-product slices without `ticket_map_id` may be Gate-B-only; still fail closed if hostile is missing.

## Rubric (fail closed)

Pass only if **all** are true:

1. `structural_success` is the MAP **product job + weld proofs** (when mapped), not a thinner rewrite that keeps the ticket name. Prefer-product PLACE/craft: structural Success matches Prefer intent, not mechanical-shape alone.
2. `success_object` names a **player-visible** Play-path outcome (LaunchShell / WorldgenCraft). Refuse `contract_bound` / `meta_written` / `hotkey_bound`.
3. A stranger one-liner of Success matches the MAP job / Prefer intent on the Play path. Metas / HUD / taught hotkeys do not count.
4. Required `do_not_waive` includes (when map Prefer): `hotkey_as_product_ux`, `config_meta_without_effect`, `stub_as_hours`, `map_job_name_only`, `explicit_met_implicit_miss`, `intent_collapsed_to_mechanics`.
5. Refuse wording-minimal / `intent_collapsed_to_mechanics` — Gate B blocks before greenlight.
6. Azgaar is **altitude** (options → control → readable map), not a JS/WebView port Success (GEN rows).
7. Partial hit → **staging incomplete**, never KEEP. Staging without hostile → **fail** (not warning).

## Operator F5 (not this skill)

Operator F5 validates **intended behavior/feel**, not mechanical Prefer shape. Do not treat Gate A green as F5.

## Output

Write/update `{slice_id}.prefer-result.json` fields:

```json
{
  "map_fidelity_hostile_ok": true,
  "map_fidelity_hostile": {
    "ok": true,
    "verdict": "pass|fail",
    "summary": "one sentence",
    "checked_ticket_map_id": "GEN-terrain-product",
    "gate_a_ok": true
  }
}
```

On fail: `map_fidelity_hostile_ok: false` and list which proofs were collapsed.

## Not your job

- Welding LIVE code
- Gate B₂ weld intent after LIVE weld (`prefer-weld-intent-validate` / `weld_intent_hostile_ok`)
- Operator F5 of the running game
- Advancing `next_world_pointer` without operator F5
- Stamping `factory_greenlit: true` on chat factory-bypass receipts
