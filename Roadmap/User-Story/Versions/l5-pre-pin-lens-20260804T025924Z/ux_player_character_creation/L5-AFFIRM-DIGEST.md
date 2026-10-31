# L5-AFFIRM-DIGEST — `ux_player_character_creation`

- label: Players can author characters and submit them for DM acceptance into a world
- affirm_status: yellow
- l5_origin: pass_b_aligned
- needs_pin: true
- moment_count: 6
- thin_floor: 4

## Contract (What it is)

Player authors and owns a character before and after DM greenlight. Builds may be unbound or against a campaign invite (entry into campaign and world); invited builds disable banned options from world and campaign configs with overwrite-request path. Accept flow: invite → attach → greenlight. Incomplete builds are unfinished characters, not a draft type. Background→world proposals stay DM-gated and retconnable.

## Moments

- **Seat:** player · **Trigger:** player opens/continues an unfinished character build (unbound or invite-bound) · **Observable response:** builder shows legal options; banned invite options disabled or overwrite-requestable · **Refusal/guard:** cannot invent a separate “draft object” type; incomplete stays unfinished character · **Residue:** character record owned by the player
- **Seat:** player · **Trigger:** player submits character for DM acceptance (invite → attach → greenlight path) · **Observable response:** submission visible on DM review rail · **Refusal/guard:** no silent auto-accept; ownership does not transfer on submit · **Residue:** pending-greenlight state on the campaign/world attach
- **Seat:** privileged_access (DM) · **Trigger:** DM greenlights, returns-with-notes, or negotiates overwrite · **Observable response:** player sees accept / notes / overwrite outcome · **Refusal/guard:** DM cannot seize ownership; player keeps authorship after greenlight · **Residue:** character bound into world/campaign package or returned unfinished
- **Seat:** player · **Trigger:** player accepts campaign/world invite package while building or attaching · **Observable response:** bound rules/content/visual defaults install for that world/campaign · **Refusal/guard:** cosmetics cannot substitute for package authority · **Residue:** invite package attached to the character’s campaign seat
- **Seat:** player · **Trigger:** background→world proposal from the build · **Observable response:** proposal queued for DM · **Refusal/guard:** never auto-writes world canon · **Residue:** DM-retconnable world suggestion only
- **Seat:** shared_table · **Trigger:** table later invites the same character into another campaign in the same world · **Observable response:** re-attach / greenlight path without forcing rebuild-from-scratch · **Refusal/guard:** one-campaign forever not mandated · **Residue:** multi-campaign membership under world container

## PoC cut

PoC proves **build legality feedback → submit → DM greenlight or return-with-notes → player keeps ownership**, plus thin invite attach. Defer rich builder chrome, multi-campaign polish, and deep overwrite UX. Full vision keeps unbound-then-invite and divergent option sets.

## Gate

- ok: True
- violations: []
- warnings: ['needs_pin']
