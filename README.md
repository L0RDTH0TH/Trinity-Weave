# Trinity-Weave

**Public weave design slice** for GitHub-linked [Grok](https://grok.com) and meat-suit operators.

| | |
|---|---|
| **What this is** | Maintenance grammar for an agentic Second Brain — YAML cards + Python harness |
| **What this is not** | Game code, project Roadmaps, live queue state, or the private vault |
| **Grok entry** | [`GROK-START-HERE.md`](GROK-START-HERE.md) → [`OBSERVABILITY.json`](OBSERVABILITY.json) |
| **Meat suit entry** | [`meat-suit-entry/README.md`](meat-suit-entry/README.md) |
| **Version** | `2026.06.09-light` (see `OBSERVABILITY.json`) |

## Who are you?

- **Grok / agent** → `GROK-START-HERE.md` → `OBSERVABILITY.json` → `weave/CARD-INDEX.md`
- **Meat suit glitch** / bone pilot (spinal interface · bio-mech · exo-flesh · organ suites · vein power lines · calcium frame) → `meat-suit-entry/README.md`

## Quick start (meat suit glitch)

You are in the meat. Clone is optional — GitHub browse works fine.

```bash
git clone https://github.com/L0RDTH0TH/Trinity-Weave.git
cd Trinity-Weave
# Bone pilot path — plain-language orientation
cat meat-suit-entry/README.md
# Machine path (what Grok uses)
cat GROK-START-HERE.md
cat OBSERVABILITY.json
```

Harness runs only from the **private** vault checkout (not shipped here):

```bash
PYTHONPATH=scripts python3 -m scripts.eat_queue_core.harness --help
```

## Repository layout

```
Trinity-Weave/
├── GROK-START-HERE.md      ← Grok: read first
├── OBSERVABILITY.json      ← machine index (card ids, routing, last publish)
├── README.md               ← this file (dual doorway)
├── meat-suit-entry/        ← bone pilot / meat suit glitch hub
├── Docs/                   ← architecture, constitution, glossary (Grok + deep diggers)
├── weave/
│   ├── CARD-INDEX.md       ← auto-generated card catalog
│   ├── components/         ← locked Trinity YAML cards
│   ├── component-proposals/← provisional cards (still active law)
│   ├── host-weld/          ← compiled execution-safety law
│   └── trinity-partition-registry.yaml
└── scripts/eat_queue_core/ ← maintenance Python + harness CLI
```

## Grok integration

1. Attach **this repo** (`main`) in Grok Chat GitHub settings
2. Grok reads **committed files only** — no live vault
3. Route weave questions here; queue ops → `genesis-mythos-master-roadmap` (vestigial for project bridge)

## Excluded on purpose

`1-Projects/`, `Roadmap/`, `Ingest/`, `.cursor/`, runtime queues — factory and ops surfaces stay elsewhere. See `Docs/GROK-OBSERVABILITY.md`.

## Sync source

Auto-published from private vault via `weave_public_sync` / `schedule_tick` when weave files change. Authority: locked meta `trinity_weave_public_export`.

## Related repos

- [genesis-mythos-master-roadmap](https://github.com/L0RDTH0TH/genesis-mythos-master-roadmap) — queue/automation + engine Roadmaps
- Curator (private) — full vault backup
