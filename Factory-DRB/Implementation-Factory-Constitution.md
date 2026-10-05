---
title: Implementation-Factory-Constitution
project-id: godot-genesis-mythos-master
status: signed
constitution_signed: true
constitution_signed_at: "2026-06-10T18:00:00Z"
constitution_review_receipt: Ingest/Agent-Research/Raw/Stack-Vetting/b5-operator-constitution-review-2026-06-10.md
precedes: closed_alpha
requires_stack_baseline: true
requires_trinity: stack_baseline_honesty
closed_alpha_release_ref: Factory-DRB/Release-Definitions/closed-alpha-v1.md
pipeline_proof_receipt: Factory-DRB/Pipeline-Proof-Receipt.md
stack_baseline_receipt: Ingest/Agent-Research/Raw/Stack-Vetting/b5-operator-stack-baseline-review-2026-06-14.md
trinity_honesty_ref: Factory-DRB/Stack-Baseline-Honesty-Trinity-v1.md
---

# Implementation-Factory-Constitution

Governs **Closed Alpha** and beyond. **Effective** after Product 1 (vetted tech stack) and this sign-off.

**Pipeline proof alone does not unlock factory lanes.** **Trinity honesty is mandatory — never optional.**

**Closed Alpha build order** is defined only in [[Factory-DRB/Release-Definitions/closed-alpha-v1]] — not in the lane table below.

## Article I — Two foundations

1. **Tech stack (external BOM)** — full PMG domain manifest; fresh search; interop-gated; Path B vetted (`operator_stack_baseline_vetted: true`).
2. **Spine (internal sockets)** — C# interfaces; gameplay never binds vendor types directly.

## Article II — Factory lanes (six, post-Constitution)

**Lane ownership** — primary artifact when a lane activates. **Not** Closed Alpha build sequence.

| Lane | Factory | Primary artifact (lane charter) |
|------|---------|--------------------------------|
| Perspective | PerspectiveStack | Sparky / `ICameraRig` — **Slice 3** per closed-alpha-v1 |
| Regional | RegionalState | ModuleFactory — hydrate **after** core loop |
| Asset | AssetContent | ADC/TAC |
| Audio | AudioContent | AuDC |
| Rules | RulesEngine | rules plugins — **Slice 1** |
| Sim | SimTick | tick + bus — **Slice 1** |

Lanes serialize onto **one vertical slice at a time** per [[Factory-DRB/Release-Definitions/closed-alpha-v1]] (`core_loop` → `dm_command` → `sparky_feel`).

## Article III — Honesty, recovery & Trinity (mandatory)

Factory honesty is **not** optional narrative. Every Success claim on stack or factory output must satisfy:

1. **Factory-Honesty-Recovery-Doctrine-v1** — `little_val_ok`, anti-pattern checks, recovery ladder.
2. **Trinity `stack_baseline_honesty`** — `trinity_align --trinity-id stack_baseline_honesty` green before stack sign-off scope Success and before any manifest flip that asserts vetted state.
3. **Operator surface** — F6/headless smokes + receipts under `Ingest/Agent-Research/Raw/Stack-Vetting/` for external proof.

**Forbidden anti-patterns:** `skeleton_marked_operational`, `poc_assumed_locked`, `missing_interop_receipt`, `file_exists_integrate_theater`, **Trinity bypass**, **perspective_first_build** (camera before core loop).

Closed Alpha slices extend the Trinity **track & weld** model — slice cards as needed; honesty machinery is never waived for speed.

## Article IV — Release tiers

1. `pipeline_proof` — factory runs (complete)
2. `stack_baseline` — **vetted** — full Tech Stack operational (Path B complete 2026-06-14)
3. `closed_alpha` — gameplay on vetted stack — **[[Factory-DRB/Release-Definitions/closed-alpha-v1|closed-alpha-v1]]** (**provisional** — operator retract 2026-06-15; `factory_ship_valid: false`)
4. `open_beta` — **next tier** (TBD definition)

## Article V — Prefer authorship + proxy subordination (host law)

**Normative surface:** [[Factory-DRB/Prefer-Authorship-Host-Law|Prefer-Authorship-Host-Law]] · host-weld pilot `implementation_factory_loop`.

1. **Dispatch preflight** fail-closed before first lane agent (armed paths ⊆ zone union; identity drift; shell-era checklist under worldgen Prefer).
2. **Proxies subordinate** — `host_touch_budget` (diff lines only), bootstrap stubs, continues, and shell waives cannot alone pass Prefer product seats.
3. **`prefer_authorship_pass`** binds Hot Wheels craft ≠ Terrain3D car (YT Y19Mw5YsgjI) with durable negative examples every Prefer.
4. **Eat liveness** — L2 `escalate_review_seat` / hard_block exits `implementation_eat` (no zombie spin).

## Sign-off (complete)

Operator set `constitution_signed: true` when **all** of:

| Gate | Status |
|------|--------|
| `operator_stack_baseline_vetted: true` | ✓ 2026-06-14 |
| Path B tracker — all rows operational | ✓ |
| `trinity_align stack_baseline_honesty` | ✓ 2026-06-10 |
| This document reviewed | ✓ |

## Related

- [[Factory-DRB/Release-Definitions/closed-alpha-v1]]
- [[Factory-DRB/Stack-Research-Plan-v1]]
- [[Factory-DRB/Factory-Honesty-Recovery-Doctrine-v1]]
- [[Factory-DRB/Stack-Baseline-Honesty-Trinity-v1]]
- [[Factory-DRB/Trinity-Integration-Check-2026-06-13]]
- [[Horizon-Q3-Demo-Spec]]
- [[Ingest/Agent-Research/Raw/Stack-Vetting/b5-operator-constitution-review-2026-06-10]]
