---
title: Batch digest — ux_collaborative_table_agency
parent_id: ux_collaborative_table_agency
walk_surface: batch_digest
---

# Batch digest — `ux_collaborative_table_agency`

**Parent:** Shared virtual-tabletop loop with character agency and DM orchestration
**Contract:** Virtual tabletop for collaborative storytelling: players act through character tools in an open 3D world; the DM is the privileged orchestrator in the same product loop. Loop is player agency → system and DM resolution → world reacts → roleplay inside that structure. Motives/stakes are table-defined and recorded; player speech can be transcribed. NPC dialogue is the DM’s responsibility — assist tools surface context, they do not replace the DM as speaker by default.

**Parent does_not_mandate (inherit — do not re-litigate):**
- DM is only a cue issuer for other players
- players and DM share identical control envelopes
- system-owned NPC dialogue is the product default
- player social play defaults to dialogue-option trees
- play must be combat-primary / hack-and-slash

Child surface: `inherits_parent_anti_mandate` + **local** `alternatives_not_banned`.
Missing local alternatives = **yellow** (polish), not red re-scope.
Open full `WALK.md` only for yellow / red / thin ids.

| id | status | inherits | alt_n | alternatives_not_banned | local_does_not_mandate | summary |
|----|--------|----------|-------|-------------------------|------------------------|---------|
| `ux_application_shell` | pending | yes | 2 | Minimal app chrome vs denser navigation hierarchy; Single primary nav vs multi-rail shell |  | Baseline shell — screen regions, chrome placement, layout mapping for any product (under Shared virtual-tabletop loop with character agency and DM orchestration). |
| `ux_primary_navigation` | pending | yes | 2 | Minimal app chrome vs denser navigation hierarchy; Single primary nav vs multi-rail shell |  | How users move between major areas — menus, routes, breadcrumbs, spatial wayfinding (under Shared virtual-tabletop loop with character agency and DM orchestration). |
