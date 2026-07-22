# Project branch layout (locked)

Branch name: `project/genesis-mythos-master`

```text
project/genesis-mythos-master/   ← branch name (not a folder on branch)
├── GROK-PROJECT-START.md
├── PROJECT-OBSERVABILITY.json
├── TERTIARY-INDEX.json
├── genesis-mythos-master-goal.md
├── genesis-mythos-master-Roadmap-MOC.md
└── Roadmap/
    ├── (conceptual phases…)
    ├── Execution/
    └── User-Story/
        ├── CATALOG-MINT-BLANK.md  ← single-row dialogue contract
        ├── MINT-EPOCH.md          ← poison guard / active mint epoch
        ├── user-story-state.md
        ├── slice-catalog.yaml
        └── scopes/<row_id>/L5.md …
```

`PROJECT-OBSERVABILITY.json` includes a `bridge` block:

```json
"bridge": {
  "trinity_repo": "L0RDTH0TH/Trinity-Weave",
  "main_branch": "main",
  "project_branch": "project/genesis-mythos-master",
  "layout_version": "1"
}
```

Gate cards (`catalog_mint_gate`, `catalog_mint`, etc.) live on **`main`**, not this branch.

**Mint with Grok:** do **not** attach this project branch. On **`main`**, open `weave/component-proposals/catalog_mint.yaml` then `Docs/catalog-mint/<project_id>/`. Historical remint is cite-only (`MINT-EPOCH.md`). Cursor applies approved rows → `catalog_mint_pack_emit` (+ weave publish) so Grok sees the updated pack.
