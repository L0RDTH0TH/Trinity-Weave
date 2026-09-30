---
title: PF1 Ruleset Content Scaffold (Execution) — genesis-mythos-master
created: 2026-09-29
tags: [execution, pf1, pathfinder, rules-content, junior-mandatory, genesis-mythos-master]
para-type: Project
project-id: genesis-mythos-master
roadmap_track: execution
status: active
ruleset_lock: pathfinder_pf1
cdr: Roadmap/Conceptual-Decision-Records/rules-base-pathfinder-pf1-2026-09-29.md
howto_ref: Roadmap/Execution/Docs/Junior-Tech-Adapt-How-To.md
host_index_ref: Roadmap/Execution/Docs/SeamRegistry-CSharp-Host-Index.md
---

# PF1 Ruleset Content Scaffold

**Purpose:** Close the hostile “F2 path named, tables absent” gap for Execution. Vault-side **junior-facing** table/slot scaffolding for first plugin id **`pathfinder_pf1`**. Game-repo files under `res://rules/pathfinder_pf1/` are minted from these shapes (Half B) — this note is the **content contract**, not Paizo text dump.

**Authority:** CDR [[../../Conceptual-Decision-Records/rules-base-pathfinder-pf1-2026-09-29|rules-base-pathfinder-pf1-2026-09-29]] · Recipes [[Junior-Tech-Adapt-How-To]] §3–4 · Host bind [[SeamRegistry-CSharp-Host-Index]] §B4.

**Not legal advice.** Fill cells only from operator-cleared open material / originals; strip Paizo trademarks and setting IP unless licensed.

---

## 0. Plugin host bind (must)

| Slot | Value |
|------|--------|
| `rules.plugin_id` / `RulesetPluginId` | `pathfinder_pf1` |
| Demo binder id (6.2.5) | `demo_ruleset_pf1` |
| Seam | `rules.plugin.core` **PUBLISHED** before `BindPlugin` |
| Dice | `IRulesPluginHost.Roll` → `IDiceRoller` only (DiceRoller MIT); **no** UI-direct rolls; **no** AGPL dice libs |
| ActiveRuleset default | `pathfinder_pf1` |
| Receipt (Exemplar) | `R.rules.pf1_bind` — ActiveRuleset == `pathfinder_pf1` ∧ Roll→`IDiceRoller` |

```csharp
// see Junior-Tech-Adapt-How-To §3–4 — normative signatures on Host Index §B4
_active = new RulesetPluginId("pathfinder_pf1");
host.BindPlugin(plugin); // Unavailable if seam unpublished
host.Roll(DiceExpression.Parse("1d20+3"), frame); // → IDiceRoller
```

---

## 1. Game-repo layout (F2 remint target)

```
res://rules/pathfinder_pf1/
  plugin_manifest.json          # id, version, table_index
  check_schema.json             # d20 check / opposed / save / attack
  tables/
    abilities.json              # Str Dex Con Int Wis Cha
    skills.json                 # skill_id, ability, trained_only, armor_check
    conditions.json             # condition_id → modifier bags
    bab_save_progressions.json  # BAB/save curves L1–20 + class slots (vault filled)
    spells_slots.json           # wizard/sorcerer/cleric slot matrices (vault L1–5+)
    spells_list.json            # spell-list scaffolding for 5.2.1 registry
  demo/
    demo_check_schema.json      # minimal 6.2.5 pass/fail probe
```

Vault mirror for junior copy-paste (same shapes): sections below. Prefer deepen Phase-5 / 5.1 / 5.2 / 5.2.1 — **do not invent 5.2.2+** for remint.

---

## 2. `plugin_manifest.json` (shape)

```json
{
  "plugin_id": "pathfinder_pf1",
  "edition": "pathfinder_1e",
  "display_name": "Pathfinder 1e (first plugin)",
  "check_schema": "check_schema.json",
  "tables": [
    "tables/abilities.json",
    "tables/skills.json",
    "tables/conditions.json",
    "tables/bab_save_progressions.json",
    "tables/spells_slots.json",
    "tables/spells_list.json"
  ],
  "demo_binder": "demo/demo_check_schema.json",
  "dice_host": "IDiceRoller",
  "notes": "Content pack only — host stays ruleset-agnostic"
}
```

---

## 3. `check_schema.json` — PF1 d20 surface

| Field | Type | Notes |
|-------|------|--------|
| `schema_id` | string | `pf1_check_v0` |
| `roll` | expression | default `1d20` via `IDiceRoller` |
| `modes` | enum | `check`, `save`, `attack`, `opposed`, `caster_level` |
| `modifiers[]` | `{source, value}` | ability, ranks, misc, circumstance, … |
| `dc` | int \| ref | fixed or table lookup |
| `success` | rule | `total >= dc` (no PF2e degree ladder as default) |
| `critical` | optional | nat 20 / nat 1 hooks — plugin-defined; host records audit only |

**Demo probe (6.2.5):** one `CheckRequest` with `mode=check`, `roll=1d20+mod`, `dc=10`, emit `rule_demo_pass` | `rule_demo_fail` → `demo_rule_check_complete`.

```json
{
  "schema_id": "pf1_check_v0",
  "plugin_id": "pathfinder_pf1",
  "default_roll": "1d20",
  "modes": ["check", "save", "attack", "opposed", "caster_level"],
  "success_rule": "total_gte_dc",
  "forbid_pf2e_degree_ladder_as_default": true
}
```

---

## 4. Table stubs (enough cells that F2 ≠ empty)

### 4.1 `abilities.json`

```json
{
  "plugin_id": "pathfinder_pf1",
  "abilities": [
    {"id": "str", "name": "Strength"},
    {"id": "dex", "name": "Dexterity"},
    {"id": "con", "name": "Constitution"},
    {"id": "int", "name": "Intelligence"},
    {"id": "wis", "name": "Wisdom"},
    {"id": "cha", "name": "Charisma"}
  ],
  "modifier_formula": "floor((score - 10) / 2)"
}
```

### 4.2 `skills.json` (starter set — expand in remint)

| skill_id | ability | trained_only |
|----------|---------|--------------|
| acrobatics | dex | false |
| climb | str | false |
| diplomacy | cha | false |
| knowledge_arcana | int | true |
| perception | wis | false |
| stealth | dex | false |
| spellcraft | int | true |
| use_magic_device | cha | true |

### 4.3 `conditions.json` (slot bag)

| condition_id | effect_slots (examples) |
|--------------|-------------------------|
| flat_footed | lose_dex_to_ac |
| fatigued | str_dex_penalty |
| shaken | fear_penalty |
| stunned | no_actions |
| invisible | stealth_bonus_bag |

Junior fills numeric bags from cleared sources; empty `modifiers: []` is allowed only with `status: stub_shape`.

### 4.4 `bab_save_progressions.json` — junior-usable BAB + saves (PF1)

**Curves (PF1 core math — fill from cleared sources; not Paizo prose):**

| Curve id | Formula (character level L = 1..20) |
|----------|--------------------------------------|
| `bab_full` | BAB = L |
| `bab_three_quarter` | BAB = floor(L × 3 / 4) |
| `bab_half` | BAB = floor(L / 2) |
| `save_good` | bonus = 2 + floor(L / 2) |
| `save_poor` | bonus = floor(L / 3) |

**Expanded 1–20 (copy into game-repo JSON):**

| L | bab_full | bab_3/4 | bab_half | save_good | save_poor |
|---|----------|---------|----------|-----------|-----------|
| 1 | 1 | 0 | 0 | 2 | 0 |
| 2 | 2 | 1 | 1 | 3 | 0 |
| 3 | 3 | 2 | 1 | 3 | 1 |
| 4 | 4 | 3 | 2 | 4 | 1 |
| 5 | 5 | 3 | 2 | 4 | 1 |
| 6 | 6 | 4 | 3 | 5 | 2 |
| 7 | 7 | 5 | 3 | 5 | 2 |
| 8 | 8 | 6 | 4 | 6 | 2 |
| 9 | 9 | 6 | 4 | 6 | 3 |
| 10 | 10 | 7 | 5 | 7 | 3 |
| 11 | 11 | 8 | 5 | 7 | 3 |
| 12 | 12 | 9 | 6 | 8 | 4 |
| 13 | 13 | 9 | 6 | 8 | 4 |
| 14 | 14 | 10 | 7 | 9 | 4 |
| 15 | 15 | 11 | 7 | 9 | 5 |
| 16 | 16 | 12 | 8 | 10 | 5 |
| 17 | 17 | 12 | 8 | 10 | 5 |
| 18 | 18 | 13 | 9 | 11 | 6 |
| 19 | 19 | 14 | 9 | 11 | 6 |
| 20 | 20 | 15 | 10 | 12 | 6 |

**Class progression slots (starter set — deepen; do not invent 5.2.2+):**

| class_id | bab | fort | ref | will | hd | notes |
|----------|-----|------|-----|------|----|-------|
| fighter | full | good | poor | poor | d10 | full BAB reference |
| rogue | three_quarter | poor | good | poor | d8 | 3/4 BAB |
| wizard | half | poor | poor | good | d6 | prepared arcane |
| cleric | three_quarter | good | poor | good | d8 | prepared divine |
| sorcerer | half | poor | poor | good | d6 | spontaneous arcane |

```json
{
  "plugin_id": "pathfinder_pf1",
  "curves": {
    "bab_full": {"formula": "L", "levels": [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]},
    "bab_three_quarter": {"formula": "floor(L*3/4)", "levels": [0,1,2,3,3,4,5,6,6,7,8,9,9,10,11,12,12,13,14,15]},
    "bab_half": {"formula": "floor(L/2)", "levels": [0,1,1,2,2,3,3,4,4,5,5,6,6,7,7,8,8,9,9,10]},
    "save_good": {"formula": "2+floor(L/2)", "levels": [2,3,3,4,4,5,5,6,6,7,7,8,8,9,9,10,10,11,11,12]},
    "save_poor": {"formula": "floor(L/3)", "levels": [0,0,1,1,1,2,2,2,3,3,3,4,4,4,5,5,5,6,6,6]}
  },
  "classes": [
    {"class_id": "fighter", "bab": "bab_full", "fort": "save_good", "ref": "save_poor", "will": "save_poor", "hd": "d10"},
    {"class_id": "rogue", "bab": "bab_three_quarter", "fort": "save_poor", "ref": "save_good", "will": "save_poor", "hd": "d8"},
    {"class_id": "wizard", "bab": "bab_half", "fort": "save_poor", "ref": "save_poor", "will": "save_good", "hd": "d6", "caster": "prepared_arcane"},
    {"class_id": "cleric", "bab": "bab_three_quarter", "fort": "save_good", "ref": "save_poor", "will": "save_good", "hd": "d8", "caster": "prepared_divine"},
    {"class_id": "sorcerer", "bab": "bab_half", "fort": "save_poor", "ref": "save_poor", "will": "save_good", "hd": "d6", "caster": "spontaneous_arcane"}
  ]
}
```

**Attack mode (check_schema):** `mode=attack` → `1d20 + BAB + ability_mod + misc` vs AC/touch; critical hooks plugin-defined; host audits only.

### 4.5 `spells_slots.json` — class/level slot matrix (PF1)

Slots = spells **per day** at each spell level (0–9). Arrays are length 10: index = spell level. Character level is the outer key. **Vault fills L1–20** (junior-usable); game-repo mint remains Half B.

**Wizard (prepared arcane) — spells/day by character level (PF1 core progression scaffold):**

| Char L | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|--------|---|---|---|---|---|---|---|---|---|---|
| 1 | 3 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 2 | 4 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 3 | 4 | 2 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 4 | 4 | 3 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 5 | 4 | 3 | 2 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| 6 | 4 | 3 | 3 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| 7 | 4 | 4 | 3 | 2 | 1 | 0 | 0 | 0 | 0 | 0 |
| 8 | 4 | 4 | 3 | 3 | 2 | 0 | 0 | 0 | 0 | 0 |
| 9 | 4 | 4 | 4 | 3 | 2 | 1 | 0 | 0 | 0 | 0 |
| 10 | 4 | 4 | 4 | 3 | 3 | 2 | 0 | 0 | 0 | 0 |
| 11 | 4 | 4 | 4 | 4 | 3 | 2 | 1 | 0 | 0 | 0 |
| 12 | 4 | 4 | 4 | 4 | 3 | 3 | 2 | 0 | 0 | 0 |
| 13 | 4 | 4 | 4 | 4 | 4 | 3 | 2 | 1 | 0 | 0 |
| 14 | 4 | 4 | 4 | 4 | 4 | 3 | 3 | 2 | 0 | 0 |
| 15 | 4 | 4 | 4 | 4 | 4 | 4 | 3 | 2 | 1 | 0 |
| 16 | 4 | 4 | 4 | 4 | 4 | 4 | 3 | 3 | 2 | 0 |
| 17 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 3 | 2 | 1 |
| 18 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 3 | 3 | 2 |
| 19 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 3 | 3 |
| 20 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 |

**Cleric (prepared divine)** — same slot matrix as wizard for scaffold (PF1 shared caster table shape); domain bonus slots = optional plugin hook (`bonus_slots_from_ability`).

**Sorcerer (spontaneous) — `slots_by_character_level` (spells/day):**

| Char L | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|--------|---|---|---|---|---|---|---|---|---|---|
| 1 | 5 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 2 | 6 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 3 | 6 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 4 | 6 | 6 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 5 | 6 | 6 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 6 | 6 | 6 | 5 | 3 | 0 | 0 | 0 | 0 | 0 | 0 |
| 7 | 6 | 6 | 6 | 4 | 0 | 0 | 0 | 0 | 0 | 0 |
| 8 | 6 | 6 | 6 | 5 | 3 | 0 | 0 | 0 | 0 | 0 |
| 9 | 6 | 6 | 6 | 6 | 4 | 0 | 0 | 0 | 0 | 0 |
| 10 | 6 | 6 | 6 | 6 | 5 | 3 | 0 | 0 | 0 | 0 |
| 11 | 6 | 6 | 6 | 6 | 6 | 4 | 0 | 0 | 0 | 0 |
| 12 | 6 | 6 | 6 | 6 | 6 | 5 | 3 | 0 | 0 | 0 |
| 13 | 6 | 6 | 6 | 6 | 6 | 6 | 4 | 0 | 0 | 0 |
| 14 | 6 | 6 | 6 | 6 | 6 | 6 | 5 | 3 | 0 | 0 |
| 15 | 6 | 6 | 6 | 6 | 6 | 6 | 6 | 4 | 0 | 0 |
| 16 | 6 | 6 | 6 | 6 | 6 | 6 | 6 | 5 | 3 | 0 |
| 17 | 6 | 6 | 6 | 6 | 6 | 6 | 6 | 6 | 4 | 0 |
| 18 | 6 | 6 | 6 | 6 | 6 | 6 | 6 | 6 | 5 | 3 |
| 19 | 6 | 6 | 6 | 6 | 6 | 6 | 6 | 6 | 6 | 4 |
| 20 | 6 | 6 | 6 | 6 | 6 | 6 | 6 | 6 | 6 | 6 |

**Sorcerer `spells_known_by_character_level` (full L1–20):**

| Char L | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|--------|---|---|---|---|---|---|---|---|---|---|
| 1 | 4 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 2 | 5 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 3 | 5 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 4 | 6 | 3 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 5 | 6 | 4 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 6 | 7 | 4 | 2 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| 7 | 7 | 5 | 3 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| 8 | 8 | 5 | 3 | 2 | 1 | 0 | 0 | 0 | 0 | 0 |
| 9 | 8 | 5 | 4 | 3 | 2 | 0 | 0 | 0 | 0 | 0 |
| 10 | 9 | 5 | 4 | 3 | 2 | 1 | 0 | 0 | 0 | 0 |
| 11 | 9 | 5 | 5 | 4 | 3 | 2 | 0 | 0 | 0 | 0 |
| 12 | 9 | 5 | 5 | 4 | 3 | 2 | 1 | 0 | 0 | 0 |
| 13 | 9 | 5 | 5 | 4 | 4 | 3 | 2 | 0 | 0 | 0 |
| 14 | 9 | 5 | 5 | 4 | 4 | 3 | 2 | 1 | 0 | 0 |
| 15 | 9 | 5 | 5 | 4 | 4 | 4 | 3 | 2 | 0 | 0 |
| 16 | 9 | 5 | 5 | 4 | 4 | 4 | 3 | 2 | 1 | 0 |
| 17 | 9 | 5 | 5 | 4 | 4 | 4 | 3 | 3 | 2 | 0 |
| 18 | 9 | 5 | 5 | 4 | 4 | 4 | 3 | 3 | 2 | 1 |
| 19 | 9 | 5 | 5 | 4 | 4 | 4 | 3 | 3 | 3 | 2 |
| 20 | 9 | 5 | 5 | 4 | 4 | 4 | 3 | 3 | 3 | 3 |

```json
{
  "plugin_id": "pathfinder_pf1",
  "slot_schema": {
    "dimensions": ["character_level", "spell_level_0_to_9"],
    "bonus_slots_from_ability": "optional_plugin_hook",
    "forbid_pf2e_focus_as_default": true
  },
  "classes": {
    "wizard": {
      "caster_type": "prepared_arcane",
      "slots_by_character_level": {
        "1": [3,1,0,0,0,0,0,0,0,0], "2": [4,2,0,0,0,0,0,0,0,0], "3": [4,2,1,0,0,0,0,0,0,0],
        "4": [4,3,2,0,0,0,0,0,0,0], "5": [4,3,2,1,0,0,0,0,0,0], "6": [4,3,3,2,0,0,0,0,0,0],
        "7": [4,4,3,2,1,0,0,0,0,0], "8": [4,4,3,3,2,0,0,0,0,0], "9": [4,4,4,3,2,1,0,0,0,0],
        "10": [4,4,4,3,3,2,0,0,0,0], "11": [4,4,4,4,3,2,1,0,0,0], "12": [4,4,4,4,3,3,2,0,0,0],
        "13": [4,4,4,4,4,3,2,1,0,0], "14": [4,4,4,4,4,3,3,2,0,0], "15": [4,4,4,4,4,4,3,2,1,0],
        "16": [4,4,4,4,4,4,3,3,2,0], "17": [4,4,4,4,4,4,4,3,2,1], "18": [4,4,4,4,4,4,4,3,3,2],
        "19": [4,4,4,4,4,4,4,4,3,3], "20": [4,4,4,4,4,4,4,4,4,4]
      }
    },
    "sorcerer": {
      "caster_type": "spontaneous_arcane",
      "slots_by_character_level": {
        "1": [5,3,0,0,0,0,0,0,0,0], "2": [6,4,0,0,0,0,0,0,0,0], "3": [6,5,0,0,0,0,0,0,0,0],
        "4": [6,6,3,0,0,0,0,0,0,0], "5": [6,6,4,0,0,0,0,0,0,0], "6": [6,6,5,3,0,0,0,0,0,0],
        "7": [6,6,6,4,0,0,0,0,0,0], "8": [6,6,6,5,3,0,0,0,0,0], "9": [6,6,6,6,4,0,0,0,0,0],
        "10": [6,6,6,6,5,3,0,0,0,0], "11": [6,6,6,6,6,4,0,0,0,0], "12": [6,6,6,6,6,5,3,0,0,0],
        "13": [6,6,6,6,6,6,4,0,0,0], "14": [6,6,6,6,6,6,5,3,0,0], "15": [6,6,6,6,6,6,6,4,0,0],
        "16": [6,6,6,6,6,6,6,5,3,0], "17": [6,6,6,6,6,6,6,6,4,0], "18": [6,6,6,6,6,6,6,6,5,3],
        "19": [6,6,6,6,6,6,6,6,6,4], "20": [6,6,6,6,6,6,6,6,6,6]
      },
      "spells_known_by_character_level": {
        "1": [4,2,0,0,0,0,0,0,0,0], "2": [5,2,0,0,0,0,0,0,0,0], "3": [5,3,0,0,0,0,0,0,0,0],
        "4": [6,3,1,0,0,0,0,0,0,0], "5": [6,4,2,0,0,0,0,0,0,0], "6": [7,4,2,1,0,0,0,0,0,0],
        "7": [7,5,3,2,0,0,0,0,0,0], "8": [8,5,3,2,1,0,0,0,0,0], "9": [8,5,4,3,2,0,0,0,0,0],
        "10": [9,5,4,3,2,1,0,0,0,0], "11": [9,5,5,4,3,2,0,0,0,0], "12": [9,5,5,4,3,2,1,0,0,0],
        "13": [9,5,5,4,4,3,2,0,0,0], "14": [9,5,5,4,4,3,2,1,0,0], "15": [9,5,5,4,4,4,3,2,0,0],
        "16": [9,5,5,4,4,4,3,2,1,0], "17": [9,5,5,4,4,4,3,3,2,0], "18": [9,5,5,4,4,4,3,3,2,1],
        "19": [9,5,5,4,4,4,3,3,3,2], "20": [9,5,5,4,4,4,3,3,3,3]
      }
    },
    "cleric": {
      "caster_type": "prepared_divine",
      "slots_by_character_level": {
        "1": [3,1,0,0,0,0,0,0,0,0], "2": [4,2,0,0,0,0,0,0,0,0], "3": [4,2,1,0,0,0,0,0,0,0],
        "4": [4,3,2,0,0,0,0,0,0,0], "5": [4,3,2,1,0,0,0,0,0,0], "6": [4,3,3,2,0,0,0,0,0,0],
        "7": [4,4,3,2,1,0,0,0,0,0], "8": [4,4,3,3,2,0,0,0,0,0], "9": [4,4,4,3,2,1,0,0,0,0],
        "10": [4,4,4,3,3,2,0,0,0,0], "11": [4,4,4,4,3,2,1,0,0,0], "12": [4,4,4,4,3,3,2,0,0,0],
        "13": [4,4,4,4,4,3,2,1,0,0], "14": [4,4,4,4,4,3,3,2,0,0], "15": [4,4,4,4,4,4,3,2,1,0],
        "16": [4,4,4,4,4,4,3,3,2,0], "17": [4,4,4,4,4,4,4,3,2,1], "18": [4,4,4,4,4,4,4,3,3,2],
        "19": [4,4,4,4,4,4,4,4,3,3], "20": [4,4,4,4,4,4,4,4,4,4]
      }
    }
  }
}
```

`ICharacterCreationHost` (F3) reads these matrices — host stays ruleset-agnostic; deepen existing 5.1/5.2 leaves only.

### 4.6 `spells_list.json` — spell-list scaffolding (agency metadata feed)

Shape for [[Phase-5-2-1-SpellMetadataRegistry-and-SpellAgencyPerspectiveManifest-Roadmap-2026-09-29-1319|5.2.1 SpellMetadataRegistry]]. **Ids + slots only** — no full spell text dump; junior fills from cleared open material.

| Field | Type | Notes |
|-------|------|--------|
| `spell_id` | string | stable id (`magic_missile`, `cure_light_wounds`) |
| `school` | enum | abjuration…universal (PF1 schools) |
| `descriptors[]` | string | optional (`fear`, `mind-affecting`) |
| `level_by_class` | map | `{wizard:1, sorcerer:1, cleric:null}` |
| `components` | `{V,S,M,F,DF}` bools | material/focus refs as opaque ids |
| `casting_time` | enum | `standard`, `swift`, `full_round`, … |
| `range` | enum/ref | `personal`, `touch`, `close`, … |
| `agency_overlays` | ref | optional → SpellAgencyPerspectiveManifest |
| `status` | enum | `stub_shape` \| `content_ok` |

**Starter demo set (12 ids — enough for 5.2.1 + Exemplar graybox + L3 probes):**

| spell_id | school | wizard | sorcerer | cleric | agency note |
|----------|--------|--------|----------|--------|-------------|
| detect_magic | divination | 0 | 0 | 0 | observe-only overlay |
| light | evocation | 0 | 0 | 0 | cantrip/orison surface |
| magic_missile | evocation | 1 | 1 | — | combat surface |
| mage_armor | conjuration | 1 | 1 | — | self buff |
| cure_light_wounds | conjuration | — | — | 1 | heal; divine seat |
| sleep | enchantment | 1 | 1 | — | mind-affecting refuse wrong seat |
| invisibility | illusion | 2 | 2 | — | stealth / agency overlay |
| web | conjuration | 2 | 2 | — | area control |
| fireball | evocation | 3 | 3 | — | AoE combat |
| dispel_magic | abjuration | 3 | 3 | 3 | cross-class utility |
| haste | transmutation | 3 | 3 | — | buff / agency tempo |
| cure_serious_wounds | conjuration | — | — | 3 | mid heal; divine seat |

Add `tables/spells_list.json` to `plugin_manifest.tables` when minting game-repo (Half B). Vault authority for shapes: **this section**.

```json
{
  "plugin_id": "pathfinder_pf1",
  "spells": [
    {"spell_id": "detect_magic", "school": "divination", "level_by_class": {"wizard": 0, "sorcerer": 0, "cleric": 0}, "components": {"V": true, "S": true}, "status": "stub_shape"},
    {"spell_id": "light", "school": "evocation", "level_by_class": {"wizard": 0, "sorcerer": 0, "cleric": 0}, "components": {"V": true, "M": true}, "status": "stub_shape"},
    {"spell_id": "magic_missile", "school": "evocation", "level_by_class": {"wizard": 1, "sorcerer": 1}, "components": {"V": true, "S": true}, "status": "stub_shape"},
    {"spell_id": "mage_armor", "school": "conjuration", "level_by_class": {"wizard": 1, "sorcerer": 1}, "components": {"V": true, "S": true, "F": true}, "status": "stub_shape"},
    {"spell_id": "cure_light_wounds", "school": "conjuration", "level_by_class": {"cleric": 1}, "components": {"V": true, "S": true}, "status": "stub_shape"},
    {"spell_id": "sleep", "school": "enchantment", "descriptors": ["mind-affecting"], "level_by_class": {"wizard": 1, "sorcerer": 1}, "components": {"V": true, "S": true, "M": true}, "status": "stub_shape"},
    {"spell_id": "invisibility", "school": "illusion", "level_by_class": {"wizard": 2, "sorcerer": 2}, "components": {"V": true, "S": true, "M": true}, "status": "stub_shape"},
    {"spell_id": "web", "school": "conjuration", "level_by_class": {"wizard": 2, "sorcerer": 2}, "components": {"V": true, "S": true, "M": true}, "status": "stub_shape"},
    {"spell_id": "fireball", "school": "evocation", "level_by_class": {"wizard": 3, "sorcerer": 3}, "components": {"V": true, "S": true, "M": true}, "status": "stub_shape"},
    {"spell_id": "dispel_magic", "school": "abjuration", "level_by_class": {"wizard": 3, "sorcerer": 3, "cleric": 3}, "components": {"V": true, "S": true}, "status": "stub_shape"},
    {"spell_id": "haste", "school": "transmutation", "level_by_class": {"wizard": 3, "sorcerer": 3}, "components": {"V": true, "S": true, "M": true}, "status": "stub_shape"},
    {"spell_id": "cure_serious_wounds", "school": "conjuration", "level_by_class": {"cleric": 3}, "components": {"V": true, "S": true}, "status": "stub_shape"}
  ]
}
```

---

## 5. How-To ↔ Host Index wiring

| Doc | Section | Points to |
|-----|---------|-----------|
| [[Junior-Tech-Adapt-How-To]] | §3 DiceRoller | Host Index §B4 `IDiceRoller` |
| [[Junior-Tech-Adapt-How-To]] | §4 PF1 remint F1–F5 | **this scaffold** + Phase-5 remint table |
| [[SeamRegistry-CSharp-Host-Index]] | §B4 Rules | default plugin `pathfinder_pf1` → this scaffold + How-To §4 |
| Phase-5 primary | remint path F2 | `res://rules/pathfinder_pf1/` + **this note as vault scaffold** |
| 6.2.5 RuleCheckProbe | binder | `demo_ruleset_pf1` / `check_schema` above |
| 6.4 Exemplar | `R.rules.pf1_bind` | ActiveRuleset == `pathfinder_pf1` |

---

## 6. Junior verify (content)

- [ ] `plugin_id` is **`pathfinder_pf1`** (not `pathfinder_pf2e_orc`, not `srd_5_1`)
- [ ] At least abilities + skills + check_schema + **BAB L1–20 curves** + **spell-slot L1–20 matrices** exist under remint path **or** this vault scaffold is linked from Phase-5 F2 status
- [ ] Demo binder uses `demo_ruleset_pf1` / `pf1_check_v0`
- [ ] Spell-list scaffolding feeds 5.2.1 registry (starter ≥12 spell_ids)
- [ ] All contested rolls go through `IDiceRoller`
- [ ] No PF2e degree-of-success ladder as the **default** success rule

## Status

Minted **2026-09-29** with PF1 operator lock; thickened BAB/save L1–20; **design-gate 2026-09-30** filled spell-slot **L1–20** (wizard/cleric/sorcerer) + sorcerer spells_known L1–20 + **12** spell_ids. Game-repo file mint remains Half B (`half_b_deferred`).
