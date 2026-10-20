---
name: prefer-map-fidelity-validate
description: >-
  Hostile Prefer validation (Gate B₁) — MAP job+proofs vs armed Prefer packet.
  Use for VALIDATE prefer_map_fidelity or before any Prefer Success claim
  (staging or KEEP) on Prefer-applicable product slices.
  Does not replace Gate B₂ weld intent (prefer_weld_intent) or operator F5.
---

# Prefer map fidelity validate (Gate B₁ — hostile Prefer)

## When

- Queue / Task: `VALIDATE` with `params.validation_type: prefer_map_fidelity`
- Before **any** Prefer `claim_class` Success altitude (`staging`, `staging_awaiting_f5`, `ask_success` / KEEP) on Prefer-applicable product slices
- Mechanical Gate A alone must **never** green Success to the operator

## Inputs

1. **Active ticket MAP** — resolve from `1-Projects/<project-id>/Factory-DRB/factory-project.yaml` → `ticket_map_runtime.map_note` / `map_id`, else discovery of the project’s sole `ticket_map: true` + `map_status: active` note. Do **not** hardcode a product map filename. Row for `ticket_map_id` on that map.
2. Armed packet: `{slice_id}.armed.yaml` (must set `ticket_map_id` for map Prefers)
3. Prefer brief + `prefer-result.json` if present
4. Gate A CLI (must already be green when Gate A applies):

```bash
PYTHONPATH=scripts python3 scripts/prefer_map_fidelity_check.py \
  --armed 1-Projects/genesis-mythos-master/Factory-DRB/slice-briefs/<slice>.armed.yaml
```

If Gate A exits non-zero → verdict **fail** (do not soft-pass). Prefer-product slices without `ticket_map_id` may be Gate-B-only; still fail closed if hostile is missing.

## Rubric (fail closed)

Pass only if **all** are true:

1. `structural_success` is the MAP **product job + weld proofs** (when mapped), not a thinner rewrite that keeps the ticket name.
2. `success_object` names a **player-visible** Play-path outcome on the project’s LIVE entry (from `factory-project.yaml` → `game_repo_path` + Prefer `live_write_target` / Play scene). Refuse `contract_bound` / `meta_written` / `hotkey_bound`. Do not require WorldgenCraft unless that is the Prefer’s Play path.
3. A stranger one-liner of Success matches the MAP job / Prefer intent on that Play path. Metas / HUD / taught hotkeys do not count.
4. Required `do_not_waive` includes (when map Prefer): `hotkey_as_product_ux`, `config_meta_without_effect`, `stub_as_hours`, `map_job_name_only`, `explicit_met_implicit_miss`, `intent_collapsed_to_mechanics` — plus any map-local codes the Prefer arms.
5. Refuse wording-minimal / `intent_collapsed_to_mechanics` — Gate B blocks before greenlight.
6. Inspiration altitude (Azgaar / Townscaper / FG / etc.) is **only** when the Prefer cites that exemplar — not a default for every ticket.
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
    "checked_ticket_map_id": "WB-polygon-substrate",
    "gate_a_ok": true
  }
}
```

On fail: `map_fidelity_hostile_ok: false` and list which proofs were collapsed.

## Not your job

- Welding LIVE code
- Gate B₂ weld intent after LIVE weld (`prefer-weld-intent-validate` / `weld_intent_hostile_ok`)
- Operator F5 of the running game
- Advancing map recovery pointers without operator F5
- Stamping `factory_greenlit: true` on chat factory-bypass receipts
