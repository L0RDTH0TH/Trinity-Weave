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

Gate cards (`catalog_mint_gate`, etc.) live on **`main`**, not this branch.

**Mint with Grok:** attach `main` (gate cards) + this project branch (catalog instance). Propose rows → vault apply → `project_bridge_sync` → push.
