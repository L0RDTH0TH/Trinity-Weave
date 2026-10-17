---
name: prefer-weld-intent-validate
description: >-
  Hostile weld-intent validation (Gate B₂) — Prefer Success painting brief vs
  LIVE Play-path behavior after GREENLIGHT weld. Use for VALIDATE prefer_weld_intent
  or before any Success / ready-for-F5 / KEEP when LIVE weld is claimed.
  Separate from Gate B₁ prefer_map_fidelity (map_fidelity_hostile_ok).
  Does not rewrite Prefer Success. Does not replace operator F5.
---

# Prefer weld intent validate (Gate B₂ — hostile)

## When

- Queue / Task: `VALIDATE` with `params.validation_type: prefer_weld_intent`
- **After** Gate B₁ (`map_fidelity_hostile_ok`) → GREENLIGHT → weld LIVE
- Before staging Success / ready-for-F5 / KEEP / ask_success when `live_weld_landed` or `factory_greenlit` is claimed
- Chat/hotfix receipts that claim greenlit or LIVE success without factory B₂

**Smoke path:** after B₁ → weld → B₂ (this skill) → operator F5. PLACE-product stays awaiting B₁ until redesign lands — do not GREENLIGHT WELD PLACE-product solely to exercise this skill.

## Pipeline (fields separate)

| Gate | Field | Role |
|------|-------|------|
| A | mechanical MAP | `prefer_map_fidelity_check` |
| B₁ | Prefer hostile | `map_fidelity_hostile_ok` via `prefer_map_fidelity` |
| GREENLIGHT → weld | LIVE | operator word |
| **B₂** | **Weld intent hostile** | **`weld_intent_hostile_ok`** (this skill) |
| F5 | Operator feel | KEEP latch |

## Inputs

1. Prefer Success + refuses (Prefer brief / armed packet) — **read-only**; do **not** rewrite
2. LIVE change set / files touched under Code-Repos
3. Evidence pack from harness `build_evidence_pack` (behavior checklist)
4. Optional MCP/Godot probes — **evidence only**, never sole pass (`verify_mcp_only` refuse)
5. Gate B₁ already green when Prefer-applicable

```bash
PYTHONPATH=scripts python3 scripts/prefer_weld_intent_check.py \
  --armed 1-Projects/genesis-mythos-master/Factory-DRB/slice-briefs/<slice>.armed.yaml \
  --evidence-json /tmp/weld-intent-evidence.json
```

## Rubric (fail closed)

**Picture question:** If Prefer is the painting brief, are LIVE mechanics brush strokes for that picture — or another picture sharing labels?

Pass only if **all** are true:

1. Play-path / behavior matches Prefer Success (e.g. place: same-seat ghost≡commit; update-four + coast still run; Full survives neighbor rebuild; Prefer refuses not violated in LIVE).
2. Pass basis is **behavior**, not AST / Prefer-word→method-name string match (string-match = **fail**).
3. Not “compiles” / Gate A again.
4. Proof tags / factory logs / KEEP headers — **indictment only**; they **cannot** pass. Piggyback fixture with `piggyback_place_v1` Success / KEEP header = **fail**.
5. MCP/Godot optional; `verify_mcp_only` = refuse.
6. You do **not** rewrite Prefer Success to fit what shipped (Guard 3). Prefer-lie → operator call, not validator rewrite.
7. **Stamp alone never passes.** `weld_intent_hostile_ok: true` / nested `{ok: true}` without a valid `weld_intent_evidence` behavior pack = **fail**.
8. **Place-class required keys.** For place / PLACE-product / dual_place markers, every place behavior key must be **present and true** (missing `update_four_ran` = fail). Unknown Prefer class = fail-closed.
9. **Bypass** only when `factory_bypass: true` **and** non-empty `factory_bypass_ack` / `operator_bypass_ack` / `operator_ack`. Bypass + `factory_greenlit: true` = fail.

## Grok guards (binding)

1. **Logs cannot acquit.**
2. **Latch sees skipped-factory welds** — Success / ready-for-F5 / KEEP / greenlit without B₂ stamp **and** behavior evidence = hard fail. Bypass only `factory_bypass: true` + ack quote; bypass must never say greenlit.
3. **B₂ does not edit the picture.**

## Output

Write/update `{slice_id}.prefer-result.json` fields (**additive** — do not clear or rewrite Prefer Success):

```json
{
  "weld_intent_hostile_ok": true,
  "weld_intent_hostile": {
    "ok": true,
    "verdict": "pass|fail",
    "summary": "one sentence",
    "pass_basis": "behavior",
    "map_fidelity_hostile_ok": true
  },
  "weld_intent_evidence": {
    "prefer_class": "place",
    "pass_basis": "behavior",
    "behavior": {
      "same_seat_ghost_eq_commit": true,
      "update_four_ran": true,
      "coast_gate_ran": true,
      "full_survives_neighbor_rebuild": true,
      "prefer_refuses_not_violated_in_live": true
    },
    "tags_are_not_pass_evidence": true
  }
}
```

On fail: `weld_intent_hostile_ok: false` and list behavior gaps. Leave Prefer Success text unchanged.

## Not your job

- Rewriting Prefer Success / refuses to match shipped LIVE
- Operator F5 of feel
- Gate B₁ Prefer-vs-MAP (use prefer-map-fidelity-validate)
- Treating proof tags as pass
- GREENLIGHT WELD of PLACE-product unless operator explicitly orders it
