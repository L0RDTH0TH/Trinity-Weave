# CATALOG MINT — DIALOGUE CONTRACT (Grok)

**STOP. Read this before anything else.**

You are **not** minting Trinity weave cards (`CARD-INDEX` / OBSERVABILITY / spine / corps / self-wrap / harness).

You are negotiating **one Genesis Mythos product deliverable row at a time**.

**Where (on this repo `main`):**

| Need | Path |
|------|------|
| This contract | `Docs/gmm-catalog-mint/CATALOG-MINT-BLANK.md` |
| Product feedstock | `Docs/gmm-catalog-mint/PMG-EXCERPT.md` |
| Legal pin titles | `Docs/gmm-catalog-mint/PIN-INDEX.md` |
| Applied rows mirror | `Docs/gmm-catalog-mint/slice-catalog.yaml` |

Bone pilot + Cursor apply approvals into the vault; you only propose.

---

## Dialogue contract

| Turn | Who | What |
|------|-----|------|
| 1 | Grok | Propose **exactly one** candidate row |
| 2 | Bone pilot | `approve` / `edit` / `reject` |
| 3 | Grok | Settle that slot only; then next |

Opening line every reply:

> Filling one product catalog row from PMG — not weave CARD-INDEX. Awaiting approve / edit / reject.

Closing line every reply:

> Bone pilot: `approve` / `edit` / `reject`. No next row until settled.

---

## Row shape (copy exactly)

```yaml
  - id: snake_case_deliverable_noun
    dimension: ui_surface
    label: Human-readable deliverable name
    planned: true
    mint_status: proposed
    conceptual_pin: "[[Exact-Title-From-PIN-INDEX]]"
    execution_pins: []
    depends_on: []
    touchstone_refs: []
```

`dimension` one of: `ui_surface` | `sim_system` | `world_gen` | `dm_rail` | `player_rail` | `rules` | `session_bootstrap` | `platform` | `other`

**Is a row:** player/DM/world/sim deliverable (Session 0, WorldCam, player-lite, …).  
**Not a row:** weave integration, roadmap scaffold, catalog population, PMG mapping.

`conceptual_pin` must be a title from `PIN-INDEX.md` — or say `needs pin` and list candidates from that file. Never invent links.
