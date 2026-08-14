# L5-AFFIRM-DIGEST — `ux_mental_stat_interpretation`

- label: Mental stats surface available read paths not only sheet numbers
- affirm_status: yellow
- l5_origin: pass_b_aligned
- needs_pin: true
- moment_count: 5
- thin_floor: 4

## Contract (What it is)

INT, WIS, and CHA can drive visual cues on people, places, and objects that hold relevant information. The cue signals that a mental-stat path is available — it does not spill the content. Cues are stat-gated per player where appropriate; the DM can place or fire cues. Structure menu for presentation, not auto-solving the interaction and not one social-scene skin.

## Moments

- **Seat:** shared_table (player) · **Trigger:** player approaches a person/place/object that holds relevant information · **Observable response:** a mental-stat cue appears (or stays absent) without spilling the content · **Refusal/guard:** low stats may hide *this* cue, not all social information · **Residue:** player knows a read path exists
- **Seat:** player · **Trigger:** player inspects / follows the cue (check or roleplay start) · **Observable response:** presentation structure menu opens (diegetic vs highlight, etc.) toward a read path · **Refusal/guard:** cue does not auto-reveal facts without check or roleplay · **Residue:** success/fail leaves knowledge state — not a romance-tree unlock by default
- **Seat:** privileged_access (DM) · **Trigger:** DM places or fires a cue · **Observable response:** armed cue becomes available to eligible seats · **Refusal/guard:** cues are not DM-only with zero player affordance once armed · **Residue:** cue remains until resolved or cleared
- **Seat:** shared_table · **Trigger:** visibility policy applies (per-player vs party-shared) · **Observable response:** only eligible players see the cue · **Refusal/guard:** cannot force one insight-beat as the only presentation · **Residue:** asymmetric information stays honest to the table contract
- **Seat:** player · **Trigger:** player declines or walks past the cue · **Observable response:** no auto-solve; content stays sealed · **Refusal/guard:** system does not dump sheet-number chrome as the whole product · **Residue:** world unchanged; cue may persist for later

## PoC cut

PoC proves **cue appears → player inspects → content stays sealed until check/roleplay**, with DM place/fire and simple per-player visibility. Defer always-on auras, dense mental-stat texture, and multi-presentation polish. Full vision keeps the structure menu of cue styles.

## Gate

- ok: True
- violations: []
- warnings: ['needs_pin']
