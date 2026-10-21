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
| `main` | `scripts/eat_queue_core/weave/factory/bindings.py`, `proof_runner.py`, `host_law.py`, `tests/test_harness_product_denylist.py`, `tests/test_bindings_resolve.py`, `tests/test_proof_runner.py` |
| `project/<project_id>` | `Factory-DRB/bindings/{identity,engine,lanes,proof-catalog,host-law,legacy-refuse}.yaml` |

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

## Genesis is a consumer

Harness tests use a blank **fixture-project** id synthesized in tests — not Genesis. Genesis bindings on `project/genesis-mythos-master` are data that **uses** the schema after `main` is green.
