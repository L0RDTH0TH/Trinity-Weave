# L5-AFFIRM-DIGEST — `ux_collaborative_table_agency`

- label: Shared virtual-tabletop loop with character agency and DM orchestration
- affirm_status: yellow
- l5_origin: pass_b_aligned
- needs_pin: true
- moment_count: 6
- thin_floor: 4

## Contract (What it is)

Virtual tabletop for collaborative storytelling: players act through character tools in an open 3D world; the DM is the privileged orchestrator in the same product loop. Loop is player agency → system and DM resolution → world reacts → roleplay inside that structure. Motives/stakes are table-defined and recorded; player speech can be transcribed. NPC dialogue is the DM’s responsibility — assist tools surface context, they do not replace the DM as speaker by default.

## Moments

- **Seat:** shared_table (player) · **Trigger:** player issues character intent in the open 3D world (move, speak, interact — not a dialogue-option tree default) · **Observable response:** intent is visible to the table / queued for system+DM resolution · **Refusal/guard:** wrong seat; identical control envelope denied for DM-only tools · **Residue:** motive/stakes note or world hook recorded when the table defines it
- **Seat:** privileged_access / dm_as_player · **Trigger:** DM resolves or overrides a player intent (accept, modify, deny) · **Observable response:** resolution is visible; world reaction begins · **Refusal/guard:** system does not auto-speak for NPCs; DM remains speaker by default · **Residue:** world/NPC state change readable to players
- **Seat:** shared_table · **Trigger:** world reacts after resolution (NPC move, door, rumor, pressure) · **Observable response:** players see/feel the reaction in-world; roleplay continues inside that structure · **Refusal/guard:** no silent backend-only mutation without table-visible residue · **Residue:** lasting world/campaign-readable cost or opportunity
- **Seat:** shared_table · **Trigger:** table captures motive/stakes or optional speech transcript · **Observable response:** light note / recap affordance updates shared session memory · **Refusal/guard:** heavy mandatory transcription not required · **Residue:** stake record available for later session prep / combat / lore
- **Seat:** privileged_access · **Trigger:** DM opens NPC context assist (not auto-dialogue) · **Observable response:** context prompts surface for the DM to speak · **Refusal/guard:** assist does not replace DM as speaker · **Residue:** none unless DM acts into the world
- **Seat:** shared_table · **Trigger:** use shell regions / primary navigation to reach the play loop (supporting chrome, not the loop itself) · **Observable response:** layout and wayfinding land the seats in the collaborative frame (`ux_application_shell`, `ux_primary_navigation`) · **Refusal/guard:** chrome without intent→resolve→react is incomplete product · **Residue:** session stays in the shared product, not a separate DM-only app

## PoC cut

PoC proves **player intent → DM/system resolve/override → visible world react** with thin stake capture and minimal shell/nav. Defer rich transcription, deep NPC assist libraries, and combat-primary defaults. Shell/nav stay supporting chrome, not the first product claim.

## Gate

- ok: True
- violations: []
- warnings: ['needs_pin']
