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

**L5** (`scopes/<row>/L5.md`) is the **UX → factory bridge**: Pass-B **+ Conceptual pin** complete vision bar (moments, PoC, hard deps, out of scope). It is **not** a fourth pillar and **not** a substitute for SERIES/WALK touch.

**Anti-mandates + alternatives** are **rails across all seats** (structure menus; exemplar ≠ product default). They are **not** the third trinity seat — Execution is.

## Operator ladder

1. Conceptual feed ready → freeze  
2. **Pass A** — series Meaning  
3. Trinity publish series → **Pass B** — children Meaning (batches)  
4. **Archive any premature L5** (fresh path has no L5 yet at pin time; live Pass-B-only L5s poison pin-before-L5)  
5. **Pin derive v2** — Cursor proposes PIN-INDEX titles + `conceptual_pin_refs` + pack **PIN-EXCERPTS** → Grok validate (judgment on same text) → Grok mint gate if yellow → operator confirm/waive  
6. **L5 draft** — Pass-B + resolved pin (or recorded waive); structure gate → Grok content affirm → cross-row flags → attest  
7. `catalog_signed_at` only when board attest allows  
8. **Operator Loop 2** — depth-slice / budget / scope levels (L5 → L4…L1) — **not** the L5 definition step  
9. Loop 3 / Execution deepen with `ux_context` — do not invent outside L5  

**Children Meaning ≠ child L5 batches.** Children thicken touch under a series. A child gets its own L5 only when promoted to a **planned** catalog row.

**Independence example:** worldgen can reach depth 5 with only minimal camera (e.g. DM WorldCam) while full FP envelopes stay deferred in camera PoC / budget.

## Grok validation ladder (content only)

Grok validates the **published Trinity pack**. Cursor drafts **ahead** of Grok turns (not gen-as-validate). Stale pack → refuse and ask for Trinity republish — do not invent feedstock.

```text
1. Pass A — series individually (one SERIES / turn; full Meaning receipt)
2. Pass B — children summaries batched (one parent / turn; BATCH-DIGEST first; full WALK only yellow/red/thin)
3. Pin derive — planned-row pin proposals batched (PIN-DERIVE-STATUS + per-row PIN-DERIVE + PIN-EXCERPTS; digest-first)
4. L5 affirm — planned-row L5s batched (only after pins confirmed/waived; L5-AFFIRM-STATUS + digests)
```

| Forbidden | Why |
|-----------|-----|
| Series L5 **before** Pass B children lock | L5 is Pass-B projection |
| L5 draft/affirm **before** pin confirm/waive | Conceptual lens missing; premature L5 poisons the path |
| Mandatory **child L5** affirm batches | Only if that child is a planned row with an L5 |
| Walking all full L5s / pin notes every turn | Digest-first; one receipt per turn |
| Calling L5 affirm “Operator Loop 2” | Loop 2 = depth slicer / catalog levels |
| Forcing a green proxy when no honest span exists | Use Grok mint gate / `mint_target` — not invented parents |

Receipt shapes: series Meaning (Pass A) · [`CHILD-BATCH-VALIDATION`](CHILD-BATCH-VALIDATION.md) · [`PIN-DERIVE-VALIDATION`](PIN-DERIVE-VALIDATION.md) · [`L5-AFFIRM-VALIDATION`](L5-AFFIRM-VALIDATION.md).

## Gate split

| Who | Job |
|-----|-----|
| Cursor (`l5_affirm` / pin derive emit) | Structure — pin legality, refs (≥1 primary), L5 sections, origin, moment *count*, pack-smell, anchors, PIN-EXCERPTS emit |
| Grok (this ladder) | Content — pin fit, altitude, anti-mandate, play-verbs, dual-rail, Pass-B drift; **mint_target volume gate** |
| Operator | Confirm/waive pins; cross-row symphony flags + sign; terminate re-derive loop |

## Anti-patterns

- Treating mint children as automatic L5 children  
- Treating L5 as the whole “touch” pillar (erases SERIES/WALK)  
- Treating anti-mandates as Execution  
- Keeping live L5s while deriving pins (poison for pin-before-L5)  
- Signing because “L5 files exist” without pin gate + Grok content affirm + attest  
- Coarse whole-note pins that force later rails to **guess** which prose licensed the UX  
- Cursor flooding speculative `mint_target` walls (Grok owns volume)  

## Cross-links

- [[WHAT-GOOD-LOOKS-LIKE]] · [[UX-MINT-RUBRIC]] · [[PIN-DERIVE-VALIDATION]] · [[L5-AFFIRM-VALIDATION]] · [[CHILD-BATCH-VALIDATION]]  
- [[3-Resources/Second-Brain/Docs/Slice-Catalog-and-Slicer]] · [[3-Resources/Second-Brain/Docs/Roadmap-Factory-Pipeline]] · [[3-Resources/Second-Brain/Docs/Dual-Roadmap-Track]]
