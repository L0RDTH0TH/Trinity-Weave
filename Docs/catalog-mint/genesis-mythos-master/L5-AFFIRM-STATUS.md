# L5-AFFIRM-STATUS — `genesis-mythos-master`

emitted_at: 2026-08-03T20:13:57.872284Z

## Per-row

| row_id | status | moments | needs_pin | violations |
|--------|--------|---------|-----------|------------|
| `ux_world_generation` | yellow | 6 | True | — |
| `ux_dm_campaign_creation` | yellow | 6 | True | — |
| `ux_player_character_creation` | yellow | 6 | True | — |
| `ux_dm_session_prep` | yellow | 6 | True | — |
| `ux_early_game` | yellow | 4 | True | — |
| `ux_mid_game` | yellow | 5 | True | — |
| `ux_late_game` | yellow | 6 | True | — |
| `ux_mental_stat_interpretation` | yellow | 5 | True | — |
| `ux_collaborative_table_agency` | yellow | 6 | True | — |
| `ux_quiet_between_pillars` | yellow | 3 | True | — |
| `ux_combat_play_surface` | yellow | 6 | True | — |
| `ux_camera_control_envelopes` | yellow | 13 | True | — |
| `ux_living_world_continuity` | yellow | 19 | True | — |
| `ux_backstory_legacy_integration` | yellow | 6 | True | — |
| `ux_world_authorship_modability` | yellow | 6 | True | — |

## Cross-row flags (max 3)

_Operator fills after digest batch is green — before attest/sign._

1. **World ≠ campaign** — worldgen + living-world vs campaign creation / session0 / tone: durable container vs bootstrap; no collapse in hard deps.
2. **Dual-rail seats** — camera (player FP vs DM WorldCam/MapCam/Sensorium/pilot) and table agency (player tools vs DM orchestration) must agree; combat must not imply identical control envelopes.
3. **Rules consumed, not owned** — combat (and resolution surfaces) stay “consumes pre-compiled rule math”; rule-engine depth stays Conceptual/Execution, not a new UX series.

Suggested checks: world ≠ campaign; dual-rail seats agree; rules consumed not owned by UX row; living-world as readable residue.
