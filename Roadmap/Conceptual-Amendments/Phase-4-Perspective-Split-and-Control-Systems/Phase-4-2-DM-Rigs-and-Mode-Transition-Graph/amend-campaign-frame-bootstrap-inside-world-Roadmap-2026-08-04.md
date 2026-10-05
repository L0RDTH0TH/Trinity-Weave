---
title: amend-campaign-frame-bootstrap-inside-world-Roadmap-2026-08-04
parent_roadmap_note: "[[Phase-4-2-1-TransitionGuardRegistry-and-DM-Session-Authority-Roadmap-2026-07-16-0456]]"
amends_section: "## Behavior"
frozen_parent_at_handoff: "2026-07-17T05:59:24Z"
color_key: Orange
tags:
  - conceptual-amendment
  - genesis-mythos-master
  - campaign-frame
  - pin-weld
para-type: Project
project-id: genesis-mythos-master
roadmap_track: conceptual
status: active
created: 2026-08-04
links:
  - "[[Phase-4-2-1-TransitionGuardRegistry-and-DM-Session-Authority-Roadmap-2026-07-16-0456]]"
  - "[[genesis-mythos-master-goal]]"
---

# Campaign frame bootstrap inside an existing world

**Amends:** [[Phase-4-2-1-TransitionGuardRegistry-and-DM-Session-Authority-Roadmap-2026-07-16-0456#Behavior]]

## Intent

Post-freeze companion so catalog row `ux_dm_campaign_creation` has an honest Conceptual weld for **campaign-frame bootstrap inside a durable world** — not worldgen, not Horizon demo loop, not app Launch-Flow / DevLeakageGuard alone.

## Behavior (amendment weld)

DM/orchestrator authors or revises a **campaign frame** as a player-facing authorship act **inside** an attached world:

1. Bound the frame: tone, public facts, cast expectations, logging/chronicle seam, exit to world or session prep.
2. Require **DM session authority** (parent TransitionGuardRegistry) so frame edits and mode transitions stay in collaborative table — FP↔DM guards still apply.
3. Attach to an **existing or newly attached world container** — never collapse into Phase-2 worldgen; never treat demo Horizon loop as product campaign parent.
4. Exit paths: hand to session prep / spawn bootstrap for cast entry; do not own PC creation.

## Scope

**In:** campaign-frame bootstrap contract; world-attachment precondition; authority-gated frame edits; public-fact / cast-expectation surfaces.

**Out:** world generation; LaunchFlow DevLeakageGuard; Horizon demo gameplay loop as law; player character creation; factory/L5; Execution serializers.

## Why not parent Behavior alone

Parent `## Behavior` licenses transition guards / session authority machinery. It does **not** license “campaign frame inside world” product Meaning. This amendment is the missing span for L5 **and** later Execution feedstock.

## Pin weld

- Catalog row: `ux_dm_campaign_creation`
- Role: **primary** Conceptual pin after dual-approve mint
- Parent remains **supporting** (session-authority machinery)
- Horizon Demo remains **contrast**
