# Mint pack — `genesis-mythos-master`

**Law:** open `weave/component-proposals/catalog_mint.yaml` first (Trinity card).

**This folder** is feedstock for product `slice-catalog.yaml` rows — not CARD-INDEX.

| File | Use |
|------|-----|
| `PACK-MANIFEST.yaml` | synced_at + required files |
| `FEED-ENVELOPE.yaml` | Core vs thickeners + completeness flags |
| `MINT-BACKLOG.yaml` | **Walk queue** — machine mirror (Grok pack) |
| `MINT-BACKLOG.md` | **Obsidian prune surface** — operator edits status / labels here |
| `CHILD-BATCH-STATUS.md` | **Same-width child batches** — locked vs active parent (prefer over chat memory) |
| `scopes/<parent>/BATCH-DIGEST.md` | **Pass B primary** — receipt-first summaries; open full `WALK.md` only for flagged ids |
| `scopes/` walk tree | `SERIES.md` + `children-of-<parent>/<child>/WALK.md` |
| `_shared/CHILD-BATCH-VALIDATION.md` | Pass B receipt shape + velocity rules |
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

**Two-pass mint (first-class):** series cards complete + on Grok-facing Trinity/GitHub before any children mine.

1. Confirm `MINT-BACKLOG` has `backlog_status: frozen_for_mint` and `mint_phase` in series walk (or bone pilot names an item id).
2. **Pass A — series only:** process pending `walk_tier: series` sequentially. Do **not** walk coverage/thickeners as peers.
3. **Altitude:** series parents must be `product_contract`. AP / scene captions are thickeners only — never promote to series.
4. **Anti-mandate:** Actual-Play exemplars ≠ product default. Prefer structure menus / capability contracts. Name **≥2 alternatives this row does not ban**.
5. **DM seat:** privileged DM tools OK; refuse DM-as-infrastructure; keep orchestrator fun (`dm_as_player`) visible.
6. When all series are `done`: bone pilot runs pack emit + **Trinity/GitHub sync** and records `series_published_trinity_ref`. Children mine is **blocked** until that ref exists (Curator backup is not the gate).
7. **Pass B — children:** after series Trinity gate + `children_greenlit`, Grok+user validate **one same-width batch** under `active_child_batch`. Open `CHILD-BATCH-STATUS.md` + `scopes/<parent>/BATCH-DIGEST.md` first. Return **one** receipt per [`CHILD-BATCH-VALIDATION.md`](../_shared/CHILD-BATCH-VALIDATION.md). Open full `WALK.md` only for yellow/red/thin. Do **not** walk children one-by-one like series. After green: bone pilot `lock_child_batch` → Trinity sync → `publish_children`.
8. Follow card legs. **One pending UX noun per turn** during **Pass A series only**. Pass B = **one batch receipt per turn**. Do not invent the list. Reject summaries that still contain `Feedstock:` / AP label dumps / `Pillars: (infer…)` residue.
9. **Ground Meaning selectively:** cite pack `CONCEPTUAL-EXCERPT` (PMG); pull poll index / fulfill only for thin or contested ids. Friction check once per batch (or contested child).

**When you need more info during mint:** open `ROADMAP-RESOURCE-INDEX.yaml`, find the roadmap entry, follow `wiki_links` / `linked_resources`. Bodies not in pack → ask bone pilot for fulfill (`tert_id`) or paste. Do not invent notes.

synced_at: `2026-08-03T17:20:13Z`

Connector = Trinity-Weave published pack for the named `project_id` (`Docs/catalog-mint/<project_id>/`). Vault is inaccessible to Grok. Ask bone pilot to re-run `catalog_mint_pack_emit` + Trinity sync if files are missing or stale.
