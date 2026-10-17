# Product factory operator path (trialing)

**`factory_greenlit: true`** (operator 2026-10-01). Operator home: [[Half-B-Alpha-Mode]].

## Normative greenlit sequence

1. Pick catalog work **or** update/extend the **current** Code-Repos version.
2. Enforce `engine_stock_first` / FPS PRECONDITIONS for touched concerns.
3. Advance **PDF → adventure packet** when cartridge is in scope (structured pack; IP honesty).
4. MCP necessary checks per [[MCP-Playtest-WalkLook]]; operator F5 for walk+look.
5. Keep **`factory_greenlit: true`** (operator); do **not** revive archived investor demo as live Success. Do **not** claim ask_success from staging alone. Load [[FEEDSTOCK-SHAPE]] before shaped Half-B claims. Do not auto-dispatch — wait for launch word `WELD`.

## Conductor path (greenlit — still word-gated)

1. `./scripts/run-product-factory-session.sh`
2. `PYTHONPATH=scripts python3 -m scripts.eat_queue_core.harness headless_eat --lane <lane> --force`
3. Optional overnight: `headless_overnight --lane <lane>`

Integration proofs: `scripts/eat_queue_core/tests/test_product_factory_operator_path.py`

## Feedstock shape lock (operator check)

Before accepting Half-B staging as “shaped”: confirm [[FEEDSTOCK-SHAPE]] is loaded (`operator_confirmed: true`) and focus feedstock/L5 seasoning (and visual bar when visual) landed in the output. Miss → `inspiration_shape_miss`. See `FEEDSTOCK-SHAPE.md` · `INSPIRATION-HALF-B-SHAPE.md`.

## Ask fidelity

Same endpoint as the ask (`ask_fidelity` / `fidelity_match_ask`). Staging = foundation; `ask_success` = house (`done_when`). Demo ≠ spine; chargen ≠ dropdown. Reject `fidelity_miss`. See [[Half-B-Alpha-Mode]] · `Ask-Fidelity-Exemplars`.


## Chat default factory (binding — 2026-10-16)

**DEFAULT for chat** that touches Prefer / factory / LIVE Code-Repos: run the factory path (Prefer → Gate A/B → greenlight → weld). Do not silently hotfix LIVE or skip Prefer.

Before a chat hotfix / direct LIVE skip of Prefer:

1. **STOP** and **ASK** the operator explicitly whether to skip the factory.
2. Bypass **only** on explicit yes.
3. Receipt: `factory_bypass: true` + non-empty `factory_bypass_ack` / `operator_bypass_ack` / `operator_ack` quote (flag alone does not skip B₂).
4. **Never** stamp `factory_greenlit: true` on bypass — greenlit is factory-path only.

Hostile Prefer (Gate B) is required on every Prefer Success claim (staging and KEEP). Operator F5 = feel / intended behavior, not mechanical Prefer shape. See [[Prefer-Authorship-Host-Law]] §C.3 + Chat default factory · [[Prefer-Map-Fidelity-Automation-Plan]].
