---
title: UX mint rubric (cross-project)
---

# UX mint rubric (cross-project)

Law for post-conceptual-freeze backlog draft. Enforced via series packs + taxonomy + `ux_mint_taxonomy.py` / `ux_mint_series.py`.

## Purpose (LLM-feed-first)

Catalog mint drafts **experience nouns** as the primary feed for later L5 / pseudo-code. Later walks argue **content** (scope, agency, honest skins) — not repeatedly repair **entry shape**.

## Sets of series (primary walk)

Mine emits **sets of series** — extensible ordered families of maximal-reach parents — not one fixed noun list and not CR/BG episode captions as peers.

| Layer | Path | Role |
|-------|------|------|
| **Series packs** | `Templates/.../UX-MINT-SERIES/` (+ optional project overlay) | **Only** source of `walk_tier: series` parents |
| **Core taxonomy** | `UX-MINT-TAXONOMY.core.yaml` | Product-agnostic coverage slots |
| **Domain packs** | `.../domains/<id>.yaml` | Coverage supplements |
| **Project profile** | `UX-MINT-TAXONOMY.project.yaml` | Domain pack selection |
| **Altitude exemplars** | `Docs/catalog-mint/_shared/SERIES-ALTITUDE-EXEMPLARS.md` | Pack-authoring targets (cite-only) |

## Walk tiers

| `walk_tier` | Role | `supplement` |
|-------------|------|--------------|
| `series` | Series-pack parents — **walk first** (`altitude: product_contract` only) | `false` |
| `coverage` | Taxonomy slots (coverage gate) | `true` |
| `thickener` | AP scene skins, theme seeds, texture | `true` |

**Invariant:** Actual-Play `label`/`summary` candidates are **never** `walk_tier: series`.

## Altitude

| `altitude` | Series parent? |
|------------|----------------|
| `product_contract` | **Yes** |
| `experience_texture` | No → thickener / L5 |
| `scene_exemplar` | No → thickener / skin |

## Anti-mandate (plain language)

Do not let one Critical Role / BG3 *moment* become product law.

| Term | Meaning |
|------|---------|
| **Structure menu** | Family of legitimate shapes the table can choose |
| **Capability contract** | What the surface can do without requiring one plot |
| **AP = skin** | Feedstock proves a feel can exist; episode dressing is optional under a parent |

**Smell:** “the game begins by…”, “first session teaches…”, “the only correct ending is…”

**Freeze gate (fail-closed):** each non-dropped series parent needs **≥2** `alternatives_not_banned` **or** ≥2 `does_not_mandate` strings before `frozen_for_mint`.

Pack members should carry `does_not_mandate: [...]` so Cursor/Grok see anti-mandate at walk time.

## DM seat (privilege vs infrastructure)

- **OK:** DM greater access, different seat, privileged tools, different gameplay experience.
- **Refuse:** DM as system infrastructure (rail/cue-bot/machine) with no orchestrator fun.
- Tag DM-facing surfaces `dm_as_player` (and `privileged_access` when true).

## Depth-spread (later walks)

After parents lock: mint **same-width sibling batches** per depth (maximal horizontal band), then deepen. No hard count of 7 — stop a band at diminishing returns (duplicate feel, episode-only, anti-mandate fail).

## Lenses (audit / tags — do not replace catalog)

Tutorial/play-flow, seat/DM-as-player, time-scale, pillar, authorship/modability, anti-mandate, agency-envelope, continuity/downtime, depth-spread, altitude.

Companion: `MINT-LENS-AUDIT.md` (tutorial-shaped coverage checklist). **Catalog remains** `slice-catalog.yaml` handles.

## Feedstock (authority order)

1. PMG  
2. Actual-Play cards — **evidence / skins** (not primary nouns)  
3. Influence / research / rules / pins  
4. Resources → Archives (cite-only)

## Series member wording

Prefer verb/state contracts (“combat can resolve by authored non-win paths”) over chrome-first parents (“campfire identity chrome”).

## Operator gate

1. Harvest → backlog (`proposed`) + lens audit  
2. Prune (altitude, anti-mandate, DM-fun) → freeze (coverage + alternatives gates)  
3. Grok walks `pending` series first  
4. Friction check before `done`  
5. Later: same-width child batches under locked parents  

## Remine prep (after mine redesign)

See catalog-mint skill **Remine checklist**: snapshot → wipe poison → `generate(..., merge=False)` → pack emit → prune/freeze → walk. Wipe may run without remine in the same change set.
