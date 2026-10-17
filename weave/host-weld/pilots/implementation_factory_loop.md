---
title: Implementation factory loop (Track C pilot)
created: 2026-06-09
tags: [host-weld, pilot, implementation, track-c, second-brain]
status: trialing
trinity_refs:
  - engine_stock_authority
  - ask_fidelity
  - implementation_segment_charter
  - implementation_gate_catalog
  - implementation_handoff_tunnel
  - mcp_postedit_validator
  - cursor_engine_mcp_loop
  - stack_baseline_honesty
  - factory_output_conduct
source: horizon-q3_demo_plan
---

# Implementation factory loop (Track C)

**Status:** trialing — first pilot instance `godot-genesis-mythos-master` / Horizon-Q3 Demo v1.

## Outcome

Roadmap design (Tracks A+B) stays **readonly input**. Half B **generates and updates** LIVE Code-Repos (`genesis-mythos-alpha-20260930` or successor) with **maintenance receipts** for every MCP/engine edit cycle. **Require** filled [[Half-B-Weld-Brief-Template]] + [[FEEDSTOCK-SHAPE]] before shaped claims. Umbrella [[alpha_architecture_half_b]]; first slice [[alpha0_worldgen_dualgrid_sparky_r1]]. Investor demo **archived** — not Success. **`factory_greenlit: true`** (operator greenlight 2026-10-01). See [[Half-B-Alpha-Mode]].

## Factory rules (any project / lane)

| Rule | Requirement |
|------|-------------|
| Readonly inputs | `1-Projects/<project_id>/Roadmap/` + `Roadmap/Execution/` + instance spec |
| Write target | `5-Attachments/Code-Repos/<slug>/` |
| Effective track | `implementation` |
| MCP loop | Cursor → MCP → engine → mcp_postedit_validate receipt |
| Receipt sinks | `.technical/parallel/maintenance/mcp-implementation-receipts.jsonl` + lane mirror |
| Host law | `.technical/weave/host-weld/live/safety.md` |
| Forbidden | Autonomous edits under `.cursor/rules/**` |



## Update machine (generate + extend)

Half B is not greenfield-only:

| Mode | Target |
|------|--------|
| Generate | New catalog/capability welds into current exhibit |
| Update / extend | Fix, deepen, extend systems or cartridge on the **live** tree |

Same stock gates (`engine_stock_authority`, FPS/F5). Receipts for extend/fix are first-class. Do not invent a parallel throwaway repo to avoid updating current version.

**Cartridge:** PDF → adventure packet → `content/packs/<id>/` (schema: pack.json / beats / sites / pregens). Exemplar ingest: `Ingest/PZO9500-9E_WeBeGoblinsFree.pdf`. Placeholder `example_goblin_oneshot` = shape feedstock only. No Paizo prose dump.

**Greenlit:** `factory_greenlit: true` (operator 2026-10-01). Investor / `horizon_demo_investor` ask remains **archived** (do not revive) — see `4-Archives/Projects/genesis-mythos-master/horizon-demo-investor-ask-retired-20261001T072552Z/`. Greenlight is operator-owned; not via archived investor Success. Slice receipts stay `claim_class: staging` until eat/attest.


## Feedstock shape lock (required) + inspiration → output shape

**Required before shaped Half-B claims:** load operator lock `3-Resources/Second-Brain/Docs/catalog-mint/_shared/FEEDSTOCK-SHAPE.md` (`operator_confirmed: true`, `lock_id: feedstock_shape_v1`, `factory_greenlit: true`). Missing lock ⇒ do not claim properly shaped Half-B output.

**Generalized Half-B law** — not demo-only. Inspirations are **focus-scoped mandatory** per weld (not a fixed global list): resolve → cite → land, or `inspiration_shape_miss`. Seasoning = rest of INDEX when not in focus. Visual welds load [[Visual-Factory-Direction-Stylized-Low-Poly]].

| Requirement | Detail |
|-------------|--------|
| Lock | [[FEEDSTOCK-SHAPE]] confirmed — pointer package (matrix/gates/ask_fidelity; three cams; DF possible; investor archived) |
| Load | Focus feedstock INDEX/cards + L5/ASSUMPTION-LOG for the weld; visual lane also stylized low poly bar |
| Cite | Receipt names move-pin(s) / visual bar shaping the output |
| Fail | `inspiration_shape_miss` when flavor exists upstream but output is generic / unshaped |
| Demo catalog | Provisional horizon / investor rows **archived** — **not** live Success |

Normative: `FEEDSTOCK-SHAPE.md` · `INSPIRATION-HALF-B-SHAPE.md`.  
`claim_class: staging`. `factory_greenlit: true`.

## Ask fidelity (house ≠ foundation)

Trinity `ask_fidelity` — gate `fidelity_match_ask` (**block**). Reject: `fidelity_miss`.

Before implement/update Success:

1. Hand-off **must** carry `ask_id`, `done_when` (experience / house bar), `forbidden_substitutes`.
2. Receipt **must** set `claim_class`: `staging` (foundation OK) or `ask_success` (house met).
3. `ask_success` requires quoting `done_when` and **not** delivering a substitute.
4. Examples: character creation ↚ dropdown/OptionButton stub; do **not** optimize toward archived `horizon_demo_investor` as live Success.
5. Run structural check: `scripts/eat_queue_core/weave/ask_fidelity.py` (`evaluate_ask_fidelity`). Validator type `ask_fidelity` for hostile pass.

Stock/FPS/F5 remain **how** / feel attest — they do not prove the house.

## Half-B gates (factory_greenlit: true — operator; staging claim_class until slice attest)

### Pattern — `engine_stock_first` (block)

Before **any** Code-Repos write matching a [[Godot-Implementation-Decision-Matrix]] concern or Tech-Stack-Manifest `stack-*` row:

1. Load Trinity `engine_stock_authority`. **Copy the masters** — engine physics, Terrain3D, Pathfinder→calcs; do not invent parallel game systems.
2. **Funnel** = seat routing + context via Host Index — DM gets skill-check results they called; NPC relationship/history feeds DM RP context. Not “ban NPC systems.”
3. Name the stock authority id; **quote** matrix Prefer/Never or [[Junior-Tech-Adapt-How-To]] reject line. Missing quote / second authority / parallel notify channel = `engine_pattern_miss`.

### Specialized — player / camera / look / move

1. Resolve [[ENGINE-COMPILE-PACK-stock_godot_fps]] + matrix + [[Godot-Stock-Patterns]]; **quote** principle + Player move/look row.
2. Gate `godot_stock_fps` = **block** — stock `CharacterBody3D` + eye-child `Camera3D` + capture. Hosts select cameras; never own locomotion.
3. Walk+look Done = **operator F5 only** on `res://dev/FpsSanity.tscn` — `operator_kinesthetic_walk_look` = **block**.
4. Ban: “MCP verified walk+look.” Reject: `engine_pattern_miss` | `gui_input_steal` | `seat_ok_feel_fail` | `verify_mcp_only`.
5. Do **not** claim factory greenlit / Alpha Success from MCP, scene inspection, or checklist alone.

Trinity refs: `engine_stock_authority`, `implementation_gate_catalog`, `implementation_segment_charter`, `implementation_handoff_tunnel`.  
Pointers: [[Half-B-Alpha-Mode]] · [[MCP-Playtest-WalkLook]] · [[Tech-Stack-Manifest-v1]] · `Ingest/PZO9500-9E_WeBeGoblinsFree.pdf` · project `AGENTS.md`.


## Prefer authorship + proxy subordination (host law — 2026-10-01)

**Binding** for worldgen / Terrain3D-feed Prefer welds. Full law: `1-Projects/genesis-mythos-master/Factory-DRB/Prefer-Authorship-Host-Law.md` (Constitution Article V).

| Gate | Behavior |
|------|----------|
| Dispatch preflight | Fail-closed: armed paths ⊆ zone union; identity drift; shell-era checklist under worldgen Prefer |
| Proxy subordination | Diff-line `host_touch_budget` (advisory on Prefer); bootstrap stubs ≠ drop ready; continue dedupe; waives cannot silence product Prefer seats |
| `prefer_authorship_pass` | Durable Hot Wheels ≠ Terrain3D car (YT Y19Mw5YsgjI); auto-injected on matching slices; producer mission overlay |
| Eat liveness | L2 `escalate_review_seat` / hard_block → `implementation_eat` exits (`stop_eat`) |

Authorship maintenance = Prefer cannot close if layer-contract seats fail; **no proxy overrides product seats.**

## Stack baseline honesty (Path B)

Product 1 = vetted tech stack. Claims use honesty ladder in [[Factory-DRB/Stack-Baseline-Honesty-Trinity-v1]] — **`stack_baseline_honesty`** Trinity card must align green before manifest sign-off.

## Daily loop

Weave (goal-authority / PQ / this pilot) → Cursor Agent → MCP → Engine + Code-Repos → mcp_postedit_validate → maintenance receipts → prototype history.

## Instance block — Godot pilot

| Field | Value |
|-------|--------|
| project_id | godot-genesis-mythos-master |
| lane | godot |
| engine_adapter | godot_4_6_3_dotnet |
| Demo spec | 1-Projects/godot-genesis-mythos-master/Horizon-Q3-Demo-Spec.md |
| Repo path | 5-Attachments/Code-Repos/genesis-mythos-demo/ |
| MCP primary | ~/.local/bin/godot-mcp-primary.sh start |
| Cursor MCP | npx -y godot-mcp-server (tomyud 0.5.0) |
| Language | C# primary |

**Forbidden:** sandbox EAT-QUEUE resume; 6.2 rollup deepens; HANDOFF_AUDIT_REPAIR on godot PQ.

## Factory output conduct (Closed Alpha)

Product 2 slice Success is **factory output**, not weave corpus conduct alone. The **`factory_output_conduct`** Trinity card binds:

| Check | Proof |
|-------|--------|
| Graybox critical path | All slice smokes run `Main.tscn` (Q3 graybox) |
| Visual weld | `SparkyDmFreeCamRig` on Main — not legacy `DMCameraRig` stand-in |
| Narrative drift | `Core/` scan for deferral phrases (`Post-R1`, `until then`, `stack proof only`, …) |
| Config ladder | `factory_orchestrator.factory_output_trinity_gate` — **enforcement_mode: off\|warn\|block** |

**Staged rollout:** `warn` (default) → trace warnings on Layer 1 / harness without blocking grandfathered slices → `block` at ship sign-off.

**Harness:**

```bash
PYTHONPATH=scripts PYTHONPATH=scripts python3 -m eat_queue_core.weave.factory.cli --vault-root . factory-output-gate
```

**Grandfather:** Slices 1–4 marked `complete_pre_conduct` in goal-authority until re-proof under block mode.

**Related:** [[1-Projects/godot-genesis-mythos-master/Factory-DRB/Release-Definitions/closed-alpha-v1]] · `factory_output_conduct` card

## Vault roadmap feed (user story depth)

When `feed_authority: vault_roadmap`, factory jobs are shaped by the **user story depth pipeline** — not raw execution pins alone.

| Stage | Module / command | Output |
|-------|------------------|--------|
| L5 authoring | `scopes/<row_id>/L5.md` | Complete vision per catalog row |
| Depth slicer | `depth_slicer` / `harness depth_slice` | `L4.md` … `L1.md` factory food |
| Rollout budget | `rollout_slicer` / `SET_ROLLOUT_BUDGET` | `target_depth` per row |
| Dispatch | `work_order_translate` | `dispatch_depth = current_depth + 1`; `slice_id` uses dispatch depth |
| Weld receipt | `depth_bump` | bumps `current_depth` after lane success |

**Honesty:** `current_depth` is a weld receipt only. Do not dispatch full pins when a level scope file exists. Operator experiential + catalog sign gates block `vault_roadmap` staging (see `.cursor/plans/roadmap_factory_operator_loop.plan.md`).

**Weave card:** `user_story_depth_pipeline` (component-proposals).


## Chat default factory (binding — 2026-10-16)

**DEFAULT for chat** that touches Prefer / factory / LIVE Code-Repos: run the factory path (Prefer → Gate A → **B₁** Prefer hostile → greenlight → weld → **B₂** weld intent hostile → F5). Do not silently hotfix LIVE or skip Prefer.

Before a chat hotfix / direct LIVE skip of Prefer:

1. **STOP** and **ASK** the operator explicitly whether to skip the factory.
2. Bypass **only** on explicit yes.
3. Receipt: `factory_bypass: true` + non-empty `factory_bypass_ack` / `operator_bypass_ack` / `operator_ack` quote (flag alone does not skip B₂).
4. **Never** stamp `factory_greenlit: true` on bypass — greenlit is factory-path only.
5. Chat receipts claiming greenlit / LIVE Success without B₂ stamp **and** behavior evidence pack → hard fail (Gate B₂ latch). Bare stamp without evidence fails.

**Gate B₁** (`map_fidelity_hostile_ok` / `prefer_map_fidelity`) — required on every Prefer Success claim (staging and KEEP) **before** GREENLIGHT.
**Gate B₂** (`weld_intent_hostile_ok` / `prefer_weld_intent`) — after weld LIVE; Prefer Success painting brief vs LIVE Play-path behavior; logs/tags indict only; stamp alone never passes (need `weld_intent_evidence`); place missing required behavior keys fails; B₂ does not rewrite Prefer Success.
Operator F5 = feel / intended behavior, not Prefer shape or proof tags. See [[Prefer-Authorship-Host-Law]] §C.3 + Chat default factory · [[Prefer-Map-Fidelity-Automation-Plan]].
