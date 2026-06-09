---
title: Maintenance Trinity Constitution
created: 2026-06-02
tags: [second-brain, weave, maintenance, trinity]
para-type: Resource
status: active
---

# Maintenance Trinity constitution (Phases 5–13)

**Status (2026-06-06):** Phases **5–8** dual-lock and vault compensation **shipped**. **9+10 PASS** achieved **2026-06-05** (`121/121` green). **Phase 13 host weld cutover** complete (bridge, archive `20260606T055949Z`, `host_weld_sync`, `live/safety.md` aligned). **Enter service** — maintenance downshifts to inspect-and-repair; see § Weave operational model in integration plan.

**Operator runbooks:** [[3-Resources/Second-Brain/Docs/Maintenance-Trinity-Phase4-Runbook|Phase 4 runbook]] · [[3-Resources/Second-Brain/Docs/Host-Weld-Cutover-Runbook|Host weld cutover]]

## Maintenance corps charter

> **Maintenance maintains non–maintenance-core Trinity cards and their operational legs; it advises on maintenance-core gaps.**

**Non–maintenance-core** means every Trinity card and code leg outside the frozen **maintenance core (A)** registry block — provisionals, `conceptual_spine` cards, bridge tunnels (**D** via **B**), and other mutable weave sections. Maintenance does **not** fill missing cards or promote provisionals to core; it **aligns what is mutable** and **surfaces how to fix what is frozen**.

| Layer | Maintenance maintains | Maintenance advises only |
|-------|----------------------|---------------------------|
| **A — maintenance core** (18 ids) | Read, align, gate (`integrity_ok`) | Disconnects → `provisional-core-recommendations.jsonl`; backlog rank |
| **B — locked bridges** | Catch-up PQ scope; doctrine on **D** stubs | Bridge consolidation (operator trigger) |
| **C / mutable cards** | Auto-curate `stale_touch`; touch+align; spine guards | — |
| **Missing cards / orphans** | — | `assess_trinity_card_backlog`, `MAINTENANCE_NOTE`, `trinity_card_generate` / `ghost_skill_audit` stubs (no lock, no promote) |

**Operator** owns maintenance-core Conceptual and YAML (`--operator-mutation` only). **System** never applies gap fixes to core.

Launch loop: `trinity_catchup_sweep` → optional PQ (`TRINITY_SPINE_CATCHUP`, `MAINTENANCE_NOTE`) → `EAT-QUEUE` maintenance lane → `lane_status_board`.

## Separation of responsibility

| Actor | Scope |
|-------|--------|
| **Operator** | **Maintenance core** — all legs; optional **conceptual spine lock** on non-core cards |
| **Maintenance corps** | Non-core operational legs (Touch/Rules/Contract), provisionals, bridge tunnels |
| **System on core** | Align + gate; **no** touch refresh / promote / cascade writes unless `--operator-mutation`. Gate may **hash-only** re-sync after metrics append (closure churn). |

Registry: `.technical/weave/trinity-partition-registry.yaml` → `maintenance_core:` block.

## Lock kinds

| `lock_kind` | System may mutate | Production `trinity_pack` |
|-------------|-------------------|-------------------------|
| `maintenance_core` | **No** (operator harness only) | Yes when card exists in `components/` |
| `usage_proven` | **No** (hash reconcile only; operator unfreeze) | Yes when card exists in `components/` |
| `conceptual_spine` | Touch/Rules/Contract only | Yes |
| `full` (default operator lock) | No | Yes |

## Harness

```bash
# Operator edits core Touch hash
PYTHONPATH=scripts python3 -m scripts.eat_queue_core.harness trinity_touch_refresh \
  --vault-root . --trinity-id lane_status_board --operator-mutation

# Lock provisional → components/
PYTHONPATH=scripts python3 -m scripts.eat_queue_core.harness trinity_lock_card \
  --vault-root . --trinity-id my_card --lock-kind conceptual_spine
```

## Phase 6 — outward curation

- **`respects_locked_spine`** — non-core cards must not overlap core `primary_paths` or list core in `pairs_with` / `tunnel_via`; enforced on `write_trinity_card` and align meta persist.
- **`resolve_consumable_trinity_id`** — production `trinity_pack` / PQ `params.trinity_id` only for consumable ids; provisionals land in `trinity_id_advisory`.
- **Catch-up** — `curate_stale_non_core` auto touch+align for **stale_touch only** on non-core; core disconnects → `.technical/weave/provisional-core-recommendations.jsonl` (never auto-fix).
- **Bridge stub** — `build_provisional_bridge_stub()` + template `.technical/weave/templates/trinity-provisional-bridge.yaml`.

```bash
PYTHONPATH=scripts python3 -m scripts.eat_queue_core.harness trinity_catchup_sweep --vault-root . --no-queue
# Disable auto-curation: --no-curate
```

## Code

- `scripts/eat_queue_core/weave/trinity_dual_lock.py` — `assert_system_may_mutate`, helpers
- `scripts/eat_queue_core/weave/trinity_spine_guard.py` — `respects_locked_spine`, provisional core recommendations
- All writes go through `write_trinity_card` (guard enforced)

## Phase 7 — bridge lifecycle + backlog

- **`trinity_bridge_consolidate`** — operator merges ≥2 provisional bridges with same `tunnel_via` → one locked bridge + registry row.
- **`assess_trinity_card_backlog`** — ranks maintenance cards by **drift × usage**; board **Backlog** table under Trinity spine; optional `params.trinity_backlog_top` on maintenance PQ lines.
- **Pseudo-clock:** `trinity_backlog_on_pseudo_clock` (with or without catch-up sweep).

```bash
PYTHONPATH=scripts python3 -m scripts.eat_queue_core.harness trinity_bridge_consolidate \
  --vault-root . --tunnel-via lane_status_board --dry-run
PYTHONPATH=scripts python3 -m scripts.eat_queue_core.harness assess_trinity_card_backlog --vault-root .
```

Config: `trinity_backlog_top_n`, `trinity_backlog_on_pseudo_clock`, `trinity_backlog_usage_weight`.

## Phase 8 — vault compensation (A/B/C/D bridge model)

When code shipped dual-lock behavior (Phases 5–7) before the corpus matched, **Phase 8** aligns vault YAML with the constitution:

| Card | Role | Location |
|------|------|----------|
| **A** | Frozen maintenance core | `.technical/weave/components/` (18 ids) |
| **B** | Locked bridge (cartilage) | `trinity_spine_maintenance`, `trinity_upgrade_integration` |
| **C** | Corps / provisional targets | `.technical/weave/component-proposals/` |
| **D** | New provisional bridge for harness changes | proposals with `touch.tunnel_via` → **B**, never **A** |

**Stamp rules:** `meta.lock_kind: maintenance_core`, `meta.system_mutable: false`. Doctrine in `rules.precedence`; add `rules.forbidden` short line only when `test_*` guard count > existing forbidden count (avoids `precedence_collapse`).

```bash
PYTHONPATH=scripts python3 -m scripts.eat_queue_core.harness trinity_phase8_vault_compensation --vault-root .
PYTHONPATH=scripts python3 -m scripts.eat_queue_core.harness trinity_stamp_core_cards --vault-root .
PYTHONPATH=scripts python3 -m scripts.eat_queue_core.harness trinity_touch_refresh \
  --vault-root . --maintenance-set --operator-mutation
```

Code: `scripts/eat_queue_core/weave/trinity_vault_compensation.py`. D stubs deployed: `catchup_corpus_tunnel` → `trinity_spine_maintenance`; `upgrade_compensator_tunnel` → `trinity_upgrade_integration`.

## Phase 9 — weave spine enforcement (self-wrap)

**Program north star:** Launch the **core loose** so the system **wraps itself in its inner workings**. Self-wrap integrates maintenance into the **Trinity spine**, **aligns the legs**, and **proves the code through tests** — not YAML-only touch refresh.

**Charter:** Maintenance aligns the Trinity spine, clears weave clogs, runs **corps evidence** (Phase 10), and **enforces in weave only after conduct is evidenced** — so a written card becomes the live center of the weave around it.

### Canonical cycle (lens-first — 2026-06-06)

Order is **normative**; maps to § Enforcement ladder.

| Step | Harness block | Ladder rung |
|------|---------------|-------------|
| 0 | `load_mvl_bundle` | Meta perception |
| 1 | `align_spine` (lens-informed) | **2 — Spine aligned** |
| 2 | `mvl_lens` gate | Meta wiring verify |
| 3 | `meta_corpus_charter` | Charter advisory (bulk promote off) |
| 4 | `host_weld_sync` (full corpus only) | Host law surgical sync |
| 5 | `unclog` | **2** (plumbing) |
| 6 | `regenerate_complete` (optional) | Scorched earth — operator only |
| 7 | `corps_sweep` + repair loop | **3–4** |
| 8 | `enforce_in_weave` | **5 — Enforce** (only if `conduct_ok`) |
| 9 | `observe` | **6 — Observe** |

```bash
PYTHONPATH=scripts python3 -m scripts.eat_queue_core.harness trinity_weave_self_wrap \
  --vault-root . --full-corpus
```

**Trust gate:** When corps `conduct_ok` is false, `enforce_in_weave` is skipped (`provisional_enforcement_untrusted`) — enforcement without evidence is invalid.

**Disconnect classes:** `spine_drift`, `spine_violation_weave`, **`clog`**, `gap` (advisory).

Artifacts: `.technical/weave/spine-enforcement-graph.yaml`, `trinity-weave-self-wrap-*.json` under `.technical/weave/validation/`. Code: `trinity_weave_self_wrap.py`, `trinity_lens_informed_align.py`.

Config: `trinity_weave_self_wrap_enabled`, `trinity_mvl_conductor_enabled`, `trinity_lens_informed_align_enabled`, `trinity_host_weld_sync_enabled`, `trinity_clog_pass_before_board`.

---

## Enforcement ladder (modus operandi)

Maintenance earns the right to **enforce in code** only after **conceptual alignment is evidenced**. Order is strict; **no step may be skipped or faked**.

| Rung | Phase / tier | Question | Evidence |
|------|--------------|----------|----------|
| **1 — Core stabilized** | **8** | Is maintenance **A** frozen? | `lock_kind: maintenance_core`, dual-lock |
| **2 — Spine aligned** | **9** align + unclog | Entry points, graph, plumbing? | Spine graph; clog clear |
| **3 — Legs ↔ Conceptual** | **10 T0 + T1** | Touch/Rules describe role? | `shape_ok`, `semantic_ok` |
| **4 — Intent-conduct** | **10 T2 + 10d** | Weave **behaves** as intent? | **`conduct_ok`** — real unittest green |
| **5 — Enforce in weave** | **9 enforce** | Symbolic probes pass **after** conduct? | Enforce downstream of T2 |
| **6 — Observe** | **9 board** | Gauges consistent? | Board last — detector, not primary gate |

**Modus operandi (locked):**

- **Conceptual is the spec.** T2 tests are the acceptance suite.
- **Not sufficient for T2:** import-only smoke, empty `test_*`, touch-hash churn with failing proofs.
- **Sufficient for T2:** Proofs encoding **primary_case** outcomes; **10d** repair when red.

**9+10 PASS (enter service):** `trinity_weave_self_wrap` with **`pass_gate_ok: true`** on **full corpus** including **intent-conduct** — achieved **2026-06-05** (`trinity-weave-self-wrap-20260605T194633Z.json`, 121/121).

**Exit codes (harness self-wrap):**

| Code | Meaning |
|------|---------|
| **0** | `pass_gate_ok` green |
| **2** | Cycle OK; corpus not green (acceptance audit) |
| **1** | Infrastructure failure (align, regen, compensation) |

Read stderr `=== trinity_weave_self_wrap ===` and JSON **`operator_outcome`** (`cycle_ok`, `pass_gate_ok`, `next_steps`).

---

## Phase 10 — Provisional corps (nervous system) — **shipped**

**Charter:** Operator maintains **core A**. **Maintenance corps** maintains the rest — every provisional and bridge **D** stub. Phase 10 **sweeps** YAML into spine-safe shape, **nerve-tests** each card, and runs a **repair loop** until `pass_gate` or bounded stop.

### Three-tier poke (T0 → T1 → T2)

| Tier | What | Pass gate field |
|------|------|-----------------|
| **T0** | Shape / spine hygiene | `shape_ok`, `spine_ok` |
| **T1** | Semantic / legs vs Conceptual (optional **10c** LLM) | `semantic_ok` |
| **T2** | **Intent-conduct** — real behavior proofs | **`conduct_ok`** |

**Nerve map:** `.technical/weave/corps-nerve-map.json` each run.

### pass_gate booleans

| Field | Meaning |
|-------|---------|
| `shape_ok` | YAML/spine hygiene |
| `spine_ok` | `respects_locked_spine`, align legs |
| `semantic_ok` | Legs match Conceptual (T1) |
| **`conduct_ok`** | Intent-conduct proofs green (T2) — **required for 9+10 PASS** |

Default **strict conduct** (`trinity_corps_conduct_pending_ok: false`) — import-only smoke is **not** green.

### Repair stack (10d → 10f → 10g)

| Module | Role |
|--------|------|
| **10d** `corps_conduct_repair.py` | Card YAML + signal prune from Conceptual |
| **10f** `corps_test_code_repair.py` | Test-code surgery after card repair |
| **10g** `corps_conduct_repair_pack.py` | Proof stderr pack + 11b Pull slice before `manual_required` |
| **10g apply** `corps_conduct_repair_apply.py` | Bounded auto patch (default **off**) |

Packs: `.technical/weave/conduct-repair-packs/<trinity_id>-<ts>.md`. Audit: `corps-repair-audit.jsonl`.

### Operator commands

```bash
# Acceptance audit (no burn)
PYTHONPATH=scripts python3 -m scripts.eat_queue_core.harness trinity_weave_self_wrap \
  --vault-root . --full-corpus

# Cluster dev
PYTHONPATH=scripts python3 -m scripts.eat_queue_core.harness trinity_provisional_corps_sweep \
  --vault-root . --cluster architect_* --full-corpus

# Scorched earth (destructive — Trinity cards only, not host weld; operator-initiated only)
PYTHONPATH=scripts python3 -m scripts.eat_queue_core.harness trinity_weave_self_wrap \
  --vault-root . --full-corpus --regenerate-complete
```

See [[3-Resources/Second-Brain/Docs/Regenerate-Complete-Doctrine|Regenerate-Complete-Doctrine]] — **never** automated; no surgery loop on roadmap.

```bash
# Phase 14 — scoped delta (new factory / segment)
PYTHONPATH=scripts python3 -m scripts.eat_queue_core.harness trinity_expand_self \
  --vault-root . --scope-ids my_new_factory
```

**Hard stops:** no writes to `components/` maintenance_core without `--operator-mutation`; no auto-lock/promote.

Config: `trinity_corps_sweep_enabled`, `trinity_corps_sweep_before_enforce`, `trinity_corps_auto_repair_enabled`, `trinity_corps_llm_repair_enabled` (default **false**), `trinity_corps_conduct_repair_pack_enabled`, `trinity_corps_conduct_repair_auto_apply_enabled` (default **false**).

---

## Phase 11b — MVL conductor (`trinity_prompt_context`)

**Locked meta** — bidirectional **Pull** (given `trinity_id` → prompt slice) and **Route** (given user prompt → id, `task_kind`, lane). Loaded **before** `align_spine` via `load_mvl_bundle`.

- Code: `trinity_mvl_lens.py`, `trinity_prompt_context_slice.py`, `trinity_lens_informed_align.py`
- Meta prepend includes: `maintenance_honesty_anchor`, `host_execution_safety_contract`, style, authoring, lifecycle, …
- **Route indexes** dispatcher/funnels — does not replace `.cursor/rules` routing; host law is separate (§ Phase 13).

**Meta corpus charter:** `trinity_meta_corpus_enabled: false` by default — bulk promote deferred until service downshift.

---

## Phase 13 — Cursor host weld

**Problem:** Legacy `.cursor/rules/**` sprawl contradicted locked meta and bridge. **Solution:** Immutable **bridge socket** → **archive** legacy out of production → **`host_weld_sync`** surgically fills `host-weld/live/` from **meta + archive reference**.

### Two welds (do not conflate)

| Weld | Source of truth | Who writes |
|------|-----------------|------------|
| **Trinity segment** | `components/` + provisionals | Harness / operator-mutation |
| **Cursor host** | `cursor_host_adapter` meta + `host-weld/live/` | Maintenance via `host_weld_sync`; **never** `.cursor/rules/` |

### Precedence (on conflict)

Locked Trinity meta → **host-weld live/trialing** → bridge socket → chat. **Archive is reference only** — not loaded by Cursor.

### Socket + manifest (this vault)

| Path | Role |
|------|------|
| `.cursor/rules/always/host-weld-bridge.mdc` | Always-on Read of manifest + active `live/` |
| `.technical/weave/host-weld/manifest.yaml` | Slug registry, `legacy_archive_root`, `socket_retained` |
| `.technical/weave/host-weld/live/*.md` | Promoted host law (maintenance may write surgically) |
| `4-Archives/.../Second-Brain-Host-Weld-Legacy/<stamp>/` | Mint reference only |

**First slug shipped:** `safety` ← locked **`host_execution_safety_contract`** meta.

```bash
PYTHONPATH=scripts python3 -m scripts.eat_queue_core.harness trinity_host_weld_sync --vault-root .
```

**Full operator procedure:** [[3-Resources/Second-Brain/Docs/Host-Weld-Cutover-Runbook|Host-Weld-Cutover-Runbook]]

Config: `trinity_host_weld_sync_enabled` (default true when MVL on).

---

## Phase 16 — Knob parity proofs (service era)

**Rule:** Any change under a profile dimension must be evaluated on **every enumerated option** unless operator documents intentional asymmetry.

**Canonical enums** (Config-Profiles): `speed_mode` fast|balance|extreme; `repair_strategy` repair_first|forward_first; `validator_tier` forgiving|aggressive.

**Resolver (Python):** `scripts/eat_queue_core/config_resolve_profile.py` — familial parse, default bundle, profile expansion, merge order.

**Matrix harness:** `trinity_knob_parity` — factory × single-knob sweep cells; artifact `.technical/weave/validation/knob-parity-matrix.json`.

| Factory | Proof focus |
|---------|-------------|
| `queue_dispatch` | `pipeline_mode`, `roadmap_pass_order`, validator tier |
| `roadmap_resume` | Same as queue dispatch |
| `corps_sweep` | Expansion resolves for all speed/tier options |
| `weave_self_wrap` | Extreme nested validator passes |
| `gitforge_tail` | Fast → GitForge skip (`speed`) |

```bash
PYTHONPATH=scripts python3 -m scripts.eat_queue_core.harness trinity_knob_parity --vault-root .
```

Wired on **`trinity_weave_self_wrap --full-corpus`** as `knob_parity` step (advisory; fails cycle when red cells). Config: `trinity_knob_parity_enabled`.

**Advisory:** Locked `config_knob_parity` meta `touch.knob_families` may drift from Config-Profiles — matrix reports `meta_knob_drift`; fix via `--operator-mutation` on meta touch when ready.

---

## Phase 14 — expand_self (delta wrap)

**Additive onboarding** for new factories/segments after **9+10 PASS** — scoped align + corps only; **no** full-corpus burn, **no** `--regenerate-complete`.

| | `expand_self` | `--regenerate-complete` |
|--|---------------|-------------------------|
| **Intent** | Weld new provisionals onto track | Yard-wide scorched earth |
| **Scope** | `--scope-ids` or `--corps-cluster` | All eligible unlocked cards |
| **Initiation** | Operator or PQ (future) | **Operator CLI only** — never automated |
| **Regen** | **Forbidden** combined | Explicit `--regenerate-complete` |

```bash
PYTHONPATH=scripts python3 -m scripts.eat_queue_core.harness trinity_expand_self \
  --vault-root . --scope-ids my_new_factory,peer_card
```

Code: `trinity_expand_self.py`, harness `trinity_expand_self` / `trinity_weave_self_wrap --expand-self`. Config: `trinity_expand_self_enabled`.

**Doctrine:** [[3-Resources/Second-Brain/Docs/Regenerate-Complete-Doctrine|Regenerate-Complete-Doctrine]] — scorched earth is operator-initiated; no automated surgery loop planned.

Runbook: [[3-Resources/Second-Brain/Docs/Expand-Self-Runbook|Expand-Self-Runbook]]

---

## Weave operational model (enter service)

After **9+10 PASS**, maintenance **re-roles**: same drivetrain (harness, pack, spine guards, MVL lenses), different consist — factory Runs lead; maintenance does scheduled MOW (`expand_self`, `redesign_factory`, `usage_proven`). See integration plan § Weave operational model.

**Honesty anchor** (`maintenance_honesty_anchor` meta): claim tiers structural > inferred > narrative; distinct from **execution safety** (`host_execution_safety_contract`) which governs **mutation authorization** (backup, snapshot, bands, trash).

---

## Phase 9–10 legacy note (superseded sections)

The following were **draft/TBD** in earlier constitution revisions and are **superseded** by sections above:

- Old cycle order `align → enforce → unclog` — replaced by **lens-first** cycle table.
- Phase 10 "implementation TBD" — corps + pass_gate **shipped** 2026-06-04/05.
- Batch size 7 as default full corpus — self-wrap defaults to **full corpus** + repair loop.

Config: `trinity_corps_sweep_enabled`, `trinity_corps_sweep_before_enforce`, `trinity_corps_sweep_auto_hygiene`, `trinity_corps_nerve_test_enabled`, `trinity_corps_conduct_pending_ok` (default `false`), `trinity_corps_proof_adequacy_strict` (default `false`).

## Cross-links

- `.cursor/plans/maintenance_trinity_integration_2b0215e3.plan.md`
- [[3-Resources/Second-Brain/Docs/Maintenance-Trinity-Phase4-Runbook|Maintenance-Trinity-Phase4-Runbook]]
- [[3-Resources/Second-Brain/Docs/Host-Weld-Cutover-Runbook|Host-Weld-Cutover-Runbook]]
- [[3-Resources/Second-Brain/Docs/Maintenance-Trinity-Lock-Checklist|Maintenance-Trinity-Lock-Checklist]]
- [[3-Resources/Second-Brain/Docs/Component-Trinity|Component-Trinity]]
