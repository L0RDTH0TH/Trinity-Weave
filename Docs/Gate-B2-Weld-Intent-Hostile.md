---
title: Gate B₂ — Weld intent hostile (Grok public brief)
created: 2026-10-16
updated: 2026-10-16
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
2. **Latch sees skipped-factory welds.** Staging Success / ready-for-F5 / KEEP / greenlit without `weld_intent_hostile_ok` when LIVE claimed = hard fail (including chat receipts). Bypass only `factory_bypass: true` + operator ack quote; bypass must **never** say `factory_greenlit: true`.
3. **B₂ does not edit the picture.** Prefer-lie is an operator call — validator must **not** rewrite Prefer Success to fit what shipped.

## Rubric (fail closed)

**Picture question:** If Prefer is the painting brief, are LIVE mechanics brush strokes for that picture — or another picture sharing labels?

Pass only if **all** are true:

1. Play-path / behavior matches Prefer Success (behavior evidence, not AST).
2. Pass basis is **behavior**, not Prefer-word→method-name string match (string-match = **fail**).
3. Not “compiles” / Gate A again.
4. Proof tags / factory logs / KEEP headers — indictment only; they **cannot** pass.
5. MCP/Godot optional; `verify_mcp_only` = refuse.
6. Do **not** rewrite Prefer Success (Guard 3).

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

## Chat default factory

DEFAULT for chat that touches Prefer / factory / LIVE: Prefer → A → B₁ → greenlight → weld → **B₂** → F5. Before skipping factory: STOP and ASK; only on explicit yes; receipt `factory_bypass: true` + ack; never greenlit on bypass.
