---
title: Forge-style DM placement preview
schema_version: 1
source_title: Halo 3 Forge
signal: strong
research_status: operator_seed
assumption: true
liked: "Glowing placement preview with valid/invalid color, menu pick, hide toggles"
why_it_worked: "DM puts objects/monsters into the world with immediate spatial feedback"
fits_our_game: "DM World Cam placement UX for monsters/props"
refuse_to_copy:
  - "DM tools must look like Halo Forge UI"
  - "Players must use Forge to author maps"
maps_to_series:
  - ux_camera_control_envelopes
  - ux_dm_session_prep
ip_posture: pattern_only_no_clone
---

# Forge-style DM placement preview

**Job:** privileged placer sees a live preview of what they are putting down and whether it is legal/hidden.

## Refuse

- Product must clone Halo Forge chrome
- Players author the world through the same tool by default
