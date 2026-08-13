# Mint pack — `genesis-mythos-master`

**Law:** open `weave/component-proposals/catalog_mint.yaml` first (Trinity card).

**Catalog frame:** each planned row is a **mini-trinity** (Conceptual · UX Meaning/L5 · Execution) — see [`_shared/CATALOG-MINI-TRINITY.md`](../_shared/CATALOG-MINI-TRINITY.md).

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
| `PIN-DERIVE-STATUS.md` | **Pin-before-L5 board** — digest-first Conceptual weld proposals |
| `scopes/<row>/PIN-DERIVE.md` | Pin derive primary — open full Conceptual note only when contested |
| `L5-AFFIRM-STATUS.md` | **L5 affirm board** (after pins) — digest-first; cross-row flags before attest |
| `scopes/<row>/L5-AFFIRM-DIGEST.md` | L5 affirm primary — open full `L5.md` only for yellow/red/thin |
| `scopes/<row>/L5.md` | Series Pass-B **+ pin** complete vision (after pin confirm) |
| `scopes/<parent>/children-of-<parent>/<child>/L5.md` | Child L5 after series L5; inherits series pins |
| `_shared/CHILD-BATCH-VALIDATION.md` | Pass B receipt shape + velocity rules |
| `_shared/PIN-DERIVE-VALIDATION.md` | Pin derive receipt shape |
| `_shared/L5-AFFIRM-VALIDATION.md` | L5 affirm receipt shape |
| `_shared/CATALOG-MINI-TRINITY.md` | Per-row mini-trinity + **Grok validation ladder** |
| `CONCEPTUAL-EXCERPT.md` | PMG / conceptual roll-up |
| `PIN-INDEX.md` | Legal conceptual_pin titles |
| `ROADMAP-RESOURCE-INDEX.yaml` | **Poll index** — roadmap notes + connected resources + tert_ids |
| `PIN-EXCERPTS/` | **Mandatory for pin derive** — plain same-span weld text (Grok ≠ highlight UI) |
| `Actual-Play-Feedstock/` | **Human phenomenology cards** (feel-pattern paraphrases) — Grok-readable on `main` |
| `Inspiration-UX-Feedstock/` | **Pinable games/tools + derived move-pins** — feedstock after series; seasoning mine after pins |
| `_shared/INSPIRATION-UX-FEEDSTOCK.md` | Inspiration MO law (feedstock + seasoning phases) |
| `_shared/INSPIRATION-SEASONING-VALIDATION.md` | Post-`apply_pins` seasoning gate receipt shape |
| `Inspiration-UX-Feedstock/INSPIRATION-SEASONING-STATUS.md` | Seasoning mine board (maps → Conceptual) |
| `Tech-Stack-Excerpt.yaml` | Locked/trialing/integrated stack rows |
| `Stack-Domain-Registry-Excerpt.yaml` | Domain ids + spine_interface |
| `slice-catalog.yaml` | Applied rows mirror |

## Feed envelope

**Core (always):** conceptual excerpt + THIS backlog noun + pins index + stack excerpts + catalog mirror.

**Human feedstock (when present):** `Actual-Play-Feedstock/` moment cards; `Inspiration-UX-Feedstock/` pinable sources + derived move-pins (pattern seasoning).

**Thickeners (optional — no auto-flood):** `neighbor_refs` (same `ux_axis` / backlog-adjacent, only when bone pilot requests `include_neighbors`), poll index, fulfill pastes, gap research when completeness flags fire.

See `FEED-ENVELOPE.yaml` for the machine summary of core / thickeners / completeness.

## Walk Order

**Grok ladder (content) v4:** series individually → (optional feedstock polish) → **Conceptual pin gate** (pin derive + seasoning maps, shared board) → **Pass B** → **series L5** → **children L5**. Never L5 before pin confirm. Never Pass B before shared pin gate closes. Never children L5 before series L5. Seasoning is **not** a separate ladder gate. **Operator Loop 2** = depth slice → validate levels — not L5. Cursor drafts ahead; Grok validates published pack only ([`CATALOG-MINI-TRINITY.md`](../_shared/CATALOG-MINI-TRINITY.md)).

**Two-pass mint (first-class):** series cards complete + on Grok-facing Trinity/GitHub before any children mine.

1. Confirm `MINT-BACKLOG` has `backlog_status: frozen_for_mint` and `mint_phase` in series walk (or bone pilot names an item id).
2. **Pass A — series only:** process pending `walk_tier: series` sequentially. Do **not** walk coverage/thickeners as peers.
3. **Altitude:** series parents must be `product_contract`. AP / scene captions are thickeners only — never promote to series.
4. **Anti-mandate:** Actual-Play exemplars ≠ product default. Prefer structure menus / capability contracts. Name **≥2 alternatives this row does not ban**.
5. **DM seat:** privileged DM tools OK; refuse DM-as-infrastructure; keep orchestrator fun (`dm_as_player`) visible.
6. When all series are `done`: bone pilot runs pack emit + **Trinity/GitHub sync** and records `series_published_trinity_ref`. Children mine is **blocked** until that ref exists (Curator backup is not the gate).
7. **Inspiration feedstock (after series Trinity):** User+Cursor build `Inspiration-UX-Feedstock/` — INDEX, LIKED-SNIPPETS, cards, share receipt. Grok polish optional (jobs/patterns, ≥1 refuse, challenge hyper-fit). Law: [`_shared/INSPIRATION-UX-FEEDSTOCK.md`](../_shared/INSPIRATION-UX-FEEDSTOCK.md).
8. **Archive premature L5** if any exist before Conceptual pins.
9. **Pin derive (digest-first; after Trinity; before Pass B):** open `PIN-DERIVE-STATUS.md` + per-row `PIN-DERIVE.md` + `PIN-EXCERPTS/`. One receipt per [`PIN-DERIVE-VALIDATION.md`](../_shared/PIN-DERIVE-VALIDATION.md). ≥1 `role: primary`. Titles only from `PIN-INDEX.md`. Yellow → Grok mint gate (loop cap one).
10. **Inspiration seasoning maps (same Conceptual pin gate — required):** open `INSPIRATION-SEASONING-STATUS.md` + feedstock cards. Map → Conceptual/series. Set RECEIPT `inspiration_seasoning_disposition: applied|waived` (`waived` needs `inspiration_seasoning_waive_reason`). Harness fail-closed while `open`. Not a separate ladder unlock.
11. **Pass B — children:** only after shared pin gate closed + `children_greenlit`. Open `CHILD-BATCH-STATUS.md` + `BATCH-DIGEST.md` first. One receipt per [`CHILD-BATCH-VALIDATION.md`](../_shared/CHILD-BATCH-VALIDATION.md). After green: `lock_child_batch` → Trinity → `publish_children`.
12. Follow card legs. **One pending UX noun per turn** during Pass A. Pass B = **one batch receipt per turn**. Ground Meaning selectively via `CONCEPTUAL-EXCERPT` / poll index.

### L5 affirm (after Pass B + lens pack; not Operator Loop 2)

13. **Series L5 affirm (digest-first):** open `L5-AFFIRM-STATUS.md` + digests. One receipt per [`L5-AFFIRM-VALIDATION.md`](../_shared/L5-AFFIRM-VALIDATION.md). Full `L5.md` only yellow/red/thin.
14. **Children L5** — all Pass B children under each parent after that series L5; inherit series pins. Digest-first batches.
15. Operator fills **Cross-row flags (max 3)** → family attest → **Operator Loop 2** → then `catalog_signed_at`. L5 files existing ≠ signed.

**When you need more info during mint:** open `ROADMAP-RESOURCE-INDEX.yaml`, find the roadmap entry, follow `wiki_links` / `linked_resources`. Bodies not in pack → ask bone pilot for fulfill (`tert_id`) or paste. Do not invent notes.

synced_at: `2026-08-13T23:24:30Z`

Connector = Trinity-Weave published pack for the named `project_id` (`Docs/catalog-mint/<project_id>/`). Vault is inaccessible to Grok. Ask bone pilot to re-run `catalog_mint_pack_emit` + Trinity sync if files are missing or stale.
