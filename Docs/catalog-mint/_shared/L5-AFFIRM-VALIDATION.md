---
title: L5 affirm validation (receipt)
audience: grok_github_integration
updated: 2026-08-07
---

# L5 affirm validation

**After Pass B lock + pin confirm/waive + inspiration seasoning apply/waive** — Pass-B **+ Conceptual pin** (+ seasoning) L5 projection review. Same receipt discipline as Pass B children. **Not** a second mint harvest, not pin derive, and **not** Operator Loop 2 (depth slicer → level validate).

**Frame:** [[CATALOG-MINI-TRINITY]] ladder v4. Never draft/affirm L5 before pin confirm/waive. **Series L5 before children L5** for that parent. **Children L5 = all Pass B children**, batched under parent; inherit series pins + series L5 (promote-to-planned skipped for now). Seasoning may cite inspiration/AP move-pins — never treat game titles as Conceptual pins.

## Failure modes (catch quickly)

1. **Pass-B drift** — L5 ignores locked SERIES / BATCH-DIGEST / WALK contract  
2. **Missing Conceptual lens** — unresolved `needs_pin` without waive, or pin ignored in Source anchors  
3. **Missing play-verbs** — thin parents without moment inventory (seat / trigger / response / refusal / residue)  
4. **Pack-content bleed** — class/spell/monster/merchant lists inside L5  
5. **PoC = full vision** — first cut not honestly smaller  
6. **Backend-only framing** — services/registries without observable player/DM moments  

## Velocity rules

- **Digest-first.** Open `L5-AFFIRM-STATUS.md` + per-row `L5-AFFIRM-DIGEST.md`. Open full `scopes/<row>/L5.md` only for yellow / red / thin ids.
- **One receipt per affirm turn.** Do **not** walk all full L5s.
- **Max ~5 highest-signal issues.**
- **Yellow vs red:** Missing polish = **yellow**. Unresolved `needs_pin` without waive / Pass-B drift / missing moments on thin parents / pack-smell = **red**.
- **Cross-row:** After digests green, operator fills **Cross-row flags (max 3)** on STATUS before attest — Grok may suggest up to 3; do not invent a symphony gate.

## Mandatory receipt shape

```text
## L5 affirm validation — <project_id>
Batch scope: [all planned / listed row ids]

### Pass / Fail summary
- N green
- M needs re-scope (**red** — list ids + one-line reason)
- K thin / needs grounding (list ids)
- P yellow (polish — list ids)

### Dual-rail / Pass-B / pin check
- L5s still project locked SERIES contracts? Y/N + drift
- Conceptual pins present (or waived) and used as lens? Y/N
- Thin parents have ≥ floor moments? Y/N

### Highest-signal issues (max 5)
1. …
2. …

### Cross-row flags (suggest ≤3; operator owns STATUS)
1. …
2. …
3. …

### Recommended next action
- Operator attest / re-draft subset / return to pin derive / etc.
```

## Operator close

- **Green (series + children family)** → fill cross-row flags → family attest → **Operator Loop 2** (depth slice → Grok+user validate levels) → then `catalog_signed_at`  

- **Yellow / red** → Cursor re-draft flagged rows (`force_overwrite`) → re-emit digests → re-validate subset  
- **Do not** treat “L5 files exist” as ready
