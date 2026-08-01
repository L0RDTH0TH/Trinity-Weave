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
2. Process **pending** items **sequentially** — prefer `walk_tier: series` first (series packs), then coverage, then thickeners. Bone pilot may reorder via manual edit.
3. **Altitude:** series parents must be `product_contract`. AP / scene captions are thickeners only — never promote to series.
4. **Anti-mandate:** Actual-Play exemplars ≠ product default. Prefer structure menus / capability contracts. Name **≥2 alternatives this row does not ban** (see `_shared/WHAT-GOOD-LOOKS-LIKE.md` + pack `does_not_mandate`).
5. **DM seat:** privileged DM tools OK; refuse DM-as-infrastructure; keep orchestrator fun (`dm_as_player`) visible.
6. Follow card legs. **One pending UX noun per turn** — prefer `walk_tier: series` first; do not invent the list.
7. **Ground Meaning in project goals/intent:** cite pack `CONCEPTUAL-EXCERPT` (PMG) and, when needed, poll `ROADMAP-RESOURCE-INDEX.yaml` for the owning roadmap/resource; request fulfill/`tert_id` or paste if the body is not in pack. Do not invent note titles/bodies; do not ground only on AP skins.
8. Preflight every draft; never CARD-INDEX. After Cursor apply: friction check before `done`.

**When you need more info during mint:** open `ROADMAP-RESOURCE-INDEX.yaml`, find the roadmap entry, follow `wiki_links` / `linked_resources`. Bodies not in pack → ask bone pilot for fulfill (`tert_id`) or paste. Do not invent notes.

synced_at: `2026-08-01T07:20:25Z`

Connector = Trinity-Weave published pack for the named `project_id` (`Docs/catalog-mint/<project_id>/`). Vault is inaccessible to Grok. Ask bone pilot to re-run `catalog_mint_pack_emit` + Trinity sync if files are missing or stale.
