---
title: Half B Alpha 0 — implementation receipt (public)
created: 2026-09-30
updated: 2026-09-30
audience: bone_pilot
status: provisional
factory_greenlit: false
release_stage: alpha_0
---

# Alpha 0 implementation receipt

**Factory is NOT greenlit.** This is a public Trinity receipt that Alpha 0 **table + example module** work landed in the vault game tree. Trinity-Weave does **not** host game source (`5-Attachments/` is forbidden on this remote).

## What landed (capabilities)

| Capability | Status | Primary paths (vault / Curator private) |
|------------|--------|----------------------------------------|
| `table_front_door` | implemented | `…/src/Genesis/Table/FrontDoorUi.cs`, `GameSessionRoot.cs` |
| `session_roles` | implemented | `…/src/Genesis/Table/SessionRoleBoard.cs` |
| `module_pack_load` | implemented | `…/src/Genesis/Module/ModulePackLoader.cs`, `ModulePackModels.cs`, `content/packs/example_goblin_oneshot/` |
| `rules_min_pf1` | implemented (shaped) | `…/rules/pathfinder_pf1/`, `…/src/Genesis/Rules/RulesHosts.cs` |
| `seats_fp_dm` | implemented | `…/src/Genesis/Table/TablePlaySession.cs` (+ existing seat/camera hosts) |
| `lan_listen_server` | **not** Alpha 0 | deferred to `alpha_1` |

Root game path: `5-Attachments/Code-Repos/genesis-mythos-alpha/genesis-mythos/`

## Example cartridge (original placeholder — not Paizo text)

Pack id: `example_goblin_oneshot`

| File | Role |
|------|------|
| `content/packs/example_goblin_oneshot/pack.json` | Stable id, honesty banner, `release_stage: alpha_0` |
| `pregens.json` | 4 example goblin PCs (placeholder stats) |
| `sites.json` | Cave Mouth Path + Scrap Clearing |
| `beats.json` | Stealth DC 12 check + short scrap vs placeholder mongrel |

Honesty in pack: original example cartridge for Alpha 0 — **not** a licensed adventure dump. **No PDF** in the game tree.

## Excluded from any public surface

- `Ingest/PZO9500-9E_WeBeGoblinsFree.pdf` (and any Paizo / We Be Goblins copyrighted text dumps)
- Vault-private notes, queues, `.technical/parallel/`, Curator-only operator state
- Claiming factory greenlight or CampaignCapable from this receipt

## Where the code actually lives

| Lane | Remote / path | Role |
|------|----------------|------|
| **Curator private** | `L0RDTH0TH/Curator` via vault backup (`gmm-curator-export`) | Full vault including Code-Repos Alpha 0 |
| **Trinity-Weave public** | this repo — `Docs/` receipts + Half B Alpha mode | Weave law + operator visibility; **not** game tree |
| **GMMR public** | `L0RDTH0TH/genesis-mythos-master-roadmap` | Roadmap / integration contract only — **not** Code-Repos |

There is **no** dedicated public game remote configured in Second-Brain-Config. Residual gap: Alpha 0 **source** is Curator-private until an operator-owned public game export is added.

## Private backup hash (Curator)

Curator commit that mirrored Alpha 0 game files (private):

- `5096d7dcb` — `auto: 2026-09-30T00:44:41-04:00 — Cursor task: Alpha 0: table front door + example goblin module pack + PF1-min session (offline)`

## Play bar (local)

See game `README.md` under Code-Repos: Host table → pick `example_goblin_oneshot` → Enter play → Player/DM seats → skill check / skirmish. Offline only.

## Related

- [[Half-B-Alpha-Mode]] — normative Alpha mode path (factory still not greenlit)
- Game write target remains Code-Repos; Trinity stays weave + docs
