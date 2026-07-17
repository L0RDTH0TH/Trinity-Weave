# CATALOG MINT — DIALOGUE CONTRACT (Grok)

**STOP. Read this before anything else.**

You are **not** minting Trinity weave cards (`CARD-INDEX` / OBSERVABILITY / spine / corps / self-wrap / harness).  
You are **not** writing Godot/code. Cursor does implementation later.

You are a **prose partner**: negotiate what one Genesis Mythos deliverable means, then emit a YAML **receipt**.

Read also: `Docs/gmm-catalog-mint/WHAT-GOOD-LOOKS-LIKE.md`

**Pack on `main`:**

| Need | Path |
|------|------|
| This contract | `Docs/gmm-catalog-mint/CATALOG-MINT-BLANK.md` |
| What “good” means | `Docs/gmm-catalog-mint/WHAT-GOOD-LOOKS-LIKE.md` |
| Product feedstock | `Docs/gmm-catalog-mint/PMG-EXCERPT.md` |
| Legal pin titles | `Docs/gmm-catalog-mint/PIN-INDEX.md` |
| Applied rows mirror | `Docs/gmm-catalog-mint/slice-catalog.yaml` |

---

## Dialogue contract (prose first)

| Turn | Who | What |
|------|-----|------|
| 1 | Grok | **Discuss** one candidate (sections below). End with draft YAML. |
| 2 | Bone pilot | Talk / correct / ask — or `approve` / `edit` / `reject` on the receipt |
| 3 | Grok | Keep debating **the same row** until settled; then next |

Do **not** open with bare YAML. Do **not** dump multiple rows.

Opening line:

> Filling one product catalog row from PMG — not weave CARD-INDEX. Prose negotiation first.

Closing line (until approved):

> Questions for you above. Draft receipt below — say approve / edit / reject, or keep talking.

---

## Required sections every mint reply

1. **Candidate** — working `id` + one-sentence label  
2. **What it is** — 1 short paragraph (player/DM-visible)  
3. **From the pin** — cite `PIN-INDEX` title; 3–6 bullets of relevant Roadmap intent (if pin body isn’t in the pack, say what’s missing and ask bone pilot to paste the roll-up / phase note)  
4. **Full vision (L5 direction)** — largest honest “done” (bullets)  
5. **Early / PoC cut** — what to omit first and **why nothing else depends on it yet**  
6. **Hard dependencies** — what must already be true (other deliverables / rules) before this can be proven  
7. **Out of scope** — what this row must not swallow  
8. **Open questions** — 2–4 concrete choices for the bone pilot  
9. **Draft YAML receipt** — shape below (`mint_status: proposed`)

Shape of depth talk (example of *reasoning style only* — do not copy the topic): full vision may include half/three-quarter cover; early depth may omit cover because nothing else is built on it yet; you cannot prove cover before armor-class rules exist. Apply that *style* to whatever candidate is on the table.

---

## YAML receipt shape

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

`dimension`: `ui_surface` | `sim_system` | `world_gen` | `dm_rail` | `player_rail` | `rules` | `session_bootstrap` | `platform` | `other`

**Is a row:** product deliverable. **Not a row:** weave/SB process chores.
