# FPS controller compare (Prefer vs tutorial)

`project.godot` **main_scene** stays `res://dev/FpsSanity.tscn` (Prefer / ours). Do not change it for this compare work.

## Scenes

| Scene | What it is | How to run |
|-------|------------|------------|
| `dev/FpsSanity.tscn` | Prefer `Player` + `PlayerFp` | F5 (main) or open + F6 |
| `dev/FpsSanityTutorial.tscn` | Same floor/lights; tutorial `PlayerTutorial` | Open scene → **F6** (Play Current Scene) |
| `dev/FpsSanityCompare.tscn` | Both players on one floor (ours x=-2, tutorial x=+2) + labels + overview cam | Open scene → **F6** |

## Controls (both FPS scenes)

- WASD move, mouse look (captured on ready)
- Esc free mouse; click to recapture
- Tutorial only: Space jump, Shift sprint; head bob + FOV juice from the tutorial pattern

## Architecture (one-liner)

- **Ours:** `CharacterBody3D` yaw + child `Camera3D` pitch (`PlayerFp`).
- **Tutorial:** `CharacterBody3D` + `Head` (Node3D) yaw + child `Camera3D` pitch (`PlayerTutorial`); move uses head basis.
