---
title: Batch digest — ux_dm_campaign_creation
parent_id: ux_dm_campaign_creation
walk_surface: batch_digest
---

# Batch digest — `ux_dm_campaign_creation`

**Parent:** DM can bootstrap a campaign frame inside a world
**Contract:** Orchestrator creates or revises a campaign frame (tone, bounds, public facts, cast expectations, logging seam) as a player-facing authorship act inside an existing or newly attached world — not the world container itself. Exit to world or session prep; not player character creation.

**Parent does_not_mandate (inherit — do not re-litigate):**
- every campaign begins in captivity
- offline Microscope play is required before Session 0
- starting a campaign must regenerate the whole world
- campaign creation's default next step is player character creation
- DM is the primary author of player characters after frame bootstrap

Child surface: `inherits_parent_anti_mandate` + **local** `alternatives_not_banned`.
Missing local alternatives = **yellow** (polish), not red re-scope.
Open full `WALK.md` only for yellow / red / thin ids.

| id | status | inherits | alt_n | alternatives_not_banned | local_does_not_mandate | summary |
|----|--------|----------|-------|-------------------------|------------------------|---------|
| `ux_session0_bootstrap` | pending | yes | 2 | Short Session-0 vs expanded tone/onboarding wizard; Preset tone packs vs fully custom profile |  | In-tool session 0 — bounds, tone pick, intent propose, table accept/revise (under DM can bootstrap a campaign frame inside a world). |
| `ux_session_onboarding` | pending | yes | 2 | Short Session-0 vs expanded tone/onboarding wizard; Preset tone packs vs fully custom profile |  | First-run or session-start rituals — setup, preferences, identity tone before core use (under DM can bootstrap a campaign frame inside a world). |
| `ux_tone_profile_surface` | pending | yes | 2 | Short Session-0 vs expanded tone/onboarding wizard; Preset tone packs vs fully custom profile |  | How the chosen tone biases chrome, previews, and felt world without siloed presets (under DM can bootstrap a campaign frame inside a world). |
