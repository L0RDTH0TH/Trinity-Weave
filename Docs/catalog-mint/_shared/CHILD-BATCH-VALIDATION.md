---
title: Child batch validation (Pass B receipt)
audience: grok_github_integration
updated: 2026-08-07
---

# Child batch validation (Pass B)

Same-width **peer review under one parent** — not a second series walk and not ad-hoc “does this look ok?” chat.

**Ladder v4 precondition:** Conceptual `apply_pins` done **and** inspiration seasoning apply **or** explicit waive ([[INSPIRATION-SEASONING-VALIDATION]]). Children Meaning is lensed by series + Conceptual + seasoning (+ AP).

## Failure modes (catch quickly)

1. **Altitude bleed** — child still reads like a series parent or an AP skin  
2. **Anti-mandate failure** — one plot / structure elevated as product law  
3. **Lens / dual-rail drift** — child no longer sits cleanly under the locked parent (or DM seat / agency envelope is broken)

## Velocity rules

- **Batch, not item-by-item.** One structured receipt per active parent.
- **Receipt-first.** Primary artifacts: rewritten `summary` + **local** `alternatives_not_banned` (and any true local `does_not_mandate` deltas). Parent anti-mandate is inherited via `inherits_parent_anti_mandate` — do not re-litigate it on the child. Notes / feedstock stay secondary.
- **Digest-first.** Open `CHILD-BATCH-STATUS.md` + `scopes/<parent>/BATCH-DIGEST.md`. Open full `WALK.md` only for yellow / red / thin ids.
- **Yellow vs red:** Missing local alternatives = **yellow** (polish). Altitude bleed / dual-rail drift / anti-mandate failure as product plot = **red** (re-scope).
- **Selective grounding.** Pull `ROADMAP-RESOURCE-INDEX.yaml` or ask fulfill/`tert_id` only when a child is thin or contested.
- **Friction once per batch** (or per contested child if flagged) — see [[FRICTION-CHECK]].
- **Same-width only.** Stay on `active_child_batch` until lock. Do not jump to the next queued parent.
- **Reuse locked parent language.** Children inherit parent altitude / anti-mandate; they must not re-litigate it. Cursor drafts local alternatives; Grok polishes.

## Mandatory receipt shape

Return **one** receipt (not a per-child essay):

```text
## Batch validation — <parent_id>
Parent series altitude / contract: [1–2 lines]

### Pass / Fail summary
- N green
- M needs re-scope (**red** — list ids + one-line reason)
- K thin / needs grounding (list ids)
- P missing local alternatives (**yellow** — polish; not altitude failure)

### Dual-rail / lens check
- All children still under parent contract? Y/N + any drift
- DM seat / agency envelope intact? Y/N

### Highest-signal issues (max 5)
1. …
2. …

### Recommended next action
- Lock batch / re-mine subset / pull specific roadmap notes / etc.
```

## Operator close

- **Green** → bone pilot `lock_child_batch` → pack emit → Trinity weave publish → `publish_children` (record SHA).  
- **Yellow / red** → re-scope flagged children only; re-validate the changed subset.  
- **Thin** → fulfill or poll-index pull for those ids only.
