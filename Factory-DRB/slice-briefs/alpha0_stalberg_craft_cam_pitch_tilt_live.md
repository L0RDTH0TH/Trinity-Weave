---
title: Craft cam pitch tilt — separate LIVE (not Prefer Success)
created: 2026-10-04T19:58:20Z
slice_ref: alpha0_stalberg_dual_art_style_r1
camera_altitude: separate_from_art_prefer
live_path: 5-Attachments/Code-Repos/genesis-mythos-alpha-20260930/genesis-mythos/Camera/CraftPlanarCamRig.cs
---

# Craft cam pitch tilt (same session, separate action)

| Knob | Before | After |
|------|--------|-------|
| `PitchDegrees` | −72 (unused; pose ≈ atan(3850/875) ≈ **77°** look-down) | **−40°** default (drives pose) |
| Pitch band | n/a | **−55° … −35°** (look-down 35–55°) |
| `CameraDistance` | 875 (horizontal) | **2200** (horizontal at default pitch) |
| `CameraHeight` | 3850 (independent) | **derived** `distance * tan(|pitch|)` ≈ 1845 @ 40° |
| Orbit | 360° yaw (Q/E + MMB X) | unchanged + **MMB Y adjusts pitch** |
| Pan / zoom | WASD + wheel | unchanged |

Taxonomy: `vtt_planar_ortho` / craft envelope — planar lock + slight angle (Camera-Mode-Taxonomy-Live). Matrix Prefer (player FPS row) not this seat; craft cam is host-selected envelope.
