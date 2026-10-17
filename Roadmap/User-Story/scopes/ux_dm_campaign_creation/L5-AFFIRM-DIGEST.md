# L5-AFFIRM-DIGEST — `ux_dm_campaign_creation`

- label: DM can bootstrap a campaign frame inside a world
- affirm_status: green
- l5_origin: pass_b_aligned
- needs_pin: false
- moment_count: 6
- thin_floor: 0

## Contract (What it is)

Orchestrator creates or revises a campaign frame (tone, bounds, public facts, cast expectations, logging seam) as a player-facing authorship act inside an existing or newly attached world — not the world container itself. Exit to world or session prep; not player character creation.

## Moments

- **Seat:** dm_as_player, privileged_access · **Trigger:** enter `ux_session0_bootstrap` · **Observable response:** In-tool session 0 — bounds, tone pick, intent propose, table accept/revise (under DM can bootstrap a campaign frame inside a world). · **Refusal/guard:** out of contract / wrong seat · **Residue:** lasting readable state from this moment
- **Seat:** dm_as_player, privileged_access · **Trigger:** enter `ux_session_onboarding` · **Observable response:** First-run or session-start rituals — setup, preferences, identity tone before core use (under DM can bootstrap a campaign frame inside a world). · **Refusal/guard:** out of contract / wrong seat · **Residue:** lasting readable state from this moment
- **Seat:** dm_as_player, privileged_access · **Trigger:** enter `ux_tone_profile_surface` · **Observable response:** How the chosen tone biases chrome, previews, and felt world without siloed presets (under DM can bootstrap a campaign frame inside a world). · **Refusal/guard:** out of contract / wrong seat · **Residue:** lasting readable state from this moment
- **Seat:** dm_as_player, privileged_access · **Trigger:** contract clause 1 · **Observable response:** Orchestrator creates or revises a campaign frame (tone, bounds, public facts, cast expectations, logging seam) as a player-facing authorship act inside an existing or newly attached world — not the world container itself · **Refusal/guard:** anti-mandate / wrong altitude · **Residue:** durable table-visible consequence when applicable
- **Seat:** dm_as_player, privileged_access · **Trigger:** contract clause 2 · **Observable response:** Exit to world or session prep · **Refusal/guard:** anti-mandate / wrong altitude · **Residue:** durable table-visible consequence when applicable
- **Seat:** dm_as_player, privileged_access · **Trigger:** contract clause 3 · **Observable response:** not player character creation · **Refusal/guard:** anti-mandate / wrong altitude · **Residue:** durable table-visible consequence when applicable

## PoC cut

First cut proves the parent contract with a small surface set (`ux_session0_bootstrap`, `ux_session_onboarding`); defer `ux_tone_profile_surface` and deeper chrome. Keep anti-mandate and authored structure menus honest.

## Gate

- ok: True
- violations: []
- warnings: []
