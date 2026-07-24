# UX mint rubric (cross-project)

Law for `MINT-BACKLOG.yaml` harvest after conceptual freeze. Enforced in `ux_mint_backlog.py`.

## Purpose

Catalog mint walks **player/DM experience nouns** — how the product *feels* and *flows* — not backend phases or stack domains.

## Required `ux_axis` set

Every backlog (unless operator waives an axis in `waived_axes`) must cover:

| Axis | Experience focus |
|------|------------------|
| `perspective_overrides` | Scry / Clairvoyance / FP presentation feel |
| `agency` | Player authorship loops |
| `dm_player_rails` | Shared DM/player session chrome and flow |
| `class_chrome` | Class/subclass visible identity polish |
| `combat_cast_feedback` | Cast/hit sensory feedback (not damage formulas) |
| `session0_identity_art` | Session 0 rituals, art direction, palette |

Supporting (optional, never the whole list): `presentation_shells`.

## Include / exclude

**Include:** Scry presentation, class chrome, booming-blade *feedback*, art direction, rail feel.  
**Exclude:** Phase titles as rows, stack domain ids, pure damage/rules resolution, factory chores. Spell *families* may be one noun — not one row per SRD spell.

## Entry fields

`id`, `label`, `dimension`, `ux_axis`, `summary`, `conceptual_pin`, `derived_from` (pin path or `pmg:…`), optional `ux_family`, `status` (`pending` \| `in_dialogue` \| `done` \| `dropped`).

## Operator gate

1. Harvest writes `backlog_status: proposed`
2. Bone pilot prunes → `frozen_for_mint`
3. Grok walks next `pending` only when frozen (or operator names an id)
4. After apply: friction check — “Does this stub reduce imagined friction for [persona]?” before `done`

## Pack

See `MINT-PACK.md` **Walk Order**. Mirror: `Docs/catalog-mint/<project_id>/MINT-BACKLOG.yaml`.
