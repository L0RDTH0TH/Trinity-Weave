# Branches

## `main` — weave law

- `weave/components/` — locked cards
- `weave/component-proposals/` — provisional cards (still authoritative for active gates)
- `OBSERVABILITY.json`, `weave/CARD-INDEX.md`
- `Docs/bone-pilot/` — you are here

## `project/<project-id>` — project instances

Pilot: **`project/godot-genesis-mythos-master`**

Artifacts at **branch root** (not nested under a `project/` folder on the branch):

See [[PROJECT-BRANCH-LAYOUT|PROJECT-BRANCH-LAYOUT]] for the canonical tree.

## Rules

- **Never merge** project branches into `main`
- Weave sync updates `main` only; project sync updates `project/<id>` only
- Push budget prioritizes **`main`** before project branches
