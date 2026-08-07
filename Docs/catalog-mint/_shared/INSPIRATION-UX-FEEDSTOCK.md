---
title: Inspiration UX feedstock (first-class MO)
audience: cursor_grok_operator
updated: 2026-08-07
---

# Inspiration UX feedstock (first-class MO)

**Pinable sources** (games/tools/mod ecosystems) are **not** catalog pins. From them you derive **move-pins** (pattern language) that **season** children harvest and L5 — same family as Actual-Play. Never write a game title into `conceptual_pin`.

## UX spine — three TTRPG pillars

Inspiration seasons systems under **Exploration · Roleplay · Combat**. Roleplay is not “just talking.”

| Pillar | Player face | System face (examples) |
|--------|-------------|------------------------|
| **Roleplay** | Talk, decide, perform | Factions, guilds, NPC sheets, reputation, relationship→economy |
| **Exploration** | Travel, notice, poke the world | Habitat, seasons, travel, world-as-adversary, living continuity |
| **Combat** | Orchestrate the fight | Turns, range, threat, resolution |

Cross-cutting **tools** (DM cam, situational lenses, mod seams) support pillars — they do not replace them.

## Translation job

> When a player talks about **system A** and doing **X**, they often imagine it through **game G**.  
> → Extract the **pattern** → map to **our system(s)** under pillar(s) → write **refuse**.

Overarching product lens: **multiplayer living-world fantasy with real DM/player agency in 3D** — borrow UX jobs from digital cousins; refuse skins that collapse us into single-player authored story or fixed MMO/CRPG/shooter shape.

## Mods as research

Mods mark **community-diagnosed weak spots** in a base game and show **how players augmented them** (often as stacks — Campfire with Frostfall, etc.). Research the weak part + the augmentation pattern (including placement UX that may rhyme with DM Forge glow). Prefer that signal over treating any mod as a portable feature pack.

## DM resource layer

Grand-strategy / colony sims (Stellaris, Dwarf Fortress, Civilization, Anno, …) inform a **background resource/politics engine** that helps the world feel alive. **DM override is first-class and intentional** on top of that engine — not “DM must play a 4X,” and not a sim the table cannot privilege-override. Off-screen faction/military continuity (Bannerlord-class) and indifferent permanent consequence (Kenshi-class) thicken the same “world moves without you” job.

## World shaping / midband base

Tables at midband power often expect a **base** or claimable place. Authorship should feel **Townscaper-class click-add** for placing world/grid elements (intent). Realization should be **player design → NPC background labor → calendar wait** — refuse survival-builder place-build loops (Rust/ARK as light foils only).

## Ladder

1. Pass A series **what-is** + Trinity `publish_series`  
2. **Inspiration dialogue** (Grok + user): pinable list + liked snippets → patterns until satisfied  
3. Write **`INSPIRATION-DIALOGUE-RECEIPT.md`** (mandatory)  
4. Derived move-pins; Cursor **auto-elevates** into children/L5 **seasoning only** with **trace**  
5. Pass B → Conceptual pin derive → series/children L5 (seasoned)

## Dialogue receipt (mandatory)

Path: `Roadmap/User-Story/Inspiration-UX-Feedstock/INSPIRATION-DIALOGUE-RECEIPT.md`

- Accepted derived move-pin ids  
- Explicitly rejected or deferred pins  
- Operator **satisfied** statement  

Soft backlog flag may mirror; receipt is durable. Grok does **not** declare victory.

## Derived move-pin atom

Under `cards/`: `source_title`, `liked`, `why_it_worked`, `fits_our_game`, `refuse_to_copy` (≥1), `maps_to_series[]`, optional `pillars[]` (`exploration` | `roleplay` | `combat` | `tooling`), `research_status`, `signal`, `assumption`.

## Auto-elevate

**Allowed:** children harvest seasoning; L5 seasoning / alternatives / refuse.  
**Forbidden without Decision Wrapper:** SERIES what-is; locked/validated child batches; operator-attested L5.

Mandatory ASSUMPTION-LOG fields: `assumption`, `source_snippet`, `derived_pin_id`, `maps_to_series`, `elevated_into`. Optional `divergence_from_user`.

## Grok dialogue rules

- Argue the **job** — not the game skin. Prefer **implicit** over first explicit UI latch.  
- ≥1 **refuse** per derived pin; challenge hyper-fit.  
- Mine **clusters** (e.g. open-world living cast).  
- Mods = weak-spot + community augmentation research.  
- Map pins to **pillar(s)** when possible.  
- User declares satisfied.

## Coverage

Every INDEX source → ≥1 derived move-pin. Stronger → more pins. Weak → stubs OK until a desk needs them.

## Cross-links

- [[CATALOG-MINI-TRINITY]] · [[WHAT-GOOD-LOOKS-LIKE]] · Actual-Play feedstock (parallel)  
