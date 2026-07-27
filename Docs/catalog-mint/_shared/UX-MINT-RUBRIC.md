---
title: UX mint rubric (cross-project)
---

# UX mint rubric (cross-project)

Law for post-conceptual-freeze backlog draft. Enforced via split taxonomy + `ux_mint_taxonomy.py`.

## Purpose (LLM-feed-first)

Catalog mint drafts **experience nouns** as the primary feed for later L5 / pseudo-code.

## Split taxonomy architecture

| Layer | Path | Role |
|-------|------|------|
| **Core** | `Templates/Roadmap/User-Story/UX-MINT-TAXONOMY/UX-MINT-TAXONOMY.core.yaml` | Product-agnostic framework + minimal slots |
| **Manifest** | `.../UX-MINT-TAXONOMY/manifest.yaml` | Domain pack registry + defaults |
| **Domain packs** | `.../UX-MINT-TAXONOMY/domains/<id>.yaml` | Game, web, etc. (optional per project) |
| **Project profile** | `Roadmap/User-Story/UX-MINT-TAXONOMY.project.yaml` | `domain_packs: []` or `[game_vtt]` |
| **Overlay** | `UX-MINT-TAXONOMY.overlay.yaml` | Operator slot tweaks |

## Feedstock (authority order)

1. PMG (full / high limit)
2. **Actual-Play-Feedstock** moment / feel-pattern cards (`actual_play:`) — **primary signal**
3. Influence deck + Agent-Research (project aliases)
4. Rules CDRs + Factory-DRB
5. Phase 4–6 + UX-relevant pins
6. Remaining conceptual / Phase 1–3
7. Resources → Archives (cite-only)

**Corpus weight (GMM):** BG feel-pattern cards + CR table cards are **co-primary**. Architecture pins are coverage thickeners, not the experiential source of truth.

Harvest emits **Actual-Play experience nouns as the primary mint walk**, then taxonomy slots as **coverage supplements**, then pin/theme thickeners. Prefer phenomenology cards over architecture pins when both match. Enrichment must pull `actual_play:` excerpts first.

**Walk tiers**

| `walk_tier` | Role | `supplement` |
|-------------|------|--------------|
| `phenomenology` | CR/BG moment-card nouns — **walk first** | `false` |
| `coverage` | Taxonomy slots (coverage gate; collapsed pillars) | `true` |
| `thickener` | Theme seeds / pin headings | `true` |

## Post-harvest quality gates (human criteria)

Before freeze, the backlog should show first-class nouns (or clear maps) for:

1. **Camp / quiet between pillars** — continuous fiction, not only a rest button
2. **Stolen or soft-power loss of agency** — wake-in-violation, institutional seizure, absent seat
3. **Moral choice that changes who you fight and who trusts you**
4. **Information that feels earned** (player assembled it) — not spoon-fed lore
5. **Control-surface mapping** — screen region, persistence, input verbs, spatial feedback anchors
6. **Ordinary progression rhythm** — table/world felt the numbers move (not only mythic pacts)
7. **Human-operated story** — living reaction / fourth option; refuse dialogue-wheel-only social model

If those fail, add Wave B cards or Grok deepen (D) — do not freeze a system-noun list.

## Operator gate

1. Harvest → `MINT-BACKLOG.md` + `.yaml` (`proposed`)
2. Prune in Obsidian against the quality gates above → `frozen_for_mint`
3. Grok walks `pending` nouns
4. Friction check before `done`
