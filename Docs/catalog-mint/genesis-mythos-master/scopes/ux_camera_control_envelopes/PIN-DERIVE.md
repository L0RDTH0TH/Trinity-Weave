# PIN-DERIVE — `ux_camera_control_envelopes`

- label: Perspective and control envelopes can change and cleanly return
- status: proposed
- schema: pin_v2
- recommended: [[Phase-4-1-Player-FP-and-Perspective-Envelope-Roadmap-2026-06-26-1705]]
- pin_focus: Perspective/control envelopes change and cleanly return (player FP vs DM cams)
- alternate: [[Phase-4-1-3-WorldCam-MapCam-and-SensoriumAttach-FOV-Roadmap-2026-07-16-0845]]
- vision_drift: false
- vision_drift_cite: _(none)_

## conceptual_pin_refs

- title: [[Phase-4-1-Player-FP-and-Perspective-Envelope-Roadmap-2026-06-26-1705]] | heading: ## Behavior | role: primary | excerpt_note: Player FP / perspective envelope machinery | color_key: Cyan
- title: [[Phase-4-1-3-WorldCam-MapCam-and-SensoriumAttach-FOV-Roadmap-2026-07-16-0845]] | heading: ## Behavior | role: supporting | excerpt_note: DM WorldCam/MapCam/Sensorium envelopes | color_key: Blue

## mint_target

_(none — Grok mint gate owns volume)_

## Series contract (Pass A / Trinity published)

Baseline player FP and a set of explicit temporary envelopes that change perspective and/or control then hard-restore. Overrides (scry/divination, dominate, liminal/unconscious, planar/gate, absent-proxy, etc.) always return to baseline FP or the declared prior state. DM rail is first-class in the same parent: WorldCam is the DM default; MapCam, Sensorium Attach, and DM pilot are explicit departures with hard restore. Players never use WorldCam/MapCam. Every enter declares controller, presentation, duration, and return target.

## Candidates (PIN-INDEX only)

1. [[Phase-4-1-Player-FP-and-Perspective-Envelope-Roadmap-2026-06-26-1705]]
2. [[Phase-4-1-3-WorldCam-MapCam-and-SensoriumAttach-FOV-Roadmap-2026-07-16-0845]]
3. [[Phase-4-1-2-UnifiedSceneGraph-CameraInterpolatorRegistry-and-PlayerFPRig-Roadmap-2026-07-16-0828]]

## Rationale

FP envelope is structure; WorldCam/MapCam supporting for dual-rail cams.

## Operator

- [ ] confirm recommended
- [ ] confirm alternate
- [ ] waive (reason below)

waive_reason:

_Excerpt = weld; heading = locator. Pack PIN-EXCERPTS must match cited spans._

_Shared pin gate also requires INSPIRATION-SEASONING-RECEIPT `inspiration_seasoning_disposition: applied|waived` (waive needs reason)._
