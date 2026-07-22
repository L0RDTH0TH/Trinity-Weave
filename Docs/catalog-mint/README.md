# Catalog mint packs (Grok-visible on `main`)

**Instruction law:** `weave/component-proposals/catalog_mint.yaml`

**Layout:**

```text
Docs/catalog-mint/
  ACTIVE.md
  _shared/WHAT-GOOD-LOOKS-LIKE.md
  <project_id>/
    MINT-PACK.md
    PACK-MANIFEST.yaml
    CONCEPTUAL-EXCERPT.md
    PIN-INDEX.md
    ROADMAP-RESOURCE-INDEX.yaml   ← poll roadmap + connected resources
    PIN-EXCERPTS/
    Tech-Stack-Excerpt.yaml
    Stack-Domain-Registry-Excerpt.yaml
    slice-catalog.yaml
```

**Poll rule:** when minting and more context is needed, open `ROADMAP-RESOURCE-INDEX.yaml` first; follow `wiki_links` / `linked_resources`; request fulfill by `tert_id` (or paste) if bodies are not in `PIN-EXCERPTS/`.

Refresh (vault / Cursor):

```bash
PYTHONPATH=scripts python3 -m scripts.eat_queue_core.harness catalog_mint_pack_emit --vault-root . --project-id <id>
```

Validate a draft receipt before apply:

```bash
PYTHONPATH=scripts python3 -m scripts.eat_queue_core.harness catalog_mint_receipt_validate \
  --vault-root . --project-id <id> --receipt-file /path/to/receipt.yaml
```
