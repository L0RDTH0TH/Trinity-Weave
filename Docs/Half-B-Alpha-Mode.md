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

Implementation **prefers** catalog rows tagged `alpha_0` before `alpha_1` / `beta`. Rows should carry a `release_stage` (or equivalent) tag; project-branch catalog YAML may still be catching up — treat this as normative wire target.

## Alpha 0 DONE (table product bar)

Not a spine/demo bar. Done when:

1. **Minimal front door** — Host table / pick module / enter
2. **Session roles** — DM + player seats
3. **Module pack load** — example goblin-style pack: pregens, 1–2 sites, 1 check, 1 skirmish
4. **FP play + DM rail + seat refuse**
5. **PF1-shaped resolution** via rules plugin host
6. Placeholder art OK; **not** campaign ship; **not** full worldgen/chargen

### First Alpha 0 capability list (provisional names)

| Capability | Stage |
|------------|-------|
| `table_front_door` | alpha_0 |
| `session_roles` | alpha_0 |
| `module_pack_load` | alpha_0 |
| `rules_min_pf1` | alpha_0 |
| `seats_fp_dm` | alpha_0 (existing shell OK as feedstock) |
| `lan_listen_server` | **alpha_1 only** — do not implement under Alpha 0 |

Game write target: `5-Attachments/Code-Repos/genesis-mythos-alpha/` (or the project's declared Code-Repos path).

## Keep / Cut / Add

### Keep

- Catalog rows as authority for what gets implemented
- Game repo write target under Code-Repos
- Host Index / no invent seams
- Roadmap Execution as **readonly feedstock** (no infinite Execution-tree deepen as Half B)
- Honesty: demo/loop alone ≠ campaign-capable Success

### Cut or defer (pre-greenlight Half B)

1. **Full multi-section factory BOM** — must not block writing Alpha 0 code. For `alpha_0`: slim BOM (`product` + `build_progress`) hard-gates; other sections **advisory**. Full BOM → beta / closed_alpha honesty.
2. **`factory_output_conduct` block mode** — not required to start Alpha 0. Default **warn** (or **off**) for `alpha_0`; **block** only when operator explicitly promotes a ship claim.
3. **Overnight / headless / multi-loop product conductor** — **not** normative for Alpha 0.
4. **Phase-6-only** or “proof-loop receipts = product Success” — remove / mark non-normative.
5. **Three-operator-loop UX theater** — not required before a table front door exists.

### Add

- This Alpha mode operator path
- Release-stage tags on the implementation path
- Alpha 0 / Alpha 1 exit criteria (below)
- Explicit: factory not greenlit until operator manual validation

## Normative Alpha 0 operator path (simple)

1. Select catalog rows tagged **`alpha_0`** (prefer over alpha_1/beta).
2. Implement in the game repo (`genesis-mythos-alpha` / declared Code-Repos).
3. Playtest the table + example module cartridge.
4. Record a receipt (honest: what worked / what is stub).

**Non-normative for Alpha 0:** `headless_eat`, `headless_overnight`, multi-loop `factory_staged` conductor, three-operator-loop UX before front door, closed_alpha conduct **block**.

Config hooks (when vault Config is present):

- `factory_orchestrator.implementation_release_stage: alpha_0 | alpha_1 | beta`
- `factory_orchestrator.factory_output_trinity_gate: off | warn | block` — for alpha_0 prefer `warn` or `off`; use `block` only for ship claims
- Product-factory state may mirror `implementation_release_stage` under `product_factory`

## Alpha 1 exit criteria (preview)

Alpha 0 bar **plus** local LAN host/join (`lan_listen_server`). Still not campaign ship; still not full worldgen/chargen.

## Honesty

- Demo / loop / stack-green alone ≠ campaign-capable Success
- Example module = cartridge, not product identity
- This rework does **not** turn Half B “on”

## Card map

| Card | Alpha mode stance |
|------|-------------------|
| `product_factory_operator_path` | Simple catalog→implement→playtest path is normative for alpha_0 |
| `product_factory_pipeline` | Staged; not greenlit; loops not required before front door |
| `factory_product_bom` | Slim / advisory for alpha_0 |
| `factory_output_conduct` | warn/off for alpha_0; block only on ship promote |
| `implementation_segment_charter` | Release tags + table product bar |
| `implementation_handoff_tunnel` | Catalog + release_stage in hand-off |
| `implementation_gate_catalog` | Alpha capabilities, not M0–M8 demo ladder as product Success |

## Manual validation checklist (bone pilot)

Copy/paste after reviewing the push:

```
[ ] Alpha 0 exit criteria written and match table+module product
[ ] Full BOM is not a hard gate for alpha_0
[ ] output_conduct block is not required to start alpha_0
[ ] Normative path is simple implement-from-catalog-rows, not overnight conductor
[ ] Example module is explicitly a cartridge, not product identity
[ ] Phase-6-only is not global law
[ ] Commit pushed and hash recorded
```

After checklist pass, operator may explicitly greenlight factory operation in a later message.
