# L5-AFFIRM-DIGEST — `ux_combat_play_surface`

- label: Combat can resolve by authored paths including non-win ends
- affirm_status: yellow
- l5_origin: pass_b_aligned
- needs_pin: true
- moment_count: 6
- thin_floor: 4

## Contract (What it is)

Combat is a distinct play surface the whole table enters and exits: combat chrome and audio for both seats; authorship menu of ends (fight, disengage/flee, parley, stakes, surrender, escape-with-cost, and other legitimate paths); DM gates all actions, owns the encounter cast with creature chrome and voice tools, and can adjust live values. Movement is a readable terrain-aware envelope. Surface consumes pre-compiled rule math from an import/library path. Power band gates offer and lasting costs. Not one flee caption and not the full rules-math pack.

## Moments

- **Seat:** shared_table (player) · **Trigger:** player issues a combat intent (attack, cast, move, disengage start) · **Observable response:** intent is queued visibly under DM gate; cast/hit sensory feedback when the action resolves (`ux_combat_cast_feedback`) · **Refusal/guard:** DM denies / retcons; out-of-turn or illegal envelope · **Residue:** HP/conditions/position change readable to the table
- **Seat:** shared_table · **Trigger:** player or DM opens the authored-ends menu (fight continue / flee-disengage / parley / stakes / surrender / escape-with-cost) · **Observable response:** available ends and stakes are visible enough to choose · **Refusal/guard:** end not offered this encounter; power-band blocks lasting-cost offer · **Residue:** chosen end leaves lasting cost or clean exit back to explore/social/quiet
- **Seat:** privileged_access (DM) · **Trigger:** DM gates a PC or creature action, or adjusts live cast values · **Observable response:** gate decision and live-value change are visible on the combat rail; creature chrome/voice tools stay DM-owned · **Refusal/guard:** player cannot bypass DM gate; players do not share identical combat control envelopes · **Residue:** encounter state updated; retcon path remains DM-owned
- **Seat:** shared_table · **Trigger:** unit moves inside the terrain-aware movement envelope · **Observable response:** legal range / free movement reads on the surface for PCs and DM-controlled creatures · **Refusal/guard:** illegal terrain / blocked path · **Residue:** new position persists for the next intent
- **Seat:** shared_table · **Trigger:** combat enter from explore/social/quiet, or exit after an authored end · **Observable response:** layout + combat audio shift for both seats; exit restores prior play surface · **Refusal/guard:** cannot exit mid-gated action without DM end · **Residue:** combat chrome off; any lasting costs still readable in the world
- **Seat:** shared_table · **Trigger:** surface requests resolution math for a gated action · **Observable response:** pre-compiled rule-library results are consumed (no in-surface rules authorship) · **Refusal/guard:** missing library / invalid import · **Residue:** numeric outcome feeds sensory feedback and lasting state — packs own spell/monster lists

## PoC cut

PoC proves **fight + flee/disengage + parley** ends, DM gate on a small cast, basic movement envelope, thin cast/hit feedback, and enter/exit from explore. Defer surrender/escape-with-cost tooling depth, multi-wave authoring, rich voice libraries, advanced terrain deformation, and XP/loot chrome. Full vision keeps the wider ends menu and cast ownership.

## Gate

- ok: True
- violations: []
- warnings: ['needs_pin']
