# L5-AFFIRM-DIGEST — `ux_player_character_creation`

- label: Players can author characters and submit them for DM acceptance into a world
- affirm_status: green
- l5_origin: pass_b_aligned
- needs_pin: false
- moment_count: 6
- thin_floor: 4

## Contract (What it is)

Player authors and owns a character before and after DM greenlight. Builds may be unbound or against a campaign invite (entry into campaign and world); invited builds disable banned options from world and campaign configs with overwrite-request path. Accept flow: invite → attach → greenlight. Incomplete builds are unfinished characters, not a draft type. Background→world proposals stay DM-gated and retconnable.

## Moments

- **Seat:** player, shared_table · **Trigger:** contract clause 1 · **Observable response:** Player authors and owns a character before and after DM greenlight · **Refusal/guard:** anti-mandate / wrong altitude · **Residue:** durable table-visible consequence when applicable
- **Seat:** player, shared_table · **Trigger:** contract clause 2 · **Observable response:** Builds may be unbound or against a campaign invite (entry into campaign and world) · **Refusal/guard:** anti-mandate / wrong altitude · **Residue:** durable table-visible consequence when applicable
- **Seat:** player, shared_table · **Trigger:** contract clause 3 · **Observable response:** invited builds disable banned options from world and campaign configs with overwrite-request path · **Refusal/guard:** anti-mandate / wrong altitude · **Residue:** durable table-visible consequence when applicable
- **Seat:** player, shared_table · **Trigger:** contract clause 4 · **Observable response:** Accept flow: invite → attach → greenlight · **Refusal/guard:** anti-mandate / wrong altitude · **Residue:** durable table-visible consequence when applicable
- **Seat:** player, shared_table · **Trigger:** contract clause 5 · **Observable response:** Incomplete builds are unfinished characters, not a draft type · **Refusal/guard:** anti-mandate / wrong altitude · **Residue:** durable table-visible consequence when applicable
- **Seat:** player, shared_table · **Trigger:** contract clause 6 · **Observable response:** Background→world proposals stay DM-gated and retconnable · **Refusal/guard:** anti-mandate / wrong altitude · **Residue:** durable table-visible consequence when applicable

## PoC cut

PoC names the play-verb moments in Moment inventory (intent / resolve / residue) with thin chrome; defer pack-content depth, multi-wave tooling, and non-essential polish. Full vision remains larger than this cut.

## Gate

- ok: True
- violations: []
- warnings: []
