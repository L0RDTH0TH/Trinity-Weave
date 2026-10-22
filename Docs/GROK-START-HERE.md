---
title: Grok — start here (Trinity-Weave)
created: 2026-06-09
updated: 2026-10-21
audience: grok_github_integration
---

# Grok — start here

**Repo:** [L0RDTH0TH/Trinity-Weave](https://github.com/L0RDTH0TH/Trinity-Weave)

**Capability:** Grok **cannot** be given the private Second-Brain vault. Trinity-Weave is the public surface so Grok **can** navigate published project material.

**Layout:** **`main`** = Trinity (**the system** — mint law + pack walk queue + **config anti-hardcode harness**). **`project/<project_id>`** = **the project being served** (PMG + full `Roadmap/` + **`Factory-DRB/bindings/`**). Mint uses both.

**Config anti-hardcode (2026-10-21):** Product nouns (engine, lanes, probes, host-law refuses, `game_repo_path`) live in **project** `Factory-DRB/bindings/*.yaml`. Harness on **`main`** only has fail-closed resolve + engine-neutral proof ops + host-law evaluator + denylist + Pass-4 eat-path fixture. Do **not** expect Genesis/Godot constants in harness Python. See [Docs/BINDINGS-CONFIG-ANTI-HARDCODE.md](Docs/BINDINGS-CONFIG-ANTI-HARDCODE.md).

**Pass 6 Prefer-align (not GREENLIGHT):** `main` `e60fdff` — `prefer_align.py` + `tests/test_prefer_align_eat.py`. Tip B Genesis Prefer/identity scrub on `project/genesis-mythos-master` (not GREENLIGHT).

**Pass 7 evidence law (not GREENLIGHT):** discover write-target entries into Prefer-align; eat Success = `evaluate_behavior_evidence` only (agent pack rejected). Re-run B₁ before GREENLIGHT.

**Pass 5 Tip A (single-seat check — not GREENLIGHT):** `main` `c25a447`. See `Docs/HALF-B-CONTRACT.md` + `tests/test_implementation_single_seat.py`.

**Pass 4 tip (refuse-demo only — not a functional feedstock→Genesis line):** code tip `main` `7b39fc9` · routing tip `main` `0dab4f0` · `project/genesis-mythos-master` `c5732fa`. Audit via BINDINGS doc Surfaces table + `tests/test_blank_project_contract_eat.py` + Pass-4 tokens in `tests/test_harness_product_denylist.py`. No GREENLIGHT.

**Two-pass mint:** **Pass A** = lock `walk_tier: series` only, then Trinity-publish series (**one series noun per turn**). **Pass B** = after `children_greenlit`, validate the **active same-width child batch** via `CHILD-BATCH-STATUS` + `BATCH-DIGEST.md` → one receipt (`_shared/CHILD-BATCH-VALIDATION.md`). Full `WALK.md` only for flagged ids. **World ≠ campaign** — world is the durable container; campaigns (and casts) nest inside it.

**Project navigation (mint):** bone pilot names **`project_id`** → open **`main` pack** `Docs/catalog-mint/<project_id>/` (walk queue) **and** branch **`project/<project_id>`** (PMG + full `Roadmap/` grounding). Both surfaces. Not “main only.”

**Not a mint corpus:** `/home/workdir/artifacts/` sandbox. Load from GitHub **Trinity-Weave**.

**Custom instructions (paste into Grok Chat):** [Docs/Grok-Second-Brain-Custom-Instructions.md](https://github.com/L0RDTH0TH/Trinity-Weave/blob/main/Docs/Grok-Second-Brain-Custom-Instructions.md)

---

## STOP — “mint the catalog” / product deliverables

**Only when the bone pilot explicitly instructs mint and names `project_id`.** Otherwise talk normally — do not open a mint session or emit a YAML receipt. Do not guess `project_id` from branches or ACTIVE.md.

When instructed:

1. Use the **named** `project_id` from the mint cue.
2. Open **`weave/component-proposals/catalog_mint.yaml`** (Trinity card — process / touch / rules).
3. Open pack **`Docs/catalog-mint/<project_id>/`** — `MINT-PACK.md` Walk Order, backlog gates (`mint_phase`, Trinity refs, `children_greenlit`), conceptual, pins, index, stack excerpts. Poll the index; request fulfill by `tert_id` for missing bodies.
4. **Series incomplete / no `series_published_trinity_ref`:** one pending **series** receipt per turn.
5. **Children greenlit:** open `CHILD-BATCH-STATUS` + active `BATCH-DIGEST.md`; return **one** batch receipt (`CHILD-BATCH-VALIDATION.md`); do not invent the list; ask republish if pack stale.
6. Preflight every draft; await `approve` / `edit` / `reject`.

Ignore archived `gmm-catalog-mint` if old links surface it.

---

## What this repo is (weave law)

Trinity-Weave is the public design manual + code slice for an agentic Second Brain maintenance layer (YAML cards, harness, host-weld) **and** the published per-project mint packs.

Bone pilot / Cursor must **publish** pack updates here for Grok to see them. Stale pack = ask for republish.

## Read order — weave law only (not mint)

1. `OBSERVABILITY.json`
2. `Docs/ARCHITECTURE-OVERVIEW.md`
3. `weave/CARD-INDEX.md` — **card** catalog, not product mint
4. `Docs/GLOSSARY-FOR-EXTERNAL-READERS.md`

## Question routing

| Question | Where |
|----------|--------|
| Mint / walk for a named project | **`main` (system):** catalog_mint + pack walk queue · **`project/<id>` (served):** PMG + Roadmap grounding |
| Project engine / lanes / probes / host-law | **`project/<id>`:** `Factory-DRB/bindings/` (`identity`, `engine`, `lanes`, `proof-catalog`, `host-law`, `legacy-refuse`) |
| Harness resolve / denylist / proof ops | **`main`:** `scripts/eat_queue_core/weave/factory/bindings.py`, `proof_runner.py`, `host_law.py`, `tests/test_harness_product_denylist.py` |
| Prefer-align gate | **`main`:** `weave/factory/prefer_align.py` · `tests/test_prefer_align_eat.py` · live eat blocks before agent |
| Half B contract / single-seat check | **`main`:** `Docs/HALF-B-CONTRACT.md` · `tests/test_implementation_single_seat.py` · `lane_factories.dispatch_slice_lanes` · `implementation_handoff.py` · `review_seats.run_integration_pass` |
| Pass 4 eat-path fail-closed audit | **`main`:** `Docs/BINDINGS-CONFIG-ANTI-HARDCODE.md` · `prefer_authorship_contract.py` · `operator_feedback.py` · `closed_alpha_passes.py` · `engine_preflight.py` · `implementation_handoff.py` · `lane_agent_registry.py` · `tests/test_blank_project_contract_eat.py` · denylist `PASS4_TOKENS` · **`project/genesis-mythos-master`:** bindings (`host-law` empty, `required_playtest_ids: []`, `build_command: ''`) |
| Weave cards / host-weld / harness | `weave/components/`, `weave/component-proposals/` |
| Gate B₂ weld intent (Prefer vs LIVE) | `Docs/Gate-B2-Weld-Intent-Hostile.md` + `Docs/Skills/prefer-weld-intent-validate/` · project Prefer law on `project/<id>` |
| Live queue / Watcher / vault notes | Unavailable — ask for paste or fulfill |

## Hard limits

- **Cannot** access private vault / Watcher / `1-Projects/…`
- Never confuse **card catalog** (`CARD-INDEX`) with **product slice-catalog** (`Docs/catalog-mint/<id>/slice-catalog.yaml`)
- Pasteable custom instructions: [Docs/Grok-Second-Brain-Custom-Instructions.md](https://github.com/L0RDTH0TH/Trinity-Weave/blob/main/Docs/Grok-Second-Brain-Custom-Instructions.md)

## Key paths

| Path | Contents |
|------|----------|
| `weave/component-proposals/catalog_mint.yaml` | **Mint instruction law** |
| `Docs/catalog-mint/<project_id>/` | **That project’s published pack** (navigate here when `project_id` is named) |
| `Docs/GROK-PROJECT-BRIDGE.md` | Bridge notes |
| `Docs/Grok-Second-Brain-Custom-Instructions.md` | **Paste into Grok Chat → Custom instructions** |
| `meat-suit-entry/` | Bone pilot hub |
| `weave/components/*.yaml` | Locked cards |
| `scripts/eat_queue_core/harness.py` | CLI (operator/Cursor — pack emit / receipt validate) |
| `scripts/eat_queue_core/weave/factory/bindings.py` | Fail-closed project bindings resolve (no silent product defaults) |
| `Factory-DRB/bindings/` on `project/<id>` | Project-owned identity / engine / lanes / proof-catalog / host-law |
| `Docs/BINDINGS-CONFIG-ANTI-HARDCODE.md` | Anti-hardcode law + Pass 1–4 publish tips (Pass 4 = refuse-demo, not functional line) |
| `scripts/eat_queue_core/tests/test_blank_project_contract_eat.py` | Pass 4 blank-project contract eat (bind + handoff + empty build preflight) |
| `Docs/HALF-B-CONTRACT.md` | Pass 5 Half B what→check contract (no method inputs) |
| `scripts/eat_queue_core/tests/test_implementation_single_seat.py` | Pass 5 single-seat + keys-from-packet + empty-build integration |
| `Docs/Gate-B2-Weld-Intent-Hostile.md` | **Gate B₂** rubric + three Grok guards + validator shape |
| `Docs/Skills/prefer-weld-intent-validate/` | Published B₂ hostile skill |
| `scripts/prefer_weld_intent_check.py` | B₂ CLI / receipt latch |
| `weave/host-weld/pilots/` | Chat latch / factory default (trialing) |
