---
title: Pin derive validation (Conceptual weld receipt)
audience: grok_github_integration
updated: 2026-08-04
---

# Pin derive validation

**First-class pin-before-L5 MO** — after Pass B lock, before L5. Same receipt discipline as Pass B / L5 affirm. **Not** inventing Conceptual notes and **not** L5 authoring.

**Frame:** [[CATALOG-MINI-TRINITY]] — Grok ladder step 3 (after Pass A + Pass B). Live premature `L5.md` must be archived; pin derive must not lean on Pass-B-only L5 prose.

**Join:** Catalog row = `conceptual_pin_refs[]` (why this shape) → `execution_pins[]` (how it builds) → L5 (vision bar).

## Weld contracts

1. **Excerpt = weld; heading = locator.** Pack `PIN-EXCERPTS` text is what licensed the UX claim for this derive. Heading locates the span in the vault; renames later are drift signals, not silent rewrites of the weld.
2. **Same-span visibility.** Cursor and Grok must see the **same** excerpt text. Missing/empty excerpt when a heading is claimed = **red** (process bug). Soft warn (not hard-fail v1) when excerpt ≳ ~1200 chars — prefer paragraph / short subsection.
3. **Grok ≠ highlight UI.** Highlightr marks live in the vault parent for operator nav/drift. Grok grounds on **pack plain excerpts** + project branch — do **not** expect Grok to parse `<mark>` markup.
4. **≥1 `role: primary` ref** per row. Supporting/contrast optional. “All supporting” = yellow/red.
5. **Structure vs consequence.** Pin enabling Conceptual **machinery**; band/role/prep deltas as headings or amendments — do not invent parallel Phase parents that fight the frozen map.
6. **Freeze.** Write-block on frozen parent prose. Amendments = create path under `Conceptual-Amendments/<relative-parent-path>/`. Highlightr wrap-only marks = annotation carve-out (no wording rewrite).

## Failure modes (catch quickly)

1. **Invented title** — recommended pin / ref title not in `PIN-INDEX.md`  
2. **Wrong altitude / seat** — pin owns Execution chrome or a sibling UX series, not this Conceptual prose  
3. **World ≠ campaign collapse** — worldgen pin used for campaign bootstrap (or reverse)  
4. **Overclaim** — whole Phase claimed when only a slice licenses the contract (`pin_focus` / `excerpt_note` dishonest)  
5. **Cross-row collision** — identical primary span without distinct `excerpt_note` / supporting refs  
6. **Missing primary** — no `role: primary`  
7. **Visibility fail** — heading set but PIN-EXCERPT missing/empty  
8. **Proxy green** — forced fit when honest span missing (should be yellow + Grok mint gate)

## Grok mint_target gate (volume)

Cursor may leave **sparse** `mint_target` hints. **Grok owns volume:**

- If yellow because pins are weak: read roadmap (project branch + PIN-EXCERPTS / PIN-INDEX) and output **pass-this-to-Cursor** pin locations (title + heading + role + why).
- If no honest location: propose **few** high-signal where-targets (parent + section intent / `path_class: child|amendment`) — not a parallel missing-note map.
- Cursor updates → republish pack → Grok revalidates with User.
- **Loop cap:** at most **one** Cursor re-derive pass after Grok’s first pass-to-Cursor / propose; then operator **confirm / waive / mint_target**.

## Velocity rules

- **Digest-first.** Open `PIN-DERIVE-STATUS.md` + per-row `scopes/<row>/PIN-DERIVE.md` + matching `PIN-EXCERPTS/`. Open full Conceptual bodies only for yellow/red/contested ids (project branch or fulfill).
- **One receipt per pin-derive turn.**
- **Max ~5 highest-signal issues.**
- **Yellow vs red:** Prefer alternate / sharpen refs / Grok gate = **yellow**. Invented title / world≠campaign / wrong seat / empty excerpt with heading / no primary = **red**.
- **Legal pins only** from `PIN-INDEX.md` (prefer `*Roadmap*` over `*Roll-up*`; ignore `.pre-*` hygiene copies).

## Mandatory receipt shape

```text
## Pin derive validation — <project_id>
Batch scope: [all planned / listed row ids]
Schema: pin v2 (conceptual_pin_refs + PIN-EXCERPTS)

### Pass / Fail summary
- N green (primary span licenses UX)
- M needs re-derive (**red** — list ids + one-line reason)
- K thin / needs grounding (list ids)
- P yellow (prefer alt / sharpen refs / mint gate — list ids)

### Cross-row check
- World ≠ campaign pins distinct? Y/N
- Dual-rail seats (camera / table agency) not collapsed? Y/N
- Shared parents have distinct excerpt_note / supporting refs? Y/N
- Same-span excerpts present for claimed headings? Y/N

### Highest-signal issues (max 5)
1. …

### Pass-to-Cursor (if yellow weak pins)
- row_id → title + heading + role + why
- or mint_target propose (few): parent + section intent + path_class

### Recommended next action
- Operator confirm/waive → apply_pins (outside derive) / one re-derive / etc.
```

## Operator close

- **Green / yellow polish** → operator confirms or waives per row → `apply_pins` (follow-on) → only then L5 mint  
- **Red** → Cursor re-derive flagged rows (within loop cap) → re-emit STATUS + excerpts → re-validate subset  
- **Do not** draft L5 while pins remain unresolved without an explicit waive
