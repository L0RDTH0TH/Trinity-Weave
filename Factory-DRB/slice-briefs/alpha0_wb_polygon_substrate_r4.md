---
title: Prefer — WB-polygon-substrate r4 (moment)
created: 2026-10-24
updated: 2026-10-24
slice_id: alpha0_wb_polygon_substrate_r4
ask_id: alpha0_wb_polygon_substrate
ticket_map_id: WB-polygon-substrate
project-id: genesis-mythos-master
proof_shape: moment
claim_class: ask_success
prefer_class: foundation
factory_greenlit: false
status: prefer_b1_ready_awaiting_greenlight
para-type: Resource
tags:
  - prefer
  - ticketment
  - wb-polygon-substrate
  - moment
  - genesis-mythos-master
---

# Prefer — WB-polygon-substrate r4 (moment)

**Map row:** `WB-polygon-substrate` on [[World-Builder-Session-Prep-Ticket-Map]]  
**Kind:** moment / `ask_success` — one ugly polygon, one point, same solid stays.  
**Not:** contract yaml/index lookup. Do not Prefer-join r1–r3 archives.

## Product job (map)

Foundation — A GM can point at a low-fidelity polygon solid and that solid stays the same polygon that was pointed at.

## Structural success (this row only)

Foundation — A GM can point at a low-fidelity polygon solid and that solid stays the same polygon that was pointed at.

Point-and-stay only. Not living (`WB-sim-clock`). Not save (`WB-world-container` / `WB-world-document`). Not occupancy / hierarchy / site records. Not dials. Not flight or live rail. Not deep authoring. Art reskin is not this ticket.

## Proof

| Field | Value |
|-------|--------|
| `proof_shape` | `moment` |
| `claim_class` | `ask_success` |
| `success_object` | `point_and_stay_polygon_solid` |
| `behavior_keys` | `shows_low_fidelity_polygon` · `points_at_that_polygon` · `sees_same_polygon_after_point` · `watches_pointed_solid_stay` |
| `behavior_key_checks` | distinct proof-catalog probe ids (one probe must not green every key) |
| Operator F5 | **Required** before KEEP — stranger watches the point-and-stay act on the tiny board |

## Out of scope (section A open neighbors)

`CAMP-cast-seam`, `CAMP-create`, `CAMP-scope-split`, `CAMP-select`, `CAMP-switch`, `WB-sim-clock`, `WB-world-container`, `WB-world-document`, `WELD-one-world`

## Factory socket

- Write target: `5-Attachments/Code-Repos/genesis-mythos-align` (virgin until GREENLIGHT weld)
- `factory_greenlit: false` until operator GREENLIGHT
- Do **not** arm `WB-world-container`
- Prior Prefer/weld archives are reference only — do not Prefer-join

## Armed packet

[[alpha0_wb_polygon_substrate_r4.armed.yaml]]
