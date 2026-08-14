---
title: Lore — Core vs Table dual system
schema_version: 1
source_title: Operator lore-pack doctrine (2026-08-13 dialogue + Tal’dorei Exemplar pivot)
signal: strong
research_status: feedstock_lock_operator
assumption: false
liked: "Portable Core Lore (roles, paradigms, tone) vs local Table Lore (fillers, rulings, mutations); prebuilt packs; shared-table requirement; Tal’dorei as first Exemplar source under adventure-module import/migration grammar; upstream data for pantheons, structures, factions, magic, floats, etc."
why_it_worked: "Shared conceptual grammar that can travel between maps, without mixing campaign-local fillers into the portable pack"
fits_our_game: "Dual system: Core Lore = portable prebuilt conceptual pack that defines roles; Table Lore = local non-portable overlay for named fillers, rulings, bans, campaign history, and addenda. **Exemplar pivot CLOSED (2026-08-13):** Core Lore packages use the same import/migration grammar as adventure modules (`adventure-module-ruleset-migration` — native when aligned; else DM migration with audit). First Exemplar source = **Tal’dorei**: extract transferable Core (roles, paradigms, cultural grammar, institutional/religious frames, magical assumptions, political/economic logic, historical frames); leave named fillers / campaign history / rulings / bans / addenda in Table Lore only. Shared-table discipline remains. Growing Core during play is out of scope. Exemplar content extraction can proceed as a separate feedstock task; architecture is locked. Grounds in `pantheons-institutional-faith`, `structures-gen-cultural-historical`, `factions-as-persons-fingers-ripples`, `ability-checks-float-membrane`, `knowledge-flow-channels`, `conditions-felt-state-machine`."
refuse_to_copy:
  - "Geography-locked lore that cannot travel between maps"
  - "Single mutable pack that mixes Core and Table concerns and then requires distillation"
  - "Growing the Core pack as a normal play activity"
  - "Table mutations contaminating the shared Core package"
  - "Mandatory single official lore for every possible table (architecture stays open; Exemplar is the supported default)"
  - "Importing Tal’dorei as a setting bible instead of extracting portable Core roles"
maps_to_series:
  - ux_living_world_continuity
  - ux_dm_campaign_creation
  - ux_collaborative_table_agency
  - ux_backstory_legacy_integration
  - ux_mental_stat_interpretation
pillars:
  - roleplay
  - exploration
  - tooling
ip_posture: pattern_only_no_clone
---

# Lore — Core vs Table

**Job:** lore supplies the shared conceptual and cultural grammar the system and table use to roleplay. It defines the roles, assumptions, and expressive vocabulary that pantheons, factions, NPCs, magic, structures, and residual history draw from. It is **not** a geography-locked setting bible.

## Dual system

| Layer | Texture |
|-------|---------|
| **Core Lore** | Portable, prebuilt, sharable package. Defines roles, paradigms, tonal boundaries, magical assumptions, political and economic logic, historical frames, religious structure, cultural dialects, and the conceptual source of floated information. It defines the **role**, not who currently fills it. |
| **Table Lore** | Local, non-portable overlay that lives only at that table. Holds specific named entities that fill the roles, campaign history, table rulings that required a lore explanation, bans, addenda, and any mutations that arise through play. Table Lore does **not** feed back into the Core package. “Because I am the DM” remains an acceptable justification for a Table Lore ruling. |

## Shared-table discipline

All players at a table must use the **same Core Lore package** (analogous to using the same ruleset package).

## Import / migration grammar (closed 2026-08-13)

Core Lore packages follow the same grammar as adventure modules (`adventure-module-ruleset-migration`):

- **Native** when the pack’s ruleset/assumptions align with the table’s active rules.
- Else **DM migration + audit**.

## Exemplar pivot (closed 2026-08-13)

**Source:** Tal’dorei (concrete first Exemplar).

| Layer | Extract |
|-------|---------|
| **Core (transferable)** | Roles, paradigms, cultural grammar, institutional/religious frames, magical assumptions, political/economic logic, historical frames — portable pack only. |
| **Table (local)** | Named fillers, campaign history, rulings, bans, addenda — non-contaminating; never feeds Core. |

Architecture is locked. Exemplar **content extraction** may proceed as a separate Cursor feedstock task.

## Lifecycle

Packs are **prebuilt**. Worlds grow into them. Growing the Core pack during play is **out of scope**. Addenda are allowed and remain Table Lore (or become explicit future pack updates). Incomplete Core packs are not expected in normal use.

## Major domains a Core pack is expected to cover

Politics, economics, history, religion / pantheon frame, magic and how it is handled, cultural dialects, and the conceptual material that feeds floated information under ability scores and investment systems.

## Tonal range

Architecture accepts the full spectrum (Grimm-dark → mid/high fantasy → planar traversal, etc.). Each Core pack declares its own center of gravity. Mid-to-high fantasy Exemplar remains the supported default center for this project’s first pack.

## Upstream data

Core Lore feeds pantheons, structures gen cultural dialects, factions, institutional weather, transformative anchors, magic feel, treasure provenance flavors, ability-check floats, BBEG forms, and related surfaces.

## Refuse (required)

- Geography-locked lore that cannot travel between maps
- Single mutable pack that mixes Core and Table concerns and then requires distillation
- Growing the Core pack as a normal play activity
- Table mutations contaminating the shared Core package
- Mandatory single official lore for every possible table (architecture stays open; Exemplar is the supported default)
- Importing Tal’dorei as a setting bible instead of extracting portable Core roles
