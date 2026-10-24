---
title: Gate B₂ — Weld intent hostile (Grok public brief)
created: 2026-10-16
updated: 2026-10-17
audience: grok_github_integration
---

# Gate B₂ — Weld intent hostile

Public Trinity-Weave brief so Grok can validate **Gate B₂** without the private vault. Project law lives on `project/genesis-mythos-master`; harness + this rubric live on `main`.

## Pipeline (fields separate — B₁ ≠ B₂)

| Gate | Field | Role |
|------|-------|------|
| A | mechanical MAP | `prefer_map_fidelity_check` |
| **B₁** | Prefer hostile | `map_fidelity_hostile_ok` via `prefer_map_fidelity` |
| GREENLIGHT → weld | LIVE | operator word |
| **B₂** | **Weld intent hostile** | **`weld_intent_hostile_ok`** (this gate) |
| F5 | Operator feel | KEEP latch |

Prefer draft → Gate A → Gate B₁ → GREENLIGHT → weld LIVE → **Gate B₂** → operator F5.

**PLACE-product** stays awaiting B₁ (`map_fidelity_hostile_ok`), unwelded, `factory_greenlit: false` until redesign — do **not** GREENLIGHT / weld PLACE-product solely to exercise B₂.

## Validator (vault Config is private — publishable shape)

```yaml
validator:
  prefer_weld_intent:
    model: auto
    skill: prefer-weld-intent-validate
```

Queue / Task: `VALIDATE` with `params.validation_type: prefer_weld_intent`.

## Grok guards (binding)

1. **Logs cannot acquit.** Proof tags / factory logs / KEEP headers may **indict only** — never pass. Piggyback fixture with `piggyback_place_v1` Success / KEEP header → B₂ **fail**.
2. **Latch sees skipped-factory welds.** Staging Success / ready-for-F5 / KEEP / greenlit without B₂ stamp **and** valid behavior evidence when LIVE claimed = hard fail (including chat receipts). Bypass only `factory_bypass: true` **and** non-empty `factory_bypass_ack` / `operator_bypass_ack` / `operator_ack`; bypass must **never** say `factory_greenlit: true`.
3. **B₂ does not edit the picture.** Prefer-lie is an operator call — validator must **not** rewrite Prefer Success to fit what shipped.

## Closed stops (2026-10-17 — Grok re-validate)

| Hole | Close |
|------|--------|
| Hand-stamped `weld_intent_hostile_ok: true` with no evidence pack | **Fail** — `weld_intent:missing_evidence_pack` / `stamp_alone_not_evidence` |
| Partial place `behavior` omitting keys (e.g. no `update_four_ran`) | **Fail** — `weld_intent:behavior_key_missing:*` (missing ≠ pass) |
| `factory_bypass: true` without ack quote | **Fail** — `weld_intent:bypass_missing_operator_ack` (no B₂ skip) |
| Bypass + `factory_greenlit: true` | **Fail** — `weld_intent:bypass_must_not_claim_greenlit` |
| Unknown Prefer class | **Fail-closed** — `weld_intent:unknown_prefer_class_fail_closed` |

## Rubric (fail closed)

**Picture question:** If Prefer is the painting brief, are LIVE mechanics brush strokes for that picture — or another picture sharing labels?

**Contract Prefers:** Prefer names `behavior_key_checks` (one probe per key). Harness runs `entrypoint_result_equals` (operation + compared value). Agent return-dict, agent stamp files, and exit-code-alone are **not** evidence. Feedstock is not re-read at B₂.

Pass only if **all** are true:

1. Play-path / behavior matches Prefer Success (behavior evidence, not AST).
2. Pass basis is **behavior**, not Prefer-word→method-name string match (string-match = **fail**).
3. Not “compiles” / Gate A again.
4. Proof tags / factory logs / KEEP headers — indictment only; they **cannot** pass.
5. MCP/Godot optional; `verify_mcp_only` = refuse.
6. Do **not** rewrite Prefer Success (Guard 3).
7. Stamp field alone never passes — require `weld_intent_evidence` with `pass_basis: behavior` and class-required keys all **present and true**.
8. Place / PLACE-product / dual_place: require full place checklist (`same_seat_ghost_eq_commit`, `update_four_ran`, `coast_gate_ran`, `full_survives_neighbor_rebuild`, `prefer_refuses_not_violated_in_live`).

## Harness (on `main`)

| Artifact | Path |
|----------|------|
| Module | `scripts/eat_queue_core/weave/factory/prefer_weld_intent.py` |
| Tests | `scripts/eat_queue_core/tests/test_prefer_weld_intent.py` |
| CLI | `scripts/prefer_weld_intent_check.py` |
| Wiring | `prefer_authorship_contract.py` · `lane_agent_registry.py` |
| Skill (published copy) | `Docs/Skills/prefer-weld-intent-validate/SKILL.md` |
| Host-weld chat latch | `weave/host-weld/pilots/product_factory_pipeline.md` · `implementation_factory_loop.md` |

```bash
PYTHONPATH=scripts python3 scripts/prefer_weld_intent_check.py \
  --armed Factory-DRB/slice-briefs/<slice>.armed.yaml \
  --evidence-json /tmp/weld-intent-evidence.json
# Chat / Success receipt latch:
PYTHONPATH=scripts python3 scripts/prefer_weld_intent_check.py --receipt /path/to/receipt.json
```

Stamp field: `weld_intent_hostile_ok: true` (additive on `{slice}.prefer-result.json` — never clear Prefer Success).

## Project law (on `project/genesis-mythos-master`)

- `Factory-DRB/Prefer-Authorship-Host-Law.md` — B₁ vs B₂ table + chat latch
- `Factory-DRB/Prefer-Map-Fidelity-Automation-Plan.md` — automation plan + three guards
- `Factory-DRB/World-Builder-Mini-Game-Ticket-Map.md` — ticket map
- `Factory-DRB/slice-briefs/alpha0_stalberg_dual_place_product_r1.prefer-result.json` — PLACE-product still awaiting B₁ (`weld_intent_hostile_ok: false`)

## Wiring (harness)

| Path | B₂ seat |
|------|---------|
| `run_prefer_authorship_pass` | `validate_weld_intent_latch` (+ embedded `chat_hotfix_receipt` / `hotfix_receipt` via `scan_chat_hotfix_receipt`) |
| `keep_latch_allowed` | B₁ + B₂ when LIVE/greenlit + operator F5 |
| `post_weld_keep_latch` | B₁ + B₂ + F5 |
| CLI `--receipt` | `scan_chat_hotfix_receipt` |
| `review_pass_runner` → `prefer_authorship_pass` | inherits authorship latch |

## Chat default factory

DEFAULT for chat that touches Prefer / factory / LIVE: Prefer → A → B₁ → greenlight → weld → **B₂** → F5. Before skipping factory: STOP and ASK; only on explicit yes; receipt `factory_bypass: true` + ack quote field; never greenlit on bypass.

## Residual gap (honest)

Free-form chat Success that never touches armed yaml, prefer-result, `prefer_authorship_pass`, KEEP latch, or `prefer_weld_intent_check --receipt` is still outside the harness. Host-law / pilots require agents to run the latch or CLI on those claims; the mechanical seat cannot intercept arbitrary chat text that was never written to a receipt field.
