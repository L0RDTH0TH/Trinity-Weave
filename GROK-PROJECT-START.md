# Grok — project start (genesis-mythos-master)

**Branch:** `project/genesis-mythos-master` (branch name — artifacts at **branch root**, not nested under `project/`)

## Player / camera Code-Exhibit (mandatory)

Before any write touching player / camera / look / move:

1. Open `Roadmap/Execution/Docs/Godot-Implementation-Decision-Matrix.md` + `Godot-Stock-Patterns.md` (pin `PIN-stock_godot_fps.md`).
2. **Quote** the matrix principle line and the Player move/look row in your report.
3. Stock `CharacterBody3D` FPS only; hosts select cameras — they do not own locomotion.
4. Missing quote or invent-a-camera ⇒ **invalid pass**. Walk+look Done = **operator F5 only** (ban “MCP verified walk+look”).
5. Reject codes: `engine_pattern_miss` | `gui_input_steal` | `seat_ok_feel_fail` | `verify_mcp_only`.

Canonical agent brief: [[AGENTS]]. Trinity Half-B PRECONDITIONS + gates `godot_stock_fps` / `operator_kinesthetic_walk_look`. Factory remains not greenlit.

## If the task is catalog mint

**STOP — this is not `weave/CARD-INDEX` / OBSERVABILITY / harness mint.**

1. `Roadmap/User-Story/CATALOG-MINT-BLANK.md` — **dialogue contract** (one row per turn)
2. `genesis-mythos-master-goal.md` — PMG feedstock
3. Live `Roadmap/Phase-*/…` notes — real `conceptual_pin` titles
4. `Roadmap/User-Story/slice-catalog.yaml` — what is already applied
5. `Roadmap/User-Story/MINT-EPOCH.md` — poison guard (ignore archives)

Then: propose **exactly one** product deliverable row → await bone-pilot `approve` / `edit` / `reject` → next.
Do **not** invent wiki-links. Do **not** dump a batch of rows. Do **not** talk about spine/corps/self-wrap.

## General read order (non-mint)

1. `PROJECT-OBSERVABILITY.json` — nodes, edges, fingerprints
2. `TERTIARY-INDEX.json` — metadata-only tertiary pointers (bodies via fulfill packs)
3. `genesis-mythos-master-goal.md` / `genesis-mythos-master-Roadmap-MOC.md`
4. `Roadmap/` — conceptual, Execution, User-Story (catalog + scopes)

## Locked branch root layout

```text
project/genesis-mythos-master/   ← git branch name
├── GROK-PROJECT-START.md
├── PROJECT-OBSERVABILITY.json
├── TERTIARY-INDEX.json
├── genesis-mythos-master-goal.md
├── genesis-mythos-master-Roadmap-MOC.md
└── Roadmap/
    ├── Execution/
    └── User-Story/
        ├── CATALOG-MINT-BLANK.md   ← mint dialogue contract
        ├── MINT-EPOCH.md
        ├── slice-catalog.yaml
        └── scopes/<row_id>/L5.md …
```

## Weave law (not on this branch)

Gate cards (`catalog_mint_gate`, etc.) live on **`main`**: `weave/component-proposals/` and `weave/components/`.
They explain **how** mint works — they are **not** the product catalog you fill.

## Hard limits

- No live vault access from GitHub — stale remote possible; check `bridge` fingerprints
- Tertiary bodies only via mediated fulfill packs (bone pilot + Cursor gate)
