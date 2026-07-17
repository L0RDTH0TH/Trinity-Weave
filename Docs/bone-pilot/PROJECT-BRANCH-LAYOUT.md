# Project branch layout (locked)

Branch name: `project/godot-genesis-mythos-master`

```text
├── GROK-PROJECT-START.md
├── PROJECT-OBSERVABILITY.json
├── TERTIARY-INDEX.json
├── godot-genesis-mythos-master-goal.md
├── godot-genesis-mythos-master-Roadmap-MOC.md
└── Roadmap/
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
  "project_branch": "project/godot-genesis-mythos-master",
  "layout_version": "1"
}
```

Gate cards (`catalog_mint_gate`, etc.) live on **`main`**, not this branch.
