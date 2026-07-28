# Mint pack — `genesis-mythos-master`

**Law:** open `weave/component-proposals/catalog_mint.yaml` first (Trinity card).

**This folder** is feedstock for product `slice-catalog.yaml` rows — not CARD-INDEX.

| File | Use |
|------|-----|
| `PACK-MANIFEST.yaml` | synced_at + required files |
| `FEED-ENVELOPE.yaml` | Core vs thickeners + completeness flags |
| `MINT-BACKLOG.yaml` | **Walk queue** — machine mirror (Grok pack) |
| `MINT-BACKLOG.md` | **Obsidian prune surface** — operator edits status / labels here |
| `CONCEPTUAL-EXCERPT.md` | PMG / conceptual roll-up |
| `PIN-INDEX.md` | Legal conceptual_pin titles |
| `ROADMAP-RESOURCE-INDEX.yaml` | **Poll index** — roadmap notes + connected resources + tert_ids |
| `PIN-EXCERPTS/` | Optional pin body mirrors |
| `Actual-Play-Feedstock/` | **Human phenomenology cards** (feel-pattern paraphrases) — Grok-readable on `main` |
| `Tech-Stack-Excerpt.yaml` | Locked/trialing/integrated stack rows |
| `Stack-Domain-Registry-Excerpt.yaml` | Domain ids + spine_interface |
| `slice-catalog.yaml` | Applied rows mirror |

## Feed envelope

**Core (always):** conceptual excerpt + THIS backlog noun + pins index + stack excerpts + catalog mirror.

**Human feedstock (when present):** `Actual-Play-Feedstock/` moment cards — pattern paraphrases from live-table / digital-D&D *feel* exemplars (not story clones). Prefer these when critiquing backlog quality.

**Thickeners (optional — no auto-flood):** `neighbor_refs` (same `ux_axis` / backlog-adjacent, only when bone pilot requests `include_neighbors`), poll index, fulfill pastes, gap research when completeness flags fire.

See `FEED-ENVELOPE.yaml` for the machine summary of core / thickeners / completeness.

## Walk Order

1. Confirm `MINT-BACKLOG` has `backlog_status: frozen_for_mint` (Obsidian `.md` or YAML mirror; or bone pilot names an item id).
2. Process **pending** items **sequentially** (one UX noun per receipt). Bone pilot may reorder via manual edit.
3. **Anti-mandate:** Actual-Play exemplars ≠ product default. Prefer structure menus / capability contracts over single-skin story nouns. If several pending siblings share one feedstock pin, ask whether a **general parent** should replace N narrow clones before drafting.
4. Map experience shape → pseudo-code stubs; do **not** invent backlog entries. In Meaning prose, name **alternatives this row does not ban** (see `_shared/WHAT-GOOD-LOOKS-LIKE.md`).
5. After Cursor apply: friction check (`Docs/catalog-mint/_shared/FRICTION-CHECK.md`) — persona friction **and** “does this encode one plot/structure as the product default?” — before marking the item `done`.

**When you need more info during mint:** open `ROADMAP-RESOURCE-INDEX.yaml`, find the roadmap entry, follow `wiki_links` / `linked_resources`. Bodies not in pack → ask bone pilot for fulfill (`tert_id`) or paste. Do not invent notes.

synced_at: `2026-07-28T20:43:49Z`

Connector = **main only**. Ask bone pilot to re-run `catalog_mint_pack_emit` if files are missing.
