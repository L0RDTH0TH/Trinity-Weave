# Trinity-Weave

**Public weave architecture** for GitHub-linked [Grok](https://grok.com) and meat-suit operators.

| | |
|---|---|
| **What this is** | Maintenance grammar — YAML cards + Python harness + host-weld law |
| **What this is not** | Live runtime state, game code, or unpublished local workspaces |
| **Grok entry** | [`GROK-START-HERE.md`](GROK-START-HERE.md) → [`OBSERVABILITY.json`](OBSERVABILITY.json) |
| **Meat suit entry** | [`meat-suit-entry/README.md`](meat-suit-entry/README.md) |
| **Version** | see `OBSERVABILITY.json` → `weave_core_version` |

## Who are you?

- **Grok / agent** → `GROK-START-HERE.md` → `OBSERVABILITY.json` → `weave/CARD-INDEX.md`
- **Meat suit glitch** / bone pilot (spinal interface · bio-mech · exo-flesh · organ suites · vein power lines · calcium frame) → `meat-suit-entry/README.md`

## Quick start (meat suit glitch)

```bash
git clone https://github.com/L0RDTH0TH/Trinity-Weave.git
cd Trinity-Weave
cat meat-suit-entry/README.md
cat GROK-START-HERE.md
cat OBSERVABILITY.json
```

## Repository layout

```
Trinity-Weave/
├── GROK-START-HERE.md      ← Grok: read first
├── OBSERVABILITY.json      ← machine index (card ids, routing, last publish)
├── README.md               ← this file (dual doorway)
├── meat-suit-entry/        ← bone pilot / meat suit glitch hub
├── Docs/                   ← architecture, constitution, glossary
├── weave/
│   ├── CARD-INDEX.md       ← auto-generated card catalog
│   ├── components/         ← locked Trinity YAML cards
│   ├── component-proposals/← provisional cards (active law; may evolve)
│   ├── host-weld/          ← compiled execution-safety law
│   └── trinity-partition-registry.yaml
└── scripts/eat_queue_core/ ← maintenance Python + harness CLI
```

## Branches

| Branch | Role |
|--------|------|
| `main` | Weave law — cards, harness, indexes, meat-suit entry |
| `project/<id>` | Project **instances** (Roadmap, catalog, observability) — never merge into `main` |

Pilot project branch: `project/genesis-mythos-master` (see `meat-suit-entry/PROJECT-BRANCH-LAYOUT.md`).

## Grok integration

1. Attach **this repo** in Grok Chat GitHub settings (`main` + optional `project/<id>`)
2. Ground answers in **committed** files only
3. Weave / gates → `main`; project instances → `project/<id>`; tertiary bodies → mediated fulfill packs

## Not in this repo

Live queues, unpublished workspaces, resolve maps, fulfill pack bodies. See `Docs/GROK-OBSERVABILITY.md`.
