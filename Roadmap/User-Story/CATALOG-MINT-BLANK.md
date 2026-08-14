# CATALOG MINT — vault pointer (Cursor / export)

**Grok instruction law is not this file.**

On Trinity-Weave **`main`**:

1. `weave/component-proposals/catalog_mint.yaml`
2. `Docs/catalog-mint/<project_id>/` (see `Docs/catalog-mint/ACTIVE.md`)

Bone pilot applies approved receipts into:

`Roadmap/User-Story/slice-catalog.yaml`

**Prune / freeze the harvest in Obsidian:**

`Roadmap/User-Story/MINT-BACKLOG.md`

Taxonomy (split): `Templates/Roadmap/User-Story/UX-MINT-TAXONOMY/`  
Project profile: `Roadmap/User-Story/UX-MINT-TAXONOMY.project.yaml` (`domain_packs: []` for core-only)
(Machine mirror: `MINT-BACKLOG.yaml`.)

Draft after conceptual freeze:

```bash
PYTHONPATH=scripts python3 -c "
from pathlib import Path
from eat_queue_core.weave.user_story.ux_mint_backlog import generate_ux_mint_backlog
print(generate_ux_mint_backlog(Path('.'), project_id='<id>').to_dict())
"
```

Then refresh the pack:

```bash
PYTHONPATH=scripts python3 -m scripts.eat_queue_core.harness catalog_mint_pack_emit --vault-root . --project-id <id>
PYTHONPATH=scripts python3 -m scripts.eat_queue_core.harness catalog_mint_receipt_validate --vault-root . --project-id <id> --receipt-file <receipt.yaml>
```

See also: `MINT-EPOCH.md` (poison guard).
