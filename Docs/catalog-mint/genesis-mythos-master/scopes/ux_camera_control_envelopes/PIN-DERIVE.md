# PIN-DERIVE — `ux_camera_control_envelopes`

- label: Perspective and control envelopes can change and cleanly return
- status: proposed
- recommended: [[Phase-4-1-Player-FP-and-Perspective-Envelope-Roadmap-2026-06-26-1705]]
- pin_focus: Perspective/control envelopes change and cleanly return (player FP vs DM WorldCam/MapCam/Sensorium)
- alternate: [[Phase-4-1-3-WorldCam-MapCam-and-SensoriumAttach-FOV-Roadmap-2026-07-16-0845]]

## Series contract (Pass B locked)

Baseline player FP and a set of explicit temporary envelopes that change perspective and/or control then hard-restore. Overrides (scry/divination, dominate, liminal/unconscious, planar/gate, absent-proxy, etc.) always return to baseline FP or the declared prior state. DM rail is first-class in the same parent: WorldCam is the DM default; MapCam, Sensorium Attach, and DM pilot are explicit departures with hard restore. Players never use WorldCam/MapCam. Every enter declares controller, presentation, duration, and return target.

## Candidates (PIN-INDEX only)

1. [[Phase-4-1-Player-FP-and-Perspective-Envelope-Roadmap-2026-06-26-1705]]
2. [[Phase-4-1-3-WorldCam-MapCam-and-SensoriumAttach-FOV-Roadmap-2026-07-16-0845]]
3. [[Phase-4-1-2-UnifiedSceneGraph-CameraInterpolatorRegistry-and-PlayerFPRig-Roadmap-2026-07-16-0828]]

## Rationale

FP + WorldCam notes cover dual-rail camera envelopes; interpolator is tertiary for transition craft.

## Operator

- [ ] confirm recommended
- [ ] confirm alternate
- [ ] waive (reason below)

waive_reason:
