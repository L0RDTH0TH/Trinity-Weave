---
title: L5 affirm validation (Loop 2 receipt)
audience: grok_github_integration
updated: 2026-08-03
---

# L5 affirm validation (Loop 2)

**First-class Loop 2 MO** — Pass-B-aligned L5 projection review. Same receipt discipline as Pass B children. **Not** a second mint harvest and not a full L5 walk.

## Failure modes (catch quickly)

1. **Pass-B drift** — L5 ignores locked SERIES / BATCH-DIGEST / WALK contract  
2. **Missing play-verbs** — thin parents without moment inventory (seat / trigger / response / refusal / residue)  
3. **Pack-content bleed** — class/spell/monster/merchant lists inside L5  
4. **PoC = full vision** — first cut not honestly smaller  
5. **Backend-only framing** — services/registries without observable player/DM moments  

## Velocity rules

- **Digest-first.** Open `L5-AFFIRM-STATUS.md` + per-row `L5-AFFIRM-DIGEST.md`. Open full `scopes/<row>/L5.md` only for yellow / red / thin ids.
- **One receipt per affirm turn.** Do **not** walk all full L5s.
- **Max ~5 highest-signal issues.**
- **Yellow vs red:** Missing polish / soft `needs_pin` = **yellow**. Pass-B drift / missing moments on thin parents / pack-smell = **red**.
- **Cross-row:** After digests green, operator fills **Cross-row flags (max 3)** on STATUS before attest — Grok may suggest up to 3; do not invent a symphony gate.

## Mandatory receipt shape

```text
## L5 affirm validation — <project_id>
Batch scope: [all planned / listed row ids]

### Pass / Fail summary
- N green
- M needs re-scope (**red** — list ids + one-line reason)
- K thin / needs grounding (list ids)
- P yellow (needs_pin / polish — list ids)

### Dual-rail / Pass-B check
- L5s still project locked SERIES contracts? Y/N + drift
- Thin parents have ≥ floor moments? Y/N

### Highest-signal issues (max 5)
1. …
2. …

### Cross-row flags (suggest ≤3; operator owns STATUS)
1. …
2. …
3. …

### Recommended next action
- Operator attest / re-draft subset / resolve needs_pin before sign / etc.
```

## Operator close

- **Green** → fill cross-row flags → attest → only then depth-slice / `catalog_signed_at`  
- **Yellow / red** → Cursor re-draft flagged rows (`force_overwrite`) → re-emit digests → re-validate subset  
- **Do not** treat “L5 files exist” as Loop 2 ready
