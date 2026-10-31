---
title: Prefer Map Fidelity + Weld Intent Automation Plan
created: 2026-10-15
updated: 2026-10-16
project-id: genesis-mythos-master
status: active
automation_landed: 2026-10-15
hostile_every_success: 2026-10-16
weld_intent_b2_landed: 2026-10-16
para-type: Resource
aliases:
  - Prefer-Map-Fidelity-Automation-Plan
---

# Prefer Map Fidelity + Weld Intent Automation Plan

Operator does **not** review Prefer prose. Feedstock → Prefer compose → **gates** → greenlight weld → **weld-intent hostile** → F5 product.

**Binding:** Hostile Prefer (**Gate B₁**) fires on **every** Prefer/factory Success claim (staging **and** KEEP) **before** GREENLIGHT. After weld LIVE, **Gate B₂** (weld intent hostile) fires before ready-for-F5 / KEEP. Mechanical-shape Success must **never** green to the operator. Operator F5 validates intended behavior/feel — not Prefer shape and not log tags.

## Layers

| Gate | Kind | Role | Field |
|------|------|------|-------|
| **A — Mechanical** | Harness (`prefer_map_fidelity.py`) | `ticket_map_id` → MAP row; proofs in `structural_success`; `success_object` deny-list; product-map `do_not_waive`. Fail → Prefer / authorship pass fails. | (mechanical) |
| **B₁ — Hostile Prefer** | Validator `prefer_map_fidelity` | LLM rubric: Success ≡ MAP job+proofs **or** Prefer structural intent; Play-path visible; refuse thin rewrite / `intent_collapsed_to_mechanics`. **Required before any Success claim** (staging or KEEP) pre-GREENLIGHT. | `map_fidelity_hostile_ok` |
| **C — Pre-GREENLIGHT** | Factory / Layer 0 | No weld GREENLIGHT / Success receipt unless **A** (when map Prefer) **and B₁** are green. Staging does **not** land LIVE on A alone. | — |
| **B₂ — Weld intent hostile** | Validator `prefer_weld_intent` + `prefer_weld_intent.py` | Prefer Success = painting brief; LIVE = brush strokes for **that** picture? Behavior / Play-path only. Logs/tags **indict only**. String-match Prefer→methods = fail. `verify_mcp_only` refuse. **Does not rewrite Prefer Success.** Required when LIVE weld / greenlit / post-weld Success claimed. | `weld_intent_hostile_ok` |
| **D — KEEP latch** | Prefer result + map pointer | `claim_class: ask_success` / KEEP only if A (when applicable) + B₁ + **B₂** (when welded) + operator F5. | both + F5 |

## Pipeline (target)

Prefer draft → Gate A (optional map) → Gate B₁ Prefer hostile (`map_fidelity_hostile_ok`) → GREENLIGHT → weld LIVE → **Gate B₂ weld intent hostile (`weld_intent_hostile_ok`)** → operator F5 (feel/KEEP). Fields separate.

## B₂ Grok guards (binding)

1. **Logs cannot acquit.** Proof tags / factory logs / KEEP headers may indict only — never pass. Piggyback fixture with `piggyback_place_v1` Success / KEEP header → B₂ **fail**.
2. **Latch sees skipped-factory welds.** Staging Success / ready-for-F5 / KEEP / greenlit without B₂ stamp **and** valid behavior evidence when LIVE claimed = hard fail (including chat receipts). Bare `weld_intent_hostile_ok: true` without evidence fails; place missing required behavior keys fails; bypass only `factory_bypass` + non-empty ack quote; bypass must **never** say greenlit.
3. **B₂ does not edit the picture.** B₁ green, weld, B₂ red → rework weld. Prefer-lie is operator call.

**Closed 2026-10-17:** stamp-alone, partial place behavior, bypass-without-ack — see [[Gate-B2-Weld-Intent-Hostile]].

## Not in scope

- Replacing operator F5 of the **product** (feel / intended behavior).
- Porting Azgaar JS.
- Auto-KEEP.
- Treating Gate A mechanical-shape or proof tags as operator Success.
- GREENLIGHT WELD of PLACE-product until B₁ redesign lands (`map_fidelity_hostile_ok`); PLACE stays unwelded / `factory_greenlit: false`. GEN-biomes stays unarmed.

## Deliverables

### B₁ (landed 2026-10-15 / every-Success 2026-10-16)

1. `scripts/eat_queue_core/weave/factory/prefer_map_fidelity.py` + `tests/test_prefer_map_fidelity.py`
2. Wired into `run_prefer_authorship_pass` when map Prefer **or** Prefer-applicable product slice
3. CLI `scripts/prefer_map_fidelity_check.py`
4. Validator `prefer_map_fidelity` in Second-Brain-Config + skill `prefer-map-fidelity-validate`
5. Host-Law C.3 harness cite

### B₂ (landed 2026-10-16)

1. `scripts/eat_queue_core/weave/factory/prefer_weld_intent.py` + `tests/test_prefer_weld_intent.py`
2. Latch + chat/hotfix receipt scanner + evidence pack builder (tags = indictment-only)
3. CLI `scripts/prefer_weld_intent_check.py`
4. Validator `prefer_weld_intent` in Second-Brain-Config + skill `prefer-weld-intent-validate`
5. Host-Law C.3 B₂ + chat-default factory + host-weld pilots

**Smoke path:** after B₁ → weld → B₂ (documented; do not stall PLACE-product on B₁ redesign).

## Operator loop (semi-auto)

1. Point at MAP row / next ticket — agent drafts Prefer from MAP proofs (or Prefer-product seat).
2. Gate A runs in authorship pass / CLI when map Prefer — you do not read Prefer.
3. **Required before any Success claim (staging or KEEP) pre-GREENLIGHT:** `VALIDATE` `prefer_map_fidelity` (Gate B₁).
4. You greenlight weld only when A (if applicable) + B₁ green; weld LIVE.
5. **Required after weld before ready-for-F5 / KEEP:** `VALIDATE` `prefer_weld_intent` (Gate B₂) → `weld_intent_hostile_ok`.
6. KEEP / pointer only after A + B₁ + B₂ + your F5.

## Chat default factory (cross-link)

Chat defaults to the factory path (A → B₁ → greenlight → weld → B₂ → F5). Before a chat hotfix / direct LIVE skip of Prefer: **STOP and ASK** explicitly to skip factory; only on explicit yes; receipt `factory_bypass: true` + ack quote; never stamp `factory_greenlit: true` on bypass. See Prefer-Authorship-Host-Law § Chat default factory + host-weld pilots.

## Cross-links

- Active map socket: `factory-project.yaml` → `ticket_map_runtime.map_note` / `map_id` (harness `resolve_active_ticket_map_rel`) — currently [[World-Builder-Session-Prep-Ticket-Map]]
- Retired mini-game map (archive only): `4-Archives/Projects/genesis-mythos-master/world-builder-mini-game-ticket-map-retired-20261019T203200Z`
- [[Ticket-Map-Schema]] (vault-wide map shape; picker `scripts/factory_weld_launch_clip.py`)
- [[Prefer-Authorship-Host-Law]] §C.3
- Skills: prefer-map-fidelity-validate · prefer-weld-intent-validate
