---
title: Half B Alpha mode — Genesis Mythos table releases
created: 2026-09-30
updated: 2026-09-30
audience: bone_pilot
status: provisional
factory_greenlit: false
---

# Half B Alpha mode

**Factory is NOT greenlit.** This note reworks the Half B (implementation) path so Alpha 0 can proceed from catalog rows without the heavy overnight / full-BOM / closed-alpha conduct ladder. Operator must manually validate, then explicitly greenlight factory operation in a later message.

## Godot stock FPS — PRECONDITIONS (enforceable)

Canonical junior law (vault / project Execution Docs — **not** duplicated here):

- `1-Projects/genesis-mythos-master/Roadmap/Execution/Docs/Godot-Implementation-Decision-Matrix.md`
- `1-Projects/genesis-mythos-master/Roadmap/Execution/Docs/Godot-Stock-Patterns.md`
- `1-Projects/genesis-mythos-master/Roadmap/Execution/Docs/PIN-stock_godot_fps.md`
- Project brief: `1-Projects/genesis-mythos-master/AGENTS.md`

```text
PRECONDITION for any Code-Exhibit write touching player / camera / look / move:
  1. Decision Matrix + Stock Patterns paths resolved
  2. Agent output quotes principle line + Player move/look matrix row
  3. Implementation matches stock CharacterBody3D pattern (not envelope-as-mover)
Missing any ⇒ pass status = invalid; do not push playable claim; do not mark Alpha Success
```

**Principle (must be quotable):** ClassDB first. Host Index binds. Never parallel physics/controller. Prefer stock Godot; extend only at seat/authority boundaries.

**Hard veto:** walk OR look fail ⇒ not Alpha Success.  
**Presentation scrap:** human “no camera difference” ⇒ typed reject `engine_pattern_miss` (not more HUD).  
**MCP:** synthetic input / automated probes are **necessary, not sufficient**. **Only operator F5** sets walk+look Done. Ban phrasing: “MCP verified walk+look.”  
See [[MCP-Playtest-WalkLook]].

### Failure taxonomy (reject codes — first-class)

| Code | Meaning |
|------|---------|
| `engine_pattern_miss` | Invented controller / free-fly-as-player / envelope-as-mover / no stock CharacterBody3D |
| `gui_input_steal` | Menu/Control permanently eats mouse/keys after Enter play |
| `seat_ok_feel_fail` | Seats/Unauthorized OK in code but walk+look still fail for human |
| `verify_mcp_only` | Agent certified feel from MCP alone |

### Little-val / hostile evidence

Claims FPS or Alpha player ready → must evidence `CharacterBody3D`, child `Camera3D`, mouse capture path, **and** matrix quote. Else `engine_pattern_miss`.

### Gates (implementation_gate_catalog)

| Gate id | Severity | Notes |
|---------|----------|--------|
| `godot_stock_fps` | **block** | Player/camera/locomotion slices |
| `operator_kinesthetic_walk_look` | **block** | Always for Alpha Success / playable push |

If a harness schema only accepts `warn` today: set warn **and** treat as block for Alpha player-camera; promote to literal block when schema allows. Prefer real `block` when supported.

## Product north star

| Term | Meaning |
|------|---------|
| **Product** | The **table** (runtime/platform): FP players, DM rail, seats, session, rules plugin host, module load slot, later LAN |
| **Modules** | Cartridges on the table |
| **We Be Goblins!-style** | **Example module pack only** — not the product name or identity |
| **Alpha** | Table + one example module playtest bar — **not** camera harness, **not** full worldgen/chargen |

Catalog rows + release tags drive implementation. Phase-6-only read locks were a temporary spike tourniquet — **not** global law.

## Release stages

| Stage | Scope |
|-------|--------|
| `alpha_0` | Offline table + one example module pack |
| `alpha_1` | Same + local LAN host/join |
| `beta` | Harden UX/seats; optional 2nd module |

Implementation **prefers** catalog rows tagged `alpha_0` before `alpha_1` / `beta`.

## Alpha 0 DONE (table product bar)

1. **Minimal front door** — Host table / pick module / enter  
2. **Session roles** — DM + player seats  
3. **Module pack load** — example goblin-style pack  
4. **FP play + DM rail + seat refuse** (stock CharacterBody3D; operator F5 for walk+look)  
5. **PF1-shaped resolution** via rules plugin host  
6. Placeholder art OK; **not** campaign ship; **not** full worldgen/chargen  

| Capability | Stage |
|------------|-------|
| `table_front_door` | alpha_0 |
| `session_roles` | alpha_0 |
| `module_pack_load` | alpha_0 |
| `rules_min_pf1` | alpha_0 |
| `seats_fp_dm` | alpha_0 |
| `stock_godot_fps` / `input_focus_contract` | alpha_0 (Execution PIN) |
| `lan_listen_server` | **alpha_1 only** |

Game write target: `5-Attachments/Code-Exhibit/genesis-mythos-alpha/`.

## Keep / Cut / Add

### Keep

- Catalog rows as authority; Code-Exhibit write target; Host Index / no invent seams  
- Roadmap Execution readonly feedstock; honesty: demo/loop ≠ campaign Success  

### Cut or defer

1. Full multi-section BOM hard-gate for alpha_0 → slim/advisory  
2. `factory_output_conduct` **block** not required to start alpha_0  
3. Overnight / headless / multi-loop conductor **not** normative for alpha_0  
4. Phase-6-only / proof-loop = product Success — non-normative  
5. Three-operator-loop UX before front door  

### Add

- This Alpha mode path + release tags + Alpha exit criteria  
- Godot Decision Matrix + Stock Patterns PRECONDITIONS (above)  
- Explicit: factory not greenlit until operator manual validation  

## Normative Alpha 0 operator path (simple)

1. Select catalog rows tagged **`alpha_0`** (incl. stock FPS pins).  
2. Satisfy Godot PRECONDITIONS if touching player/camera.  
3. Implement in Code-Exhibit.  
4. Playtest; **operator F5** for walk+look.  
5. Record honest receipt.  

**Non-normative:** `headless_eat`, overnight, multi-loop `factory_staged`, closed_alpha conduct **block** as start gate.

## Honesty

- Demo / loop / stack-green alone ≠ campaign-capable Success  
- Example module = cartridge, not product identity  
- This note does **not** turn Half B “on” (`factory_greenlit: false`)  

## Card map

| Card | Alpha mode stance |
|------|-------------------|
| `product_factory_operator_path` | Simple path normative; forbidden Success around missing FPS quote / non-stock / MCP-only feel |
| `product_factory_pipeline` | Staged; not greenlit |
| `factory_product_bom` | Slim / advisory for alpha_0 |
| `factory_output_conduct` | warn/off for alpha_0 |
| `implementation_segment_charter` | PRECONDITIONS on player/camera segments |
| `implementation_handoff_tunnel` | Catalog + release_stage |
| `implementation_gate_catalog` | `godot_stock_fps` + `operator_kinesthetic_walk_look` **block** |

## Alpha 0 implementation status

See [[Half-B-Alpha-0-Implementation-Receipt]]. Trinity does **not** host Code-Exhibit on main Docs path as game source of truth for weave law. Factory remains **not** greenlit. Walk+look remain subject to operator F5 + stock FPS gates.

## Manual validation checklist (bone pilot)

```
[ ] Alpha 0 exit criteria match table+module product
[ ] Full BOM not hard gate for alpha_0
[ ] output_conduct block not required to start alpha_0
[ ] Normative path = catalog→implement→playtest (not overnight)
[ ] Example module = cartridge, not product identity
[ ] Phase-6-only not global law
[ ] Godot PRECONDITIONS + gates godot_stock_fps / operator_kinesthetic_walk_look present
[ ] Commit pushed and hash recorded
```
