---
title: Pin derive validation (Conceptual weld receipt)
audience: grok_github_integration
updated: 2026-08-04
---

# Pin derive validation

**First-class pin-before-L5 MO (v3)** — after Pass B lock, before L5. Same receipt discipline as Pass B / L5 affirm.

**Frame:** [[CATALOG-MINI-TRINITY]]. **Join:** `conceptual_pin_refs[]` → `execution_pins[]` → L5.

## Weld contracts

1. **Excerpt = weld; heading = locator.**  
2. **Same-span visibility** — empty excerpt when heading claimed = **red**. Soft warn ≳ ~1200 chars.  
3. **Grok ≠ highlight UI** — pack plain excerpts only.  
4. **≥1 `role: primary`.**  
5. **Structure vs consequence** — no invented Phase parents; amendments under `Conceptual-Amendments/<relative-parent-path>/`.  
6. **Freeze** write-block; Highlightr wrap-only carve-out.  
7. **First-emit heuristic:** If **≥2** planned series recommend the **same PIN-INDEX title as primary** on first emit, force either **distinct primary spans** or **demote** the shared title to supporting and pick consequence primaries.  
8. **Post-mint Grok subset** defaults to **that row only** (not the whole yellow set).

## Mint funnel (before L5)

1. Grok sparse `mint_target` when no honest span (volume gate — few, high-signal).  
2. **Cursor gate:** accept / refine / reject. Reject requires one-line **`reject_reason`** on the card so the same `proposed_title` is not re-proposed.  
3. **Operator gate:** approve mint. **No waive-as-proxy** after dual approval — write the file.  
4. Write amendment → Highlightr on parent → PIN-INDEX → re-pin → PIN-EXCERPTS → Trinity → Grok **single-row** subset.  
5. On write: set `mint_target.minted: true` and `mint_target.path` (propose must not look still-open). Clear `mint_target` at **`apply_pins`**.

## Failure modes

Invented title · wrong seat · world≠campaign · overclaim · identical primary weld without distinct spans · missing primary · empty excerpt · proxy green when mint_target should fire · re-proposing a rejected title without new reason.

## Grok mint_target gate (volume)

- Yellow + locations exist → **pass-to-Cursor** (loop cap **one**).  
- Yellow + no honest span → sparse `mint_target`.  
- After amendment mint → subset reval **that row only**.

## Velocity rules

Digest-first · one receipt per turn · max ~5 issues · legal titles from PIN-INDEX only.

## Mandatory receipt shape

```text
## Pin derive validation — <project_id>
Batch scope: [all planned | subset: <row_id>]
Schema: pin v3 (refs + PIN-EXCERPTS + mint funnel)

### Pass / Fail summary
…

### Pass-to-Cursor / mint_target
…

### Recommended next action
- Dual-approve mint → write amendment → single-row reval / board confirm → apply_pins → L5
```

## Operator close

- Board confirm → `apply_pins` (clears minted `mint_target`) → L5  
- Do **not** draft L5 while approved mint_targets remain unminted
