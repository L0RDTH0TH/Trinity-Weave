---
title: Bindings — config anti-hardcode
created: 2026-10-21
updated: 2026-10-21
audience: grok_github_integration
---

# Bindings — config anti-hardcode

The weave must not bake a product into harness Python. Families live in **project** YAML; Trinity **`main`** only ships the resolver, engine-neutral proof ops, host-law evaluator, and a denylist regression net.

## Surfaces

| Branch | What Grok should read |
|--------|------------------------|
| `main` | `scripts/eat_queue_core/weave/factory/bindings.py`, `proof_runner.py`, `host_law.py`, `prefer_authorship_contract.py`, `operator_feedback.py` (`required_playtest_ids`), `closed_alpha_passes.py`, `engine_preflight.py`, `implementation_handoff.py`, `lane_agent_registry.py`, `tests/test_harness_product_denylist.py` (Pass-4 tokens), `tests/test_bindings_resolve.py`, `tests/test_proof_runner.py`, `tests/test_blank_project_contract_eat.py`, `tests/test_implementation_single_seat.py`, `Docs/HALF-B-CONTRACT.md` |
| `project/<project_id>` | `Factory-DRB/bindings/{identity,engine,lanes,proof-catalog,host-law,legacy-refuse}.yaml` — Genesis tip: `host-law` `entries: []`, `proof-catalog.required_playtest_ids: []`, `engine.build_command: ''`, `identity.queue_lane` set |

## Rules (locked)

- One raising resolver. Missing family/key → `binding_missing`. Unknown Prefer probe id → `unknown_probe`.
- `game_repo_path` sole source: `bindings/identity.yaml`. `factory-project.yaml` keeps eat latches only.
- Proof ops on `main` are only: `file_exists`, `file_contains`, `field_equals`, `command_exits_zero`. Scene/engine nouns are **args** in that project’s `proof-catalog.yaml`. Empty checklist → run nothing. Never iterate the whole catalog.
- `host-law.yaml` entries: `{id, cite, refuse_code, applies_when}`. Absent file → not applicable. Harness does not special-case video ids.
- Registries deleted, not shadowed: missing `engine.yaml` / `lanes.yaml` raises; no Python fallback dict for forgotten lanes.
- Denylist grows in the **same commit** that deletes tokens from production `scripts/`.
- CLI: one helper `add_project_id_argument(required=True)` — no silent project-id defaults.
- No GREENLIGHT implied by publish.

## Publish tips (Trinity-Weave)

| Pass | Tip (approx) | Content |
|------|----------------|---------|
| 1 | `ab3f217` | Resolver + Pass-1 denylist + fail-closed Family A (fixture-proven) |
| 2 | `5ebe2d0` | `proof_runner`; delete `LANE_ADAPTER` / baked checklists; `half_b` purge; Pass-2 denylist |
| 3 | `46183b0` (+ project `b847329`) | `host_law` evaluator; Half-B docs off main allowlist; Genesis bindings consumer on `project/genesis-mythos-master` |
| 4 | `7b39fc9` (+ project `c5732fa`) | Eat-path fail-closed: `host_law_ids` only; delete closed-alpha release alias; `proof-catalog.required_playtest_ids`; lane from identity; no Godot binary invent; blank-project contract-eat fixture; Half-B pilots off main; Pass-4 denylist. **Refuse demo injection — not a functional feedstock→Genesis line.** |
| 5 | `c25a447` | Half B single-seat check: `Docs/HALF-B-CONTRACT.md`; empty Prefer lanes → one `implementation` seat (not catalog); handoff = `behavior_keys` from armed Prefer; `integration_pass` invents nothing when `build_command` empty; bind = `topology_law` + `host_law_ids` only. **Prove the check — not GREENLIGHT / weld / concert.** |
| 6 | `e60fdff` | Prefer-align fail-closed + exit evidence pack = `behavior_keys` each true; live eat calls align before agent; blank fixture. **Not GREENLIGHT.** |
| 6b | `d50c3bb` (project) | Genesis Prefer/identity scrub so r2 can pass Prefer-align: empty `game_repo_path`, `host_law_ids: []`, cites/stamp/umbrella cleared. **Not GREENLIGHT.** |
| 7 | *(this tip)* | Discover write-target entries into Prefer-align; exit Success = `evaluate_behavior_evidence` only (reject agent-sourced pack). **Not GREENLIGHT. Re-run B₁ before any ticket.** |

## Genesis is a consumer

Harness tests use a blank **fixture-project** id synthesized in tests — not Genesis. Genesis bindings on `project/genesis-mythos-master` are data that **uses** the schema after `main` is green.

## Pass 4 tip claim

After Pass 4 the factory can **refuse a demo injection**. It does **not** claim a working production line from feedstock to a Genesis capability. Feedstock→Genesis remains a later fixture, then r2 — not this publish. No GREENLIGHT.

## Pass 5 tip claim

After Pass 5 Tip A the factory can dispatch **one** seat whose handoff is Prefer keys only, with no method invent when `build_command` is empty. It does **not** GREENLIGHT, weld, F5, or turn on multi-lane concert. Genesis consumer is Tip B after this tip is on `origin/main`.

## Pass 6 tip claim

Prefer-align blocks dispatch when Prefer and project config disagree; exit Success is an evidence pack for Prefer `behavior_keys` only. No Prefer rewrite. No GREENLIGHT. Tip B (Genesis Prefer/identity scrub) follows on the project branch after this tip is on `origin/main`.

## Pass 7 tip claim

Live runner discovers write-target files into Prefer-align. Exit Success is **only** B₂ `evaluate_behavior_evidence` (`pass_basis: behavior`); agent `{key: true}` fails. Empty proof catalog stays red. **Not GREENLIGHT.** Re-run Gate B₁ on scrubbed r2 before any GREENLIGHT.
