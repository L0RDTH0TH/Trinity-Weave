# L5-AFFIRM-DIGEST — `ux_camera_control_envelopes`

- label: Perspective and control envelopes can change and cleanly return
- affirm_status: yellow
- l5_origin: pass_b_aligned
- needs_pin: true
- moment_count: 13
- thin_floor: 0

## Contract (What it is)

Baseline player FP and a set of explicit temporary envelopes that change perspective and/or control then hard-restore. Overrides (scry/divination, dominate, liminal/unconscious, planar/gate, absent-proxy, etc.) always return to baseline FP or the declared prior state. DM rail is first-class in the same parent: WorldCam is the DM default; MapCam, Sensorium Attach, and DM pilot are explicit departures with hard restore. Players never use WorldCam/MapCam. Every enter declares controller, presentation, duration, and return target.

## Moments

- **Seat:** player, dm_as_player, privileged_access · **Trigger:** enter `ux_absent_proxy` · **Observable response:** When a player is absent, their PC stays in the shared fiction via a session-policy delegate (another player or the DM) who receives that character's controls so the DM is not forced to run monsters and the missing PC at  · **Refusal/guard:** out of contract / wrong seat · **Residue:** lasting readable state from this moment
- **Seat:** player, dm_as_player, privileged_access · **Trigger:** enter `ux_agency_handoff_enter_exit` · **Observable response:** How enter and exit of a control or perspective handoff feel at the table — liminal timing, who sees the transfer, and the social beat of taking or releasing the stick — without restating the parent's declare-controller / · **Refusal/guard:** out of contract / wrong seat · **Residue:** lasting readable state from this moment
- **Seat:** player, dm_as_player, privileged_access · **Trigger:** enter `ux_baseline_fp` · **Observable response:** Default embodied play — what the human sees and touches in this pillar (under Perspective and control envelopes can change and cleanly return). · **Refusal/guard:** out of contract / wrong seat · **Residue:** lasting readable state from this moment
- **Seat:** player, dm_as_player, privileged_access · **Trigger:** enter `ux_baseline_fp_controls` · **Observable response:** How move, look, and intent issuance feel and where control surfaces sit relative to first-person view (under Perspective and control envelopes can change and cleanly return). · **Refusal/guard:** out of contract / wrong seat · **Residue:** lasting readable state from this moment
- **Seat:** player, dm_as_player, privileged_access · **Trigger:** enter `ux_divination_override` · **Observable response:** Temporary rules-bound departure from baseline FP for remote sensing (scry, clairvoyance, find path, and kin) (under Perspective and control envelopes can change and cleanly return). · **Refusal/guard:** out of contract / wrong seat · **Residue:** lasting readable state from this moment
- **Seat:** player, dm_as_player, privileged_access · **Trigger:** enter `ux_dm_mapcam` · **Observable response:** Map-fixed orthographic DM rail — tokens, measurements, fog, LOS adjudication feel (under Perspective and control envelopes can change and cleanly return). · **Refusal/guard:** out of contract / wrong 

## PoC cut

First cut proves the parent contract with a small surface set (`ux_absent_proxy`, `ux_agency_handoff_enter_exit`); defer `ux_baseline_fp`, `ux_baseline_fp_controls`, `ux_divination_override`, `ux_dm_mapcam` and deeper chrome. Keep anti-mandate and authored structure menus honest.

## Gate

- ok: True
- violations: []
- warnings: ['needs_pin']
