---
title: Series altitude exemplars (pack-authoring targets)
---

# Series altitude exemplars

**Authority:** cite-only for authors of `UX-MINT-SERIES` packs. **Not** the mine output contract and not catalog law.

## Altitude ladder

| Altitude | Allowed as `walk_tier: series`? | Example |
|----------|----------------------------------|---------|
| `product_contract` | **Yes** | Combat can resolve by authored non-win paths |
| `experience_texture` | No → thickener / L5 | How fear feels in the quiet after a roll |
| `scene_exemplar` | No → thickener / skin note | Empty-chair fracture after a specific CR death |

## Good pack member shape (product_contract)

```yaml
- role_key: world_generation
  label: Table can generate or import a persistent living world
  summary: >
    World is the durable container — multiple campaigns and character sets can
    share it over time.
  altitude: product_contract
  seat: [shared_table, dm_as_player, privileged_access]
  does_not_mandate:
    - one world equals exactly one campaign forever
    - worldgen is only a Session 0 checkbox with no persistent container
```

```yaml
- role_key: combat_play_surface
  label: Combat can resolve by authored paths including non-win ends
  summary: >
    Combat authorship menu (fight, flee, parley, stakes) as product contract —
    not one flee-or-die caption.
  altitude: product_contract
  seat: [shared_table]
  does_not_mandate:
    - flee is the only correct authored end
    - combat always resolves to XP loot chrome
```

## Good DM-facing member (privilege + player fun)

```yaml
- role_key: dm_session_prep
  label: DM can prep a session without leaving the collaborative table frame
  summary: >
    Session prep reduces orchestrator cognitive load as a player experience —
    privileged tools, not invisible infrastructure.
  altitude: product_contract
  seat: [dm_as_player, privileged_access]
  does_not_mandate:
    - prep must be a separate offline app
```

## Bad → demote (scene_exemplar)

```yaml
# DO NOT put in series packs as a parent:
- role_key: empty_chair_fracture
  label: Empty-chair fracture
  summary: Party feels the missing seat after a specific death beat.
  altitude: scene_exemplar   # thickener / skin under living_world_continuity or mid_game
```

## Verb/state preference

Prefer: “party membership can change by exit (not only death)”  
Avoid as parent: “campfire identity chrome” (chrome is child/surface under a contract).
