# Trinity-Weave

**Public weave design slice** for GitHub-linked [Grok](https://grok.com) and external readers.

| | |
|---|---|
| **What this is** | Maintenance grammar for an agentic Second Brain — YAML cards + Python harness |
| **What this is not** | Game code, project Roadmaps, live queue state, or the private vault |
| **Grok entry** | [`GROK-START-HERE.md`](GROK-START-HERE.md) → [`OBSERVABILITY.json`](OBSERVABILITY.json) |
| **Version** | `2026.06.09-light` (see `OBSERVABILITY.json`) |

## Quick start (humans)

```bash
git clone https://github.com/L0RDTH0TH/Trinity-Weave.git
cd Trinity-Weave
# Read-only context — no install required for Grok
cat GROK-START-HERE.md
cat OBSERVABILITY.json
```

To run harness locally you need the **private** vault checkout (not shipped here):

```bash
PYTHONPATH=scripts python3 -m scripts.eat_queue_core.harness --help
```

## Repository layout

```
Trinity-Weave/
├── GROK-START-HERE.md      ← Grok: read first
├── OBSERVABILITY.json      ← machine index (card ids, routing, last publish)
├── README.md               ← this file
├── Docs/                   ← architecture, constitution, glossary
├── weave/
│   ├── CARD-INDEX.md       ← auto-generated card catalog
│   ├── components/         ← locked Trinity YAML cards
│   ├── host-weld/          ← compiled execution-safety law
│   └── trinity-partition-registry.yaml
└── scripts/eat_queue_core/ ← maintenance Python + harness CLI
```

## Grok integration

1. Attach **this repo** (`main`) in Grok Chat GitHub settings
2. Grok reads **committed files only** — no live vault
3. Route weave questions here; queue ops → `genesis-mythos-master-roadmap`

## Excluded on purpose

`1-Projects/`, `Roadmap/`, `Ingest/`, `.cursor/`, runtime queues — factory and ops surfaces stay on other remotes. See `Docs/GROK-OBSERVABILITY.md`.

## Sync source

Auto-published from private vault via `weave_public_sync` / `schedule_tick` when weave files change. Authority: locked meta `trinity_weave_public_export`.

## Related repos

- [genesis-mythos-master-roadmap](https://github.com/L0RDTH0TH/genesis-mythos-master-roadmap) — queue/automation + engine Roadmaps
- Curator (private) — full vault backup
