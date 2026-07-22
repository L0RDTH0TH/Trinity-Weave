# Grok — start here

**Repo:** [L0RDTH0TH/Trinity-Weave](https://github.com/L0RDTH0TH/Trinity-Weave)  
**What the bone pilot’s GitHub connector usually sees:** **`main` only** (OAuth login — **no branch picker**).

---

## STOP — “mint the catalog” / product deliverables

**Only when the bone pilot explicitly instructs mint and names `project_id`.** Otherwise talk normally — do not open a mint session or emit a YAML receipt. Do not guess `project_id` from branches or ACTIVE.md.

When instructed:

1. Use the **named** `project_id` from the mint cue.
2. Open **`weave/component-proposals/catalog_mint.yaml`** (Trinity card — process / touch / rules).
3. Open pack **`Docs/catalog-mint/<project_id>/`** — pull conceptual + pins + `ROADMAP-RESOURCE-INDEX.yaml` + tech-stack excerpts. Poll the index for more context; request fulfill by `tert_id` for missing bodies.
4. Preflight every draft; **one** YAML receipt; await `approve` / `edit` / `reject`.

Ignore archived `gmm-catalog-mint` if old links surface it.

---

## What this repo is (weave law)

Trinity-Weave is the public design manual + code slice for an agentic Second Brain maintenance layer (YAML cards, harness, host-weld).

You see **committed git** (usually `main`). Bone pilot may paste packs for anything else.

## Read order — weave law only (not mint)

1. `OBSERVABILITY.json`
2. `Docs/ARCHITECTURE-OVERVIEW.md`
3. `weave/CARD-INDEX.md` — **card** catalog, not product mint
4. `Docs/GLOSSARY-FOR-EXTERNAL-READERS.md`

## Question routing

| Question | Where |
|----------|--------|
| Mint catalog / product deliverable rows (any project) | **`catalog_mint` card** + **`Docs/catalog-mint/<project_id>/`** |
| Weave cards / host-weld / harness | `weave/components/`, `weave/component-proposals/` |
| Live queue / Watcher | Unavailable — ask for paste |

## Hard limits

- No live vault / Watcher
- Never confuse **card catalog** (`CARD-INDEX`) with **product slice-catalog** (`Docs/catalog-mint/<id>/slice-catalog.yaml`)
- Pasteable custom instructions: `Docs/Grok-Second-Brain-Custom-Instructions.md`

## Key paths

| Path | Contents |
|------|----------|
| `weave/component-proposals/catalog_mint.yaml` | **Mint instruction law** |
| `Docs/catalog-mint/` | **Per-project packs** (+ `ACTIVE.md`) |
| `Docs/GROK-PROJECT-BRIDGE.md` | Bridge notes |
| `Docs/Grok-Second-Brain-Custom-Instructions.md` | Paste into Grok Chat |
| `meat-suit-entry/` | Bone pilot hub |
| `weave/components/*.yaml` | Locked cards |
| `scripts/eat_queue_core/harness.py` | CLI (operator/Cursor — pack emit / receipt validate) |
