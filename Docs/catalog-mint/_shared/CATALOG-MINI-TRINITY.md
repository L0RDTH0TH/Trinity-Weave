---
title: Catalog Mini-Trinity (first-class MO)
audience: cursor_grok_operator
updated: 2026-08-04
---

# Catalog Mini-Trinity (first-class MO)

Each **planned** catalog row is a **mini project trinity**: flood the LLM from three angles, keep collisions traceable. This is **catalog law** — not a side mode and not a second mint for L5 children.

**Join key:** Catalog row = `conceptual_pin_refs[]` (why this shape) → `execution_pins[]` (how it builds) → L5 (vision bar). Agents must not invent “why X over Y” outside cited refs + CDR alternatives.

## Seats (per planned row)

| Seat | Artifact | Question |
|------|----------|----------|
| **Conceptual** | `conceptual_pin` + `conceptual_pin_refs[]` → roadmap / CDR / amendments | What is this in plain prose (which span)? |
| **UX (touch)** | Pass A `SERIES.md` + Pass B `WALK.md` / `BATCH-DIGEST.md` | How does it feel in player/DM hands? |
| **Execution** | `execution_pins[]` → Execution roadmap notes | How is that touch built (pseudo-code / interfaces / ACs)? |

**L5** (`scopes/<row>/L5.md`) is the **UX → factory bridge**: Pass-B **+ Conceptual pin** complete vision bar. It is **not** a fourth pillar and **not** a substitute for SERIES/WALK touch.

**Anti-mandates + alternatives** are **rails across all seats**. They are **not** the third trinity seat — Execution is.

## Operator ladder (v3)

1. Conceptual feed ready → freeze  
2. **Pass A** — series Meaning (what-is)  
3. Trinity publish series  
4. **Inspiration UX dialogue** (first-class) — Grok+user: pinable game/tool list + liked snippets → **pattern** derived move-pins until satisfied → write `INSPIRATION-DIALOGUE-RECEIPT.md` → Cursor may auto-elevate into children/L5 **seasoning only** with assumption trace (see [[INSPIRATION-UX-FEEDSTOCK]])  
5. **Pass B** — children Meaning (batches), seasoned by inspiration + Actual-Play derived pins  
6. **Archive any premature L5** (conditional — only if live L5 exists before Conceptual pins)  
7. **Pin derive v2** — Cursor first emit (shared-primary heuristic) + PIN-EXCERPTS → Grok validate → pass-to-Cursor (loop cap 1) if needed → sparse `mint_target` if no honest span  
8. **Mint funnel (before L5):** dual-approved `mint_target` (Cursor + operator) → write Conceptual-Amendment → Highlightr carve-out → PIN-INDEX → re-pin → excerpts → Trinity → **Grok subset that row only** — **no waive-as-proxy** for approved targets  
9. Operator **board confirm** all rows → **`apply_pins`** (clears `mint_target`)  
10. **Series L5** draft/affirm — Pass-B + resolved pin + inspiration/AP seasoning (shapes children)  
11. **Children L5** — **all** Pass B children, batched under each parent, **after** series L5; inherit series `conceptual_pin_refs` + series L5 (no per-child pin derive by default; promote-to-planned skipped for now)  
12. Family attest (series + children digests green; operator cross-row flags)  
13. **Operator Loop 2** — **only** depth slicer → Grok + user validate levels — **not** L5 definition; do not require L1 files before the slicer runs  
14. Operator sets `catalog_signed_at`  
15. Loop 3 / Execution deepen — `execution_pins[]` fill as deepen **references/mints** notes; do not invent outside L5  

**Confirmed mint_targets mint before L5** because Conceptual feedstock serves **L5 and Execution**.

## Grok validation ladder (content only)

```text
1. Pass A — series individually
2. Inspiration dialogue — patterns from pinable sources (until user satisfied + receipt)
3. Pass B — children summaries batched
4. Pin derive — batched; after amendment mint → subset = that row only
5. Series L5 affirm — only after pins confirmed (and approved mints written)
6. Children L5 affirm — batched under parent after series L5
```

| Forbidden | Why |
|-----------|-----|
| L5 before pin confirm / before approved mint written | Conceptual lens missing |
| Children L5 before series L5 for that parent | Series shapes children |
| Waive-as-proxy after mint_target dual-approved | Must mint the file |
| Re-walking greens after single-row amendment | Subset = that row only |
| Speculative amendment walls | Grok volume + dual gate |
| Calling L5 “Operator Loop 2” | Loop 2 = depth slice + level validate only |

## Gate split

| Who | Job |
|-----|-----|
| Cursor | Structure; first-emit heuristic; accept/refine/reject `mint_target` (`reject_reason` if reject); PIN-EXCERPTS |
| Grok | Content; mint_target volume; post-mint **single-row** subset |
| Operator | Approve mint; board confirm; terminate loops |

## Anti-patterns

- L5 against proxy when an approved `mint_target` sits unminted  
- Leaving `mint_target` looking “proposed” after the file exists (set `minted: true` + path; clear at `apply_pins`)  
- Cursor flooding speculative `mint_target` walls  

## Cross-links

- [[WHAT-GOOD-LOOKS-LIKE]] · [[PIN-DERIVE-VALIDATION]] · [[L5-AFFIRM-VALIDATION]] · [[CHILD-BATCH-VALIDATION]] · [[INSPIRATION-UX-FEEDSTOCK]]  
- [[3-Resources/Second-Brain/Docs/Slice-Catalog-and-Slicer]] · [[3-Resources/Second-Brain/Docs/Dual-Roadmap-Track]]
