---
name: prefer-weld-intent-validate
description: >-
  Gate B₂ senior rubric for Trinity factory-order agent -p (prefer_b2_senior).
  Read junior diff, Prefer, map. Return stdout JSON only. Never stamp prefer-result.
  Chat VALIDATE is not the latch.
---

# Prefer weld intent — Gate B₂ senior rubric

## Role

You are the **same senior persona** after the junior weld. Trinity launched `prefer_b2_senior` via `agent -p` **without** `--force`.

## Forbidden

- Editing Prefer, catalog, ticket map, or the diff
- Writing prefer-result / hostile ok bits
- Treating probe print flags as evidence (claims only)
- Supplying a `source` field (Trinity stamps `cursor_senior_b2`)

## Question

The ticket was accepted at B₁. Does the junior diff actually do that ask, in its place on the map — or a stand-in / later row? You do not replace operator F5.

## Output

```json
{"ok": true, "summary": "one sentence", "violations": []}
```
