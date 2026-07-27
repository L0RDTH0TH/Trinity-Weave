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

**Core-only example (website):** `domain_packs: []` — no game/VTT slots.  
**Game example:** omit profile (uses manifest default `game_vtt`) or `domain_packs: [game_vtt]`.

## Feedstock (authority order)

1. PMG (full / high limit)
2. **Actual-Play-Feedstock** moment / feel-pattern cards (`actual_play:`)
3. Influence deck + Agent-Research (project aliases)
4. Rules CDRs + Factory-DRB
5. Phase 4–6 + UX-relevant pins
6. Remaining conceptual / Phase 1–3
7. Resources → Archives (cite-only)

Harvest emits **taxonomy rows** (coverage gate) plus **supplement** pin-nouns (`supplement: true`, optional `maps_to`). Summaries include feedstock excerpts when detect hits. Prefer phenomenology cards over architecture pins when both match.

## Operator gate

1. Harvest → `MINT-BACKLOG.md` + `.yaml` (`proposed`)
2. Prune in Obsidian → `frozen_for_mint`
3. Grok walks `pending` nouns
4. Friction check before `done`

If still thin after A+B+C harvest, run a Grok deepen pass (action D) before freeze.
