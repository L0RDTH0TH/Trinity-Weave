---
title: Grok — start here (Trinity-Weave)
created: 2026-06-09
updated: 2026-08-01
audience: grok_github_integration
---

# Grok — start here

**Repo:** [L0RDTH0TH/Trinity-Weave](https://github.com/L0RDTH0TH/Trinity-Weave)

**Custom instructions (paste into Grok Chat):**  
→ **[Docs/Grok-Second-Brain-Custom-Instructions.md](https://github.com/L0RDTH0TH/Trinity-Weave/blob/main/Docs/Grok-Second-Brain-Custom-Instructions.md)**  
(canonical on `main` — do not hunt the private vault)

**Capability:** Grok **cannot** be given the private Second-Brain vault. Trinity-Weave is the public surface so Grok **can** navigate published project material.

**Layout:** **`main`** = Trinity (**the system** — mint law + pack walk queue). **`project/<project_id>`** = **the project being served** (PMG + full `Roadmap/`). Mint uses both.

**Two-pass mint:** Pass A = pending `walk_tier: series` only until series are done **and** `series_published_trinity_ref` is set on the pack backlog. Pass B = after `children_greenlit`, validate Cursor child drafts lensed by series (`parent_id`) — do not invent the child list. Details: pack `MINT-PACK.md` Walk Order + custom instructions above.

**World ≠ campaign** — world is the durable container; campaigns (and casts) nest inside it.

**Project navigation (mint):** bone pilot names **`project_id`** → open **`main` pack** `Docs/catalog-mint/<project_id>/` (walk queue) **and** branch **`project/<project_id>`** (PMG + full `Roadmap/` grounding). Both surfaces. Not “main only.”

**Not a mint corpus:** `/home/workdir/artifacts/` sandbox. Load from GitHub **Trinity-Weave**.

---

## STOP — “mint the catalog” / product deliverables

**Only when the bone pilot explicitly instructs mint and names `project_id`.** Otherwise talk normally — do not open a mint session or emit a YAML receipt. Do not guess `project_id` from branches or ACTIVE.md.

When instructed:

1. Use the **named** `project_id` from the mint cue.
2. Confirm custom instructions match [this file](https://github.com/L0RDTH0TH/Trinity-Weave/blob/main/Docs/Grok-Second-Brain-Custom-Instructions.md) (or ask bone pilot to refresh paste).
3. Open **`weave/component-proposals/catalog_mint.yaml`** (Trinity card — process / touch / rules).
4. Open pack **`Docs/catalog-mint/<project_id>/`** — `MINT-PACK.md`, backlog (`mint_phase` / Trinity refs), conceptual, pins, index, stack excerpts. Poll the index; request fulfill by `tert_id` for missing bodies.
5. Obey **two-pass** Walk Order (series first; children only when greenlit). Preflight every draft; series = one YAML receipt/turn; children = batch validate Cursor drafts. Await `approve` / `edit` / `reject`.

Ignore archived `gmm-catalog-mint` if old links surface it.

---

## What this repo is (weave law)

Trinity-Weave is the public design manual + code slice for an agentic Second Brain maintenance layer (YAML cards, harness, host-weld) **and** the published per-project mint packs.

Bone pilot / Cursor must **publish** pack updates here for Grok to see them. Stale pack = ask for republish.

## Read order — weave law only (not mint)

1. `OBSERVABILITY.json`
2. `Docs/ARCHITECTURE-OVERVIEW.md`
3. `weave/CARD-INDEX.md` — **card** catalog, not product mint
4. `Docs/GLOSSARY-FOR-EXTERNAL-READERS.md`

## Question routing

| Question | Where |
|----------|--------|
| Mint / walk for a named project | **`main` (system):** catalog_mint + pack walk queue · **`project/<id>` (served):** PMG + Roadmap grounding |
| Custom instructions paste | [Docs/Grok-Second-Brain-Custom-Instructions.md](https://github.com/L0RDTH0TH/Trinity-Weave/blob/main/Docs/Grok-Second-Brain-Custom-Instructions.md) |
| Weave cards / host-weld / harness | `weave/components/`, `weave/component-proposals/` |
| Live queue / Watcher / vault notes | Unavailable — ask for paste or fulfill |

## Hard limits

- **Cannot** access private vault / Watcher / `1-Projects/…`
- Never confuse **card catalog** (`CARD-INDEX`) with **product slice-catalog** (`Docs/catalog-mint/<id>/slice-catalog.yaml`)
- Pasteable custom instructions: **[Docs/Grok-Second-Brain-Custom-Instructions.md](https://github.com/L0RDTH0TH/Trinity-Weave/blob/main/Docs/Grok-Second-Brain-Custom-Instructions.md)**

## Key paths

| Path | Contents |
|------|----------|
| [`Docs/Grok-Second-Brain-Custom-Instructions.md`](https://github.com/L0RDTH0TH/Trinity-Weave/blob/main/Docs/Grok-Second-Brain-Custom-Instructions.md) | **Paste into Grok Chat → Custom instructions** |
| `weave/component-proposals/catalog_mint.yaml` | **Mint instruction law** |
| `Docs/catalog-mint/<project_id>/` | **That project’s published pack** (navigate here when `project_id` is named) |
| `Docs/GROK-PROJECT-BRIDGE.md` | Bridge notes |
| `meat-suit-entry/` | Bone pilot hub |
| `weave/components/*.yaml` | Locked cards |
| `scripts/eat_queue_core/harness.py` | CLI (operator/Cursor — pack emit / receipt validate) |
