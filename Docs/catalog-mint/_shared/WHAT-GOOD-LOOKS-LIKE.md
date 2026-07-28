# What a “good” catalog mint looks like

## Two different artifacts

| Artifact | When | Who writes | Purpose |
|----------|------|------------|---------|
| **Catalog row** (YAML in `slice-catalog.yaml`) | After you settle the dialogue | Cursor applies | Stable **id + pin + deps** handle for factory later |
| **L5 scope** (`scopes/<id>/L5.md`) | After row exists + Loop 2 appetite | Mostly Grok prose with you, Cursor files it | Full vision / PoC cuts / REQ language — **not code** |

Mint chat is for **negotiating meaning**. The YAML is a **receipt**, not the conversation.

## What “good” mint prose covers (before you say approve)

1. **What it is** — player/DM-visible deliverable in plain English (from PMG + pin).
2. **Why this pin** — which Roadmap note owns it; what nearby notes are *not* this row.
3. **Full vision (L5 direction)** — largest honest “done” (bullets OK).
4. **PoC / early depth cut** — what you would **omit** first without lying (same shape as: full rules include ½/¾ cover; L1 omits them because nothing else depends on them yet).
5. **Hard dependencies** — “cannot validate X until Y exists” (same shape as: cover before AC is nonsense).
6. **Out of scope** — explicit exclusions so the row doesn’t swallow the product.
7. **Alternatives this does *not* ban** — legitimate sibling structures that stay first-class (e.g. regular tavern alongside captivity; win/parley alongside flee). If you cannot name any, the row is probably an exemplar-mandate — re-scope.
8. **Open questions** — 2–4 choices for you; Grok does not invent code or harness steps.
9. **Draft YAML** — only after the above, as a candidate receipt.

### Smell language (stop and re-scope)

Treat these as red flags that the draft is minting a **default story** instead of a product surface:

- “the game begins by…”, “first session teaches…”, “must start…”
- “the only correct ending is…”, “exploration *is* jailbreak” (as product law)
- Twisting every warm open into a secret prison / soft constraint
- One CR/BG episode caption with no reusable structure menu

**Exemplar ≠ product default.** Actual-Play cards prove a *feel* can exist; they do not require every campaign to use that skin.

## What a good *row* looks like (YAML)

Minimal, stable nouns — not essays:

```yaml
  - id: player_fp_perspective_envelope   # deliverable noun
    dimension: ui_surface                  # one bucket
    label: Player FP perspective envelope  # human name
    planned: true
    mint_status: proposed
    conceptual_pin: "[[Phase-4-1-…-Roadmap-…]]"  # from PIN-INDEX only
    execution_pins: []                     # empty until execution track
    depends_on: []                         # other row ids once they exist; else note in prose
    touchstone_refs: []
```

A “good” first entry is **narrow enough to debate**, pinned to a real note, with deps/out-of-scope settled in chat. It is **not** a full L5 document stuffed into YAML. Narrow ≠ “one mandatory campaign plot.” Prefer **structure menus** and **capability contracts** over single-skin story nouns.

## Historical note

Older remint rows carried extra factory fields (`l5_path`, attestation gates, …). Greenfield mint starts **simple**. Depth and L5 prose come after the row is approved.
