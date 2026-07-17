# What is Trinity-Weave?

Trinity-Weave is the **public weave architecture** for this operator's Second Brain maintenance layer — YAML cards, harness scripts, and indexes that describe how the grammar works.

## One repo, two branch kinds

- **`main`** — weave **law** (locked + provisional component YAML)
- **`project/<project-id>`** — **instances** for one project (Roadmap, catalog, observability)

Never merge `project/*` into `main`.

## Grok uses this repo

Grok reads committed git on Trinity-Weave. Tertiary note bodies arrive only via **fulfill packs** the bone pilot approves.

See [[GROK-VS-BONE-PILOT|Grok vs bone pilot]] and `Docs/GROK-PROJECT-BRIDGE.md`.
