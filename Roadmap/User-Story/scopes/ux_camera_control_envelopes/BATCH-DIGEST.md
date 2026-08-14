---
title: Batch digest — ux_camera_control_envelopes
parent_id: ux_camera_control_envelopes
walk_surface: batch_digest
---

# Batch digest — `ux_camera_control_envelopes`

**Parent:** Perspective and control envelopes can change and cleanly return
**Contract:** Baseline player FP and a set of explicit temporary envelopes that change perspective and/or control then hard-restore. Overrides (scry/divination, dominate, liminal/unconscious, planar/gate, absent-proxy, etc.) always return to baseline FP or the declared prior state. DM rail is first-class in the same parent: WorldCam is the DM default; MapCam, Sensorium Attach, and DM pilot are explicit departures with hard restore. Players never use WorldCam/MapCam. Every enter declares controller, presentation, duration, and return target.

**Parent does_not_mandate (inherit — do not re-litigate):**
- players get free third-person orbit as default
- DM tools exist only as debug infrastructure
- envelope exits leave soft residual control or wrong perspective
- camera modes can become permanent without a restore path
- players may use WorldCam or MapCam as free exploration seats

Child surface: `inherits_parent_anti_mandate` + **local** `alternatives_not_banned`.
Missing local alternatives = **yellow** (polish), not red re-scope.
Open full `WALK.md` only for yellow / red / thin ids.

| id | status | inherits | alt_n | alternatives_not_banned | local_does_not_mandate | summary |
|----|--------|----------|-------|-------------------------|------------------------|---------|
| `ux_absent_proxy` | done | yes | 2 | Volunteer delegate vs DM-proposed vote for who holds the stick; Soft revoke on owner return vs hard cutover with table ack |  | When a player is absent, their PC stays in the shared fiction via a session-policy delegate (another player or the DM) who receives that character's controls so the DM is not forced to run monsters and the missing PC at once. Table may volunteer a delegate, or the DM may propose a vote and players choose who is stuck with it; policy is per-session and revocable when the owner returns. This is an agency / control envelope under camera-control — not Sensorium (read-only sight) and not permanent ownership transfer. |
| `ux_agency_handoff_enter_exit` | done | yes | 2 | Sparse vs rich transfer chrome at enter/exit; Quiet stick-pass vs announced table beat |  | How enter and exit of a control or perspective handoff feel at the table — liminal timing, who sees the transfer, and the social beat of taking or releasing the stick — without restating the parent's declare-controller / hard-restore law. |
| `ux_baseline_fp` | done | yes | 2 | Minimal HUD vs richer diegetic embodiment chrome; Strict FP-only default vs rare comfort assists that still restore to FP |  | Default embodied play — what the human sees and touches in this pillar (under Perspective and control envelopes can change and cleanly return). |
| `ux_baseline_fp_controls` | done | yes | 2 | Gesture-light vs denser intent surfaces in FP; Look-then-act vs simultaneous look/move issuance |  | How move, look, and intent issuance feel and where control surfaces sit relative to first-person view (under Perspective and control envelopes can change and cleanly return). |
| `ux_divination_override` | done | yes | 2 | Sparse vs frequent rules-bound remote-sense use; Thin scry pane vs fuller remote presentation that still hard-restores |  | Temporary rules-bound departure from baseline FP for remote sensing (scry, clairvoyance, find path, and kin) (under Perspective and control envelopes can change and cleanly return). |
| `ux_dm_mapcam` | done | yes | 2 | Measurement-first MapCam vs token/fog-first layout; Rare MapCam dips vs frequent grid adjudication |  | Map-fixed orthographic DM rail — tokens, measurements, fog, LOS adjudication feel (under Perspective and control envelopes can change and cleanly return). |
| `ux_dm_pilot` | done | yes | 2 | Session-policy DM pilot vs rules-triggered only; Brief pilot envelopes vs longer possession-like duration (still restore) |  | When session/rules put the DM in control of an entity via pilot envelope (under Perspective and control envelopes can change and cleanly return). |
| `ux_dm_sensorium` | done | yes | 2 | Strict read-only bind vs annotated LOS helpers that never transfer intent; Short Sensorium peeks vs sustained watch |  | Read-only sight bind to an entity — no intent transfer; adjudicate what they see (under Perspective and control envelopes can change and cleanly return). |
| `ux_dm_worldcam` | done | yes | 2 | DM who rarely leaves WorldCam vs frequent MapCam/Sensorium/pilot use; Comfort-smooth WorldCam motion vs snappy cuts (final state still explicit) |  | Free-flight DM observation rail — how mastery feels in this pillar (under Perspective and control envelopes can change and cleanly return). |
| `ux_dominate_pilot` | done | yes | 2 | Thin vs fuller dominate-pilot embodiment in early builds; Strict rules-duration vs session-extended pilot that still hard-restores |  | Dominator pilots the target — FP and control from the dominated body (under Perspective and control envelopes can change and cleanly return). |
| `ux_dominate_victim` | done | yes | 2 | Sparse vs rich passenger / liminal chrome for the victim; Locked-input only vs light passenger cues without restoring control early |  | Victim presentation during dominate — passenger FP, locked input, liminal chrome (under Perspective and control envelopes can change and cleanly return). |
| `ux_liminal_unconscious` | done | yes | 2 | Sparse vs rich liminal/unconscious presentation; Hard blackout vs soft liminal that still returns to baseline |  | Status-bound liminal or unconscious presentation and return to baseline (under Perspective and control envelopes can change and cleanly return). |
| `ux_planar_travel_override` | done | yes | 2 | Brief gate flash vs longer planar transition presentation; Rules-only planar departures vs session-flavored transitions (still restore) |  | How planar travel or gate-like transitions feel as temporary perspective/agency departures (under Perspective and control envelopes can change and cleanly return). |
