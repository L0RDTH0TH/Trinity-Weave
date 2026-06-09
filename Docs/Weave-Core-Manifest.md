---
title: Weave Core Manifest (light public slice)
created: 2026-06-09
tags: [weave, trinity-weave, phase-18, grok]
---

# Weave Core Manifest (light public slice)

**Public repo:** [L0RDTH0TH/Trinity-Weave](https://github.com/L0RDTH0TH/Trinity-Weave)  
**Authority:** locked meta `trinity_weave_public_export` + `public_surface_topology`  
**Not included:** project factory output (`1-Projects/`, `Roadmap/`, `Ingest/`, game code)

## Purpose

Light Phase 18 distribution for **Grok** and external readers: weave maintenance grammar, filled meta, host-weld law. Second Brain vault remains private (Curator); this repo is the **weave design corpus** only.

## Shipped layers

| Layer | Export path | Notes |
|-------|-------------|-------|
| Weave Python | `scripts/eat_queue_core/weave/` | Maintenance spine, schedule, harness entry |
| Schedule plane | `scripts/eat_queue_core/schedule_*.py`, `pseudo_clock.py` | Background rhythm |
| Locked meta YAML | `weave/components/*.yaml` | Filled doctrine cards |
| Registry | `weave/trinity-partition-registry.yaml` | Maintenance partition ids |
| Host weld law | `weave/host-weld/live/`, `manifest.yaml` | Compiled execution gates |
| Bridge socket | `Docs/Rules/host-weld-bridge.mdc` | Reference copy of Cursor bridge |
| Design docs | `Docs/Weave-Core-Manifest.md`, `Docs/External-Weave-Handoff.md`, `Docs/Maintenance-Trinity-Constitution.md` | Operator + Grok context |
| Grok pointer | `Docs/Grok-Trinity-Weave-Context.md` | Navigation for GitHub-linked Grok |

## Locked meta ids (public)

- `trinity_prompt_context`
- `harness_runtime_contract`
- `schedule_event_planes`
- `cursor_host_adapter`
- `persona_atlas`
- `vault_layout_naming_doctrine`
- `agent_implementation_style`
- `factory_lifecycle_doctrine`
- `maintenance_honesty_anchor`
- `config_knob_parity`
- `host_execution_safety_contract`
- `trinity_card_authoring`
- `conceptual_style_guide`
- `public_surface_topology`
- `trinity_weave_public_export`

## Forbidden (never published here)

- `1-Projects/**`, `2-Areas/**`, `Ingest/**`, `Roadmap/**`, `5-Attachments/**`
- `.technical/parallel/**` (runtime queues, institute state)
- `component-proposals/` (provisional churn)
- Full `.cursor/` tree (ops agents/skills — see integration mirror on `genesis-mythos-master-roadmap`)

## Publish harness

**Manual:**

```bash
PYTHONPATH=scripts python3 -m scripts.eat_queue_core.harness weave_public_sync --vault-root .
```

**Automatic (pseudo-clock):** `schedule_tick` listener plane runs change-gated `weave_public_publish` every tick (when allowlisted fingerprint changes). Commits use `chore(weave): schedule_tick tick=N external-backup sync`. State: `schedule.json` → `weave_publish_fingerprint`, `last_weave_publish_at`.

Config: `Second-Brain-Config.md` § `weave_publish` + `schedule_planes.weave_publish_*`.

## Related surfaces

| Surface | Repo | Use |
|---------|------|-----|
| Curator private | `gmm-curator-export` | Full vault backup |
| Weave public | **Trinity-Weave** | Grok weave/design |
| Integration mirror | `genesis-mythos-master-roadmap` | Queue/automation ops |
| Engine roadmap | same, per-track branches | Factory Roadmap output only |
