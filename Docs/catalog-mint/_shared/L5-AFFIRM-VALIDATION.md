---
title: L5 affirm validation (receipt)
audience: grok_github_integration
updated: 2026-08-04
---

# L5 affirm validation

**After pin confirm/waive** — Pass-B **+ Conceptual pin** L5 projection review. Same receipt discipline as Pass B children. **Not** a second mint harvest, not pin derive, and **not** Operator Loop 2 (depth slicer).

**Frame:** [[CATALOG-MINI-TRINITY]] — Grok ladder step 4 (after Pass A, Pass B, pin derive). Never affirm series L5 before Pass B children are locked. Never draft/affirm L5 before pin confirm/waive. Child L5 affirm only if that child is a **planned** catalog row.

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

- **Green** → fill cross-row flags → attest → only then depth-slice / `catalog_signed_at` (Operator Loop 2)  
- **Yellow / red** → Cursor re-draft flagged rows (`force_overwrite`) → re-emit digests → re-validate subset  
- **Do not** treat “L5 files exist” as ready
