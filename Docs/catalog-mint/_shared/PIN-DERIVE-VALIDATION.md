---
title: Pin derive validation (Conceptual weld receipt)
audience: grok_github_integration
updated: 2026-08-04
---

# Pin derive validation

**First-class pin-before-L5 MO** — after Pass B lock, before L5. Same receipt discipline as Pass B / L5 affirm. **Not** inventing Conceptual notes and **not** L5 authoring.

**Frame:** [[CATALOG-MINI-TRINITY]] — Grok ladder step 3 (after Pass A + Pass B). Live premature `L5.md` must be archived; pin derive must not lean on Pass-B-only L5 prose.

## Failure modes (catch quickly)

1. **Invented title** — recommended pin not in `PIN-INDEX.md`  
2. **Wrong altitude / seat** — pin owns Execution chrome or a sibling UX series, not this Conceptual prose  
3. **World ≠ campaign collapse** — worldgen pin used for campaign bootstrap (or reverse)  
4. **Overclaim** — one Phase note claimed as the whole product when it only covers a slice (`pin_focus` missing or dishonest)  
5. **Cross-row collision** — two series recommend the identical pin without distinct `pin_focus`

## Velocity rules

- **Digest-first.** Open `PIN-DERIVE-STATUS.md` + per-row `scopes/<row>/PIN-DERIVE.md`. Open full Conceptual roadmap bodies only for yellow/red/contested ids (project branch or fulfill).
- **One receipt per pin-derive turn.** Do **not** walk all 130 PIN-INDEX notes.
- **Max ~5 highest-signal issues.**
- **Yellow vs red:** Weak `pin_focus` / prefer alternate candidate = **yellow**. Invented title / world≠campaign collapse / wrong seat = **red**.
- **Legal pins only** from `PIN-INDEX.md` (prefer `*Roadmap*` over `*Roll-up*`; ignore `.pre-*` hygiene copies).

## Mandatory receipt shape

```text
## Pin derive validation — <project_id>
Batch scope: [all planned / listed row ids]

### Pass / Fail summary
- N green (recommended pin fit)
- M needs re-derive (**red** — list ids + one-line reason)
- K thin / needs grounding (list ids)
- P yellow (prefer alt / sharpen pin_focus — list ids)

### Cross-row check
- World ≠ campaign pins distinct? Y/N
- Dual-rail seats (camera / table agency) not collapsed? Y/N
- Duplicate recommended pins have distinct pin_focus? Y/N

### Highest-signal issues (max 5)
1. …
2. …

### Recommended next action
- Operator confirm/waive → apply_pins (outside derive) / re-derive subset / etc.
```

## Operator close

- **Green / yellow polish** → operator confirms or waives per row → `apply_pins` (follow-on) → only then L5 mint  
- **Red** → Cursor re-derive flagged rows → re-emit STATUS → re-validate subset  
- **Do not** draft L5 while pins remain unresolved without an explicit waive
