---
title: Batch digest — ux_world_generation
parent_id: ux_world_generation
walk_surface: batch_digest
---

# Batch digest — `ux_world_generation`

**Parent:** DM can create (table can shape) a persistent living world
**Contract:** Durable world container — DM creates initial form via wizard+preview (tone-aware shape families, cached/pre-existing assets); table can shape; players do not author the first world. Physical/settlement layers + monster-region tags; import/attach first-class; every world-hitting change is DM-retconnable. Multiple campaigns/casts attach to the same world.

**Parent does_not_mandate (inherit — do not re-litigate):**
- one world equals exactly one campaign forever
- worldgen is only a Session 0 checkbox with no persistent container
- players author the first world
- world create forces unconstrained multi-knob fresh-noise every time
- world creation's default next step is player character creation

Child surface: `inherits_parent_anti_mandate` + **local** `alternatives_not_banned`.
Missing local alternatives = **yellow** (polish), not red re-scope.
Open full `WALK.md` only for yellow / red / thin ids.

| id | status | inherits | alt_n | alternatives_not_banned | local_does_not_mandate | summary |
|----|--------|----------|-------|-------------------------|------------------------|---------|
| `ux_worldgen_gui` | pending | yes | 3 | Propose/refine dialogue vs one-shot generate-and-accept; Preview scaffold before persist vs write-through generation; Thin prompt vs deep scaffold menu before first world commit |  | Collaborative generation dialogue — propose scaffolds, choose/refine, preview, accept/regenerate a persistent living world) (under DM can create (table can shape) a persistent living world). |
