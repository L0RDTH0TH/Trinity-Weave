---
title: Batch digest — ux_backstory_legacy_integration
parent_id: ux_backstory_legacy_integration
walk_surface: batch_digest
---

# Batch digest — `ux_backstory_legacy_integration`

**Parent:** Backstory and legacies can hook into play and chronicle
**Contract:** Backstory and legacies are a first-class player seeding system: players seed personal history, relationships, debts, places, and claims; the system floats those hooks to the DM; the DM weaves timing, intensity, and form under the world/campaign gate (accept, revise, retcon). Players do not auto-write canon. Seeds appear in play and player-lite chronicle as structure menu — not a mandated reunion ordeal and not DM-only lore with no player surface.

**Parent does_not_mandate (inherit — do not re-litigate):**
- every backstory forces a mid-game reunion ordeal
- legacies are DM-only lore with no player surface
- system auto-weaves hooks without DM accept
- one identity-pact skin is the product default for legacies
- players may auto-write world canon from backstory without DM gate

Child surface: `inherits_parent_anti_mandate` + **local** `alternatives_not_banned`.
Missing local alternatives = **yellow** (polish), not red re-scope.
Open full `WALK.md` only for yellow / red / thin ids.

| id | status | inherits | alt_n | alternatives_not_banned | local_does_not_mandate | summary |
|----|--------|----------|-------|-------------------------|------------------------|---------|
| `ux_chronicle_buckets` | pending | yes | 2 | Strict three-bucket separation vs soft merged chronicle views; Thin personal archive vs richer searchable chronicle |  | Keep world ripples, session chronicle, and personal archive distinct in UX (under Backstory and legacies can hook into play and chronicle). |
| `ux_class_chrome_discovery` | pending | yes | 2 | Optional vs always-on identity chrome in the embodied moment; Sparse diegetic notice vs explicit class/identity recognition surface |  | How class or identity polish is noticed and used without leaving the embodied moment (under Backstory and legacies can hook into play and chronicle). |
| `ux_player_lite_lore_gui` | pending | yes | 2 | Minimal inbox+Legacies vs fuller recap/chronicle chrome; Read-mostly vs light intent-propose without DM-write power |  | Intent inbox, Legacies, last-session recap, personal chronicle — not sim admin (under Backstory and legacies can hook into play and chronicle). |
